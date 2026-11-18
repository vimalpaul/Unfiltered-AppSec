# 01. Application Security Fundamentals

| Field | Value |
|---|---|
| Document ID | UAPPSEC-01-001 |
| Status | Draft baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Application and product security lifecycle across web, API, mobile, distributed, cloud-native and AI-enabled systems |
| Classification | Public |

## 1. Executive summary

Application security (AppSec) is the discipline of managing security risk in software systems across their design, implementation, acquisition, integration, deployment, operation, maintenance and retirement. It addresses defects in code, insecure architecture, identity and authorization failures, data exposure, unsafe integrations, configuration weaknesses, software supply-chain compromise and abuse of legitimate business functionality.

AppSec is not synonymous with penetration testing, vulnerability scanning or secure coding. Those activities are important but cover only parts of the system and lifecycle. An effective AppSec capability translates business and regulatory needs into testable security requirements, places those requirements into engineering workflows, verifies that controls work under realistic threat conditions, and ensures that vulnerabilities and incidents are managed throughout the product's supported life.

The core operating chain is:

**Business objective → application context → architecture and data → threat and abuse analysis → risk decision → security requirement → control design → implementation → verification → evidence → operation and response → improvement.**

This chapter establishes the vocabulary and engineering model used throughout the knowledge base. Detailed implementation is delegated to the specialized chapters referenced below.

## 2. Purpose and applicability

Use this chapter when:
- Establishing an AppSec or Product Security capability.
- Defining the scope of an application security assessment.
- Explaining the difference between vulnerability testing and lifecycle security.
- Building a security requirements baseline.
- Determining which specialist chapters are required for an application.
- Selecting security measures based on architecture, data and business risk.

It applies to internally developed, externally acquired, SaaS, mobile, web, API, cloud-hosted, on-premises, embedded-within-an-application and AI-integrated software. It does not assume one development methodology or cloud provider.

## 3. Terminology and discipline boundaries

| Term | Meaning in this knowledge base | Boundary |
|---|---|---|
| Application Security | Engineering and assurance of security properties in software and its runtime dependencies | Broad discipline spanning the application lifecycle |
| Product Security | Security of a product as delivered and maintained for customers, including design, build, release, vulnerability handling and support | Broader than an individual application test |
| Secure SDLC | Security activities, requirements and gates integrated into the software development lifecycle | Does not mean one prescribed development methodology |
| Security Architecture | Structure of security-relevant components, trust boundaries, control placement, flows and failure handling | Must be grounded in the actual system design |
| Threat Modeling | Structured identification of assets, trust assumptions, threats, abuse cases, mitigations and residual risks | Not a one-time diagram exercise |
| Security Assessment | Evidence-based evaluation of control design and operation against stated criteria | Requires scope, method, evidence and limitations |
| Penetration Testing | Authorized, bounded testing that attempts to demonstrate security weaknesses and realistic attack paths | One verification technique, not a substitute for design assurance |
| Vulnerability Management | Lifecycle for identifying, validating, prioritizing, assigning, fixing, disclosing and retesting weaknesses | Includes operational and product support decisions |
| DevSecOps | Engineering and operating practices that integrate security into development and delivery workflows | Not merely installing scanners in CI/CD |
| Security Assurance | Evidence and evaluation that stated requirements and controls are designed and operating adequately | Assurance strength depends on evidence quality and test coverage |

## 4. Security objectives and properties

### 4.1 Core information security objectives

| Objective | Engineering meaning | Example application requirement |
|---|---|---|
| Confidentiality | Information is disclosed only to authorized principals and purposes | A learner can retrieve only records belonging to their tenant and permitted role |
| Integrity | Data, code, configuration and transactions cannot be altered outside approved authority | A client cannot alter another tenant's report, grade or account setting |
| Availability | Authorized users can access functions within defined service expectations | Login and assessment submission have capacity controls, graceful degradation and recovery |
| Authenticity | Identities, services, messages and artifacts can be validated as genuine | Service-to-service calls authenticate the workload and validate issuer, audience and key material |
| Accountability | Security-relevant actions can be attributed and investigated | Administrative changes record actor, target, time, action and outcome |
| Privacy | Personal data is processed with appropriate purpose, minimization, transparency and rights support | Data collection and retention are tied to a defined purpose and deletion workflow |
| Resilience | The application can withstand, contain and recover from defined failures and attacks | Critical services can restore transactionally consistent state after compromise or failure |

These properties can conflict. For example, detailed telemetry may improve accountability but create additional personal-data exposure. Strong authentication may reduce account takeover but introduce availability and accessibility concerns. The architecture must make these trade-offs explicit.

### 4.2 Security objectives are contextual

