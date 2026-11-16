#!/usr/bin/env python3
"""Configures a GitHub repository (settings + rulesets) according to the harness, using `gh`.

Usage:
  github_setup.py settings  OWNER/REPO
  github_setup.py rulesets  OWNER/REPO --types python,csharp,react
  github_setup.py codeql    OWNER/REPO

Prints OK / WARN / MANUAL for each item; never prints tokens.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys


def gh_api(method: str, path: str, body: dict | None = None) -> tuple[bool, str]:
    cmd = ["gh", "api", "-X", method, path]
    if body is not None:
        cmd += ["--input", "-"]
    p = subprocess.run(cmd, input=json.dumps(body) if body is not None else None, capture_output=True, text=True)
    return p.returncode == 0, (p.stdout if p.returncode == 0 else p.stderr).strip()


def report(status: str, what: str, detail: str = "") -> None:
    print(f"[{status:6}] {what}" + (f" — {detail.splitlines()[0][:160]}" if detail else ""))


MANUAL = [
    "Features > Sponsorships: off",
    "Features > Preserve this repository: off",
    "Features > Issues/Pull requests permissions: Collaborators only",
    "Commits > Allow comments on individual commits: on",
    "Archives > Include Git LFS objects in archives: off",
    "Pushes > Limit how many branches and tags can be updated in a single push: off",
    "Issues > Auto-close issues with merged linked pull requests: on",
    "Dependabot version updates: on (se activa con .github/dependabot.yml)",
]


def settings(repo: str) -> None:
    body = {
        "is_template": False, "has_wiki": False, "has_issues": True, "has_projects": False, "has_discussions": False,
        "allow_merge_commit": False, "allow_squash_merge": True, "allow_rebase_merge": False,
        "squash_merge_commit_title": "PR_TITLE", "squash_merge_commit_message": "BLANK",
        "allow_update_branch": True, "allow_auto_merge": False, "delete_branch_on_merge": True,
        "web_commit_signoff_required": True,
        "security_and_analysis": {
            "secret_scanning": {"status": "enabled"},
            "secret_scanning_push_protection": {"status": "enabled"},
        },
    }
    ok, out = gh_api("PATCH", f"/repos/{repo}", body)
    report("OK" if ok else "WARN", "General / Features / Pull Requests / Commits / Secret scanning + push protection", "" if ok else out)
    for label, method, path in [
        ("Dependency graph + Dependabot alerts", "PUT", f"/repos/{repo}/vulnerability-alerts"),
        ("Dependabot security updates", "PUT", f"/repos/{repo}/automated-security-fixes"),
        ("Release immutability", "PUT", f"/repos/{repo}/immutable-releases"),
    ]:
        ok, out = gh_api(method, path)
        report("OK" if ok else "WARN", label, "" if ok else out)
    for m in MANUAL:
        report("MANUAL", m)


def main_ruleset(types: set[str]) -> dict:
    checks = ["quality", "unit-tests", "pr-title"]
    if types & {"python", "csharp"}:  # backend present
        checks.append("integration-tests")
    return {
        "name": "Protect main", "target": "branch", "enforcement": "active",
        "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}],
        "conditions": {"ref_name": {"include": ["refs/heads/main"], "exclude": []}},
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {"type": "required_linear_history"},
            {"type": "pull_request", "parameters": {
                "required_approving_review_count": 1, "dismiss_stale_reviews_on_push": True,
                "require_code_owner_review": False, "require_last_push_approval": True,
                "required_review_thread_resolution": True, "allowed_merge_methods": ["squash"]}},
            {"type": "code_scanning", "parameters": {"code_scanning_tools": [
                {"tool": "CodeQL", "security_alerts_threshold": "high_or_higher", "alerts_threshold": "errors"}]}},
            {"type": "code_quality", "parameters": {"severity": "errors"}},
            {"type": "required_status_checks", "parameters": {
                "strict_required_status_checks_policy": False,
                "required_status_checks": [{"context": c} for c in checks]}},
        ],
    }


def release_ruleset() -> dict:
    return {
        "name": "Protect releases", "target": "branch", "enforcement": "active",
        "bypass_actors": [{"actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "always"}],
        "conditions": {"ref_name": {"include": ["refs/heads/release/v*"], "exclude": []}},
        "rules": [{"type": "deletion"}, {"type": "update"}, {"type": "non_fast_forward"}],
    }


def rulesets(repo: str, types: set[str]) -> None:
    ok, out = gh_api("GET", f"/repos/{repo}/rulesets")
    existing = {r["name"]: r["id"] for r in json.loads(out)} if ok else {}
    for rs in (main_ruleset(types), release_ruleset()):
        def push(body: dict) -> tuple[bool, str]:
            rid = existing.get(body["name"])
            return gh_api("PUT", f"/repos/{repo}/rulesets/{rid}", body) if rid else gh_api("POST", f"/repos/{repo}/rulesets", body)
        ok, out = push(rs)
        if not ok and any(r["type"] == "code_quality" for r in rs["rules"]):
            rs["rules"] = [r for r in rs["rules"] if r["type"] != "code_quality"]
            ok, out = push(rs)
            if ok:
                report("MANUAL", f"Ruleset «{rs['name']}»: regla «code quality» (severidad: errors) no admitida por la API; actívala en la UI")
        report("OK" if ok else "WARN", f"Ruleset «{rs['name']}»", "" if ok else out)


def codeql(repo: str) -> None:
    ok, out = gh_api("PATCH", f"/repos/{repo}/code-scanning/default-setup", {"state": "configured", "query_suite": "default"})
    report("OK" if ok else "WARN", "CodeQL default setup", "" if ok else out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["settings", "rulesets", "codeql"])
    ap.add_argument("repo")
    ap.add_argument("--types", default="", help="comma-separated: python,csharp,react")
    a = ap.parse_args()
    {"settings": lambda: settings(a.repo), "rulesets": lambda: rulesets(a.repo, set(filter(None, a.types.split(",")))),
     "codeql": lambda: codeql(a.repo)}[a.action]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
