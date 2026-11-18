# Distributed Systems and Integration Security Engineering

| Field | Value |
|---|---|
| Document ID | UAPPSEC-11-001 |
| Status | Draft engineering baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Microservices, service-to-service communication, event-driven systems, message brokers, webhooks, service mesh, distributed workflows and third-party integrations |
| Classification | Public |

## 1. Executive summary

Distributed systems divide application behavior across independently deployed services, processes, teams, infrastructure boundaries and organizations. A request may cross an API gateway, several microservices, a service mesh, a message broker, asynchronous workers, third-party APIs and data stores before a business operation is complete. Each hop introduces a trust decision, an availability dependency, a data-handling boundary and an opportunity for identity or authorization context to be lost or misinterpreted.

The security boundary is therefore not the browser-to-API edge. It is the complete business workflow, including synchronous calls, asynchronous messages, scheduled jobs, retries, callbacks, event replay, dead-letter queues, administrative tools and downstream integrations.

A distributed system can fail securely at one service and still fail overall:
- A gateway authenticates a user, but a downstream service trusts a caller-supplied user ID.
- A service mesh establishes mTLS, but the receiving service accepts every authenticated workload.
- A message broker authenticates a producer, but permits it to publish to every topic.
- A consumer processes a valid event more than once and duplicates a payment or account change.
- A webhook signature is checked, but a previously valid request can be replayed.
- A retry policy amplifies an outage into a cascading failure.
- A trace ID is propagated, but sensitive data is copied into trace baggage and exported to a third party.
- A third-party integration is trusted indefinitely after its certificate, signing key, permissions or business relationship changes.

The engineering objective is to preserve identity, authorization, integrity, confidentiality, ordering assumptions, tenant context, workflow state and evidence across every boundary. Controls must be designed for failure, duplication, delay, partial completion, compromised services, stale trust and cross-organization communication.

**Core rule:** authenticate each caller or producer, authorize the exact action at the receiving boundary, validate the message and business state, constrain replay and resource consumption, and preserve an auditable outcome.

## 2. Purpose, audience and applicability

### 2.1 Purpose

Provide a reusable engineering playbook to design, implement, review, test and operate distributed application architectures and integrations. It supports architecture reviews, microservices and platform engineering, API and event-driven product security, workload identity and zero-trust architecture, message broker and queue security, webhook and partner integration security, distributed transaction and workflow assurance, security testing, detection engineering, incident response and supplier assurance.

### 2.2 Audience

Application security engineers, software architects, backend developers, platform engineers, API teams, integration engineers, SRE, DevSecOps, cloud security, IAM, SOC, incident response, product owners, technology risk and auditors.

### 2.3 Systems in scope

- Synchronous microservice communication over HTTP/REST, gRPC and other RPC protocols.
- Service discovery, API gateways, ingress, egress and service mesh.
- Human and workload identity propagation.
- OAuth-based delegation and token exchange.
- mTLS, workload certificates and service identity.
- Event-driven architectures and event buses.
- Message brokers, queues, topics, streams and consumer groups.
- Kafka, RabbitMQ and managed messaging services.
- CloudEvents and AsyncAPI-described interfaces.
- Webhooks, callbacks, partner APIs and SaaS integrations.
- Distributed transactions, sagas, outbox/inbox patterns and event sourcing.
- Distributed caches, tracing, logs and telemetry.
- Multi-tenant and cross-organization integration paths.

### 2.4 Out of scope and specialist dependencies

This is not a full protocol specification, broker administration manual, cryptographic design standard, distributed database textbook or legal opinion. Protocol-level behavior must be checked against the exact specification and implementation version. Broker security must be validated against the deployed release, authentication plugin, authorization model, topology and managed-service offering.

This chapter complements rather than replaces Chapter 06 API and Service Security, Chapter 07 Identity and Access Security, Chapter 08 Data Security and Privacy Engineering, Chapter 10 Cloud-Native Application Security, and planned Chapters 13 Software Supply Chain Security, 14 Security Verification and Assessment and 16 AppSec Operations and Incident Response.

## 3. Terminology

| Term | Meaning |
|---|---|
| Distributed system | Multiple independent processes/services cooperate to provide a system capability |
| Microservice | Independently deployable service implementing a bounded capability |
| Service-to-service | Communication between workload identities rather than direct end-user interaction |
| Workload identity | Cryptographic or platform identity assigned to a process, service or runtime |
| Service mesh | Infrastructure layer providing service discovery, traffic management, telemetry and often workload security |
| Sidecar proxy | Per-workload proxy that handles network traffic and may enforce transport or policy controls |
| East-west traffic | Traffic between services inside an environment or network |
| North-south traffic | Traffic entering or leaving an application environment |
| Message broker | Infrastructure that accepts, routes, stores or delivers messages |
| Queue | Messaging destination commonly distributing messages to one or more consumers |
| Topic | Logical stream or publish/subscribe destination |
| Event | Immutable statement that something occurred |
| Command | Request for a receiver to perform an action |
| Event envelope | Metadata and payload that describe a message/event |
| Consumer | Component that receives and processes messages |
| Producer | Component that publishes messages |
| Consumer group | Coordinated group of consumers sharing partitions or messages |
| Delivery semantics | Guarantees such as at-most-once, at-least-once or effectively-once processing |
| Idempotency | Repeating the same operation does not create an unintended additional effect |
| Replay | Re-submission of a previously valid message or request |
| Dead-letter queue | Destination for messages that cannot be processed under configured rules |
| Outbox pattern | Persisting an event intent with business state, then publishing it asynchronously |
| Inbox pattern | Persisting message identity/processing state to prevent duplicate effects |
| Saga | Distributed business transaction coordinated through local transactions and compensating actions |
| Correlation ID | Identifier linking related operations across a workflow |
| Trace context | Standardized distributed tracing context propagated across process boundaries |
| Baggage | Propagated key-value context that can cross service boundaries |
| Token exchange | Issuing a new token from a presented token for a different audience or delegation context |
| Confused deputy | A privileged component is tricked into exercising its authority for an unauthorized caller |
| Trust domain | Namespace and authority boundary for workload identities and trust bundles |
| Schema registry | System for managing message schemas and compatibility rules |

## 4. Distributed-system reference architecture

### 4.1 Logical architecture

~~~mermaid
flowchart TB
    USER["User / Partner / External System"]
    EDGE["Edge API Gateway / WAF"]
    AUTH["Identity Provider / Token Service"]
    subgraph TRUST["Application Trust Domain"]
      A["Order Service"]
      B["Payment Service"]
      C["Inventory Service"]
      D["Notification Service"]
      MESH["Service Mesh / Workload Identity"]
      BROKER["Message Broker / Event Bus"]
      WORKER["Async Consumers / Workers"]
      DATA["Databases / Object Stores"]
      OBS["Logs / Metrics / Traces"]
    end
    subgraph PARTNER["External Trust Domain"]
      WEBHOOK["Partner Webhook Endpoint"]
      EXT["Third-Party API"]
    end
    USER --> EDGE
    EDGE --> A
    AUTH --> EDGE
    A <--> MESH
    B <--> MESH
    C <--> MESH
    D <--> MESH
    A --> BROKER
    B --> BROKER
    C --> BROKER
    BROKER --> WORKER
    WORKER --> DATA
    A --> DATA
    B --> DATA
    C --> DATA
    A --> OBS
    B --> OBS
    C --> OBS
    WORKER --> OBS
    A --> EXT
    EXT --> WEBHOOK
    WEBHOOK --> A
~~~

The diagram is conceptual. A production design must show actual service identities, token issuers, certificate authorities, trust domains, network paths, broker namespaces, topic/queue ACLs, message schemas, data owners, partner trust, telemetry destinations and failure handling.

### 4.2 Synchronous and asynchronous boundaries

| Property | Synchronous request/response | Asynchronous message/event |
|---|---|---|
| Caller knowledge | Usually receives immediate response | Producer may not know processing outcome |
| Authentication | Connection and/or request identity | Broker connection and message origin/producer identity |
| Authorization | At each service operation | At publish, consume and business processing |
| Retry | Client, proxy or service retry | Broker redelivery, consumer retry and replay |
| Duplication | Client retries can duplicate side effects | At-least-once delivery commonly creates duplicates |
| Ordering | Request sequence and concurrent execution | Partition, queue or broker-specific ordering |
| Timeout | Caller waits for bounded response | Processing and acknowledgement deadlines |
| Failure | Error response or connection failure | Delayed, retried, dead-lettered or lost message |
| Evidence | Request/response logs and trace | Producer, broker, consumer and workflow records |

