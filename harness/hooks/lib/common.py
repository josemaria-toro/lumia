"""Git/onboarding helpers shared by every guardrail."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parents[2]
ROOT = HARNESS_DIR.parent
MARKER = HARNESS_DIR / ".onboarded"

# Paths that cannot change after onboarding without an ADR.
PROTECTED = ("harness/", ".claude/settings.json", ".claude/commands/onboarding.md", "CLAUDE.md", "AGENTS.md")
MAIN_BRANCHES = ("main", "master")


def git(args: list[str], cwd: str | Path | None = None) -> tuple[int, str]:
    try:
        p = subprocess.run(["git", *args], cwd=str(cwd or ROOT), capture_output=True, text=True, timeout=15)
        return p.returncode, p.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return 1, ""


def is_repo(cwd=None) -> bool:
    return git(["rev-parse", "--is-inside-work-tree"], cwd)[0] == 0


def has_commits(cwd=None) -> bool:
    return git(["rev-parse", "--verify", "-q", "HEAD"], cwd)[0] == 0


def commit_count(cwd=None) -> int:
    rc, out = git(["rev-list", "--count", "HEAD"], cwd)
    return int(out) if rc == 0 and out.isdigit() else 0


def current_branch(cwd=None) -> str | None:
    rc, out = git(["symbolic-ref", "--short", "-q", "HEAD"], cwd)
    return out if rc == 0 and out else None


def local_identity(cwd=None) -> tuple[str, str]:
    return (git(["config", "--local", "--get", "user.name"], cwd)[1],
            git(["config", "--local", "--get", "user.email"], cwd)[1])


def is_onboarded() -> bool:
    return MARKER.exists()


def onboarding_needed(cwd=None) -> bool:
    """Onboarding applies when not a git repo, or the repo only has the initial commit."""
    if is_onboarded():
        return False
    return (not is_repo(cwd)) or commit_count(cwd) <= 1


def relpath(path: str | Path, cwd: str | Path | None = None) -> str | None:
    """Path relative to the project root (posix), or None when outside it."""
    p = Path(path)
    if not p.is_absolute():
        p = Path(cwd or ROOT) / p
    try:
        return p.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return None


def is_protected(rel: str | None) -> bool:
    if rel is None:
        return False
    return any(rel == p or (p.endswith("/") and rel.startswith(p)) for p in PROTECTED)


def adr_authorizes_harness_change() -> bool:
    """True if an ADR flagged `harness-change: true` is new or modified in the working tree."""
    adr_dir = ROOT / "docs" / "adr"
    if not adr_dir.is_dir():
        return False
    flagged = [f for f in adr_dir.glob("*.md")
               if re.search(r"^harness-change:\s*true\s*$", f.read_text(errors="ignore")[:2000], re.M | re.I)]
    if not flagged:
        return False
    if not is_repo():
        return True
    _, out = git(["status", "--porcelain", "--", "docs/adr"])
    changed = {line[3:].strip() for line in out.splitlines()}
    return any(f.relative_to(ROOT).as_posix() in changed for f in flagged)


def pending_openspec_changes() -> list[str]:
    d = ROOT / "openspec" / "changes"
    if not d.is_dir():
        return []
    return sorted(p.name for p in d.iterdir() if p.is_dir() and p.name != "archive")