A public brochure site, a multi-tenant payroll product and a medical application do not have identical security priorities. A risk assessment must identify:
- Business functions whose loss would materially affect operations.
- Data classes and the consequences of disclosure, alteration, loss or misuse.
- Users, administrators, service identities and external parties.
- Legal, contractual and sector obligations that actually apply.
- Recovery objectives and dependencies.
- Threat actors and their likely opportunities.
- The organization's risk tolerance and accountable decision-maker.

A generic severity label cannot replace this context.

## 5. Application asset and attack-surface model

An application inventory should include more than hostnames and source repositories.

| Asset class | Examples | Security questions |
|---|---|---|
| Business capability | Payment, assessment, payroll, customer onboarding, reporting | What abuse would change a business outcome or bypass a control? |
| Application components | Browser client, mobile client, API, background worker, admin portal | Which components enforce security and which only display decisions? |
| Data | Personal data, credentials, tokens, payment records, source code, logs, exports | Where is data collected, derived, copied, cached, retained and deleted? |
| Identities | Customers, staff, administrators, service accounts, workload identities | Who authenticates them and how are permissions granted and revoked? |
| Interfaces | HTTP endpoints, GraphQL resolvers, queues, webhooks, file uploads, SSO callbacks | What input crosses a trust boundary and what authorization is applied? |
| Runtime and infrastructure | Cloud resources, containers, databases, gateways, identity providers | Which controls are inherited and which must the application implement? |
| Software supply chain | Source, package dependencies, registries, build runners, artifacts, signing keys | Can an attacker alter code or artifacts before release? |
| Security configuration | CORS, cookies, headers, OAuth clients, TLS, secrets, feature flags | Who owns changes and how are unsafe values detected? |
| Operational assets | Logs, alerts, backups, runbooks, deployment credentials | Can responders identify, contain and recover from abuse? |
| Third-party services | Payment gateway, email provider, analytics SDK, identity provider, AI model API | What data and authority are disclosed to the provider? |

Attack surface includes exposed entry points and the paths by which a user, dependency or compromised component can influence privileged operations or data. The attack surface changes when features, roles, APIs, integrations, deployment topology or data flows change.

## 6. Application security lifecycle

~~~mermaid
flowchart LR
    P[Product strategy and procurement] --> R[Requirements and data classification]
    R --> D[Architecture and threat modeling]
    D --> I[Implementation and code review]
    I --> B[Build and dependency controls]
    B --> V[Security verification]
    V -->|Pass or approved exception| L[Release and deployment]
    V -->|Defect| I
    L --> O[Runtime operations and monitoring]
    O --> H[Vulnerability handling and incident response]
    H --> F[Fix, patch, mitigate or retire]
    F --> D
    O --> Q[Periodic review and assurance]
    Q --> R
~~~

### 6.1 Lifecycle control objectives

| Lifecycle stage | Required security outcomes | Typical evidence |
|---|---|---|
| Strategy and procurement | Product purpose, data, system owner, supplier risk and security expectations are known | Product charter, application inventory, supplier assessment |
| Requirements | Security and privacy requirements are testable, prioritized and owned | Security requirements, data classification, acceptance criteria |
| Architecture | Trust boundaries, assets, threats, control placement and residual risk are reviewed | Architecture diagram, DFD, threat model, decisions |
| Implementation | Secure coding, peer review, secret management and developer environments are controlled | Pull requests, review records, static-analysis results |
| Build and supply chain | Source and dependencies are controlled; build inputs and artifacts are traceable | SBOM, provenance, build logs, signature verification |
| Verification | Security requirements are tested using suitable methods | Test cases, scan output, penetration-test evidence, retest |
| Release | Risk is accepted by the correct owner and artifacts are authorized | Release approval, exception register, signed artifact |
| Operations | Security events, access, vulnerabilities, backups and changes are managed | Logs, alerts, patch records, access reviews |
| Incident and vulnerability response | Weaknesses and incidents are triaged, contained, communicated and corrected | Incident timeline, advisory, root-cause analysis, corrective action |
| Retirement | Access, data, keys, dependencies and integrations are safely removed | Decommission checklist, deletion evidence, revoked credentials |

## 7. Risk model for application decisions

Risk should be expressed as a scenario, not merely as a scanner severity.

A useful statement format is:

> Because **[threat actor or failure condition]** can exploit **[weakness or control gap]** through **[attack path]**, they may affect **[asset or business process]**, resulting in **[business, privacy, financial, legal or operational impact]** under **[assumptions and conditions]**.

### 7.1 Risk analysis dimensions

- **Impact:** confidentiality, integrity, availability, privacy, fraud, safety, legal exposure, contractual penalties, reputation and customer trust.
- **Likelihood:** exposure, attacker capability, prerequisites, exploit complexity, availability of public tooling, reachability and compensating controls.
- **Exploitability:** authentication requirement, user interaction, network position, required privileges, attack complexity and exploit reliability.
- **Business context:** data sensitivity, tenant population, transaction value, privilege concentration, criticality and recovery capability.
- **Evidence confidence:** reproducibility, affected versions, reachability and whether the result is confirmed or inferred.

