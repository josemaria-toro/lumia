"""Guardrails for shell commands (git, gh, package managers, secrets, protected paths)."""
from __future__ import annotations

import os
import re
import shlex

from lib import common, rules
from lib.events import Event

SPLIT_RE = re.compile(r"&&|\|\||;|\n|(?<!\|)\|(?!\|)")
HEREDOC_RE = re.compile(r"(<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n).*?\n[ \t]*\2[ \t]*(?=\n|\)|$)", re.S)
VALUE = r"(\"(?:[^\"\\]|\\.)*\"|'[^']*'|[^\s\"']+)"
WRITE_VERBS = {"rm", "mv", "tee", "truncate", "chmod", "ln", "install", "rsync", "dd", "rmdir", "shred"}


def _tokens(seg: str) -> list[str]:
    try:
        return shlex.split(seg)
    except ValueError:
        return seg.split()


def _flag_values(cmd: str, flags: str) -> list[str]:
    out = []
    for m in re.finditer(rf"(?:(?<=\s)|^)(?:{flags})(?:\s+|=){VALUE}", cmd):
        v = m.group(1)
        out.append(v[1:-1] if v[:1] in "\"'" and v[-1:] == v[:1] else v)
    return out


def _commit_messages(cmd: str) -> list[str]:
    msgs = []
    for v in _flag_values(cmd, r"-[a-zA-Z]*m|--message"):
        if not v.startswith("$(") and not v.startswith("`"):
            msgs.append(v)
    for m in re.finditer(r"\$\(\s*cat\s*<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)\n[ \t]*\1[ \t]*(?=\n|\)|$)", cmd, re.S):
        msgs.append(m.group(2))
    return msgs


def _git_sub(toks: list[str]) -> tuple[str, list[str]]:
    i = 1
    while i < len(toks):
        t = toks[i]
        if t in ("-C", "-c", "--git-dir", "--work-tree", "--namespace"):
            i += 2
        elif t.startswith("-"):
            i += 1
        else:
            return t, toks[i + 1:]
    return "", []


def _positional(args: list[str]) -> list[str]:
    return [a for a in args if not a.startswith("-")]


# --------------------------------------------------------------------------- git
def _git(toks, cmd, cwd, state) -> list[str]:
    sub, args = _git_sub(toks)
    v: list[str] = []
    repo = common.is_repo(cwd)
    branch = common.current_branch(cwd) if repo else None
    on_main = repo and common.has_commits(cwd) and branch in common.MAIN_BRANCHES and not state["switched"]

    if sub == "commit":
        if "--no-verify" in args or "-n" in args:
            v.append("`git commit --no-verify` está prohibido: no se pueden saltar los hooks.")
        if on_main:
            v.append("Commit directo en 'main' prohibido. Crea una rama (bug|change|chore|feature|hotfix/short-description).")
        if repo and not all(common.local_identity(cwd)):
            v.append("Falta la identidad local de git (user.name/user.email). Ejecuta el onboarding o configúrala con `git config --local`.")
        for m in _commit_messages(cmd):
            v += rules.check_conventional(m, "El mensaje de commit")
    elif sub in ("checkout", "switch"):
        create = [a for a in args if a in ("-b", "-B", "-c", "-C")]
        if create:
            pos = _positional(args)
            if pos:
                v += rules.check_branch(pos[0])
        state["switched"] = True
    elif sub == "branch":
        if any(a in ("-d", "-D", "--delete") for a in args):
            for name in _positional(args):
                if name in common.MAIN_BRANCHES or name.startswith("release/"):
                    v.append(f"No se puede borrar la rama protegida «{name}».")
        elif not any(a.startswith("-") for a in args):
            pos = _positional(args)
            if pos:
                v += rules.check_branch(pos[0])
    elif sub == "push":
        flags = [a for a in args if a.startswith("-")]
        pos = _positional(args)
        refspecs = pos[1:]
        if any(f in ("-f", "--force", "--mirror") or f.startswith(("--force-with-lease", "--force-if-includes")) for f in flags) \
                or any(r.startswith("+") for r in refspecs):
            v.append("`git push --force` (y variantes) está prohibido.")
        deleting = any(f in ("-d", "--delete") for f in flags) or any(r.startswith(":") for r in refspecs)
        targets = [r.split(":")[-1].removeprefix("refs/heads/") for r in refspecs] if refspecs else ([branch] if branch else [])
        for t in targets:
            if deleting and (t in common.MAIN_BRANCHES or t.startswith("release/")):
                v.append(f"No se puede borrar la rama protegida «{t}».")
            elif t in common.MAIN_BRANCHES and common.is_onboarded() and not deleting:
                v.append("Push directo a 'main' prohibido: usa una rama y abre una pull request.")
    elif sub == "config":
        scope = any(a in ("--global", "--system") for a in args)
        readonly = any(a in ("--get", "--get-all", "--get-regexp", "--list", "-l") for a in args)
        if scope and not readonly:
            v.append("No se puede modificar la configuración global/system de git: usa `git config --local` (identidad local).")
    elif sub in ("merge", "rebase", "cherry-pick") and on_main:
        v.append("No se integran cambios localmente en 'main': usa una pull request con squash.")
    return v


