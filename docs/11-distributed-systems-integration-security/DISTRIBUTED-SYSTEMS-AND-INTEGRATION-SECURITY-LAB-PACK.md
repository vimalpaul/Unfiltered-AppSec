# Distributed Systems and Integration Security Lab Pack

| Field | Value |
|---|---|
| Document ID | UAPPSEC-11-LAB-001 |
| Status | Draft lab specifications |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Microservices, mTLS, workload identity, service mesh, brokers, events, webhooks, distributed workflows and telemetry |
| Classification | Public |

## 1. Safety, authorization and environment controls

These labs are designed for local containers, disposable Kubernetes clusters, synthetic applications and explicitly authorized sandbox infrastructure. Do not use production services, real customer data, payment endpoints, partner webhooks or production broker topics.

Before starting:
- Confirm the lab owner, scope and authorized environment.
- Use synthetic tenants, users, credentials, events and transaction references.
- Use a local broker or disposable broker namespace.
- Disable real email, SMS, payment, identity and third-party side effects.
- Do not point callback or webhook tests at public or internal production services.
- Use local mock endpoints for SSRF and metadata tests.
- Do not generate uncontrolled message floods, poison-message storms or resource exhaustion.
- Set message size, concurrency, retry and retention limits.
- Record exact versions of broker, runtime, service mesh, SDK, schema and CLI.
- Protect test private keys and signing secrets; redact them from evidence.
- Review cleanup steps before deployment and verify all test resources are removed.

The lab pack is a set of specifications. A lab is not considered validated until its environment, commands, expected results, teardown and evidence have been reproduced by a reviewer.

## 2. Common reference environment

Recommended topology:
- Service A: synthetic order API and event producer.
- Service B: payment simulation service.
- Service C: inventory simulation service.
- Worker D: notification consumer.
- Local broker: Kafka or RabbitMQ.
- Optional local Kubernetes cluster and service mesh.
- Local test CA or SPIFFE/SPIRE sandbox where supported.
- Local identity/token issuer or mock token service.
- Synthetic database for order state and inbox/outbox records.
- Local webhook receiver and callback sink.
- Local OpenTelemetry collector and trace viewer.

All services must use synthetic records and local network destinations. The payment service must simulate results and must not connect to a real payment processor.

## 3. Evidence record

For each lab capture:
- Lab ID, title and learner.
- Authorization and sandbox owner.
- Environment and exact component versions.
- Service identity, broker principal and permissions used.
- Initial topology and preconditions.
- Test data identifiers, with no real personal data.
- Exact steps and sanitized commands.
- Expected and observed results.
- Broker, service, identity and telemetry evidence.
- Finding, root cause, remediation and retest.
- Resource cleanup verification.
- Reviewer and closure status.

Do not capture raw tokens, private keys, passwords, full sensitive payloads or production identifiers.

## 4. Lab 01 — Service inventory and trust-boundary mapping

**Objective:** Build an inventory of services, interfaces, identities, message paths and data owners.

**Prerequisites:** Synthetic microservice repository or supplied local reference application.

### Procedure

1. Identify all deployable services and background workers.
2. Record inbound and outbound protocols for each component.
3. Identify gateway, mesh, broker, schema registry, identity provider and telemetry collector.
4. Draw synchronous request paths and asynchronous event paths.
5. Identify producers, consumers, topics, queues and consumer groups.
6. Record data categories and tenant boundaries.
7. Identify external integrations and callback endpoints.
8. Record service owners, environment and criticality.
9. Mark every trust boundary and identity transition.
10. Review the map with a second learner and identify missing edges.

**Expected result:** Every service and integration has an owner, purpose, identity and documented communication path.

**Evidence:** Service inventory, data-flow diagram, trust-boundary diagram and open-question register.

**Teardown:** No infrastructure required.

## 5. Lab 02 — Workload identity versus user identity

**Objective:** Demonstrate why service identity and delegated user identity are separate security inputs.

**Prerequisites:** Two local services and a mock identity issuer.

### Procedure

1. Configure Service A to authenticate to Service B using a test workload credential.
2. Configure a synthetic user token for a test user.
3. Send a request with only workload identity and observe the receiver's authenticated caller.
4. Send a request with workload identity and a valid user token.
5. Confirm the receiver validates the workload and user context independently.
6. Modify the user identifier in a custom header while retaining the original token.
7. Verify the receiver ignores the untrusted header and derives subject from validated claims.
8. Remove the user token and attempt a user-specific action.
9. Verify the service denies the action if delegated user context is required.
10. Record which operations are service-only and which require user delegation.

