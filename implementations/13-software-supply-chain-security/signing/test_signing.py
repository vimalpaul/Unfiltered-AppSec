import sys
from pathlib import Path
import tempfile
import unittest

PROVENANCE_DIR = Path(__file__).resolve().parents[1] / "provenance"
sys.path.insert(0, str(PROVENANCE_DIR))

from build_demo_artifact import build_artifact
from verify_build_metadata import validate

REPOSITORY = "vimalpaul/Unfiltered-AppSec"
REVISION = "b" * 40
WORKFLOW = ".github/workflows/cosign-artifact-signing.yml"


class CosignBuildFixtureTests(unittest.TestCase):
    def test_shared_builder_binds_synthetic_artifact_to_cosign_workflow(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact = root / "unfiltered-appsec-demo.tar.gz"
            metadata = root / "build-metadata.json"
            build_artifact(artifact, metadata, REPOSITORY, REVISION, WORKFLOW)
            self.assertEqual(
                validate(artifact, metadata, REPOSITORY, REVISION, WORKFLOW),
                [],
            )

    def test_metadata_rejects_slsa_workflow_identity_for_cosign_build(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            artifact = root / "unfiltered-appsec-demo.tar.gz"
            metadata = root / "build-metadata.json"
            build_artifact(artifact, metadata, REPOSITORY, REVISION, WORKFLOW)
            errors = validate(
                artifact,
                metadata,
                REPOSITORY,
                REVISION,
                ".github/workflows/slsa-build-provenance.yml",
            )
            self.assertIn("build_workflow does not match the expected workflow", errors)


if __name__ == "__main__":
    unittest.main()
