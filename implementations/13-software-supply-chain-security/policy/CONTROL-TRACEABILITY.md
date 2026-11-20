# Implementation Traceability — Initial Baseline

This is a deliberately narrow implementation slice. Control IDs below must be reconciled to the canonical Chapter 13 control register during the next traceability review; no control is considered fully effective merely because this implementation exists.

| Implementation asset | Security intent | Evidence produced | Not covered |
|---|---|---|---|
| `.github/workflows/supply-chain-baseline.yml` | Read-only CI execution, exact event-SHA checkout, short token exposure | Workflow run, event SHA, test log | Branch protection, trusted build, SLSA provenance, deployment |
| `scripts/release_manifest.py` | Detect source file additions, removals and modifications relative to a recorded manifest | Deterministic SHA-256 manifest and verification output | Component/package inventory, dependency identity, SBOM, signature, provenance |
| `tests/test_release_manifest.py` | Validate deterministic behavior and tamper detection | Unit-test results | Independent security review and production testing |
| `policy/release-policy.md` | Define release evidence expectations and fail-closed conditions | Reviewed policy document | Technical enforcement in GitHub/cloud/runtime |

## Assurance state

- Authored: yes.
- Committed: only after the repository write is confirmed.
- Workflow executed: pending GitHub Actions run.
- Independently validated: no.
- Production enforcement: no.
