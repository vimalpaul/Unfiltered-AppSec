# 03. Secure SDLC and Product Security Operating Model

| Field | Value |
|---|---|
| Document ID | UAPPSEC-03-001 |
| Status | Draft baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Lifecycle governance and engineering controls for internally developed, acquired and maintained software |
| Classification | Public |

## 1. Executive summary

A Secure Software Development Lifecycle (SSDLC) is the set of governance, engineering, verification and operational practices that make security part of software delivery rather than a final inspection. It applies to internally developed applications, purchased software, software-as-a-service integrations, mobile products, APIs, cloud-native workloads and AI-enabled features.

The objective is not to insert an identical security checklist into every sprint. It is to identify the risk and assurance needs of each product, select security activities proportional to those needs, assign accountable owners, integrate controls into the work already performed and retain evidence that requirements were satisfied.

This chapter defines:
- A product security operating model and responsibility structure.
- Risk-tiered lifecycle gates that work with Agile, Kanban, Waterfall and DevOps.
- Security requirements and their acceptance criteria.
- Architecture and threat-model review triggers.
- Secure implementation, source, build and dependency controls.
- Security verification and release decisions.
- Vulnerability, exception and feedback processes.
- Evidence and metrics for assurance.

The baseline is designed to be tailored to the organization. It is not a certification scheme and it does not prescribe one software delivery method.

## 2. Purpose and applicability

Apply this chapter when:
- Establishing an AppSec programme or product security function.
- Introducing security gates into engineering delivery.
- Defining product security responsibilities and escalation paths.
- Setting requirements for vendors and acquired software.
- Determining the required assurance before production release.
- Establishing exception and vulnerability-management processes.

The chapter covers new development, substantial changes, acquired applications, integrations, platform migrations and ongoing maintenance. It does not prescribe the detailed secure coding or testing methods covered in specialized chapters.

## 3. Operating model

### 3.1 Three connected operating layers

| Layer | Responsibility | Expected outputs |
|---|---|---|
| Product and business governance | Define product criticality, risk appetite, budget, regulatory context and accountable risk owners | Product security policy, risk decisions, security roadmap and exception authority |
| Engineering delivery | Translate requirements into design, code, build, release and runtime controls | Secure architecture, code review, pipeline policy, test evidence and remediation |
| Independent assurance and oversight | Challenge assumptions and verify control implementation proportionate to risk | Independent review, audit evidence, penetration test, control assessment and improvement findings |

The security organization should help establish standards, coach teams, review high-risk designs and validate controls. It should not become the sole owner of product risk or the final approver of business risk that belongs to a product owner or designated executive.

### 3.2 Roles and responsibilities

| Activity | Accountable role | Responsible contributors | Consulted / informed |
|---|---|---|---|
| Product criticality and business impact | Product owner / business owner | Product manager | Security, privacy, operations |
| Data classification and processing purpose | Data owner / privacy owner | Product and data engineering | Legal, AppSec |
| Security requirements | Engineering/product owner | AppSec, architect, developers | Privacy, compliance, operations |
| Architecture and threat model | Solution architect | Engineering, AppSec, data and platform teams | Product owner, SOC |
| Secure code and code review | Engineering lead | Developers, reviewers | AppSec |
| CI/CD and build controls | Platform / DevSecOps lead | Build engineering, developers | AppSec, operations |
| Security testing plan | Engineering lead or assurance owner | AppSec, QA, specialist testers | Product owner, SOC |
| Release risk decision | Authorized release / business risk owner | Engineering and security provide evidence | Legal, compliance, operations |
| Risk exception | Designated risk owner under policy | Control owner and AppSec document the case | Business, legal, audit |
| Vulnerability intake and PSIRT | Product security owner | AppSec, engineering, support and communications | Legal, privacy, SOC, customers as required |
| Production detection and response | Service owner / incident commander | SOC, SRE, engineering, AppSec | Management, legal, privacy |

A RACI matrix should be tailored for each organization. One person may hold multiple roles in a small team, but the decision rights must remain explicit.

## 4. Application risk tiering

Risk tiering selects the level of assurance. It must not be reduced to a simplistic public/internal label.

### 4.1 Recommended input dimensions

