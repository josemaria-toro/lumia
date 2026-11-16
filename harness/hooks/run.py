#!/usr/bin/env python3
"""Single entry point for agent hooks: run.py <agent> <guard>.

  agent: claude
  guard: bash | file | session-start

Exit codes: 0 = allow, 2 = block (reason on stderr, shown to the agent).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from guards import files, session, shell  # noqa: E402
from lib import events  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) != 3 or argv[1] != "claude":
        print("uso: run.py claude <bash|file|session-start>", file=sys.stderr)
        return 1
    guard = argv[2]
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}
    ev = events.from_claude(guard, payload)
    if ev is None:
        return 0
    if ev.kind == "session_start":
        print(json.dumps(session.context(ev)))
        return 0
    violations = shell.check(ev) if ev.kind == "shell" else files.check(ev)
    if violations:
        print("🛑 Harness: acción bloqueada por los guardarraíles.\n" + "\n".join(f"- {v}" for v in violations), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
