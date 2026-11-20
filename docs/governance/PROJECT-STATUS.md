# Project Status and Continuity Register

| Field | Value |
|---|---|
| Document ID | UAPPSEC-GOV-004 |
| Status | Active tracking record |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2026-12-18 |
| Classification | Public |

## 1. Repository baseline

- Repository: https://github.com/vimalpaul/Unfiltered-AppSec
- Default branch: main
- Visibility: Public
- Initial repository inspection: 2026-11-18
- Starting state: empty repository, no files and no commits
- GitHub access: read/write/admin permission confirmed through the connected account
- Existing content preserved: not applicable; initial repository was empty
- Current milestone: Milestone 11 Software Supply Chain Security engineering, lab specifications and initial executable implementation baseline

## 2. Current work state

| Work item | Deliverable | State | Evidence / next action |
|---|---|---|---|
| Repository discovery | Owner, visibility, default branch, permissions, initial tree | Complete | GitHub repository metadata confirmed; repository was empty |
| Project charter | Mission, scope, audience, geographic coverage, safety | Draft baseline created | Review at first governance checkpoint |
| Architecture | Chapter taxonomy, dependencies, traceability and phases | Draft baseline created | Use as canonical chapter map |
| Research method | Evidence grading, mapping rules and QA scorecard | Draft baseline created | Apply to every substantial chapter |
| Continuity register | Completed and pending work tracking | Active | Update after each committed milestone |
| AppSec fundamentals | Security objectives, lifecycle, risk and core concepts | Draft baseline created | Expand with detailed secure SDLC and secure coding chapters |
| Architecture and trust boundaries | Reference system, DFD, threat modeling and design review | Draft baseline created | Add deeper architecture patterns and case studies |
| Source catalogue | Authoritative source inventory and evidence grades | Initial baseline created | `references/source-register.md`; verify source currency at each chapter review |
| Standards baseline | Versioned source and mapping method | Initial baseline created | `docs/18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md`; build detailed clause/control mappings chapter by chapter |
| Global regulatory register | Initial India, Qatar, Saudi Arabia, UAE and EU records | Initial research baseline | `docs/19-global-regulatory/GLOBAL-REGULATORY-REGISTER.md`; expand by country and sector; validate amendments and applicability |
| Secure SDLC | Operating model and lifecycle control implementation | Draft baseline created | `docs/03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md`; expand with implementation-specific pipeline patterns and assurance procedures |
| Secure coding | Language patterns and code review | Draft baseline created | `docs/04-secure-coding/SECURE-CODING-AND-CODE-REVIEW.md`; deepen version-specific framework examples and exact ASVS traceability |
| Secure coding labs | Isolated reproducible exercises and assessment rubric | Draft lab specifications created | `docs/04-secure-coding/SECURE-CODING-LAB-PACK.md`; implement and reproduce containers before marking validated |
| Web application security | Browser, HTTP, server-side, client-side and business logic controls | Draft baseline created | `docs/05-web-application-security/WEB-APPLICATION-SECURITY-ENGINEERING.md`; expand exact ASVS/WSTG mappings and version-specific examples |
| Web application security labs | Isolated reproducible web security exercises | Draft lab specifications created | `docs/05-web-application-security/WEB-APPLICATION-SECURITY-LAB-PACK.md`; implement and validate lab environments before marking complete |
| API and service security | REST, GraphQL, gRPC, webhooks, API authorization and service trust | Draft baseline created | `docs/06-api-service-security/API-AND-SERVICE-SECURITY-ENGINEERING.md`; add exact ASVS IDs and protocol-version-specific implementation profiles |
| API and service security labs | Isolated API protocol, authorization and integration exercises | Draft lab specifications created | `docs/06-api-service-security/API-AND-SERVICE-SECURITY-LAB-PACK.md`; implement and validate lab environments before marking complete |
| Data security and privacy engineering | Data lifecycle, classification, cryptography, key management, privacy, retention and deletion | Draft baseline created | `docs/08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-ENGINEERING.md`; add exact ASVS IDs and jurisdiction-specific legal review |
| Data security and privacy labs | Isolated data lifecycle, encryption, privacy and deletion exercises | Draft lab specifications created | `docs/08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-LAB-PACK.md`; implement and validate environments before marking complete |
| Identity and access security | Authentication, federation, session and authorization | Draft baseline created | `docs/07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY.md`; expand exact ASVS and regulator mappings and version-specific executable examples |
| Identity and access labs | Reproducible identity, federation, authorization and PAM exercises | Draft lab specifications created | `docs/07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY-LAB-PACK.md`; implement and validate isolated environments before marking complete |
| Mobile application security | Android, iOS, hybrid apps, mobile identity, platform storage, IPC, deep links, WebViews, release assurance and backend integration | Draft baseline created | `docs/09-mobile-application-security/MOBILE-APPLICATION-SECURITY-ENGINEERING.md`; align exact control/test IDs to pinned MASVS/MASTG releases and add implementation-specific examples |
| Mobile application security labs | Isolated Android, iOS, cross-platform, backend and release exercises | Draft lab specifications created | `docs/09-mobile-application-security/MOBILE-APPLICATION-SECURITY-LAB-PACK.md`; implement and validate device/emulator environments before marking complete |
| Cloud-native application security | Cloud governance, IAM, workload identity, network, containers, Kubernetes, serverless, IaC, CI/CD, monitoring and recovery | Draft baseline created | `docs/10-cloud-native-application-security/CLOUD-NATIVE-APPLICATION-SECURITY-ENGINEERING.md`; pin exact provider/CIS versions and validate service-specific implementation profiles |
| Cloud-native application security labs | Isolated cloud, container, Kubernetes, serverless, IaC and CI/CD exercises | Draft lab specifications created | `docs/10-cloud-native-application-security/CLOUD-NATIVE-APPLICATION-SECURITY-LAB-PACK.md`; implement and validate local/cloud environments and cleanup/cost controls before marking complete |
| Distributed systems and integration security | Microservices, workload identity, service authorization, service mesh, brokers, events, webhooks, distributed workflows, third-party integrations and telemetry | Draft baseline created | `docs/11-distributed-systems-integration-security/DISTRIBUTED-SYSTEMS-AND-INTEGRATION-SECURITY-ENGINEERING.md`; validate broker/service-mesh version profiles, add exact standards traceability and reproduce implementation labs |
| Distributed systems and integration security labs | Isolated workload identity, mTLS, broker ACL, event integrity, replay, outbox/inbox, saga, webhook, SSRF, resilience and telemetry exercises | Draft lab specifications created | `docs/11-distributed-systems-integration-security/DISTRIBUTED-SYSTEMS-AND-INTEGRATION-SECURITY-LAB-PACK.md`; implement and independently validate pinned environments before marking complete |
| Software supply-chain implementation | Initial read-only CI baseline, deterministic SHA-256 source integrity manifest, unit tests, release evidence policy and control traceability | Implemented; main-branch CI run passed; PR-triggered validation pending | `implementations/13-software-supply-chain-security/README.md`; `.github/workflows/supply-chain-baseline.yml`; do not describe as SBOM, SLSA provenance, signing or production enforcement |
| AI and LLM application security | Prompt injection, RAG, vector and embedding security, tool authorization, agents, MCP, model/data supply chain, output handling, privacy and operations | Draft baseline created: 46 test cases and 26 detection scenarios | `docs/12-ai-llm-application-security/AI-AND-LLM-APPLICATION-SECURITY-ENGINEERING.md`; verify framework editions, provider-specific behavior and exact AI risk-control traceability |
| AI and LLM application security labs | Isolated prompt injection, cross-tenant RAG, tool/agent, MCP, output, supply-chain, multimodal, privacy and incident-response exercises | Draft specifications created: 30 labs | `docs/12-ai-llm-application-security/AI-AND-LLM-APPLICATION-SECURITY-LAB-PACK.md`; implement and independently validate pinned sandbox environments before marking complete |
| Software supply chain security | Repository governance, developer endpoints, dependencies, registries, CI/CD, runners, SBOM, SCA/VEX, provenance, signing, containers, releases, suppliers and AI assets | Draft engineering baseline created: 23 controls, 35 tests and 28 detection scenarios | `docs/13-software-supply-chain-security/SOFTWARE-SUPPLY-CHAIN-SECURITY-ENGINEERING.md`; validate the expanded NIST SSDF/SLSA v1.2/CISA 2026 mappings, add platform-specific GitHub/GitLab and cloud workload identity implementation profiles, and reproduce build/provenance/signing controls |
| Software supply chain security labs | Isolated repository, registry, dependency, SBOM, runner, OIDC, provenance, signing, container, supplier and incident-response exercises | Draft lab specifications created: 27 labs | `docs/13-software-supply-chain-security/SOFTWARE-SUPPLY-CHAIN-SECURITY-LAB-PACK.md`; implement and independently validate pinned environments before marking complete |
| Labs and templates | Safe reproducible labs and professional templates | Pending | Build alongside technical chapters |
| AI agent workflows | Governed automation design and assessment | Pending | Build after core architecture and agent-security content |