Do not assume that an HTTP 200 response means downstream asynchronous work completed. Do not assume a broker acknowledgement means the business transaction committed.

### 4.3 Trust boundaries

Identify at least:
1. External user/partner to gateway.
2. Gateway to first application service.
3. Service A to Service B.
4. Workload identity provider to workload.
5. Service to authorization/token service.
6. Producer to broker.
7. Broker to consumer.
8. Consumer to database or external API.
9. Service to third-party SaaS.
10. Third-party callback to webhook endpoint.
11. Tenant A to Tenant B.
12. Production to non-production.
13. Service to telemetry collector.
14. Telemetry collector to external observability provider.
15. Primary region to disaster recovery region.
16. Human operator to broker, mesh and service administration.

For every boundary, record subject, issuer, authentication method, authorization decision point, data classification, protocol, timeout, retry behavior, replay protection, telemetry and owner.

## 5. Threat model

### 5.1 Adversary profiles

- External attacker who can invoke exposed APIs or webhooks.
- Malicious or compromised tenant publishing crafted events.
- Attacker who compromises one service and attempts lateral movement.
- Attacker with broker credentials or topic/queue access.
- Stolen workload token or certificate holder.
- Malicious or compromised third-party integration.
- Insider with excessive broker, mesh or service administration rights.
- Compromised CI/CD pipeline deploying a malicious service.
- Attacker exploiting message deserialization, schema or parser weaknesses.
- Ransomware or extortion actor disrupting message flow or deleting evidence.

### 5.2 High-value assets

- User and workload identities, tokens, certificates and private keys.
- Authorization policy, trust bundles, service discovery and mesh configuration.
- Business commands, events, payment instructions and workflow state.
- Broker credentials, ACLs, topics, queues, offsets and retained messages.
- Customer and tenant data in payloads, headers, traces and dead-letter queues.
- Partner API credentials, webhook signing secrets and callback allowlists.
- Schema registry, event contracts and compatibility rules.
- Outbox/inbox tables, idempotency records and transaction state.
- Logs, traces, correlation identifiers and security audit records.
- Administrative control planes and emergency recovery paths.

### 5.3 Attack-path catalogue

| Attack path | Preconditions | Potential impact | Primary controls |
|---|---|---|---|
| Service identity spoofing | Weak or absent workload authentication | Unauthorized service calls and lateral movement | mTLS/workload identity, trust-domain validation |
| Over-trusted mesh identity | Mesh authenticates caller but receiver lacks authorization | Any authenticated workload invokes sensitive operations | Service-level authorization and policy tests |
| Token audience confusion | Token accepted by unintended service | Token replay across services | Audience/issuer/subject validation, token exchange |
| Confused deputy | Privileged service accepts untrusted caller context | Unauthorized data access or privileged downstream action | Explicit delegation, resource authorization and scoped tokens |
| Broker credential theft | Static or broad broker credential | Topic/queue read/write, data exfiltration or command injection | Short-lived identity, ACLs, secret rotation |
| Unauthorized topic publish | Broad producer ACL | Forged business event or downstream state manipulation | Producer/topic authorization, schema validation and event provenance |
| Unauthorized consumption | Broad consumer ACL | Sensitive data disclosure or workflow manipulation | Consumer group/topic ACLs, encryption and audit |
| Message replay | No unique event ID, expiry or idempotency | Duplicate payments, account changes or notifications | Event ID, idempotency ledger, replay window |
| Poison message | Unsafe parser or unexpected payload | Consumer crash, code execution or processing denial | Schema validation, safe parsing, resource bounds, quarantine |
| Schema confusion | Incompatible or ambiguous message contracts | Incorrect interpretation, validation bypass or data corruption | Versioned schemas, compatibility policy and strict validation |
| DLQ data leakage | DLQ accessible to broad operators or tools | Sensitive payload exposure | DLQ ACLs, encryption, retention and redaction |
| Webhook forgery | Weak signature or secret management | Fake state changes or unauthorized workflow triggers | Signature verification, key rotation and sender authorization |
| Webhook replay | Signature valid but no timestamp/nonce check | Repeated action | Timestamp tolerance, unique event IDs and idempotency |
| Callback SSRF | Caller controls callback URL | Internal service probing or cloud metadata access | URL allowlist, DNS/redirect checks and egress controls |
| Trace context abuse | Untrusted trace headers accepted blindly | Log injection, cardinality attack or information leakage | Strict parsing, bounds, sampling and trust boundary reset |
| Retry storm | Unbounded retries and no jitter/budget | Cascading outage and resource exhaustion | Bounded retry, backoff, jitter, circuit breaker and bulkhead |
| Out-of-order events | Ordering assumptions not enforced | Invalid workflow transitions | Partitioning, sequence numbers and state machine validation |
| Cross-tenant event leakage | Tenant identity trusted from payload only | Cross-tenant data disclosure or action | Authenticated producer context and server-side tenant authorization |
| Integration privilege drift | Partner access not periodically reviewed | Persistent unauthorized access | Contract review, scoped identity, expiry and access review |
| Broker administration compromise | Shared/admin credentials or exposed management interface | Global message access and control | Privileged access, network restriction and audit |
| Telemetry data exposure | Sensitive attributes exported in spans | PII, token or business data leakage | Data minimization, redaction and collector controls |
| Partial transaction failure | Distributed side effects lack recovery design | Inconsistent order/payment/inventory state | Saga, outbox/inbox, reconciliation and compensation |
| Service discovery poisoning | Untrusted registration or DNS manipulation | Traffic redirection and service impersonation | Authenticated registration, TLS identity validation and DNS controls |

### 5.4 Threat-modeling workflow

1. Define business workflow and system owners.
2. Identify all synchronous and asynchronous components.
3. Draw trust boundaries and message/data flows.
4. Inventory human, service, broker, partner and operator identities.
5. Identify commands, events, notifications and data exports.
6. Mark message producers, brokers, consumers and replay paths.
7. Identify ordering, delivery, retry, timeout and consistency assumptions.
8. Apply STRIDE and abuse-case analysis at each boundary.
9. Identify tenant and data ownership semantics.
10. Record threat, precondition, impact, control, residual risk and owner.
11. Define negative tests and expected evidence.
12. Reassess after topology, broker, identity or integration changes.

## 6. Service-to-service identity and authentication

### 6.1 Separate workload identity from user identity

A receiving service often needs to know both:
- Which workload is making this network call?
- On whose behalf, if anyone, is the workload acting?

These are different identities. A workload certificate identifies a service or process. A user access token or delegated assertion conveys end-user context. Do not substitute one for the other.

The receiver should validate the caller workload identity and separately validate any user/delegation context required for the business operation.

### 6.2 Mutual TLS

mTLS provides mutual certificate-based authentication at the transport layer and protects the channel. It does not determine whether an authenticated workload may perform a specific operation or access a particular tenant's record.

Implementation requirements:
- Use approved TLS versions and cipher configuration.
- Validate certificate chain, issuer, validity period, key usage and identity mapping.
- Bind certificates to workload identity, not merely an arbitrary subject string.
- Maintain trust bundles and certificate issuance policy.
- Automate short-lived certificate issuance and renewal.
- Plan revocation, compromise response and trust-domain changes.
- Prevent fallback to plaintext or unauthenticated listeners.
- Validate the identity at the actual receiving boundary.
- Record peer identity and authorization outcome.
- Test proxy-to-proxy and application-to-application paths separately.

mTLS termination at a gateway or sidecar means the downstream application may not directly observe the original peer certificate. If identity is forwarded in headers or metadata, the receiving service must accept that assertion only from a trusted proxy, prevent client spoofing, and validate its integrity and provenance.

### 6.3 Workload identity with SPIFFE/SPIRE

SPIFFE defines a portable identity namespace and SVID documents; the Workload API provides a standardized way for workloads to obtain identity material. X.509-SVIDs can establish TLS and are generally preferable to replayable JWT-SVIDs where the architecture supports them. JWT-SVIDs require tight audience, lifetime and replay handling.

Design:
1. Define trust domains and SPIFFE ID naming conventions.
2. Establish node/workload attestation and registration policy.
3. Ensure only the intended workload can access its identity endpoint.
4. Issue short-lived SVIDs and trust bundles.
5. Validate the exact SPIFFE ID at the receiver.
6. Restrict trust-domain federation to explicit peers.
7. Rotate keys/certificates and test bundle updates.
8. Monitor issuance, renewal, failed attestation and unexpected identity use.
9. Revoke or remove registration when workloads are decommissioned.
10. Document behavior during identity provider or trust-bundle outage.

### 6.4 OAuth and token exchange

