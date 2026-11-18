# Repository Architecture and Build Roadmap

| Field | Value |
|---|---|
| Document ID | UAPPSEC-GOV-002 |
| Status | Draft baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Classification | Public |

## 1. Architecture principles

The repository is arranged around the application security lifecycle and the dependencies between engineering disciplines. The chapter sequence is not a linear claim that security happens once. Secure design, implementation, verification and operations form a feedback loop.

The information architecture follows these principles:

1. **Lifecycle coverage:** discovery, design, build, release, deployment, operation, maintenance and retirement.
2. **Separation of concerns:** foundational concepts, technology-specific playbooks, assurance, regulation, labs and templates have separate homes.
3. **Traceability:** threats connect to requirements, controls, tests, evidence and obligations.
4. **Technology neutrality:** common engineering principles are separated from implementation-specific instructions.
5. **Version awareness:** standards, platform guidance, tools and laws are identified by version and status.
6. **Usefulness over volume:** no empty placeholder chapters and no duplicated encyclopedic copy.
7. **Safety:** practical instructions default to isolated labs and authorized systems.
8. **Maintainability:** each significant topic has a clear owner, status, source base and review trigger.

## 2. Repository tree

The target structure is:

~~~text
/
├── README.md
├── CONTRIBUTING.md
├── docs/
│   ├── governance/
│   ├── 01-fundamentals/
│   ├── 02-architecture-threat-modeling/
│   ├── 03-secure-sdlc-product-security/
│   ├── 04-secure-coding-code-review/
│   ├── 05-web-application-security/
│   ├── 06-api-service-security/
│   ├── 07-identity-access-security/
│   ├── 08-data-privacy-cryptography/
│   ├── 09-mobile-application-security/
│   ├── 10-cloud-native-application-security/
│   ├── 11-distributed-systems-integration/
│   ├── 12-ai-llm-application-security/
│   ├── 13-software-supply-chain/
│   ├── 14-security-verification-assessment/
│   ├── 15-vulnerability-management-psirt/
│   ├── 16-appsec-operations-incident-response/
│   ├── 17-devsecops-tooling/
│   ├── 18-standards-frameworks/
│   ├── 19-global-regulatory/
│   ├── 20-industry-use-cases/
│   ├── 21-labs-exercises/
│   ├── 22-templates-deliverables/
│   ├── 23-ai-agents-automation/
│   └── 24-glossary-indexes/
├── labs/
│   ├── local-environments/
│   ├── web/
│   ├── api/
│   ├── mobile/
│   ├── cloud-native/
│   └── ai-security/
├── templates/
│   ├── architecture/
│   ├── assessment/
│   ├── governance/
│   └── operations/
├── references/
│   ├── source-register.md
│   ├── standards-register.md
│   └── regulatory-register.md
└── .github/
    ├── ISSUE_TEMPLATE/
    └── workflows/
~~~

Directories will be created when the first meaningful file is ready. A directory without content is not a deliverable.

## 3. Chapter specifications and dependencies

| Chapter | Purpose and required deliverables | Depends on |
|---|---|---|
| 00 Governance and Methodology | Project charter, scope, research protocol, source quality, architecture, QA gates, status and contribution rules | None |
| 01 AppSec Fundamentals | Security objectives, risk concepts, lifecycle, core terminology, control model and AppSec operating concepts | 00 |
| 02 Architecture and Threat Modeling | Reference architecture, DFDs, trust-boundary analysis, threat enumeration, abuse cases, design review workflow | 01 |
| 03 Secure SDLC and Product Security | Product security operating model, roles, security requirements, lifecycle gates, exceptions and maturity | 01, 02 |
| 04 Secure Coding and Code Review | Language-specific threat patterns, defensive coding, review workflow and examples | 01, 03 |
| 05 Web Application Security | HTTP and browser security, server/client controls, browser boundaries, business logic and test methods | 01, 02, 04, 07, 08 |
| 06 API and Service Security | API architecture, authz, object/property/function controls, protocol-specific testing and API inventory | 02, 05, 07, 08 |
| 07 Identity and Access Security | Identity lifecycle, authentication, authorization, sessions, tokens and federation | 02, 05, 06 |
| 08 Data Security and Privacy Engineering | Data lifecycle, classification, minimization, cryptography, privacy controls and deletion | 01, 02 |
| 09 Mobile Application Security | Platform architecture, local data, application components, inter-process communication and mobile testing | 02, 07, 08 |
| 10 Cloud-Native Application Security | Cloud organization and landing zones, human/workload IAM, provider control planes, container images/runtime, Kubernetes, serverless, managed services, IaC, CI/CD, observability and recovery | 02, 07, 08, 13, 17 |
| 11 Distributed Systems and Integration Security | Microservices, events, queues, service-to-service auth, webhooks and trust delegation | 02, 06, 07, 10 |
| 12 AI and LLM Application Security | AI-specific threat models, model/data/tool boundaries, RAG, agent execution and model supply chain | 02, 08, 11, 13, 23 |
| 13 Software Supply Chain Security | Dependency governance, SBOM, provenance, build integrity, signing and supplier risk | 03, 10, 17 |
| 14 Security Verification and Assessment | Test strategy, ASVS-derived requirements, SAST/DAST/IAST/SCA, manual assessment and evidence | 03–13 |
| 15 Vulnerability Management and PSIRT | Intake, triage, exploitability, severity, coordinated disclosure, patch and advisory lifecycle | 03, 13, 14, 16 |
| 16 AppSec Operations and Incident Response | Telemetry, detection, investigation, containment, recovery, evidence preservation and learning | 05–15 |
| 17 DevSecOps and Security Tooling | Pipeline security architecture, tool evaluation, automation, policy-as-code and operating procedures | 03, 04, 13, 14 |
| 18 Standards and Frameworks | Exact editions, control mapping, rationale, coverage gaps and audit evidence | 01–17 |
| 19 Global Regulatory and Jurisdiction Mapping | Country-specific laws and regulator controls with applicability analysis | 01–18 |
| 20 Industry and Business Use Cases | Industry architectures, risk patterns, controls, evidence and scenario-specific obligations | 01–19 |
| 21 Labs and Practical Exercises | Isolated environments, setup, scenarios, test instructions, expected results and teardown | Relevant technical chapter |
| 22 Templates and Professional Deliverables | Reusable inventories, threat models, plans, reports, risk records and evidence packs | 02–20 |
| 23 AI Agents and Automation | Governed architecture, tool permission models, approvals, logging, evaluation and emergency disable | 03, 12, 17 |
| 24 Glossary, Taxonomy and Master Indexes | Canonical vocabulary, source index and cross-chapter traceability | All chapters |