**Expected result:** The receiver distinguishes caller workload from end-user subject and never trusts arbitrary identity headers.

**Evidence:** Sanitized request/decision logs and authorization matrix.

**Teardown:** Remove mock users and test credentials.

## 6. Lab 03 — mTLS service authentication

**Objective:** Verify that two services authenticate each other using test certificates.

**Prerequisites:** Local test CA, two local services and a TLS-capable client.

### Procedure

1. Create a test CA and issue a server certificate to Service B.
2. Issue a distinct client certificate to Service A.
3. Configure Service B to require client certificate authentication.
4. Call Service B with the valid Service A certificate.
5. Repeat without a client certificate.
6. Repeat with an expired certificate.
7. Repeat with a certificate from an untrusted CA.
8. Repeat with a valid certificate mapped to an unauthorized workload identity.
9. Confirm the TLS layer and application authorization produce the expected outcomes.
10. Rotate the Service A certificate and verify renewal without disabling authentication.

**Expected result:** Only trusted, valid and correctly identified workloads establish the protected channel; application authorization remains independently enforced.

**Evidence:** Certificate metadata with private material redacted, TLS results and authorization logs.

**Teardown:** Revoke/delete test certificates and local CA material.

## 7. Lab 04 — SPIFFE identity and trust-domain validation

**Objective:** Understand SPIFFE IDs, SVIDs, trust bundles and workload identity validation.

**Prerequisites:** Local SPIRE/SPIFFE training environment or a mock identity service. Do not deploy a production trust authority.

### Procedure

1. Define a lab trust domain and naming convention.
2. Register two synthetic workloads with distinct identities.
3. Retrieve an X.509-SVID using the supported Workload API.
4. Inspect the SPIFFE ID and certificate validity without exposing the private key.
5. Configure Service A to validate Service B's SVID.
6. Verify a valid same-domain workload is accepted.
7. Verify an unregistered workload is rejected.
8. Introduce an untrusted trust bundle in a controlled test and confirm validation fails.
9. Rotate the test SVID and verify the receiving service accepts the new valid identity.
10. Remove one registration and verify that identity can no longer authenticate after the trust/credential lifecycle takes effect.

**Expected result:** Workload identity is tied to attested registration and explicit trust, not an arbitrary service name.

**Evidence:** Sanitized SPIFFE ID, trust bundle metadata, certificate validation and rejection logs.

**Teardown:** Remove registrations, test authority and temporary trust bundles.

## 8. Lab 05 — OAuth token audience and token exchange

**Objective:** Prevent a token intended for one service from being accepted by another service.

**Prerequisites:** Local test authorization server and two resource services.

### Procedure

1. Register Service A and issue a token for Service B.
2. Configure Service B to validate issuer, audience, expiry, signature and intended token profile.
3. Send the token to Service B and verify the intended request works subject to authorization.
4. Send the same token to Service C and verify it is rejected for wrong audience.
5. Configure a token exchange flow for Service A to obtain a narrowly scoped token for Service C.
6. Inspect subject, actor, audience and scopes in the exchanged token.
7. Attempt an exchange that requests broader privileges than the source identity is allowed.
8. Verify the token service rejects the privilege expansion.
9. Test expired and not-yet-valid tokens.
10. Record token lifetime and revocation behavior.

**Expected result:** Each resource service accepts only tokens intended for it, and exchange does not amplify authority.

**Evidence:** Redacted claims, issuer configuration and positive/negative authorization results.

**Teardown:** Delete test clients, keys and tokens.

## 9. Lab 06 — Service-level authorization and confused deputy

**Objective:** Verify that an authenticated service cannot use its authority for an unauthorized caller.

**Prerequisites:** Two synthetic tenants, an order service and a privileged downstream service.

### Procedure

1. Create tenant A and tenant B with separate synthetic records.
2. Configure Service A to call a downstream report service using its workload identity.
3. Implement a user-delegated operation with tenant context derived from a validated token.
4. Request tenant A's report as tenant A user.
5. Modify a caller-supplied tenant header to tenant B.
6. Attempt to request tenant B's report using tenant A identity.
7. Verify the report service performs object and tenant authorization itself.
8. Attempt the same request from a different authenticated service that lacks the permission.
9. Verify the downstream service denies both unauthorized paths.
10. Record the exact policy decision and test for alternate routes.