Use token exchange when a service must obtain a token appropriate for a downstream audience or explicit delegation context. A service should not forward a broad token to every downstream dependency.

Requirements:
- Validate issuer, audience, expiry, not-before, signature and intended token profile.
- Restrict accepted algorithms and key sources.
- Validate scopes/claims against the service's own policy.
- Bind tokens to intended clients or proof-of-possession where appropriate.
- Use distinct audiences for distinct resource servers.
- Limit token lifetime and refresh authority.
- Distinguish impersonation from delegation.
- Preserve the original actor and the acting service where supported.
- Prevent privilege amplification during exchange.
- Reject tokens intended for another environment or trust domain.

A signed JWT is not inherently safe for every service. Signature verification alone does not prove that the token is intended for the current audience or authorizes the requested object and action.

### 6.5 Identity propagation patterns

| Pattern | Use | Main risk | Required safeguard |
|---|---|---|---|
| Token forwarding | Downstream service needs original user token | Token audience too broad; token leakage | Narrow audience, scope and lifetime; validate at every service |
| Token exchange | Downstream needs a distinct audience or delegated token | Incorrect actor/delegation semantics | Restrict subject/actor and target audience; record exchange |
| Signed internal assertion | Gateway conveys authenticated context to internal service | Forged headers or trust in arbitrary proxy | Cryptographic integrity, trusted issuer and proxy-only acceptance |
| mTLS plus user token | Authenticate workload and user context separately | Mistaking workload authentication for user authorization | Validate both identities and authorize business action |
| Brokered workflow identity | Async worker acts after user request | User token expiry or over-broad stored credential | Persist minimal authorized intent and re-evaluate policy at processing time |

Do not blindly persist a long-lived bearer token inside an event for a future consumer. Prefer a minimal, authorized business command with actor and correlation metadata, then let the consumer use its own workload identity and re-check the required authorization/state.

## 7. Service-level authorization

### 7.1 Every receiving service enforces its own authorization

A gateway or service mesh can enforce common ingress and workload policies. It cannot automatically understand all domain-specific object, property, tenant and workflow rules.

At each service boundary:
1. Authenticate the workload caller.
2. Validate delegated user context if present.
3. Identify the operation and target resource.
4. Resolve tenant and ownership from trusted server-side data.
5. Evaluate role, attribute, relationship and business-state policy.
6. Apply field/property-level restrictions.
7. Validate workflow state and separation of duties.
8. Record allow/deny decision with safe context.
9. Fail closed when required authorization inputs are unavailable.

### 7.2 Authorization policy design

Use RBAC for stable roles, ABAC for contextual attributes, and relationship-based authorization for graph or ownership relationships where appropriate. Many systems need a combination.

Policy inputs may include workload identity and trust domain, user subject/actor/delegated authority, tenant and resource owner, resource classification, requested action and property, environment and deployment identity, time/risk state/transaction status, and device/network/session context where relevant.

Do not accept tenant, role, owner or permission attributes from an untrusted message payload as authoritative. Resolve or verify them using trusted identity and domain state.

### 7.3 Policy distribution and outage behavior

If authorization is centralized:
- Define policy source of truth and versioning.
- Define policy distribution and cache lifetime.
- Decide which decisions can be cached and for how long.
- Define fail-closed behavior for sensitive operations.
- Avoid stale allow decisions after revocation.
- Test policy service outage and partial network partition.
- Log policy version and decision context.
- Define emergency deny/kill-switch behavior.
- Prevent policy update channels from being writable by application workloads.

## 8. Service mesh and proxy security

### 8.1 What a service mesh can provide

Depending on implementation and configuration, a service mesh can provide workload certificate management, mTLS, service identity, traffic policy, authorization policy, retries, timeouts, circuit breaking, telemetry and controlled egress.

It is not a substitute for application security. A mesh does not inherently understand the business meaning of an order, customer, payment or tenant.

### 8.2 Mesh design requirements

- Restrict mesh control-plane access.
- Authenticate control-plane components and workload proxies.
- Protect certificate authority and trust-bundle distribution.
- Enforce strict mTLS where intended; avoid silent permissive fallback.
- Use explicit service authorization policies.
- Prevent direct pod/node paths that bypass proxy enforcement.
- Validate identity headers and metadata at trust boundaries.
- Restrict egress gateways and external service registration.
- Test sidecar-less workloads, host networking and excluded ports.
- Monitor proxy configuration changes and certificate issuance.
- Define behavior during control-plane outage and certificate expiry.
- Keep mesh and proxy versions supported and patched.

### 8.3 Gateway versus mesh versus application

| Layer | Suitable responsibilities | Not sufficient for |
|---|---|---|
| API gateway | External ingress, coarse authentication, rate limits, routing, request size and protocol controls | All internal service authorization or object-level access |
| Service mesh | Workload identity, mTLS, service-level policy, traffic and telemetry | Business ownership, tenant semantics and all application authorization |
| Application service | Domain authorization, object/property checks, business state, input validation and transaction rules | Infrastructure-wide identity and network controls |
| Broker | Producer/consumer authentication, destination ACLs, retention and delivery controls | Domain authorization and business event truth |
| Identity provider | Identity issuance, authentication and token services | Authorization of every application object and action |

### 8.4 Proxy bypass tests

Review direct pod IP access, NodePort and host networking, excluded inbound/outbound ports, sidecar injection failure, unmeshed namespaces, health and admin ports, alternate DNS names and service endpoints, gateway bypass and internal load balancer paths, proxy metadata/header spoofing, and traffic from privileged nodes and host processes.

## 9. Message broker and queue security

### 9.1 Broker security objectives

- Authenticate every producer, consumer and administrator.
- Authorize publish, consume, configure and management operations separately.
- Restrict access to specific topics, queues, exchanges, routing keys, consumer groups, virtual hosts and resources.
- Encrypt transport and protect broker-to-broker communication.
- Protect stored messages, replicas, logs and backups.
- Constrain message size, rate, retention and consumer resource use.
- Prevent unauthorized topic creation, binding changes and administrative actions.
- Monitor access, ACL changes, authentication failures and unusual consumption.
- Define broker upgrade, backup, restore and compromise response.

### 9.2 Kafka security considerations

For Apache Kafka and compatible managed services:
- Configure TLS for client, broker, controller and inter-broker communication as appropriate.
- Use a supported SASL mechanism or client certificate authentication according to the deployment.
- Enable and test authorization; authentication alone is insufficient.
- Scope ACLs to topic, group, cluster and transactional ID resources as required.
- Restrict topic creation and administrative APIs.
- Protect consumer group access and transactional producer IDs.
- Review wildcard ACLs and superuser configuration.
- Secure Kafka Connect, Streams, schema registry and administrative tooling separately.
- Protect credentials and truststores.
- Review listener exposure and advertised listener configuration.
- Audit ACL changes, topic configuration, consumer offsets and administrative operations.
- Validate retention, compaction, replication and deletion against data classification.

### 9.3 RabbitMQ security considerations

For RabbitMQ:
- Use TLS for client and inter-node connections as required.
- Use supported authentication backends and strong credential lifecycle.
- Avoid remote use of default guest credentials.
- Restrict users to required virtual hosts.
- Apply configure, write and read permissions with resource patterns.
- Review topic permissions and exchange/queue bindings.
- Restrict management UI/API and administrative tags.
- Use per-service credentials or identity integration where supported.
- Monitor connection churn, authentication failures, permission changes and queue growth.
- Secure definitions exports, configuration, cookie secrets and backups.
- Review federation, shovel, plugins and management extensions as separate trust paths.

### 9.4 Managed brokers

Managed services may operate the broker infrastructure but customer responsibilities commonly include identity, client authentication, network exposure, topic/queue authorization, encryption settings, data retention, message payload privacy, consumer code, integration secrets and monitoring. Verify the exact responsibility model for the service and SKU.

### 9.5 Producer and consumer authorization matrix

| Principal | Destination | Allowed action | Example restriction |
|---|---|---|---|
| Order service | orders.created | Publish | Cannot consume payment events |
| Payment service | orders.created | Consume | Cannot configure or delete topic |
| Payment service | payments.completed | Publish | Cannot publish to admin topic |
| Notification worker | notifications.email | Consume | Cannot read payment payloads |
| Reporting service | orders.summary | Consume | Read-only, no raw customer PII |
| Platform operator | Broker control plane | Admin as approved | JIT access, MFA, audit and expiry |

This is illustrative. Real topic names, principals and permissions must be mapped to business data and workload owners.

## 10. Event and message security

### 10.1 Event versus command

