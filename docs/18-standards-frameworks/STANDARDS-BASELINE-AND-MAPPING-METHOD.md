# AppSec Standards Baseline and Mapping Method

| Field | Value |
|---|---|
| Document ID | UAPPSEC-18-001 |
| Status | Initial research baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Standards and framework selection, edition control and AppSec traceability |
| Classification | Public |

## 1. Purpose

This document establishes how the knowledge base selects, interprets and maps application security standards and frameworks. It identifies the initial authoritative baseline and prevents three common mapping errors:

1. Treating an awareness taxonomy as a complete verification standard.
2. Treating an organizational framework as a technical control test plan.
3. Treating a mapping relationship as proof of implementation or legal compliance.

A standard can provide security requirements, an organizational outcome model, a testing method, a maturity model or a sector-specific control set. These purposes are complementary but not interchangeable.

## 2. Baseline selection

### 2.1 Core application security references

| Reference | Publisher / edition | Purpose in this KB | Correct use | Important limitation |
|---|---|---|---|---|
| OWASP Application Security Verification Standard | OWASP, ASVS 5.0.0, stable release 2025-05-30 | Primary technical requirement and verification backbone for web applications and services | Derive applicable requirements, design controls and repeatable verification cases | Select requirements by architecture and risk; do not claim that adopting ASVS alone proves security |
| OWASP Top 10 | OWASP, Top 10:2025 final | Awareness and risk communication | Explain common categories of web application risk and organize learning | Not a complete application inventory, threat model, secure coding standard or test plan |
| OWASP API Security Top 10 | OWASP, 2023 edition | API risk awareness and initial attack-case taxonomy | Organize API authorization, authentication, resource, business-flow and inventory tests | Does not replace protocol-specific design, API inventory or detailed verification criteria |
| NIST Secure Software Development Framework | NIST SP 800-218 v1.1 final, 2022-02-03 | Lifecycle and software producer practice baseline | Structure organization preparation, software protection, secure production and vulnerability response | High-level practice framework; not a line-by-line application technical verification catalog |
| NIST Cybersecurity Framework | NIST CSF 2.0, published 2024-02-26 | Governance and enterprise risk outcome model | Connect AppSec capability and outcomes to enterprise cybersecurity governance | Does not prescribe a specific application architecture or test suite |
| PCI DSS | PCI SSC, v4.0.1 | Payment-card environment requirements where applicable | Derive software development, access, vulnerability and assessment obligations for an in-scope environment | Applicability depends on payment flows, roles, cardholder data environment, contractual/acquirer requirements and current PCI SSC rules |
| ISO/IEC 27001 | ISO/IEC 27001:2022 | Information security management system context | Map AppSec processes into risk treatment, asset management, supplier and operational governance | ISMS certification does not demonstrate that an application is technically secure |
| ISO/IEC 27034 | ISO/IEC 27034 series | Application security management and process context | Use when designing organizational application-security processes | Confirm the applicable part and current edition from the ISO catalogue before a formal audit mapping |
| ISO/IEC 29147 and 30111 | Vulnerability disclosure and vulnerability handling standards, edition-specific | Product security and coordinated vulnerability handling | Structure disclosure policy, intake, triage and remediation | Verify exact current editions and licensing before publishing clause-level mappings |
| OWASP Software Assurance Maturity Model | OWASP SAMM | AppSec programme maturity and improvement | Assess governance, design, implementation, verification and operations maturity | Maturity assessment is not a product-level penetration test or certification |
| MITRE CWE and CAPEC | MITRE weakness and attack-pattern catalogues | Weakness taxonomy and attack-pattern relationships | Normalize weakness descriptions and connect defects to attack patterns | Catalogues are taxonomies; applicability and exploitability remain context-dependent |

### 2.2 Version and status handling

- **Stable final:** may be selected as a baseline after scope and applicability review.
- **Draft / public draft:** monitor and test against where useful, but do not call it a final requirement.
- **Bleeding edge:** useful for research and contribution; not the normative production baseline unless explicitly adopted with documented risk.
- **Superseded / withdrawn:** retain only for historical or contract-specific relevance.
- **Sector or contract profile:** apply only after determining the organization's role and scope.