**Expected result:** A privileged service does not become a confused deputy; downstream authorization uses verified subject, tenant, action and resource.

**Evidence:** Authorization decision log, policy test and tenant isolation matrix.

**Teardown:** Delete synthetic tenants and records.

## 10. Lab 07 — Service mesh policy and proxy bypass

**Objective:** Verify mesh mTLS and authorization are not bypassed through alternate network paths.

**Prerequisites:** Disposable Kubernetes cluster and local service mesh.

### Procedure

1. Deploy Service A and Service B in a lab namespace.
2. Enable strict mTLS and a narrow allow policy for Service A to call Service B.
3. Verify the intended call succeeds.
4. Verify an unauthorized workload is denied.
5. Attempt direct service IP access where the lab network permits.
6. Inspect sidecar injection and excluded ports.
7. Test a workload in a namespace without mesh injection.
8. Inspect NodePort, host-network and alternate ingress paths if configured.
9. Verify the policy still protects Service B or that alternate paths are blocked.
10. Record mesh control-plane and proxy configuration versions.

**Expected result:** The allowed service path works; unauthorized and bypass paths are denied or covered by equivalent application/network controls.

**Evidence:** Mesh policy, workload identity, connectivity matrix and proxy logs.

**Teardown:** Remove mesh policies and lab namespace.

## 11. Lab 08 — Kafka producer and consumer ACLs

**Objective:** Enforce least-privilege access to a test Kafka topic and consumer group.

**Prerequisites:** Disposable Kafka cluster with TLS and authorization enabled.

### Procedure

1. Create synthetic producer, consumer and operator principals.
2. Create a test topic and consumer group.
3. Grant producer permission only to publish to the designated topic.
4. Grant consumer permission only to read the designated topic and group.
5. Verify intended publish and consume operations.
6. Attempt producer access to an unrelated topic.
7. Attempt consumer access to an unrelated topic or group.
8. Attempt topic creation and ACL modification using application principals.
9. Verify denied operations are logged.
10. Review wildcard ACLs, superuser configuration and listener exposure.

**Expected result:** Producer, consumer and operator permissions are distinct and scoped.

**Evidence:** ACL export with sensitive identifiers sanitized and positive/negative test output.

**Teardown:** Delete test principals, topic and consumer group.

## 12. Lab 09 — RabbitMQ virtual host and resource permissions

**Objective:** Restrict application access to one virtual host and the required exchange/queue operations.

**Prerequisites:** Disposable RabbitMQ instance.

### Procedure

1. Create a lab virtual host and synthetic exchange/queue.
2. Create distinct producer and consumer users.
3. Grant producer write permission to the intended exchange only.
4. Grant consumer read permission to the intended queue only.
5. Verify intended publish and consume operations.
6. Attempt access to another virtual host.
7. Attempt configure permission using application credentials.
8. Attempt to access the management interface as a non-admin.
9. Verify denied actions are logged.
10. Confirm default guest access is not enabled remotely.

**Expected result:** Applications cannot administer the broker or access unrelated virtual hosts and resources.

**Evidence:** User/permission matrix and sanitized broker logs.

**Teardown:** Delete test users, virtual host, exchanges and queues.

## 13. Lab 10 — Event schema validation and schema evolution

**Objective:** Validate event structure, bounds and compatibility before processing.

**Prerequisites:** Local event producer/consumer and JSON Schema or schema registry.

### Procedure

1. Define a versioned order-created event schema.
2. Publish a valid synthetic event and confirm it is processed.
3. Publish an event missing a required field.
4. Publish a field with an incorrect type.
5. Publish an oversized string and deeply nested payload.
6. Publish an unknown event type.
7. Introduce a backward-compatible schema change.
8. Introduce a deliberately incompatible change in a separate test version.
9. Verify compatibility policy blocks or flags the incompatible change.
10. Record how consumer versions handle unknown optional and critical fields.

**Expected result:** Invalid or incompatible events are rejected safely before business processing.

**Evidence:** Schema versions, compatibility output and consumer validation logs.

**Teardown:** Remove lab schemas and test events.