Qualitative or quantitative scales may be used, but scoring must be calibrated and documented. Do not multiply arbitrary values and present the result as objective precision. CVSS can inform technical severity; it does not fully determine enterprise risk or remediation priority. EPSS and known-exploitation intelligence can inform likelihood; they do not replace local exposure analysis.

### 7.2 Treatment options

| Treatment | Decision | Minimum governance |
|---|---|---|
| Mitigate | Implement or strengthen a control | Owner, due date and verification |
| Avoid | Remove the risky function or exposure | Product or architecture approval |
| Transfer/share | Allocate contractual or insurance responsibility where appropriate | Contract review; residual risk remains |
| Accept | Retain residual risk knowingly | Named risk owner, rationale, scope, expiry and review |
| Defer | Time-bound delay while planning action | Interim controls, accountable owner and escalation |

An exception must not become permanent merely because the due date passes. Expired exceptions require review and re-approval.

## 8. Security principles used across chapters

### 8.1 Secure by design

Security properties are architectural requirements. The design must identify where enforcement occurs, what the trusted computing base is, how identities are established, what happens when a dependency fails and how controls are verified.

### 8.2 Secure by default

A new installation or tenant should start with restrictive permissions and safe settings. Features, debug interfaces, sample credentials and administrative endpoints should not become externally exposed by default.

### 8.3 Least privilege

Users, processes, services, build agents and AI agents receive only the privileges required for a defined task and time. Authorization must be enforced server-side and at the resource or operation boundary.

### 8.4 Complete mediation

Every protected operation must make an authorization decision using trusted identity and context. A prior UI check, hidden button, client-supplied role or cached decision is not sufficient authority for a sensitive server-side operation.

### 8.5 Defense in depth

Use layered controls with distinct failure modes. A gateway filter may reduce exposure, but the application still needs correct authorization. Encryption does not prevent an authorized but over-privileged service from disclosing decrypted data. A WAF does not correct an insecure business rule.

### 8.6 Minimize attack surface and complexity

Remove unused endpoints, dependencies, permissions, debug features, exposed metadata and unnecessary data collection. Complexity increases the number of interactions and failure states that must be understood and verified.

### 8.7 Fail safely

A failed identity provider, policy service, key store or dependency must not silently turn a denied operation into an allowed one. Availability requirements may demand a carefully designed degraded mode, but the decision must be explicit, bounded, monitored and tested.

### 8.8 Make controls observable

Security decisions should generate appropriately protected telemetry. Logs must support investigation without storing plaintext passwords, bearer tokens, private keys or unnecessary personal data.

## 9. Control taxonomy

| Control family | Purpose | Application examples |
|---|---|---|
| Preventive | Reduce probability of a successful attack | Parameterized queries, server-side authorization, secure defaults, strong authentication |
| Detective | Identify attack attempts or control failure | Audit events, anomaly detection, integrity monitoring, dependency alerts |
| Responsive | Limit damage after detection | Account lock/recovery workflow, token revocation, feature disablement, incident playbooks |
| Recovery | Restore secure operation | Tested backups, artifact rebuild, key rotation, data reconciliation |
| Governance | Ensure ownership and risk decisions | Security requirements, approval gates, risk exceptions, supplier controls |
| Assurance | Demonstrate implementation and effectiveness | Design reviews, automated tests, independent assessment, evidence registers |

Controls can belong to multiple families. Classification is used to identify gaps, not to force a single category.

## 10. Roles and accountability

| Role | Primary AppSec responsibility |
|---|---|
| Product owner | Defines product purpose, risk appetite, priorities and acceptance authority within delegated limits |
| Business/data owner | Classifies data, defines permitted use and determines business impact |
| Solution architect | Owns system architecture, trust boundaries and design decisions |
| Engineering lead | Ensures secure implementation, code review, remediation and release readiness |
| Developer | Implements requirements and tests, handles secrets safely and fixes defects |
| AppSec engineer | Advises on requirements and architecture, performs or coordinates security verification, tracks risk and validates remediation |
| Platform/DevOps team | Secures runtime, build, deployment, identity and platform configuration |
| SOC/incident response | Monitors security telemetry and responds to suspected compromise |
| Privacy/legal/compliance | Interprets obligations and advises on data processing and regulatory scope |
| Internal audit/assurance | Independently evaluates governance and control evidence |

Security accountability cannot be delegated entirely to an AppSec specialist. Product and business owners remain accountable for risk decisions within their authority.

## 11. Practical use case: multi-tenant learning platform

**Scenario classification:** Composite industry scenario, not a reported incident.

