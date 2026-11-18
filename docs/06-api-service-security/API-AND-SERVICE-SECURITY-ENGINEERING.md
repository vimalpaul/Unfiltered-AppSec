# API and Service Security Engineering Playbook

| Field | Value |
|---|---|
| Document ID | UAPPSEC-06-001 |
| Status | Draft engineering baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | REST/HTTP APIs, GraphQL, gRPC, webhooks, service-to-service interfaces and API management |
| Classification | Public |

## 1. Executive summary

APIs expose application capabilities, business workflows, identities, data and integration boundaries. Their security is not achieved by putting an API gateway in front of them, validating a JWT, or publishing an OpenAPI document. The service must enforce the correct subject, action, object, property, tenant, workflow state and business constraint at the point where the operation is performed.

The central API security principle is:

**Authenticate the caller, authorize the exact operation on the exact resource and properties, validate the business state, constrain resource consumption, and record an auditable outcome.**

API security spans:
- API discovery, ownership, inventory and lifecycle.
- Protocol and interface contract security.
- Authentication, token validation and workload identity.
- Function-, object-, property- and relationship-level authorization.
- Input schema validation, output minimization and serialization.
- Business-flow integrity, idempotency and concurrency.
- Resource consumption, quotas and abuse prevention.
- Server-side requests, webhooks and unsafe downstream consumption.
- API gateway, service mesh and network trust boundaries.
- Logging, detection, incident response and deprecation.
- Contract testing, security testing, evidence and remediation.

A gateway can enforce shared controls, but it cannot reliably replace domain-level authorization. A valid access token proves an authentication/authorization context issued by a trusted authority; it does not automatically prove the caller may read or mutate every object named in a request.

## 2. Purpose, audience and applicability

### 2.1 Purpose

Provide a practitioner playbook to design, implement, test and operate secure APIs and service integrations. It is intended for application security engineers, API developers, platform engineers, security architects, penetration testers, product security teams, SOC teams, technology owners and auditors.

### 2.2 Scope

In scope:
- REST and HTTP resource APIs.
- GraphQL APIs and resolver execution.
- gRPC and Protocol Buffers.
- Webhooks, callbacks and event delivery.
- Internal and external service-to-service APIs.
- API gateways, reverse proxies and service meshes.
- API authentication and authorization integration.
- API discovery, versioning, schema and contract management.
- Business logic, multi-tenancy and resource-consumption controls.
- API testing, monitoring and incident response.

Related chapters:
- Chapter 05 covers browser and web application security, including browser-origin behavior and web front-end interactions.
- Chapter 07 owns identity lifecycle, authentication architecture, federation, token and session engineering in depth.
- Chapter 02 owns architecture, trust boundaries and threat modeling.
- Chapter 04 owns language-specific secure coding and code-review patterns.
- Chapter 08 owns data security and privacy engineering.
- Chapter 11 will cover broader distributed systems and event integration architecture.
This chapter defines API-specific enforcement and assessment requirements, and links to those foundations.

### 2.3 Terms

- **API consumer:** user, application, partner, workload or service that calls an API.
- **API provider:** service that exposes an API operation.
- **Resource:** business object represented or manipulated by an API.
- **Subject:** authenticated principal or workload acting on a request.
- **Operation:** action performed on a resource, such as read, update, approve or delete.
- **Property:** individual field or attribute within a resource.
- **Tenant:** logical customer, organization or isolation domain.
- **Contract:** machine-readable or human-readable description of operations, schemas, errors and security behavior.
- **Gateway:** intermediary that routes and may apply shared policies to API traffic.
- **Service identity:** identity assigned to a workload or service rather than a human user.

### 2.4 Assumptions and limitations

- The operator has authority to assess the API and its dependencies.
- API examples use synthetic identities and data.
- The API protocol, gateway, runtime and deployment versions must be recorded during real assessments.
- Standards mappings are not legal opinions or evidence of compliance.
- A control is not considered implemented merely because it appears in an API specification or gateway policy.

## 3. API architecture and trust boundaries

### 3.1 Reference architecture

~~~mermaid
flowchart LR
    C[Browser / Mobile / Partner / Workload] --> EDGE[DNS / CDN / DDoS / WAF]
    EDGE --> GW[API Gateway / Ingress]
    GW --> AUTH[Identity Provider / Token Introspection]
    GW --> SVC[API Service]
    SVC --> POLICY[Domain Authorization / Policy]
    SVC --> DB[(Database)]
    SVC --> CACHE[(Cache)]
    SVC --> OBJ[(Object Storage)]
    SVC --> MQ[Queue / Event Bus]
    SVC --> OUT[External API / Partner]
    SVC --> LOG[Audit / Security Telemetry]
    GW --> LOG
    AUTH --> LOG
    MQ --> WORKER[Background Worker]
    WORKER --> DB
    WORKER --> OUT
~~~

The architecture is logical. A gateway may be absent, multiple gateways may exist, and services may communicate through direct calls or events. Document the actual topology, not the desired diagram.

### 3.2 Trust boundaries

Explicitly model:
- Public internet to API edge.
- Edge to gateway/ingress.
- Gateway to service runtime.
- Service to identity provider or introspection endpoint.
- Service to database, cache and object storage.
- Service to another internal service.
- Service to third-party API.
- Webhook sender to webhook receiver.
- Event broker to consumer.
- Human user to workload identity.
- Tenant A to tenant B.
- Partner environment to enterprise environment.
- CI/CD deployment identity to API runtime.
- API provider to API consumer's interpretation of response data.

### 3.3 Request execution model

For every operation, define:
1. Protocol and transport acceptance.
2. Host, authority, route and method validation.
3. Request size, content type and parser constraints.
4. Authentication and token validation.
5. Scope, audience and client/workload validation.
6. Function-level authorization.
7. Tenant and relationship resolution from trusted context.
8. Object-level authorization.
9. Property-level read/write authorization.
10. Schema, type, range and business validation.
11. State transition, idempotency and concurrency enforcement.
12. Data access using constrained queries.
13. Downstream request authorization and destination validation.
14. Response minimization and serialization.
15. Audit and security telemetry.
16. Error handling and correlation.

Checks must be enforced at the provider and domain layer. A consumer's hidden UI field, route guard or supplied tenant ID is not a trusted authorization decision.

## 4. API inventory, ownership and attack surface

### 4.1 Inventory requirements

Maintain an authoritative inventory of:
- API name, stable ID, owner and business purpose.
- Provider team and support contact.
- Environment and deployment location.
- Public, partner, internal or restricted exposure.
- Base URL, hostnames, routes and methods.
- Protocol, version and content types.
- OpenAPI/GraphQL schema/Proto contract location and revision.
- Authentication mechanism, issuer, audience and client identities.
- Authorization model and tenant boundary.
- Data classifications and sensitive properties.
- Rate limits, quotas and expensive operations.
- Dependencies, external destinations and downstream APIs.
- Gateway, WAF, service mesh and network policies.
- Logging, tracing, audit and alert coverage.
- Lifecycle status, deprecation date and retirement owner.
- Test coverage, findings, exceptions and evidence.

