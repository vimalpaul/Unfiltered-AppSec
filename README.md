# Unfiltered AppSec Knowledge Base

**Project identity:** Unfiltered AppSec  
**Repository:** https://github.com/vimalpaul/Unfiltered-AppSec  
**Knowledge-base release:** 0.1 foundation  
**Research cut-off for this baseline:** 18 November 2026  
**Status:** Foundation established; domain chapters in staged development  
**Classification:** Public repository. Do not commit customer-confidential, personal, credential, exploit-target or non-public architecture data.

## Mission

Unfiltered AppSec is a practitioner-grade, evidence-led application security engineering knowledge base. It connects secure architecture and product requirements to implementation, verification, vulnerability handling, operational readiness, governance and continuous improvement.

It is designed to be used as an engineering reference and an actionable playbook library by application security engineers, developers, security architects, product security teams, DevSecOps practitioners, penetration testers, technology leaders, auditors, consultants, researchers and trainers.

This is not a vulnerability list, a web-pentest-only manual, or a compliance checklist. Its organizing model is:

**Business context → Systems and architecture → Assets and data → Threats and weaknesses → Risk → Requirements → Controls → Implementation → Verification → Evidence → Operations → Governance → Continuous improvement.**

## Scope

The knowledge base covers the full application and product security lifecycle across:

- Web applications, browser clients and server-rendered applications.
- APIs, GraphQL, REST, gRPC, webhooks and service-to-service interfaces.
- Mobile applications and mobile backends.
- Identity, authentication, authorization, federation, sessions and secrets.
- Application architecture, threat modeling, secure design and security requirements.
- Secure SDLC, secure coding, code review and developer enablement.
- Cloud-native applications, containers, Kubernetes, serverless and microservices.
- Data protection, cryptography, privacy engineering and secure storage.
- Software supply chain, open-source dependencies, build systems, CI/CD and provenance.
- Application testing, penetration testing, verification, vulnerability management and product security incident response.
- Security logging, detection, response, recovery and product security operations.
- AI-enabled applications, LLM integrations, retrieval-augmented generation and agentic application workflows.
- Standards, regulatory obligations, sector use cases, labs, templates and governed automation.

Coverage is technology-neutral. Practical examples will use representative stacks such as Java/Spring, .NET, Node.js/TypeScript, Python, React, common relational and NoSQL databases, cloud services and mobile platforms. Examples are illustrative unless explicitly labelled as verified public incidents.

Geographic scope is global. Dedicated workstreams will cover India and Middle Eastern jurisdictions, including Qatar, Saudi Arabia, the United Arab Emirates and other GCC countries individually. A regional label never substitutes for country-specific legal analysis.

## How to use the knowledge base

1. Start with [Project Charter](docs/governance/PROJECT-CHARTER.md) and [Architecture and Roadmap](docs/governance/REPOSITORY-ARCHITECTURE-AND-ROADMAP.md).
2. Review [Project Status](docs/governance/PROJECT-STATUS.md) to find the last verified milestone and next planned chapter.
3. Use the chapter relevant to the system or decision being engineered. Follow the cross-references to requirements, threats, tests, evidence and regulatory obligations.
4. For implementation, use a procedure and its prerequisites, authorization, stop conditions, expected observations, evidence, remediation and retest criteria. Do not treat an overview as an execution procedure.
5. For assurance, use the exact edition and source identifier in the standards and regulatory registers. A crosswalk is not a legal opinion, an audit result or proof of compliance.
6. For practical work, use isolated labs and synthetic data. Real testing requires documented authorization and agreed rules of engagement.

## Knowledge architecture

