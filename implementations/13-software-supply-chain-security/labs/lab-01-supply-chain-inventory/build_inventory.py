#!/usr/bin/env python3
"""Validate a synthetic supply-chain inventory and generate deterministic evidence."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

CATEGORIES = (
    "source_repositories", "source_controls", "dependencies", "registries",
    "workflows", "runners", "identities", "artifacts", "suppliers",
    "deployment_targets",
)
CRITICALITIES = {"low", "medium", "high", "critical"}
TRUST_ZONES = {
    "developer", "source-control", "third-party", "build",
    "identity", "artifact", "deployment",
}
ID_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9._-]{2,63}$")
SENSITIVE_KEY = re.compile(r"(password|token|secret|private.?key|credential|client.?secret)", re.I)


class InventoryError(ValueError):
    """Raised when the inventory violates the lab evidence contract."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise InventoryError(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_inventory(data: Any) -> dict[str, Any]:
    require(isinstance(data, dict), "inventory root must be an object")
    required = {"schema_version", "inventory_id", "product", "revision", "scope",
                "assets", "relationships", "risks"}
    require(set(data) == required, f"top-level fields must be exactly: {sorted(required)}")
    require(data["schema_version"] == "1.0", "unsupported schema_version")
    require(nonempty(data["inventory_id"]) and ID_PATTERN.fullmatch(data["inventory_id"]),
            "inventory_id must be a stable uppercase identifier")
    product = data["product"]
    require(isinstance(product, dict) and set(product) == {"name", "description", "owner"}, "product must contain exactly name, description and owner")
    for field in ("name", "description", "owner"):
        require(nonempty(product.get(field)), f"product.{field} is required")
    require(isinstance(data["revision"], str) and re.fullmatch(r"[0-9a-f]{7,64}", data["revision"]),
            "revision must be a hexadecimal source revision")
    scope = data["scope"]
    require(isinstance(scope, dict) and set(scope) == {"environment", "discovery_method", "limitations"}, "scope must contain exactly environment, discovery_method and limitations")
    require(scope.get("environment") in {"synthetic-lab", "test", "staging", "production"},
            "scope.environment is invalid")
    require(nonempty(scope.get("discovery_method")), "scope.discovery_method is required")
    require(isinstance(scope.get("limitations"), list), "scope.limitations must be an array")

    assets = data["assets"]
    require(isinstance(assets, dict), "assets must be an object")
    require(set(assets) == set(CATEGORIES), "assets must contain exactly the ten defined categories")
    index: dict[str, dict[str, Any]] = {}
    for category in CATEGORIES:
        records = assets[category]
        require(isinstance(records, list), f"assets.{category} must be an array")
        for position, asset in enumerate(records):
            prefix = f"assets.{category}[{position}]"
            require(isinstance(asset, dict), f"{prefix} must be an object")
            for field in ("id", "name", "owner", "criticality", "trust_zone", "source",
                          "evidence_refs", "attributes"):
                require(field in asset, f"{prefix}.{field} is required")
            asset_id = asset["id"]
            require(nonempty(asset_id) and ID_PATTERN.fullmatch(asset_id),
                    f"{prefix}.id must be a stable uppercase identifier")
            require(asset_id not in index, f"duplicate asset identifier: {asset_id}")
            for field in ("name", "owner", "source"):
                require(nonempty(asset[field]), f"{prefix}.{field} must be non-empty")
            require(asset["criticality"] in CRITICALITIES,
                    f"{prefix}.criticality is invalid for {asset_id}")
            require(asset["trust_zone"] in TRUST_ZONES,
                    f"{prefix}.trust_zone is invalid for {asset_id}")
            require(isinstance(asset["evidence_refs"], list) and bool(asset["evidence_refs"])
                    and all(nonempty(ref) for ref in asset["evidence_refs"]),
                    f"{prefix}.evidence_refs must contain non-empty references")
            require(isinstance(asset["attributes"], dict), f"{prefix}.attributes must be an object")
            for key, value in asset["attributes"].items():
                if SENSITIVE_KEY.search(str(key)):
                    require(isinstance(value, str)
                            and value.startswith(("vault://", "secret-manager://", "key-vault://")),
                            f"{prefix}.attributes.{key} must be an opaque secret-manager reference, never a secret value")
            index[asset_id] = asset

    require(bool(index), "inventory must contain at least one asset")
    mermaid_ids = [re.sub(r"[^A-Za-z0-9_]", "_", asset_id) for asset_id in index]
    require(len(mermaid_ids) == len(set(mermaid_ids)), "asset identifiers collide after Mermaid node normalization")
    relationships = data["relationships"]
    require(isinstance(relationships, list), "relationships must be an array")
    relationship_ids: set[str] = set()
    for position, rel in enumerate(relationships):
        prefix = f"relationships[{position}]"
        require(isinstance(rel, dict), f"{prefix} must be an object")
        for field in ("id", "from", "to", "relationship", "crosses_trust_boundary"):
            require(field in rel, f"{prefix}.{field} is required")
        rel_id = rel["id"]
        require(nonempty(rel_id) and ID_PATTERN.fullmatch(rel_id),
                f"{prefix}.id must be a stable uppercase identifier")
        require(rel_id not in relationship_ids, f"duplicate relationship identifier: {rel_id}")
        relationship_ids.add(rel_id)
        require(rel["from"] in index, f"{rel_id} references unknown source asset: {rel['from']}")
        require(rel["to"] in index, f"{rel_id} references unknown target asset: {rel['to']}")
        require(rel["from"] != rel["to"], f"{rel_id} must not be a self-referential relationship")
        require(nonempty(rel["relationship"]), f"{rel_id}.relationship is required")
        require(isinstance(rel["crosses_trust_boundary"], bool),
                f"{rel_id}.crosses_trust_boundary must be boolean")

    risks = data["risks"]
    require(isinstance(risks, list), "risks must be an array")
    risk_ids: set[str] = set()
    for position, risk in enumerate(risks):
        prefix = f"risks[{position}]"
        require(isinstance(risk, dict), f"{prefix} must be an object")
        for field in ("id", "asset_id", "scenario", "likelihood", "impact",
                      "treatment", "owner", "status"):
            require(field in risk, f"{prefix}.{field} is required")
        risk_id = risk["id"]
        require(nonempty(risk_id) and ID_PATTERN.fullmatch(risk_id),
                f"{prefix}.id must be a stable uppercase identifier")
        require(risk_id not in risk_ids, f"duplicate risk identifier: {risk_id}")
        risk_ids.add(risk_id)
        require(risk["asset_id"] in index, f"{risk_id} references unknown asset: {risk['asset_id']}")
        require(nonempty(risk["scenario"]) and nonempty(risk["treatment"])
                and nonempty(risk["owner"]), f"{risk_id} requires scenario, treatment and owner")
        require(risk["likelihood"] in {"low", "medium", "high"}, f"{risk_id} likelihood is invalid")
        require(risk["impact"] in {"low", "medium", "high", "critical"}, f"{risk_id} impact is invalid")
        require(risk["status"] in {"open", "mitigating", "accepted", "closed"},
                f"{risk_id} status is invalid")

    normalized = json.loads(json.dumps(data, sort_keys=True))
    connected = {endpoint for rel in relationships for endpoint in (rel["from"], rel["to"])}
    unconnected = sorted(set(index) - connected)
    normalized["summary"] = {
        "asset_count": len(index),
        "unconnected_asset_ids": unconnected,
        "asset_category_count": len(CATEGORIES),
        "relationship_count": len(relationships),
        "trust_boundary_crossings": sum(1 for rel in relationships if rel["crosses_trust_boundary"]),
        "risk_count": len(risks),
        "critical_asset_count": sum(1 for asset in index.values() if asset["criticality"] == "critical"),
    }
    return normalized


