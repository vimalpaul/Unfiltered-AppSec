# 02. Application Architecture and Trust Boundaries

| Field | Value |
|---|---|
| Document ID | UAPPSEC-02-001 |
| Status | Draft baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Logical application architecture, data flows, identity and privilege boundaries, external dependencies and threat-model preparation |
| Classification | Public |

## 1. Executive summary

Application security architecture defines how an application's components, identities, data and security controls interact. It establishes where trust is placed, where authorization is enforced, how input crosses boundaries, which components can affect sensitive assets, how failures are contained and how the design can be verified.

A useful architecture review does not stop at a technology diagram. It identifies:
- Assets and business operations.
- Human, machine and workload identities.
- Entry points, APIs, messages, file transfers and callbacks.
- Data stores, caches, logs, backups and exports.
- Trust boundaries and privilege transitions.
- Security decision points and policy enforcement.
- External dependencies, administrative paths and build/deployment paths.
- Failure conditions and degraded operating modes.
- Threats, abuse cases, controls and validation evidence.

This chapter supplies an architecture and threat-modeling method. It is an engineering baseline, not a claim that one reference architecture is safe for every deployment.

## 2. Purpose, scope and prerequisites

Use this chapter during product inception, architecture design, major feature changes, cloud migration, tenant-model changes, identity integration, third-party integration, sensitive data processing and security reviews after a material incident.

Prerequisites:
- Business purpose and important workflows.
- Application inventory and accountable product owner.
- Initial data classification and user/role model.
- Available architecture and deployment information.
- Known external integrations and hosting dependencies.
- Agreed review scope and participants.

The method applies to browser applications, mobile backends, APIs, service-oriented systems, cloud-native applications and AI-enabled systems. Specialized chapters will extend it for mobile, Kubernetes, event-driven systems and AI agents.

## 3. Architecture description: what must be modeled

### 3.1 Four complementary views

| View | Questions answered | Typical artifact |
|---|---|---|
| Business and capability | Which business process is enabled, who uses it, what could be abused? | Context diagram, use-case map |
| Logical application | Which components, APIs, services and data stores cooperate? | Component diagram |
| Deployment and runtime | Where are components deployed, what network and platform boundaries exist? | Deployment diagram |
| Security and trust | Which identities and data are trusted, which privileges change, where are controls enforced? | DFD, trust-boundary map, identity flow |

A diagram is incomplete if it omits security-relevant background workers, management interfaces, scheduled jobs, file transfer, telemetry or build-to-release paths.

### 3.2 Minimum component inventory

For each component record:
- Unique component identifier and name.
- Business purpose and owner.
- Technology, version and support status.
- Environment and deployment location.
- Data processed, stored, transmitted or derived.
- Inbound and outbound interfaces.
- Human and machine identities used.
- Privileges and secrets available.
- External and internal dependencies.
- Security enforcement responsibilities.
- Logging, monitoring, backup and recovery behavior.

## 4. Reference logical architecture

The following is an illustrative multi-tenant SaaS architecture. It demonstrates useful separation of responsibilities. It is not a deployment prescription.

~~~mermaid
flowchart TB
    subgraph EXT[External and untrusted zone]
        U[Browser or mobile client]
        IDP[External identity provider]
        PARTNER[Partner API and webhook sender]
    end

    subgraph EDGE[Internet-facing trust zone]
        WAF[Edge protection and rate controls]
        GW[API gateway / reverse proxy]
    end

    subgraph APP[Application service trust zone]
        WEB[Web frontend / BFF]
        API[Application API]
        AUTHZ[Authorization policy enforcement]
        SVC[Business service layer]
        WORKER[Background worker]
        FILE[File processing service]
    end

    subgraph DATA[Restricted data zone]
        DB[(Transactional database)]
        CACHE[(Cache)]
        OBJ[(Object storage)]
        AUDIT[(Security audit store)]
    end

    subgraph OPS[Privileged operations zone]
        ADMIN[Privileged admin portal]
        CI[Build and deployment pipeline]
        SECRETS[Secrets and key management]
        OBS[Monitoring and incident response]
    end

    U -->|HTTPS| WAF
    PARTNER -->|Authenticated webhook| WAF
    WAF --> GW
    GW --> WEB
    GW --> API
    WEB --> IDP
    API --> IDP
    API --> AUTHZ
    AUTHZ --> SVC
    SVC --> DB
    SVC --> CACHE
    SVC --> OBJ
    WORKER --> SVC
    FILE --> OBJ
    API --> AUDIT
    ADMIN -->|MFA + privileged authorization| API
    CI -->|Signed deployment artifact| APP
    SECRETS --> APP
    APP --> OBS
    AUDIT --> OBS