# ---------------------------------------------------------------------------- gh
def _gh(toks, cmd) -> list[str]:
    v: list[str] = []
    a, b = (toks[1] if len(toks) > 1 else ""), (toks[2] if len(toks) > 2 else "")
    rest = toks[3:]
    if a == "auth" and (b == "token" or "--show-token" in rest or "-t" in rest):
        v.append("No se pueden mostrar tokens de `gh` (secretos).")
    if a == "pr" and b in ("create", "edit"):
        titles = _flag_values(cmd, r"--title|-t")
        if b == "create" and not titles:
            v.append("`gh pr create` requiere `--title` explícito con formato Conventional Commits.")
        for t in titles:
            v += rules.check_conventional(t, "El título de la PR")
        if rules.ATTRIBUTION_RE.search(cmd):
            v.append("La PR contiene atribución a un agente de IA (prohibido).")
        for base in _flag_values(cmd, r"--base|-B"):
            if b == "create" and base != "main" and not base.startswith("release/"):
                v.append("Las PRs se abren hacia 'main'.")
    elif a == "pr" and b == "merge":
        if not ({"--squash", "-s"} & set(rest)):
            v.append("Las PRs se integran **solo** con squash (`gh pr merge --squash`).")
        if {"--merge", "-m", "--rebase", "-r"} & set(rest):
            v.append("Merge commits y rebase merge están desactivados: solo squash.")
        if "--admin" in rest:
            v.append("`--admin` (saltarse las reglas de protección) está prohibido.")
        if {"--auto"} & set(rest):
            v.append("Auto-merge desactivado en el repositorio.")
        for t in _flag_values(cmd, r"--subject|-t"):
            v += rules.check_conventional(t, "El título del squash")
    elif a == "release" and b == "create":
        pos = _positional(rest)
        if pos and not rules.TAG_RE.match(pos[0]):
            v.append(f"El tag de release «{pos[0]}» debe tener formato v<MAJOR.MINOR.PATCH>.")
        for t in _flag_values(cmd, r"--target"):
            if not t.startswith("release/v"):
                v.append("Las releases se generan desde una rama release/v<version>.")
        if rules.ATTRIBUTION_RE.search(cmd):
            v.append("La release contiene atribución a un agente de IA (prohibido).")
    elif a == "repo" and b == "delete":
        v.append("`gh repo delete` está prohibido.")
    elif a == "secret" and b == "set" and ({"--body", "-b"} & set(rest) or any(r.startswith("--body=") for r in rest)):
        v.append("No pases secretos como argumento: `gh secret set NAME` los lee por stdin.")
    elif a == "api":
        method = next(iter(_flag_values(cmd, r"-X|--method")), "GET").upper()
        if method == "DELETE" and re.search(r"/rulesets|/protection", cmd):
            v.append("No se pueden borrar rulesets ni protecciones de rama.")
    return v


