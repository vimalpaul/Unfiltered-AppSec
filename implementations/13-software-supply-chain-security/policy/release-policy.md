# Initial Release Evidence Policy

**Status:** Proposed baseline; not an enforced production policy.

## Required evidence before a production release

1. Approved source revision and review record.
2. Dependency inventory and vulnerability disposition for direct and transitive components.
3. SPDX or CycloneDX SBOM generated from the actual release artifact/build, with a digest linking the SBOM to that artifact.
4. Build provenance identifying source revision, builder identity, build definition and artifact digest.
5. Artifact signature or attestation verified against an explicitly approved identity, issuer and trust policy.
6. Test, SAST, SCA, secret-scanning and container/IaC results where applicable, with documented exceptions and expiry.
7. Release approval by an authorized role and a tested rollback/revocation path.
8. Retained, access-controlled release evidence and an incident contact.

## Fail-closed conditions

Block promotion when:
- the artifact digest differs between build, SBOM, provenance, signature or deployment;
- the signer or builder identity is not allow-listed;
- required provenance is missing or cannot be verified;
- a policy-defined vulnerability threshold is exceeded without an approved, time-bound exception;
- a critical dependency is unmaintained or its source cannot be established;
- required review or release authorization is absent.

## Exception record

Each exception must include a unique ID, affected product and artifact digest, control/test ID, risk rationale, compensating controls, approver, creation date, expiry date, remediation owner and closure evidence. An exception is not a silent pass.

## Enforcement boundary

This document does not configure GitHub rulesets, branch protection, environment protection, cloud IAM or deployment admission. Repository owners must configure and independently test those controls. Do not claim enforcement based only on this policy file.
