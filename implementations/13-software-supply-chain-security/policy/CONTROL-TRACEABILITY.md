# Implementation Traceability — Initial Baseline

This is a deliberately narrow implementation slice. Control IDs below must be reconciled to the canonical Chapter 13 control register during the next traceability review; no control is considered fully effective merely because this implementation exists.

| Implementation asset | Security intent | Evidence produced | Not covered |
|---|---|---|---|
| `.github/workflows/supply-chain-baseline.yml` | Read-only CI execution, exact event-SHA checkout, short token exposure | Workflow run, event SHA, test log | Branch protection, trusted build, SLSA provenance, deployment |
| `scripts/release_manifest.py` | Detect source file additions, removals and modifications relative to a recorded manifest | Deterministic SHA-256 manifest and verification output | Component/package inventory, dependency identity, SBOM, signature, provenance |
| `tests/test_release_manifest.py` | Validate deterministic behavior and tamper detection | Unit-test results | Independent security review and production testing |
| `policy/release-policy.md` | Define release evidence expectations and fail-closed conditions | Reviewed policy document | Technical enforcement in GitHub/cloud/runtime |
| `.github/workflows/sbom-generation.yml` | Generate CycloneDX 1.7 and SPDX 2.3, conditionally scan SPDX with pinned Grype, and retain report-only evidence | [Successful run 44757253987](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44757253987); uploaded SBOM and Grype evidence artifact ID `14639231729` | Actual product build/image coverage, VEX, severity enforcement, provenance and signature |
| `sbom/validate_sbom.py` and `sbom/test_validate_sbom.py` | Check required top-level format and metadata fields | Unit tests and successful workflow validation | Full official JSON Schema validation and independent review |
| `sca/validate_grype_report.py` and `sca/test_validate_grype_report.py` | Check Grype report structure before evidence retention | Three unit tests and successful scan validation | Finding correctness, exploitability, reachability and independent review |
| `vex/validate_openvex.py` and `vex/test_validate_openvex.py` | Validate core OpenVEX v0.2.0 document/statement fields; require not-affected justification or impact statement; require affected action statement; apply conservative release policy | [VEX workflow 44764156909](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44764156909); 10 policy tests and synthetic document validation passed | Full official schema/JSON-LD validation, VEX signing, real finding mapping, product release enforcement and independent approval workflow |
| `vex/decision-record-template.json` | Capture scanner, product, artifact, component, exploitability, evidence, remediation, approval and lifecycle context | Versioned internal case template | No real product case has been populated or approved |

## Assurance state

- Authored: yes.
- Committed: yes; files are present on `main`.
- Workflow executed: successful on main-branch push at commit `63223ad4b6c6103f91d463fd60262b82fc2f0717`; [GitHub Actions run 44755594677](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755594677) reports all steps successful.
- Independently validated: no; CI execution is not an independent assessment.
- Production enforcement: no.

- SBOM workflow executed: successful on main at commit `15c7c9af17cbd1f5145fd151c09467164bd105b9`; [run 44755935644](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755935644). Artifact ID `14636948729`, digest `sha256:295bd0d6cb116cd4f7c7cf1919664eff276efde802d1969284c629d193bd9446`, expiry 2026-12-04.

- Grype SCA execution: successful on commit `bceba4b6b6fd26918b22a3198c8743b804fa9f53`; [run 44757253987](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44757253987). Syft identified 2 SPDX package records; Grype v0.122.1 used a valid vulnerability DB (schema 6.1.10, built 2026-11-20) and reported 0 vulnerability matches. Artifact ID `14639231729`, digest `sha256:cbdd4aa9592920fc044be122e2e62ab7a16a668fb3154a1f04b9d5bb824c1d7f`. This is a repository-filesystem scan, report-only, not an application-release assurance result.


- VEX validation workflow: successful on commit `5361f1b15979812e6ce7a471523a1e84d209ba56`; [run 44764156909](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44764156909). The job passed all 10 unit tests, validated the explicitly synthetic OpenVEX example, and confirmed that no production VEX record currently exists. This is CI evidence for the validator only; no product-level VEX decision was made.
