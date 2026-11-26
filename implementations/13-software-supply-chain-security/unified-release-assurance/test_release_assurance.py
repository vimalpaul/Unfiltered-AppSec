"""Unit tests for the unified release-assurance policy validator."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from release_assurance import PolicyError, validate_manifest


REVISION = "a" * 40
REPOSITORY = "vimalpaul/Unfiltered-AppSec"
REF = "refs/heads/main"
WORKFLOW = ".github/workflows/unified-release-assurance.yml"
SIGNER = "vimalpaul/Unfiltered-AppSec/.github/workflows/slsa-build-provenance.yml"
COSIGN_IDENTITY = "https://github.com/vimalpaul/Unfiltered-AppSec/.github/workflows/unified-release-assurance.yml@refs/heads/main"
ISSUER = "https://token.actions.githubusercontent.com"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReleaseAssuranceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.artifact = self.root / "release.tar.gz"
        self.artifact.write_bytes(b"synthetic release fixture")
        self.evidence_root = self.root / "evidence"
        self.evidence_root.mkdir()
        self.files = {}
        for name, content in {
            "sbom.json": b'{"bomFormat":"CycloneDX","specVersion":"1.7"}',
            "sca.json": b'{"status":"not_run_no_package_records"}',
            "slsa.json": b'{"verified":true}',
            "cosign.json": b'{"verificationMaterial":true}',
        }.items():
            path = self.evidence_root / name
            path.write_bytes(content)
            self.files[name] = path

        artifact_digest = digest(self.artifact)
        sbom_digest = digest(self.files["sbom.json"])
        common = {"run_id": "123456", "run_attempt": "1"}
        self.manifest = {
            "schema_version": 1,
            "release_id": "synthetic-123456-1",
            "release_classification": "synthetic-training-fixture",
            "created_at": "2026-11-26T12:00:00Z",
            "run_id": "123456",
            "run_attempt": "1",
            "source": {"repository": REPOSITORY, "ref": REF, "revision": REVISION, "workflow": WORKFLOW},
            "artifact": {"name": self.artifact.name, "sha256": artifact_digest,
                         "kind": "synthetic-training-fixture"},
            "evidence": {
                "sbom": {"status": "verified", "path": "sbom.json", "sha256": sbom_digest,
                         "subject_sha256": artifact_digest, "generation_scope": "extracted-release-artifact",
                         "format": "CycloneDX 1.7", "package_count": 0, **common},
                "sca": {"path": "sca.json", "sha256": digest(self.files["sca.json"]),
                        "subject_sha256": artifact_digest, "sbom_sha256": sbom_digest,
                        "scanner": "Grype", "scanner_version": "0.122.1",
                        "scan_status": "not_run_no_package_records",
                        "disposition": "not_evaluated_no_package_records", "match_count": None,
                        **common},
                "slsa_provenance": {"status": "verified", "path": "slsa.json",
                        "sha256": digest(self.files["slsa.json"]), "subject_sha256": artifact_digest,
                        "verification_method": "gh-attestation-verify", "signer_workflow": SIGNER,
                        "oidc_issuer": ISSUER, "predicate_type": "https://slsa.dev/provenance/v1",
                        "source_repository": REPOSITORY, "source_ref": REF, "source_revision": REVISION,
                        **common},
                "cosign_signature": {"status": "verified", "path": "cosign.json",
                        "sha256": digest(self.files["cosign.json"]), "subject_sha256": artifact_digest,
                        "verification_method": "cosign-verify-blob", "signer_identity": COSIGN_IDENTITY,
                        "oidc_issuer": ISSUER, "source_repository": REPOSITORY,
                        "source_ref": REF, "source_revision": REVISION, **common},
            },
        }
        self.policy = {
            "schema_version": 1,
            "release_classification": "synthetic-training-fixture",
            "source": {"repository": REPOSITORY, "ref": REF, "workflow": WORKFLOW},
            "provenance": {"signer_workflow": SIGNER, "oidc_issuer": ISSUER},
            "cosign": {"certificate_identity": COSIGN_IDENTITY, "oidc_issuer": ISSUER},
            "sbom": {"accepted_formats": ["CycloneDX 1.7", "SPDX 2.3"],\n                    "required_generation_scope": "extracted-release-artifact"},\n            "sca": {"allow_empty_inventory_for_demo": True},
        }

    def tearDown(self):
        self.temp.cleanup()

    def validate(self):
        return validate_manifest(self.manifest, self.policy, self.artifact, self.evidence_root)

    def assert_rejected(self, mutate, expected):
        mutate()
        with self.assertRaisesRegex(PolicyError, expected):
            self.validate()

    def test_valid_demonstration_manifest_passes_without_production_promotion(self):
        result = self.validate()
        self.assertEqual(result["policy_decision"], "DEMO_PASS_NOT_FOR_PRODUCTION")
        self.assertFalse(result["promotion_authorized"])

    def test_artifact_tampering_is_rejected(self):
        self.artifact.write_bytes(b"tampered")
        with self.assertRaisesRegex(PolicyError, "artifact digest mismatch"):
            self.validate()

    def test_missing_sbom_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"].pop("sbom"), "required evidence")

    def test_missing_provenance_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"].pop("slsa_provenance"), "required evidence")

    def test_missing_cosign_signature_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"].pop("cosign_signature"), "required evidence")

    def test_mismatched_sbom_subject_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"]["sbom"].update(subject_sha256="0" * 64),
                             "SBOM is not bound")

    def test_mismatched_sca_subject_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"]["sca"].update(subject_sha256="0" * 64),
                             "SCA record is not bound")

    def test_sca_must_reference_exact_sbom_document(self):
        self.assert_rejected(lambda: self.manifest["evidence"]["sca"].update(sbom_sha256="0" * 64),
                             "exact SBOM document")

    def test_mismatched_provenance_subject_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"]["slsa_provenance"].update(subject_sha256="0" * 64),
                             "SLSA provenance subject")

    def test_untrusted_provenance_workflow_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"]["slsa_provenance"].update(
            signer_workflow="attacker/repo/.github/workflows/build.yml"), "not allow-listed")

    def test_untrusted_cosign_identity_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"]["cosign_signature"].update(
            signer_identity="https://attacker.invalid/workflow"), "not allow-listed")

    def test_wrong_oidc_issuer_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"]["cosign_signature"].update(
            oidc_issuer="https://attacker.invalid"), "OIDC issuer")

    def test_wrong_source_revision_is_rejected(self):
        self.assert_rejected(lambda: self.manifest["evidence"]["slsa_provenance"].update(
            source_revision="b" * 40), "source_revision mismatch")

    def test_evidence_file_tampering_is_rejected(self):
        self.files["cosign.json"].write_bytes(b"tampered bundle")
        with self.assertRaisesRegex(PolicyError, "evidence file digest mismatch"):
            self.validate()

    def test_path_traversal_is_rejected(self):
        self.manifest["evidence"]["sbom"]["path"] = "../outside.json"
        with self.assertRaisesRegex(PolicyError, "path traversal"):
            self.validate()

    def test_evidence_from_different_run_is_rejected(self):
        self.manifest["evidence"]["sbom"]["run_id"] = "999"
        with self.assertRaisesRegex(PolicyError, "different workflow run"):
            self.validate()

    def test_empty_inventory_is_not_misrepresented_as_clean(self):
        self.manifest["evidence"]["sca"]["disposition"] = "zero vulnerabilities"
        with self.assertRaisesRegex(PolicyError, "must not be described as vulnerability-free"):
            self.validate()

    def test_non-demo_release_classification_is_rejected(self):
        self.manifest["release_classification"] = "production"
        with self.assertRaisesRegex(PolicyError, "does not match policy"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
