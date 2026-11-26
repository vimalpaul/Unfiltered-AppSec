# Chapter 13 — Software Supply-Chain Security Implementation Pack

| Field | Value |
|---|---|
| Status | Executable prototype baseline — not production assurance |
| Scope | Read-only CI, source integrity manifest, CycloneDX/SPDX SBOM generation, report-only SCA, OpenVEX validation, signed SLSA provenance, Cosign keyless artifact signing and release evidence policy |
| Safety | No production credentials, long-lived signing keys or deployment access; Syft, Grype and Cosign are version/digest pinned, and Cosign's Sigstore release bundle is verified |
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
- `signing/` — Cosign v3.1.6 release pin, keyless signing policy, signing fixture tests and GitHub OIDC signature workflow.
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

## 5. Workflow trust model

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
| SLSA build provenance | Synthetic artifact, separate build/sign jobs, GitHub Sigstore-signed SLSA provenance, exact signer/source/digest verification and three negative tests passed | [Run 45790878803](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/45790878803); attestation [72577521](https://github.com/vimalpaul/Unfiltered-AppSec/attestations/72577521); evidence artifact `15103185028` (expires 2026-12-10). Synthetic only; no SLSA level or production assurance claim |
| Artifact signing / verification | Cosign v3.1.6 keyless blob signing, Sigstore bundle verification and four negative tests passed on a synthetic artifact | [Cosign run 45791994671](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/45791994671); evidence artifact `15103446197` (expires 2026-12-10); production signing and release integration remain open |
| Container hardening / scanning | Not implemented | Add actual image build, digest pinning, scanning and deployment verification |
| Branch protection / rulesets | Not verified | Read effective repository rules and test enforcement with an authorized change |

A committed file is not proof that a GitHub setting is enabled. A green workflow is not proof that all supply-chain risks are controlled. Update this table only when the corresponding evidence exists.

## 7. Next implementation increments

1. Add and verify pull-request trigger coverage; review artifact access and retention settings.
2. Add project-specific build and dependency discovery without assuming a language or package manager.
3. Extend SBOM generation to the actual application build/image and bind each SBOM to the exact artifact digest; add full schema validation and package inventory reconciliation.
4. Connect real product scanner findings to reviewed OpenVEX records, VEX signing, evidence retention, VEX status updates and product-specific release gates.
5. Independently review the synthetic SLSA workflow, then adapt its separate build/sign pattern to a real application build with complete materials capture.
6. Assess GitHub-hosted and self-hosted builders against every applicable SLSA Build requirement; do not infer Build L2/L3 from a successful attestation.
7. Implement separate artifact signing/verification for actual release outputs, then container and deployment enforcement after the real build/deploy architecture is established.

## 8. Safe-use restrictions

Do not put customer source, private package credentials, production tokens, signing keys, cloud credentials or non-public architecture data in this public repository. Run compromise exercises only against synthetic dependencies and disposable environments.

## 9. SLSA provenance execution evidence

The synthetic SLSA workflow completed successfully on 2026-11-26: [run 45790878803](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/45790878803), source commit `1a81f191a3a1e8b23962e1ad4a9b90b6694d763c`. The build job passed 8 unit tests, fetched the exact event commit, created a deterministic archive and uploaded it to a separate attestation job. The attestation job verified the metadata and artifact SHA-256 `890a3bb79f8a6695b50a20860ce37404944ef4f21cc1c7ece1386a87eef84909`, generated a GitHub Sigstore-signed SLSA provenance attestation, and verified the signature, repository, signer workflow, source ref, source digest, OIDC issuer, predicate type and hosted-runner requirement with GitHub CLI.

The verified builder identity was `https://github.com/vimalpaul/Unfiltered-AppSec/.github/workflows/slsa-build-provenance.yml@refs/heads/main`; build type was `https://actions.github.io/buildtypes/workflow/v1`. The signature was uploaded to the Sigstore transparency log (Rekor log index `4122760007`) and GitHub attestation ID `72577521`. Three negative tests passed: modified artifact rejected, incorrect signer workflow rejected, and incorrect source commit rejected.

The retained evidence artifact is ID `15103185028`, digest `sha256:694058beb9ac19cc9aa8331867de489d90d399e66f49af1171ce7c19809ea87e`, with GitHub retention through 2026-12-10. This is a successful synthetic workflow demonstration, not an independent SLSA assessment, a production application build, or a claim of Build L2/L3.


## 10. Cosign artifact-signing execution evidence

The synthetic Cosign workflow completed successfully on 2026-11-26: [run 45791994671](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/45791994671), source commit `e04b39fdf72bc8ee4c51c8a6668cda3db302bcb1`. The build job passed two signing-fixture tests, fetched the exact event commit, and generated the deterministic synthetic archive. The separate signing job verified the build metadata and archive digest, checked the pinned Cosign v3.1.6 binary and its Sigstore release bundle, and verified the binary using the official release signer identity before installation.

Cosign signed the archive using a short-lived GitHub OIDC identity and created `cosign-signature.sigstore.json`. Verification passed for the exact certificate identity, OIDC issuer, repository, source ref, source commit and workflow trigger. Four negative tests rejected a modified blob, incorrect signer identity, incorrect OIDC issuer and incorrect source revision.

- Artifact SHA-256: `efe0d00c0552e89029750baf35b7620842a9a447b188f0d50f25473e8d8c69ac`
- Cosign version: `v3.1.6`
- Evidence artifact ID: `15103446197`
- Evidence artifact digest: `sha256:bf1cc7ac71b2cea025133d660cb25392fe42dd48686c7dfce2140f7795941747`
- Evidence retention: through 2026-12-10.

This demonstrates a detached signature over a synthetic file. It is not a production signing deployment, key-management assessment, SLSA level claim or release gate.
