#!/usr/bin/env python3
"""Basic structural validation for a Grype JSON vulnerability report."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


def validate_report(path: Path) -> int:
    report: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(report, dict):
        raise ValueError("Grype report root must be a JSON object")
    matches = report.get("matches")
    if not isinstance(matches, list):
        raise ValueError("Grype report must contain a matches array")
    descriptor = report.get("descriptor")
    if not isinstance(descriptor, dict):
        raise ValueError("Grype report must contain descriptor metadata")
    if descriptor.get("name") != "grype":
        raise ValueError("Report descriptor name must be grype")
    print(f"Grype report structure valid: {len(matches)} vulnerability matches")
    return len(matches)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    try:
        validate_report(args.report)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Grype report validation failed: {exc}", file=sys.stderr)
        return 1
    print("Basic report checks passed; this is not a finding-quality or schema assessment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
