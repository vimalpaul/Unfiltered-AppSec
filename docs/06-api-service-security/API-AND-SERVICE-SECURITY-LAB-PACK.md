# API and Service Security Lab Pack

| Field | Value |
|---|---|
| Document ID | UAPPSEC-06-LAB-001 |
| Status | Draft lab specifications |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Isolated REST, GraphQL, gRPC, webhook and service identity exercises |
| Classification | Public |

## 1. Safety and lab architecture

These exercises are designed for local, disposable services and synthetic data. Do not execute them against public APIs, customer systems, production identities, real payment services or third-party integrations without explicit written authorization and a defined rules-of-engagement document.

### Mandatory safety controls

- Run all vulnerable services on loopback or a private isolated lab network.
- Use synthetic tenants, users, tokens, resources and webhook endpoints.
- Do not use production credentials, API keys, certificates or customer records.
- Do not expose deliberately vulnerable services to the public internet.
- Do not run uncontrolled fuzzing, denial-of-service, destructive operations or high-volume scans.
- Use mock identity providers, DNS, external APIs and webhook receivers.
- Restrict CPU, memory, disk, connection counts, queue depth and outbound network access.
- Record and pin container images and dependencies before claiming reproducibility.
- Stop if traffic leaves the lab network or real data is encountered.
- Destroy lab credentials and reset synthetic data after each exercise.

### Suggested lab components

- REST service with two tenants and multiple roles.
- GraphQL service exposing the same synthetic domain objects.
- gRPC service with unary and streaming methods.
- Local identity provider or deterministic mock token issuer.
- API gateway/reverse proxy.
- Mock partner API and webhook receiver.
- Synthetic relational database.
- Local DNS and controlled egress simulator.
- Logs/traces viewer.
- Intercepting proxy and API client.

This file defines lab specifications, not a prebuilt or independently validated lab environment.

## 2. Common evidence record

Record lab ID, learner, date, application build, protocol, endpoint, role/client identity, tenant, object, property, preconditions, exact steps, expected and observed result, sanitized evidence, root cause, remediation, regression tests, residual risk, teardown and reviewer result.

Never record live tokens, passwords, API keys, private keys, signing secrets or real personal data.

## 3. Lab 01: API inventory and contract drift

**Objective:** Identify undocumented routes and compare runtime behavior with the approved API contract.

**Prerequisites:** Local REST API, source route list and OpenAPI contract.

### Procedure

1. Record the API owner, base URL, version and environment.
2. Review the OpenAPI document and list operations, methods, schemas and security requirements.
3. Review source route/controller mappings.
4. Compare route list with gateway configuration.
5. In the local environment, exercise documented operations using synthetic accounts.
6. Compare observed routes, methods, status codes and response properties with the contract.
7. Identify undocumented, deprecated, debug or alternate-version routes.
8. Add ownership, lifecycle and security metadata to the inventory.
9. Configure a CI contract-diff check.
10. Confirm intentional differences have an owner and expiry.

**Expected result:** Every exposed route is inventoried, owned and mapped to a versioned contract; undocumented operations are removed or explicitly approved.

**Evidence:** Sanitized route inventory, contract diff and CI output.

**Teardown:** Remove test routes and credentials.

## 4. Lab 02: Function-level authorization (BFLA)

**Objective:** Verify that a low-privilege identity cannot invoke administrative API functions.

**Prerequisites:** Synthetic learner, analyst and administrator accounts.

### Procedure

1. Map the API's business functions and required roles.
2. Call a normal learner operation with the learner identity.
3. Identify an administrative operation from the local contract or application workflow.
4. Invoke the administrative operation using the learner identity.
5. Repeat with analyst and administrator identities.
6. Test alternate methods and versioned routes for the same function.
7. Verify that UI visibility is not the enforcement point.
8. Implement deny-by-default operation policies at the provider/domain layer.
9. Add a role-by-operation negative test matrix.
10. Confirm denied calls produce useful but non-sensitive audit events.

**Expected result:** Only explicitly authorized subjects can invoke each function, regardless of route or client UI.

**Evidence:** Sanitized request/response matrix and policy tests.

**Teardown:** Delete synthetic users.

## 5. Lab 03: Object-level authorization (BOLA)

**Objective:** Verify that a subject cannot read or mutate another tenant/user's object by changing an identifier.