~~~

### 4.1 Boundaries that must be explicit

The diagram shows logical zones, but the actual design review must define:
- Whether a browser session, mobile app or partner service is untrusted input.
- How identity claims are validated and transformed into application principals.
- Whether the gateway terminates TLS and what identity context it forwards.
- Whether internal service calls authenticate workloads.
- Whether authorization is checked at the service or data-access boundary.
- How tenant identity is determined and propagated.
- Whether worker messages can be forged, replayed or re-ordered.
- Which components can read secrets or decrypt data.
- Whether admin and support functions use a separate privilege path.
- How production deployment credentials and signing keys are protected.

A network subnet is not automatically a trust boundary. A trust boundary exists where data, authority, privilege or assumptions cross between components or administrative domains.

## 5. Data-flow modeling

### 5.1 Data-flow diagram notation

A practical DFD should identify:
- **External entity:** a user, partner, identity provider or external service.
- **Process:** a component that receives, transforms or emits data.
- **Data store:** a database, cache, queue, object store, log or backup.
- **Data flow:** a directional transfer with protocol, identity and relevant data.
- **Trust boundary:** a boundary across which the trust assumptions change.

Record the data classification, sensitivity, integrity requirement and retention characteristics for each important flow. Identify authentication and authorization context separately from business data.

### 5.2 Example transaction sequence

~~~mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant G as API Gateway
    participant A as Application API
    participant P as Authorization Policy
    participant D as Data Store
    participant L as Audit Service

    C->>G: HTTPS request with access token and object ID
    G->>A: Forward request after transport and gateway checks
    A->>A: Validate token issuer, audience, signature, expiry and claims
    A->>P: Authorize subject, tenant, action and resource
    P-->>A: Permit or deny with policy decision context
    alt Permit
        A->>D: Query within authorized tenant/resource scope
        D-->>A: Return permitted record
        A->>L: Record security-relevant read event
        A-->>C: Return permitted response
    else Deny
        A->>L: Record denied access outcome
        A-->>C: Return non-disclosing error response
    end
~~~

The sequence is illustrative. The policy decision may be embedded in the application or provided by a separate service. If a separate policy service is used, its availability, integrity, identity and failure behavior become part of the threat model.

## 6. Trust, identity and privilege boundaries

### 6.1 Identity is not authorization

Authentication establishes evidence about an identity or principal. Authorization determines whether that principal may perform a specific operation on a specific resource under the current context.

A trustworthy authorization decision may require:
- Validated principal and authentication strength.
- Tenant or organization membership from a trusted source.
- Resource ownership or relationship.
- Role and attribute assignments.
- Requested action and resource type.
- Data classification and contextual policy.
- Resource state and business workflow state.
- Time, device or transaction context where justified.

A role claim alone is not enough to authorize every resource. A correctly authenticated user can still be unauthorized for a particular object, field, export or business action.

### 6.2 Common trust-boundary failure modes

| Boundary | Failure mode | Design consideration |
|---|---|---|
| Browser to server | Client controls role, tenant or price fields | Treat client input as untrusted; derive authority from validated server-side context |
| API gateway to service | Identity headers can be spoofed or misinterpreted | Authenticate the gateway-to-service link and define signed or otherwise protected identity context |
| Service to service | Internal network location is treated as identity | Authenticate workload identity and authorize service actions |
| Application to database | Application has broad database privilege | Use scoped accounts, narrow query paths, row/object policy where appropriate and audited admin access |
| Worker to queue | Message fields are trusted without producer identity | Authenticate producer, validate schema and tenant context, protect replay and idempotency |
| Application to file/object storage | User controls object key or storage path | Bind object references to server-side authorization and safe storage policy |
| Application to identity provider | Claims are trusted without validating issuer/audience/nonce or flow binding | Implement protocol validation and reject invalid or ambiguous identity assertions |
| Build system to production | Build agent can access production secrets or alter release artifact | Separate build, signing and deployment identities and verify artifact provenance |
| Admin portal to application | Privileged path shares ordinary user controls without additional governance | Strong authentication, narrowly scoped roles, approval and enhanced audit |

