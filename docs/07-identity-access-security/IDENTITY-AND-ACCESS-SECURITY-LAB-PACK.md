# Identity and Access Security Lab Pack

| Field | Value |
|---|---|
| Document ID | UAPPSEC-07-LAB-001 |
| Status | Draft lab specifications |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Isolated identity, authentication, federation and authorization exercises |
| Classification | Public |

## 1. Safety and prerequisites

These exercises are designed for local applications, synthetic identities and disposable identity-provider tenants. Do not target public identity providers, customer tenants, employee accounts or production directories.

Before each lab:
- Obtain permission from the owner of the local application and identity platform.
- Use a private isolated network or loopback-only services.
- Use synthetic users, tenants, groups, certificates and tokens.
- Do not send real password-reset emails, SMS or push notifications.
- Do not expose signing keys, client secrets, access tokens or refresh tokens in evidence.
- Do not use real production identity providers or employee accounts.
- Set resource and request limits.
- Snapshot or rebuild the environment before the exercise.
- Stop if a request leaves the lab network or a real credential is discovered.

The learner must explain the trust boundary, threat, expected result, evidence, remediation and regression test. A scanner result alone is not a complete lab submission.

## 2. Common lab record

Record learner, date, lab ID, app/IdP/library versions, isolated network confirmation, test identities and roles, protocol/configuration, prerequisites, reproduction steps, expected and observed result, root cause, applicable weakness, remediation diff, regression test, evidence location, teardown and reviewer outcome.

Never submit raw passwords, private keys, client secrets, bearer tokens, refresh tokens, session cookies, recovery codes or personal identity documents.

## 3. Lab 01: Authentication versus authorization

**Objective:** Demonstrate that successful authentication does not grant access to every object.

**Weakness:** Broken object-level authorization; relevant CWE may include CWE-862/CWE-863/CWE-639 depending on root cause.

**Prerequisites:** Local API, disposable database, two synthetic users and one synthetic tenant.

### Procedure

1. Create user A and user B with distinct synthetic identities.
2. Create one private record owned by each user.
3. Authenticate as user A and request user A's record.
4. Record the allowed result.
5. Authenticate as user A and request user B's record using the known synthetic test identifier.
6. Record whether the API checks only authentication or also the resource relationship.
7. Implement a service-level authorization check binding subject, action, resource and tenant.
8. Add a negative regression test for user A accessing user B's record.
9. Verify user B can still access their own record.
10. Inspect audit output for actor, resource, action, tenant and decision.

**Expected result:** User A can access only resources authorized by the application policy. A random or unguessable identifier is not treated as authorization.

**Evidence:** Test account matrix, redacted requests/responses, authorization code and regression results.

**Teardown:** Delete synthetic records and accounts.

## 4. Lab 02: OAuth authorization code with PKCE and state

**Objective:** Verify the authorization transaction is bound to the initiating client/browser and the code cannot be redeemed without the correct PKCE verifier.

**Prerequisites:** Local OIDC provider and test client configured for Authorization Code flow.

### Procedure

1. Configure one test client with an exact loopback redirect URI.
2. Start an authorization transaction and record generated state, nonce and PKCE challenge metadata without exposing production secrets.
3. Complete a normal authorization and confirm callback state matches the stored transaction.
4. Repeat with a deliberately mismatched state in the local lab.
5. Verify the client rejects the callback and does not establish a session.
6. Attempt code redemption without the correct PKCE verifier in the lab.
7. Verify the token endpoint rejects the request.
8. Test an unregistered redirect URI and confirm rejection.
9. Inspect the client configuration for wildcard redirect entries and remove them.
10. Add automated tests for state mismatch, missing/wrong PKCE verifier and redirect mismatch.

**Expected result:** Only the initiating transaction can complete. Authorization codes are bound to the client transaction through PKCE. Redirect destinations match the registered URI exactly.