**Prerequisites:** Two synthetic tenants, two users and separate records.

### Procedure

1. Create a record owned by user A in tenant A.
2. Create a separate record for user B in tenant B.
3. Retrieve user A's record with user A's identity.
4. Attempt to retrieve user B's record using user A's identity and the synthetic identifier.
5. Attempt update, delete, export and nested-resource operations against the foreign object.
6. Repeat using alternate endpoints and bulk routes.
7. Verify that ownership and tenant relationships come from trusted server-side data.
8. Replace unrestricted ID lookup with an authorization-aware query or explicit policy check.
9. Add positive and negative tests for all object actions.
10. Verify that error responses do not leak restricted object details where policy requires concealment.

**Expected result:** Access is limited to objects the authenticated subject is authorized to use.

**Evidence:** Redacted requests, database state and regression tests.

**Teardown:** Delete synthetic records and tenants.

## 6. Lab 04: Property-level authorization and mass assignment (BOPLA)

**Objective:** Prevent users from reading or modifying privileged object fields.

**Prerequisites:** Local profile/account API with synthetic role, tenant and status fields.

### Procedure

1. Review the documented request and response schema.
2. Record fields a normal user may read and update.
3. Retrieve the normal user's object and inspect returned properties.
4. Submit a write request containing synthetic privileged fields such as role, owner, tenant, approval state or account status.
5. Inspect server state to determine whether any privileged property changed.
6. Test unknown properties, null values, nested properties and alternate casing.
7. Implement explicit request DTOs and response projections.
8. Enforce property permissions in the domain service.
9. Add field-level read/write tests for every role.
10. Confirm audit fields and server-controlled values cannot be overwritten.

**Expected result:** Only approved properties are readable or writable; privileged state remains server-controlled.

**Evidence:** Before/after object state, sanitized payload and tests.

**Teardown:** Reset synthetic records.

## 7. Lab 05: Tenant isolation and relationship authorization

**Objective:** Verify that tenant and relationship context cannot be forged through request parameters.

**Prerequisites:** Two tenants, synthetic user memberships and delegated access.

### Procedure

1. Create tenant A and tenant B with separate resources.
2. Give user A membership only in tenant A.
3. Create one delegated relationship in the local system.
4. Access a tenant A resource normally.
5. Change tenant ID, organization ID and owner ID in request parameters.
6. Attempt access to tenant B records.
7. Test revoked and expired delegation.
8. Test nested relationship access and parent/child resources.
9. Derive tenant context from trusted identity/membership records.
10. Add cross-tenant and revoked-relationship regression tests.

**Expected result:** Server-side membership and relationship policy controls all access; caller-supplied tenant identifiers cannot grant access.

**Evidence:** Membership state, redacted requests and tests.

**Teardown:** Remove test tenants and delegations.

## 8. Lab 06: OAuth access token validation

**Objective:** Verify that the API accepts only tokens matching its configured issuer, audience, signature and claim policy.

**Safety:** Use a local mock issuer and synthetic signing keys only.

### Procedure

1. Configure a local issuer, signing key and API audience.
2. Obtain a valid synthetic access token.
3. Call the protected endpoint with the valid token.
4. Test missing and malformed tokens.
5. Test expired and not-yet-valid tokens.
6. Test wrong issuer and wrong audience.
7. Test an invalid signature and an unapproved signing algorithm.
8. Test an ID token where an access token is required.
9. Test missing scope/client context.
10. Implement explicit issuer, audience, algorithm, token-type and time validation.
11. Add automated negative test cases and key-rotation tests.

**Expected result:** Only correctly issued access tokens for the intended API and operation are accepted.

**Evidence:** Mock issuer config, sanitized claims and test output. Never save raw bearer tokens.

**Teardown:** Destroy test keys and tokens.

## 9. Lab 07: API key lifecycle and least privilege

**Objective:** Verify API keys are scoped, owned, revocable and not exposed.

**Prerequisites:** Local integration API and synthetic client keys.

### Procedure

1. Create two test integration clients with separate keys.
2. Record owner, purpose, expiry, scope and allowed API.
3. Verify each key can call only its assigned operation.
4. Attempt to use key A against key B's tenant/resource.
5. Inspect logs and confirm secrets are redacted.
6. Rotate key A using an overlap window.
7. Revoke the old key and verify it is rejected.
8. Test expired and unknown keys.
9. Confirm key material is not embedded in client-side assets or URLs.
10. Add rotation, revocation and scope regression tests.

