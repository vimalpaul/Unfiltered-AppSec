# Implementation Traceability — Initial Baseline

This is a deliberately narrow implementation slice. The VEX assets below implement part of canonical control SSC-C-008 and provide an executable check for test SSC-T-011. The remaining implementation rows are evidence assets, not claims that their full canonical controls are effective. No control is considered fully effective merely because this implementation exists.

| Implementation asset | Security intent | Evidence produced | Not covered |
|---|---|---|---|
| `.github/workflows/supply-chain-baseline.yml` | Read-only CI execution, exact event-SHA checkout, short token exposure | Workflow run, event SHA, test log | Branch protection, trusted build, SLSA provenance, deployment |
| `scripts/release_manifest.py` | Detect source file additions, removals and modifications relative to a recorded manifest | Deterministic SHA-256 manifest and verification output | Component/package inventory, dependency identity, SBOM, signature, provenance |
| `tests/test_release_manifest.py` | Validate deterministic behavior and tamper detection | Unit-test results | Independent security review and production testing |
| `policy/release-policy.md` | Define release evidence expectations and fail-closed conditions | Reviewed policy document | Technical enforcement in GitHub/cloud/runtime |
| `.github/workflows/sbom-generation.yml` | Generate CycloneDX 1.7 and SPDX 2.3, conditionally scan SPDX with pinned Grype, and retain report-only evidence | [Successful run 44757253987](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44757253987); uploaded SBOM and Grype evidence artifact ID `14639231729` | Actual product build/image coverage, VEX, severity enforcement, provenance and signature |
| `sbom/validate_sbom.py` and `sbom/test_validate_sbom.py` | Check required top-level format and metadata fields | Unit tests and successful workflow validation | Full official JSON Schema validation and independent review |
| `sca/validate_grype_report.py` and `sca/test_validate_grype_report.py` | Check Grype report structure before evidence retention | Three unit tests and successful scan validation | Finding correctness, exploitability, reachability and independent review |
| `vex/validate_openvex.py` and `vex/test_validate_openvex.py` | Partial implementation of SSC-C-008; executable negative test for SSC-T-011; validate core OpenVEX v0.2.0 fields and apply conservative release policy | [VEX workflow 44764156909](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44764156909); 10 policy tests and synthetic document validation passed | Full official schema/JSON-LD validation, VEX signing, real finding mapping, product release enforcement and independent approval workflow |
| `vex/decision-record-template.json` | Capture scanner, product, artifact, component, exploitability, evidence, remediation, approval and lifecycle context | Versioned internal case template | No real product case has been populated or approved |
| `provenance/build_demo_artifact.py`, `provenance/verify_build_metadata.py` and `provenance/test_provenance.py` | Build a deterministic synthetic artifact; bind source repository/revision and SHA-256; reject digest/source/workflow mismatches | Eight unit tests in the isolated build job; metadata check repeated before attestation | Metadata is not signed provenance; no production application or complete dependency graph is built |
| `.github/workflows/slsa-build-provenance.yml` | Partial implementation of SSC-C-011, SSC-C-012 and SSC-C-013; executable evidence for SSC-T-016 (provenance generation), SSC-T-017 (artifact tampering) and SSC-T-019 (untrusted signer); generate signed SLSA provenance in a separate job, verify subject/source/signer, reject tampering | [Successful run 45790878803](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/45790878803); attestation [72577521](https://github.com/vimalpaul/Unfiltered-AppSec/attestations/72577521); evidence artifact `15103185028`; eight unit tests and three negative tests passed | No SLSA Build L2/L3 claim; no SSC-T-020 deployment enforcement, production artifact, hardened builder assessment or complete materials capture |
| `signing/` and `.github/workflows/cosign-artifact-signing.yml` | Partial implementation of SSC-C-012 and SSC-C-013; executable evidence for SSC-T-017 (tamper rejection), SSC-T-018 (approved identity signs exact artifact) and SSC-T-019 (untrusted signer rejection); use Cosign keyless blob signature and verify certificate identity, issuer, repository, ref and source SHA | [Successful run 45791448527](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/45791448527); Cosign v3.1.6 binary and release bundle verified; two fixture tests and four negative tests passed; evidence artifact `15101489683` | No production release signing, signing-service administration, revocation/recovery exercise, SLSA level claim or deployment gate |

## Assurance state

- Authored: yes.
- Committed: yes; files are present on `main`.
- Workflow executed: successful on main-branch push at commit `63223ad4b6c6103f91d463fd60262b82fc2f0717`; [GitHub Actions run 44755594677](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755594677) reports all steps successful.
- Independently validated: no; CI execution is not an independent assessment.
- Production enforcement: no.

- SBOM workflow executed: successful on main at commit `15c7c9af17cbd1f5145fd151c09467164bd105b9`; [run 44755935644](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755935644). Artifact ID `14636948729`, digest `sha256:295bd0d6cb116cd4f7c7cf1919664eff276efde802d1969284c629d193bd9446`, expiry 2026-12-04.

- Grype SCA execution: successful on commit `bceba4b6b6fd26918b22a3198c8743b804fa9f53`; [run 44757253987](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44757253987). Syft identified 2 SPDX package records; Grype v0.122.1 used a valid vulnerability DB (schema 6.1.10, built 2026-11-20) and reported 0 vulnerability matches. Artifact ID `14639231729`, digest `sha256:cbdd4aa9592920fc044be122e2e62ab7a16a668fb3154a1f04b9d5bb824c1d7f`. This is a repository-filesystem scan, report-only, not an application-release assurance result.


- VEX validation workflow: successful on commit `5361f1b15979812e6ce7a471523a1e84d209ba56`; [run 44764156909](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44764156909). The job passed all 10 unit tests, validated the explicitly synthetic OpenVEX example, and confirmed that no production VEX record currently exists. This is CI evidence for the validator only; no product-level VEX decision was made.


## SLSA provenance implementation status

- Authored: yes; deterministic synthetic artifact builder, metadata verifier, unit tests, verification policy and isolated signing workflow are committed.
- Action pin: `actions/attest` v4.2.2 at full commit `1e69f48acb82d1966a394da916b4c1698aa569d6`; upload/download actions are pinned to full commit SHAs.
- Build/sign separation: build job has `contents: read`; attestation job alone has `id-token: write` and `attestations: write`, and does not check out or execute repository build scripts.
- Workflow executed: successful on 2026-11-26; [run 45790878803](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/45790878803). Verified artifact digest `sha256:890a3bb79f8a6695b50a20860ce37404944ef4f21cc1c7ece1386a87eef84909`; attestation ID `72577521`; Rekor log index `4122760007`; evidence artifact `15103185028` (digest `sha256:694058beb9ac19cc9aa8331867de489d90d399e66f49af1171ce7c19809ea87e`, expires 2026-12-10).
- Independent validation: no.
- Negative tests: tampered artifact, untrusted signer workflow and incorrect source revision were rejected as expected.
- SLSA level: not claimed; Build L2/L3 assessment remains open.


## Cosign artifact-signing implementation status

- Authored: yes; Cosign v3.1.6 binary/release-bundle pins, keyless signing workflow, verification policy and signing tests are committed.
- Workflow executed: successful on 2026-11-26; [run 45791448527](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/45791448527).
- Artifact digest: `sha256:980a27c8160b2c654b21fec1f5abbe73d6017f3ad8b29755bd55804ed68cc290`.
- Evidence artifact: `15101489683`; digest `sha256:e8c60302c2c7a8362390aad561f8aaef28454fb197e404e6eeb71481f9cd9d3c`; expiry 2026-12-10.
- Negative tests: modified blob, wrong certificate identity, wrong OIDC issuer and wrong source revision rejected.
- Production signing and release enforcement: not implemented.