def generate_outputs(data: dict[str, Any], output_dir: Path) -> dict[str, str]:
    normalized = validate_inventory(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    assets = []
    for category in CATEGORIES:
        for asset in normalized["assets"][category]:
            assets.append({
                "asset_id": asset["id"], "category": category, "name": asset["name"],
                "owner": asset["owner"], "criticality": asset["criticality"],
                "trust_zone": asset["trust_zone"], "source": asset["source"],
                "evidence_refs": ";".join(asset["evidence_refs"]),
            })
    relationships = [{
        "relationship_id": rel["id"], "from_asset": rel["from"], "to_asset": rel["to"],
        "relationship": rel["relationship"],
        "crosses_trust_boundary": str(rel["crosses_trust_boundary"]).lower(),
        "notes": rel.get("notes", ""),
    } for rel in normalized["relationships"]]
    risks = [{
        "risk_id": risk["id"], "asset_id": risk["asset_id"], "scenario": risk["scenario"],
        "likelihood": risk["likelihood"], "impact": risk["impact"],
        "treatment": risk["treatment"], "owner": risk["owner"], "status": risk["status"],
    } for risk in normalized["risks"]]

    import io
    outputs: dict[str, str] = {}
    outputs["inventory.normalized.json"] = json.dumps(normalized, indent=2, sort_keys=True) + "\n"
    for filename, fields, rows in (
        ("assets.csv", ["asset_id", "category", "name", "owner", "criticality", "trust_zone", "source", "evidence_refs"], assets),
        ("relationships.csv", ["relationship_id", "from_asset", "to_asset", "relationship", "crosses_trust_boundary", "notes"], relationships),
        ("risk-register.csv", ["risk_id", "asset_id", "scenario", "likelihood", "impact", "treatment", "owner", "status"], risks),
    ):
        buffer = io.StringIO(newline="")
        writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        outputs[filename] = buffer.getvalue()

    graph = ["flowchart LR"]
    for asset in assets:
        label = f'{asset["asset_id"]} — {asset["name"]}'.replace('"', "'").replace("\n", " ")
        graph.append(f'  {asset["asset_id"].replace("-", "_")}["{label}"]')
    for rel in normalized["relationships"]:
        edge = "-.->|" if rel["crosses_trust_boundary"] else "-->|"
        graph.append(f'  {rel["from"].replace("-", "_")} {edge}{rel["relationship"]}| {rel["to"].replace("-", "_")}')
    outputs["trust-boundary-map.mmd"] = "\n".join(graph) + "\n"

    summary = normalized["summary"]
    report = [
        "# Synthetic supply-chain inventory assessment", "",
        f'- Inventory: {normalized["inventory_id"]}',
        f'- Product: {normalized["product"]["name"]}',
        f'- Revision: {normalized["revision"]}',
        f'- Environment: {normalized["scope"]["environment"]}', "",
        "## Coverage", "",
        f'- Assets: **{summary["asset_count"]}** across **{summary["asset_category_count"]}** categories',
        f'- Relationships: **{summary["relationship_count"]}**',
        f'- Trust-boundary crossings: **{summary["trust_boundary_crossings"]}**',
        f'- Critical assets: **{summary["critical_asset_count"]}**',
        f'- Risk scenarios: **{summary["risk_count"]}**',
        f'- Unconnected assets: **{len(summary["unconnected_asset_ids"])}**', "",
        "## Limitations", "",
        *[f'- {item}' for item in normalized["scope"]["limitations"]],
        "- Counts measure supplied records, not completeness of a real environment.",
        "- Relationship arrows express declared flows; they are not runtime telemetry.",
        "- A trust-boundary marker indicates a review boundary, not a confirmed security weakness.",
        "",
    ]
    outputs["assessment-summary.md"] = "\n".join(report)
    for filename, content in outputs.items():
        (output_dir / filename).write_text(content, encoding="utf-8", newline="")
    checksums = []
    for filename in sorted(outputs):
        digest = hashlib.sha256((output_dir / filename).read_bytes()).hexdigest()
        checksums.append(f"{digest}  {filename}")
    (output_dir / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        normalized = validate_inventory(data)
        generate_outputs(data, args.output_dir)
    except (OSError, json.JSONDecodeError, InventoryError) as exc:
        print(f"Inventory validation failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(normalized["summary"], indent=2, sort_keys=True))
    print(f"Evidence generated: {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