**Expected result:** Keys have least privilege, clear ownership, safe rotation and immediate revocation.

**Evidence:** Redacted key metadata, policy and tests.

**Teardown:** Revoke and delete all test keys.

## 10. Lab 08: REST pagination, filtering and PATCH controls

**Objective:** Prevent unbounded queries and unauthorized property updates.

**Prerequisites:** Local REST API with synthetic records.

### Procedure

1. Record allowed filters, sort fields, page size and patchable properties.
2. Request a normal page.
3. Test oversized page size and offset.
4. Submit an unknown sort field and filter operator.
5. Attempt to modify an immutable or privileged property using PATCH.
6. Test duplicate/unknown JSON properties and nested patch paths.
7. Inspect whether counts or aggregates include foreign tenant records.
8. Add explicit allow-lists, bounded pagination and per-property patch policy.
9. Add negative and positive regression tests.
10. Confirm legitimate API clients remain compatible.

**Expected result:** Queries are bounded and only authorized properties can change.

**Evidence:** Sanitized requests, query behavior and tests.

**Teardown:** Reset test data.

## 11. Lab 09: GraphQL field and resolver authorization

**Objective:** Verify that authorization is enforced at field, resolver and domain layers.

**Prerequisites:** Local GraphQL service exposing synthetic users, organizations and documents.

### Procedure

1. Identify sensitive schema fields and nested relationships.
2. Query allowed fields as a normal user.
3. Attempt to query restricted fields.
4. Query a nested object owned by another synthetic user.
5. Invoke mutations with unauthorized object identifiers.
6. Test aliases and fragments that access the same restricted field through alternate paths.
7. Test subscriptions for tenant/user isolation.
8. Implement shared domain authorization and field policy.
9. Add tests across query, mutation, nested resolver and subscription paths.
10. Verify errors do not reveal restricted data or internal resolver details.

**Expected result:** GraphQL cannot bypass authorization enforced by REST or the domain layer.

**Evidence:** Sanitized operations, resolver policy and regression tests.

**Teardown:** Delete synthetic GraphQL data.

## 12. Lab 10: GraphQL demand control

**Objective:** Bound query depth, breadth, aliases, batching and resolver cost.

**Prerequisites:** Local GraphQL service with nested list fields and a mock database.

### Procedure

1. Record normal query shapes and expected cost.
2. Configure maximum depth and list nesting.
3. Test a query beyond the configured depth.
4. Test many aliases for the same expensive field.
5. Test a batch containing multiple operations.
6. Test large pagination values.
7. Configure complexity/cost weights for expensive fields.
8. Apply per-client/tenant query budgets and resolver deadlines.
9. Verify rejected operations fail before expensive work.
10. Add performance and limit regression tests.

**Expected result:** Excessive queries are rejected or throttled before exhausting resources; normal operations remain available.

**Evidence:** Query samples, cost configuration and metrics.

**Teardown:** Restore normal query limits.

## 13. Lab 11: gRPC method and message authorization

**Objective:** Verify TLS identity, method authorization, message bounds and safe streaming behavior.

**Prerequisites:** Local gRPC server, test certificates and synthetic service identities.

### Procedure

1. Configure the test server with TLS.
2. Connect using an approved synthetic client certificate.
3. Call an allowed RPC method.
4. Attempt a privileged RPC using a lower-privilege identity.
5. Test an oversized message within safe local limits.
6. Test malformed or unexpected message fields.
7. Review reflection and health service exposure.
8. Configure method-level policy, message limits and deadlines.
9. Test a stream with role revocation or expiry.
10. Add positive/negative tests for unary and streaming RPCs.

**Expected result:** Only approved workload identities and actions are accepted; message and stream resources are bounded.

**Evidence:** Sanitized gRPC metadata, certificate identity mapping and test output.

**Teardown:** Destroy test certificates and server.

## 14. Lab 12: Webhook signature and replay protection

**Objective:** Verify inbound webhooks are authenticated, time-bounded and idempotent.

**Prerequisites:** Local mock sender, receiver and synthetic signing secret.

