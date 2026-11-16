"""SessionStart: injects the harness status into the agent context."""
from __future__ import annotations

from lib import common
from lib.events import Event


def context(ev: Event) -> dict:
    cwd = ev.cwd
    lines = ["[Harness] Las reglas están en harness/rules/ y los guardarraíles (hooks) están activos."]
    if common.onboarding_needed(cwd):
        lines.append("ONBOARDING PENDIENTE: el espacio de trabajo no está onboardeado. Antes de cualquier otra tarea, ejecuta el proceso descrito en harness/onboarding/README.md (comando /onboarding).")
    else:
        branch = common.current_branch(cwd)
        if branch:
            lines.append(f"Rama actual: {branch}.")
        pending = common.pending_openspec_changes()
        if pending:
            lines.append(f"Especificaciones OpenSpec sin archivar: {', '.join(pending)}. No se puede abrir otra hasta archivarlas.")
    return {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "\n".join(lines)}}
