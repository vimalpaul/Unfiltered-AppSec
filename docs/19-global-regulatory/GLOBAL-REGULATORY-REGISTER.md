# Global AppSec Regulatory Register

| Field | Value |
|---|---|
| Document ID | UAPPSEC-19-001 |
| Status | Initial research baseline; not legal advice |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-01-18 |
| Scope | Initial India, Qatar, Saudi Arabia, UAE and EU research, with global expansion model |
| Classification | Public |

## 1. Purpose and legal-use warning

This register identifies laws, regulator controls and official guidance that may affect application and product security. It is a research and engineering input, not a legal opinion and not a declaration that an organization is compliant.

Regulatory applicability depends on facts such as:
- Where the organization is established and operates.
- Whether the organization offers products or services into a jurisdiction.
- The type of entity and its role: controller, processor, manufacturer, importer, service provider, financial entity, critical infrastructure operator or government supplier.
- Data categories, data subjects and processing purposes.
- Sector, transaction flows and criticality.
- Whether a product with digital elements is placed on a regulated market.
- Contractual, customer, procurement or certification commitments.
- Cross-border transfers, outsourcing and sub-processing.

A legal owner or qualified counsel must confirm scope, exemptions, effective dates and interpretation before a compliance decision or external representation is made.

## 2. Regulatory classification

| Classification | Meaning |
|---|---|
| Binding legislation | Statute, regulation or directive implemented through the applicable legal process |
| Mandatory regulator requirement | A binding rule, direction or control issued by an empowered regulator for entities in scope |
| National cybersecurity standard | A national control or assurance standard whose binding effect depends on its legal mandate, entity scope, certification, regulator or contract |
| Sector framework | Control framework applicable to particular regulated sectors or entities |
| Contractual / procurement | Requirement imposed through contract, customer agreement or procurement |
| Voluntary standard / guidance | Recommended or adopted by policy, but not automatically a legal obligation |

## 3. Initial jurisdiction register

