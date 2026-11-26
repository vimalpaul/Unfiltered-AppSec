import json
from pathlib import Path
import tempfile
import unittest

from build_demo_artifact import build_artifact
from verify_build_metadata import validate

REPOSITORY = "vimalpaul/Unfiltered-AppSec"
REVISION = "a" * 40
WORKFLOW = ".github/workflows/slsa-build-provenance.yml"


class ProvenanceFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.artifact = self.root / "demo.tar.gz"
        self.metadata = self.root / "build-metadata.json"
        build_artifact(self.artifact, self.metadata, REPOSITORY, REVISION, WORKFLOW)

    def tearDown(self):
        self.temp.cleanup()

    def test_metadata_binds_artifact_to_source_revision(self):
        self.assertEqual(
            validate(self.artifact, self.metadata, REPOSITORY, REVISION, WORKFLOW),
            [],
        )

    def test_artifact_tampering_is_detected(self):
        with self.artifact.open("ab") as stream:
            stream.write(b"tampered")
        errors = validate(self.artifact, self.metadata, REPOSITORY, REVISION, WORKFLOW)
        self.assertIn("artifact SHA-256 mismatch", errors)

    def test_wrong_repository_is_rejected(self):
        errors = validate(self.artifact, self.metadata, "attacker/other-repo", REVISION, WORKFLOW)
        self.assertIn("source_repository does not match the expected repository", errors)

    def test_wrong_commit_is_rejected(self):
        errors = validate(self.artifact, self.metadata, REPOSITORY, "b" * 40, WORKFLOW)
        self.assertIn("source_revision does not match the exact expected commit", errors)

    def test_wrong_workflow_is_rejected(self):
        errors = validate(self.artifact, self.metadata, REPOSITORY, REVISION, ".github/workflows/other.yml")
        self.assertIn("build_workflow does not match the expected workflow", errors)

    def test_invalid_metadata_digest_is_rejected(self):
        data = json.loads(self.metadata.read_text(encoding="utf-8"))
        data["artifact_sha256"] = "not-a-digest"
        self.metadata.write_text(json.dumps(data), encoding="utf-8")
        errors = validate(self.artifact, self.metadata, REPOSITORY, REVISION, WORKFLOW)
        self.assertIn("artifact_sha256 must be 64 lowercase hexadecimal characters", errors)

    def test_deterministic_build_output(self):
        second_artifact = self.root / "second.tar.gz"
        second_metadata = self.root / "second-metadata.json"
        build_artifact(second_artifact, second_metadata, REPOSITORY, REVISION, WORKFLOW)
        self.assertEqual(self.artifact.read_bytes(), second_artifact.read_bytes())

    def test_invalid_revision_rejected(self):
        with self.assertRaises(ValueError):
            build_artifact(
                self.root / "invalid.tar.gz",
                self.root / "invalid.json",
                REPOSITORY,
                "not-a-full-commit",
                WORKFLOW,
            )


if __name__ == "__main__":
    unittest.main()
