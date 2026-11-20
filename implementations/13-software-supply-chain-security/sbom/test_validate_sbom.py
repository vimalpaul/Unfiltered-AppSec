import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from validate_sbom import validate_cyclonedx, validate_spdx


class SbomValidationTests(unittest.TestCase):
    def test_valid_cyclonedx_17(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bom.json"
            path.write_text(json.dumps({
                "bomFormat": "CycloneDX",
                "specVersion": "1.7",
                "serialNumber": "urn:uuid:11111111-1111-4111-8111-111111111111",
                "version": 1,
                "components": [],
            }), encoding="utf-8")
            self.assertEqual(validate_cyclonedx(path), 0)

    def test_valid_spdx_23(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bom.json"
            path.write_text(json.dumps({
                "spdxVersion": "SPDX-2.3",
                "SPDXID": "SPDXRef-DOCUMENT",
                "name": "synthetic",
                "dataLicense": "CC0-1.0",
                "creationInfo": {"creators": ["Tool: synthetic"]},
                "packages": [],
            }), encoding="utf-8")
            self.assertEqual(validate_spdx(path), 0)

    def test_wrong_cyclonedx_version_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bom.json"
            path.write_text(json.dumps({
                "bomFormat": "CycloneDX",
                "specVersion": "1.6",
                "serialNumber": "urn:uuid:11111111-1111-4111-8111-111111111111",
                "version": 1,
                "components": [],
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "specVersion 1.7"):
                validate_cyclonedx(path)


if __name__ == "__main__":
    unittest.main()