| Jurisdiction | Instrument / authority | Current research position | AppSec relevance | Applicability caution |
|---|---|---|---|---|
| India | Digital Personal Data Protection Act 2023 and Digital Personal Data Protection Rules 2025; MeitY / Data Protection Board | Primary Gazette text reviewed; phased commencement identified | Personal-data safeguards, access controls, monitoring, retention, processor contracts, breach communications and privacy-by-design implications | Rules have staggered commencement. Confirm the Act commencement notifications, 2025 Rules corrigendum and exact operative date of each relevant provision |
| India | CERT-In Directions No. 20(3)/2022-CERT-In dated 2022-04-28; CERT-In under IT Act section 70B | Official directions portal and published direction text reviewed | Incident logging, six-hour reporting for listed cyber incidents, 180-day log retention in India, time synchronization and point of contact | Applicability is tied to the entities and incidents described in the directions; confirm current FAQs, extensions and later updates |
| Qatar | National Information Assurance Standard (NIA) v2.1, NCSA, May 2023 | Official standard reviewed | Software Security domain SS; web security controls; lifecycle, development/test separation, assurance before production, secure coding, component connectivity and cryptography | Confirm the regulated entity, national policy, certification, sector and contractual basis. Do not label every control as a universally applicable statute |
| Qatar | Personal Data Privacy Protection Law No. 13 of 2016; competent Qatari authority and official legal portal | Identified for dedicated research | Personal data processing, privacy, technical and organizational safeguards | Detailed articles, amendments, implementing guidance, sector scope and current competent authority require a separate legal-source review |
| Saudi Arabia | National Cybersecurity Authority Essential Cybersecurity Controls ECC 2:2024 | Official NCA document reviewed | Control subdomain 2-15 Web Application Security; wider governance, asset, identity, vulnerability, penetration testing, logging, cloud and supplier control domains | ECC applies to government agencies and specified affiliated and critical national infrastructure entities. NCA strongly encourages other entities; determine binding scope |
| Saudi Arabia | Personal Data Protection Law (PDPL), Royal Decree M/19, amended by Royal Decree M/148; SDAIA and applicable implementing/transfer regulations | Official SDAIA source identifies law, amendments and regulations | Personal-data processing, controller/processor duties, data-subject rights and cross-border transfers | Establish the role, processing and transfer basis; confirm current official implementing and transfer rules |
| United Arab Emirates | Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data; UAE Government | Official government description reviewed | Security and confidentiality of personal data, governance and processing controls | Check statutory scope and exclusions, including distinct regimes in financial free zones such as DIFC and ADGM and sector-specific requirements |
| European Union | GDPR, Regulation (EU) 2016/679 | Official EUR-Lex text reviewed | Privacy by design/default (Art. 25), processor controls (Art. 28), security of processing (Art. 32), breach notification (Art. 33) and DPIA (Art. 35) | Applicability depends on GDPR territorial and material scope and the controller/processor role |
| European Union | Cyber Resilience Act, Regulation (EU) 2024/2847 | Official EUR-Lex text reviewed; Article 14 reporting timetable confirmed | Product security lifecycle, vulnerability handling, product risk assessment, secure-by-design, support/updates and actively exploited vulnerability reporting | Applies to products with digital elements and relevant economic operators/manufacturers according to scope and role. Article 14 applies from 2026-09-11; general application is 2027-12-11 |
| European Union | NIS2 Directive (EU) 2022/2555 | Official EUR-Lex transposition date reviewed | Cyber risk management, supply-chain security, vulnerability handling, incident response and business continuity | Directive requirements operate through national transposition and are limited to entities and sectors in scope; analyze each member state's implementing law |
| European Union | DORA, Regulation (EU) 2022/2554 | Official EUR-Lex application date reviewed | ICT risk management, incident handling, resilience testing and ICT third-party risk for financial entities | Applies to financial entities in scope; also assess contractual and oversight relationships with ICT providers |
| United Kingdom | UK GDPR and Data Protection Act 2018; Information Commissioner's Office (ICO) guidance | Official ICO data-security guidance reviewed; legislation-specific change tracking needed | Risk-appropriate technical and organizational security measures, access restriction, resilience, vulnerability management and security testing | UK data protection law and guidance are subject to amendment; ICO states some guidance is under review following the Data (Use and Access) Act |
| Oman | Personal Data Protection Law, Royal Decree 6/2022; Executive Regulation, Ministerial Decision 34/2024; MTCIT | Official MTCIT records reviewed | Personal-data permissions and safeguards, controller/processor obligations, child data and breach procedures | Determine scope, permit requirements, exemptions, cross-border processing and relevant sector rules |
| United States | Federal and state privacy/security and sector regimes | Not yet mapped in detail | Potential requirements under health, finance, consumer privacy, state breach and critical-sector regimes | No single horizontal AppSec law covers all entities. Determine state, sector, entity, data and contract coverage before selecting controls |
| Singapore | Personal Data Protection Act and sector-specific financial/critical-system requirements | Planned research | Personal-data security and regulated system controls | Verify current PDPC and sector-regulator materials and scope before mapping |
| Australia | Privacy Act and APRA / critical-infrastructure regimes | Planned research | Privacy security and sector controls, software and third-party risk | Verify current amendments, regulated entity classes and sector rules before mapping |
| Brazil | LGPD and ANPD guidance | Planned research | Personal-data security, incident and processor governance | Confirm current legal text, ANPD regulations and cross-border transfer rules |
| Japan | Act on the Protection of Personal Information and PPC guidance | Planned research | Personal-data processing, security management measures and breach handling | Confirm current consolidated law, guidance and cross-border conditions |
| South Africa | POPIA and Information Regulator guidance | Planned research | Security safeguards, operator controls and compromise notification | Confirm applicable sections, current guidance and sector rules |
| Bahrain | Personal Data Protection Law No. 30 of 2018 and Personal Data Protection Authority | Planned research | Personal-data security and cross-border processing | Confirm current regulations, authority material and sector requirements from primary sources |
| Other GCC jurisdictions | Country-specific privacy, cyber and sector requirements | Planned country-by-country research | Data handling, cloud, application security, vulnerability, incident and supplier requirements | GCC membership does not create one uniform legal regime |

