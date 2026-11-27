#!/usr/bin/env python3
"""Read-only branch protection and CODEOWNERS auditor for Chapter 13 Lab 02."""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
POLICY_PATH = ROOT / "policy.json"
OWNER = re.compile(r"^@[A-Za-z0-9-]+(?:/[A-Za-z0-9_.-]+)?$")


class AuditError(ValueError):
    """Input or API evidence cannot be safely evaluated."""


def load_policy(path: Path = POLICY_PATH) -> dict[str, Any]:
    policy = json.loads(path.read_text(encoding="utf-8"))
    required = {"schema_version", "policy_id", "minimum_approving_reviews", "dismiss_stale_reviews",
                "require_code_owner_reviews", "require_strict_status_checks", "require_admin_enforcement",
                "allow_bypass_actors", "allow_force_pushes", "allow_deletions", "codeowners_locations", "sensitive_paths"}
    if set(policy) != required:
        raise AuditError("policy.json fields do not match the supported contract")
    if policy["schema_version"] != "1.0" or not isinstance(policy["minimum_approving_reviews"], int) or policy["minimum_approving_reviews"] < 1:
        raise AuditError("unsupported policy version or approval threshold")
    if not isinstance(policy["sensitive_paths"], list) or not policy["sensitive_paths"]:
        raise AuditError("policy must define sensitive paths")
    return policy


def finding(items: list[dict[str, str]], code: str, message: str) -> None:
    items.append({"code": code, "message": message})


def enabled(value: Any) -> bool | None:
    return value.get("enabled") if isinstance(value, dict) and isinstance(value.get("enabled"), bool) else None


