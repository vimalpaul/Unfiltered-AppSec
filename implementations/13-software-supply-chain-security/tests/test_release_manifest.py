import json
from pathlib import Path
import tempfile
import unittest

from scripts.release_manifest import build_manifest, generate, verify


class ReleaseManifestTests(unittest.TestCase):
    def test_manifest_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "a.txt").write_text("alpha", encoding="utf-8")
            (root / "b.txt").write_text("beta", encoding="utf-8")
            first = build_manifest(root)
            second = build_manifest(root)
            self.assertEqual(first, second)
            self.assertEqual(
                [entry["path"] for entry in first["entries"]],
                ["a.txt", "b.txt"],
            )

    def test_output_manifest_is_not_self_hashed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "source.txt").write_text("content", encoding="utf-8")
            output = root / "dist" / "manifest.json"
            generate(root, output)
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual([x["path"] for x in data["entries"]], ["source.txt"])
            verify(root, output)

    def test_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.txt"
            source.write_text("original", encoding="utf-8")
            output = root / "manifest.json"
            generate(root, output)
            source.write_text("tampered", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Integrity verification failed"):
                verify(root, output)

    def test_symbolic_link_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target.txt"
            target.write_text("safe", encoding="utf-8")
            link = root / "link.txt"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("Symbolic links unavailable on this platform")
            with self.assertRaisesRegex(ValueError, "Symbolic links"):
                build_manifest(root)


if __name__ == "__main__":
    unittest.main()