### Procedure

1. Configure a local webhook integration and synthetic signing secret.
2. Send a valid event with timestamp and delivery ID.
3. Verify the receiver accepts and records the event.
4. Modify the body without updating the signature.
5. Send an invalid signature.
6. Send a stale timestamp.
7. Replay a previously accepted delivery ID.
8. Rotate the signing secret using a documented overlap period.
9. Implement raw-body signature verification, constant-time MAC comparison, timestamp validation and durable deduplication.
10. Add tests for altered body, stale timestamp, replay and rotation.

**Expected result:** Forged and replayed events are rejected; legitimate retries do not duplicate side effects.

**Evidence:** Redacted headers, event IDs and state transitions. Never include the secret.

**Teardown:** Delete integration and test secret.

## 15. Lab 13: Webhook destination SSRF controls

**Objective:** Prevent a webhook sender from reaching arbitrary or prohibited network destinations.

**Safety:** Use only local mock DNS and mock destination services. Do not probe cloud metadata endpoints or real private networks.

### Procedure

1. Configure a webhook destination using an approved mock hostname.
2. Verify successful delivery to the approved service.
3. Configure a denied mock destination.
4. Test a hostname that resolves to a blocked address in the local DNS simulator.
5. Test a redirect from approved to denied destination.
6. Test an address change between validation and connection using the simulator.
7. Apply scheme/host/IP allow-list, redirect revalidation and controlled egress.
8. Add connection/read timeout and response-size limits.
9. Verify the sender does not return internal response content to the configuring user.
10. Add positive/negative destination tests.

**Expected result:** Only approved destinations can be reached; DNS and redirect changes cannot bypass policy.

**Evidence:** Mock DNS records, egress logs and policy tests.

**Teardown:** Stop mock DNS and destination services.

## 16. Lab 14: Idempotency and concurrent business operations

**Objective:** Preserve a business invariant when clients retry or concurrently submit state-changing API operations.

**Prerequisites:** Local synthetic booking, assessment or inventory API with a limited resource.

### Procedure

1. Define a business invariant, such as one active booking per synthetic resource.
2. Complete one normal operation.
3. Retry with the same idempotency key and identical request.
4. Reuse the same key with a different request body.
5. Submit concurrent requests using separate keys against the one remaining synthetic resource.
6. Inspect database state and audit events.
7. Implement durable idempotency storage, request fingerprinting and atomic constraints.
8. Recheck authorization and state at commit time.
9. Add retry, conflicting-key and concurrency regression tests.
10. Verify failed operations do not partially mutate state.

**Expected result:** Duplicate requests do not create duplicate side effects and concurrent execution preserves the invariant.

**Evidence:** Sanitized request IDs, transaction state and test output.

**Teardown:** Reset inventory/booking state.

## 17. Lab 15: API resource consumption and abuse limits

**Objective:** Verify layered limits for request size, concurrency, pagination, batches and expensive operations.

**Safety:** Run only in local lab with conservative test ceilings; do not conduct denial-of-service testing.

### Procedure

1. Record configured limits at gateway and service.
2. Submit normal requests and establish baseline.
3. Test just below and just above the approved payload limit.
4. Test batch count and pagination ceilings.
5. Test bounded concurrency using a small number of synthetic requests.
6. Test an expensive report/query under a configured budget.
7. Verify rate-limit behavior and Retry-After where applicable.
8. Configure per-client, per-tenant and per-operation quotas.
9. Add metrics for rejected requests, queue depth and execution time.
10. Add regression tests for limits and legitimate burst behavior.

**Expected result:** Excessive requests are bounded without relying solely on source IP; service remains stable.

**Evidence:** Configuration, response codes and resource metrics.

**Teardown:** Restore baseline quotas and clear test queues.

## 18. Lab 16: Unsafe upstream API consumption

**Objective:** Verify that responses from an external service are treated as untrusted data.

**Prerequisites:** Local mock upstream API with valid and intentionally malformed response modes.

### Procedure

1. Configure the consumer to call a mock upstream endpoint.
2. Verify a valid schema response is processed.
3. Return an unexpected content type.
4. Return malformed JSON and missing required fields.
5. Return out-of-range numeric and unexpected enum values.
6. Return an unapproved redirect and invalid certificate in the mock environment.
7. Return an oversized response within the local test harness.
8. Implement strict TLS, endpoint, redirect, schema, size and timeout validation.
9. Add circuit breaker/retry policy without retry storms.
10. Add regression tests for malformed and hostile upstream behavior.

