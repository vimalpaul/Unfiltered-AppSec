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
- Current milestone: Milestone 0 foundation and first technical chapters

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
| Standards baseline | Version-aware source and mapping method | Initial baseline created | Build detailed clause/control mappings chapter by chapter |
| Global regulatory register | Initial India, Qatar, Saudi Arabia, UAE and EU records | Initial research baseline | Expand by country and sector; validate amendments and applicability |
| Secure SDLC | Operating model and lifecycle control implementation | Pending | Next major technical chapter |
| Secure coding | Language patterns and code review | Pending | Depends on Secure SDLC and fundamentals |
| Web application security | Technical controls and test procedures | Pending | Depends on architecture, identity, data security |
| API security | Protocol and authorization testing | Pending | Start with OWASP API Security Top 10 and object/property authorization |
| Identity and access security | Authentication, federation, session and authorization | Pending | Core dependency for web and API chapters |
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

1. Complete the Secure SDLC and Product Security operating model.
2. Build secure coding and code review playbooks, starting with common web stacks and language-specific patterns.
3. Develop the Web Application Security chapter, organized by control objectives and testable abuse cases rather than only vulnerability names.
4. Develop API Security, with detailed object-level, property-level and function-level authorization procedures.
5. Expand the standards crosswalk using exact ASVS and framework identifiers.
6. Expand India and GCC regulatory chapters into country- and sector-specific records with applicability decision logic.
7. Establish common test-case, evidence, finding and remediation templates.
8. Build isolated labs tied to requirements and verification cases.

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

The initial architecture and documents are foundation drafts. Their existence demonstrates repository initialization, not final approval or independent technical review. The first two technical chapters are substantive starting baselines and remain open for expansion, cross-chapter verification and practitioner review.