## 7. Threat modeling method

Threat modeling is a repeatable analysis of how a system could be abused or fail and what controls are required. It should be performed early, refreshed when architecture or data changes, and connected to verification.

### 7.1 Method steps

1. **Define objective and scope.** Identify the feature, system boundary, release, environments and decisions required.
2. **Identify business and technical assets.** Include money, decisions, records, identities, secrets, data and critical service availability.
3. **Describe use and abuse cases.** Capture legitimate workflows and ways to misuse them.
4. **Build architecture and DFDs.** Include all interfaces, data stores, identities and administrative paths.
5. **Mark trust and privilege boundaries.** Record what changes at each boundary and why it is trusted.
6. **Enumerate threats.** Use STRIDE as a prompt, not as proof of completeness. Add privacy misuse, business logic abuse, fraud, supply-chain and resilience scenarios.
7. **Analyze attack paths.** State prerequisites, attacker position, affected component, weakness and possible business consequence.
8. **Select and verify mitigations.** Define security requirements and choose controls that interrupt the path.
9. **Assess residual risk.** Assign owner, treatment and due date; record assumptions and missing evidence.
10. **Create verification cases.** Test both expected allowed behavior and prohibited behavior.
11. **Maintain the model.** Trigger review on feature, data, role, integration, platform, threat or regulatory change.

### 7.2 STRIDE prompt model

| STRIDE category | Security property at risk | Application examples | Typical control direction |
|---|---|---|---|
| Spoofing | Authenticity | Forged identity assertion, stolen session, fake service caller | Strong identity validation, credential protection, workload identity |
| Tampering | Integrity | Modified assessment score, altered request property, forged event | Authorization, integrity checks, transaction rules, signed artifacts |
| Repudiation | Accountability | Privileged change cannot be attributed | Protected audit event, trusted timestamps and access controls over logs |
| Information disclosure | Confidentiality/privacy | Cross-tenant read, debug response, exposed object storage | Authorization, data minimization, encryption, safe errors |
| Denial of service | Availability | Expensive query, unbounded upload, OTP abuse | Resource quotas, timeouts, queue limits, graceful degradation |
| Elevation of privilege | Authorization | User reaches admin route, mass assignment changes role | Deny-by-default authorization, privilege separation and property allowlists |

STRIDE is useful for systematic threat prompts. It does not guarantee coverage of privacy harms, business workflow abuse, algorithmic manipulation or emerging AI-specific threats. These require additional analysis.

### 7.3 Threat record format

Every material threat should have:
- Stable threat ID.
- Scenario and affected use case.
- Threat actor or failure condition.
- Asset and boundary.
- Preconditions and attack path.
- Weakness or missing control.
- Impact and likelihood rationale.
- Existing mitigations and their evidence.
- Required mitigation and owner.
- Residual risk and decision.
- Test case and closure evidence.
- Source or assumption classification.

## 8. Worked threat scenario: cross-tenant assessment disclosure

**Scenario classification:** Composite SaaS scenario for engineering training; not a verified public incident.

### 8.1 Business context

A multi-tenant learning platform stores assessment results in a shared database. A learner authenticates successfully and requests an assessment result by identifier. The endpoint uses a numeric record ID and verifies that the user is logged in, but the data query does not constrain the record to the user's authorized tenant or learner relationship.

### 8.2 Attack path

1. An authenticated user opens their own assessment result.
2. The client sends a request containing an assessment-result identifier.
3. The user changes the identifier to a value associated with another record.
4. The API confirms only that the user has a valid session.
5. The service retrieves the record without object-level authorization.
6. Sensitive result data is returned to the wrong tenant or user.

