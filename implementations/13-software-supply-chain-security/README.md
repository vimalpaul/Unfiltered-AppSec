# Chapter 13 — Software Supply-Chain Security Implementation Pack

| Field | Value |
|---|---|
| Status | Initial implementation baseline — not production assurance |
| Scope | Read-only CI, source integrity manifest, CycloneDX/SPDX SBOM generation, report-only SCA, OpenVEX validation, signed SLSA build provenance prototype and release evidence policy |
| Safety | No production credentials, signing keys or deployment access; only pinned Syft/Grype scanner binaries are downloaded and SHA-256 checked |
| Related engineering baseline | [Chapter 13 engineering](../../docs/13-software-supply-chain-security/SOFTWARE-SUPPLY-CHAIN-SECURITY-ENGINEERING.md) |
| Related labs | [Chapter 13 lab pack](../../docs/13-software-supply-chain-security/SOFTWARE-SUPPLY-CHAIN-SECURITY-LAB-PACK.md) |

## 1. Purpose

This directory translates Chapter 13 controls into executable repository assets. The baseline uses low-privilege GitHub Actions jobs, a pinned artifact-upload Action, and pinned Syft/Grype scanner binaries whose downloaded archives are checked against recorded SHA-256 digests. It does not install application dependencies or use deployment credentials or signing keys.

The first implementation proves only that:
- the workflow can retrieve the exact event commit using a short-lived, read-only repository token;
- the repository's Python evidence utility passes its unit tests;
- a deterministic SHA-256 source-file manifest can be generated and checked against the current checkout.

It does **not** prove that the application builds securely, that dependencies are vulnerability-free, that an SBOM is complete, that provenance meets SLSA, that artifacts are signed, or that branch protection is enabled.

## 2. Contents

- `.github/workflows/supply-chain-baseline.yml` — minimal-permission CI validation workflow; no external Actions are invoked.
- `.github/workflows/sbom-generation.yml` — pinned Syft SBOM generation, structural validation and artifact upload; the upload Action is pinned to a full commit SHA.
- `sbom/` — Syft version/digest record, SBOM scope notes, validator and validator unit tests.
- `sca/` — Grype version/digest record, report validator and SCA unit tests.
- `vex/` — OpenVEX v0.2.0 core validator, synthetic fixtures, policy tests, internal decision-record template and production-record intake directory.
- `provenance/` — deterministic synthetic artifact builder, metadata/digest verifier, unit tests, expected verification policy and GitHub signed provenance workflow.
- `scripts/release_manifest.py` — generate and verify a deterministic SHA-256 file-integrity manifest.
- `tests/test_release_manifest.py` — unit tests for path handling, tamper detection and deterministic output.
- `policy/release-policy.md` — release evidence gates and operational configuration checklist.

## 3. Prerequisites

- GitHub-hosted Ubuntu runner for the included workflow.
- Python 3.10+ for local execution.
- Git available in PATH.
- A local clone of this repository for developer use.

No Python packages are required; the utility uses only the Python standard library.

## 4. Run locally

From the repository root:

```bash
python scripts/release_manifest.py generate --root . --output dist/release-manifest.json
python scripts/release_manifest.py verify --root . --manifest dist/release-manifest.json
python -m unittest discover -s tests -v
```

The manifest excludes the `.git` directory and the manifest output itself. It records repository-relative file paths, byte sizes and SHA-256 digests. It refuses symbolic links and paths that resolve outside the selected root. It is an integrity inventory, **not an SPDX or CycloneDX SBOM**.

## 5. CI trust model

The workflow:
- runs on pull requests and pushes to `main`;
- grants only `contents: read`;
- uses Git directly rather than third-party checkout/upload Actions;
- exposes the built-in token only to the checkout step;
- fetches the exact event SHA and checks it out detached;
- executes repository-controlled tests with no deployment or signing secrets;
- does not publish artifacts or deploy anything.

Treat all code in a pull request as untrusted. Do not add secrets, privileged self-hosted runners, write permissions, deployment environments or privileged workflow triggers to this validation job.

## 6. Maturity and evidence

| Capability | State | Evidence required to advance |
|---|---|---|
| Read-only CI workflow authored | Implemented in repository | Successful main-branch push run: [run 44755594677](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755594677); PR-triggered validation remains pending |
| Deterministic file integrity manifest | Implemented in code | Unit tests plus CI run; review generated manifest semantics |
| SPDX/CycloneDX SBOM | Implemented for this repository filesystem using pinned Syft 1.57.1; CI passed and uploaded two SBOM formats | [Run 44755935644](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755935644); actual product-release SBOM and full schema validation remain open |
| VEX disposition | OpenVEX v0.2.0 core validator, not-affected justification checks, affected action-statement checks and conservative release-gate prototype; CI passed | [VEX run 44764156909](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44764156909); no production VEX record exists and full official schema/JSON-LD validation is not implemented |
| SCA vulnerability matching | Implemented as a report-only Grype scan of the generated SPDX SBOM; main-branch CI passed with 2 package records and 0 matches | [Run 44757253987](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44757253987); no severity threshold or release gate is enforced |
| SLSA build provenance | Synthetic artifact, isolated attestation job, GitHub Sigstore attestation and exact signer/digest verification workflow authored; execution pending | [Implementation guide](provenance/README.md); require successful run, signed bundle, CLI verification and negative tests before marking executed; no SLSA level claim |
| Artifact signing / verification | Not implemented | Establish trust policy, sign in a controlled test environment and verify negative cases |
| Container hardening / scanning | Not implemented | Add actual image build, digest pinning, scanning and deployment verification |
| Branch protection / rulesets | Not verified | Read effective repository rules and test enforcement with an authorized change |

A committed file is not proof that a GitHub setting is enabled. A green workflow is not proof that all supply-chain risks are controlled. Update this table only when the corresponding evidence exists.

## 7. Next implementation increments

1. Add and verify pull-request trigger coverage; review artifact access and retention settings.
2. Add project-specific build and dependency discovery without assuming a language or package manager.
3. Extend SBOM generation to the actual application build/image and bind each SBOM to the exact artifact digest; add full schema validation and package inventory reconciliation.
4. Connect real product scanner findings to reviewed OpenVEX records, VEX signing, evidence retention, VEX status updates and product-specific release gates.
5. Add provenance generation and verification against the actual builder identity.
6. Add signing and verification with a disposable test identity before defining production trust.
7. Add container and deployment policy only after the repository's real build/deploy architecture is known.

## 8. Safe-use restrictions

Do not put customer source, private package credentials, production tokens, signing keys, cloud credentials or non-public architecture data in this public repository. Run compromise exercises only against synthetic dependencies and disposable environments.