## 4. Cross-chapter traceability model

Every major control or security requirement should be traceable through the following chain:

~~~mermaid
flowchart TD
    B[Business objective and obligations] --> A[Application and data architecture]
    A --> T[Threats and abuse cases]
    T --> R[Risk statement and owner]
    R --> Q[Security requirement]
    Q --> C[Preventive, detective and recovery controls]
    C --> I[Implementation and configuration]
    I --> V[Verification and tests]
    V --> E[Evidence and residual risk]
    E --> O[Operations, monitoring and response]
    O --> G[Governance, review and improvement]
    G --> B
~~~

The traceability key should be stable, for example:
- Requirement: REQ-AUTHZ-004
- Threat: THR-TENANT-002
- Control: CTRL-AUTHZ-007
- Test: TEST-API-BOLA-003
- Evidence: EVD-REL-2026-014
- Risk: RISK-DATA-021
- Obligation: REG-EU-CRA-ART14-001

IDs in examples are illustrative and must not be mistaken for an official external control identifier.

## 5. Build sequence

### Phase 0: Governance and research foundation
- Confirm repository ownership, branch and access.
- Establish charter, scope, chapter architecture, research method, status tracking and contribution rules.
- Build the authoritative source and standards registers.
- Define metadata, IDs, labels and quality gates.

### Phase 1: Core engineering foundation
1. AppSec fundamentals and security objectives.
2. Application architecture, data flows and trust boundaries.
3. Threat modeling, abuse cases and security design reviews.
4. Secure SDLC and product security operating model.
5. Security requirements and risk treatment.

### Phase 2: Core application engineering
1. Web security and browser controls.
2. API and service security.
3. Identity, authentication, authorization and session management.
4. Data security, privacy engineering and cryptography.
5. Secure coding and code review.

### Phase 3: Platform and emerging application patterns
1. Mobile application security.
2. Cloud-native, containers, Kubernetes and serverless.
3. Distributed systems, event-driven workflows and integrations.
4. AI/LLM application and agent security.
5. Software supply chain and build integrity.

### Phase 4: Verification and operational lifecycle
1. Security testing strategy and detailed test procedures.
2. SAST, DAST, IAST, SCA, secrets, IaC and container scanning.
3. Penetration testing and verification evidence.
4. Vulnerability management, disclosure and PSIRT.
5. Security telemetry, incident response and recovery.

### Phase 5: Assurance and sector context
1. Standards and framework crosswalks.
2. Regulatory research, jurisdiction by jurisdiction.
3. Sector-specific use cases and control profiles.
4. Audit evidence and professional deliverables.

### Phase 6: Labs and automation
1. Isolated labs aligned to chapters.
2. Reproducible assessment worksheets and answer keys.
3. Governed AI workflows and agent evaluations.
4. Repository-wide validation, gap register and release process.

## 6. Initial scope boundaries and assumptions

- The first release establishes the global architecture; it does not assert that every jurisdiction or technology is already researched.
- Regulatory research records obligations and technical implications, but applicability remains entity-specific.
- The project will use stable published versions as baselines and maintain a separate watchlist for drafts and proposed changes.
- The initial public repository contains no client material.
- Tool recommendations will include prerequisites, intended use, limitations, licensing and operational fit; tools will not be treated as substitutes for engineering controls.
- Practical exploitation content will be confined to authorized assessment procedures and isolated labs.

## 7. Milestone acceptance

A phase can be closed only when all deliverables for that milestone are committed, cross-referenced, checked and reflected in the status register. Missing content is recorded as a gap, not concealed by a completion percentage.