An event states that something happened. A command requests an action. This distinction affects authorization, idempotency, audit and replay.

- Events should be immutable facts with a defined source and time.
- Commands should express intended action and be authorized at execution time.
- Do not treat an event's presence on a broker as proof that the event is true.
- Do not allow a producer to claim another service's identity through payload fields.
- Define who may publish each event type and who may consume it.

### 10.2 Event envelope

A message envelope should define unique event/message ID, event type and schema version, producer/source identity, subject or aggregate identifier where appropriate, occurrence time and optional expiry, tenant context derived from trusted origin or verified claim, correlation and causation identifiers, content type and payload schema, optional signature/integrity metadata where threat model requires it, and data classification and retention handling.

Example CloudEvents-style event (illustrative; identifiers and payload are synthetic):

~~~json
{
  "specversion": "1.0",
  "id": "evt-8f31d7c2",
  "source": "urn:example:orders-service",
  "type": "com.example.orders.created.v1",
  "subject": "order/ORD-TEST-1042",
  "time": "2026-11-18T10:30:00Z",
  "datacontenttype": "application/json",
  "dataschema": "https://schemas.example.invalid/orders/created/1.0.0",
  "data": {
    "orderReference": "ORD-TEST-1042",
    "tenantReference": "TENANT-TEST-A",
    "amountMinor": 12500,
    "currency": "USD"
  }
}
~~~

The payload's tenantReference is data, not proof of tenant authorization. The consumer must validate it against trusted producer identity and domain state.

### 10.3 Schema validation and evolution

- Validate message structure before business processing.
- Enforce maximum payload, nesting, array, string and numeric bounds.
- Reject unknown critical enum values and ambiguous types.
- Use safe deserialization; avoid unsafe native object deserialization.
- Pin schema and compatibility policy.
- Define backward/forward compatibility and consumer rollout order.
- Treat schema registry as a privileged control plane.
- Restrict who can register, modify or delete schemas.
- Sign or attest schema releases where needed.
- Test malformed, truncated, oversized and semantically invalid messages.
- Prevent a schema change from silently changing authorization or financial meaning.

### 10.4 Message integrity and authenticity

Transport TLS protects data in transit between connected endpoints, but messages may be stored, forwarded, replayed or processed after transport termination. For high-risk workflows, consider application-level integrity and provenance controls.

Options include broker ACLs and authenticated producer identity, signed event envelopes or signed payloads, message authentication codes with managed keys, content digest and HTTP message signatures for applicable HTTP/webhook exchanges, and immutable audit records linking producer, event ID, payload digest and processing outcome.

If messages are signed:
- Define exactly which fields are covered.
- Include event ID, type, source, timestamp, schema version and payload digest.
- Define key ownership, rotation, revocation and trust.
- Prevent signature stripping or algorithm downgrade.
- Validate identity-to-key binding.
- Define replay handling separately; a valid signature does not prevent replay.
- Avoid exposing signing keys to arbitrary application components.

### 10.5 Replay, duplicates and idempotency

At-least-once delivery means consumers must expect duplicates. A unique message ID alone is not enough unless processing state is stored atomically with the business effect.

Recommended consumer sequence:
1. Authenticate producer and broker connection.
2. Validate event type, schema, expiry and trusted source.
3. Validate tenant and business authorization.
4. Begin database transaction.
5. Insert message ID into inbox/idempotency table with a uniqueness constraint.
6. If already processed, return the recorded outcome without repeating the effect.
7. Apply business state change.
8. Persist processing result and outbox event in the same transaction where appropriate.
9. Commit.
10. Acknowledge the broker message only after durable processing.

If the database commit succeeds but broker acknowledgement fails, redelivery should be harmless. If processing fails before commit, the message should be retried or quarantined according to policy.

### 10.6 Ordering and sequencing

Do not assume global message ordering unless the broker and design explicitly guarantee it. Define partition key or queue grouping, aggregate/entity sequence number, expected state transition, out-of-order behavior, late event policy, duplicate and gap detection, and reconciliation/replay procedure.

Consumers should reject or quarantine impossible state transitions rather than blindly applying stale events.

## 11. Distributed transactions and workflow integrity

### 11.1 Why distributed transactions fail

A business workflow may update an order database, call a payment provider, reserve inventory and publish notifications. These actions do not usually share one atomic database transaction. Network failures, timeouts and partial commits can leave different services with different views of state.

### 11.2 Transactional outbox

The outbox pattern records the business state change and event intent in one local database transaction. A separate publisher reads committed outbox rows and publishes them. The publisher may publish a row more than once, so consumers still require idempotency.

Requirements:
- Commit business update and outbox row atomically.
- Use stable event IDs.
- Restrict outbox table access.
- Protect payloads and redact unnecessary sensitive fields.
- Use publisher leases/locking or safe parallelization.
- Track attempts, last error and published state.
- Prevent unbounded outbox growth.
- Monitor lag and poison records.
- Define cleanup and retention after confirmed publication.

### 11.3 Inbox pattern

The inbox records message identity and processing state to prevent duplicate effects.

Requirements:
- Enforce uniqueness for event ID within the correct producer/consumer scope.
- Persist inbox state and business effect atomically where possible.
- Distinguish received, processing, completed and failed states.
- Handle concurrent duplicate delivery.
- Retain records long enough to cover replay and broker retention windows.
- Define reprocessing and operator override with audit.

### 11.4 Saga and compensating actions

A saga coordinates a business transaction through local transactions and compensating actions. A compensation is not necessarily a perfect rollback; it is a new business action that restores an acceptable state.

Design:
- Explicit state machine and allowed transitions.
- Unique workflow and step IDs.
- Per-step timeout and retry policy.
- Idempotent command handling.
- Compensation owner and failure handling.
- Manual intervention and escalation state.
- Durable event history and audit.
- Protection against duplicate or forged completion events.
- Reconciliation for uncertain external outcomes.
- Safe cancellation and expiry behavior.

Do not assume a timeout means the remote action did not occur. A payment request may have succeeded while the response was lost. Query provider state using a stable idempotency key before retrying a potentially non-idempotent action.

### 11.5 Event sourcing

Where event sourcing is used:
- Protect event store write and read permissions.
- Validate event schema and producer identity.
- Preserve append-only history where required.
- Prevent unauthorized event mutation/deletion.
- Protect snapshots and projections.
- Define replay and rebuild permissions.
- Ensure replay does not re-trigger external side effects unintentionally.
- Separate historical event truth from derived read models.
- Protect personal data and retention obligations; immutable history may complicate deletion requirements and needs an explicit design.

## 12. Webhook and callback security

### 12.1 Inbound webhook

- Authenticate the sender using a documented signature, mTLS, OAuth or equivalent.
- Verify signature over the exact raw bytes or canonical representation defined by the provider.
- Compare signatures using constant-time comparison where applicable.
- Bind signing keys to the registered partner and endpoint.
- Validate timestamp and enforce a bounded clock-skew window.
- Track event IDs/nonces and reject replay.
- Validate content type, size, schema and expected event type.
- Enforce tenant and resource ownership.
- Return acknowledgement only after durable receipt according to the contract.
- Process asynchronously where appropriate.
- Rate-limit by partner and endpoint.
- Record safe evidence without logging secrets or full sensitive payloads.
- Support key rotation with explicit overlap and retirement.

Never parse and reserialize JSON before verifying a signature if the provider's signature is defined over the original raw request body.

### 12.2 Outbound webhook and callback URL

A feature that sends a request to a user- or partner-supplied callback URL creates an SSRF boundary.

Controls:
1. Prefer registered partner endpoints over arbitrary user URLs.
2. Require HTTPS and validate certificate/hostname.
3. Apply hostname and port allowlists.
4. Resolve A and AAAA records and reject loopback, link-local, private, reserved and internal destinations unless specifically approved.
5. Revalidate every redirect and resolved destination.
6. Prevent DNS rebinding and alternate IP encodings.
7. Restrict outbound network paths and metadata service access.
8. Do not forward internal credentials, cookies or authorization headers to callback targets.
9. Apply response size, timeout and redirect limits.
10. Log destination identity and outcome safely.

### 12.3 Webhook delivery reliability

- Use stable delivery ID.
- Use bounded retry with exponential backoff and jitter.
- Set a maximum retry age and attempt count.
- Define manual redrive and replay authorization.
- Preserve original event ID across retries.
- Require receiver idempotency.
- Separate transient errors from permanent validation errors.
- Avoid retrying 4xx responses blindly.
- Define delivery status and partner-visible observability.
- Protect the delivery queue and payload retention.

## 13. Third-party and cross-organization integrations

### 13.1 Integration inventory