## 4. India: detailed AppSec implications

### 4.1 Digital Personal Data Protection Rules 2025

The Ministry of Electronics and Information Technology published the Digital Personal Data Protection Rules 2025 in the Gazette in November 2025. The Gazette text provides phased commencement:
- Rules 1, 2 and 17 to 21 commence on publication.
- Rule 4 commences one year after publication.
- Rules 3, 5 to 16, 22 and 23 commence eighteen months after publication.

The official Gazette identifies the notification date as 13 November 2025, while the MeitY listing records publication of the Rules on 14 November 2025 and separately lists a corrigendum dated 16 December 2025. Therefore, implementation teams must confirm the operative Gazette publication date and corrigendum before calculating a legal deadline. As at 18 November 2026, the one-year commencement point for Rule 4 has passed; the eighteen-month tranche is not yet due under the original schedule.

Rule 6, "Reasonable security safeguards", is in the eighteen-month tranche. The published text describes minimum safeguards including:
- Encryption, obfuscation, masking or tokenization as appropriate.
- Access controls for computer resources.
- Access visibility through logs, monitoring and review.
- Continued processing measures such as backups.
- Retention of relevant logs and personal data for one year for specified detection, investigation and remediation purposes, subject to other applicable law.
- Appropriate processor-contract provisions and technical/organizational measures.

The text of Rule 7 addresses communication to affected Data Principals and the Board after a personal-data breach. Its commencement is also within the eighteen-month tranche under the original schedule.

**Engineering preparation:** build privacy and security requirements into data flows now; inventory personal data; map controllers/Data Fiduciaries and processors; minimize collection; implement access controls and protected audit trails; design deletion, backup, incident and communication processes; and preserve evidence. Do not describe Rule 6 as already in force before its commencement.

### 4.2 CERT-In Directions, 28 April 2022

The directions were issued under section 70B(6) of the Information Technology Act 2000. The listed entities include service providers, intermediaries, data centres, body corporates and government organizations. Among other requirements, the directions include:
- Report cyber incidents listed in Annexure I within six hours of noticing them or being informed.
- Enable ICT system logs and securely maintain them for a rolling 180 days within Indian jurisdiction.
- Synchronize system clocks with NTP sources traceable to NIC or NPL, subject to the stated provisions.
- Designate a point of contact for CERT-In.

For application operators, this affects logging architecture, centralized time synchronization, log retention and integrity, incident classification, escalation, evidence capture and response readiness. Logs should be useful for attribution and reconstruction while avoiding plaintext credentials, bearer tokens, cryptographic secrets and unnecessary personal data.

Do not assume every defect or generic security alert automatically constitutes a reportable Annexure I incident. The incident-response owner must assess the actual event against the directions and current CERT-In clarifications.

### 4.3 India implementation evidence

- Personal-data inventory, purpose and processing records.
- Data-flow and processor/sub-processor map.
- Access-control and privileged-access records.
- Encryption and key-management evidence.
- Data retention, backup and deletion design.
- Log coverage, integrity, access restriction, retention and time synchronization evidence.
- Incident classification and CERT-In reporting decision records.
- Breach communication and Board notification process when applicable.
- Contractual security clauses and supplier assurance.
- Approved exceptions and legal applicability decisions.

## 5. Qatar: National Information Assurance Standard

The National Cyber Security Agency's National Information Assurance Standard v2.1 is dated May 2023. Its Software Security [SS] domain states that security should be integrated into software development and acquisition rather than added as an afterthought.