## 14. Lab 11 — Event replay and idempotent consumer

**Objective:** Ensure duplicate delivery does not repeat a business side effect.

**Prerequisites:** Local broker, synthetic database and consumer application.

### Procedure

1. Create a synthetic order with a unique event ID.
2. Configure consumer to persist inbox ID and business effect in one transaction.
3. Publish the event once and verify the intended state change.
4. Publish the same event ID and payload again.
5. Verify no duplicate state change occurs.
6. Publish a new event ID for the same business object and evaluate business-level idempotency rules.
7. Simulate database commit success followed by broker acknowledgement failure.
8. Allow broker redelivery and verify no duplicate effect.
9. Attempt concurrent delivery of the same event to two workers.
10. Verify the unique constraint and transaction prevent duplicate effects.

**Expected result:** Redelivery, acknowledgement loss and concurrent duplicate processing do not create duplicate business effects.

**Evidence:** Inbox rows with sensitive fields omitted, transaction logs and state before/after.

**Teardown:** Delete synthetic records and broker topic/queue.

## 15. Lab 12 — Outbox publisher failure window

**Objective:** Demonstrate safe event publication when the publisher crashes after broker publish.

**Prerequisites:** Local relational database, broker and outbox worker.

### Procedure

1. Create an order update and outbox row within one database transaction.
2. Run the outbox publisher and publish the event.
3. Simulate a publisher crash before marking the outbox row as published.
4. Restart the publisher and allow it to publish the same event again.
5. Confirm the consumer's inbox/idempotency logic prevents duplicate business effects.
6. Test publisher concurrency and row locking/lease behavior.
7. Test a poison outbox row and bounded retry.
8. Verify outbox lag and failure metrics.
9. Verify cleanup does not delete unpublished events.
10. Record reconciliation procedure for stuck rows.

**Expected result:** Business update and event intent are atomic; duplicate publication is safe and observable.

**Evidence:** Database transaction, outbox status, broker message IDs and consumer result.

**Teardown:** Remove test tables, rows and broker resources.

## 16. Lab 13 — Saga compensation and uncertain remote outcome

**Objective:** Validate a distributed workflow with failure and compensation.

**Prerequisites:** Local order, inventory and payment simulation services. No real payment endpoint.

### Procedure

1. Define a synthetic order workflow with reserve inventory, authorize payment and confirm order.
2. Record allowed state transitions.
3. Run a successful workflow.
4. Configure the inventory step to fail and verify payment is not incorrectly captured.
5. Configure a payment timeout where the simulated provider actually records success but the response is lost.
6. Verify the orchestrator queries provider state using a stable idempotency key before retrying.
7. Simulate a later step failure and invoke the documented compensation.
8. Simulate compensation failure and route to manual reconciliation state.
9. Attempt duplicate completion and compensation events.
10. Verify every transition is durable and auditable.

**Expected result:** Workflow does not assume timeout equals failure; duplicate steps are safe and compensation reaches a defined state.

**Evidence:** Saga state timeline, synthetic provider ledger and compensation log.

**Teardown:** Reset local simulation state.

## 17. Lab 14 — Signed inbound webhook and replay protection

**Objective:** Verify raw-body signature, timestamp and event ID handling.

**Prerequisites:** Local webhook sender and receiver with synthetic signing key.

### Procedure

1. Register a synthetic partner and test signing key.
2. Create a canonical webhook request according to the lab signature contract.
3. Send a valid request and verify acceptance.
4. Change one byte in the raw body without updating the signature.
5. Send an invalid signature and verify rejection.
6. Send a valid signature with an expired timestamp.
7. Replay a previously accepted event ID with a valid signature.
8. Verify the receiver rejects duplicate processing.
9. Rotate the test signing key and verify the defined overlap and retirement process.
10. Confirm logs do not contain the signing secret or full sensitive payload.

**Expected result:** Only authentic, timely and non-duplicate webhook events are accepted.

**Evidence:** Redacted signature metadata, timestamp checks, event ledger and receiver logs.

**Teardown:** Delete test partner and signing key.

## 18. Lab 15 — Outbound callback SSRF defense

**Objective:** Ensure a callback feature cannot reach internal or metadata endpoints.

**Prerequisites:** Local callback sender, mock public destination, mock private destination and mock metadata endpoint.

### Procedure