- Data sensitivity, volume and impact to individuals.
- Business criticality and maximum tolerable outage.
- External exposure and attack surface.
- User population and tenant model.
- Privileged operations and ability to affect other systems.
- Financial, safety, legal and regulatory consequences.
- Third-party and supply-chain dependencies.
- Internet-facing administrative paths.
- Use of cryptographic keys, payment data or high-value credentials.
- AI model, retrieval and tool-execution authority.
- Recovery capability and control maturity.

### 4.2 Example assurance tiers

The following tier model is an organizational design option, not a regulator-mandated classification.

| Tier | Example context | Minimum assurance posture |
|---|---|---|
| Tier 1 – Critical | Payment processing, regulated financial workflows, identity platform, critical customer records, high-impact administrative plane | Formal threat model; independent architecture review; explicit security requirements; mandatory code/dependency/secret/IaC checks as relevant; manual security testing; independent assessment before material release; tracked risk approval; enhanced monitoring and response rehearsal |
| Tier 2 – High | Internet-facing multi-tenant SaaS, customer portals, APIs handling personal or commercial-sensitive data | Threat model for significant changes; documented authorization model; automated pipeline security checks; manual testing of high-risk workflows; release evidence and named risk owner |
| Tier 3 – Standard | Internal business applications with limited sensitivity and bounded privilege | Baseline security requirements; approved patterns; automated code/dependency/secret checks; risk-based validation; controlled release and vulnerability remediation |
| Tier 4 – Low | Static informational application with no sensitive data or privileged transaction flow | Secure configuration baseline, dependency and platform hygiene, change control and basic verification |

A low tier is not permission to ignore known vulnerabilities, legal requirements or shared-platform risks. Re-tier whenever data, exposure, tenant model, business function, privileged access or integration changes.

## 5. SSDLC lifecycle and security gates

~~~mermaid
flowchart TD
    A[Idea / acquisition] --> B[Product intake and risk tier]
    B --> C[Security and privacy requirements]
    C --> D[Architecture and threat model]
    D --> E[Plan and backlog]
    E --> F[Implement and peer review]
    F --> G[Build and supply-chain checks]
    G --> H[Security verification]
    H --> I{Release criteria met?}
    I -->|No| J[Fix, mitigate or request risk exception]
    J --> F
    I -->|Yes| K[Approved release and deployment]
    K --> L[Runtime protection and monitoring]
    L --> M[Vulnerability handling and incident response]
    M --> N[Patch, improve or retire]
    N --> C
~~~

### 5.1 Gate definition

Each gate should define:
- Entry criteria.
- Required inputs.
- Activities and accountable owner.
- Exit criteria.
- Evidence retained.
- Risk exception authority.
- Escalation and stop conditions.

A gate is an evidence-based decision, not a meeting or a checkbox.

### 5.2 Lifecycle control matrix

| Stage / gate | Required activities | Minimum exit evidence | Stop or escalation conditions |
|---|---|---|---|
| Intake | Identify product owner, business purpose, data, market, supplier and criticality | Application record, owner, initial risk tier, regulatory screening | No accountable owner; unknown data purpose; unclear supplier rights |
| Requirements | Define security/privacy requirements and acceptance tests | Approved requirement set, owner and verification method | Sensitive processing or privileged workflow has no security requirements |
| Design | Review architecture, trust boundaries, identity, data flow, threat model and abuse cases | Versioned diagrams, threat register, decisions and mitigations | Critical threat lacks control owner or risk treatment |
| Implementation | Secure coding, peer review, dependency control, secrets handling and safe configuration | Review records, static-analysis results and resolved findings | Hardcoded secret, unsafe authorization path or prohibited build condition |
| Build | Protect source, build runner, dependencies, artifact and signing credentials | Build provenance, dependency inventory, scan results, artifact integrity evidence | Artifact cannot be traced to reviewed source or secret exposure is unresolved |
| Verification | Validate requirements using automated and manual tests proportionate to risk | Test plan, cases, results, evidence, defects and retest | Critical requirement untested; critical/high defect unresolved without authorized treatment |
| Release | Confirm scope, residual risk, rollback, monitoring and support readiness | Release decision, exception records, deployment approval | Unowned risk, unsupported component, missing rollback or insufficient response readiness |
| Operations | Monitor, patch, review access, test recovery and assess changes | Security events, vulnerability SLA, access reviews and recovery evidence | Material exposure or compromise not contained through incident process |
| Retirement | Revoke access, remove data and secrets, close integrations and preserve required records | Decommission approval, deletion evidence, credential revocation | Legal hold or retention requirement unresolved |

