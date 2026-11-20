# Chapter 13 — Software Supply-Chain Security Implementation Pack

| Field | Value |
|---|---|
| Status | Initial implementation baseline — not production assurance |
| Scope | Repository checkout, read-only CI validation, deterministic source-file integrity manifest and release evidence verification |
| Safety | No production credentials, signing keys, deployment access or external package installation |
| Related engineering baseline | [Chapter 13 engineering](../../docs/13-software-supply-chain-security/SOFTWARE-SUPPLY-CHAIN-SECURITY-ENGINEERING.md) |
| Related labs | [Chapter 13 lab pack](../../docs/13-software-supply-chain-security/SOFTWARE-SUPPLY-CHAIN-SECURITY-LAB-PACK.md) |

## 1. Purpose

This directory starts translating the Chapter 13 controls into executable repository assets. It deliberately begins with a small, low-privilege baseline that can run in GitHub Actions without third-party Actions, package downloads, deployment credentials or signing keys.

The first implementation proves only that:
- the workflow can retrieve the exact event commit using a short-lived, read-only repository token;
- the repository's Python evidence utility passes its unit tests;
- a deterministic SHA-256 source-file manifest can be generated and checked against the current checkout.

It does **not** prove that the application builds securely, that dependencies are vulnerability-free, that an SBOM is complete, that provenance meets SLSA, that artifacts are signed, or that branch protection is enabled.

## 2. Contents

- `.github/workflows/supply-chain-baseline.yml` — minimal-permission CI validation workflow; no external Actions are invoked.
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
| SPDX/CycloneDX SBOM | Not implemented | Generate from a real release/build, validate schema and reconcile inventory |
| SCA and VEX | Not implemented | Select tools, configure policy, validate findings and dispositions |
| SLSA provenance / attestations | Not implemented | Select supported builder and verify attestation subject, source and builder identity |
| Artifact signing / verification | Not implemented | Establish trust policy, sign in a controlled test environment and verify negative cases |
| Container hardening / scanning | Not implemented | Add actual image build, digest pinning, scanning and deployment verification |
| Branch protection / rulesets | Not verified | Read effective repository rules and test enforcement with an authorized change |

A committed file is not proof that a GitHub setting is enabled. A green workflow is not proof that all supply-chain risks are controlled. Update this table only when the corresponding evidence exists.

## 7. Next implementation increments

1. Confirm workflow execution and capture run URL, commit SHA and test output.
2. Add project-specific build and dependency discovery without assuming a language or package manager.
3. Add Syft SBOM generation and schema validation, then bind the SBOM to an immutable artifact digest.
4. Add SCA policy, vulnerability disposition and VEX evidence.
5. Add provenance generation and verification against the actual builder identity.
6. Add signing and verification with a disposable test identity before defining production trust.
7. Add container and deployment policy only after the repository's real build/deploy architecture is known.

## 8. Safe-use restrictions

Do not put customer source, private package credentials, production tokens, signing keys, cloud credentials or non-public architecture data in this public repository. Run compromise exercises only against synthetic dependencies and disposable environments.
