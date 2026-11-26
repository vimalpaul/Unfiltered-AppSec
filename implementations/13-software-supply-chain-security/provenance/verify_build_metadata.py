#!/usr/bin/env python3
"""Verify synthetic artifact metadata before it is passed to the attestation job.

This verifies a local digest and source binding only. It does not verify a signature.
Cryptographic provenance verification is performed by GitHub CLI gh attestation verify.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(
    artifact: Path,
    metadata_path: Path,
    expected_repository: str,
    expected_revision: str,
    expected_workflow: str,
) -> list[str]:
    errors: list[str] = []
    try:
        metadata: Any = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read metadata JSON: {exc}"]

    if not isinstance(metadata, dict):
        return ["metadata root must be a JSON object"]
    if metadata.get("schema_version") != 1:
        errors.append("unsupported metadata schema_version")
    if metadata.get("artifact_name") != artifact.name:
        errors.append("artifact_name does not match downloaded artifact")
    recorded = metadata.get("artifact_sha256")
    if not isinstance(recorded, str) or not SHA256_RE.fullmatch(recorded):
        errors.append("artifact_sha256 must be 64 lowercase hexadecimal characters")
    elif artifact.exists() and sha256_file(artifact) != recorded:
        errors.append("artifact SHA-256 mismatch")
    if metadata.get("source_repository") != expected_repository:
        errors.append("source_repository does not match the expected repository")
    if metadata.get("source_revision") != expected_revision or not REVISION_RE.fullmatch(expected_revision):
        errors.append("source_revision does not match the exact expected commit")
    if metadata.get("build_workflow") != expected_workflow:
        errors.append("build_workflow does not match the expected workflow")
    if metadata.get("artifact_kind") != "synthetic-training-fixture":
        errors.append("artifact_kind is not the expected synthetic fixture")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--workflow", required=True)
    args = parser.parse_args()
    errors = validate(
        args.artifact,
        args.metadata,
        args.repository,
        args.revision,
        args.workflow,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Artifact digest and source metadata checks passed; signature verification is separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
