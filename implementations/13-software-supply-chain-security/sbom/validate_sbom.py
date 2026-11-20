#!/usr/bin/env python3
"""Perform basic structural checks on Syft-generated CycloneDX and SPDX JSON."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: JSON root must be an object")
    return data


def validate_cyclonedx(path: Path) -> int:
    data = load_json(path)
    if data.get("bomFormat") != "CycloneDX":
        raise ValueError(f"{path}: bomFormat must be CycloneDX")
    if data.get("specVersion") != "1.7":
        raise ValueError(f"{path}: expected CycloneDX specVersion 1.7")
    if not isinstance(data.get("serialNumber"), str) or not data["serialNumber"]:
        raise ValueError(f"{path}: missing serialNumber")
    if not isinstance(data.get("version"), int):
        raise ValueError(f"{path}: missing integer BOM version")
    components = data.get("components", [])
    if not isinstance(components, list):
        raise ValueError(f"{path}: components must be an array")
    print(f"CycloneDX 1.7: {len(components)} top-level components")
    return len(components)


def validate_spdx(path: Path) -> int:
    data = load_json(path)
    if data.get("spdxVersion") != "SPDX-2.3":
        raise ValueError(f"{path}: expected SPDX-2.3")
    for field in ("SPDXID", "name", "dataLicense", "creationInfo"):
        if field not in data:
            raise ValueError(f"{path}: missing required SPDX field {field}")
    packages = data.get("packages", [])
    if not isinstance(packages, list):
        raise ValueError(f"{path}: packages must be an array")
    print(f"SPDX 2.3: {len(packages)} package records")
    return len(packages)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cyclonedx", required=True, type=Path)
    parser.add_argument("--spdx", required=True, type=Path)
    args = parser.parse_args()
    try:
        validate_cyclonedx(args.cyclonedx)
        validate_spdx(args.spdx)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"SBOM validation failed: {exc}", file=sys.stderr)
        return 1
    print("Basic SBOM structure checks passed; full schema validation is not performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
