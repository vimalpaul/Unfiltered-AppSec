#!/usr/bin/env python3
"""Fail-closed validator for a unified, synthetic release-evidence manifest.

Cryptographic verification is performed by GitHub CLI and Cosign in the workflow.
This utility validates their recorded results, artifact/evidence digests, source
identity, evidence linkage, and the demonstration-only policy boundary.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
RELEASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$")


class PolicyError(Exception):
    """Raised when evidence fails a release policy requirement."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyError(f"cannot read valid JSON from {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PolicyError(f"{path} must contain a JSON object")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PolicyError(message)


def resolve_evidence_file(root: Path, relative: str) -> Path:
    require(isinstance(relative, str) and relative.strip() != "", "evidence path is required")
    posix = PurePosixPath(relative)
    require(not posix.is_absolute(), f"absolute evidence path is forbidden: {relative}")
    require(".." not in posix.parts, f"path traversal is forbidden: {relative}")
    candidate = root.joinpath(*posix.parts)
    require(candidate.is_file(), f"evidence file is missing: {relative}")
    resolved_root = root.resolve()
    resolved = candidate.resolve()
    require(resolved.is_relative_to(resolved_root), f"evidence path escapes evidence root: {relative}")
    require(not candidate.is_symlink(), f"symlink evidence is forbidden: {relative}")
    return resolved


def verify_evidence_file(root: Path, record: dict[str, Any], label: str) -> str:
    path = resolve_evidence_file(root, record.get("path", ""))
    expected = record.get("sha256", "")
    require(isinstance(expected, str) and SHA256_RE.fullmatch(expected), f"{label}: invalid evidence SHA-256")
    actual = sha256_file(path)
    require(actual == expected, f"{label}: evidence file digest mismatch")
    return actual


def validate_manifest(manifest: dict[str, Any], policy: dict[str, Any], artifact_path: Path, evidence_root: Path,
                      expected_source_revision: str | None = None, expected_run_id: str | None = None,
                      expected_run_attempt: str | None = None) -> dict[str, Any]:
    require(manifest.get("schema_version") == 1, "unsupported manifest schema_version")
    require(policy.get("schema_version") == 1, "unsupported policy schema_version")

    release_id = manifest.get("release_id", "")
    require(isinstance(release_id, str) and RELEASE_ID_RE.fullmatch(release_id), "invalid release_id")
    require(manifest.get("release_classification") == policy.get("release_classification"),
            "release classification does not match policy")
    require(manifest.get("release_classification") == "synthetic-training-fixture",
            "this validator is currently scoped to synthetic training fixtures only")

    source = manifest.get("source")
    artifact = manifest.get("artifact")
    evidence = manifest.get("evidence")
    require(isinstance(source, dict), "source object is required")
    require(isinstance(artifact, dict), "artifact object is required")
    require(isinstance(evidence, dict), "evidence object is required")

    expected_source = policy.get("source", {})
    for field in ("repository", "ref", "workflow"):
        require(source.get(field) == expected_source.get(field), f"source {field} is not allow-listed")
    revision = source.get("revision", "")
    require(isinstance(revision, str) and GIT_SHA_RE.fullmatch(revision), "source revision must be a full Git SHA")
    if expected_source_revision is not None:
        require(revision == expected_source_revision, "manifest source revision differs from the workflow event SHA")
    require(manifest.get("run_id") not in (None, ""), "workflow run_id is required")
    require(manifest.get("run_attempt") not in (None, ""), "workflow run_attempt is required")
    if expected_run_id is not None:
        require(str(manifest["run_id"]) == str(expected_run_id), "manifest run_id differs from the current workflow run")
    if expected_run_attempt is not None:
        require(str(manifest["run_attempt"]) == str(expected_run_attempt), "manifest run_attempt differs from the current workflow attempt")

    require(artifact_path.is_file(), "release artifact is missing")
    actual_artifact_digest = sha256_file(artifact_path)
    declared_digest = artifact.get("sha256", "")
    require(isinstance(declared_digest, str) and SHA256_RE.fullmatch(declared_digest),
            "artifact SHA-256 is invalid")
    require(actual_artifact_digest == declared_digest, "release artifact digest mismatch")
    require(artifact.get("name") == artifact_path.name, "artifact name does not match the supplied file")
    require(artifact.get("kind") == "synthetic-training-fixture", "unexpected artifact kind")

    required = ("sbom", "sca", "slsa_provenance", "cosign_signature")
    for name in required:
        require(isinstance(evidence.get(name), dict), f"required evidence record is missing: {name}")

    sbom = evidence["sbom"]
    require(sbom.get("status") == "verified", "SBOM evidence is not verified")
    require(sbom.get("subject_sha256") == actual_artifact_digest,
            "SBOM is not bound to the exact release artifact digest")
    required_scope = policy.get("sbom", {}).get("required_generation_scope", "extracted-release-artifact")
    require(sbom.get("generation_scope") == required_scope,
            "SBOM was not generated from the extracted release artifact")
    accepted_formats = policy.get("sbom", {}).get("accepted_formats", ["CycloneDX 1.7", "SPDX 2.3"])
    require(sbom.get("format") in accepted_formats, "unsupported SBOM format")
    sbom_digest = verify_evidence_file(evidence_root, sbom, "SBOM")
    package_count = sbom.get("package_count")
    require(isinstance(package_count, int) and package_count >= 0, "SBOM package_count must be a non-negative integer")

    sca = evidence["sca"]
    require(sca.get("subject_sha256") == actual_artifact_digest,
            "SCA record is not bound to the exact release artifact digest")
    require(sca.get("sbom_sha256") == sbom_digest, "SCA report does not identify the exact SBOM document")
    require(sca.get("scanner") == "Grype", "unexpected SCA scanner")
    require(isinstance(sca.get("scanner_version"), str) and sca["scanner_version"], "SCA scanner version is required")
    sca_digest = verify_evidence_file(evidence_root, sca, "SCA report")
    sca_status = sca.get("scan_status")
    created_at = manifest.get("created_at")
    require(isinstance(created_at, str), "manifest created_at timestamp is required")
    try:
        manifest_time = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PolicyError("manifest created_at is not ISO-8601") from exc
    require(manifest_time.tzinfo is not None, "manifest created_at must include a timezone")
    database_evidence = None
    if package_count == 0:
        require(policy.get("sca", {}).get("allow_empty_inventory_for_demo") is True,
                "empty SBOM inventory is not permitted by policy")
        require(sca_status == "not_run_no_package_records",
                "empty inventory must be explicitly recorded as not scanned")
        require(sca.get("disposition") == "not_evaluated_no_package_records",
                "empty inventory must not be described as vulnerability-free")
        require(sca.get("match_count") is None, "match_count must be null when no scan was run")
    else:
        require(sca_status == "completed_report_only", "SCA scan did not complete")
        require(isinstance(sca.get("match_count"), int) and sca["match_count"] >= 0,
                "SCA match_count must be a non-negative integer")
        require(sca.get("threshold_enforced") is False,
                "this demonstration does not implement a production severity threshold")
        database = sca.get("database")
        require(isinstance(database, dict), "completed SCA evidence must include database metadata")
        require(database.get("valid") is True, "Grype vulnerability database is not valid")
        require(isinstance(database.get("schema_version"), str) and database["schema_version"],
                "Grype database schema version is required")
        built_at = database.get("built_at")
        require(isinstance(built_at, str), "Grype database build timestamp is required")
        status_path = database.get("status_path")
        status_sha = database.get("status_sha256")
        status_file = resolve_evidence_file(evidence_root, status_path)
        verify_evidence_file(evidence_root, {"path": status_path, "sha256": status_sha}, "Grype database status")
        status_fields = {}
        for line in status_file.read_text(encoding="utf-8").splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                status_fields[key.strip().lower()] = value.strip()
        require(status_fields.get("status", "").lower() == "valid", "Grype database status file is not valid")
        require(status_fields.get("schema") == database["schema_version"],
                "Grype database schema does not match status evidence")
        require(status_fields.get("built") == built_at, "Grype database build time does not match status evidence")
        try:
            database_time = datetime.fromisoformat(built_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise PolicyError("Grype database build timestamp is not ISO-8601") from exc
        require(database_time.tzinfo is not None, "Grype database build timestamp must include a timezone")
        max_age_hours = policy.get("sca", {}).get("max_database_age_hours", 72)
        age_seconds = (manifest_time - database_time).total_seconds()
        require(age_seconds >= 0, "Grype database build timestamp is in the future")
        require(age_seconds <= max_age_hours * 3600, "Grype vulnerability database is stale")
        database_evidence = {"schema_version": database["schema_version"], "built_at": built_at,
                             "valid": True, "status_sha256": status_sha}

    provenance = evidence["slsa_provenance"]
    require(provenance.get("status") == "verified", "SLSA provenance was not verified")
    require(provenance.get("subject_sha256") == actual_artifact_digest,
            "SLSA provenance subject digest does not match the release artifact")
    require(provenance.get("verification_method") == "gh-attestation-verify",
            "SLSA provenance must be verified by GitHub CLI")
    require(provenance.get("signer_workflow") == policy["provenance"]["signer_workflow"],
            "SLSA signer workflow is not allow-listed")
    require(provenance.get("oidc_issuer") == policy["provenance"]["oidc_issuer"],
            "SLSA OIDC issuer is not trusted")
    require(provenance.get("predicate_type") == "https://slsa.dev/provenance/v1",
            "unexpected SLSA predicate type")
    for field in ("source_repository", "source_ref", "source_revision"):
        expected = {"source_repository": source["repository"], "source_ref": source["ref"],
                    "source_revision": revision}[field]
        require(provenance.get(field) == expected, f"SLSA provenance {field} mismatch")
    provenance_digest = verify_evidence_file(evidence_root, provenance, "SLSA attestation bundle")

    signature = evidence["cosign_signature"]
    require(signature.get("status") == "verified", "Cosign signature was not verified")
    require(signature.get("subject_sha256") == actual_artifact_digest,
            "Cosign signature subject digest does not match the release artifact")
    require(signature.get("verification_method") == "cosign-verify-blob",
            "Cosign signature must be verified with cosign verify-blob")
    require(signature.get("signer_identity") == policy["cosign"]["certificate_identity"],
            "Cosign signer identity is not allow-listed")
    require(signature.get("oidc_issuer") == policy["cosign"]["oidc_issuer"],
            "Cosign OIDC issuer is not trusted")
    for field, expected in (("source_repository", source["repository"]),
                            ("source_ref", source["ref"]),
                            ("source_revision", revision)):
        require(signature.get(field) == expected, f"Cosign {field} mismatch")
    signature_digest = verify_evidence_file(evidence_root, signature, "Cosign signature bundle")

    run_identity = (str(manifest["run_id"]), str(manifest["run_attempt"]))
    for label, record in (("SBOM", sbom), ("SCA", sca), ("SLSA", provenance), ("Cosign", signature)):
        require((str(record.get("run_id")), str(record.get("run_attempt"))) == run_identity,
                f"{label} evidence comes from a different workflow run or attempt")

    return {
        "schema_version": 1,
        "release_id": release_id,
        "release_classification": "synthetic-training-fixture",
        "artifact": {"name": artifact["name"], "sha256": actual_artifact_digest},
        "source": {"repository": source["repository"], "ref": source["ref"], "revision": revision,
                   "workflow": source["workflow"]},
        "evidence": {
            "sbom": {"status": "verified", "sha256": sbom_digest, "format": sbom["format"],
                     "package_count": package_count},
            "sca": {"status": sca_status, "sha256": sca_digest, "match_count": sca.get("match_count"),
                    "disposition": sca["disposition"], "database": database_evidence},
            "slsa_provenance": {"status": "verified", "bundle_sha256": provenance_digest,
                                "signer_workflow": provenance["signer_workflow"]},
            "cosign_signature": {"status": "verified", "bundle_sha256": signature_digest,
                                 "signer_identity": signature["signer_identity"]},
        },
        "policy_decision": "DEMO_PASS_NOT_FOR_PRODUCTION",
        "promotion_authorized": False,
        "limitations": [
            "This is a synthetic training fixture, not a production release.",
            "Cryptographic attestation and signature checks were performed by GitHub CLI and Cosign before this policy validator ran.",
            "The SCA result is report-only; no production severity threshold or release exception process is enforced.",
            "A successful demonstration does not establish a SLSA Build level or production builder assurance."
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="validate release evidence and write a decision report")
    validate.add_argument("--manifest", type=Path, required=True)
    validate.add_argument("--policy", type=Path, required=True)
    validate.add_argument("--artifact", type=Path, required=True)
    validate.add_argument("--evidence-root", type=Path, required=True)
    validate.add_argument("--output", type=Path, required=True)
    validate.add_argument("--expected-source-revision", required=True)
    validate.add_argument("--expected-run-id", required=True)
    validate.add_argument("--expected-run-attempt", required=True)
    args = parser.parse_args()

    try:
        result = validate_manifest(
            load_json(args.manifest),
            load_json(args.policy),
            args.artifact,
            args.evidence_root,
            expected_source_revision=args.expected_source_revision,
            expected_run_id=args.expected_run_id,
            expected_run_attempt=args.expected_run_attempt,
        )
    except PolicyError as exc:
        print(f"RELEASE POLICY REJECTED: {exc}", file=sys.stderr)
        return 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("RELEASE POLICY: DEMO_PASS_NOT_FOR_PRODUCTION")
    print(f"Artifact SHA-256: {result['artifact']['sha256']}")
    print("All four evidence records reference the exact artifact digest.")
    print("Promotion authorized: false")
    print(f"Decision report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