For each integration record business purpose and data flow, provider legal entity and service, system owner and partner owner, data categories and classification, API/webhook/broker/file-transfer mechanism, authentication and authorization model, credential/key/certificate owner and expiry, permitted endpoints/operations/data scope, regions and subprocessors, rate limits/availability/incident contacts, retention/deletion/export behavior, contract/SLA/security evidence/exit plan, review date and termination procedure.

### 13.2 Least privilege and isolation

- Use distinct credentials per integration and environment.
- Scope tokens and API keys to required endpoints and actions.
- Separate production and test identities.
- Restrict source networks only as an additional control, not as sole authentication.
- Avoid shared partner accounts.
- Use mTLS or signed requests for high-risk interfaces where supported.
- Limit outbound destinations and data fields.
- Validate inbound payloads and event sources.
- Prevent one partner from selecting another partner's tenant context.
- Review access and credentials at contract renewal and personnel changes.

### 13.3 Third-party compromise

Plan for a partner signing-key compromise, malicious payload, data breach, service outage or abrupt termination. Maintain a process to disable credentials, block destinations, pause message consumption, quarantine events, rotate keys, reconcile in-flight transactions and notify relevant owners.

## 14. Resilience and denial-of-service controls

### 14.1 Timeouts and deadlines

- Set connection, TLS handshake, request, response and total workflow deadlines.
- Propagate remaining deadline where protocol supports it.
- Avoid nested services each applying a larger timeout than the caller.
- Define cancellation behavior for abandoned requests.
- Ensure timeouts do not cause duplicate side effects.
- Bound broker processing and acknowledgement time.

### 14.2 Retries and backoff

- Retry only operations that are safe or protected by idempotency.
- Use exponential backoff with jitter.
- Set retry budgets and maximum attempts.
- Avoid retrying permanent validation/authentication failures.
- Prevent retry multiplication across layers.
- Use circuit breakers for unhealthy dependencies.
- Monitor retry rate and queue age.
- Ensure operator redrive follows the same idempotency and authorization rules.

### 14.3 Bulkheads and resource controls

- Isolate thread pools, connection pools and queues by critical dependency.
- Bound concurrent requests and in-flight messages.
- Set maximum message size and batch size.
- Limit consumer prefetch and unacknowledged messages.
- Apply per-tenant quotas.
- Protect expensive parsing, decompression and cryptographic operations.
- Define backpressure and load shedding.
- Alert on queue depth, oldest message age and consumer lag.

### 14.4 Circuit breaker caveats

A circuit breaker reduces repeated calls to a failing dependency. It does not fix the dependency, preserve business state or guarantee safe recovery. Test half-open behavior, probe volume, fallback correctness, retry interaction and data consistency.

## 15. Distributed observability and trace security

### 15.1 Correlation and trace context

Use standard trace context where possible. Treat incoming trace headers and baggage as untrusted input at external boundaries.

- Validate header syntax and size.
- Generate or reset context according to trust policy.
- Do not place secrets, tokens, PII or business-confidential values in baggage.
- Bound attribute count, length and cardinality.
- Avoid user-controlled high-cardinality metric labels.
- Prevent trace context from being used as authentication or authorization.
- Propagate correlation and causation IDs separately where needed.
- Preserve trace linkage across asynchronous producer/consumer processing.
- Do not assume every message remains in one trace for long-running workflows.
- Protect telemetry transport and backend access.

### 15.2 Sensitive data in telemetry

Exclude or redact access tokens, refresh tokens, API keys, session cookies, passwords, private keys, signing secrets, full payment credentials, unnecessary personal data, health/special-category data unless approved and minimized, full message payloads where metadata is sufficient, and internal topology or confidential partner identifiers when not required.

Instrumentation libraries and automatic capture can collect data that application teams did not explicitly log. Review instrumentation, collectors, exporters, sampling, retention, access and third-party processor terms.

### 15.3 Required distributed telemetry

Capture, where appropriate:
- Workload identity and authenticated peer.
- User/delegation context in a safe pseudonymous form.
- Service, operation and environment.
- Event/message ID, type and schema version.
- Producer, broker and consumer group.
- Correlation, causation and trace identifiers.
- Authorization decision and policy version.
- Retry, redelivery, DLQ and idempotency result.
- Processing duration and outcome.
- Destination and dependency result.
- Key/certificate lifecycle events.
- Administrative policy and ACL changes.

## 16. Configuration and operational security

- Store service credentials and signing keys in approved secret/key systems.
- Rotate certificates, tokens and broker credentials.
- Protect service discovery, DNS and control-plane configuration.
- Restrict broker and mesh management interfaces to trusted administration networks.
- Separate application, broker and platform administrators.
- Use just-in-time privileged access for high-impact changes.
- Review service registrations and stale workloads.
- Protect schema registries and API/event contracts.
- Version and approve authorization policies.
- Keep broker, proxy, runtime and client libraries supported.
- Monitor configuration drift.
- Protect backups, offsets, outbox/inbox state and DLQ exports.
- Test restore and replay in isolated environments.
- Document emergency shutdown, quarantine and redrive.

## 17. Security verification methodology

### 17.1 Assessment phases

1. Authorization, scope and rules of engagement.
2. Architecture and workflow discovery.
3. Service and integration inventory.
4. Workload identity and mTLS review.
5. User identity propagation and token exchange review.
6. Service-level authorization assessment.
7. Service mesh and gateway bypass review.
8. Broker authentication, authorization and encryption review.
9. Topic, queue, group and virtual-host permission review.
10. Event schema, integrity and provenance review.
11. Replay, idempotency and ordering tests.
12. Outbox, inbox, saga and distributed transaction review.
13. Webhook signature, replay and SSRF review.
14. Third-party integration review.
15. Resilience, retry and resource exhaustion review.
16. Telemetry privacy and security review.
17. Detection and incident response validation.
18. Findings, remediation and retest.

### 17.2 Rules of engagement

- Obtain written authorization from application, platform, broker and integration owners.
- Confirm which services, namespaces, topics, queues, consumer groups, partner endpoints and environments are in scope.
- Use synthetic tenants, records, credentials and events.
- Do not publish test messages to production topics unless explicitly approved.
- Do not replay real payment, identity, deletion or operational commands.
- Do not perform uncontrolled load, broker flood, consumer lag or poison-message tests.
- Do not access or export real DLQ payloads unless approved and necessary.
- Do not rotate or revoke production keys without a change plan.
- Do not test third-party endpoints without partner authorization.
- Define stop conditions and emergency contacts.
- Preserve sanitized evidence and redact all secrets.
- Ensure test events cannot trigger real downstream actions.

### 17.3 Distributed systems test catalogue

The IDs below are internal project identifiers, not external standards control IDs.

