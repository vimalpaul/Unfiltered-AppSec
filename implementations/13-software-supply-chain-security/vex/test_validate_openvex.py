import copy
import hashlib
import unittest

from validate_openvex import release_gate, validate_document, CONTEXT


def sample(status="under_investigation"):
    statement = {
        "vulnerability": {"name": "CVE-2099-0001", "description": "Synthetic test vulnerability"},
        "products": [
            {
                "@id": "pkg:generic/demo-product@1.0.0",
                "hashes": {
                    "sha-256": hashlib.sha256(b"synthetic fixture artifact").hexdigest()
                },
            }
        ],
        "status": status,
    }
    if status == "not_affected":
        statement["justification"] = "vulnerable_code_not_in_execute_path"
    if status == "affected":
        statement["action_statement"] = "Upgrade the synthetic component in the test fixture."
    return {
        "@context": CONTEXT,
        "@id": "https://example.invalid/vex/synthetic-fixture",
        "author": "Unfiltered AppSec Test Fixture",
        "role": "Synthetic test only",
        "timestamp": "2026-11-20T10:00:00Z",
        "version": 1,
        "statements": [statement],
    }


class OpenVexTests(unittest.TestCase):
    def test_under_investigation_is_structurally_valid(self):
        self.assertEqual(validate_document(sample()), [])

    def test_not_affected_requires_justification_or_impact(self):
        doc = sample("not_affected")
        doc["statements"][0].pop("justification")
        self.assertTrue(any("requires a valid justification" in e for e in validate_document(doc)))

    def test_invalid_justification_rejected(self):
        doc = sample("not_affected")
        doc["statements"][0]["justification"] = "scanner_found_no_path"
        self.assertTrue(any("not a recognized" in e for e in validate_document(doc)))

    def test_affected_requires_action_statement(self):
        doc = sample("affected")
        doc["statements"][0].pop("action_statement")
        self.assertTrue(any("requires an action_statement" in e for e in validate_document(doc)))

    def test_invalid_timestamp_rejected(self):
        doc = sample()
        doc["timestamp"] = "not-a-date"
        self.assertTrue(any("RFC3339" in e for e in validate_document(doc)))

    def test_missing_product_identity_rejected(self):
        doc = sample()
        doc["statements"][0]["products"] = [{}]
        self.assertTrue(any("must contain @id" in e for e in validate_document(doc)))

    def test_release_gate_blocks_under_investigation(self):
        self.assertTrue(any("blocks release" in e for e in release_gate(sample())))

    def test_release_gate_blocks_affected(self):
        self.assertTrue(any("blocks release" in e for e in release_gate(sample("affected"))))

    def test_release_gate_allows_not_affected_with_hash_and_justification(self):
        self.assertEqual(release_gate(sample("not_affected")), [])

    def test_release_gate_requires_artifact_hash(self):
        doc = sample("fixed")
        doc["statements"][0]["products"][0].pop("hashes")
        self.assertTrue(any("requires an exact sha-256" in e for e in release_gate(doc)))

    def test_document_without_statements_rejected(self):
        doc = sample()
        doc["statements"] = []
        self.assertTrue(any("non-empty array" in e for e in validate_document(doc)))


if __name__ == "__main__":
    unittest.main()
