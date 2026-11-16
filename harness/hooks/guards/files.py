"""Guardrails for file writes/edits (secrets, protected harness, SQL scripts, Python imports)."""
from __future__ import annotations

import re
from pathlib import Path

from lib import common, rules
from lib.events import Event

SENSITIVE_EXT = (".pem", ".key", ".pfx", ".p12", ".snk", ".jks")
SKIP_PARTS = {"node_modules", ".venv", "venv", ".git", "site-packages"}


def _is_env_secret(name: str) -> bool:
    return name == ".env" or (name.startswith(".env.") and not name.endswith((".example", ".sample", ".template")))


def _top_package(path: Path) -> str | None:
    pkg = None
    for parent in path.parents:
        if (parent / "__init__.py").exists() or parent == path.parent:
            pkg = parent.name
        else:
            break
    return pkg


def check(ev: Event) -> list[str]:
    v: list[str] = []
    path = Path(ev.path if Path(ev.path).is_absolute() else Path(ev.cwd or common.ROOT) / ev.path)
    rel = common.relpath(path)
    name = path.name
    new_text = "\n".join(new for _, new in ev.edits)

    if common.is_onboarded() and common.is_protected(rel) and not common.adr_authorizes_harness_change():
        v.append(f"«{rel}» pertenece al harness, protegido tras el onboarding: cualquier cambio requiere un ADR con `harness-change: true` en docs/adr/.")

    if _is_env_secret(name) or name.lower().endswith(SENSITIVE_EXT):
        v.append(f"No se crean ficheros de secretos/claves en el repositorio («{name}»). Usa variables de entorno o un gestor de secretos y un `.env.example` sin valores reales.")

    if rel and "harness/templates" not in rel:
        found = rules.scan_secrets(new_text)
        if found:
            v.append(f"El contenido incluye posibles secretos ({', '.join(found)}). Usa variables de entorno / gestor de secretos.")

    if not SKIP_PARTS & set(path.parts):
        parts = {p.lower() for p in path.parts}
        if "migrations" in parts or name == "alembic.ini":
            v.append("Las migraciones no están admitidas: genera un script <yymmdd>.sql.")
        if name.endswith(".sql") and "tests" not in parts and "test" not in parts:
            v += rules.check_sql_name(name)
            exists = path.exists()
            for old, new in ev.edits:
                if old is None and exists:
                    v.append("Un script <yymmdd>.sql existente no se sobrescribe: añade los cambios al final con ALTER.")
                elif old is not None and exists:
                    body = path.read_text(errors="ignore").rstrip()
                    if not (new.startswith(old) and body.endswith(old.rstrip())
                            and re.search(r"\bALTER\b", new[len(old):], re.I)):
                        v.append("En un script <yymmdd>.sql existente solo se pueden añadir cambios al final con ALTER; lo ya definido no se modifica.")
        if name.endswith(".py"):
            if name == "__init__.py":
                top = _top_package(path)
                if top and re.search(rf"^\s*(?:from|import)\s+{re.escape(top)}\b", new_text, re.M):
                    v.append("En `__init__.py` las importaciones internas usan rutas relativas (`from .module import X`).")
            elif re.search(r"^\s*from\s+\.", new_text, re.M):
                v.append("Fuera de `__init__.py` las importaciones usan rutas absolutas, no relativas.")
    return list(dict.fromkeys(v))