### 4.2 Discovery sources

Correlate:
- API gateway and ingress route configuration.
- OpenAPI documents and generated clients.
- GraphQL schemas and persisted-operation registries.
- Proto files and gRPC reflection/configuration.
- Source code route/controller mappings.
- DNS, certificates and cloud load balancers.
- Service mesh and service catalog.
- CI/CD deployment manifests.
- Mobile and web client network traces within authorized scope.
- Partner integration registers and webhook subscriptions.
- Observed traffic and access logs.
- Developer portals and API management platforms.

Do not assume an API is absent because it is not in the developer portal. Shadow, zombie, debug, legacy and alternate-version APIs must be identified.

### 4.3 API inventory schema

| Field | Description |
|---|---|
| API ID | Stable unique identifier |
| Name / owner | Product name and accountable owner |
| Endpoint | Base URL and route |
| Environment | Dev/test/stage/prod |
| Exposure | Public/partner/internal/restricted |
| Protocol | REST, GraphQL, gRPC, webhook, other |
| Version | Contract and deployment version |
| Authentication | Issuer, client type, token/session |
| Authorization | Function, object, property, tenant policy |
| Data | Classification and sensitive fields |
| Dependencies | Downstream services and data stores |
| Limits | Rate, concurrency, payload, query cost |
| Contract | Schema path and hash/revision |
| Monitoring | Trace, audit and alert status |
| Lifecycle | Active, deprecated, retired |
| Assurance | Last assessment, findings, exception |

## 5. API threat model

### 5.1 Threat questions

- Who can call this API and from which trust zone?
- Is the caller a human, browser, mobile app, partner or workload?
- How is the caller authenticated and what is the token audience?
- Can the caller choose object IDs, tenant IDs, role IDs or owner IDs?
- Does the operation read or change sensitive properties?
- Are authorization rules enforced per function, object and property?
- Can one call trigger many downstream operations?
- Can the caller create expensive queries, exports or background jobs?
- Can the API fetch a URL or call an arbitrary external destination?
- Does the provider trust data or headers from a gateway without validating provenance?
- Can requests be replayed or submitted concurrently?
- Are callbacks and webhooks authenticated and replay-protected?
- Are old versions and undocumented routes still deployed?
- Can errors expose schema, identifiers, tokens or internal topology?
- What evidence proves the control worked?

### 5.2 API abuse-case model

For every operation, document:
- Subject and client identity.
- Required function/permission.
- Resource and tenant.
- Allowed properties and state transitions.
- Preconditions, postconditions and invariants.
- Data sensitivity and business impact.
- Expected denial behavior.
- Rate, concurrency and size limits.
- Downstream side effects.
- Audit event and correlation fields.
- Positive, negative and abuse-case tests.

## 6. OWASP API Security Top 10:2023 risk model

The 2023 list is used as a risk taxonomy, not a complete API security standard or test plan.

| ID | Risk | Engineering focus |
|---|---|---|
| API1:2023 | Broken Object Level Authorization (BOLA) | Authorize each requested object in caller/tenant context |
| API2:2023 | Broken Authentication | Correct identity proof, token validation, credential lifecycle and abuse controls |
| API3:2023 | Broken Object Property Level Authorization (BOPLA) | Control readable and writable fields; prevent excessive data exposure and mass assignment |
| API4:2023 | Unrestricted Resource Consumption | Bound request, compute, storage, concurrency and downstream cost |
| API5:2023 | Broken Function Level Authorization (BFLA) | Enforce permission for administrative and privileged operations |
| API6:2023 | Unrestricted Access to Sensitive Business Flows | Protect high-value workflows from automation, replay and abuse |
| API7:2023 | Server Side Request Forgery | Constrain server-originated network requests and destinations |
| API8:2023 | Security Misconfiguration | Harden gateways, services, CORS, TLS, errors, debug and deployment |
| API9:2023 | Improper Inventory Management | Discover, own, version, deprecate and retire every API |
| API10:2023 | Unsafe Consumption of APIs | Validate and constrain responses from upstream/third-party APIs |

Do not force every defect into one category. A single attack path may involve several risks, such as BOLA plus mass assignment plus unrestricted business flow.

## 7. Authorization engineering: function, object, property and relationship

### 7.1 Function-level authorization (BFLA)

Function authorization answers: may this subject invoke this capability?

Examples:
- Learner cannot publish a course.
- Customer cannot approve their own refund.
- Read-only analyst cannot change security policy.
- Partner client cannot invoke internal administration operations.
- Service account cannot perform human-only approval.

Controls:
- Define permissions by business action, not merely URL.
- Enforce at controller and domain/service boundary.
- Deny by default.
- Protect alternate methods, routes, versions and batch operations.
- Separate administration plane from normal customer operations.
- Require approval/step-up for high-impact actions where appropriate.
- Test each role/client against every sensitive operation.

### 7.2 Object-level authorization (BOLA)

Object authorization answers: may this subject act on this particular object?

For each operation using an identifier:
1. Resolve the subject from verified identity context.
2. Resolve tenant and ownership from trusted server-side data.
3. Load the target object through an authorization-aware query or policy check.
4. Verify relationship, ownership, delegated access and object state.
5. Enforce action-specific permission.
6. Apply the decision to read, update, delete, export and nested access paths.
7. Avoid returning existence details when policy requires non-disclosure.
8. Record material allow/deny outcomes.

Never trust a client-supplied ownerId, tenantId or organizationId as proof of relationship.

### 7.3 Property-level authorization (BOPLA)

Property authorization answers: which fields may this subject read or change?

Sensitive fields include:
- role, permissions and account status;
- tenantId, ownerId and organizationId;
- price, discount, balance, credit and billing state;
- approval status and risk score;
- MFA state and recovery attributes;
- internal notes, security flags and audit metadata;
- personal identifiers and restricted profile fields.

Controls:
- Use explicit request DTOs and response projections.
- Define readable and writable property sets per role and operation.
- Avoid binding arbitrary JSON to persistence entities.
- Compute privileged fields server-side.
- Filter nested objects and GraphQL fields using the same domain policy.
- Test property omission, null, unexpected field and alternate casing.
- Do not assume a field is safe because it is absent from the UI.

### 7.4 Relationship-based authorization

Some systems require graph relationships such as owner, manager, project member, delegated administrator, parent account, guardian or resource collaborator.

Model relationship types and traversal rules explicitly. Prevent users from manufacturing relationships through request fields. Bound relationship depth and query cost. Test revocation, transitive membership, inheritance, cycles and cross-tenant edges.

### 7.5 Authorization decision model

