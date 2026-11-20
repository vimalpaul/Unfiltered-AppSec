#!/usr/bin/env python3
"""Validate core OpenVEX v0.2.0 fields and apply a conservative release gate.

This is not a complete JSON-LD or official JSON Schema validator.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlparse

CONTEXT = "https://openvex.dev/ns/v0.2.0"
STATUSES = {"not_affected", "affected", "fixed", "under_investigation"}
JUSTIFICATIONS = {
    "component_not_present",
    "vulnerable_code_not_present",
    "vulnerable_code_not_in_execute_path",
    "vulnerable_code_cannot_be_controlled_by_adversary",
    "inline_mitigations_already_exist",
}
BLOCKING_STATUSES = {"affected", "under_investigation"}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def valid_timestamp(value: Any) -> bool:
    if not nonempty(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate_document(document: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["document root must be a JSON object"]

    if document.get("@context") != CONTEXT:
        errors.append(f"@context must equal {CONTEXT}")
    doc_id = document.get("@id")
    if not nonempty(doc_id) or not urlparse(doc_id).scheme:
        errors.append("@id must be a non-empty IRI")
    if not nonempty(document.get("author")):
        errors.append("author must identify an individual or organization")
    if not valid_timestamp(document.get("timestamp")):
        errors.append("timestamp must be an RFC3339-compatible date-time")
    version = document.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        errors.append("version must be a positive integer")

    statements = document.get("statements")
    if not isinstance(statements, list) or not statements:
        errors.append("statements must be a non-empty array")
        return errors

    for index, statement in enumerate(statements):
        prefix = f"statements[{index}]"
        if not isinstance(statement, dict):
            errors.append(f"{prefix} must be an object")
            continue

        vuln = statement.get("vulnerability")
        if not isinstance(vuln, dict) or not nonempty(vuln.get("name")):
            errors.append(f"{prefix}.vulnerability.name is required")

        status = statement.get("status")
        if status not in STATUSES:
            errors.append(f"{prefix}.status must be one of {sorted(STATUSES)}")

        timestamp = statement.get("timestamp", document.get("timestamp"))
        if not valid_timestamp(timestamp):
            errors.append(f"{prefix} must have a valid timestamp directly or by inheritance")

        products = statement.get("products")
        if not isinstance(products, list) or not products:
            errors.append(f"{prefix}.products must identify at least one product")
        else:
            for product_index, product in enumerate(products):
                product_prefix = f"{prefix}.products[{product_index}]"
                if not isinstance(product, dict):
                    errors.append(f"{product_prefix} must be an object")
                    continue
                identifiers = product.get("identifiers")
                hashes = product.get("hashes")
                has_id = nonempty(product.get("@id"))
                has_identifier = isinstance(identifiers, dict) and any(
                    nonempty(v) for v in identifiers.values()
                )
                has_hash = isinstance(hashes, dict) and any(
                    nonempty(v) for v in hashes.values()
                )
                if not (has_id or has_identifier or has_hash):
                    errors.append(f"{product_prefix} must contain @id, identifiers or hashes")
                if hashes is not None:
                    if not isinstance(hashes, dict):
                        errors.append(f"{product_prefix}.hashes must be an object")
                    else:
                        for algorithm, digest in hashes.items():
                            if not nonempty(algorithm) or not nonempty(digest):
                                errors.append(f"{product_prefix}.hashes entries must be non-empty")
                            if algorithm.lower() == "sha-256" and not SHA256_RE.fullmatch(digest):
                                errors.append(f"{product_prefix} sha-256 must be 64 hexadecimal characters")

        if status == "not_affected":
            justification = statement.get("justification")
            impact = statement.get("impact_statement")
            if justification not in JUSTIFICATIONS and not nonempty(impact):
                errors.append(
                    f"{prefix} not_affected requires a valid justification or impact_statement"
                )
            if justification is not None and justification not in JUSTIFICATIONS:
                errors.append(f"{prefix}.justification is not a recognized OpenVEX justification")
        if status == "affected" and not nonempty(statement.get("action_statement")):
            errors.append(f"{prefix} affected requires an action_statement")

    return errors


def release_gate(document: dict[str, Any]) -> list[str]:
    """Return policy violations for a candidate release; no approval is inferred."""
    errors = validate_document(document)
    if errors:
        return [f"invalid VEX: {error}" for error in errors]

    for index, statement in enumerate(document["statements"]):
        status = statement["status"]
        if status in BLOCKING_STATUSES:
            errors.append(f"statements[{index}] status '{status}' blocks release")
        for product_index, product in enumerate(statement["products"]):
            hashes = product.get("hashes", {})
            digest = hashes.get("sha-256") if isinstance(hashes, dict) else None
            if not nonempty(digest) or not SHA256_RE.fullmatch(digest):
                errors.append(
                    f"statements[{index}].products[{product_index}] requires an exact sha-256 for release"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--document", required=True, type=Path)
    parser.add_argument(
        "--release-gate",
        action="store_true",
        help="apply conservative status and product SHA-256 checks",
    )
    args = parser.parse_args()
    try:
        document = json.loads(args.document.read_text(encoding="utf-8"))
        errors = release_gate(document) if args.release_gate else validate_document(document)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"VEX validation failed: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    statements = document["statements"]
    print(f"OpenVEX v0.2.0 core validation passed: {len(statements)} statement(s)")
    if args.release_gate:
        print("VEX policy checks passed; this does not replace release approval or evidence verification.")
    else:
        print("Structural validation only; no product release decision was made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