| ID | Chapter | Primary contents | Status |
|---|---|---|---|
| 00 | Governance and Methodology | Charter, scope, architecture, quality gates, research method, status, contribution and safety | Foundation created |
| 01 | AppSec Fundamentals | Core concepts, risk model, security objectives, lifecycle and terminology | Foundation chapter drafted |
| 02 | Architecture and Threat Modeling | Reference architecture, trust boundaries, data flows, STRIDE, abuse cases and design review | Foundation chapter drafted |
| 03 | Secure SDLC and Product Security | Security governance in delivery, security gates, requirements, roles and maturity | Draft baseline created |
| 04 | Secure Coding and Code Review | Language-specific secure coding, patterns, anti-patterns, review methods | Draft baseline and lab pack created |
| 05 | Web Application Security | Browser, HTTP, server-side, client-side, business logic and web control engineering | Draft baseline and lab pack created |
| 06 | API and Service Security | REST, GraphQL, gRPC, webhooks, API lifecycle and service authorization | Draft baseline and lab pack created |
| 07 | Identity and Access Security | Authentication, authorization, sessions, OAuth, OIDC, SAML, MFA and IAM | Draft baseline and lab pack created |
| 08 | Data Security and Privacy Engineering | Classification, minimization, cryptography, key management, retention and privacy | Draft baseline and lab pack created |
| 09 | Mobile Application Security | Android, iOS, local storage, IPC, platform controls and backend integration | Draft baseline and lab pack created |
| 10 | Cloud-Native Application Security | Cloud IAM, workload identity, containers, Kubernetes, serverless, IaC, CI/CD and runtime | Draft baseline and lab pack created |
| 11 | Distributed Systems and Integration Security | Workload identity, service authorization, service mesh, Kafka/RabbitMQ, events, replay, idempotency, sagas, webhooks and partner integrations | Draft baseline and lab pack created |
| 12 | AI and LLM Application Security | Prompt injection, RAG, vector security, tool calling, agents, MCP, model supply chain, privacy and AI operations | Draft baseline and lab pack created |
| 13 | Software Supply Chain Security | Dependencies, SBOM, provenance, signing, build security and supplier assurance | Planned |
| 14 | Security Verification and Assessment | SAST, DAST, IAST, SCA, manual testing, penetration tests and assurance | Planned |
| 15 | Vulnerability Management and PSIRT | Intake, triage, severity, disclosure, remediation, patching and product advisories | Planned |
| 16 | AppSec Operations and Incident Response | Security telemetry, detection, incident handling, forensics and recovery | Planned |
| 17 | DevSecOps and Security Tooling | CI/CD architecture, policy-as-code, tool selection, integration and operations | Planned |
| 18 | Standards and Frameworks | OWASP, NIST, ISO/IEC, PCI DSS, CIS and traceable control mappings | Baseline register created |
| 19 | Global Regulatory and Jurisdiction Mapping | Country-specific laws, regulators, scope, applicability and technical implications | Initial jurisdictions researched |
| 20 | Industry and Business Use Cases | Finance, health, government, SaaS, retail, telecom, critical services and suppliers | Planned |
| 21 | Labs and Practical Exercises | Safe labs, scenarios, evidence, answer keys and learning assessments | Planned |
| 22 | Templates and Professional Deliverables | Inventories, threat models, requirements, plans, reports, registers and evidence | Planned |
| 23 | AI Agents and Automation | Governed agent patterns, retrieval, tool boundaries, approvals and evaluation | Planned |
| 24 | Glossary, Taxonomy and Master Indexes | Canonical terms, threat/control/test mappings, source catalogue and index | Planned |

Detailed scope and dependencies are maintained in [REPOSITORY-ARCHITECTURE-AND-ROADMAP.md](docs/governance/REPOSITORY-ARCHITECTURE-AND-ROADMAP.md).

## Project governance

- [Project Charter](docs/governance/PROJECT-CHARTER.md)
- [Architecture and Roadmap](docs/governance/REPOSITORY-ARCHITECTURE-AND-ROADMAP.md)
- [Research and Quality Method](docs/governance/RESEARCH-AND-QUALITY-METHOD.md)
- [Project Status and Continuity Register](docs/governance/PROJECT-STATUS.md)

## Current foundational chapters