1. Configure callback sender to accept only a registered local test hostname.
2. Send a valid callback to the allowlisted destination.
3. Attempt loopback, private IPv4, link-local and IPv6 destinations.
4. Attempt a hostname that resolves to a private address.
5. Attempt a redirect from an allowed hostname to a blocked destination.
6. Change DNS response between validation and connection in the controlled lab.
7. Verify the sender revalidates resolved addresses and every redirect.
8. Confirm no internal credentials, cookies or authorization headers are forwarded.
9. Verify timeout and response-size limits.
10. Confirm egress logs record the blocked attempt.

**Expected result:** Callback requests are constrained to registered destinations; internal and metadata endpoints are unreachable.

**Evidence:** Destination validation decisions and local network logs.

**Teardown:** Stop mock endpoints and remove callback configuration.

## 19. Lab 16 — Message integrity and producer provenance

**Objective:** Verify that a high-risk event cannot be modified or attributed to a different producer without detection.

**Prerequisites:** Local producer, receiver and test signing key or message authentication key.

### Procedure

1. Define canonical fields covered by the signature or digest.
2. Create a synthetic event with unique ID, source, type, timestamp, schema version and payload digest.
3. Sign the event using the test key.
4. Verify the receiver accepts the event from the registered producer.
5. Modify the payload without updating the signature.
6. Modify the source identity while retaining the original signature.
7. Replace the signing key with an untrusted key.
8. Replay a valid signed event and verify separate replay controls reject duplicate effect.
9. Rotate the test key and test trust update.
10. Record which properties are guaranteed by signature and which are enforced by authorization.

**Expected result:** Integrity and producer provenance are verifiable; signature validity does not bypass replay or business authorization.

**Evidence:** Sanitized signature validation and producer authorization results.

**Teardown:** Delete test keys and events.

## 20. Lab 17 — Dead-letter queue governance

**Objective:** Protect failed messages and control reprocessing.

**Prerequisites:** Local broker, consumer and DLQ.

### Procedure

1. Configure a test consumer with a bounded retry policy.
2. Publish a valid event and verify normal processing.
3. Publish a deliberately invalid synthetic event.
4. Verify it is retried only within configured limits.
5. Verify it is moved to the DLQ with reason and original event ID.
6. Attempt DLQ access with an unauthorized application principal.
7. Attempt manual redrive with a non-operator identity.
8. Verify approved operator access is audited.
9. Inspect DLQ payload for sensitive fields and confirm minimization.
10. Verify retention, purge and redrive approvals.

**Expected result:** DLQ is restricted, monitored, time-bounded and reprocessing is authorized and auditable.

**Evidence:** ACLs, retry counts, DLQ record metadata and operator audit.

**Teardown:** Delete test messages and DLQ.

## 21. Lab 18 — Retry storm and circuit-breaker behavior

**Objective:** Verify retries do not amplify a downstream outage.

**Prerequisites:** Local service dependency with a controllable failure mode.

### Procedure

1. Configure Service A to call a synthetic dependency.
2. Record normal request rate and latency.
3. Simulate a bounded dependency timeout.
4. Observe retries at client, proxy and service layers.
5. Verify exponential backoff and jitter.
6. Verify retry budget and maximum attempts.
7. Confirm permanent 4xx/authentication errors are not retried indiscriminately.
8. Enable circuit breaker and observe open, half-open and closed states.
9. Verify fallback does not create false success or unsafe business state.
10. Restore dependency and verify gradual recovery without retry burst.

**Expected result:** Failure is bounded, retry amplification is controlled and recovery is gradual.

**Evidence:** Request timeline, retry metrics, breaker state and service logs.

**Teardown:** Restore normal dependency behavior and remove fault injection.

## 22. Lab 19 — Trace context and telemetry privacy

**Objective:** Validate trace propagation without trusting arbitrary headers or exporting sensitive values.

**Prerequisites:** Local OpenTelemetry SDK/collector and two synthetic services.

### Procedure

1. Generate a normal trace across Service A and Service B.
2. Propagate trace context across an asynchronous message.
3. Inspect trace/span linkage.
4. Submit malformed and oversized trace headers.
5. Submit baggage containing a synthetic token marker and personal-data marker.
6. Verify inbound trust policy resets or filters untrusted context.
7. Verify collector redaction removes prohibited attributes.
8. Inspect metrics for high-cardinality user-controlled labels.
9. Inspect exported telemetry and retention/access settings.
10. Verify correlation IDs are not used as authentication or authorization.