~~~mermaid
flowchart TD
    R[Incoming API request] --> AUTHN{Identity verified?}
    AUTHN -- No --> DENY[Reject]
    AUTHN -- Yes --> FUNC{Function allowed?}
    FUNC -- No --> DENY
    FUNC -- Yes --> TENANT{Trusted tenant context?}
    TENANT -- No --> DENY
    TENANT -- Yes --> OBJ{Object relationship allowed?}
    OBJ -- No --> DENY
    OBJ -- Yes --> PROP{Requested properties allowed?}
    PROP -- No --> DENY
    PROP -- Yes --> STATE{Business state permits action?}
    STATE -- No --> DENY
    STATE -- Yes --> EXEC[Execute constrained operation]
    EXEC --> AUDIT[Record outcome]
~~~

This is a logical policy sequence. Implementations may combine decisions, but must preserve all enforcement semantics.

## 8. Authentication, OAuth and token handling

### 8.1 Authentication versus authorization

Authentication establishes a principal or workload identity. Authorization decides whether that identity may perform an operation on a resource and properties. A token's existence or cryptographic validity does not imply every API permission.

### 8.2 OAuth 2.0 security baseline

Use RFC 9700, OAuth 2.0 Security Best Current Practice (January 2025), as the protocol security baseline where OAuth is used.

Engineering requirements:
- Use Authorization Code with PKCE for interactive public clients.
- Match redirect URIs exactly using registered values.
- Do not use the Implicit grant or Resource Owner Password Credentials grant.
- Validate issuer, audience, signature, expiry, not-before, authorized party/client and intended token type as applicable.
- Separate access tokens from ID tokens; do not accept an ID token as an API access token.
- Enforce least-privilege scopes and resource-specific audiences.
- Protect authorization responses against mix-up and code injection.
- Use secure client authentication for confidential clients.
- Protect refresh tokens with rotation/reuse detection or sender constraint as appropriate.
- Consider PAR and signed request objects for high-assurance deployments.
- Consider sender-constrained tokens such as DPoP or mutual TLS where threat model and ecosystem support justify them.
- Define revocation, key rotation, issuer migration and emergency response.
- Do not log bearer tokens or place them in URLs.

OAuth is an authorization framework; OpenID Connect adds an identity layer. Use the correct protocol profile for the purpose.

### 8.3 JWT validation

If access tokens are JWTs:
1. Select trusted issuer and key-discovery location through configuration, not token-controlled arbitrary URLs.
2. Verify signature using an explicit algorithm allow-list.
3. Reject unsigned tokens and algorithm confusion.
4. Validate issuer and audience.
5. Validate exp, nbf and iat policy with bounded clock skew.
6. Validate token type/profile and required claims.
7. Validate client/authorized-party context where required.
8. Enforce scopes/permissions at the operation.
9. Reject malformed, oversized and duplicate/ambiguous claim representations according to parser policy.
10. Plan signing-key rotation and cache refresh.
11. Define revocation and compromise response; short token lifetime alone is not a complete revocation strategy.

Do not accept a token merely because a library can decode it. Decoding is not signature validation.

### 8.4 API keys

API keys are identifiers/secrets for a client integration, not proof of a human identity. If used:
- Generate high-entropy secrets.
- Store only protected representations where feasible.
- Scope each key to specific APIs, tenants and actions.
- Assign owner, purpose and expiry/rotation policy.
- Support immediate revocation.
- Never embed privileged long-lived keys in browser/mobile distributable code.
- Rate-limit and monitor each key.
- Prevent keys in URLs, logs, source control and analytics.
- Prefer workload identity or OAuth client credentials where practical.

### 8.5 Mutual TLS and workload identity

Use mutual TLS for service identity where the infrastructure can reliably issue, rotate and validate workload certificates. Validate the peer certificate chain, identity mapping, expiry, SAN and intended workload. Do not equate network reachability or a certificate from a broad shared CA with authorization to every service. Map workload identity to narrow service permissions and enforce authorization at the destination.

### 8.6 Token propagation and delegation

When service A calls service B on behalf of a user:
- Decide whether to propagate the user token, exchange it for a narrower token, or use a distinct workload identity plus signed delegation context.
- Preserve original actor and calling service in auditable context.
- Limit audience and scopes to the downstream operation.
- Avoid forwarding tokens to unrelated hosts or third parties.
- Prevent confused-deputy behavior where a privileged service uses its own authority to perform arbitrary user-selected actions.
- Define delegation expiry, revocation and consent/approval semantics.

## 9. REST API design and security

### 9.1 Resource and operation design

Use resource-oriented paths and appropriate HTTP semantics. Define methods, status codes, content types, idempotency and error schemas consistently. Avoid exposing internal database table names or raw ORM entities as API contracts.

### 9.2 Method and status behavior

- GET should not change state.
- PUT should represent replacement semantics as defined by the contract.
- PATCH must define permitted patch operations and property authorization.
- POST may create resources or execute commands; document idempotency behavior.
- DELETE must enforce object authorization and retention/deletion policy.
- OPTIONS should be deliberately configured for preflight and capability discovery.
- HEAD should not leak sensitive metadata.
- Reject unsupported methods and content types.
- Ensure method override mechanisms cannot bypass authorization.

### 9.3 PATCH and mass assignment

Patch formats can create property-level risk. Define exactly which paths and operations are allowed. Prevent writes to tenant, owner, role, price, balance, approval, security and audit properties unless a dedicated privileged workflow authorizes them. Avoid generic JSON merge/patch application to persistence objects without path authorization and invariant validation.

### 9.4 Pagination and filtering

- Require bounded page size and maximum offset/depth.
- Prefer cursor pagination for large or changing datasets.
- Bind cursors to tenant, filter and sort context where necessary.
- Validate sort fields against an allow-list.
- Apply authorization before counting or aggregating restricted objects.
- Prevent filters from exposing hidden fields or other tenants' records.
- Rate-limit expensive reports and exports.
- Ensure pagination does not create inconsistent security snapshots.

### 9.5 Bulk and batch operations

A single request may process many objects. Apply authorization to each object and each action, not only the batch envelope. Define maximum batch size, atomicity semantics, partial failure behavior, duplicate handling and idempotency. Prevent a batch endpoint from becoming a way to evade per-request quotas or enumerate object IDs.

### 9.6 Error model

Return stable, documented error codes with minimal detail. Do not expose stack traces, SQL, secrets, internal service addresses or authorization policy internals. Include correlation ID and safe diagnostic category. Ensure errors do not disclose object existence when the access policy requires concealment.

## 10. GraphQL security

### 10.1 GraphQL attack surface

GraphQL commonly exposes one endpoint with many schema fields, nested relationships, mutations, aliases, fragments, subscriptions and resolver paths. Route-level authorization alone is insufficient. Authorization must be enforced in the domain layer and at the relevant object/property boundary.

### 10.2 Schema and resolver controls