# ----------------------------------------------------------------------- generic
def _generic(toks, cmd, cwd, seg) -> list[str]:
    v: list[str] = []
    prog = os.path.basename(toks[0])
    if prog in ("apt", "apt-get", "dnf", "yum", "brew", "snap", "zypper", "pacman") and re.search(r"\bmono(-\w+)?\b", seg):
        v.append("Instalar mono está prohibido.")
    pip = prog in ("pip", "pip3") or (prog.startswith("python") and toks[1:3] == ["-m", "pip"])
    if pip and "install" in toks and not os.environ.get("VIRTUAL_ENV") and not re.search(r"activate", cmd):
        v.append("Los proyectos Python usan siempre entorno virtual: crea/activa `.venv` (o usa `.venv/bin/pip`). No instales paquetes globalmente.")
    if re.search(r"\balembic\b|dotnet\s+ef\s+migrations|makemigrations|prisma\s+migrate|flyway", seg):
        v.append("Las migraciones no están admitidas: genera un script <yymmdd>.sql.")
    if prog == "openspec" and (toks[1:2] == ["new"] or toks[1:3] == ["change", "new"]):
        pending = common.pending_openspec_changes()
        if pending:
            v.append(f"No se puede abrir otra especificación con cambios pendientes de archivar: {', '.join(pending)}.")
    return v


def _secrets_in_args(seg: str) -> list[str]:
    v = []
    if re.search(r"--(?:password|passwd|token|secret|api-key|apikey)(?:=|\s+)(?![\$\-<])\S{3,}", seg, re.I):
        v.append("No pases secretos como argumentos de línea de comandos (quedan en historial y lista de procesos): usa variables de entorno o ficheros de secretos.")
    for m in rules.CONN_RE.finditer(seg):
        if not rules.PLACEHOLDER_RE.match(m.group(2)):
            v.append("Cadena de conexión con credenciales en la línea de comandos.")
            break
    return v


def _protected_writes(toks, seg, cwd) -> list[str]:
    if not common.is_onboarded() or common.adr_authorizes_harness_change():
        return []
    prog = os.path.basename(toks[0])
    targets: list[str] = []
    if prog in WRITE_VERBS:
        targets = toks[1:]
    elif prog in ("cp", "install", "rsync") and len(toks) > 2:
        targets = [toks[-1]]
    elif prog in ("sed", "perl") and any(t.startswith("-i") or t == "--in-place" for t in toks):
        targets = toks[1:]
    elif prog == "git" and _git_sub(toks)[0] in ("rm", "mv", "checkout", "restore"):
        targets = toks[1:]
    targets += [m.group(1) for m in re.finditer(r"(?<![0-9&])>>?\s*(\S+)", seg)]
    if any(common.is_protected(common.relpath(t, cwd)) for t in targets if not t.startswith("-")):
        return ["El harness está protegido tras el onboarding: cualquier cambio requiere un ADR con `harness-change: true` en docs/adr/."]
    return []


def check(ev: Event) -> list[str]:
    cmd, cwd = ev.command, ev.cwd
    state = {"switched": False}
    v: list[str] = []
    for seg in (s.strip() for s in SPLIT_RE.split(HEREDOC_RE.sub(r"\1", cmd))):
        toks = _tokens(seg)
        while toks and (re.match(r"^\w+=", toks[0]) or toks[0] in ("sudo", "command", "env", "time")):
            toks = toks[1:]
        if not toks:
            continue
        prog = os.path.basename(toks[0])
        if prog == "git":
            v += _git(toks, cmd, cwd, state)
        elif prog == "gh":
            v += _gh(toks, cmd)
        v += _generic(toks, cmd, cwd, seg)
        v += _secrets_in_args(seg)
        v += _protected_writes(toks, seg, cwd)
    return list(dict.fromkeys(v))