## 3. Version and research watchlist

| Topic | Baseline captured | Status and handling |
|---|---|---|
| OWASP ASVS | 5.0.0 stable, published 2025-05-30 | Use as current stable verification baseline; do not use bleeding-edge as the normative baseline |
| OWASP Top 10 | 2025 final | Use for awareness and risk taxonomy; not as a complete security standard |
| OWASP API Security Top 10 | 2023 edition | Use as API risk awareness taxonomy; not as a complete test specification |
| NIST SSDF | SP 800-218 v1.1 final, 2022 | Published baseline |
| NIST SSDF revision | SP 800-218 Rev. 1 v1.2 draft dated 2025-12-17 | Monitor; do not present as final unless NIST changes the publication status |
| SLSA | v1.2 approved specification, Source and Build tracks | Use separate Source L1–L4 and Build L0–L3 claims; verify normative requirements and evidence per track |
| CISA SBOM Minimum Elements | 2026 joint guidance announced 2026-07-29 | Include component hash, license, SBOM tool name and generation context; assess AI/SaaS-specific fields |
| CycloneDX | 1.7 specification; check current 1.7.x release patch | Pin schema and tool versions; validate consumer interoperability |
| NIST CSF | CSF 2.0, 2024-02-26 | Governance and risk outcome taxonomy; not an AppSec test standard |
| PCI DSS | v4.0.1 | Use where cardholder-data environment and contractual/acquirer applicability exist |
| India DPDP Rules | 2025 Gazette notification and phased commencement | Track phased commencement; re-check corrigendum and current legal status before operational reliance |
| EU CRA | Regulation (EU) 2024/2847 | Article 14 reporting obligations apply from 2026-09-11; general application date 2027-12-11 |
| Qatar NIA | National Information Assurance Standard v2.1, May 2023 | Initial security-development and web-control mapping captured |
| Saudi ECC | ECC 2:2024 | Initial application-security subdomain mapping captured |