Relevant requirements include:
- **SS 1:** consider security in all SDLC phases and integrate it into system development and implementation.
- **SS 2:** classify applications using the national data-classification policy and apply protection appropriate to confidentiality, integrity and availability ratings.
- **SS 3:** develop and implement functional, technical and assurance security requirements.
- **SS 4:** maintain dedicated development and test infrastructure separate from production and restrict information flow.
- **SS 5:** allow production use only after appropriate quality and security assurance.
- **SS 6:** use secure programming practices, including least privilege, deny-by-default and input validation.
- **SS 7:** review or test software for vulnerabilities before production; the standard recommends independent review/testing.
- **SS 22:** review active web content for security issues and references OWASP secure web application guidance.
- **SS 23:** minimize connectivity and access between web application components.
- **SS 24:** protect personal and sensitive information at rest and in transit using appropriate cryptographic controls.

**AppSec implementation:** create an SSDLC control plan; classify applications and data; maintain separate development/test/production environments; define pre-production security assurance; establish secure code standards and code review; inventory web application components; restrict unnecessary east-west access; and protect sensitive data.

The standard and NCSA certification scheme must be read with the entity's legal, national-policy, sector and contractual applicability. The standard is not itself proof of certification or proof that a particular product meets every requirement.

## 6. Saudi Arabia: NCA Essential Cybersecurity Controls

The National Cybersecurity Authority published Essential Cybersecurity Controls ECC 2:2024. The document's scope identifies government agencies and affiliated entities, plus private-sector entities owning, operating or hosting Critical National Infrastructure; other private-sector entities are strongly encouraged to use the controls. The statement of applicability varies by entity and technology use. Cloud computing and hosting controls may be binding for entities using or planning to use such services within the specified scope.

The control architecture includes governance, cybersecurity defense, resilience, and third-party/cloud domains. The Web Application Security subdomain is **2-15**:
- **2-15-1:** cybersecurity requirements for protection of external web applications are identified, documented and approved.
- **2-15-2:** those cybersecurity requirements are implemented.

Related control areas include project management, asset management, identity and access management, data protection, cryptography, vulnerability management, penetration testing, event logging and monitoring, incident management, third-party security and cloud hosting.

**AppSec implementation:** maintain an external-application inventory; identify business and data owners; document and approve security requirements; implement controls; perform risk-based verification; retain evidence and remediation records; and map hosting and suppliers against applicable cloud/third-party requirements.

The English ECC document states that the Arabic version is binding for interpretation and that entities should obtain the latest document from NCA. Legal and audit work must use the authoritative language and current NCA publication.

## 7. European Union: key application-security instruments

### 7.1 GDPR

Where GDPR applies, Article 32 requires security of processing appropriate to risk, taking into account state of the art, implementation cost, processing nature/scope/context/purpose and risks to individuals. Its examples include encryption or pseudonymisation, ongoing confidentiality/integrity/availability/resilience, restoration capability and regular testing/evaluation of technical and organizational measures.

Other AppSec-relevant provisions include:
- Article 25: data protection by design and by default.
- Article 28: processor requirements and contractual governance.
- Article 32: security of processing.
- Article 33: personal-data breach notification by controllers to the supervisory authority under its conditions and timeline.
- Article 35: data protection impact assessment when required.

**Engineering implications:** data classification, minimization, role and access controls, privacy-safe defaults, encryption, availability/recovery, processor assurance, security testing, incident evidence and DPIA integration. The legal basis and territorial scope must be established independently.

### 7.2 Cyber Resilience Act

Regulation (EU) 2024/2847 establishes horizontal cybersecurity requirements for products with digital elements. It must not be confused with a general law applying to every custom application or every SaaS service without regard to the product and economic-operator definitions.

The Regulation's Article 71 states:
- General application from **11 December 2027**.
- Chapter IV (Articles 35 to 51) applies from **11 June 2026**.
- Article 14 applies from **11 September 2026**.