**Expected result:** Tracing works for correlation, but untrusted metadata and sensitive attributes are bounded or removed.

**Evidence:** Sanitized traces, collector policy and redaction output.

**Teardown:** Delete local traces and synthetic attributes.

## 23. Lab 20 — Service discovery and endpoint substitution

**Objective:** Verify that a service does not trust a network endpoint solely because it appears in discovery.

**Prerequisites:** Local service registry or controlled DNS/service discovery environment.

### Procedure

1. Register Service B with an approved identity and endpoint.
2. Configure Service A to discover and call Service B.
3. Verify the endpoint identity matches the expected workload identity.
4. Register a second endpoint with an untrusted identity.
5. Attempt to substitute the discovered endpoint.
6. Verify TLS identity validation rejects the substitute.
7. Attempt unauthorized service registration.
8. Review registry authentication and write permissions.
9. Inspect stale registration and decommissioning behavior.
10. Record DNS and registry change audit.

**Expected result:** Discovery provides a location, but cryptographic identity validation and authorization determine trust.

**Evidence:** Registry policy, identity validation and rejected connection logs.

**Teardown:** Remove test registrations and DNS overrides.

## 24. Lab 21 — Third-party integration lifecycle

**Objective:** Verify a partner integration can be scoped, monitored, rotated and terminated.

**Prerequisites:** Two synthetic partner identities and a local mock API.

### Procedure

1. Register partner A and partner B with separate credentials.
2. Scope partner A to a limited endpoint and synthetic tenant.
3. Verify partner A can perform only its allowed operation.
4. Attempt partner B resource access using partner A credentials.
5. Rotate partner A's test credential.
6. Verify the old credential is rejected after the agreed overlap.
7. Disable partner A and verify access is revoked.
8. Review in-flight messages and callback delivery.
9. Verify audit identifies the partner principal and operation.
10. Update integration inventory and termination record.

**Expected result:** Partner access is isolated, reviewable, rotatable and revocable.

**Evidence:** Partner access matrix, rotation logs and denied cross-partner request.

**Teardown:** Delete test partners and credentials.

## 25. Lab 22 — Cross-tenant event isolation

**Objective:** Prevent a valid event from one tenant being processed against another tenant's data.

**Prerequisites:** Multi-tenant synthetic producer, broker and consumer.

### Procedure

1. Create tenant A and tenant B with separate synthetic records.
2. Configure producer identity authorized for tenant A.
3. Publish a tenant A event with valid source identity.
4. Attempt to change the payload tenant identifier to tenant B.
5. Verify consumer derives or validates tenant from trusted producer authorization and domain state.
6. Attempt to publish tenant B event using tenant A principal.
7. Attempt to consume tenant B event with a consumer identity lacking access.
8. Verify logs capture denial without exposing payload secrets.
9. Test background worker and replay path.
10. Add regression tests for all tenant-bearing event types.

**Expected result:** Tenant context is never trusted solely because it appears in a message payload.

**Evidence:** Tenant authorization matrix and negative test results.

**Teardown:** Delete synthetic tenants and events.

## 26. Lab 23 — Distributed workflow reconciliation

**Objective:** Identify and reconcile inconsistent state after partial workflow failure.

**Prerequisites:** Local order, payment simulation, inventory simulation and durable event log.

### Procedure

1. Create a synthetic order and record its workflow ID.
2. Execute order creation and inventory reservation.
3. Simulate payment service timeout after provider-side success.
4. Simulate notification service outage.
5. Inspect each service's local state and event history.
6. Run the documented reconciliation process.
7. Verify provider-side payment state before retry or compensation.
8. Restore notification service and redrive only the authorized event.
9. Confirm the final order, inventory and payment state are consistent.
10. Record unresolved exceptions and manual approvals.

**Expected result:** Partial failure does not silently create duplicate financial effects or inconsistent business state.

**Evidence:** Workflow timeline, service state snapshots and reconciliation record.

**Teardown:** Reset synthetic workflow state.

## 27. Lab 24 — Distributed incident response tabletop

**Objective:** Practice response to a compromised producer and broker credential.

**Scenario:** A synthetic service identity is suspected of compromise. It publishes an unauthorized event to a test topic, and a consumer begins processing unexpected messages.