## 6. Security requirements engineering

### 6.1 Requirements must be testable

Avoid requirements such as "the application must be secure", "use encryption" or "prevent unauthorized access" without measurable behavior.

A useful requirement has:
- Unique identifier.
- Security objective.
- Trigger or condition.
- Required behavior.
- Scope and actor.
- Test or evidence method.
- Owner and priority.
- Related threat, data class or external obligation.

Example:

**REQ-AUTHZ-004 – Tenant object isolation**

For every operation that reads, updates, deletes or exports tenant-owned records, the server shall authorize the authenticated principal against the requested object and the principal's currently valid tenant membership before returning or changing the record. A user from Tenant A shall not retrieve or modify Tenant B data unless an explicit, approved sharing relationship grants the specific action. Verification shall include positive and negative tests using at least two tenants and multiple user roles.

This requirement is testable and identifies a control boundary and evidence model. It is a project-authored example, not a quotation from a standard.

### 6.2 Requirement categories

| Category | Example requirement themes |
|---|---|
| Identity and authentication | Authentication assurance, MFA, federation, account recovery, service identity |
| Authorization | Object, function, property, tenant, administrative and delegated access |
| Session and token | Issuer/audience validation, expiry, rotation, revocation, cookie and CSRF protections |
| Input and output | Schema validation, canonicalization, safe query handling, contextual output encoding |
| Data protection | Classification, minimization, encryption, retention, deletion, export and backup |
| Cryptography | Approved primitives, key lifecycle, algorithm agility, secure randomness and rotation |
| API and integration | Inventory, authentication, authorization, quotas, replay protection, webhook validation |
| Availability and resilience | Resource limits, rate control, timeout, idempotency, backup and recovery |
| Logging and accountability | Event coverage, identity attribution, integrity, safe redaction and retention |
| Supply chain | Dependency inventory, provenance, build integrity, signatures and supported components |
| Privacy | Purpose, notices, consent or other basis where applicable, rights support and transfer controls |
| AI features | Prompt/data boundaries, retrieval authorization, tool scope, output validation and human approval |
| Operations | Patchability, monitoring, incident response, secure configuration and support period |

### 6.3 Acceptance criteria structure

For each requirement record:
- Preconditions and test principal.
- Exact endpoint, workflow or component.
- Permitted operation and expected result.
- Prohibited operation and expected result.
- Relevant data and role combinations.
- Evidence to capture.
- Failure severity and escalation.

Do not test only the happy path. Authorization and workflow requirements require negative cases.

## 7. Secure design and architecture control

A threat model is required when material risk changes, not only at initial project creation.

### 7.1 Mandatory review triggers (recommended policy)

- New application, product or major feature.
- New internet-facing endpoint or administrative interface.
- New data class, processing purpose or export path.
- New tenant model, identity provider or authentication protocol.
- New privileged function or service account.
- New third-party API, webhook, package registry or AI tool integration.
- Significant cloud, container, orchestration or network architecture change.
- New payment, health, government or other regulated workflow.
- Material vulnerability, security incident or change in threat assumptions.
- End-of-life component or platform migration.

### 7.2 Design review evidence

- Current context, logical and deployment diagrams.
- DFD and trust-boundary map.
- Data classification and retention record.
- Identity and role matrix.
- Threat and abuse-case register.
- Security requirement set.
- Approved secure design patterns.
- Risk decisions and exceptions.
- Validation approach and owners.

See [Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md).

## 8. Secure implementation and code review

The organization should provide developers with secure libraries, approved patterns and practical training. A policy that only says "follow secure coding" is insufficient.

### 8.1 Minimum engineering practices