The OWASP ASVS website identifies version 5.0.0 as stable and published 30 May 2025. OWASP's Top 10 project identifies 2025 as its latest released version. NIST's SSDF project lists SP 800-218 Rev. 1 / v1.2 as a draft dated 17 December 2025; SP 800-218 v1.1 remains the final edition in the source catalogue at the research cut-off used here. Check the publisher before each formal mapping exercise.

## 3. What each baseline does and does not do

### 3.1 ASVS

Use ASVS as a structured technical requirement catalogue. For each application:
1. Identify architecture, data classes, user types and exposed interfaces.
2. Select the appropriate verification scope and depth.
3. Map applicable requirements to security requirements with stable internal IDs.
4. Identify implementation location and owner.
5. Define one or more positive and negative tests.
6. Preserve evidence and record exceptions.
7. Revisit selection when a feature, data class, trust boundary or threat changes.

Do not copy the whole standard into local documents. Preserve requirement identifiers, summarize the intent in original language and link to the official source. Use the official machine-readable release where the exact requirement text and version need to be reviewed.

### 3.2 OWASP Top 10

The Top 10 is appropriate for executive awareness, developer education and initial risk discussions. It can help select areas for deeper assessment. It must not be used as the sole acceptance criterion because the most relevant weakness in a particular application may be a business-specific authorization failure, a product workflow flaw, an unsafe integration or a threat not represented by a short awareness list.

### 3.3 OWASP API Security Top 10:2023

The current reference edition used in this baseline identifies:
- API1:2023 Broken Object Level Authorization.
- API2:2023 Broken Authentication.
- API3:2023 Broken Object Property Level Authorization.
- API4:2023 Unrestricted Resource Consumption.
- API5:2023 Broken Function Level Authorization.
- API6:2023 Unrestricted Access to Sensitive Business Flows.
- API7:2023 Server Side Request Forgery.
- API8:2023 Security Misconfiguration.
- API9:2023 Improper Inventory Management.
- API10:2023 Unsafe Consumption of APIs.

Treat this list as an attack-case index. Convert each risk into application-specific requirements and tests for the real API inventory, identity model and data relationships.

### 3.4 NIST SSDF

NIST SP 800-218 v1.1 groups secure development practices into:
- **Prepare the Organization (PO):** establish organizational readiness and secure development capabilities.
- **Protect the Software (PS):** protect software and its components against unauthorized access and tampering.
- **Produce Well-Secured Software (PW):** produce well-secured software through development and verification practices.
- **Respond to Vulnerabilities (RV):** identify, assess, prioritize and remediate vulnerabilities in released software.

Use the practice and task identifiers from the exact SSDF edition when creating traceable implementation records. The framework supports secure software acquisition and producer-consumer communications, but it is not a replacement for product-specific requirements and tests.

## 4. Mapping model

Every mapping record must contain:

| Field | Required content |
|---|---|
| Mapping ID | Stable project identifier |
| Source framework | Publisher, title, version and status |
| Source reference | Exact clause, control or requirement identifier |
| Target control | Internal AppSec control or requirement |
| Security outcome | What risk or failure the control is intended to reduce |
| Mapping type | Direct, Partial, Supporting, Related, or Not demonstrated |
| Rationale | Why the relationship exists |
| Applicability | Conditions under which the source applies |
| Implementation | System location, process and owner |
| Verification | Test method, expected result and evidence |
| Gaps | Missing implementation, scope gap or non-equivalence |
| Confidence | High, Medium or Low with rationale |
| Review | Source date, mapping date and next review trigger |

### Mapping type definitions

- **Direct:** the source requirement and target control address substantially the same security outcome and scope.
- **Partial:** the target control covers only a subset or requires additional controls.
- **Supporting:** the target control contributes to achieving the source requirement but is not sufficient by itself.
- **Related:** the controls concern a related risk but do not establish equivalence.
- **Not demonstrated:** no defensible implementation or evidence relationship has been shown.

## 5. Initial traceability examples

These are illustrative relationships, not official equivalence determinations.