- Treat schema fields as API operations and inventory them.
- Apply authentication and authorization to queries, mutations and subscriptions.
- Enforce object and property policy in resolvers or shared domain services.
- Prevent introspection from being treated as the primary security boundary; schema secrecy is not authorization.
- Restrict dangerous scalar coercion and custom scalar parsing.
- Validate input types and business invariants.
- Avoid exposing internal fields through nested relationships.
- Ensure resolver errors do not leak stack traces or sensitive data.
- Review federation, entity resolution and remote schema trust.

### 10.3 Demand control

Apply:
- Maximum query depth.
- Maximum list nesting.
- Field/alias breadth limits.
- Operation and batch count limits.
- Pagination and result-size limits.
- Query complexity/cost analysis.
- Per-subject and per-tenant budgets.
- Resolver timeouts and downstream concurrency limits.
- Trusted/persisted documents where the use case permits.
- Subscription connection and event rate limits.

Depth alone is not sufficient: a shallow query with hundreds of aliases or expensive fields may still exhaust resources. Request count alone is not sufficient: one GraphQL operation can trigger many resolver/database calls.

### 10.4 GraphQL testing

Test field authorization, nested object ownership, alias amplification, batch behavior, expensive resolver paths, pagination, introspection policy, error leakage, subscription authorization and revocation. Test the same data through REST and GraphQL if both interfaces expose it; a secure REST path does not guarantee a secure resolver.

## 11. gRPC and Protocol Buffers security

### 11.1 gRPC surface

gRPC uses HTTP/2 transport and Protocol Buffers by default. Security review must include transport authentication, metadata, service/method authorization, message schema, streaming behavior, deadlines, reflection, interceptors and generated code.

### 11.2 Controls

- Use TLS; use mutual TLS where workload identity and deployment requirements justify it.
- Authenticate every call and bind peer identity to a trusted principal.
- Enforce service and method-level authorization in interceptors and domain logic.
- Apply object/property authorization within the method implementation.
- Validate message fields, enum values, lengths and nested message sizes.
- Set maximum receive/send message sizes.
- Set deadlines and cancellation propagation.
- Limit concurrent streams, connection counts and per-method resource cost.
- Restrict server reflection in production or protect it deliberately.
- Protect health and administrative services.
- Validate metadata and do not trust arbitrary forwarded identity headers.
- Handle streaming authorization and revocation during long-lived streams.
- Keep proto contracts backward compatible without accidentally expanding permissions.

### 11.3 Streaming

For client/server/bidirectional streaming:
- Authenticate at connection/call start.
- Authorize each message or state transition where permissions can vary.
- Bound message count, size, duration and idle time.
- Re-check authorization after role or tenant changes where required.
- Define partial processing, retries and cancellation semantics.
- Audit stream start, privileged actions and termination without logging sensitive payloads.

## 12. Webhooks and callback security

### 12.1 Threat model

Webhook receivers accept inbound requests from external systems; webhook senders make outbound calls to subscriber-controlled destinations. Risks include spoofing, replay, SSRF, event forgery, secret leakage, duplicate processing, event ordering, endpoint takeover and denial of service.

### 12.2 Sender controls

- Sign the exact payload bytes or a well-defined canonical representation.
- Include timestamp and unique delivery/event identifier in the signed material.
- Use HMAC or asymmetric signatures with a documented algorithm and key lifecycle.
- Support secret rotation with overlap windows.
- Send over HTTPS and validate certificates.
- Avoid including credentials in callback URLs.
- Retry with bounded exponential backoff and jitter.
- Use delivery IDs and documented retry semantics.
- Do not assume exactly-once delivery.
- Avoid exposing internal error details to subscribers.

### 12.3 Receiver controls

1. Read bounded raw request body.
2. Validate content type and size.
3. Reconstruct the exact signed input according to the contract.
4. Verify signature using constant-time comparison for MACs.
5. Validate timestamp within an agreed tolerance.
6. Reject replayed delivery IDs using durable idempotency storage.
7. Authenticate the sender and bind key to expected integration.
8. Validate event type, schema and tenant/resource context.
9. Process asynchronously after durable acceptance where appropriate.
10. Apply idempotent state transitions and audit the event.

Do not parse and reserialize JSON before verifying a signature unless the protocol explicitly signs a canonicalized representation.

### 12.4 Webhook destination registration

For systems that send webhooks to customer-provided URLs:
- Validate scheme and destination.
- Resolve and block prohibited address ranges.
- Revalidate DNS and every redirect hop.
- Use controlled egress and destination allow-lists where feasible.
- Prevent link-local, loopback, private and metadata destination access unless explicitly required by design.
- Apply timeout, response-size and redirect limits.
- Avoid returning fetched response content to the configuring user.
- Separate delivery workers from privileged application services.
- Provide a safe verification/challenge mechanism.

## 13. Unsafe consumption of upstream APIs

Third-party and internal API responses are untrusted input. Validate:
- TLS certificate and hostname.
- Expected endpoint and redirect behavior.
- Response content type and size.
- JSON/XML/Protobuf schema.
- Numeric ranges, enum values and required fields.
- Error and retry semantics.
- Pagination and result count.
- Embedded URLs and file references.
- Tenant/resource identity.
- Signatures or message integrity where the integration supports them.
- Rate and timeout behavior.

Do not assume an internal service is trustworthy because it is inside a private network. Defend against compromised upstreams, stale credentials, poisoned responses, unexpected content and schema drift.

## 14. API gateways, service mesh and network controls

### 14.1 Gateway responsibilities

A gateway may provide:
- TLS termination and upstream TLS policy.
- Route/method allow-listing.
- Token validation or introspection integration.
- Coarse scope/client checks.
- Request size and timeout limits.
- Rate limits and quotas.
- WAF and protocol anomaly detection.
- Header normalization.
- Request correlation and access logging.
- API version routing.
- Deprecation and sunset controls.

A gateway usually cannot determine domain object ownership or field-level policy without reliable domain context. Keep authoritative business authorization in the service/domain layer.

### 14.2 Trusting gateway identity headers

If the gateway injects identity headers:
- Strip client-supplied copies before injecting trusted values.
- Restrict service ingress to the gateway or use cryptographically authenticated upstream identity.
- Bind the header to a verified token/identity.
- Prevent direct-origin bypass.
- Document which headers are authoritative and which are informational.
- Test alternate routes, private load balancers and debug endpoints.

### 14.3 Service mesh

Service mesh mTLS provides workload-to-workload transport identity, not complete business authorization. Use service identity, namespace/workload policy, egress restrictions and destination policy. Avoid broad allow-all service identities. Ensure policy applies to bypass paths and non-mesh traffic.

## 15. API schema and contract security

### 15.1 OpenAPI

Use a maintained OpenAPI specification version and validate the document in CI. At the time of this baseline, the official OpenAPI Specification is 3.2.1, published 10 September 2026. Confirm the current version at review time.