- Use parameterized database operations and safe query APIs.
- Enforce authorization server-side for every protected object and operation.
- Validate input against explicit schemas and business rules.
- Encode output for its destination context.
- Use approved cryptographic libraries and key-management services.
- Avoid logging passwords, access tokens, session identifiers and private keys.
- Store secrets in managed secret stores and use scoped identities.
- Pin, inventory and update dependencies according to risk.
- Restrict file processing, archive extraction, redirects and outbound network access.
- Review concurrency, transaction integrity, idempotency and state transitions.
- Use safe error handling without leaking stack traces or secrets.
- Protect administrative and support workflows separately from ordinary user workflows.

### 8.2 Review procedure

1. Confirm change purpose, affected components, data and security requirements.
2. Identify input sources, trust boundaries, identity and authorization checks.
3. Review sensitive data access, query construction, output encoding and error handling.
4. Inspect secrets, configuration, dependency and permission changes.
5. Check race conditions, replay, duplication, transaction ordering and business-state manipulation.
6. Review test coverage for expected and forbidden behaviors.
7. Run the configured static analysis, secret scanning and dependency checks.
8. Record findings and owners; do not treat dismissed warnings as fixed without rationale.
9. Verify remediation and retain review evidence.

### 8.3 Review stop conditions

Block or escalate changes when they introduce hardcoded credentials, unauthenticated privileged operations, unbounded sensitive data export, known exploitable critical dependencies without mitigation, unsafe deserialization or an authorization bypass. The organization's approved severity and exception policy determines the exact blocking threshold.

## 9. Build, dependency and release integrity

The build pipeline is a privileged part of the application architecture. It can read source, retrieve dependencies, sign artifacts and deploy production workloads.

Minimum controls:
- Protect repository membership, branch policy and review requirements.
- Use short-lived or scoped credentials where supported.
- Keep build and deployment identities separate where feasible.
- Restrict runner access to production secrets.
- Lock dependency sources and record resolved versions.
- Scan dependencies and container/IaC artifacts.
- Generate and retain a Software Bill of Materials (SBOM) in a suitable format.
- Record build inputs and provenance sufficient to associate an artifact with reviewed source and workflow.
- Sign release artifacts where appropriate and verify them before deployment.
- Protect signing keys and prevent unapproved jobs from using them.
- Restrict deployment permissions and record approvals.
- Rebuild from trusted source rather than patching an untraceable artifact.

See [Chapter 13: Software Supply Chain Security](../13-software-supply-chain-security/SOFTWARE-SUPPLY-CHAIN-SECURITY-ENGINEERING.md) for detailed implementation, build integrity, SBOM, provenance, signing and supplier assurance.

## 10. Verification strategy

No single testing technique provides complete assurance.

| Method | Finds / verifies | Limitations |
|---|---|---|
| SAST | Source-level patterns, tainted data flows and some insecure coding | May not understand runtime state, architecture or business context |
| SCA | Known vulnerable and unsupported dependencies, licenses and dependency inventory | Reachability, exploitability and transitive usage require analysis |
| Secret scanning | Credentials and key patterns committed to repositories or build logs | Detection depends on patterns and coverage; rotation is still required |
| DAST | Runtime-observable web and API weaknesses | Limited by authentication, crawling, test data and application state |
| IAST | Runtime context combined with test execution | Requires supported instrumentation and representative test paths |
| IaC / configuration scanning | Insecure infrastructure and cloud configuration patterns | Cannot prove effective deployed behavior by itself |
| Container/image scanning | Known package vulnerabilities and image configuration issues | Does not prove runtime reachability or application authorization |
| Manual code review | Complex logic, trust boundaries, business rules and unsafe design | Reviewer skill, scope and time constrain coverage |
| Threat-model validation | Whether mitigations address identified attack paths | Depends on model quality and implementation evidence |
| Penetration testing | Demonstrable attack paths across selected scope | Point-in-time, bounded by rules, access and testing period |
| Independent assessment | Challenge of design and control effectiveness | Scope and independence must be documented |

Testing should be chosen based on requirements, risks and failure modes. An automated pipeline should produce actionable results, suppress only with a recorded rationale, and route unresolved findings to owners.

## 11. Release decision model

A release decision should consider:
- Test scope and results.
- Open vulnerabilities and their exploitation context.
- Security requirement coverage.
- Threat model changes and unresolved risks.
- Dependency and artifact provenance.
- Data migration and secrets rotation.
- Operational monitoring and incident response readiness.
- Rollback and recovery.
- Regulatory and contractual release conditions.

