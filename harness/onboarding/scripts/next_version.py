#!/usr/bin/env python3
"""Computes the next release version (SemVer) from Conventional Commits merged into main.

Prints the version, or exits with code 3 when no release is justified.
The version is never stored in a file: it comes from the last `v<MAJOR.MINOR.PATCH>` tag.
"""
from __future__ import annotations

import re
import subprocess
import sys

TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
HEAD = re.compile(r"^(\w+)(?:\([^)]*\))?(!)?:")


def run(*a: str) -> str:
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout


def main() -> int:
    ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    tags = sorted((tuple(map(int, m.groups())) for t in run("tag", "--list", "v*").split() if (m := TAG.match(t))))
    last = tags[-1] if tags else None
    rng = f"v{'.'.join(map(str, last))}..{ref}" if last else ref
    bump = None
    for raw in run("log", "--first-parent", "--format=%B%x00", rng).split("\x00"):
        raw = raw.strip()
        if not raw:
            continue
        m = HEAD.match(raw.splitlines()[0])
        if not m:
            continue
        if m.group(2) or re.search(r"^BREAKING[ -]CHANGE:", raw, re.M):
            bump = "major"
        elif m.group(1) == "feat" and bump != "major":
            bump = "minor"
        elif m.group(1) == "fix" and bump is None:
            bump = "patch"
    if last is None:
        print("0.1.0")  # first release is always 0.1.0
        return 0
    if bump is None:
        return 3
    M, m_, p = last
    print({"major": f"{M + 1}.0.0", "minor": f"{M}.{m_ + 1}.0", "patch": f"{M}.{m_}.{p + 1}"}[bump])
    return 0


if __name__ == "__main__":
    sys.exit(main())