**Evidence:** Client configuration, redacted protocol trace, negative test output and regression test.

**Teardown:** Delete test client and authorization grants.

## 5. Lab 03: JWT validation profile

**Objective:** Verify that the resource server validates the intended token profile, not merely decodes JWT claims.

**Prerequisites:** Local test issuer and API; synthetic signing key pair and test tokens.

### Procedure

1. Configure the API to trust one explicit issuer and audience.
2. Obtain a valid test access token for the intended API.
3. Confirm the API accepts the token and applies resource authorization.
4. Use synthetic test tokens with wrong issuer, wrong audience, expired time, invalid signature and disallowed algorithm.
5. Confirm each invalid token is rejected.
6. Test a token issued for a different resource server.
7. Review whether key URLs or key material supplied by token headers can override trusted issuer configuration.
8. Confirm logs record validation failure reason without logging raw token.
9. Add automated tests for issuer, audience, signature, algorithm and time validation.
10. Document key rotation and unknown-key behavior.

**Expected result:** Only correctly signed, time-valid tokens from the configured issuer and intended audience are accepted. Token decoding alone never grants access.

**Evidence:** Redacted token claim metadata, verifier configuration and test output.

**Teardown:** Destroy test keys and remove test issuer configuration.

## 6. Lab 04: Session fixation, rotation and logout

**Objective:** Verify session identifiers are rotated at authentication and revoked at logout.

**Prerequisites:** Local web application with cookie-based session.

### Procedure

1. Start a fresh browser profile and capture the pre-authentication session identifier in the local lab.
2. Authenticate as a synthetic user.
3. Verify the authenticated session identifier differs from the pre-authentication identifier.
4. Inspect cookie flags and scope.
5. Log out and replay the old authenticated cookie against the local application.
6. Verify server-side session state rejects the replay.
7. Change the synthetic user's password or disable the account and verify configured revocation behavior.
8. Inspect concurrent session and idle/absolute timeout policy.
9. Add regression tests for rotation, expiry and logout invalidation.

**Expected result:** Attacker-chosen/pre-authentication session IDs are not retained as authenticated sessions. Logout and configured risk events invalidate the session.

**Evidence:** Cookie metadata with values redacted, server session state and regression results.

**Teardown:** Clear local browser profile and delete test sessions.

## 7. Lab 05: Multi-tenant authorization and property-level control

**Objective:** Prevent cross-tenant access and mass assignment of privileged properties.

**Prerequisites:** Local API with tenant A, tenant B, tenant administrator and learner accounts.

| Identity | Tenant | Role |
|---|---|---|
| learner-a | tenant-a | learner |
| admin-a | tenant-a | tenant administrator |
| learner-b | tenant-b | learner |

### Procedure

1. Sign in as learner-a and read a resource in tenant A.
2. Request a synthetic resource in tenant B.
3. Submit a request containing a different tenant identifier.
4. Submit privileged properties such as role, owner, approval state or platform administrator flag.
5. Inspect database state and API response.
6. Implement tenant membership resolution from trusted server-side identity context.
7. Use explicit request DTOs containing only caller-writable fields.
8. Enforce object and property authorization in the service layer.
9. Add tenant-aware database query constraints and cache keys as defense in depth.
10. Repeat positive and negative tests, including search and export endpoints.

**Expected result:** Tenant A cannot access tenant B data; user-supplied tenant and role properties cannot alter privilege or ownership; allowed same-tenant actions continue to work.

**Evidence:** Before/after database state, test matrix, API responses and audit events.

**Teardown:** Remove synthetic tenants and records.

## 8. Lab 06: WebAuthn/passkey challenge and relying-party binding

**Objective:** Verify challenge freshness, origin/RP binding and credential-to-account association.

**Prerequisites:** Local HTTPS development origin, supported browser/authenticator and maintained WebAuthn server library.

### Procedure