Contract requirements:
- Every operation has an owner and purpose.
- Security requirements are explicit at global and operation level.
- Request and response schemas are defined.
- Sensitive fields are identified.
- Error responses are documented.
- Pagination, limits and idempotency are described.
- Deprecated operations are marked with a removal plan.
- External references are reviewed and pinned/controlled.
- Examples contain synthetic data only.
- Generated clients and servers are reviewed for unsafe defaults.

OpenAPI is a contract format, not proof that runtime enforcement matches the contract.

### 15.2 Contract drift

Compare deployed routes and schemas with approved contracts. Detect undocumented operations, changed security declarations, unexpected response fields, relaxed validation, missing limits and stale versions. Run compatibility checks in CI and deployment. Maintain exceptions for intentional deviations with owners and expiry.

### 15.3 Schema validation limits

Schema validation catches structural errors but does not prove authorization, workflow validity, business invariants, safe resource consumption or correct downstream behavior. Validate semantics at the domain layer.

## 16. Input validation, serialization and deserialization

- Use strict schemas and reject unexpected fields where practical.
- Set maximum body, nesting, array and string sizes.
- Reject ambiguous duplicate keys according to parser behavior.
- Define number precision and overflow behavior.
- Avoid unsafe polymorphic deserialization of untrusted types.
- Restrict XML external entities and external resource resolution.
- Avoid unsafe object deserialization formats.
- Use parameterized database access.
- Validate path, query, header and body sources independently.
- Canonicalize identifiers and enforce exact syntax.
- Ensure validation and execution use the same canonical value.
- Apply content-type enforcement and reject unexpected media types.

## 17. Data minimization and response security

- Return only fields required by the consumer and operation.
- Apply property-level authorization before serialization.
- Avoid generic entity serialization.
- Mask or omit sensitive personal, financial and security attributes.
- Avoid exposing internal IDs, topology or implementation detail unless needed.
- Protect exports and bulk responses with stronger authorization and audit.
- Use cache controls suitable for sensitivity.
- Ensure errors and debug metadata do not reveal hidden properties.
- Review nested relationships and aggregate endpoints.
- Treat GraphQL selection sets and REST projections as untrusted requests, not authorization policy.

## 18. Resource consumption and API abuse

### 18.1 Resource dimensions

Bound:
- Requests per second and burst.
- Concurrent requests and streams.
- Payload size and decompressed size.
- Batch item count.
- GraphQL depth, breadth, aliases and cost.
- Pagination size and maximum result set.
- Query execution time and database rows scanned.
- File size, export size and generated report size.
- Queue depth and background job count.
- Downstream calls and fan-out.
- Webhook retry volume.
- Memory, CPU, storage and connection pool use.

### 18.2 Layered limits

Use limits at edge, gateway, service, identity/client, tenant and operation level. A global IP rate limit is not enough for authenticated multi-tenant APIs. A per-IP control may also harm users behind NAT or be bypassed by distributed clients.

### 18.3 Sensitive business flow protection

Identify workflows with financial, operational or scarce-resource value:
- account creation and invitation;
- password recovery and MFA enrollment;
- coupon and promotion redemption;
- booking, reservation and inventory;
- payment, refund and transfer;
- assessment or certification completion;
- report/export generation;
- approval and privileged configuration;
- trial activation and quota consumption.

Apply business-specific velocity, uniqueness, idempotency, proof-of-intent, risk signals, approval, concurrency and anomaly detection. Do not rely only on generic HTTP rate limiting.

## 19. Idempotency, replay and concurrency

For non-idempotent operations, define an idempotency key or equivalent deduplication mechanism:
- Bind the key to authenticated subject, tenant, operation and request fingerprint.
- Store outcome durably for the defined replay window.
- Reject reuse with materially different request content.
- Handle concurrent requests atomically.
- Define retention and key expiry.
- Ensure retries return the prior outcome rather than duplicating side effects.
- Protect against key guessing and cross-tenant collisions.

For state-changing operations use database constraints, transactions, optimistic concurrency or locking as appropriate. Re-check authorization and business invariants at commit time. A preflight read is not proof that the state remains valid.

## 20. SSRF and outbound API requests

Any feature that accepts a URL or dynamically selects an upstream is an SSRF candidate. Use fixed destinations or strict allow-lists. Validate scheme, hostname and resolved IP. Revalidate redirects and DNS resolution. Block loopback, link-local, private, multicast, reserved and metadata destinations unless explicitly needed and isolated. Use egress proxies, network policy, timeouts and response limits. Never trust URL validation performed only in the client.

## 21. Caching and API data isolation

- Do not shared-cache private responses without a safe cache-key and authorization model.
- Include tenant/principal variation where required.
- Use private/no-store controls for sensitive data as appropriate.
- Ensure cache keys account for relevant host, path, query and headers.
- Prevent cache poisoning from unkeyed input.
- Invalidate cached data on access revocation and permission changes.
- Avoid caching authorization decisions beyond the approved freshness window.
- Test CDN, gateway, application and client caches separately.
- Do not assume internal APIs are exempt from cache isolation.

## 22. API versioning, deprecation and retirement

Maintain explicit versions and support windows. Do not leave obsolete endpoints active indefinitely. For every deprecation:
1. Identify consumers and owners.
2. Assess data and security differences.
3. Publish a migration plan and timeline.
4. Instrument version usage.
5. Notify consumers and provide test environment.
6. Apply sunset controls and deadline.
7. Confirm no critical consumer remains.
8. Remove route, credentials, secrets and deployment configuration.
9. Verify the old route is unreachable.
10. Retain required audit and contract evidence.

Versioning must not create an authorization bypass where old and new routes enforce different policies.

## 23. Logging, tracing and security monitoring

### 23.1 Event fields

Record relevant:
- API ID, route template and version.
- Request/correlation/trace ID.
- Authenticated subject and client/workload identity.
- Tenant context from trusted resolution.
- Operation and resource reference, appropriately pseudonymized.
- Authorization decision and policy version.
- Response status and error category.
- Rate/quota decision.
- Request size, response size and execution duration.
- Downstream service and outcome.
- Schema validation or signature failure.
- Webhook delivery ID and replay decision.
- Administrative changes and key lifecycle events.

Do not log bearer tokens, API secrets, private keys, passwords, full sensitive payloads or unnecessary personal data. Query strings may contain secrets and should be redacted.

### 23.2 Detection scenarios