- [01. Application Security Fundamentals](docs/01-fundamentals/APPSEC-FUNDAMENTALS.md)
- [02. Application Architecture and Trust Boundaries](docs/02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [03. Secure SDLC and Product Security](docs/03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [04. Secure Coding and Code Review](docs/04-secure-coding/SECURE-CODING-AND-CODE-REVIEW.md)
- [05. Web Application Security Engineering](docs/05-web-application-security/WEB-APPLICATION-SECURITY-ENGINEERING.md)
- [05. Web Application Security Lab Pack](docs/05-web-application-security/WEB-APPLICATION-SECURITY-LAB-PACK.md)
- [06. API and Service Security Engineering](docs/06-api-service-security/API-AND-SERVICE-SECURITY-ENGINEERING.md)
- [06. API and Service Security Lab Pack](docs/06-api-service-security/API-AND-SERVICE-SECURITY-LAB-PACK.md)
- [08. Data Security and Privacy Engineering](docs/08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-ENGINEERING.md)
- [08. Data Security and Privacy Lab Pack](docs/08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-LAB-PACK.md)
- [09. Mobile Application Security Engineering](docs/09-mobile-application-security/MOBILE-APPLICATION-SECURITY-ENGINEERING.md)
- [09. Mobile Application Security Lab Pack](docs/09-mobile-application-security/MOBILE-APPLICATION-SECURITY-LAB-PACK.md)
- [10. Cloud-Native Application Security Engineering](docs/10-cloud-native-application-security/CLOUD-NATIVE-APPLICATION-SECURITY-ENGINEERING.md)
- [10. Cloud-Native Application Security Lab Pack](docs/10-cloud-native-application-security/CLOUD-NATIVE-APPLICATION-SECURITY-LAB-PACK.md)
- [11. Distributed Systems and Integration Security Engineering](docs/11-distributed-systems-integration-security/DISTRIBUTED-SYSTEMS-AND-INTEGRATION-SECURITY-ENGINEERING.md)
- [11. Distributed Systems and Integration Security Lab Pack](docs/11-distributed-systems-integration-security/DISTRIBUTED-SYSTEMS-AND-INTEGRATION-SECURITY-LAB-PACK.md)
- [12. AI and LLM Application Security Engineering](docs/12-ai-llm-application-security/AI-AND-LLM-APPLICATION-SECURITY-ENGINEERING.md)
- [12. AI and LLM Application Security Lab Pack](docs/12-ai-llm-application-security/AI-AND-LLM-APPLICATION-SECURITY-LAB-PACK.md)
- [07. Identity and Access Security](docs/07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY.md)
- [07. Identity and Access Security Lab Pack](docs/07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY-LAB-PACK.md)
- [04. Secure Coding Lab Pack](docs/04-secure-coding/SECURE-CODING-LAB-PACK.md)
- [Standards Baseline and Mapping Method](docs/18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md)
- [Global Regulatory Register](docs/19-global-regulatory/GLOBAL-REGULATORY-REGISTER.md)

## Source and evidence discipline

The master [Authoritative Source Register](references/source-register.md) records the initial primary sources, editions and evidence grades.

Important claims must be traceable to primary sources where possible. Sources are graded A through D based on authority and evidentiary strength. Each mapping identifies the exact edition or legal instrument, its scope, applicability conditions, relationship to the target control and limitations.

The baseline source catalogue includes the stable OWASP ASVS 5.0.0 release, OWASP Top 10:2025, OWASP API Security Top 10:2023, NIST SP 800-218 SSDF 1.1 and its later draft revision, NIST CSF 2.0, PCI DSS 4.0.1, and jurisdiction-specific primary sources. Drafts and final publications are never silently conflated.

## Safety and authorization

All testing instructions are for systems that the practitioner owns or is explicitly authorized to assess. Labs must be isolated, reproducible and populated with synthetic data. Testing against third-party or production systems requires written authorization, defined scope, allowed techniques, testing windows, rate limits, emergency contacts and stop conditions. No customer secrets, credentials, access tokens, production data or private architecture should be committed to this public repository.

## Content status

A file existing does not make a chapter complete. A major chapter must pass the quality gates in the research method and receive a documented status review. Planned chapters are not represented as implemented. Jurisdiction entries are not legal advice and require applicability analysis by qualified counsel or the relevant compliance function.

## Contribution model

Contributions should be precise, sourced, reproducible and safe. See [CONTRIBUTING.md](CONTRIBUTING.md). Every substantial change should update relevant indexes, status, cross-references, source records and revision notes.

## Maintenance

Review dynamic references at least quarterly and sooner when a regulator, standards publisher, vendor or national CERT issues a material update. Trigger a review when a framework revision, vulnerability class, major exploit pattern, legal amendment, platform end-of-life or significant incident changes the assumptions in a chapter.