## 4. Next work sequence

1. Implement and independently validate Chapter 13 labs in pinned environments; add executable GitHub/GitLab workflow examples, SLSA v1.2 source/build verification profiles, SBOM schema tests and release-policy examples.
2. Expand Chapter 12 with the complete numbered OWASP GenAI LLM Top 10 2026 mapping, Agentic Top 10 ASI01–ASI10 test traceability, ACS runtime-control implementation profiles, current MCP security profiles, provider-specific controls, model artifact and dataset provenance, and repeatable evaluation methodology.
3. Expand Chapter 11 with exact broker-version profiles, service-mesh implementation matrices, protocol-level security requirements and traceable test-to-control mappings.
4. Expand Chapter 10 with provider-specific identity federation, cloud policy, service configuration and exact CIS/provider framework traceability; validate current editions.
5. Expand Chapter 09 with exact MASVS control-to-MASWE-to-MASTG v2 test traceability and pinned platform implementation examples.
6. Expand Chapters 08 and 07 with exact ASVS mappings, cryptographic lifecycle examples and federation implementation profiles.
7. Expand Chapter 06 with exact ASVS mappings, API contract automation and protocol-version-specific GraphQL/gRPC profiles.
8. Implement and reproduce the web, API, identity, data, mobile, cloud-native, distributed-systems, AI/LLM, software supply-chain and secure-coding labs in pinned isolated environments.
9. Expand India and GCC regulatory research into country- and sector-specific records with applicability decision logic.
10. Establish reusable inventories, threat-model, assessment, finding, remediation and evidence templates.
11. Continue standards crosswalks into chapter-specific requirement-to-test mappings.
## 5. Continuity rules

When continuing this project:
- Read this status file and the repository tree first.
- Inspect the most recent relevant commit and chapter before adding content.
- Continue the next pending item in the roadmap.
- Do not recreate or overwrite a completed chapter without a documented reason.
- After each milestone, update this register and the root README if the navigation or status changed.
- Record exact paths, commit SHA, validation performed and unresolved gaps.
- Treat a failed validation as a pending task, not as a success.

## 6. Quality status

The initial architecture and documents are foundation drafts. Their existence demonstrates repository initialization, not final approval or independent technical review. Chapters 04 and 07 include substantive engineering playbooks and lab specifications; lab specifications are not equivalent to executed and independently validated lab environments.

### Preliminary chapter scorecard

Scores use the 0–5 scale defined in the Research and Quality Method. Vectors are ordered as: scope, technical depth, evidence, standards mapping, regulatory mapping, use cases, diagrams, implementation, verification, operations, AI governance, navigation, QA and maintenance.

