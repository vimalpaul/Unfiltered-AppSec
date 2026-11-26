#!/usr/bin/env python3
"""Create a deterministic synthetic tar.gz artifact and a digest metadata record."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile
from typing import Any

REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_artifact(
    output: Path,
    metadata_output: Path,
    repository: str,
    revision: str,
    workflow: str,
) -> dict[str, Any]:
    if not REPOSITORY_RE.fullmatch(repository):
        raise ValueError("repository must be in owner/repository form")
    if not REVISION_RE.fullmatch(revision):
        raise ValueError("revision must be a full 40-character lowercase Git commit SHA")
    if not workflow.startswith(".github/workflows/") or ".." in Path(workflow).parts:
        raise ValueError("workflow must be a repository-relative .github/workflows path")

    build_info = {
        "artifact_kind": "synthetic-training-fixture",
        "build_definition": workflow,
        "source_repository": repository,
        "source_revision": revision,
    }
    payloads = {
        "README.txt": (
            "Unfiltered AppSec synthetic provenance fixture.\n"
            "This archive is not a production application or release.\n"
        ).encode("utf-8"),
        "build-info.json": (
            json.dumps(build_info, sort_keys=True, indent=2) + "\n"
        ).encode("utf-8"),
        "src/demo.txt": b"Synthetic source payload for supply-chain provenance testing.\n",
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as raw:
        import gzip

        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as archive:
                for name in sorted(payloads):
                    data = payloads[name]
                    info = tarfile.TarInfo(name=name)
                    info.size = len(data)
                    info.mode = 0o644
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    info.mtime = 0
                    archive.addfile(info, io.BytesIO(data))

    metadata = {
        "schema_version": 1,
        "artifact_name": output.name,
        "artifact_sha256": sha256_file(output),
        "artifact_kind": "synthetic-training-fixture",
        "source_repository": repository,
        "source_revision": revision,
        "build_workflow": workflow,
        "statement": "This metadata is a build-job check record, not a signed provenance statement.",
    }
    metadata_output.parent.mkdir(parents=True, exist_ok=True)
    metadata_output.write_text(
        json.dumps(metadata, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata-output", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--workflow", required=True)
    args = parser.parse_args()
    metadata = build_artifact(
        args.output,
        args.metadata_output,
        args.repository,
        args.revision,
        args.workflow,
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