| Detection ID | Scenario | Signals | Response |
|---|---|---|---|
| API-D-001 | BOLA enumeration | One subject accesses many sequential/unrelated object IDs | Investigate object authorization and account |
| API-D-002 | BFLA probing | Low-privilege client repeatedly invokes admin operations | Block, investigate role and route coverage |
| API-D-003 | BOPLA mass assignment | Unexpected privileged properties in write payloads | Reject and inspect affected records |
| API-D-004 | Token abuse | Invalid issuer/audience, signature failures, replay or unusual client usage | Revoke/rotate and investigate identity provider |
| API-D-005 | Resource exhaustion | Costly operations, high concurrency, deep queries or large batches | Throttle and inspect abusive principal |
| API-D-006 | Sensitive workflow automation | Abnormal velocity in refund, coupon, booking or assessment actions | Apply business controls and review impact |
| API-D-007 | SSRF attempt | Blocked destination, unusual DNS/redirect or egress denial | Contain fetcher and inspect feature |
| API-D-008 | API inventory drift | New route, schema or hostname without owner/approval | Block release or assign emergency review |
| API-D-009 | Unsafe upstream response | Schema mismatch, unexpected redirect or invalid certificate | Quarantine integration and investigate provider |
| API-D-010 | Webhook replay/spoofing | Invalid signature, stale timestamp or duplicate event ID | Reject, rotate secret if needed, investigate sender |
| API-D-011 | Cross-tenant access anomaly | Subject repeatedly references foreign tenant/resource | Investigate tenant context and policy |
| API-D-012 | Deprecated API usage | Calls to retired or sunset version | Notify owner and enforce retirement plan |
| API-D-013 | Gateway bypass | Requests reach service without expected gateway identity/path | Restrict ingress and investigate topology |
| API-D-014 | Service identity anomaly | Workload calls unexpected service or action | Restrict workload identity and inspect compromise |

Tune detections to normal usage and business schedules. An alert is a lead, not proof of compromise.

## 24. API security testing methodology

### 24.1 Authorization and scope

Before testing:
- Obtain written authorization and exact API host/route scope.
- Confirm test environment, tenants and synthetic accounts.
- Identify permitted roles and client identities.
- Define rate, concurrency, payload and time limits.
- Confirm whether GraphQL introspection, gRPC reflection, fuzzing, webhook replay and negative tests are permitted.
- Exclude real payment, email/SMS, external callback and destructive side effects unless explicitly approved.
- Define emergency contact and stop conditions.
- Use a test tenant and synthetic resources.
- Preserve sanitized evidence only.

### 24.2 Assessment phases

1. Inventory and ownership validation.
2. Contract/schema discovery.
3. Protocol and transport review.
4. Authentication and token validation review.
5. Function-level authorization.
6. Object-level authorization.
7. Property-level authorization.
8. Tenant and relationship isolation.
9. Input, serialization and injection review.
10. Business-flow and concurrency tests.
11. Resource consumption and abuse tests.
12. SSRF and outbound integration review.
13. Webhook signature/replay tests.
14. Gateway and service mesh review.
15. Logging, detection and incident readiness.
16. Remediation, regression and retest.

### 24.3 Test matrix design

Build a matrix across:
- Subject: anonymous, user, admin, partner, service identity.
- Tenant: own, shared, foreign, unassigned.
- Object: owned, shared, foreign, deleted, guessed, stale.
- Operation: read, create, update, delete, approve, export, bulk.
- Property: normal, privileged, immutable, sensitive, unknown.
- State: valid, invalid, expired, pending, approved, revoked.
- Transport: REST, GraphQL, gRPC, webhook.
- Execution: single, batch, replay, concurrent, retry.
- Environment: public edge, internal route, old version, direct origin.

A complete test does not merely change an ID once. It verifies the authorization policy across combinations that represent the real business model.

## 25. API security test catalogue

| Test ID | Area | Procedure focus | Expected result |
|---|---|---|---|
| API-T-001 | Inventory | Compare gateway, source routes, contracts and observed traffic | All exposed APIs have owner, version and lifecycle state |
| API-T-002 | Authentication | Missing, malformed, expired, wrong issuer/audience token | Rejected consistently |
| API-T-003 | JWT | Wrong algorithm, key, issuer, audience, type and time claims in isolated test | Token rejected |
| API-T-004 | Scope | Valid token lacking required operation scope | Operation denied |
| API-T-005 | BFLA | Invoke privileged function with lower-privilege identity | Denied at provider |
| API-T-006 | BOLA | Access another synthetic user's object | Denied without data leakage |
| API-T-007 | BOPLA read | Request sensitive properties not permitted to role | Fields omitted or access denied |
| API-T-008 | BOPLA write | Submit privileged/immutable fields in update body | Fields ignored/rejected; server state unchanged |
| API-T-009 | Tenant isolation | Change tenant/resource identifiers | Trusted tenant and relationship enforced |
| API-T-010 | Relationship | Test delegated, inherited, revoked and nested relationship access | Policy matches documented graph |
| API-T-011 | Mass assignment | Add unknown and privileged JSON properties | Strict DTO/schema prevents unintended mutation |
| API-T-012 | PATCH | Test forbidden paths and patch operation combinations | Only allowed property operations succeed |
| API-T-013 | Pagination | Excessive page size, offset, cursor tampering | Bounded and authorized results |
| API-T-014 | Filtering | Inject unknown fields/operators/sort expressions | Rejected or constrained by allow-list |
| API-T-015 | Batch | Mix authorized and unauthorized objects in batch | Per-object authorization; documented atomicity |
| API-T-016 | GraphQL depth | Submit query exceeding configured depth in local test | Rejected before expensive execution |
| API-T-017 | GraphQL breadth | Test aliases, batch operations and expensive field combinations | Cost/breadth limits enforced |
| API-T-018 | GraphQL resolver authz | Query nested foreign object and restricted field | Domain authorization denies/filters |
| API-T-019 | GraphQL subscriptions | Subscribe then revoke role/tenant access | Unauthorized stream access ends or is denied |
| API-T-020 | gRPC transport | Connect without trusted TLS identity where required | Connection/call rejected |
| API-T-021 | gRPC method authz | Invoke privileged RPC with low-privilege identity | Denied |
| API-T-022 | gRPC messages | Oversized, malformed or unexpected message fields | Bounded and validated |
| API-T-023 | gRPC streaming | Test long stream, expiry, revocation and message authorization | Stream remains within policy |
| API-T-024 | Webhook signature | Alter body, timestamp or signature | Rejected |
| API-T-025 | Webhook replay | Resubmit previously accepted delivery ID | Duplicate side effect prevented |
| API-T-026 | Webhook SSRF | Register disallowed destination in mock lab | Destination rejected |
| API-T-027 | Idempotency | Retry same key and reuse with different body | One side effect; conflicting reuse rejected |
| API-T-028 | Concurrency | Parallel requests against synthetic limited resource | Atomic invariant preserved |
| API-T-029 | Resource limits | Exceed payload, batch, concurrency or query-cost limits safely | Bounded rejection/throttling |
| API-T-030 | Sensitive flow | Repeat coupon/refund/assessment/booking action | Business rule prevents abuse |
| API-T-031 | SSRF | Test allow-listed and denied destinations in isolated mock network | Only approved destinations reached |
| API-T-032 | Upstream trust | Malformed schema, redirect and invalid certificate from mock provider | Response rejected safely |
| API-T-033 | Gateway bypass | Reach service through alternate path in lab | Direct access denied or equivalent controls enforced |
| API-T-034 | CORS | Untrusted Origin and credentialed requests | No unintended browser-readable access |
| API-T-035 | Error leakage | Cause controlled errors and inspect responses | No stack trace, secret or internal detail |
| API-T-036 | Cache isolation | Compare private response across synthetic principals/tenants | No cross-principal disclosure |
| API-T-037 | Inventory/version | Invoke old and undocumented routes | Lifecycle policy enforced; obsolete route retired |
| API-T-038 | Logging | Trigger authz denial and webhook replay | Correlated, useful, secret-free event emitted |
| API-T-039 | Token propagation | Observe downstream audience/scope and delegation | Token not over-propagated; least privilege |
| API-T-040 | Service identity | Workload invokes unapproved downstream service | Destination/action denied and logged |