### 11.1 Example release outcome

| Condition | Decision |
|---|---|
| Security requirements satisfied, critical/high findings closed or mitigated, evidence complete, no expired exception | Eligible for release approval |
| Medium findings remain with documented mitigation, owner and due date | Conditional release according to policy and risk tier |
| Critical exploitable weakness, known authorization bypass or exposed credential remains | Block release unless a formally authorized emergency-risk process explicitly governs the decision; do not silently waive |
| Test evidence missing for a critical workflow | Hold release until verified or an explicitly authorized risk decision is made |
| Artifact provenance or integrity is unknown | Block release until trusted build and artifact chain is established |
| New threat or scope change invalidates prior assessment | Reassess and obtain a new decision |

The decision authority must be authorized by organizational policy. AppSec can recommend a hold and explain the risk; business risk acceptance must be performed by the named risk owner.

## 12. Security exception process

An exception must contain:
- Exception ID and affected product, version, component and environment.
- Requirement/control not met.
- Finding and supporting evidence.
- Business reason and urgency.
- Impact and exploitability analysis.
- Existing and interim safeguards.
- Residual risk and affected users/data.
- Named risk owner and approver.
- Remediation plan and due date.
- Expiry date and review cadence.
- Conditions that automatically revoke the exception.
- Retest and closure evidence.

No indefinite exceptions. Repeated extensions require explicit review of root cause and control feasibility. Legal or regulator-mandated requirements must not be waived through an internal security exception.

## 13. Product Security and vulnerability lifecycle

A product owner must establish a process to:
1. Receive internal findings and external reports.
2. Acknowledge and track submissions.
3. Validate affected products and versions.
4. Assess exploitability, impact and exposure.
5. Coordinate remediation, mitigation or workaround.
6. Determine customer, regulator and public disclosure obligations.
7. Publish security advisories when required and appropriate.
8. Distribute patches and verify update integrity.
9. Retest and close the vulnerability.
10. Perform root-cause analysis and prevent recurrence.

Where the EU Cyber Resilience Act applies, Article 14 actively-exploited vulnerability reporting becomes a product-security process dependency from 11 September 2026. Product teams must identify who is the manufacturer, which products are in scope and how discovery timestamps and notifications are governed.

See the Global Regulatory Register and future Vulnerability Management / PSIRT chapter.

## 14. Integrating controls into common delivery models

### 14.1 Agile / Scrum

- Add security requirements and abuse cases to the backlog.
- Include risk and data changes in refinement.
- Include security acceptance criteria in the definition of done.
- Use continuous automated checks for fast feedback.
- Threat-model significant changes rather than waiting for a release milestone.
- Review risk and open findings during release planning.

### 14.2 Kanban

- Use explicit workflow states for security review, blocked findings and accepted exceptions.
- Set service-level targets for triage and remediation by risk.
- Limit work in progress for unresolved critical security issues.
- Make security dependencies visible in change records.

### 14.3 Waterfall / phase-gated delivery

- Define requirements and design assurance before implementation.
- Perform secure design reviews at architecture baselines.
- Embed security test plans in system test and acceptance test phases.
- Require controlled evidence and risk approval before production authorization.
- Reopen design assurance when change control modifies material assumptions.

### 14.4 DevOps / continuous delivery

- Automate low-latency controls where they are reliable.
- Keep policy and workflow version-controlled.
- Separate build, sign and deploy permissions.
- Apply risk-based release policy without bypassing human approval for consequential exceptions.
- Monitor production and feed incidents, vulnerabilities and operational data into engineering.

## 15. Step-by-step SSDLC implementation procedure

### 15.1 Purpose and authorization

Purpose: introduce or improve an SSDLC using existing product and engineering governance. Obtain sponsor approval from the engineering/product leadership and identify the owner authorized to define release policy. This procedure does not authorize production testing or changes.

### 15.2 Scope and prerequisites

Prerequisites:
- Named executive or product sponsor.
- Application and service inventory.
- Development methodology and toolchain inventory.
- Initial data and system criticality information.
- Current security policies and release processes.
- Security, engineering, QA, platform, operations and privacy stakeholders.