1. Configure a local relying-party ID and allowed origin.
2. Register a passkey for a synthetic user.
3. Inspect stored credential metadata; do not export private key material.
4. Authenticate using the registered credential.
5. Replay an expired or previously consumed challenge in the isolated test harness.
6. Verify rejection.
7. Attempt the flow from a different origin or RP ID in a controlled test setup.
8. Verify rejection.
9. Test credential removal and lost-device recovery through the approved recovery workflow.
10. Add regression tests for challenge reuse, origin mismatch and account binding.

**Expected result:** Authentication succeeds only for the correct relying party, origin, fresh challenge and bound account. Private keys are never sent to the server.

**Evidence:** Redacted WebAuthn metadata, server configuration and test results.

**Teardown:** Remove test credentials and local relying-party configuration.

## 9. Lab 07: SAML assertion validation

**Objective:** Verify SAML responses are accepted only from trusted issuer, for the intended audience/recipient, within time bounds and with valid signature and request correlation.

**Prerequisites:** Local SAML IdP and service provider using maintained libraries and synthetic signing certificates.

### Procedure

1. Configure trusted IdP metadata and service-provider entity ID.
2. Complete a normal solicited login and record the expected issuer, audience, recipient and request correlation.
3. Submit a synthetic response with wrong audience.
4. Submit a synthetic response with expired conditions.
5. Submit a synthetic response with invalid signature.
6. Replay a previously accepted assertion ID.
7. Verify each invalid response is rejected.
8. Review XML parser and signature validation configuration.
9. Verify claim mapping does not grant privileged roles from untrusted attributes.
10. Add regression tests for audience, recipient, signature, expiry, replay and role mapping.

**Expected result:** Only a valid, trusted, correctly scoped and non-replayed assertion creates a session.

**Evidence:** Sanitized protocol metadata, trust configuration and negative test output.

**Teardown:** Destroy synthetic certificates and federation metadata.

## 10. Lab 08: Privileged access and JIT expiry

**Objective:** Verify privileged access requires approval and automatically expires.

**Prerequisites:** Local policy engine or test application with standard user, approver and privileged role.

### Procedure

1. Create a synthetic user without privileged access.
2. Attempt a privileged operation and confirm denial.
3. Submit a JIT request with reason, resource and duration.
4. Attempt self-approval and verify it is denied where separation is required.
5. Approve using a separate synthetic approver.
6. Confirm the grant is limited to the approved role and resource.
7. Advance a controlled test clock or use a short lab expiry.
8. Verify access is removed at expiry.
9. Attempt the operation again.
10. Verify audit events contain requester, approver, reason, scope, start/end and revocation result.

**Expected result:** No standing privilege is created; the grant is scoped, approved, time-bound and automatically revoked.

**Evidence:** Approval workflow, entitlement state, audit event and expiry test.

**Teardown:** Remove test grants and users.

## 11. Lab 09: Workload identity federation

**Objective:** Verify a workload can obtain credentials only from an explicitly trusted issuer, subject, audience and environment.

**Prerequisites:** Local/mock identity issuer and test resource server, or a dedicated disposable cloud tenant approved for training.

### Procedure

1. Define a test workload identity and intended resource audience.
2. Configure an explicit trust policy for a synthetic repository/workflow subject.
3. Request credentials from the approved test workload.
4. Verify the resource server accepts the correctly scoped token.
5. Change the subject to an unapproved repository or branch.
6. Change the audience to an unrelated resource.
7. Verify both requests are denied.
8. Inspect wildcard trust patterns and remove unnecessary broad matches.
9. Verify token lifetime and permission scope.
10. Add regression tests for subject, issuer, audience and environment claims.

**Expected result:** Only the approved workload context receives narrowly scoped short-lived credentials.

**Evidence:** Redacted trust policy, token metadata and test results.

**Teardown:** Revoke federation trust and destroy test keys.

## 12. Lab 10: Service identity inventory and deprovisioning

