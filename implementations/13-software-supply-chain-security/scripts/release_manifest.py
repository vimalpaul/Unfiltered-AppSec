#!/usr/bin/env python3
"""Create and verify a deterministic SHA-256 file-integrity manifest.

This is NOT an SPDX/CycloneDX SBOM, build attestation, provenance statement,
signature, vulnerability scan, or proof that source files are trustworthy.
Uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

SCHEMA = "https://unfiltered-appsec.example/schemas/source-integrity-manifest/v1"
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules"}
MANIFEST_FORMAT = "unfiltered-appsec-source-integrity-manifest"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_commit(root: Path) -> str | None:
    try:
        value = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return value or None
    except (OSError, subprocess.CalledProcessError):
        return None


def collect_files(root: Path, output: Path | None) -> list[dict[str, Any]]:
    resolved_root = root.resolve(strict=True)
    records: list[dict[str, Any]] = []
    for current, dirs, filenames in os.walk(resolved_root, followlinks=False):
        current_path = Path(current)
        dirs[:] = sorted(
            name for name in dirs
            if name not in EXCLUDED_DIRS
            and not (current_path / name).is_symlink()
        )
        for name in sorted(filenames):
            candidate = current_path / name
            if candidate.is_symlink():
                raise ValueError(f"Symbolic links are not permitted: {candidate}")
            resolved = candidate.resolve(strict=True)
            if not resolved.is_relative_to(resolved_root):
                raise ValueError(f"Path escapes root: {candidate}")
            if output is not None and resolved == output.resolve():
                continue
            if not resolved.is_file():
                continue
            records.append({
                "path": resolved.relative_to(resolved_root).as_posix(),
                "size": resolved.stat().st_size,
                "sha256": sha256_file(resolved),
            })
    return sorted(records, key=lambda item: item["path"])


def build_manifest(root: Path, output: Path | None = None) -> dict[str, Any]:
    resolved_root = root.resolve(strict=True)
    return {
        "format": MANIFEST_FORMAT,
        "schema": SCHEMA,
        "source": {
            "repository_commit": git_commit(resolved_root),
            "root_label": ".",
        },
        "hash_algorithm": "sha256",
        "entries": collect_files(resolved_root, output),
    }


def generate(root: Path, output: Path) -> None:
    manifest = build_manifest(root, output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Generated {len(manifest['entries'])} file records: {output}")


def verify(root: Path, manifest_path: Path) -> None:
    supplied = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(supplied, dict) or supplied.get("format") != MANIFEST_FORMAT:
        raise ValueError("Unsupported manifest format")
    if supplied.get("hash_algorithm") != "sha256":
        raise ValueError("Unsupported hash algorithm")
    expected = build_manifest(root, manifest_path)
    if supplied.get("entries") != expected["entries"]:
        expected_by_path = {x["path"]: x for x in expected["entries"]}
        supplied_entries = supplied.get("entries")
        if not isinstance(supplied_entries, list):
            raise ValueError("Manifest entries must be a list")
        supplied_by_path = {
            x.get("path"): x for x in supplied_entries if isinstance(x, dict)
        }
        missing = sorted(set(expected_by_path) - set(supplied_by_path))
        unexpected = sorted(set(supplied_by_path) - set(expected_by_path))
        changed = sorted(
            path for path in set(expected_by_path) & set(supplied_by_path)
            if expected_by_path[path] != supplied_by_path[path]
        )
        raise ValueError(
            "Integrity verification failed: "
            f"missing={missing[:10]}, unexpected={unexpected[:10]}, "
            f"changed={changed[:10]}"
        )
    print(f"Verified {len(expected['entries'])} file records")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="generate a file-integrity manifest")
    gen.add_argument("--root", type=Path, default=Path("."))
    gen.add_argument("--output", type=Path, required=True)
    check = sub.add_parser("verify", help="verify a manifest against current files")
    check.add_argument("--root", type=Path, default=Path("."))
    check.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "generate":
            generate(args.root, args.output)
        else:
            verify(args.root, args.manifest)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