**Expected result:** Untrusted upstream responses cannot cause unsafe parsing, privilege changes, SSRF or resource exhaustion.

**Evidence:** Mock response set, validation policy and tests.

**Teardown:** Remove mock upstream configuration.

## 19. Lab 17: Gateway bypass and trusted identity headers

**Objective:** Verify that a service cannot be reached around required gateway policy and that client-supplied identity headers are not trusted.

**Prerequisites:** Local gateway and service on isolated network.

### Procedure

1. Record expected public gateway path and service ingress policy.
2. Call the API through the gateway using a valid synthetic identity.
3. Submit client-supplied identity/tenant headers through the gateway.
4. Verify the gateway strips and replaces untrusted values.
5. Attempt direct service access from an untrusted lab network segment.
6. Verify direct-origin access is blocked or enforces equivalent authenticated controls.
7. Inspect service logs to identify trusted gateway identity.
8. Restrict ingress and authenticate gateway-to-service traffic.
9. Add tests for header spoofing and direct path access.
10. Verify network policy covers alternate load balancers and debug paths.

**Expected result:** Client-supplied headers cannot impersonate a user or tenant and gateway controls cannot be bypassed.

**Evidence:** Sanitized traces, network policy and test output.

**Teardown:** Remove temporary routes and network rules.

## 20. Lab 18: API version lifecycle and deprecation

**Objective:** Verify old API versions are tracked, migrated and retired without authorization regressions.

**Prerequisites:** Local API with two synthetic versions.

### Procedure

1. Inventory active versions and their owners.
2. Compare security policy across old and current versions.
3. Test the same authorization cases against both versions.
4. Mark the old version deprecated and publish a synthetic sunset date.
5. Observe usage telemetry by client.
6. Migrate the test client to the current version.
7. Remove the old route and credentials.
8. Verify the old route is unreachable.
9. Add CI inventory checks for undeclared routes and deprecated version use.
10. Document evidence and rollback criteria.

**Expected result:** Every API version has an owner and lifecycle; retired routes cannot remain as hidden bypasses.

**Evidence:** Version inventory, usage logs and retirement test.

**Teardown:** Remove obsolete test version.

## 21. Assessment rubric

| Criterion | Points |
|---|---:|
| Identifies API contract, subject and trust boundary | 10 |
| Builds a correct function/object/property/tenant test model | 20 |
| Reproduces the issue safely with synthetic identities/data | 15 |
| Captures sanitized evidence and explains impact | 10 |
| Fixes root cause at provider/domain boundary | 20 |
| Adds positive, negative and abuse-case regression tests | 15 |
| Defines monitoring, residual risk and response | 5 |
| Completes teardown and records limitations | 5 |
| **Total** | **100** |

Suggested interpretation: 90–100 strong independent engineering; 75–89 competent with review; 60–74 guided remediation required; below 60 repeat the exercise. These are training thresholds, not certification.

## 22. Instructor review checklist

- Was the target explicitly authorized and isolated?
- Were all identities and resources synthetic?
- Did the learner test more than one role and tenant?
- Did the learner distinguish authentication from authorization?
- Were object, property and function controls assessed separately?
- Were GraphQL and gRPC paths assessed where present?
- Were webhook signature and replay controls tested?
- Were concurrency and idempotency semantics considered?
- Were resource limits tested conservatively?
- Did remediation fix the domain rule rather than hide a UI field?
- Were regression tests added?
- Was evidence sanitized and teardown completed?

## 23. References

1. OWASP API Security Project: https://owasp.org/projects/api-security-project/
2. OWASP API Security Top 10:2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
3. OWASP ASVS 5.0.0: https://asvs.owasp.org/
4. IETF RFC 9700: https://www.rfc-editor.org/rfc/rfc9700.html
5. OpenAPI Specification: https://spec.openapis.org/oas/
6. GraphQL Security: https://graphql.org/learn/security/
7. gRPC Authentication: https://grpc.io/docs/guides/auth/
8. NIST SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final

## 24. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial API and service security lab specifications |