| Chapter | Scores | Current judgement |
|---|---|---|
| 01 AppSec Fundamentals | 4, 3, 3, 3, 2, 3, 2, 3, 2, 3, N/A (foundational chapter), 4, 2, 3 | Useful baseline; deeper implementation and testing are delegated to specialist chapters |
| 02 Architecture and Trust Boundaries | 4, 4, 3, 2, 2, 3, 4, 3, 3, 3, N/A (AI architecture is a later chapter), 4, 2, 3 | Strong initial design and threat-model foundation; add more patterns, validated labs and exact framework mappings |
| 03 Secure SDLC and Product Security | 4, 4, 3, 3, 3, 3, 3, 4, 4, 4, N/A (agent governance is a later chapter), 4, 2, 3 | Substantive operating model; add concrete pipeline examples, implementation templates and sampled assurance evidence |
| 04 Secure Coding and Code Review | 4, 4, 3, 3, 2, 4, 3, 4, 4, 3, N/A (agent governance is a later chapter), 4, 2, 3 | Broad initial playbook and lab specifications; framework-specific executable examples and ASVS IDs remain to be validated |
| 05 Web Application Security | 4, 4, 3, 3, 2, 4, 4, 4, 4, 4, N/A (agent security is covered in dedicated chapters), 4, 2, 3 | Broad web engineering baseline and lab specifications; exact ASVS/WSTG traceability and executable lab validation remain open |
| 06 API and Service Security | 4, 4, 4, 3, 2, 4, 4, 4, 4, 4, N/A (agent security is covered in dedicated chapters), 4, 2, 3 | Broad protocol and authorization engineering baseline with lab specifications; exact ASVS traceability and executable lab validation remain open |
| 13 Software Supply Chain Security | 4, 4, 4, 4, 2, 4, 3, 4, 3, 4, 3, 4, 2, 3 | Broad source, dependency, CI/CD, SBOM, provenance, signing, container, supplier and AI asset baseline with 23 controls, 35 tests, 28 detections and 27 lab specifications; provider-specific profiles and independent lab validation remain open |
| 12 AI and LLM Application Security | 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4, 2, 3 | Broad LLM, RAG, vector, agent/tool, MCP, model supply-chain and privacy baseline with 46 test cases, 26 detection scenarios and 30 lab specifications; full OWASP LLM 2026 numbered mapping, provider-specific validation and independently executed labs remain open |
| 11 Distributed Systems and Integration Security | 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, N/A (AI/agent security is a later chapter), 4, 2, 3 | Broad microservices, workload identity, brokers, events, distributed workflow, webhook and integration baseline with lab specifications; exact broker/version traceability and independent lab execution remain open |
| 10 Cloud-Native Application Security | 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 3, 4, 2, 3 | Broad cloud, container, Kubernetes, serverless and delivery engineering baseline with lab specifications; exact provider/CIS mappings and executable cloud validation remain open |
| 09 Mobile Application Security | 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 3, 4, 2, 3 | Broad Android/iOS and hybrid mobile engineering baseline with lab specifications; exact pinned MASVS/MASTG traceability and executable lab validation remain open |
| 08 Data Security and Privacy Engineering | 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 3, 4, 2, 3 | Broad lifecycle, cryptographic and privacy engineering baseline with lab specifications; exact ASVS traceability and executable lab validation remain open |
| 07 Identity and Access Security | 4, 4, 4, 3, 2, 4, 4, 4, 4, 4, 3, 4, 2, 3 | Substantive identity engineering baseline; detailed protocol profiles, exact ASVS IDs and reproducible labs remain open |

### Open quality actions

- Independent practitioner review has not yet been performed.
- Mermaid source has been committed but rendering has not been independently validated in a documentation renderer.
- Initial repository-relative link validation covered the original 12 Markdown files. Chapter 13 was subsequently checked for relative links and cross-references to Chapters 03, 10, 11, 12 and 18; the new Chapter 13 chapter-to-lab link is also maintained. A complete repository-wide link scan, external-link availability check and rendered diagram validation remain open.
- Jurisdiction applicability requires entity- and sector-specific legal review.
- Technical procedures and labs must be implemented and reproduced in isolated environments before being marked validated.


The initial architecture and documents are foundation drafts. Their existence demonstrates repository initialization, not final approval or independent technical review. The first three technical chapters are substantive starting baselines and remain open for expansion, cross-chapter verification and practitioner review. Content and internal-link validation completed at pre-bookkeeping checkpoint `dd0d1286bdaf6a6421374ca026acba953f8f4615`; this status update records those validation results. The scores below are preliminary internal self-assessments, not independent reviews or evidence of compliance.


## Chapter 13 implementation checkpoint — 2026-11-20

An initial executable baseline has been added under `implementations/13-software-supply-chain-security/`. It includes a GitHub Actions workflow with `contents: read`, exact event-SHA checkout, standard-library unit tests, and a deterministic SHA-256 source-file integrity manifest with verification. The workflow deliberately uses no third-party Actions and receives no deployment, signing or package-registry secrets. This manifest is not an SPDX/CycloneDX SBOM and does not provide build provenance or an artifact signature. The first main-branch CI run passed all steps on commit `63223ad4b6c6103f91d463fd60262b82fc2f0717` ([run 44755594677](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755594677)): exact event-SHA checkout, unit tests and manifest generation/verification. PR-triggered validation, branch/ruleset enforcement, SBOM generation, SCA, SLSA provenance, signing, container controls and independent validation remain pending.
