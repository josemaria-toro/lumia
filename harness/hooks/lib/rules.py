"""Pure validation rules (no I/O) reused by agent hooks and git hooks."""
from __future__ import annotations

import re

CC_TYPES = "feat|fix|docs|refactor|perf|test|build|ci|chore|revert"
CC_RE = re.compile(rf"^(?:{CC_TYPES})(?:\([a-z0-9][a-z0-9._/-]*\))?!?: \S")
BRANCH_RE = re.compile(r"^(?:(?:bug|change|chore|feature|hotfix)/[a-z0-9]+(?:-[a-z0-9]+)*|release/v\d+\.\d+\.\d+)$")
TAG_RE = re.compile(r"^v\d+\.\d+\.\d+$")
NON_ENGLISH_RE = re.compile(r"[áéíóúüñÁÉÍÓÚÜÑ¿¡]")
AGENTS = r"claude|anthropic|copilot|codex|openai|chatgpt|gemini|cursor|aider|devin|windsurf"
ATTRIBUTION_RE = re.compile(
    rf"co-authored-by\s*:[^\n]*(?:{AGENTS})|generated\s+(?:with|by)[^\n]*(?:{AGENTS})|🤖|noreply@anthropic\.com",
    re.I,
)
SQL_NAME_RE = re.compile(r"^(\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\.sql$")

PLACEHOLDER_RE = re.compile(r"^(<.*>|\$\{?.*|\{.*\}|\*+|x+|changeme|password|secret|example.*|your.*|%s|.*placeholder.*)$", re.I)
SECRET_PATTERNS = [
    ("clave privada", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY")),
    ("clave de acceso AWS", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("token de GitHub", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b")),
    ("token de Slack", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("clave de API (sk-)", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{32,}")),
]
CONN_RE = re.compile(r"\b(?:postgres(?:ql)?|amqps?|mysql|mongodb(?:\+srv)?|redis)://([^/\s:@'\"]+):([^@\s'\"]+)@")


def check_conventional(text: str, what: str) -> list[str]:
    """Validates a commit subject / PR title: Conventional Commits, English, no agent attribution."""
    errors: list[str] = []
    subject = next((l for l in text.strip().splitlines() if l.strip() and not l.startswith("#")), "")
    if not CC_RE.match(subject):
        errors.append(f"{what} «{subject}» no sigue Conventional Commits (`type(scope): description`, tipos: {CC_TYPES.replace('|', ', ')}).")
    if NON_ENGLISH_RE.search(text):
        errors.append(f"{what} debe estar escrito en inglés.")
    if ATTRIBUTION_RE.search(text):
        errors.append(f"{what} contiene atribución a un agente de IA (prohibido).")
    return errors


def check_branch(name: str) -> list[str]:
    if BRANCH_RE.match(name):
        return []
    return [f"Nombre de rama «{name}» inválido. Formatos: bug|change|chore|feature|hotfix/short-description (minúsculas y guiones) o release/v<MAJOR.MINOR.PATCH>."]


def scan_secrets(text: str) -> list[str]:
    found = [label for label, rx in SECRET_PATTERNS if rx.search(text)]
    for m in CONN_RE.finditer(text):
        if not PLACEHOLDER_RE.match(m.group(2)):
            found.append("cadena de conexión con credenciales")
            break
    return found


def check_sql_name(basename: str) -> list[str]:
    if SQL_NAME_RE.match(basename):
        return []
    return [f"Los scripts SQL se llaman <yymmdd>.sql (fecha válida); «{basename}» no cumple. No se usan migraciones."]