| Internal requirement | Target outcome | Candidate source mapping | Type | Evidence expected |
|---|---|---|---|---|
| REQ-ARCH-001 | Security requirements are defined before implementation | NIST SSDF PO practices; Qatar NIA SS 1 and SS 3 | Supporting | Approved requirements, owner, design review record |
| REQ-ENV-002 | Development/test environments are separated from production | Qatar NIA SS 4 | Direct to the stated environment-separation outcome | Network and identity configuration, environment access review |
| REQ-REL-003 | No application enters production without appropriate security assurance | Qatar NIA SS 5 | Direct to the stated release-assurance outcome | Test results, release gate, approved exceptions |
| REQ-CODE-004 | Secure coding and input validation are used | Qatar NIA SS 6; ASVS selected requirements | Supporting / Direct by specific control | Code review, test, build and remediation evidence |
| REQ-WEB-005 | Exposed web application controls are identified and implemented | Saudi NCA ECC 2:2024 controls 2-15-1 and 2-15-2 | Direct to stated identification/implementation outcome | Approved external web-app requirements and implementation evidence |
| REQ-DATA-006 | Personal data has risk-appropriate protection and security testing | GDPR Article 32, where applicable; India DPDP Rules Rule 6 when effective | Related / Direct by specific requirement | Encryption, access controls, audit logs, backup and control testing |
| REQ-PSIRT-007 | Actively exploited product vulnerabilities are reported within applicable timelines | EU CRA Article 14, when manufacturer and product scope apply | Direct to reporting workflow obligation | PSIRT records, discovery timestamps, notifications and final report |

The target requirement wording above is project-authored. It is not a reproduction of the source standards.

## 6. Jurisdiction and sector standards

Standards applicability may arise through:
- Statute or regulation.
- Regulator-issued mandatory controls.
- Certification or accreditation scheme.
- Contract, customer requirement or procurement specification.
- Payment-brand or acquirer rules.
- Voluntary organizational policy.

The same framework can be mandatory for one entity and voluntary for another. The regulator or legal owner must establish applicability.

## 7. Control-to-evidence architecture

~~~mermaid
flowchart TD
    S[Source framework requirement] --> M[Applicability and mapping analysis]
    M --> R[Internal security requirement]
    R --> C[Control design and owner]
    C --> I[Implementation location]
    I --> T[Verification method]
    T --> E[Evidence and results]
    E --> G[Gap, exception or residual risk]
    G --> A[Corrective action and re-test]
    A --> E
    E --> V[Assurance review]
~~~

## 8. Quality and audit cautions

- A framework mapping is not a legal opinion.
- A control document is not proof that a control operates.
- A passing test does not prove all requirements are satisfied.
- Tool output does not replace review of false positives, false negatives and scope.
- An organization-wide certification does not mean each application has been verified.
- A sector-specific control applies only within its regulated scope.
- A draft standard must not be presented as the final normative edition.
- Copyrighted requirements must not be reproduced beyond permitted use.

## 9. Official sources and version records

1. OWASP ASVS 5.0.0: https://asvs.owasp.org/ (stable release page; published 2025-05-30).
2. OWASP ASVS downloads: https://asvs.owasp.org/downloads/
3. OWASP Top 10 project: https://owasp.org/projects/Top-Ten (Top 10:2025 final).
4. OWASP API Security Project: https://owasp.org/projects/api-security-project/ (API Security Top 10:2023).
5. OWASP API Top 10:2023: https://api-security.owasp.org/editions/2023/en/0x03-introduction/
6. NIST SP 800-218 v1.1: https://csrc.nist.gov/pubs/sp/800/218/final (final, 2022-02-03).
7. NIST SSDF project and publication status: https://csrc.nist.gov/Projects/ssdf
8. NIST CSF 2.0: https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20 (published 2024-02-26).
9. PCI SSC document library: https://www.pcisecuritystandards.org/document_library/ (PCI DSS v4.0.1 listing).
10. Qatar NCSA National Information Assurance Standard v2.1: https://assurance.ncsa.gov.qa/sites/default/files/publications/policy/2023/NCSA_CSGA_%20National_Information_Assurance_Standard_En_V2.1_0.pdf
11. Saudi NCA Essential Cybersecurity Controls ECC 2:2024: https://cdn.nca.gov.sa/api/files/public/upload/86e09090-44e4-481f-bc28-355673607654_ECC--2024-EN.pdf

## 10. Maintenance and limitations

This is a baseline register and mapping method. It does not contain a full clause-level crosswalk for every listed framework. Each detailed mapping must be added after applicability and source verification. Check official publishers before each audit, procurement or regulatory engagement. ISO catalogue details and copyrighted clause text require publisher-controlled verification.

## 11. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial standards baseline and mapping method |
