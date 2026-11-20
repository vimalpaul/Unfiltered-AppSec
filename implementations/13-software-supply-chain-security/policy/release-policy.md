# Initial Release Evidence Policy

**Status:** Proposed baseline; not an enforced production policy.

## Required evidence before a production release

1. Approved source revision and review record.
2. Dependency inventory and vulnerability disposition for direct and transitive components, with scanner source/database metadata retained.
3. A product-specific OpenVEX or equivalent VEX statement for material vulnerability dispositions, bound to the exact product/component identity and artifact digest; `under_investigation` and `affected` states must not be treated as release clearance.
4. SPDX or CycloneDX SBOM generated from the actual release artifact/build, with a digest linking the SBOM to that artifact.
5. Build provenance identifying source revision, builder identity, build definition and artifact digest.
6. Artifact signature or attestation verified against an explicitly approved identity, issuer and trust policy.
7. Test, SAST, SCA, secret-scanning and container/IaC results where applicable, with documented exceptions and expiry.
8. Release approval by an authorized role and a tested rollback/revocation path.
9. Retained, access-controlled release evidence and an incident contact.

## Fail-closed conditions

Block promotion when:
- the artifact digest differs between build, SBOM, provenance, signature or deployment;
- the signer or builder identity is not allow-listed;
- required provenance is missing or cannot be verified;
- a policy-defined vulnerability threshold is exceeded without an approved, time-bound exception;
- a material vulnerability remains `affected` or `under_investigation` without an explicitly approved risk acceptance that is permitted by policy;
- a `not_affected` disposition lacks a valid justification and evidence for the exact product artifact;
- a critical dependency is unmaintained or its source cannot be established;
- required review or release authorization is absent.

## Exception record

Each exception must include a unique ID, affected product and artifact digest, control/test ID, risk rationale, compensating controls, approver, creation date, expiry date, remediation owner and closure evidence. An exception is not a silent pass.

## Enforcement boundary

This document does not configure GitHub rulesets, branch protection, environment protection, cloud IAM or deployment admission. Repository owners must configure and independently test those controls. Do not claim enforcement based only on this policy file.

## VEX disposition requirements

- Use a recognized format and preserve its exact status semantics. The implementation baseline uses OpenVEX v0.2.0.
- Identify the product and vulnerability in every statement; retain a statement timestamp and document version.
- For `not_affected`, include a recognized machine-readable justification or an impact statement. Do not infer not-affected from zero scanner matches or missing reachability data.
- For `affected`, include an action statement describing remediation or mitigation.
- Keep `under_investigation` until the evidence supports a stronger status.
- Require independent review, evidence IDs, exact artifact digest, owner, next review date and re-evaluation triggers in the internal case record.
- Preserve superseded VEX statements and document version history. A new assessment supersedes rather than silently overwrites the prior decision.
