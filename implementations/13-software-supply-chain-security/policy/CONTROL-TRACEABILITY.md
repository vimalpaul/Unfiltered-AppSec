# Implementation Traceability — Initial Baseline

This is a deliberately narrow implementation slice. Control IDs below must be reconciled to the canonical Chapter 13 control register during the next traceability review; no control is considered fully effective merely because this implementation exists.

| Implementation asset | Security intent | Evidence produced | Not covered |
|---|---|---|---|
| `.github/workflows/supply-chain-baseline.yml` | Read-only CI execution, exact event-SHA checkout, short token exposure | Workflow run, event SHA, test log | Branch protection, trusted build, SLSA provenance, deployment |
| `scripts/release_manifest.py` | Detect source file additions, removals and modifications relative to a recorded manifest | Deterministic SHA-256 manifest and verification output | Component/package inventory, dependency identity, SBOM, signature, provenance |
| `tests/test_release_manifest.py` | Validate deterministic behavior and tamper detection | Unit-test results | Independent security review and production testing |
| `policy/release-policy.md` | Define release evidence expectations and fail-closed conditions | Reviewed policy document | Technical enforcement in GitHub/cloud/runtime |
| `.github/workflows/sbom-generation.yml` | Generate CycloneDX 1.7 and SPDX 2.3, conditionally scan SPDX with pinned Grype, and retain report-only evidence | [Successful run 44755935644](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755935644); uploaded artifact ID `14636948729` | Actual product build/image coverage, VEX, severity enforcement, provenance and signature |
| `sbom/validate_sbom.py` and `sbom/test_validate_sbom.py` | Check required top-level format and metadata fields | Unit tests and successful workflow validation | Full official JSON Schema validation and independent review |
| `sca/validate_grype_report.py` and `sca/test_validate_grype_report.py` | Check Grype report structure before evidence retention | Three unit tests and successful scan validation | Finding correctness, exploitability, reachability and independent review |

## Assurance state

- Authored: yes.
- Committed: yes; files are present on `main`.
- Workflow executed: successful on main-branch push at commit `63223ad4b6c6103f91d463fd60262b82fc2f0717`; [GitHub Actions run 44755594677](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755594677) reports all steps successful.
- Independently validated: no; CI execution is not an independent assessment.
- Production enforcement: no.

- SBOM workflow executed: successful on main at commit `15c7c9af17cbd1f5145fd151c09467164bd105b9`; [run 44755935644](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755935644). Artifact ID `14636948729`, digest `sha256:295bd0d6cb116cd4f7c7cf1919664eff276efde802d1969284c629d193bd9446`, expiry 2026-12-04.

- Grype SCA execution: successful on commit `e779b0db5fa1066a2e781e21d55c16045baf52ba`; [run 44756774695](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44756774695). Syft identified 2 SPDX package records; Grype v0.122.1 used a valid vulnerability DB (schema 6.1.10, built 2026-11-20) and reported 0 vulnerability matches. Artifact ID `14638375912`, digest `sha256:561b150ce7f9696fb6c43a1729c18d84ef0884f1c07c310f92e6dfc123d71b25`. This is a repository-filesystem scan, report-only, not an application-release assurance result.
