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
- Current milestone: Milestone 6 data security and privacy engineering playbook and lab specifications

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
| NIST CSF | CSF 2.0, 2024-02-26 | Governance and risk outcome taxonomy; not an AppSec test standard |
| PCI DSS | v4.0.1 | Use where cardholder-data environment and contractual/acquirer applicability exist |
| India DPDP Rules | 2025 Gazette notification and phased commencement | Track phased commencement; re-check corrigendum and current legal status before operational reliance |
| EU CRA | Regulation (EU) 2024/2847 | Article 14 reporting obligations apply from 2026-09-11; general application date 2027-12-11 |
| Qatar NIA | National Information Assurance Standard v2.1, May 2023 | Initial security-development and web-control mapping captured |
| Saudi ECC | ECC 2:2024 | Initial application-security subdomain mapping captured |

## 4. Next work sequence

1. Expand Chapter 08 with exact ASVS 5.0.0 requirement mappings, privacy-by-design controls and version-specific cloud KMS/key lifecycle implementation examples.
2. Expand Chapter 06 with exact ASVS 5.0.0 requirement mappings, API contract test automation and version-specific GraphQL/gRPC profiles.
3. Expand Chapter 05 with exact ASVS 5.0.0 and versioned WSTG v4.2 requirement/test mappings.
4. Expand Chapter 07 with exact ASVS 5.0.0 requirement IDs, detailed SAML/OIDC implementation profiles and framework-version-specific executable examples.
5. Implement and reproduce the web, API, identity, data security and secure coding labs in pinned, isolated environments.
6. Expand India and GCC regulatory research into country- and sector-specific records with applicability decision logic.
7. Establish reusable inventories, threat-model, assessment, finding, remediation and evidence templates.
8. Continue the standards crosswalk into chapter-specific requirement-to-test mappings.

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
| 08 Data Security and Privacy Engineering | 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 3, 4, 2, 3 | Broad lifecycle, cryptographic and privacy engineering baseline with lab specifications; exact ASVS traceability and executable lab validation remain open |
| 07 Identity and Access Security | 4, 4, 4, 3, 2, 4, 4, 4, 4, 4, 3, 4, 2, 3 | Substantive identity engineering baseline; detailed protocol profiles, exact ASVS IDs and reproducible labs remain open |

### Open quality actions

- Independent practitioner review has not yet been performed.
- Mermaid source has been committed but rendering has not been independently validated in a documentation renderer.
- A repository-relative Markdown link check was run across all 12 committed Markdown files on 2026-11-18: 22 relative references were found and none were broken. Mermaid code fences are balanced. External-link availability and rendered diagram validation have not been independently automated.
- Jurisdiction applicability requires entity- and sector-specific legal review.
- Technical procedures and labs must be implemented and reproduced in isolated environments before being marked validated.


The initial architecture and documents are foundation drafts. Their existence demonstrates repository initialization, not final approval or independent technical review. The first three technical chapters are substantive starting baselines and remain open for expansion, cross-chapter verification and practitioner review. Content and internal-link validation completed at pre-bookkeeping checkpoint `dd0d1286bdaf6a6421374ca026acba953f8f4615`; this status update records those validation results. The scores below are preliminary internal self-assessments, not independent reviews or evidence of compliance.