Stop and escalate if there is no risk owner, if a material application cannot be identified, or if a proposed policy conflicts with legal/contractual obligations and no authority can resolve it.

### 15.3 Implementation steps

1. **Inventory products.** Record business owner, technical owner, repositories, runtime, APIs, data classes, suppliers, criticality and exposure.
2. **Assign tiers.** Score the risk dimensions in Section 4. Document the rationale and approval.
3. **Define a baseline.** Select applicable ASVS requirements, organization policies and legal controls. Record the version and selection rationale.
4. **Create lifecycle gates.** Define entry, exit, evidence and decision rights for each stage.
5. **Build the requirement library.** Provide reusable requirements for identity, authorization, data, API, secrets, logging, resilience and supply chain.
6. **Establish secure patterns.** Provide maintained templates, libraries, service examples and approved configuration.
7. **Integrate tools.** Start with source/dependency/secret and infrastructure checks; configure ownership, severity policy and false-positive review.
8. **Establish design review.** Define threat-model triggers, participants and templates for critical and high-risk changes.
9. **Define verification depth.** Map risk tier to code review, automated checks, manual tests and independent assessment.
10. **Set release policy.** Define blocking thresholds, emergency path, evidence and authorized acceptance.
11. **Set exception governance.** Establish owner, expiry, review, interim safeguards and retest process.
12. **Operationalize PSIRT.** Establish reporting channels, triage, service levels, customer communication and regulator notification decision support.
13. **Train teams.** Provide role-specific training and example fixes; measure adoption through code and evidence quality.
14. **Pilot.** Select a representative application, run the process, record friction and measure false positives and time cost.
15. **Improve and scale.** Adjust requirements and policy based on pilot evidence; roll out by application tier.
16. **Assure.** Sample applications and releases to verify the SSDLC is operating, not merely documented.

### 15.4 Expected outputs

- Product/application inventory and risk tiers.
- Security requirements catalogue.
- Approved lifecycle gate and release policy.
- Threat-model and design-review records.
- Secure coding and code-review standards.
- Pipeline policy and tool ownership.
- Verification plans and evidence.
- Exception and remediation registers.
- PSIRT process and operational escalation paths.
- Training plan and effectiveness metrics.
- Management dashboard and improvement backlog.

### 15.5 Closure criteria

The programme rollout is accepted only when an independent sample demonstrates that requirements are present, gates are executed, evidence is retained, findings are owned, exceptions are time-bound and release decisions are made by the correct authority. A policy published without sampled operation is not sufficient evidence.

## 16. Metrics and programme effectiveness

| Metric | Definition | Useful segmentation |
|---|---|---|
| Tier coverage | Percentage of active applications with an approved risk tier | Business unit, product criticality |
| Requirements coverage | Applicable security requirements with owners and verification methods | Tier, requirement category |
| Threat-model freshness | Critical applications with reviewed models within policy interval and after material changes | Application, architecture change |
| Gate execution rate | Releases with required security gate evidence | Tier, release type |
| Pre-production remediation rate | Validated findings fixed before release | Severity, class, team |
| Mean time to remediate | Time from confirmed finding to verified closure | Exploited, reachable, severity, exposure |
| Exception exposure | Open and expired exceptions and cumulative time beyond due date | Risk owner, control, application |
| Repeat finding rate | Findings recurring from the same root cause | CWE, team, control family |
| Pipeline signal quality | Actionable findings / total findings reviewed | Tool and rule set |
| Security test coverage | Critical abuse cases with executed positive and negative tests | Endpoint, workflow, role, tenant |
| PSIRT readiness | Time to acknowledge, triage, contain and issue corrective action | Product, severity, jurisdiction |
| Developer enablement | Training effectiveness and secure fix adoption | Team, language, weakness class |

Do not optimize for a low number of findings or low release-block rate in isolation. Those metrics may reflect weak detection. Measure coverage, recurrence, remediation and control effectiveness together.

## 17. Standards and regulatory alignment