def evaluate_protection(protection: Any, policy: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not isinstance(protection, dict):
        finding(findings, "BRANCH_PROTECTION_MISSING", "Branch protection evidence is missing or not an object.")
        return findings
    reviews = protection.get("required_pull_request_reviews")
    if not isinstance(reviews, dict):
        finding(findings, "PULL_REQUEST_REVIEW_POLICY_MISSING", "Required pull-request review policy is not configured.")
    else:
        count = reviews.get("required_approving_review_count")
        if not isinstance(count, int) or count < policy["minimum_approving_reviews"]:
            finding(findings, "APPROVAL_THRESHOLD_LOW", "Required approving-review count is below policy.")
        if policy["dismiss_stale_reviews"] and reviews.get("dismiss_stale_reviews") is not True:
            finding(findings, "STALE_APPROVALS_NOT_DISMISSED", "Dismissal of stale approvals is not explicitly enabled.")
        if policy["require_code_owner_reviews"] and reviews.get("require_code_owner_reviews") is not True:
            finding(findings, "CODEOWNER_REVIEW_NOT_REQUIRED", "Code-owner review is not explicitly required.")
        bypass = reviews.get("bypass_pull_request_allowances")
        if not isinstance(bypass, dict):
            finding(findings, "BYPASS_ALLOWANCE_UNKNOWN", "Pull-request bypass allowances are absent or not inspectable.")
        else:
            actors = 0
            for kind in ("users", "teams", "apps"):
                entries = bypass.get(kind, [])
                if not isinstance(entries, list):
                    finding(findings, "BYPASS_ALLOWANCE_INVALID", f"Bypass field {kind} is not an array.")
                else:
                    actors += len(entries)
            if actors and not policy["allow_bypass_actors"]:
                finding(findings, "BYPASS_ACTORS_CONFIGURED", f"{actors} pull-request bypass actor(s) are configured.")
    checks = protection.get("required_status_checks")
    if not isinstance(checks, dict):
        finding(findings, "STATUS_CHECKS_MISSING", "Required status checks are not configured.")
    else:
        contexts = checks.get("contexts")
        named = checks.get("checks")
        names = [x for x in contexts if isinstance(x, str) and x.strip()] if isinstance(contexts, list) else []
        if isinstance(named, list):
            names.extend(x.get("context") for x in named if isinstance(x, dict) and isinstance(x.get("context"), str) and x["context"].strip())
        if not names:
            finding(findings, "STATUS_CHECKS_EMPTY", "No required status-check contexts are configured.")
        if policy["require_strict_status_checks"] and checks.get("strict") is not True:
            finding(findings, "STATUS_CHECKS_NOT_STRICT", "Status checks do not require the branch to be up to date.")
    if policy["require_admin_enforcement"] and enabled(protection.get("enforce_admins")) is not True:
        finding(findings, "ADMIN_ENFORCEMENT_DISABLED", "Administrator enforcement is not explicitly enabled.")
    if not policy["allow_force_pushes"] and enabled(protection.get("allow_force_pushes")) is not False:
        finding(findings, "FORCE_PUSH_POLICY_UNKNOWN_OR_ENABLED", "Force pushes are enabled or their disabled state is not explicit.")
    if not policy["allow_deletions"] and enabled(protection.get("allow_deletions")) is not False:
        finding(findings, "BRANCH_DELETION_POLICY_UNKNOWN_OR_ENABLED", "Branch deletion is enabled or its disabled state is not explicit.")
    return findings


def glob_regex(pattern: str) -> re.Pattern[str]:
    anchored = pattern.startswith("/")
    if anchored:
        pattern = pattern[1:]
    has_slash = "/" in pattern
    output, i = [], 0
    while i < len(pattern):
        char = pattern[i]
        if char == "*":
            if i + 1 < len(pattern) and pattern[i + 1] == "*":
                i += 1
                if i + 1 < len(pattern) and pattern[i + 1] == "/":
                    output.append("(?:.*/)?")
                    i += 1
                else:
                    output.append(".*")
            else:
                output.append("[^/]*")
        elif char == "?":
            output.append("[^/]")
        else:
            output.append(re.escape(char))
        i += 1
    body = "".join(output)
    if not anchored and not has_slash:
        body = "(?:.*/)?" + body
    return re.compile("^" + body + "$")


def parse_codeowners(text: str) -> list[dict[str, Any]]:
    rules = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            raise AuditError(f"CODEOWNERS line {number} has no owner")
        pattern, owners = parts[0], parts[1:]
        if pattern.startswith("!") or not all(OWNER.fullmatch(owner) for owner in owners):
            raise AuditError(f"CODEOWNERS line {number} has unsupported pattern or invalid owner")
        rules.append({"line": number, "pattern": pattern, "owners": owners, "regex": glob_regex(pattern)})
    if not rules:
        raise AuditError("CODEOWNERS has no usable ownership rules")
    return rules


def owners_for_path(path: str, rules: list[dict[str, Any]]) -> list[str]:
    owners: list[str] = []
    for rule in rules:
        if rule["regex"].match(path):
            owners = rule["owners"]
    return owners


def evaluate_codeowners(text: Any, policy: dict[str, Any]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    findings: list[dict[str, str]] = []
    if not isinstance(text, str) or not text.strip():
        finding(findings, "CODEOWNERS_MISSING", "No non-empty CODEOWNERS file was supplied.")
        return findings, {"covered_paths": [], "uncovered_paths": list(policy["sensitive_paths"]), "rule_count": 0}
    try:
        rules = parse_codeowners(text)
    except AuditError as exc:
        finding(findings, "CODEOWNERS_INVALID", str(exc))
        return findings, {"covered_paths": [], "uncovered_paths": list(policy["sensitive_paths"]), "rule_count": 0}
    covered, uncovered = [], []
    for path in policy["sensitive_paths"]:
        owners = owners_for_path(path, rules)
        if owners:
            covered.append({"path": path, "owners": owners})
        else:
            uncovered.append(path)
    if uncovered:
        finding(findings, "SENSITIVE_PATHS_UNOWNED", "Sensitive paths have no effective CODEOWNERS rule: " + ", ".join(uncovered))
    return findings, {"covered_paths": covered, "uncovered_paths": uncovered, "rule_count": len(rules)}


def evaluate_document(document: Any, policy: dict[str, Any]) -> dict[str, Any]:
    required = {"repository", "branch", "branch_protection", "codeowners_path", "codeowners_text"}
    if not isinstance(document, dict) or not required.issubset(document) or set(document) - (required | {"audit_mode"}):
        raise AuditError("audit input has missing or unsupported fields")
    if not isinstance(document["repository"], str) or not re.fullmatch(r"[^/]+/[^/]+", document["repository"]):
        raise AuditError("repository must use owner/name format")
    if not isinstance(document["branch"], str) or not document["branch"].strip():
        raise AuditError("branch must be non-empty")
    findings = evaluate_protection(document["branch_protection"], policy)
    owner_findings, ownership = evaluate_codeowners(document["codeowners_text"], policy)
    findings.extend(owner_findings)
    text = document["codeowners_text"]
    protection = document["branch_protection"]
    reviews = protection.get("required_pull_request_reviews") if isinstance(protection, dict) else None
    return {
        "schema_version": "1.0", "policy_id": policy["policy_id"],
        "audit_mode": document.get("audit_mode", "offline-fixture"),
        "repository": document["repository"], "branch": document["branch"],
        "codeowners_path": document["codeowners_path"],
        "codeowners_sha256": hashlib.sha256(text.encode()).hexdigest() if isinstance(text, str) else None,
        "branch_protection": {
            "required_approving_review_count": reviews.get("required_approving_review_count") if isinstance(reviews, dict) else None,
            "dismiss_stale_reviews": reviews.get("dismiss_stale_reviews") if isinstance(reviews, dict) else None,
            "require_code_owner_reviews": reviews.get("require_code_owner_reviews") if isinstance(reviews, dict) else None,
            "required_status_checks": protection.get("required_status_checks") if isinstance(protection, dict) else None,
            "enforce_admins": enabled(protection.get("enforce_admins")) if isinstance(protection, dict) else None,
            "allow_force_pushes": enabled(protection.get("allow_force_pushes")) if isinstance(protection, dict) else None,
            "allow_deletions": enabled(protection.get("allow_deletions")) if isinstance(protection, dict) else None
        },
        "codeowners": ownership, "findings": findings,
        "decision": "PASS" if not findings else "FAIL",
        "manual_enforcement_tests_required": True,
        "limitations": [
            "Configuration audit only; direct-push, force-push, deletion and bypass attempts are not executed.",
            "Classic branch protection endpoint only; repository and organization rulesets are not evaluated.",
            "CODEOWNERS matching implements the constrained glob subset used by this lab.",
            "Reviewer independence and team membership are not verified."
        ]
    }


def gh_api(endpoint: str) -> tuple[int, Any]:
    result = subprocess.run(["gh", "api", "-H", "X-GitHub-Api-Version: 2022-11-28", endpoint],
                            capture_output=True, text=True, check=False)
    if result.returncode == 0:
        try:
            return 200, json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise AuditError(f"GitHub API returned invalid JSON for {endpoint}") from exc
    error = result.stderr.strip()
    if "HTTP 404" in error or "Not Found" in error:
        return 404, None
    raise AuditError(f"GitHub API request failed for {endpoint}: {error or 'gh api failed'}")


def live_document(repository: str, branch: str, policy: dict[str, Any]) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        raise AuditError("repository must use owner/name format")
    if not os.environ.get("GH_TOKEN") and not os.environ.get("GITHUB_TOKEN"):
        auth = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, check=False)
        if auth.returncode:
            raise AuditError("GitHub CLI is not authenticated; run gh auth login first")
    ref = quote(branch, safe="")
    status, protection = gh_api(f"repos/{repository}/branches/{ref}/protection")
    if status == 404:
        protection = None
    path, content = None, None
    for candidate in policy["codeowners_locations"]:
        code, payload = gh_api(f"repos/{repository}/contents/{quote(candidate, safe='/')}?ref={ref}")
        if code == 404:
            continue
        if not isinstance(payload, dict) or payload.get("type") != "file" or not isinstance(payload.get("content"), str):
            raise AuditError(f"{candidate} is not a regular file or has no content")
        try:
            content = base64.b64decode(payload["content"]).decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise AuditError(f"{candidate} is not valid base64 UTF-8") from exc
        path = candidate
        break
    return {"repository": repository, "branch": branch, "branch_protection": protection,
            "codeowners_path": path, "codeowners_text": content, "audit_mode": "live-read-only"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fixture", type=Path)
    group.add_argument("--repo", help="live GitHub owner/name (GET-only)")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--policy", type=Path, default=POLICY_PATH)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        policy = load_policy(args.policy)
        document = json.loads(args.fixture.read_text(encoding="utf-8")) if args.fixture else live_document(args.repo, args.branch, policy)
        report = evaluate_document(document, policy)
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0 if report["decision"] == "PASS" else 2
    except (OSError, json.JSONDecodeError, AuditError) as exc:
        print(json.dumps({"decision": "ERROR", "error": str(exc)}, indent=2), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