As at this register's research date, Article 14 is already applicable. Under Article 14, a manufacturer must report an actively exploited vulnerability contained in a product with digital elements through the single reporting platform to the designated CSIRT coordinator and ENISA. The schedule includes:
- Early warning without undue delay and within 24 hours of becoming aware.
- Vulnerability notification without undue delay and within 72 hours, unless the information was already supplied.
- Final report no later than 14 days after a corrective or mitigating measure becomes available.

**Engineering implications:** product inventory and classification, vulnerability intake and discovery timestamps, exploitability assessment, coordinated reporting, customer communication, corrective/mitigating measures, vulnerability database readiness, support period and secure-update capability. Confirm manufacturer status, product scope and exceptions with legal/product counsel.

### 7.3 NIS2

Directive (EU) 2022/2555 required member states to transpose by 17 October 2024, with national measures applying from 18 October 2024. NIS2 has entity, sector and size/scope conditions and must be examined through each member state's implementation.

Relevant AppSec dependencies include risk management, incident handling, business continuity, supply-chain security, vulnerability handling, access control, asset management and the security of network and information systems. The knowledge base will map specific national implementing laws in later jurisdiction chapters rather than assume the directive applies identically without transposition analysis.

### 7.4 DORA

Regulation (EU) 2022/2554 applies from 17 January 2025 and concerns digital operational resilience in the financial sector. For financial entities in scope, its ICT risk-management, incident, resilience testing and ICT third-party risk requirements can affect application development, outsourcing, cloud services, software change and supplier governance.

The applicability and detailed requirements depend on the entity's status and the DORA technical standards and supervisory context. It should not be treated as a generic requirement for every application developer.

## 8. Saudi, Qatar, UAE and India: cross-border design concerns

When a product processes data for customers in several jurisdictions:
1. Identify each legal entity and its role.
2. Identify data subjects, data categories, purposes, processors and storage locations.
3. Map each international transfer and remote access path.
4. Identify localization, transfer mechanism, security and incident requirements.
5. Determine whether sector rules add requirements beyond the horizontal privacy regime.
6. Record the legal basis and approval for each transfer.
7. Ensure deletion, backup and retention schedules do not conflict.
8. Keep incident-response contacts and regulator/customer notification decision paths jurisdiction-specific.

A global SaaS design must not assume that a single region, cloud control or generic privacy policy satisfies all applicable law.

## 9. Applicability decision workflow

~~~mermaid
flowchart TD
    S[Identify product, entity and processing] --> J[Identify countries and markets served]
    J --> E[Identify entity role and sector]
    E --> D[Identify data, product and system scope]
    D --> L[Check laws, regulator instruments and contracts]
    L --> A{Instrument applies?}
    A -->|Yes| O[Record obligation, effective date and owner]
    A -->|No| N[Record exclusion and evidence]
    A -->|Unclear| C[Legal or regulator clarification]
    O --> T[Translate into security requirement]
    N --> R[Review if facts change]
    C --> T
    T --> V[Implement, test and retain evidence]
~~~

## 10. Regulatory requirement record template

| Field | Example value or instruction |
|---|---|
| Regulatory ID | REG-COUNTRY-INSTRUMENT-CLAUSE |
| Country | Exact country or territory |
| Authority | Issuing regulator |
| Instrument | Full legal or control name and identifier |
| Version / date | Edition and publication date |
| Effective date | Exact commencement or phased date |
| Entity scope | Entity roles and regulated activity |
| System/data scope | Products, processing and assets affected |
| Requirement | Original-language summary with exact source identifier |
| AppSec outcome | Security behavior required |
| Control owner | Business, product, engineering, security or privacy owner |
| Evidence | Design, implementation, test, log or contract record |
| Applicability decision | Applies / Does not apply / Pending |
| Rationale | Evidence supporting decision |
| Reviewer | Authorized legal/compliance owner |
| Review trigger | Date, legal change or business change |

## 11. Research gaps and priorities