| Source | Relationship to this chapter | Mapping caveat |
|---|---|---|
| NIST SP 800-218 SSDF v1.1 | Strong lifecycle alignment through organization preparation, software protection, secure production and vulnerability response | Map exact practices and tasks; framework is high-level |
| OWASP ASVS 5.0.0 | Supplies testable application security requirements for design and verification | Select by system risk and relevant components |
| OWASP SAMM | Supports maturity assessment of the software assurance programme | Maturity does not prove product security |
| Qatar NIA v2.1, SS 1–7 | Explicitly addresses SDLC integration, classification, requirements, environment separation, pre-production assurance and secure coding | Establish organization and certification/regulatory applicability |
| Saudi NCA ECC 2:2024 | Governance and project-management context; web-app security requirements under 2-15-1 and 2-15-2 | Applies to defined entity scope; use current NCA publication |
| EU Cyber Resilience Act | Product vulnerability lifecycle and manufacturer obligations; Article 14 reporting from 2026-09-11 | Applies to in-scope products and economic operators |
| PCI DSS v4.0.1 | Secure software development and payment-system assurance where applicable | Determine cardholder data scope and contractual/acquirer role |
| GDPR Article 25 and 32 | Privacy by design/default and security of processing when GDPR applies | Requires entity, processing and risk assessment |

## 18. Real-world business use cases

### 18.1 Composite SaaS product team

A small engineering team operates a multi-tenant learning platform. The platform has a React front end, .NET API, relational database, identity provider and cloud-hosted background workers.

The team starts with an application inventory, data classification and risk tier. A new reporting feature adds bulk export and a new tenant-admin permission. The change triggers an architecture update and threat-model review because it modifies data access and privilege scope. Requirements specify tenant filtering, export limits, audit logging and negative authorization tests. Pull requests run static analysis, secret scanning and dependency checks. The release requires manual tests using synthetic users from two tenants, review of the export flow and a risk decision for any unresolved finding. Operations monitor large export activity and privileged report generation.

This scenario illustrates lifecycle integration. It is not presented as a verified customer incident.

### 18.2 Acquired application

A business purchases a vendor-hosted case-management platform. The supplier's SOC report and penetration-test summary do not establish that the customer's configuration, role model, integration or data use is safe. The procurement process identifies the data processor, contract terms, support and vulnerability disclosure process, tenant isolation evidence, identity integration and export controls. The customer verifies its own SSO configuration, administrator access, audit logs, API tokens and data flows. The risk owner records residual supplier and shared-responsibility risk.

### 18.3 Product with digital elements

A manufacturer ships software to EU customers. The product security team establishes supported versions, vulnerability intake, security update process, coordinated disclosure and reporting responsibilities. A confirmed actively exploited vulnerability triggers a discovery timestamp, product impact assessment, mitigations, Article 14 reporting assessment and controlled customer notification process. Legal review confirms the manufacturer's role, scope and exact regulatory obligation before submission.

## 19. Limitations

This model is technology-neutral and must be tailored to the organization's size, risk, delivery model, product type and legal obligations. The risk tiers are illustrative. Exact severity thresholds, remediation SLAs, approval roles and testing frequencies must be established by organizational policy. A tool deployment is not proof of SSDLC operation.

## 20. References

1. NIST SP 800-218 SSDF v1.1: https://csrc.nist.gov/pubs/sp/800/218/final
2. NIST SSDF project and revision status: https://csrc.nist.gov/Projects/ssdf
3. OWASP ASVS 5.0.0: https://asvs.owasp.org/
4. OWASP SAMM: https://owaspsamm.org/
5. Qatar NCSA National Information Assurance Standard v2.1: https://assurance.ncsa.gov.qa/sites/default/files/publications/policy/2023/NCSA_CSGA_%20National_Information_Assurance_Standard_En_V2.1_0.pdf
6. Saudi NCA ECC 2:2024: https://cdn.nca.gov.sa/api/files/public/upload/86e09090-44e4-481f-bc28-355673607654_ECC--2024-EN.pdf
7. EU Cyber Resilience Act, Regulation (EU) 2024/2847: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847
8. PCI SSC Document Library: https://www.pcisecuritystandards.org/document_library/
9. GDPR, Regulation (EU) 2016/679: https://eur-lex.europa.eu/eli/reg/2016/679/oj

## 21. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial Secure SDLC and Product Security operating model |