A SaaS learning platform provides a browser interface, REST API, administrative console, background workers and a shared relational database. Multiple customer organizations use the same service. Learners access assigned courses and assessments; client administrators manage their own users and reports; platform administrators perform support operations.

### 11.1 Security-relevant assets

- Tenant identity and organization configuration.
- Learner profile and assessment results.
- Course documents and uploaded files.
- Authentication credentials and session tokens.
- Administrative functions and support impersonation.
- Audit events, exports and backups.
- Source repositories, build credentials and deployment artifacts.

### 11.2 Primary abuse cases

1. Learner changes an object identifier to read another learner's assessment.
2. Client administrator changes a tenant identifier to export another organization's records.
3. User modifies a request property to elevate their role or confidence/score field.
4. Support operator uses a privileged endpoint without a recorded business reason.
5. Background worker processes a forged event with an untrusted tenant identifier.
6. An exported report includes records outside the authenticated user's authorization scope.

### 11.3 Derived requirements

- Tenant context is derived from a validated server-side identity and membership, not trusted solely from a request parameter.
- Object and function authorization is enforced for every sensitive operation.
- Database access paths constrain records by the authorized tenant context.
- Privileged support functions require explicit authorization, time-bounded access and audit events.
- Data exports re-evaluate access at generation time and are scoped to authorized records.
- Sensitive actions are logged without recording bearer tokens or unnecessary personal information.
- Security tests use at least two synthetic tenants and distinct users with intentionally different permissions.

### 11.4 Evidence

Capture the role matrix, tenant model, relevant authorization policy, server-side request trace with tokens redacted, negative test results, database query behavior, audit event and retest record.

## 12. Metrics and control effectiveness

Use a balanced scorecard. A large number of scan findings alone is not proof that security is improving.

| Metric | What it measures | Interpretation cautions |
|---|---|---|
| Security requirements coverage | Applicable requirements with an owner and verification method | A requirement marked complete still needs valid evidence |
| Threat-model coverage | Critical applications and material changes with reviewed models | Model freshness and change triggers matter more than count |
| Critical/high risk age | Time from validated finding to verified remediation or accepted exception | Segment by exploitability, exposure and application criticality |
| Reopen / recurrence rate | Findings that recur after closure | Useful signal for root-cause and test quality |
| Authorization test coverage | Protected object/function paths with positive and negative tests | Endpoint count alone can mislead |
| Dependency remediation latency | Time to remediate vulnerable dependencies by risk | Include reachable and exploited context |
| Release security gate outcomes | Releases blocked, remediated or exception-approved | A low block rate can mean effective engineering or weak gates |
| Incident containment and recovery | Time to contain and restore secure service | Use consistent start/end definitions and severity grouping |
| Exception exposure | Active, expired and repeatedly extended security exceptions | Track residual risk and accountable owner |

## 13. Common misconceptions and failure modes

- **"We run a scanner, so the application is secure."** Automated tools detect only classes of conditions they can observe. They do not reliably prove business authorization, tenant isolation or workflow integrity.
- **"The frontend hides the function."** Client-side visibility is not a server authorization control.
- **"The gateway authenticates users, so every API is protected."** The API still needs authorization for each object, property and function.
- **"We use encryption, so data is protected."** Keys, authorization, endpoint exposure, plaintext processing and backups remain security concerns.
- **"The Top 10 is the complete test plan."** Awareness lists are not comprehensive verification standards or threat models.
- **"A clean penetration test means no vulnerabilities exist."** It means no in-scope issue was demonstrated under the stated method, time, access and limitations.
- **"Security is the AppSec team's job."** Engineering and product owners operate the controls; AppSec enables, challenges and verifies them.

## 14. Related chapters

- [Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [Architecture and Roadmap](../governance/REPOSITORY-ARCHITECTURE-AND-ROADMAP.md)
- [Standards Baseline and Mapping Method](../18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md)
- [Global Regulatory Register](../19-global-regulatory/GLOBAL-REGULATORY-REGISTER.md)

## 15. References

1. OWASP, Application Security Verification Standard (ASVS) 5.0.0, stable release published 2025-05-30: https://asvs.owasp.org/
2. OWASP, Top 10:2025, final project release: https://owasp.org/projects/Top-Ten
3. NIST, SP 800-218, Secure Software Development Framework (SSDF) v1.1, 2022-02-03: https://csrc.nist.gov/pubs/sp/800/218/final
4. NIST, Cybersecurity Framework 2.0, 2024-02-26: https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20
5. OWASP, API Security Top 10:2023: https://owasp.org/www-project-api-security/

## 16. Limitations and maintenance

This is the foundational model. It does not replace specialist chapters, legal analysis, product-specific architecture review or a tailored risk assessment. Examples are generic or composite unless otherwise labelled. Review when core source versions, relevant legal requirements or application architecture assumptions change.

## 17. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial AppSec fundamentals chapter |