| Gap ID | Jurisdiction / topic | Missing work | Priority | Closure evidence |
|---|---|---|---|---|
| REG-GAP-001 | India DPDP | Reconcile Gazette publication date and 2025 corrigendum; confirm Act commencement notifications and effective status of each relevant provision | High | Consolidated official source record and legal review |
| REG-GAP-002 | Qatar data protection | Verify Law No. 13 of 2016 text, amendments, implementing guidance, competent authority and sector scope | High | Primary legal text and applicability memo |
| REG-GAP-003 | Saudi PDPL | Build article-by-article controller/processor, breach, retention and transfer crosswalk against current regulations | High | SDAIA source set and legal review |
| REG-GAP-004 | UAE privacy | Verify federal PDPL rules, exemptions, regulator guidance, DIFC and ADGM regimes and relevant sector rules | High | Country and free-zone applicability matrix |
| REG-GAP-005 | EU CRA | Build detailed Annex I, Article 13, Article 14, support-period, conformity and economic-operator mapping | High | Clause/obligation register and PSIRT evidence model |
| REG-GAP-006 | EU NIS2 | Identify current member-state implementing laws and regulated entity definitions | High | Country-by-country transposition register |
| REG-GAP-007 | EU DORA | Map current technical standards and financial-sector software/supplier implications | Medium | DORA control crosswalk |
| REG-GAP-008 | United States | Federal, state and sector-specific security/privacy mapping | Medium | State/sector decision matrix |
| REG-GAP-009 | Bahrain | Verify Law No. 30 of 2018, regulations and PDPA guidance | Medium | Primary authority source set |
| REG-GAP-010 | Oman | Detailed articles, breach, transfer and permit controls under RD 6/2022 and MD 34/2024 | Medium | Article/obligation crosswalk |
| REG-GAP-011 | Singapore and Australia | Privacy and regulated-sector cyber requirements | Medium | Primary regulator source matrix |
| REG-GAP-012 | Brazil, Japan, South Africa | Current privacy security and incident requirements | Medium | Official law and authority source matrix |

## 12. Primary sources

1. India, Gazette of India, Digital Personal Data Protection Rules 2025: https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf
2. MeitY, Digital Personal Data Protection Rules 2025 listing and corrigendum: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
3. CERT-In, Directions under section 70B: https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf
4. CERT-In, Directions portal and updates: https://cert-in.org.in/Directions70B.jsp
5. Qatar NCSA, National Information Assurance Standard v2.1: https://assurance.ncsa.gov.qa/sites/default/files/publications/policy/2023/NCSA_CSGA_%20National_Information_Assurance_Standard_En_V2.1_0.pdf
6. Qatar NCSA, NIA Certification: https://ncsa.gov.qa/en/pages/certification-nia-application
7. Saudi NCA, ECC 2:2024: https://cdn.nca.gov.sa/api/files/public/upload/86e09090-44e4-481f-bc28-355673607654_ECC--2024-EN.pdf
8. Saudi NCA, ECC landing page: https://nca.gov.sa/en/regulatory-documents/controls-list/ecc/
9. Saudi SDAIA, PDPL and implementing/transfer regulations: https://dgp.sdaia.gov.sa/
10. UAE Government, Data Protection Laws: https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws
11. European Union, GDPR Regulation (EU) 2016/679: https://eur-lex.europa.eu/eli/reg/2016/679/oj
12. European Union, Cyber Resilience Act Regulation (EU) 2024/2847: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R2847
13. European Union, NIS2 Directive (EU) 2022/2555: https://eur-lex.europa.eu/eli/dir/2022/2555/oj
14. European Union, DORA Regulation (EU) 2022/2554: https://eur-lex.europa.eu/eli/reg/2022/2554/oj
15. United Kingdom ICO, Security outcomes for personal-data processing: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/security/a-guide-to-data-security/security-outcomes
16. Oman MTCIT, Personal Data Protection Law and Executive Regulation: https://www.mtcit.gov.om/sectors/governance/personal

## 13. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial researched regulatory register, technical implications and gap register |
