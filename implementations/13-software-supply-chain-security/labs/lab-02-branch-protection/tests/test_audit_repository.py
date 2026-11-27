import copy
import hashlib
import json
import unittest
from pathlib import Path
from audit_repository import AuditError, evaluate_codeowners, evaluate_document, evaluate_protection, load_policy, owners_for_path, parse_codeowners

ROOT = Path(__file__).parents[1]
POLICY = load_policy()
FIXTURE = json.loads((ROOT / "fixtures/healthy-repository.json").read_text(encoding="utf-8"))
CODEOWNERS = (ROOT / "fixtures/codeowners.healthy").read_text(encoding="utf-8")


class ProtectionTests(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(FIXTURE["branch_protection"])

    def codes(self):
        return {x["code"] for x in evaluate_protection(self.data, POLICY)}

    def test_healthy_protection(self):
        self.assertEqual(self.codes(), set())

    def test_missing_protection(self):
        self.assertIn("BRANCH_PROTECTION_MISSING", {x["code"] for x in evaluate_protection(None, POLICY)})

    def test_missing_review_policy(self):
        self.data["required_pull_request_reviews"] = None
        self.assertIn("PULL_REQUEST_REVIEW_POLICY_MISSING", self.codes())

    def test_one_approval(self):
        self.data["required_pull_request_reviews"]["required_approving_review_count"] = 1
        self.assertIn("APPROVAL_THRESHOLD_LOW", self.codes())

    def test_stale_approval_dismissal(self):
        self.data["required_pull_request_reviews"]["dismiss_stale_reviews"] = False
        self.assertIn("STALE_APPROVALS_NOT_DISMISSED", self.codes())

    def test_code_owner_review_requirement(self):
        self.data["required_pull_request_reviews"]["require_code_owner_reviews"] = False
        self.assertIn("CODEOWNER_REVIEW_NOT_REQUIRED", self.codes())

    def test_missing_bypass_allowance_evidence(self):
        self.data["required_pull_request_reviews"].pop("bypass_pull_request_allowances")
        self.assertIn("BYPASS_ALLOWANCE_UNKNOWN", self.codes())

    def test_configured_bypass_actor(self):
        self.data["required_pull_request_reviews"]["bypass_pull_request_allowances"]["teams"] = ["release-admins"]
        self.assertIn("BYPASS_ACTORS_CONFIGURED", self.codes())

    def test_missing_status_checks(self):
        self.data["required_status_checks"] = None
        self.assertIn("STATUS_CHECKS_MISSING", self.codes())

    def test_empty_status_checks(self):
        self.data["required_status_checks"]["contexts"] = []
        self.assertIn("STATUS_CHECKS_EMPTY", self.codes())

    def test_non_strict_status_checks(self):
        self.data["required_status_checks"]["strict"] = False
        self.assertIn("STATUS_CHECKS_NOT_STRICT", self.codes())

    def test_admin_enforcement(self):
        self.data["enforce_admins"]["enabled"] = False
        self.assertIn("ADMIN_ENFORCEMENT_DISABLED", self.codes())

    def test_force_push_allowed(self):
        self.data["allow_force_pushes"]["enabled"] = True
        self.assertIn("FORCE_PUSH_POLICY_UNKNOWN_OR_ENABLED", self.codes())

    def test_force_push_setting_missing(self):
        self.data.pop("allow_force_pushes")
        self.assertIn("FORCE_PUSH_POLICY_UNKNOWN_OR_ENABLED", self.codes())

    def test_branch_deletion_allowed(self):
        self.data["allow_deletions"]["enabled"] = True
        self.assertIn("BRANCH_DELETION_POLICY_UNKNOWN_OR_ENABLED", self.codes())


class CodeownersTests(unittest.TestCase):
    def test_fixture_covers_sensitive_paths(self):
        findings, result = evaluate_codeowners(CODEOWNERS, POLICY)
        self.assertEqual(findings, [])
        self.assertEqual(result["uncovered_paths"], [])
        self.assertEqual(len(result["covered_paths"]), len(POLICY["sensitive_paths"]))

    def test_missing_codeowners(self):
        findings, _ = evaluate_codeowners(None, POLICY)
        self.assertIn("CODEOWNERS_MISSING", {x["code"] for x in findings})

    def test_empty_codeowners(self):
        findings, _ = evaluate_codeowners("# comments only\n", POLICY)
        self.assertIn("CODEOWNERS_INVALID", {x["code"] for x in findings})

    def test_sensitive_path_without_owner(self):
        findings, result = evaluate_codeowners("/.github/workflows/** @northstar/platform-engineering\n/release/** @northstar/release-engineering\n", POLICY)
        self.assertIn("SENSITIVE_PATHS_UNOWNED", {x["code"] for x in findings})
        self.assertIn("package-lock.json", result["uncovered_paths"])

    def test_last_matching_rule_wins(self):
        rules = parse_codeowners("/release/** @northstar/release-engineering\n/release/manifest.json @northstar/platform-engineering\n")
        self.assertEqual(owners_for_path("release/manifest.json", rules), ["@northstar/platform-engineering"])

    def test_ownerless_rule_rejected(self):
        with self.assertRaises(AuditError):
            parse_codeowners("/release/**\n")

    def test_invalid_owner_rejected(self):
        with self.assertRaises(AuditError):
            parse_codeowners("/release/** not-an-owner")

    def test_email_owner_is_rejected(self):
        with self.assertRaises(AuditError):
            parse_codeowners("/release/** reviewer@example.invalid")

    def test_globstar_and_root_patterns(self):
        rules = parse_codeowners("/.github/workflows/** @northstar/security-engineering\n/package-lock.json @northstar/application-security\n")
        self.assertEqual(owners_for_path(".github/workflows/nested/ci.yml", rules), ["@northstar/security-engineering"])
        self.assertEqual(owners_for_path("package-lock.json", rules), ["@northstar/application-security"])


class ReportTests(unittest.TestCase):
    def test_healthy_fixture_passes_but_requires_manual_tests(self):
        report = evaluate_document(FIXTURE, POLICY)
        self.assertEqual(report["decision"], "PASS")
        self.assertTrue(report["manual_enforcement_tests_required"])
        self.assertEqual(report["audit_mode"], "offline-fixture")

    def test_missing_document_field_rejected(self):
        doc = copy.deepcopy(FIXTURE)
        doc.pop("codeowners_text")
        with self.assertRaises(AuditError):
            evaluate_document(doc, POLICY)

    def test_codeowners_digest_bound(self):
        report = evaluate_document(FIXTURE, POLICY)
        self.assertEqual(report["codeowners_sha256"], hashlib.sha256(FIXTURE["codeowners_text"].encode()).hexdigest())

    def test_config_pass_does_not_claim_enforcement_pass(self):
        report = evaluate_document(FIXTURE, POLICY)
        self.assertTrue(any("Configuration audit only" in x for x in report["limitations"]))


if __name__ == "__main__":
    unittest.main()
