# Implementation Traceability — Initial Baseline

This is a deliberately narrow implementation slice. Control IDs below must be reconciled to the canonical Chapter 13 control register during the next traceability review; no control is considered fully effective merely because this implementation exists.

| Implementation asset | Security intent | Evidence produced | Not covered |
|---|---|---|---|
| `.github/workflows/supply-chain-baseline.yml` | Read-only CI execution, exact event-SHA checkout, short token exposure | Workflow run, event SHA, test log | Branch protection, trusted build, SLSA provenance, deployment |
| `scripts/release_manifest.py` | Detect source file additions, removals and modifications relative to a recorded manifest | Deterministic SHA-256 manifest and verification output | Component/package inventory, dependency identity, SBOM, signature, provenance |
| `tests/test_release_manifest.py` | Validate deterministic behavior and tamper detection | Unit-test results | Independent security review and production testing |
| `policy/release-policy.md` | Define release evidence expectations and fail-closed conditions | Reviewed policy document | Technical enforcement in GitHub/cloud/runtime |
| `.github/workflows/sbom-generation.yml` | Generate CycloneDX 1.7 and SPDX 2.3 from the exact source commit | [Successful run 44755935644](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755935644); uploaded artifact ID `14636948729` | Actual product build/image coverage, SCA, VEX, provenance and signature |
| `sbom/validate_sbom.py` and `sbom/test_validate_sbom.py` | Check required top-level format and metadata fields | Unit tests and successful workflow validation | Full official JSON Schema validation and independent review |

## Assurance state

- Authored: yes.
- Committed: only after the repository write is confirmed.
- Workflow executed: successful on main-branch push at commit `63223ad4b6c6103f91d463fd60262b82fc2f0717`; [GitHub Actions run 44755594677](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755594677) reports all steps successful.
- Independently validated: no; CI execution is not an independent assessment.
- Production enforcement: no.
\n- SBOM workflow executed: successful on main at commit `15c7c9af17cbd1f5145fd151c09467164bd105b9`; [run 44755935644](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755935644). Artifact ID `14636948729`, digest `sha256:295bd0d6cb116cd4f7c7cf1919664eff276efde802d1969284c629d193bd9446`, expiry 2026-12-04.\n