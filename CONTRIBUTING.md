# Contributing to Unfiltered AppSec

## Contribution principles

Contributions must improve technical accuracy, practical reproducibility, traceability or navigability. Avoid shallow summaries, duplicated material and unsupported claims.

## Before contributing

1. Read the project charter, architecture and research-quality method.
2. Confirm the target chapter and whether the content already exists.
3. Identify the intended audience, technology, lifecycle stage and jurisdiction.
4. Prefer a primary source and capture its exact edition, publication date and canonical URL.
5. Check whether the source is current, draft, final, superseded, withdrawn or historical.

## Required quality for a substantial playbook

Include the dimensions that are relevant to the topic: purpose and scope; architecture and dependencies; assets, identities and data; trust boundaries; threat and failure scenarios; business impact; requirements; controls; implementation guidance; validation and evidence; operations; standards and regulatory relationships; limitations; sources; owner and review triggers.

Procedures must include authorization, prerequisites, scope and exclusions, tools and configuration, steps, expected results, evidence, stop conditions, remediation, rollback, retest and closure criteria.

## Source quality

Use evidence grades:

- **A:** law, regulator, official standards publisher, national CERT, official vendor documentation or original advisory.
- **B:** peer-reviewed research or a strong recognized technical body.
- **C:** reputable specialist analysis, independently corroborated.
- **D:** community claim or unverified lead. Do not use grade D as sole support for high-impact conclusions.

Do not invent citations, CVEs, control identifiers, dates, capabilities, test outcomes or incident attribution. Clearly label assumptions, analysis, recommendations and illustrative examples.

## Regulatory content

Identify country, sector, regulated activity, issuing authority, exact instrument, publication and effective dates, applicability conditions, exclusions, amendments and official source. Distinguish binding law, mandatory regulator requirements, contract, standards, guidance and good practice. Do not claim that an organization is compliant based on a crosswalk.

## Safety and public repository restrictions

- Use deliberately vulnerable applications, local containers or isolated test networks.
- Do not publish exploit chains against live third-party targets, real credentials, access tokens, secrets, private keys, production data, customer-specific findings or non-public architecture.
- For real assessments, require written authorization, a rules-of-engagement document, defined test window, excluded systems, non-destructive limits, emergency contacts and a stop procedure.
- Avoid destructive payloads, denial-of-service testing and persistence instructions unless a separate controlled lab explicitly requires them and the scope is demonstrably isolated.
- Sanitize logs, screenshots, request/response samples and evidence before publication.

## Documentation metadata

Substantial documents should include title, document ID, status, version, owner, created date, last reviewed date, review due date, scope, classification and source links. Do not invent approvals or reviewer identities.

## Pull requests and review

A contribution should explain the technical change, source basis, affected chapters, changed mappings and tests performed. Review Markdown links and Mermaid syntax. Check that the content does not contradict the status register or another chapter. Do not claim external validation unless it was actually performed.
