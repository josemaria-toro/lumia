"""Normalises each agent's hook payload into a tool-agnostic Event.

To support a new agent, add a `from_<agent>` function here and a branch in run.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Event:
    kind: str                      # "shell" | "write" | "session_start"
    cwd: str | None = None
    command: str = ""              # kind == "shell"
    path: str = ""                 # kind == "write"
    edits: list[tuple[str | None, str]] = field(default_factory=list)  # (old, new); old None = full content


def from_claude(guard: str, payload: dict) -> Event | None:
    cwd = payload.get("cwd")
    ti = payload.get("tool_input") or {}
    if guard == "session-start":
        return Event("session_start", cwd)
    if guard == "bash":
        return Event("shell", cwd, command=ti.get("command", ""))
    if guard == "file":
        tool = payload.get("tool_name", "")
        path = ti.get("file_path") or ti.get("notebook_path") or ""
        if tool == "Write":
            edits = [(None, ti.get("content", ""))]
        elif tool == "MultiEdit":
            edits = [(e.get("old_string", ""), e.get("new_string", "")) for e in ti.get("edits", [])]
        elif tool == "NotebookEdit":
            edits = [(None, ti.get("new_source", ""))]
        else:
            edits = [(ti.get("old_string", ""), ti.get("new_string", ""))]
        return Event("write", cwd, path=path, edits=edits)
    return None