The central failure is not identifier predictability. It is missing authorization at the object access boundary. Random identifiers may reduce guessability but do not replace access control.

### 8.3 Corrective architecture

- Establish a validated principal from the authentication protocol.
- Resolve tenant membership and user-to-resource relationships from trusted server-side data.
- Authorize the requested action against the requested object before returning or modifying it.
- Apply tenant scoping in the data access path as defense in depth.
- Ensure caches and exports preserve authorization context.
- Record denied access attempts with enough context for investigation.
- Avoid exposing existence details where that would create an additional information leak.

Illustrative query pattern:

~~~sql
SELECT r.id, r.score, r.completed_at
FROM assessment_result AS r
JOIN learner_membership AS m
  ON m.learner_id = r.learner_id
WHERE r.id = :requested_result_id
  AND m.user_id = :authenticated_user_id
  AND m.tenant_id = :authorized_tenant_id;
~~~

The placeholders represent parameterized values. The authorized tenant must come from a validated server-side membership decision, not an untrusted query parameter. The actual schema and policy must account for delegated administrators, shared courses, support access and other legitimate relationships.

### 8.4 Required verification

| Test ID | Principal | Requested resource | Expected result | Evidence |
|---|---|---|---|---|
| TM-AUTHZ-001 | Learner A, Tenant A | Learner A's own result | Permit | Request/response with synthetic identities |
| TM-AUTHZ-002 | Learner A, Tenant A | Learner B's result, same tenant | Deny unless explicit sharing policy permits | Denial and audit event |
| TM-AUTHZ-003 | Learner A, Tenant A | Learner C's result, Tenant B | Deny | Denial and no returned data |
| TM-AUTHZ-004 | Client admin, Tenant A | Report for Tenant A | Permit within assigned scope | Export scope evidence |
| TM-AUTHZ-005 | Client admin, Tenant A | Report for Tenant B | Deny | Denial and no cross-tenant rows |
| TM-AUTHZ-006 | Unauthenticated caller | Any result | Reject authentication | No sensitive object metadata returned |

A successful negative test must demonstrate that data was not disclosed through the response, cache, export, error body or secondary endpoint.

## 9. Architecture review procedure

### 9.1 Authorization and preparation

- Obtain system-owner approval and identify the review scope.
- Request current logical and deployment diagrams, API inventory, data classification, role matrix, identity flows and integration list.
- Identify system owner, architect, engineering lead, AppSec reviewer, data owner and operations contact.
- Agree on which design decisions are in scope and which environments are excluded.
- Do not request production secrets. Use redacted configuration and synthetic examples.

### 9.2 Review steps

1. Reconcile diagrams against deployed components and current API/interface inventory.
2. Identify external entry points, admin routes, background jobs, webhooks, file processing and operational interfaces.
3. Trace sensitive data from collection through processing, storage, caching, telemetry, export, backup and deletion.
4. Trace each human and machine identity from authentication to authorization enforcement.
5. Mark trust boundaries and privilege transitions.
6. Identify components with broad data or administrative access.
7. Review failure behavior for identity, policy, database, message broker and secrets dependencies.
8. Enumerate threats and misuse cases for each critical workflow.
9. Define mitigations and map them to requirements and test cases.
10. Assign residual risk and obtain decisions from authorized owners.
11. Revisit the diagram and requirements after remediation to ensure design and implementation still match.

### 9.3 Stop and escalation conditions

Pause the review or any validation activity when:
- The supplied scope does not match the system being assessed.
- Production data or credentials are exposed unexpectedly.
- A test may disrupt availability, change real records or trigger customer notifications.
- An active compromise is suspected.
- The reviewer cannot establish authorization for a proposed test.
- A critical design dependency or ownership boundary is unknown.

Escalate suspected incidents through the organization's incident-response process rather than continuing a normal design exercise.

## 10. Design patterns and trade-offs

