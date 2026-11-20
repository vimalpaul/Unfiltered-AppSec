import json
from pathlib import Path
import tempfile
import unittest

from validate_grype_report import validate_report


class GrypeReportTests(unittest.TestCase):
    def test_valid_report_with_no_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "grype.json"
            path.write_text(json.dumps({
                "matches": [],
                "descriptor": {"name": "grype", "version": "0.122.1"},
            }), encoding="utf-8")
            self.assertEqual(validate_report(path), 0)

    def test_valid_report_with_match(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "grype.json"
            path.write_text(json.dumps({
                "matches": [{"vulnerability": {"id": "CVE-2099-0001"}}],
                "descriptor": {"name": "grype"},
            }), encoding="utf-8")
            self.assertEqual(validate_report(path), 1)

    def test_missing_descriptor_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "grype.json"
            path.write_text(json.dumps({"matches": []}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "descriptor"):
                validate_report(path)


if __name__ == "__main__":
    unittest.main()