| Test ID | Domain | Test focus | Expected result |
|---|---|---|---|
| DIST-T-001 | Architecture | Inventory services, protocols and data flows | Every service and trust boundary has owner and purpose |
| DIST-T-002 | Identity | Verify each service has a distinct workload identity | No shared or ambiguous workload principal |
| DIST-T-003 | mTLS | Attempt connection without client certificate where mTLS is required | Connection is rejected |
| DIST-T-004 | Certificate validation | Test expired, untrusted, wrong-SAN/SPIFFE ID certificate | Invalid peer is rejected |
| DIST-T-005 | Trust domain | Attempt cross-domain identity not in approved federation | Untrusted domain is denied |
| DIST-T-006 | Token audience | Present token intended for another service | Receiver rejects wrong audience |
| DIST-T-007 | Token exchange | Review actor, subject, audience and delegation | No privilege amplification or unintended impersonation |
| DIST-T-008 | Identity propagation | Inject forged user/tenant headers from untrusted source | Receiver ignores or rejects spoofed context |
| DIST-T-009 | Service authorization | Authenticated workload invokes unauthorized operation | Receiver denies operation |
| DIST-T-010 | Object authorization | Service accesses another tenant's object | Cross-tenant access denied |
| DIST-T-011 | Mesh policy | Attempt direct service path bypassing proxy policy | Bypass is blocked or equivalent controls enforce |
| DIST-T-012 | Proxy trust | Send spoofed identity headers through alternate path | Untrusted identity assertion rejected |
| DIST-T-013 | Broker authentication | Connect with missing/invalid credentials | Broker rejects connection |
| DIST-T-014 | Broker authorization | Producer writes to unauthorized topic/queue | Publish denied |
| DIST-T-015 | Consumer authorization | Consumer reads unauthorized topic/queue/group | Consume denied |
| DIST-T-016 | Broker administration | Non-admin attempts topic/queue/policy change | Administrative operation denied |
| DIST-T-017 | Transport | Verify TLS and broker inter-node encryption | Required channels use approved TLS |
| DIST-T-018 | Message schema | Submit malformed, oversized or invalid event | Message rejected or safely quarantined |
| DIST-T-019 | Deserialization | Submit crafted polymorphic/native serialized payload in lab | Unsafe object construction does not occur |
| DIST-T-020 | Message integrity | Modify signed event after signing | Signature/digest validation fails |
| DIST-T-021 | Replay | Re-submit previously processed event ID | No duplicate business side effect |
| DIST-T-022 | Ordering | Deliver stale or out-of-order aggregate event | Invalid state transition rejected or reconciled |
| DIST-T-023 | Idempotency | Simulate acknowledgement loss after successful commit | Redelivery produces no duplicate effect |
| DIST-T-024 | Outbox | Crash publisher after broker publish before marking row | Duplicate publication is safe and observable |
| DIST-T-025 | Inbox | Concurrently deliver same event to multiple consumers | Only one business effect commits |
| DIST-T-026 | Saga | Fail a middle step and invoke compensation | Workflow reaches defined compensated or manual state |
| DIST-T-027 | Webhook signature | Change raw body or signature | Invalid webhook rejected |
| DIST-T-028 | Webhook replay | Resubmit valid signed webhook within/after allowed window | Duplicate or stale event rejected |
| DIST-T-029 | Callback SSRF | Use loopback, private, link-local and redirect targets | Unsafe destinations blocked |
| DIST-T-030 | Partner isolation | Use one partner credential to access another partner's resources | Cross-partner access denied |
| DIST-T-031 | Retry resilience | Simulate transient and permanent dependency errors | Bounded retries; no retry storm |
| DIST-T-032 | Resource limits | Send oversized message or high-cardinality event metadata | Resource use bounded and alert generated |
| DIST-T-033 | DLQ security | Attempt unauthorized DLQ read/redrive | Access restricted and audited |
| DIST-T-034 | Trace context | Inject oversized, malformed or sensitive baggage | Input bounded; sensitive data not exported |
| DIST-T-035 | Telemetry privacy | Inspect spans/logs for credentials and PII | Sensitive attributes are absent or redacted |
| DIST-T-036 | Service discovery | Attempt unapproved registration or endpoint substitution | Only authorized service instances are trusted |
| DIST-T-037 | Certificate lifecycle | Test rotation, expiry and revoked trust bundle | Renewal works; compromised identity is rejected |
| DIST-T-038 | Third-party lifecycle | Disable partner credential and test old access | Retired partner access fails |
| DIST-T-039 | Broker recovery | Restore test broker and replay retained messages | Recovery preserves required integrity and access controls |
| DIST-T-040 | Detection | Simulate unauthorized publish, ACL change and replay | Alerts are actionable and routed to owners |
| DIST-T-041 | Workflow authorization | Attempt command when business state prohibits action | State machine rejects operation |
| DIST-T-042 | Data minimization | Inspect event payload and DLQ retention | Only necessary fields are present and retained appropriately |

## 18. Detection engineering catalogue

| Detection ID | Scenario | Signals | Initial response |
|---|---|---|---|
| DIST-D-001 | Unusual service identity use | New source workload, trust domain or identity-to-service pair | Validate deployment and restrict identity if unauthorized |
| DIST-D-002 | mTLS/certificate anomaly | Failed certificate validation, unexpected issuer, expiry or renewal burst | Inspect CA and workload; rotate/revoke as required |
| DIST-D-003 | Token audience/delegation anomaly | Wrong audience, unexpected token exchange or actor/subject mismatch | Reject token and investigate issuer/client |
| DIST-D-004 | Unauthorized service call | Denied operation spikes or workload calling new sensitive endpoint | Review workload compromise and policy |
| DIST-D-005 | Broker credential anomaly | New source, unusual auth mechanism or repeated failures | Disable/restrict credential and review access |
| DIST-D-006 | Topic/queue ACL change | New wildcard or broad read/write/admin permission | Revert unauthorized policy and preserve audit |
| DIST-D-007 | Unusual message publishing | Volume, event type or producer deviates from baseline | Quarantine producer and inspect event provenance |
| DIST-D-008 | Consumer anomaly | New consumer group, unusual offsets or bulk reads | Restrict principal and assess data access |
| DIST-D-009 | Replay/duplicate burst | Repeated event IDs, nonce or delivery IDs | Apply idempotency/quarantine and investigate source |
| DIST-D-010 | Poison-message pattern | Repeated parse failures, crash loops or DLQ surge | Quarantine message and isolate consumer |
| DIST-D-011 | DLQ access anomaly | Unusual reads, exports or redrive by operator/service | Revoke access and review sensitive payload exposure |
| DIST-D-012 | Webhook abuse | Signature failures, timestamp violations, replay or source change | Rate-limit, reject and rotate compromised key if needed |
| DIST-D-013 | Callback SSRF attempt | Requests to internal, link-local or metadata ranges | Block egress and investigate callback feature |
| DIST-D-014 | Retry storm | Rising retries, timeout rate and queue age | Apply retry budget, circuit breaker and incident response |
| DIST-D-015 | Trace/telemetry abuse | Header size, cardinality or export volume spike | Bound context, adjust sampling and investigate |
| DIST-D-016 | Integration credential misuse | Partner key used from new context or outside expected operation | Suspend integration and contact owner |
| DIST-D-017 | Service discovery change | Unexpected endpoint registration or trust policy update | Validate change and restore trusted registry |
| DIST-D-018 | Workflow inconsistency | Invalid saga transition, repeated compensation or state mismatch | Pause workflow and reconcile business records |

A detection is not operational until its telemetry source, query, thresholds, false-positive handling, owner, runbook, severity and test evidence are defined.

## 19. Incident response and recovery

### 19.1 Response principles

- Preserve broker, service, identity, mesh, certificate, token and telemetry evidence.
- Identify affected service identities and all credentials they could access.
- Determine which messages were published, delivered, consumed, replayed or dead-lettered.
- Distinguish transport acknowledgement from business transaction completion.
- Quarantine compromised producers and consumers without deleting evidence.
- Revoke tokens, certificates, broker credentials and partner keys.
- Assess tenant and data impact across event payloads, logs, traces and DLQs.
- Determine whether external side effects occurred.
- Reconcile payment, order, inventory and workflow state with authoritative providers.
- Rebuild compromised workloads from trusted artifacts.
- Redrive only after authorization, deduplication and business-state validation.
- Coordinate partner, customer, privacy, legal and regulator communications with responsible owners.

### 19.2 Scenario playbooks

**Compromised workload identity**
1. Identify service, SPIFFE ID, issuer, certificate/token and last valid issuance.
2. Restrict the workload and revoke trust/identity as appropriate.
3. Review inbound and outbound service calls.
4. Review broker, database and external API activity.
5. Rotate downstream credentials and signing keys the service could access.
6. Inspect deployments and service discovery for persistence.
7. Rebuild from trusted artifacts and reissue identity.
8. Validate all peer authorization and record residual impact.

**Unauthorized message publication**
1. Identify producer principal, source, topic/queue and time window.
2. Restrict publish permission and quarantine affected messages.
3. Preserve broker audit, message headers, schema and payload digest.
4. Identify consumers and downstream effects.
5. Determine whether messages were processed or replayed.
6. Reverse or compensate business actions through approved workflows.
7. Remove unauthorized ACLs and rotate credentials.
8. Add producer/event authorization and detection tests.

**Webhook signing key compromise**
1. Identify partner, key ID, endpoint and exposure period.
2. Disable or rotate key using partner-approved process.
3. Reject old signatures after defined overlap.
4. Identify validly signed events during the exposure window.
5. Check event IDs, timestamps and business state.
6. Reconcile affected actions with the partner.
7. Review key storage, access and rotation controls.
8. Test the new key and replay rejection.

**Broker outage or compromise**
1. Identify affected clusters, brokers, regions and namespaces.
2. Preserve control-plane and audit evidence.
3. Restrict administration and suspect principals.
4. Determine message persistence, replication, retention and offset state.
5. Restore broker from trusted configuration and verified backup.
6. Validate ACLs, certificates, schemas and consumer offsets.
7. Reconcile in-flight events and idempotency records.
8. Resume consumers gradually and monitor duplicate/lag behavior.

## 20. Standards and framework mapping

Mappings are relevance guidance, not compliance assertions. Pin the exact edition and map individual requirements to the actual system boundary.

### 20.1 NIST SP 800-204 series

