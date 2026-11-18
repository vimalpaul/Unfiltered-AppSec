# Research, Evidence and Quality Method

| Field | Value |
|---|---|
| Document ID | UAPPSEC-GOV-003 |
| Status | Draft baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Classification | Public |

## 1. Research discipline

Research must precede material technical or regulatory claims. Prefer primary sources, exact standards editions, official regulator publications, vendor documentation and original research. Community knowledge can identify leads but must be independently corroborated before it supports a high-impact recommendation.

### Source hierarchy

| Grade | Source class | Permitted use |
|---|---|---|
| A | Law, official regulator, national CERT, official standard publisher, official vendor advisory or original protocol specification | Primary authority for claims within its scope |
| B | Peer-reviewed paper, recognized technical body or original research with transparent methods | Strong technical support, with scope and date limits |
| C | Reputable specialist publication, industry analysis or practitioner documentation independently corroborated | Context, implementation experience and corroborated patterns |
| D | Community discussion, unverified blog, social post or unattributed material | Leads only; not sole basis for material risk, legal or architecture conclusions |

Evidence grades apply to claims, not the reputation of an entire document. An official page can be authoritative for publication status but may not establish how a law applies to a specific organization.

## 2. Required source metadata

For important sources record:
- Publisher and responsible authority.
- Exact title, instrument or identifier.
- Edition, revision, version and language.
- Publication and effective dates, where relevant.
- Current status: draft, final, active, superseded, withdrawn or historical.
- Canonical URL and access date.
- Jurisdiction and regulated activity, if applicable.
- Claims supported and limitations.
- Whether the reference is primary or secondary.

For legal instruments, distinguish enactment, publication, commencement, phased application, transition, amendment and enforcement date.

## 3. Claim classification

Use explicit wording to distinguish:
- **Source fact:** directly stated by an identified source.
- **Technical analysis:** reasoned explanation derived from architecture, protocol or evidence.
- **Recommendation:** proposed control, workflow or design.
- **Assumption:** condition adopted pending evidence.
- **Illustrative scenario:** fictional or composite example.
- **Unknown:** a question requiring more evidence or specialist review.

Do not convert a recommendation into a legal requirement. Do not convert a standard's informative guidance into a mandatory control without an applicable adoption mechanism.

## 4. Standards mapping method

For each mapping capture:
1. Source framework, publisher and exact edition.
2. Exact source control, requirement or clause identifier.
3. Target AppSec requirement or control.
4. Mapping strength: Direct, Partial, Supporting, Related, or Not demonstrated.
5. Rationale and security outcome.
6. Gaps and non-equivalence.
7. Implementation example and evidence needed.
8. Applicability conditions and assumptions.
9. Confidence and review notes.

A crosswalk identifies possible relationships; it does not prove implementation, effectiveness, certification or compliance. Avoid reproducing copyrighted standards text. Summarize in original wording and preserve identifiers.

## 5. Regulatory research method

Research each country separately. For every instrument record:
- Country or territory.
- Sector and regulated activity.
- Regulator or issuing authority.
- Official title, law number or control identifier.
- Entity and technology scope.
- Applicability conditions and exclusions.
- Publication, commencement and effective dates.
- Amendments, transition and supersession.
- Security, reporting, retention, audit and supplier obligations where verified.
- Official source.
- Application security implications.
- Legal questions that need specialist interpretation.

Distinguish binding law, subordinate regulation, regulator-mandated control, contract, technical standard, certification scheme, guidance and voluntary good practice. Do not infer applicability solely from the location of a user or system.

## 6. Real-world scenario rules

Label scenarios accurately:
- Verified public incident.
- Official regulator or vendor incident report.
- Original researcher analysis.
- Composite industry scenario.
- Fictional lab.

Do not state that a fictional lab occurred in production. Do not speculate about an actor's identity or motive without reliable evidence. Include the source and its limitations for a public incident.

## 7. Procedure completeness

A procedure must state:
- Purpose and authorization.
- Scope, exclusions and stop conditions.
- Prerequisites and required access.
- Roles and responsibilities.
- Tools, versions and configuration.
- Inputs and expected outputs.
- Steps and decision points.
- Expected observations and failure conditions.
- Evidence to capture.
- Safety and operational precautions.
- Remediation, escalation and rollback.
- Retest and closure criteria.

A tool name or one-line command is not a procedure.

## 8. Chapter quality scorecard

Score each applicable dimension from 0 to 5.

| Score | Meaning |
|---|---|
| 0 | Missing |
| 1 | Mentioned only; insufficient to act |
| 2 | Partial explanation; important gaps remain |
| 3 | Substantive, technically credible baseline |
| 4 | Detailed, reproducible and well evidenced |
| 5 | Deep, cross-referenced, independently validated and maintained |

Dimensions:
1. Scope and applicability.
2. Technical depth.
3. Research and evidence.
4. Standards mapping.
5. Regulatory mapping.
6. Real-world use cases.
7. Architecture and diagrams.
8. Implementation guidance.
9. Verification and evidence.
10. Operational integration.
11. AI governance where relevant.
12. Navigation and cross-references.
13. Quality assurance.
14. Maintenance and ownership.

Use N/A only with a reason. A major playbook should not be called Complete while any critical applicable dimension is below 3 or a material safety, source, accuracy or navigation issue remains.

## 9. Review triggers

Review a chapter when:
- A cited standard changes status or edition.
- A legal instrument is amended, commenced or interpreted by an authoritative regulator.
- A vendor changes a supported security feature or product lifecycle.
- A newly exploited weakness invalidates assumptions.
- A significant incident demonstrates a material failure mode.
- A platform, language or dependency reaches end of support.
- A lab no longer reproduces its expected results.
- A cross-chapter control or identifier is changed.

Dynamic sources should be checked at least quarterly. High-impact regulatory and product-security workstreams may need more frequent review.

## 10. Publication and validation

Before publication:
- Check source links and exact edition.
- Check internal links and references.
- Render or inspect Mermaid diagrams.
- Verify examples and commands in an isolated environment when possible.
- Review for secrets, customer data and non-public target details.
- Compare mappings to the current register.
- Update the project status and revision history.
- Record what was checked and what remains unverified.

A file creation or commit is not a technical validation result.
