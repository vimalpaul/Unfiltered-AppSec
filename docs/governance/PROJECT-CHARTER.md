# Project Charter: Unfiltered AppSec

| Field | Value |
|---|---|
| Document ID | UAPPSEC-GOV-001 |
| Status | Draft baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Application and product security across the software lifecycle, technologies and jurisdictions |
| Classification | Public |

## 1. Mission and intended outcomes

Unfiltered AppSec will provide a connected reference and practical operating system for application security. It will help readers make security decisions, engineer controls, validate implementation, manage vulnerabilities and demonstrate assurance.

The knowledge base is intended to support five outcomes:

1. **Understand:** explain architecture, threats, failure modes, security principles and regulatory context.
2. **Design:** convert business and data risks into system requirements, trust boundaries, threat models and secure design decisions.
3. **Build:** implement secure patterns in application code, infrastructure, identity, data handling and delivery pipelines.
4. **Verify and operate:** test controls, collect evidence, detect abuse, respond to vulnerabilities and recover safely.
5. **Govern and improve:** map controls to obligations, evaluate maturity, track risk and improve engineering outcomes.

## 2. Project scope

### In scope

- Application, product, API, mobile and cloud-native security.
- Secure architecture, threat modeling and abuse-case engineering.
- Secure software development lifecycle (SSDLC), secure coding and code review.
- Identity, authentication, authorization, session and secrets security.
- Data, privacy, cryptography and key management.
- Application security testing and verification.
- Open-source and commercial software supply-chain security.
- Vulnerability handling, coordinated disclosure and product security incident response.
- Application telemetry, detection, incident response and resilience.
- Artificial intelligence (AI), large language model (LLM) and agent-integrated application security.
- Standards, framework mappings, global regulatory research and sector-specific use cases.
- Safe hands-on labs, professional templates, technical diagrams and governed AI workflows.

### Out of scope unless separately authorized

- Testing or exploitation of real third-party systems.
- Storage or publication of confidential client evidence.
- Legal opinions, certification decisions or claims of organizational compliance.
- Vendor endorsement or claims that a tool alone establishes security.
- Uncontrolled production changes by automated agents.
- Operational technology or infrastructure playbooks unrelated to application/product security, except where an application boundary or integration requires the relationship to be documented.

## 3. Audience and assumed knowledge

The content will be layered:

- **Foundation:** terminology, architecture, web and software fundamentals.
- **Practitioner:** implementation, configuration, reproducible testing and troubleshooting.
- **Advanced:** exploit mechanics in isolated labs, complex trust boundaries, distributed systems and attack-path analysis.
- **Architecture and leadership:** risk, control ownership, investment, assurance, operating models and governance.
- **Audit and regulatory:** evidence, mappings, jurisdiction, applicability and limitations.

A chapter must state prerequisites. Specialized chapters must not assume all readers have the same development language or cloud platform.

## 4. Technology coverage

The project is technology-neutral. Examples will be implemented using representative patterns rather than treating one vendor stack as universal. Technology chapters will record versions, deployment assumptions and end-of-life considerations. Illustrative examples may include Java/Spring, .NET, Node.js/TypeScript, Python, browser front ends, Android, iOS, SQL and NoSQL data stores, API gateways, identity providers, public cloud platforms, containers and Kubernetes.

No production design should be copied without environment-specific threat modeling and validation.

## 5. Geographic and regulatory scope

Coverage is global, not restricted to one market. Initial research priorities are:

- India: Information Technology Act and applicable rules, CERT-In directions, Digital Personal Data Protection Act and Rules, and sector regulators where relevant.
- Qatar: National Information Assurance Standard and applicable personal-data and sector requirements.
- Saudi Arabia: National Cybersecurity Authority controls, applicable sector regulators and personal-data requirements.
- United Arab Emirates: federal personal-data protection regime and distinct financial free-zone and sector regimes.
- European Union: GDPR, NIS2, Digital Operational Resilience Act (DORA), Cyber Resilience Act (CRA), and AI Act where applicable.
- United Kingdom, United States, Canada, Singapore, Australia, Brazil, Japan and South Africa as additional jurisdiction workstreams.

Legal applicability must be determined by establishment, offering, processing, sector, criticality, contracts and other statutory tests. Geographic presence alone is insufficient.

## 6. Operating model

The knowledge base will be maintained as version-controlled Markdown with Mermaid diagrams and structured registers. Supporting spreadsheets, lab code and other assets may be added when they improve the usability of the knowledge base.

Each chapter has:
- A document identifier and accountable content owner.
- A declared scope, audience, prerequisites and dependencies.
- A source register and date of research.
- A status: Planned, In progress, Draft baseline, In review, Complete, or Needs refresh.
- A quality review against the project scorecard.
- Cross-references to related threats, requirements, controls, tests, evidence and obligations.

A chapter is not marked Complete because it was created. Completion requires substantive content, reliable sources, consistent mappings, actionable implementation and validation, working navigation, safe examples and a documented review.

## 7. Security and publication model

The GitHub repository is public. Public content must not contain credentials, secrets, private customer information, personal data, internal production addresses, exploitable non-public findings or confidential diagrams. Synthetic data and clearly labelled fictional scenarios are the default.

Real-world testing material must be written for authorized use. Labs should be isolated and include a teardown. Any agent workflow that performs consequential actions must have least privilege, explicit scope, independent validation, audit logs and human approval.

## 8. Definition of done

A substantial chapter is ready for publication when:
- The purpose and applicability are clear.
- Technical depth is sufficient for the intended practitioner.
- Architecture, data flows and trust boundaries are accurate and diagrammed where useful.
- Threats connect to business impact, requirements and controls.
- Implementation and verification steps are reproducible in an authorized environment.
- Evidence, remediation and closure criteria are defined.
- Standards and legal references identify exact editions and limitations.
- Use cases are accurately labelled.
- Sources are current and traceable.
- Internal links and diagrams are checked.
- No sensitive material is present.
- Status, assumptions, gaps and maintenance triggers are explicit.

## 9. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial project charter and scope established |