| Publication | Subject | Chapter use |
|---|---|---|
| SP 800-204 (2019) | Security strategies for microservices-based application systems | Authentication/access management, service discovery, secure communications, monitoring, resiliency, load balancing, throttling and session persistence |
| SP 800-204A (2020) | Building secure microservices-based applications using service-mesh architecture | Proxy-based mesh deployment and service security infrastructure |
| SP 800-204B (2021) | ABAC for microservices using a service mesh | Mutual authentication and scalable policy-based access control |
| SP 800-204C (2022) | DevSecOps implementation for microservices with service mesh | Application, application-services, infrastructure, policy and observability as code |
| SP 800-204D (2024) | Software supply-chain security in DevSecOps CI/CD pipelines | Artifact, provenance, SBOM and pipeline security |

These publications are a coherent reference series, but they do not replace current product-specific configuration guidance.

### 20.2 IETF and protocol standards

| Source | Relevance |
|---|---|
| RFC 8693 — OAuth 2.0 Token Exchange | Delegation and token exchange across services |
| RFC 8705 — OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens | Client certificate authentication and proof-of-possession |
| RFC 8446 — TLS 1.3, with subsequent updates | Secure transport; check current RFC status and updates |
| RFC 9110 — HTTP Semantics | HTTP request and response semantics |
| RFC 9421 — HTTP Message Signatures | Signing selected HTTP message components |
| RFC 9530 — Digest Fields | Content integrity metadata |
| RFC 9700 — OAuth 2.0 Security Best Current Practice | OAuth threat mitigation |
| RFC 9457 — Problem Details for HTTP APIs | Standardized API error representation; avoid leaking sensitive details |

Do not treat message signatures as a replacement for transport security or authorization. A signed request can still be replayed or be unauthorized.

### 20.3 AsyncAPI and CloudEvents

- AsyncAPI 3.0.0 describes message-driven application interfaces and supports protocol-specific bindings.
- CloudEvents 1.0.2 defines a common event envelope and protocol bindings including HTTP, Kafka and AMQP.
- Neither specification by itself authenticates producers, authorizes consumers, encrypts payloads, enforces tenant isolation or prevents replay.
- Use contracts as part of security review, schema governance and test generation.

### 20.4 SPIFFE and workload identity

SPIFFE standardizes workload identity concepts including SPIFFE IDs, SVIDs and the Workload API. It can support mTLS and cryptographic service identity. Operators remain responsible for attestation, trust-domain policy, registration, key lifecycle, authorization and secure Workload API exposure.

### 20.5 OWASP and NIST crosswalk

| Framework/source | Relevant topics |
|---|---|
| OWASP Microservices Security Cheat Sheet | Service-to-service authentication, authorization, identity propagation and logging |
| OWASP API Security Top 10:2023 | Object/function authorization, resource consumption, SSRF, inventory and unsafe API consumption |
| NIST CSF 2.0 | Govern, Identify, Protect, Detect, Respond and Recover outcomes |
| NIST SP 800-53 Rev. 5 | Access control, identification/authentication, audit, communications protection, configuration and incident response |
| NIST SSDF SP 800-218 | Secure development and supply-chain controls for service components |
| ISO/IEC 27001:2022 | Access, supplier, cloud, logging, monitoring, cryptography, secure development and incident management |
| CSA Cloud Controls Matrix | Cloud service and shared-responsibility controls |

### 20.6 ISO/IEC 27001:2022 relevance

| Annex A control | Distributed systems relevance |
|---|---|
| 5.15–5.18 | Access control, identity and authentication information |
| 5.19–5.23 | Supplier, cloud and ICT supply-chain security |
| 5.24–5.28 | Incident management and evidence |
| 5.29–5.30 | Security during disruption and ICT readiness |
| 5.31 | Legal, statutory, regulatory and contractual requirements |
| 5.34 | Privacy and protection of PII |
| 8.8 | Technical vulnerability management |
| 8.9 | Configuration management |
| 8.13 | Information backup |
| 8.15–8.16 | Logging and monitoring |
| 8.20–8.22 | Network security, network services and segregation |
| 8.24 | Cryptography |
| 8.25–8.29 | Secure development, architecture, coding and testing |
| 8.31–8.33 | Environment separation, change management and test information |

This is a relevance map only, not an ISO compliance or certification claim.

## 21. Regulatory and jurisdiction considerations

Applicability depends on legal entity, sector, data subjects, processing, service role, transfer, contractual obligations and regulator scope. Distributed architecture creates additional questions because data and identity context may cross service, provider and national boundaries.

### 21.1 India

Assess the Digital Personal Data Protection Act, 2023 and DPDP Rules, 2025 where applicable, including phased commencement and current amendments. Review processor/subprocessor relationships, breach handling, data minimization, purpose, retention, deletion propagation, telemetry and cross-border service dependencies. CERT-In directions and sector-specific RBI, SEBI, IRDAI, telecom or other requirements may apply depending on the entity and service. Verify current applicability and deadlines with qualified counsel.

### 21.2 Qatar

Assess Qatar Personal Data Privacy Protection Law No. 13 of 2016, National Information Assurance Standard where applicable, sector-specific requirements and contractual obligations. Identify partner processing, cross-border message flows, logging, data retention and incident notification requirements. Do not assume NIA applies to every private system.

### 21.3 Saudi Arabia

Assess Saudi PDPL and implementing/transfer regulations, NCA Essential Cybersecurity Controls and Cloud Cybersecurity Controls where entity and service scope applies. Confirm current editions, data-transfer requirements, processor roles and sector overlays before setting technical or reporting deadlines.

### 21.4 UAE

Determine whether federal UAE personal data law, DIFC, ADGM, healthcare, financial, government or sector-specific regimes apply. Review integration processors, partner locations, event payloads, trace exports, support access and retention.

### 21.5 EU/EEA and UK

Assess GDPR/UK GDPR, NIS2, DORA and other sector/product obligations where applicable. Distributed services and SaaS integrations require processor mapping, subprocessor visibility, transfer controls, incident coordination, resilience and evidence of access restriction.

### 21.6 Cross-border integration checklist

For each cross-border message or service call record sender and recipient legal entities, controller/processor and independent-controller roles, data categories and purposes, primary processing and telemetry locations, subprocessors and onward transfers, encryption and key control, retention/DLQ/backup/deletion behavior, government access and contractual safeguards, incident notification responsibilities, and exit/export/partner termination process.

## 22. Industry use cases

### 22.1 Banking and payments

Threats: forged payment event, duplicate payment, replayed callback, compromised partner key, out-of-order settlement, broker privilege abuse and inconsistent transaction state.

Controls:
- Strong producer identity and topic authorization.
- Signed or authenticated payment instructions.
- Stable idempotency keys.
- Payment provider reconciliation.
- Segregation of duties and approval workflow.
- Immutable audit of authorization and processing.
- DLQ and replay restrictions.
- Strict data minimization in event payloads.

### 22.2 Healthcare integration

Threats: patient data in messages/traces, wrong-patient routing, broad consumer access, stale integration credentials and untracked partner processing.

Controls:
- Patient and tenant context verified from trusted identity and domain records.
- Minimum necessary payloads.
- Encryption and scoped access.
- Audited access to sensitive events.
- Partner and processor inventory.
- Retention/deletion across queues, DLQs, logs and backups.
- Incident coordination with processors.

### 22.3 SaaS multi-tenant platform

Threats: tenant ID spoofing, cross-tenant event consumption, shared broker access and background job confusion.

Controls:
- Tenant context established server-side.
- Per-tenant authorization in service and consumer.
- Topic/queue segregation where risk warrants.
- Per-tenant quotas and rate limits.
- Cross-tenant negative tests.
- Tenant-safe tracing and support tooling.

### 22.4 Retail and logistics

Threats: duplicate order/stock events, stale inventory updates, callback SSRF, forged delivery status and queue overload.

Controls:
- Aggregate sequence numbers.
- Idempotent inventory operations.
- Signed partner callbacks.
- State machine validation.
- Delivery event provenance.
- Bounded retries and reconciliation.

### 22.5 Industrial and OT integration

Threats: compromised cloud service or broker publishes unsafe command toward an OT gateway, forged telemetry event, unauthorized remote action or loss of audit.

Controls:
- Separate telemetry events from control commands.
- No direct broker-to-PLC/SCADA access by default.
- Use an industrial DMZ and approved gateway.
- Authenticate and authorize each command with target, operation and safety context.
- Apply operator approval and safety interlocks where required.
- Segment cloud, enterprise IT and OT trust zones.
- Record command provenance and outcome.
- Validate safe failure behavior with OT operations and safety owners.

### 22.6 Government and critical services