### Procedure

1. Assign incident commander, service owner, broker owner, IAM, AppSec, SOC and business owner.
2. Establish scope and incident timeline.
3. Identify producer identity, credential, source workload and deployment version.
4. Restrict the compromised principal and preserve broker audit logs.
5. Identify all topics/queues and consumers the principal could access.
6. Determine which messages were delivered, processed, replayed or dead-lettered.
7. Review downstream side effects and tenant impact.
8. Revoke/rotate credentials and review service trust.
9. Quarantine suspect events and reconcile business state.
10. Resume processing only after authorization, idempotency and event provenance are validated.
11. Record partner/customer/regulatory communication decisions with responsible owners.
12. Produce lessons learned and control improvements.

**Expected result:** Team can contain identity and message abuse, preserve evidence, determine business impact and recover safely.

**Evidence:** Timeline, decision log, ACL change, credential revocation and reconciliation records.

**Teardown:** Revoke exercise identities and reset test broker.

## 28. Assessment rubric

| Criterion | Points |
|---|---:|
| Architecture, service inventory and trust boundaries | 10 |
| Workload identity, mTLS and token exchange | 15 |
| Service authorization and mesh enforcement | 10 |
| Broker authentication, ACLs and administration | 10 |
| Event schema, integrity, replay and idempotency | 15 |
| Outbox, inbox, saga and reconciliation | 10 |
| Webhook, callback and partner security | 10 |
| Resilience, retry and resource controls | 5 |
| Trace privacy, detection and incident response | 10 |
| Evidence, cleanup and safe operation | 5 |
| **Total** | **100** |

Suggested training interpretation: 90–100 strong independent engineering; 75–89 competent with review; 60–74 guided remediation required; below 60 repeat the exercises. These are educational thresholds, not a certification.

## 29. Instructor review checklist

- Was the lab explicitly authorized and isolated?
- Were only synthetic tenants, credentials and events used?
- Were all services and message paths inventoried?
- Were workload and user identities treated separately?
- Was mTLS validated with invalid and unauthorized certificates?
- Were SPIFFE trust and registration boundaries understood?
- Were token audiences and delegation claims validated?
- Did every service enforce its own authorization?
- Were mesh bypass paths reviewed?
- Were Kafka/RabbitMQ permissions scoped by destination and action?
- Were schema validation and safe deserialization tested?
- Were duplicate delivery and acknowledgement-loss cases tested?
- Were outbox/inbox transactions atomic and concurrency-safe?
- Were saga compensation and uncertain external outcomes handled?
- Were webhook signatures verified over the correct representation?
- Were replay and callback SSRF controls tested?
- Were DLQ access and redrive restricted?
- Were retries bounded and circuit-breaker behavior validated?
- Were trace context and sensitive telemetry reviewed?
- Was service discovery treated as location, not identity?
- Were partner access rotation and termination tested?
- Was distributed workflow reconciliation documented?
- Was evidence sanitized and teardown verified?

## 30. References

1. NIST SP 800-204 series: https://csrc.nist.gov/pubs/sp/800/204/final
2. NIST SP 800-204A: https://csrc.nist.gov/pubs/sp/800/204/a/final
3. NIST SP 800-204B: https://csrc.nist.gov/pubs/sp/800/204/b/final
4. NIST SP 800-204C: https://csrc.nist.gov/pubs/sp/800/204/c/final
5. NIST SP 800-204D: https://csrc.nist.gov/pubs/sp/800/204/d/final
6. OWASP Microservices Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Microservices_Security_Cheat_Sheet.html
7. AsyncAPI 3.0.0: https://www.asyncapi.com/docs/reference/specification/v3.0.0
8. CloudEvents 1.0.2: https://github.com/cloudevents/spec
9. SPIFFE standards: https://github.com/spiffe/spiffe/tree/main/standards
10. gRPC authentication: https://grpc.io/docs/guides/auth/
11. Apache Kafka security: https://kafka.apache.org/documentation/#security
12. RabbitMQ access control: https://www.rabbitmq.com/docs/access-control
13. W3C Trace Context: https://www.w3.org/TR/trace-context/
14. OpenTelemetry sensitive data handling: https://opentelemetry.io/docs/security/handling-sensitive-data/

## 31. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial distributed systems and integration security lab specifications |
