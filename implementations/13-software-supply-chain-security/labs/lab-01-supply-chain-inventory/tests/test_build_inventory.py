import copy
import json
import tempfile
import unittest
from pathlib import Path

from build_inventory import InventoryError, generate_outputs, validate_inventory

FIXTURE = Path(__file__).parents[1] / "fixtures" / "synthetic-product-inventory.json"


class InventoryValidationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_synthetic_fixture_is_valid(self):
        result = validate_inventory(self.data)
        self.assertEqual(result["summary"]["asset_count"], 12)
        self.assertEqual(result["summary"]["relationship_count"], 11)
        self.assertEqual(result["summary"]["trust_boundary_crossings"], 8)
        self.assertEqual(result["summary"]["risk_count"], 5)

    def test_duplicate_asset_identifier_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["assets"]["registries"].append(copy.deepcopy(data["assets"]["dependencies"][0]))
        with self.assertRaisesRegex(InventoryError, "duplicate asset identifier"):
            validate_inventory(data)

    def test_unknown_relationship_source_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["relationships"][0]["from"] = "MISSING-ASSET"
        with self.assertRaisesRegex(InventoryError, "unknown source asset"):
            validate_inventory(data)

    def test_unknown_relationship_target_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["relationships"][0]["to"] = "MISSING-ASSET"
        with self.assertRaisesRegex(InventoryError, "unknown target asset"):
            validate_inventory(data)

    def test_self_referential_relationship_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["relationships"][0]["to"] = data["relationships"][0]["from"]
        with self.assertRaisesRegex(InventoryError, "self-referential"):
            validate_inventory(data)

    def test_duplicate_relationship_identifier_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["relationships"][1]["id"] = data["relationships"][0]["id"]
        with self.assertRaisesRegex(InventoryError, "duplicate relationship identifier"):
            validate_inventory(data)

    def test_missing_asset_owner_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["assets"]["artifacts"][0]["owner"] = ""
        with self.assertRaisesRegex(InventoryError, "owner must be non-empty"):
            validate_inventory(data)

    def test_invalid_criticality_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["assets"]["runners"][0]["criticality"] = "urgent"
        with self.assertRaisesRegex(InventoryError, "criticality is invalid"):
            validate_inventory(data)

    def test_invalid_trust_zone_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["assets"]["runners"][0]["trust_zone"] = "unknown-zone"
        with self.assertRaisesRegex(InventoryError, "trust_zone is invalid"):
            validate_inventory(data)

    def test_inline_token_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["assets"]["workflows"][0]["attributes"]["api_token"] = "ghp_synthetic_but_not_a_secret"
        with self.assertRaisesRegex(InventoryError, "opaque secret-manager reference"):
            validate_inventory(data)

    def test_secret_reference_uri_is_accepted(self):
        self.assertEqual(validate_inventory(self.data)["summary"]["asset_count"], 12)

    def test_duplicate_risk_identifier_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["risks"][1]["id"] = data["risks"][0]["id"]
        with self.assertRaisesRegex(InventoryError, "duplicate risk identifier"):
            validate_inventory(data)

    def test_risk_with_unknown_asset_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["risks"][0]["asset_id"] = "MISSING-ASSET"
        with self.assertRaisesRegex(InventoryError, "references unknown asset"):
            validate_inventory(data)

    def test_empty_inventory_is_rejected(self):
        data = copy.deepcopy(self.data)
        for category in data["assets"]:
            data["assets"][category] = []
        with self.assertRaisesRegex(InventoryError, "at least one asset"):
            validate_inventory(data)

    def test_undefined_asset_category_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["assets"]["unknown_category"] = []
        with self.assertRaisesRegex(InventoryError, "exactly the ten defined categories"):
            validate_inventory(data)

    def test_generation_is_deterministic(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            generate_outputs(self.data, Path(first))
            generate_outputs(self.data, Path(second))
            files_a = sorted(p.name for p in Path(first).iterdir())
            files_b = sorted(p.name for p in Path(second).iterdir())
            self.assertEqual(files_a, files_b)
            for name in files_a:
                self.assertEqual((Path(first) / name).read_bytes(), (Path(second) / name).read_bytes())

    def test_boundary_relationship_is_rendered_as_dashed_edge(self):
        with tempfile.TemporaryDirectory() as output:
            generate_outputs(self.data, Path(output))
            graph = (Path(output) / "trust-boundary-map.mmd").read_text(encoding="utf-8")
            self.assertIn("-.->|declares-dependency|", graph)
            self.assertIn("-->|governed-by|", graph)

    def test_outputs_include_separate_registers(self):
        with tempfile.TemporaryDirectory() as output:
            generate_outputs(self.data, Path(output))
            names = {p.name for p in Path(output).iterdir()}
            self.assertTrue({"assets.csv", "relationships.csv", "risk-register.csv",
                             "inventory.normalized.json", "trust-boundary-map.mmd",
                             "assessment-summary.md", "SHA256SUMS"}.issubset(names))


if __name__ == "__main__":
    unittest.main()