| Pattern | Benefit | Risk or trade-off | Verification focus |
|---|---|---|---|
| API gateway plus service authorization | Centralized edge controls with service-level access decisions | Gateway may become a false trust anchor or single point of failure | Direct-service exposure and forged forwarding headers |
| Central policy decision point | Consistent policy and decision evidence | Availability, latency and policy deployment become critical dependencies | Fail-open/fail-closed behavior and stale policy |
| Tenant-scoped data access | Reduces accidental cross-tenant queries | Schema and relationship complexity; shared reporting may need explicit exceptions | Negative tenant-isolation tests across all data paths |
| Separate administrative plane | Reduces exposure and privilege mixing | Operational complexity and emergency-access requirements | Strong authentication, approval and break-glass evidence |
| Event-driven worker | Decouples processing and supports scale | Replay, ordering, poison messages and identity context | Authenticated producer, idempotency, schema and tenant validation |
| Signed build artifacts | Helps detect unauthorized artifact alteration | Signing-key compromise and build provenance remain relevant | Signature validation, key protection and provenance verification |

## 11. Architecture acceptance criteria

Before a material release or design approval, confirm:
- All critical components, interfaces, external dependencies and data stores are inventoried.
- Data classification and retention assumptions are recorded.
- Human, machine and administrative identities are identified.
- Trust boundaries and authorization enforcement points are explicit.
- Sensitive read, write, export and administrative operations have testable authorization requirements.
- Threats have owners and risk treatment decisions.
- Failure modes do not silently bypass security.
- Logging is adequate for investigation and does not leak secrets.
- Supply-chain and deployment boundaries are included.
- Verification cases cover both permitted and prohibited behavior.
- Residual risk is accepted by a named authorized owner.
- Architecture and evidence have version identifiers and change triggers.

## 12. Tooling and implementation notes

Tools may help create DFDs, inspect infrastructure, discover APIs or track threats, but the quality of the analysis depends on architecture knowledge and stakeholder evidence.

Candidate categories:
- Diagramming: Mermaid, PlantUML, diagrams.net.
- Threat modeling: Microsoft Threat Modeling Tool, OWASP Threat Dragon and structured registers.
- API discovery: OpenAPI/Swagger inventory and gateway configuration.
- Infrastructure visibility: cloud asset inventory, Kubernetes manifests and IaC scanning.
- Code and dependency analysis: static analysis, software composition analysis and secret scanning.
- Validation: controlled browser proxy, API client, unit/integration tests and isolated vulnerable applications.

Selection must consider maintenance, data sensitivity, access controls, export format, team adoption and tool limitations. Tool output is evidence input, not a threat model conclusion.

## 13. Related chapters

- [AppSec Fundamentals](../01-fundamentals/APPSEC-FUNDAMENTALS.md)
- Secure SDLC and Product Security (planned)
- Identity and Access Security (planned)
- API and Service Security (planned)
- Data Security and Privacy Engineering (planned)
- Security Verification and Assessment (planned)

## 14. References

1. OWASP Threat Modeling: https://owasp.org/www-community/Threat_Modeling
2. OWASP Threat Dragon: https://owasp.org/www-project-threat-dragon/
3. OWASP ASVS 5.0.0: https://asvs.owasp.org/
4. OWASP API Security Top 10:2023: https://owasp.org/www-project-api-security/
5. NIST SP 800-218 SSDF v1.1: https://csrc.nist.gov/pubs/sp/800/218/final
6. Qatar National Information Assurance Standard v2.1, Software Security and Web Application controls: https://assurance.ncsa.gov.qa/sites/default/files/publications/policy/2023/NCSA_CSGA_%20National_Information_Assurance_Standard_En_V2.1_0.pdf
7. Saudi Arabia National Cybersecurity Authority, Essential Cybersecurity Controls ECC 2:2024: https://cdn.nca.gov.sa/api/files/public/upload/86e09090-44e4-481f-bc28-355673607654_ECC--2024-EN.pdf

## 15. Limitations and maintenance

The reference architecture is illustrative. Production designs require environment-specific diagrams and validation. STRIDE is a threat prompt method, not a proof of completeness. Example SQL is a conceptual pattern and must be adapted to the real schema, identity model and business rules. Review this chapter when identity, tenant, data, deployment, integration or trust assumptions change.

## 16. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial architecture and trust-boundary engineering chapter |