## 26. Finding quality and remediation

A finding must include:
- Stable finding ID and affected API/operation.
- Environment, version, protocol and owner.
- Required identity/role/tenant and preconditions.
- Exact synthetic object and property context.
- Sanitized request/response or RPC evidence.
- Expected and observed policy.
- Business and technical impact.
- Root cause and affected code/configuration.
- CWE/OWASP category where supportable.
- Applicable ASVS/WSTG/contract reference with exact version.
- Remediation options and regression tests.
- Residual risk, owner, target date and retest result.

Severity should reflect the real operation, data, tenant scope, privilege, exploitability, business consequence and compensating controls. Do not assign severity only from the API Top 10 category or a scanner label.

## 27. Incident response for API compromise

1. Identify affected API, version, route, client and tenant.
2. Preserve gateway, service, identity, database, message-broker and downstream logs.
3. Determine whether the issue is token compromise, BOLA/BFLA/BOPLA, SSRF, business-flow abuse, webhook forgery, supply-chain or service identity compromise.
4. Contain the affected client, key, route, operation or workload identity.
5. Revoke/rotate exposed credentials and signing keys according to incident scope.
6. Block abusive egress and destinations where required.
7. Identify accessed/changed objects and affected tenants.
8. Determine downstream side effects, including payments, emails, jobs and partner events.
9. Stop or quarantine malicious background work where safe.
10. Restore from trusted state and reconcile transactions.
11. Notify owners and affected parties through approved legal/contractual processes.
12. Add regression tests and monitor for recurrence.
13. Complete post-incident root-cause and control-gap review.

Preserve evidence before destructive cleanup. Do not revoke every service credential indiscriminately without considering dependencies and safe containment order.

## 28. Enterprise reference scenarios

### 28.1 Multi-tenant SaaS management API

**Classification:** Composite scenario.

A SaaS platform exposes organization, user, course, document, report and configuration APIs. Main risks include BOLA, BFLA, BOPLA, tenant confusion, exports and bulk operations.

Required controls:
- Tenant resolved from trusted identity/relationship context.
- Object-scoped queries and authorization.
- Property-specific DTOs and response projections.
- Separate platform and tenant administration.
- Per-operation and per-tenant rate budgets.
- Audit for role, configuration and export actions.
- Tests across tenant, role, object, property and workflow state.

### 28.2 Financial payment and refund APIs

**Classification:** Composite scenario.

Payment/refund operations require transaction integrity, strong caller identity, audience/scope restriction, idempotency, atomic state transitions, separation of duties, approval limits and immutable audit. Never trust a client-supplied amount, beneficiary, account status or approval flag without server-side validation and authorization.

### 28.3 Industrial support integration API

**Classification:** Composite scenario.

A support platform integrates with an industrial asset inventory and approval workflow. The API must not provide direct public access to control networks. Use a brokered integration, workload identity, explicit asset scope, time-bound authorization, approval, egress allow-list and immutable audit. OT safety, segmentation and change control remain independent requirements; a valid API token does not authorize a control action on a PLC or HMI.

### 28.4 Partner webhook ecosystem

**Classification:** Composite scenario.

A SaaS provider sends lifecycle and billing events to partner endpoints. Risks include forged events, replay, endpoint SSRF, duplicate delivery, key compromise and tenant confusion. Use signed payloads, timestamp/delivery ID, replay storage, destination policy, retry control and integration-specific secret rotation.

### 28.5 GraphQL mobile aggregation layer

**Classification:** Composite scenario.

A mobile application uses GraphQL to aggregate account, order and notification data. Enforce field and resolver authorization, query-cost budgets, bounded pagination, subscription controls and token audience. Do not rely on hiding fields in the mobile client.

## 29. Tooling and engineering workflow

Tool selection must be driven by the test objective, protocol, environment, authorization and evidence requirements. Tools do not replace business authorization analysis.

### 29.1 API discovery and contract tools

- OpenAPI validators and linters.
- API catalog and gateway inventory.
- GraphQL schema and operation tooling.
- Protocol Buffer and gRPC reflection tools in controlled environments.
- Service catalog and deployment manifest review.
- CI contract-diff and compatibility checks.

### 29.2 API testing tools

- Burp Suite and OWASP ZAP for HTTP/API request inspection and controlled testing.
- Postman or Bruno for collection-based functional/security regression.
- curl and HTTPie for reproducible request construction.
- Schemathesis or equivalent property-based OpenAPI testing.
- RESTler or equivalent stateful REST API fuzzing in isolated test environments.
- GraphQL-specific query and schema testing tools.
- grpcurl and grpcui for authorized gRPC exploration.
- mitmproxy for controlled HTTP traffic analysis.
- Nuclei only with reviewed templates and explicit scoped targets.
- SAST, SCA and secret scanning in CI.
- Gateway/WAF logs, OpenTelemetry traces and SIEM for operational validation.

### 29.3 Tool governance

- Pin versions and record configuration.
- Review active scan templates before execution.
- Use test accounts and isolated environments.
- Rate-limit and monitor active testing.
- Avoid sending secrets or production data to hosted scanners.
- Preserve raw and sanitized evidence separately under approved retention.
- Confirm tool output manually before reporting.
- Record false positives and coverage gaps.
- Do not run fuzzers against production without explicit approved plan and safeguards.

## 30. Standards, frameworks and regulatory mapping

### 30.1 OWASP API Security Top 10:2023

Use the ten categories in Section 6 as a risk taxonomy. Map each relevant API operation to applicable risks, controls and test cases. Do not claim that absence of a Top 10 issue proves API security.

### 30.2 OWASP ASVS 5.0.0

Use ASVS 5.0.0 as the technical requirements baseline where its scope applies. Import exact requirement IDs from the official versioned source before creating a formal traceability matrix. This playbook intentionally does not invent ASVS identifiers. A requirement-to-test crosswalk remains an open controlled deliverable.