Threats: unauthorized partner access, sensitive data propagation, service dependency outage, weak audit and ungoverned cross-domain federation.

Controls:
- Explicit trust domain and approved federation.
- Contracted service and data boundaries.
- Strong identity and key lifecycle.
- Protected audit and resilience.
- Partner access review and termination.
- Tested recovery and alternate processing.

## 23. Metrics and control effectiveness

| Metric | Definition | Use |
|---|---|---|
| Service identity coverage | Production services with unique verified workload identity / total services | Workload trust |
| mTLS enforcement coverage | Required service paths enforcing validated mTLS / total required paths | Transport assurance |
| Service authorization coverage | Sensitive operations with explicit service-level authorization / total identified sensitive operations | Authorization |
| Broker least-privilege coverage | Principals with reviewed scoped ACLs / total broker principals | Broker governance |
| Event schema validation coverage | Consumer entry points validating schema and bounds / total consumers | Message safety |
| Idempotency coverage | Side-effecting consumers with durable duplicate protection / total side-effecting consumers | Duplicate safety |
| Replay rejection rate | Detected replay attempts rejected / detected replay attempts | Replay defense |
| DLQ exposure review | DLQs with owner, ACL, retention and data classification / total DLQs | Data protection |
| Webhook verification coverage | Inbound webhook endpoints with signature/authentication and replay controls / total endpoints | Integration assurance |
| Retry amplification ratio | Downstream attempts per original request/event | Resilience |
| Trace redaction coverage | Instrumented services with approved telemetry policy / total instrumented services | Privacy |
| Integration access review | Integrations reviewed within policy interval / total active integrations | Third-party governance |
| Certificate rotation compliance | Workload certificates rotated within policy / total due certificates | Key lifecycle |
| Workflow reconciliation rate | Unresolved distributed transaction mismatches / total transactions | Business integrity |

Every metric needs scope, source, owner, frequency, target and excluded population. Broker throughput or low error rate alone does not prove secure processing.

## 24. Maturity model

| Level | Characteristics |
|---|---|
| 1 — Ad hoc | Service calls and events use inconsistent identity, authorization and logging; retries and replay are poorly understood |
| 2 — Repeatable | Service inventory, TLS, broker authentication, basic ACLs, schema validation and correlation IDs exist |
| 3 — Defined | Workload identity, service authorization, topic ACLs, idempotency, webhook verification, DLQ governance and standard contracts are implemented |
| 4 — Measured | Continuous identity/ACL review, replay tests, resilience tests, telemetry privacy and workflow reconciliation are measured |
| 5 — Adaptive | Automated trust lifecycle, policy enforcement, anomaly-driven quarantine and continuous workflow assurance operate with governed human override |

Tool deployment does not establish maturity. Require evidence of correct enforcement, operational ownership and recovery.

## 25. Implementation roadmap

### 0–30 days: discover and contain
- Inventory services, integrations, brokers, topics, queues and external callbacks.
- Identify shared credentials, unauthenticated paths and wildcard ACLs.
- Identify sensitive payloads in logs, traces and DLQs.
- Map critical business workflows and side effects.
- Identify replay, duplicate and retry assumptions.
- Assign owners and exceptions.

### 30–90 days: establish trust and integrity
- Deploy workload identity and mTLS for required service paths.
- Implement service-level authorization.
- Scope broker producer/consumer/admin permissions.
- Validate message schemas and event contracts.
- Implement idempotency for side-effecting consumers.
- Verify webhook signatures and replay controls.
- Protect DLQs, traces and integration secrets.

### 90–180 days: operationalize resilience and assurance
- Implement outbox/inbox and saga patterns where required.
- Establish bounded retries, deadlines, circuit breakers and bulkheads.
- Automate certificate and credential lifecycle.
- Add detection for identity, broker, replay and workflow anomalies.
- Test cross-tenant and cross-partner boundaries.
- Reconcile distributed workflows and test recovery.
- Map controls to exact standards and jurisdiction requirements.

## 26. Evidence and professional deliverables

A distributed systems security assessment pack should include scope, authorization and rules of engagement; service and integration inventory; architecture, trust-boundary and sequence diagrams; workload identity and certificate inventory; token exchange and identity propagation matrix; service authorization matrix; service mesh and proxy bypass review; broker, topic, queue, consumer group and ACL inventory; event catalogue and schema compatibility register; message integrity, replay and idempotency design; outbox/inbox and saga state model; webhook/callback security review; third-party and cross-border data flow register; retry, timeout, circuit breaker and resource policy; telemetry privacy and retention assessment; detection coverage and incident playbooks; findings, remediation, exception and retest records.

## 27. Limitations and assumptions

- Broker and mesh capabilities vary by product, release, plugin, hosting model and configuration.
- mTLS authenticates a workload at a transport boundary; it does not authorize all business operations.
- Message signatures provide integrity/authenticity only when key ownership and verification are correct; replay still requires separate controls.
- At-least-once delivery can create duplicates; consumers must be designed accordingly.
- "Exactly once" broker features do not automatically guarantee exactly-once external business effects across databases and third-party APIs.
- A DLQ is not automatically safe storage; it may contain highly sensitive data.
- Trace context is correlation metadata, not identity or authorization.
- Service mesh policy can be bypassed if alternate paths are not controlled.
- A compensation is not necessarily a rollback; business reconciliation may be required.
- Regulatory applicability depends on entity, sector, data, processing, jurisdiction and contract.
- This chapter is an engineering baseline, not a protocol certification, legal opinion or compliance attestation.

## 28. Related chapters

- [02. Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [03. Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [06. API and Service Security](../06-api-service-security/API-AND-SERVICE-SECURITY-ENGINEERING.md)
- [06. API and Service Security Lab Pack](../06-api-service-security/API-AND-SERVICE-SECURITY-LAB-PACK.md)
- [07. Identity and Access Security](../07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY.md)
- [08. Data Security and Privacy Engineering](../08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-ENGINEERING.md)
- [10. Cloud-Native Application Security](../10-cloud-native-application-security/CLOUD-NATIVE-APPLICATION-SECURITY-ENGINEERING.md)
- [10. Cloud-Native Application Security Lab Pack](../10-cloud-native-application-security/CLOUD-NATIVE-APPLICATION-SECURITY-LAB-PACK.md)

## 29. Authoritative references

1. NIST SP 800-204, Security Strategies for Microservices-Based Application Systems: https://csrc.nist.gov/pubs/sp/800/204/final
2. NIST SP 800-204A, Building Secure Microservices-Based Applications Using Service-Mesh Architecture: https://csrc.nist.gov/pubs/sp/800/204/a/final
3. NIST SP 800-204B, Attribute-Based Access Control for Microservices-Based Applications Using a Service Mesh: https://csrc.nist.gov/pubs/sp/800/204/b/final
4. NIST SP 800-204C, Implementation of DevSecOps for a Microservices-Based Application with Service Mesh: https://csrc.nist.gov/pubs/sp/800/204/c/final
5. NIST SP 800-204D, Strategies for the Integration of Software Supply Chain Security in DevSecOps CI/CD Pipelines: https://csrc.nist.gov/pubs/sp/800/204/d/final
6. OWASP Microservices Security Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Microservices_Security_Cheat_Sheet.html
7. RFC 8693, OAuth 2.0 Token Exchange: https://www.rfc-editor.org/rfc/rfc8693.html
8. RFC 8705, OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens: https://www.rfc-editor.org/rfc/rfc8705.html
9. RFC 9421, HTTP Message Signatures: https://www.rfc-editor.org/rfc/rfc9421.html
10. RFC 9530, Digest Fields: https://www.rfc-editor.org/rfc/rfc9530.html
11. RFC 9700, OAuth 2.0 Security Best Current Practice: https://www.rfc-editor.org/rfc/rfc9700.html
12. AsyncAPI 3.0.0 Specification: https://www.asyncapi.com/docs/reference/specification/v3.0.0
13. CloudEvents Specification: https://github.com/cloudevents/spec
14. SPIFFE Standards: https://github.com/spiffe/spiffe/tree/main/standards
15. SPIFFE Concepts: https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/
16. gRPC Authentication Guide: https://grpc.io/docs/guides/auth/
17. Apache Kafka Security: https://kafka.apache.org/documentation/#security
18. RabbitMQ Access Control: https://www.rabbitmq.com/docs/access-control
19. W3C Trace Context: https://www.w3.org/TR/trace-context/
20. OpenTelemetry Sensitive Data Handling: https://opentelemetry.io/docs/security/handling-sensitive-data/

## 30. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial distributed systems and integration security engineering playbook |