**Objective:** Demonstrate that retiring an employee or application owner does not leave service credentials and integrations orphaned.

**Prerequisites:** Local inventory, synthetic employee identity and two synthetic service identities.

### Procedure

1. Create a synthetic service identity with owner, purpose, application, environment, permission and expiry.
2. Create a second identity with missing owner/expiry to represent an inventory gap.
3. Run the inventory report and identify the orphan.
4. Simulate owner departure through an authoritative test event.
5. Identify owned jobs, API credentials, certificates and scheduled tasks.
6. Transfer ownership or retire the identity according to dependency and change-control requirements.
7. Revoke credentials and remove permissions.
8. Verify dependent service no longer authenticates with retired credentials.
9. Confirm audit evidence and exception records.
10. Add an automated report for identities with no owner, no recent use or expired review.

**Expected result:** Service identities have accountable ownership and retirement covers credentials, entitlements and dependent workloads.

**Evidence:** Inventory, owner-change event, revocation result and audit records.

**Teardown:** Delete test identities and credentials.

## 13. Lab 11: Identity incident response

**Objective:** Exercise coordinated response to synthetic account takeover.

**Prerequisites:** Local IdP, application logs, test user, synthetic token/session and incident ticket template.

### Scenario

A synthetic user reports an unexpected authenticator enrollment followed by a sensitive export. The learner must investigate and contain the event without using real credentials or data.

### Procedure

1. Identify the user, tenant, authentication events and affected session.
2. Preserve relevant identity-provider and application audit evidence.
3. Review authenticator enrollment, recovery changes, session creation and token issuance.
4. Revoke test sessions and credentials.
5. Disable the synthetic identity where appropriate.
6. Identify resources accessed and exports created.
7. Search for persistence such as new OAuth clients, API keys, service accounts or federation changes.
8. Restore the identity through a secure recovery flow.
9. Verify authorization and tenant boundaries.
10. Produce timeline, impact assessment, root cause, actions and lessons learned.

**Expected result:** Containment revokes active credentials, evidence is preserved, downstream access is investigated and recovery is verified.

**Evidence:** Timeline, redacted logs, revocation state and incident report.

**Teardown:** Reset test tenant and remove synthetic evidence.

## 14. Assessment rubric

| Criterion | Points |
|---|---:|
| Identifies subject, trust boundary and security objective | 10 |
| Explains protocol or policy behavior accurately | 15 |
| Reproduces the issue safely with synthetic identities | 15 |
| Identifies root cause and attack path | 15 |
| Implements a correct fix or policy | 20 |
| Adds positive and negative regression tests | 10 |
| Captures sanitized evidence and explains result | 10 |
| Completes teardown and records limitations | 5 |
| **Total** | **100** |

Suggested interpretation: 90–100 strong independent engineering; 75–89 working competence with review; 60–74 guided remediation required; below 60 repeat the exercise. These are training thresholds, not certification.

## 15. Instructor review checklist

- Was the lab isolated and authorized?
- Were all identities and data synthetic?
- Did the learner distinguish authentication from authorization?
- Did the learner identify issuer, audience, resource and transaction binding?
- Did the fix address root cause rather than block one test input?
- Were positive and negative cases both tested?
- Were tokens, secrets and personal data excluded from evidence?
- Was the exact library/runtime version recorded?
- Was teardown completed?
- Were limitations and untested paths documented?

## 16. References

1. NIST SP 800-63-4: https://csrc.nist.gov/pubs/sp/800/63/4/final
2. IETF RFC 9700: https://www.rfc-editor.org/rfc/rfc9700.html
3. OpenID Connect Core: https://openid.net/specs/openid-connect-core-1_0.html
4. W3C WebAuthn Level 3: https://www.w3.org/TR/webauthn-3/
5. OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
6. OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
7. OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html

## 17. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial identity and access security lab specifications |