### 30.3 NIST SP 800-218 SSDF

The SSDF supports API security through secure design, implementation, verification, release integrity and vulnerability response. Use it to map the organizational lifecycle, not as a detailed API protocol test catalog.

### 30.4 ISO/IEC 27001:2022 Annex A relevance

| Control | Theme | API engineering relevance |
|---|---|---|
| 5.8 | Information security in project management | API security requirements and delivery gates |
| 5.15 | Access control | API function, object, property and tenant policy |
| 5.16 | Identity management | Human and workload identity lifecycle |
| 5.17 | Authentication information | Token, API key and secret protection |
| 5.18 | Access rights | Scope, client and permission review |
| 5.19–5.23 | Supplier/cloud relationships | Third-party API and hosted integration governance |
| 8.8 | Technical vulnerabilities | API framework, gateway and dependency patching |
| 8.9 | Configuration management | Gateway, schema, service and policy baselines |
| 8.15 | Logging | API security event collection |
| 8.16 | Monitoring activities | Abuse, anomaly and authorization monitoring |
| 8.20–8.22 | Network security | Edge, egress, segmentation and service connectivity |
| 8.25 | Secure development life cycle | API requirements and secure design |
| 8.26 | Application security requirements | API contract and authorization requirements |
| 8.28 | Secure coding | Safe parsing, serialization and query construction |
| 8.29 | Security testing | Contract, authorization, fuzz and manual testing |
| 8.32 | Change management | Versioning, deprecation and API configuration changes |

This is a relevance mapping, not evidence of implementation or certification.

### 30.5 Regulatory considerations

API security may support privacy, cybersecurity, financial, payment, outsourcing, critical-infrastructure and product-security obligations. Applicability depends on entity, data, sector, processing role, jurisdiction, contractual obligations and effective dates. Use Chapter 19 and obtain qualified legal/compliance review before asserting applicability.

## 31. API security operating model

### 31.1 Design gate

Before implementation:
- API owner and business purpose assigned.
- Data classification and tenant boundary documented.
- Authentication and authorization model approved.
- Contract and error model reviewed.
- Rate/cost and abuse controls defined.
- Downstream and webhook destinations identified.
- Logging and incident response designed.
- Relevant ASVS and API risk requirements selected.

### 31.2 Build gate

- Schema and contract linting.
- SAST, SCA and secret scanning.
- Unit tests for authorization policy.
- Contract and compatibility tests.
- Negative property and tenant tests.
- Dependency and container checks.
- Build artifact provenance and signing where required.

### 31.3 Release gate

- DAST and authorized API assessment.
- Function/object/property authorization matrix passes.
- Rate, payload, batch and query-cost limits validated.
- Gateway and direct-origin policy verified.
- Secrets and client credentials configured.
- Logs and detections validated.
- Open findings accepted by accountable risk owner.
- Version/deprecation metadata published.

### 31.4 Operations gate

- Inventory and owner remain current.
- API traffic and client identities monitored.
- Keys, certificates and signing keys rotate.
- Deprecated versions are retired.
- Security incidents and vulnerability disclosures have owners.
- Contract drift and route changes are detected.
- Periodic access and integration reviews are performed.

## 32. Limitations and open work

- Exact ASVS 5.0.0 requirement-to-test IDs must be imported from the official versioned release and peer-reviewed before this becomes a complete crosswalk.
- OWASP API Security Top 10 2023 remains the selected awareness baseline in this version; check OWASP for future editions before each review.
- API protocol behavior and implementation vary by gateway, framework, GraphQL runtime, gRPC language and deployment topology.
- The OpenAPI 3.2.1 edition was current in the official source reviewed on 2026-11-18; confirm current version before contract adoption.
- No executable API lab environment is claimed to exist until the companion lab specifications are implemented, pinned and reproduced.
- Regulatory mappings require jurisdiction-, sector- and entity-specific legal review.
- Composite scenarios are illustrative and are not claims about actual customer incidents.
- This playbook does not replace Chapter 07 identity engineering or Chapter 11 distributed systems engineering.

## 33. Related chapters
- [11. Distributed Systems and Integration Security](../11-distributed-systems-integration-security/DISTRIBUTED-SYSTEMS-AND-INTEGRATION-SECURITY-ENGINEERING.md)

- [01. AppSec Fundamentals](../01-fundamentals/APPSEC-FUNDAMENTALS.md)
- [02. Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [03. Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [04. Secure Coding and Code Review](../04-secure-coding/SECURE-CODING-AND-CODE-REVIEW.md)
- [05. Web Application Security Engineering](../05-web-application-security/WEB-APPLICATION-SECURITY-ENGINEERING.md)
- [05. Web Application Security Lab Pack](../05-web-application-security/WEB-APPLICATION-SECURITY-LAB-PACK.md)
- [06. API and Service Security Lab Pack](API-AND-SERVICE-SECURITY-LAB-PACK.md)
- [07. Identity and Access Security](../07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY.md)
- [08. Data Security and Privacy Engineering](../08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-ENGINEERING.md)
- [09. Mobile Application Security Engineering](../09-mobile-application-security/MOBILE-APPLICATION-SECURITY-ENGINEERING.md)
- [18. Standards Baseline and Mapping Method](../18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md)
- [19. Global Regulatory Register](../19-global-regulatory/GLOBAL-REGULATORY-REGISTER.md)

## 34. References

1. OWASP API Security Project: https://owasp.org/projects/api-security-project/
2. OWASP API Security Top 10:2023: https://owasp.org/API-Security/editions/2023/en/0x11-t10/
3. OWASP API Security Project documentation: https://owasp.github.io/www-project-api-security/
4. OWASP ASVS 5.0.0: https://asvs.owasp.org/
5. OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
6. IETF RFC 9700, OAuth 2.0 Security Best Current Practice: https://www.rfc-editor.org/rfc/rfc9700.html
7. OpenAPI Specification 3.2.1: https://spec.openapis.org/oas/v3.2.1.html
8. GraphQL Security: https://graphql.org/learn/security/
9. GraphQL Authorization: https://graphql.org/learn/authorization/
10. gRPC Authentication: https://grpc.io/docs/guides/auth/
11. gRPC Authorization: https://grpc.io/docs/guides/authorization/
12. gRPC Security: https://grpc.io/docs/guides/security/
13. NIST SP 800-218 Secure Software Development Framework: https://csrc.nist.gov/pubs/sp/800/218/final
14. IETF RFC 9110 HTTP Semantics: https://www.rfc-editor.org/rfc/rfc9110.html
15. IETF RFC 9113 HTTP/2: https://www.rfc-editor.org/rfc/rfc9113.html
16. IETF RFC 8446 TLS 1.3: https://www.rfc-editor.org/rfc/rfc8446.html

## 35. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial API and service security engineering playbook |
