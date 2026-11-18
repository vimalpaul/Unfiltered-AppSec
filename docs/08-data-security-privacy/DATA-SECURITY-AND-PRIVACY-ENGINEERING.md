# Data Security and Privacy Engineering Playbook

| Field | Value |
|---|---|
| Document ID | UAPPSEC-08-001 |
| Status | Draft engineering baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Data discovery, classification, lifecycle, cryptography, key management, privacy engineering, data access, retention, deletion and breach readiness |
| Classification | Public |

## 1. Executive summary

Data security and privacy engineering protect information throughout its lifecycle: collection, creation, use, transformation, storage, sharing, transfer, backup, archival, retention and disposal. The control objective is not simply to encrypt a database. It is to ensure that the organization knows what data it holds, why it holds it, who may use it, where it flows, how it is protected, when it must be deleted, and how it can prove that the rules are enforced.

Security and privacy are related but not interchangeable:
- **Security** protects confidentiality, integrity and availability against unauthorized access, change, loss and disruption.
- **Privacy** addresses appropriate and accountable processing of information about people, including purpose, transparency, choice or other lawful basis, minimization, rights, retention, sharing and impact.
- **Data governance** assigns ownership, quality, classification, stewardship, lineage and lifecycle accountability.
- **Cryptography** provides specific security properties when algorithms, protocols, keys, endpoints and operational procedures are correctly selected and managed.

Encryption does not make excessive collection appropriate. Pseudonymization does not automatically make data anonymous. A deleted database row may remain in logs, caches, replicas, exports, backups or downstream processors. A data retention policy is ineffective unless it is implemented in every system that stores or derives the data.

The core engineering principle is:

**Know the data, constrain its purpose and movement, minimize what is retained, enforce access at every boundary, protect keys separately from data, and verify deletion and recovery across the entire data estate.**

## 2. Purpose, audience and applicability

This chapter is for application security engineers, privacy engineers, security architects, developers, data platform teams, database administrators, cloud engineers, product owners, compliance teams, incident responders and auditors.

It applies to:
- Relational and non-relational databases.
- Files, object storage, document stores and content repositories.
- Data warehouses, lakes, analytics platforms and search indexes.
- Logs, telemetry, traces, crash dumps and support exports.
- Backups, snapshots, replicas, archives and disaster recovery copies.
- Caches, queues, event streams and temporary storage.
- SaaS integrations, data processors and third-party APIs.
- AI/ML datasets, embeddings, vector stores, prompts and model outputs.
- Secrets, encryption keys, certificates and signing material.
- Personal, financial, health, authentication, business-confidential and regulated data.

Applicability of a law or standard depends on jurisdiction, entity role, data type, processing purpose, sector, contract, transfer route and effective date. This playbook is an engineering reference, not legal advice.

## 3. Core concepts and distinctions

### 3.1 Data categories

| Category | Meaning | Example | Engineering implication |
|---|---|---|---|
| Public | Approved for unrestricted disclosure | Published product brochure | Integrity and availability still matter |
| Internal | Non-public routine business data | Internal procedure | Access controls and approved sharing |
| Confidential | Disclosure could harm business or individuals | Customer contract, source code | Restricted access, encryption and audit |
| Restricted | Highest-impact or regulated data | Authentication secrets, payment data, sensitive personal data | Strong isolation, explicit access, enhanced monitoring and strict retention |
| Personal data | Information relating to an identified or identifiable person under applicable law | Name, contact details, account identifier linked to a person | Purpose, transparency, rights, minimization and lawful processing |
| Sensitive/special-category data | A legally defined higher-protection category in a jurisdiction | Health, biometric or other specially protected data depending on law | Additional legal basis and safeguards may apply |
| Pseudonymized data | Direct identifiers replaced with separately controlled values | Tokenized customer reference | Re-identification remains possible using additional information |
| Anonymized data | Data altered so individuals are not reasonably identifiable under the applicable test and context | Aggregated statistics with disclosure controls | Must assess linkage, singling-out and auxiliary data risk |

Do not use one global sensitivity label as a substitute for jurisdiction-specific legal classification.

### 3.2 Data, metadata and derived data

Treat metadata and derived data as potentially sensitive:
- filenames, paths, timestamps and location;
- account IDs, tenant IDs and stable device identifiers;
- logs, traces and analytics events;
- search indexes and embeddings;
- risk scores, profiles and inferred attributes;
- backups, exports, screenshots and support bundles;
- model prompts, retrieval context and outputs.

A derived record may remain personal or confidential even if direct identifiers are removed.

### 3.3 Data roles

Identify the roles defined by each applicable legal regime, for example controller/processor, data fiduciary/data processor, business/service provider or equivalent. Do not assume terms are interchangeable across statutes. Contracts and actual decision-making determine role; product labels alone do not.

## 4. Data governance and ownership

### 4.1 Accountability model

Assign:
- **Business data owner:** accountable for purpose, access, quality, retention and risk acceptance.
- **Data steward:** maintains definitions, classification, lineage and quality.
- **System owner:** implements technical controls in each application/platform.
- **Privacy/legal owner:** interprets applicable obligations and rights.
- **Security owner:** defines security requirements and assurance.
- **Processor/vendor owner:** oversees third-party processing and contractual safeguards.
- **Records owner:** manages statutory, contractual and business record retention.
- **Incident owner:** coordinates data breach assessment and response.

One person may hold multiple roles in a small organization, but the responsibilities must remain explicit.

### 4.2 Data inventory schema

Maintain at least:
- Data asset ID and canonical name.
- Business owner, steward and technical owner.
- Data subjects and affected populations, where applicable.
- Data elements and sensitivity classification.
- Purpose and lawful basis/authority as validated by privacy/legal teams.
- Collection source and collection point.
- System of record and downstream copies.
- Storage location, region and residency constraints.
- Processors, recipients and transfer destinations.
- Access roles, service identities and privileged pathways.
- Encryption and key-management design.
- Retention trigger, retention duration and legal hold process.
- Deletion method and evidence.
- Backup/replica/cache/log coverage.
- Data quality and accuracy controls.
- Risk assessment/DPIA reference.
- Contract/regulatory obligations.
- Last review date and change trigger.

### 4.3 Data lineage

Map source-to-destination flows, transformations and copies. Include synchronous APIs, event streams, ETL/ELT, analytics, exports, support tools, observability, test data and vendor transfers. For each edge record:
- source and destination;
- data elements and classification;
- purpose;
- protocol and encryption;
- identity and authorization;
- transformation, masking or tokenization;
- retention at destination;
- error/retry/dead-letter behavior;
- owner and evidence.

~~~mermaid
flowchart LR
    SRC[Collection / Source] --> APP[Application]
    APP --> DB[(Primary database)]
    APP --> CACHE[(Cache)]
    APP --> LOG[Logs and traces]
    DB --> REPL[Replica]
    DB --> DWH[Warehouse / Analytics]
    APP --> OBJ[Object storage]
    APP --> VENDOR[Processor / Partner]
    DB --> BACKUP[Backup / Archive]
    DWH --> MODEL[ML / Vector / Derived data]
    MODEL --> APP
~~~

This diagram is a starting point. A production inventory must show actual regions, accounts, tenants, processors and trust boundaries.

## 5. Data lifecycle engineering

For every data class, define controls at each stage.

| Lifecycle stage | Required engineering questions |
|---|---|
| Collection | Is the field necessary? Is the source trusted? Is notice/consent or another authority handled? |
| Ingestion | Is schema validation performed? Are secrets and unexpected fields rejected? |
| Use | Is access purpose-limited? Is authorization checked at the data layer? |
| Transformation | Are classification and lineage retained? Can transformations re-identify? |
| Storage | Is encryption, isolation, integrity and backup configured? |
| Sharing | Is recipient authorized? Is the minimum necessary data shared? |
| Transfer | Are location, contract, transfer mechanism and security validated? |
| Retention | Is a clear trigger and duration assigned? |
| Archival | Is access restricted and retrieval monitored? |
| Deletion | Are primary, derived, cached and backup copies covered? |
| Disposal | Is media sanitization appropriate and evidenced? |

### 5.1 Collection minimization

- Define required fields from product purpose and business requirements.
- Avoid collecting fields merely because they might be useful later.
- Prefer coarse values where exact values are unnecessary.
- Do not collect sensitive data by default.
- Make optional fields genuinely optional.
- Avoid copying identity documents unless necessary and authorized.
- Separate product analytics from identity data when feasible.
- Prevent client-controlled hidden fields from expanding collection.
- Reassess collection when features or purposes change.

### 5.2 Purpose limitation and use controls

- Bind data access to approved use cases and roles.
- Separate operational access from analytics and marketing access.
- Do not reuse production data in development/test by default.
- Gate sensitive exports and bulk queries.
- Record access to high-impact data.
- Review new features for secondary use and profiling implications.
- Enforce purpose through workflow, policy and technical boundaries where feasible.

### 5.3 Data quality and integrity

- Validate authoritative sources and input provenance.
- Define field-level validation and normalization.
- Protect critical records against unauthorized modification.
- Use transactional constraints and audit history.
- Detect conflicting updates and stale records.
- Provide correction mechanisms where required.
- Avoid treating a checksum alone as proof of authenticity if an attacker can alter both data and checksum.

## 6. Data classification and handling standard

Create a handling matrix for each sensitivity class:
- approved storage platforms;
- encryption requirements;
- identity and access restrictions;
- external sharing conditions;
- logging/redaction rules;
- permitted analytics and AI use;
- test-data restrictions;
- retention and deletion;
- backup and recovery;
- incident notification path.

Classification must be machine-actionable where practical. Tags, schemas, catalog metadata and policy engines should drive storage, access, DLP, retention and export controls. Labels without enforcement are only documentation.

## 7. Data access and isolation

### 7.1 Least privilege

- Assign access to roles and service identities based on business need.
- Separate read, write, export, administer and key-management permissions.
- Use short-lived, scoped access for support and emergency operations.
- Review dormant accounts and inherited permissions.
- Require approval for bulk access and sensitive production queries.
- Use just-in-time access for privileged operations where feasible.
- Prevent shared database accounts where accountability is required.
- Monitor service identities and rotate credentials.

### 7.2 Tenant isolation

For multi-tenant systems:
- Resolve tenant context from trusted authentication/membership data.
- Enforce tenant scope in repository/query layer, not only UI or controller filters.
- Use database row-level security where appropriate, but verify bypass roles and connection pooling behavior.
- Include tenant identity in cache keys, object paths, search indexes and event metadata.
- Test exports, reports, background jobs and admin support tooling.
- Prevent cross-tenant foreign keys and relationship edges.
- Ensure analytics aggregation does not leak small-group data.
- Test backup restore and support workflows for tenant isolation.

### 7.3 Privileged data access

Use separate workflows for:
- production database administration;
- customer support impersonation;
- incident response;
- legal hold and e-discovery;
- bulk export;
- key and secrets administration.

Require explicit purpose, approval where appropriate, time limits, strong authentication, audit and post-access review.

## 8. Cryptographic architecture

### 8.1 Start with a threat model

Before selecting cryptography, identify:
- data to protect and its classification;
- attacker capabilities and trust boundaries;
- required confidentiality, integrity, authenticity and non-repudiation properties;
- data lifetime and cryptographic lifetime;
- endpoint and key compromise scenarios;
- recovery and availability requirements;
- performance and scale constraints;
- interoperability and regulatory/contractual requirements;
- future migration and cryptographic agility.

Do not select algorithms solely because a vendor checkbox says “AES enabled”.

### 8.2 Cryptographic controls by data state

| Data state | Controls |
|---|---|
| In transit | TLS with current secure configuration, certificate validation, mutual TLS where justified |
| At rest | Database/storage encryption, volume encryption and application-level encryption where threat model requires |
| In use | Process isolation, access controls, confidential computing only where justified, memory/secret minimization |
| Backups | Encryption, separate access, protected keys and tested restore |
| Exports | Strong access controls, encryption, expiry and audit |
| Application fields | Field-level encryption/tokenization when platform-level controls do not sufficiently isolate |
| Passwords | Adaptive password hashing, never reversible encryption |
| Integrity | Authenticated encryption, MACs, digital signatures, hashes for defined integrity purposes |

### 8.3 Algorithm and mode selection

Use well-maintained cryptographic libraries and protocols. Prefer authenticated encryption with associated data (AEAD) for application data encryption, such as AES-GCM or ChaCha20-Poly1305 where supported by approved platform policy. Nonces/IVs must satisfy the algorithm's uniqueness requirements; nonce reuse with GCM can catastrophically compromise security.

Avoid:
- ECB mode;
- custom encryption algorithms;
- unauthenticated encryption without a separate integrity design;
- static or hard-coded keys;
- predictable random numbers;
- password-based encryption without a suitable password KDF and parameters;
- obsolete protocols and ciphers;
- home-grown key derivation and encoding schemes.

Do not interpret “AES-256” as a complete security design. Mode, nonce generation, key storage, authentication, rotation, error handling and implementation matter.

### 8.4 Encryption envelope pattern

~~~mermaid
flowchart TD
    P[Plaintext data] --> DEK[Generate unique data encryption key]
    DEK --> AEAD[AEAD encrypt with unique nonce and context]
    P --> AEAD
    AEAD --> CT[Ciphertext + nonce + tag]
    DEK --> KMS[Wrap DEK with key-encryption key]
    KMS --> WDEK[Wrapped DEK]
    CT --> STORE[(Data store)]
    WDEK --> STORE
    STORE --> LOAD[Authorized read]
    LOAD --> KMS
    KMS --> UNWRAP[Unwrap DEK]
    UNWRAP --> DEC[Verify tag and decrypt]
    LOAD --> DEC
    DEC --> OUT[Plaintext only in authorized process]
~~~

Store algorithm/version metadata, key identifier, nonce, authentication tag and required associated context. Bind ciphertext to record identity, tenant, field or purpose using AEAD associated data where appropriate. This can prevent ciphertext swapping between records if the context is correctly enforced.

### 8.5 Hashing, encryption and tokenization

- **Encryption** is reversible with the correct key.
- **Hashing** is one-way by design, but low-entropy values can be guessed.
- **Password hashing** uses an adaptive password KDF such as Argon2id, scrypt, bcrypt or PBKDF2 under a documented policy.
- **HMAC** provides keyed integrity/authentication for data when used correctly.
- **Tokenization** substitutes a value with a token; the token vault and mapping remain sensitive.
- **Masking** obscures values for display or controlled use; it does not necessarily remove re-identification risk.
- **Pseudonymization** reduces direct identifiability but does not automatically remove legal personal-data status.
- **Anonymization** requires a context-aware assessment of re-identification risk.

Never store passwords using reversible encryption. Use a password-storage algorithm and unique salt per password; consider a separately protected pepper only with a defined operational recovery/rotation plan.

## 9. Key management engineering

### 9.1 Key lifecycle

~~~mermaid
stateDiagram-v2
    [*] --> Generated
    Generated --> PendingActivation
    PendingActivation --> Active
    Active --> Rotating
    Rotating --> Active
    Active --> Suspended
    Active --> Compromised
    Suspended --> Active
    Suspended --> Deactivated
    Compromised --> Deactivated
    Deactivated --> Archived
    Archived --> Destroyed
    Deactivated --> Destroyed
    Destroyed --> [*]
~~~

Define controlled states, authorized transitions and evidence. A key lifecycle includes generation, registration, distribution, activation, use, backup/recovery, rotation, suspension, compromise response, deactivation, archival and destruction.

### 9.2 Key hierarchy and separation

- Separate data-encryption keys (DEKs) from key-encryption keys (KEKs).
- Use a managed KMS/HSM or equivalent protected key service for high-impact keys.
- Separate production, test and development key hierarchies.
- Separate tenant keys where risk and architecture require it.
- Separate signing, encryption, MAC and TLS key purposes.
- Do not reuse a key across unrelated protocols or purposes.
- Restrict decrypt permissions more tightly than ordinary application read access where possible.
- Keep key metadata and audit separate from application data.
- Protect key backups and recovery material with equivalent controls.

### 9.3 Key storage and access

- Do not commit keys or secrets to source control, images or build artifacts.
- Do not store raw keys in ordinary configuration files.
- Prefer cloud KMS, HSM or dedicated secret/key management services.
- Use workload identity rather than long-lived static cloud credentials.
- Restrict key use by application identity, environment, operation and resource.
- Avoid exporting raw keys; use cryptographic operations inside the vault where supported.
- Monitor key reads, decrypt operations, policy changes and exports.
- Protect break-glass access and review it after use.

### 9.4 Rotation and compromise

Define routine rotation based on cryptoperiod, exposure, risk, vendor guidance and operational constraints. Rotate immediately when compromise is suspected or confirmed. Rotation must address:
- new encryption operations;
- old ciphertext decryption;
- key identifiers and version metadata;
- replicas, backups and archives;
- cached DEKs and application memory;
- dependent services and integrations;
- rollback and recovery;
- evidence and audit.

Do not destroy an old key before all required data migration, retention and recovery obligations are addressed. Conversely, do not keep decryption keys indefinitely without a documented reason and restricted access.

### 9.5 Cryptographic agility and post-quantum readiness

Inventory algorithms, protocols, key sizes, certificates, libraries, HSM/KMS capabilities and data retention horizons. Identify long-lived confidential data vulnerable to “harvest now, decrypt later”. Track relevant NIST post-quantum cryptography standards and vendor migration roadmaps. Do not deploy experimental algorithms in production without approved standards, interoperability and risk review. Plan hybrid migration where required by authoritative guidance and ecosystem readiness.

## 10. TLS and certificate lifecycle

- Enforce current secure TLS configurations and remove obsolete protocol versions/ciphers.
- Validate certificate chains and hostnames.
- Automate issuance and renewal where possible.
- Track certificate owner, SANs, issuer, expiry, environment and dependencies.
- Protect private keys and prevent export where feasible.
- Monitor unexpected certificates and trust-store changes.
- Use mutual TLS for service identity only with lifecycle and authorization design.
- Define certificate revocation/compromise response and emergency replacement.
- Test expiry, rotation, trust-chain changes and service restart behavior.
- Avoid disabling certificate validation to “fix” connectivity.

## 11. Database and storage security

### 11.1 Database controls

- Use unique service identities and least-privilege database roles.
- Separate schema migration, application runtime and administrator identities.
- Use parameterized queries and safe ORM patterns.
- Encrypt connections and validate server identity.
- Enable storage encryption and protect underlying snapshots.
- Restrict network access and administrative endpoints.
- Protect database backups, logs, WAL/binlogs and exports.
- Audit privileged access and sensitive table operations.
- Apply row/column-level controls where appropriate and test bypass paths.
- Patch database engines and extensions.
- Disable default accounts and unnecessary features.
- Test restore integrity and access controls.

### 11.2 Object storage

- Block public access by default.
- Use scoped workload identities and bucket/container policies.
- Separate tenant/object namespaces and enforce authorization server-side.
- Use short-lived signed URLs with narrow method, object, expiry and content constraints.
- Prevent user-controlled object keys from escaping approved prefixes.
- Validate uploaded content and metadata.
- Apply malware/content inspection where appropriate.
- Protect versioning, lifecycle and replication configuration.
- Monitor public ACL/policy changes and unusual bulk reads.
- Ensure delete operations include object versions and replicas where required.

### 11.3 Caches, queues and search indexes

Treat them as data stores:
- define classification and retention;
- enforce tenant-aware keys and ACLs;
- restrict administrative access;
- encrypt transport and storage where supported;
- prevent secrets in cache keys and message headers;
- control dead-letter queues and replay;
- expire stale records and indexes;
- propagate deletion and correction events;
- protect snapshots and diagnostic dumps.

## 12. Logs, telemetry and diagnostic data

Logs often become an uncontrolled shadow database. Define an explicit event schema and data policy.

- Do not log passwords, bearer tokens, API keys, private keys, session cookies or full payment credentials.
- Redact or tokenize personal data not needed for operations.
- Avoid sensitive values in URLs and query strings.
- Restrict log search/export by role and purpose.
- Apply retention and deletion to logs, traces, metrics labels and crash dumps.
- Review third-party telemetry and analytics SDK behavior.
- Protect log integrity and access.
- Prevent tenant data leakage in shared observability platforms.
- Use synthetic data in diagnostic bundles.
- Record approved exceptions and expiry.

## 13. Data masking, tokenization and anonymization

### 13.1 Masking

Use masking for display, support, lower environments and reporting. Masking must occur before data reaches a user or environment that should not see the original. UI-only masking is insufficient if the API, export or browser source still exposes full values.

### 13.2 Tokenization

Document:
- token generation and uniqueness;
- vault or mapping storage;
- token scope and format;
- detokenization permissions;
- availability and recovery;
- rotation and re-tokenization;
- audit and fraud monitoring;
- downstream and backup handling.

A token that preserves original format or can be linked to a person remains sensitive.

### 13.3 Anonymization assessment

Assess:
- direct identifiers;
- quasi-identifiers;
- uniqueness and rare combinations;
- linkage with public/third-party data;
- small cell sizes in aggregates;
- longitudinal linkability;
- location/time precision;
- adversary knowledge and available auxiliary data;
- re-identification cost and harm;
- intended recipient and release context.

Use aggregation, suppression, generalization, noise or formal privacy techniques as appropriate. A statement that data is “anonymized” requires evidence and periodic reassessment.

## 14. Privacy engineering and privacy by design

### 14.1 Privacy objectives

Use the NIST Privacy Framework concepts of predictability, manageability and disassociability alongside confidentiality, integrity and availability.

- **Predictability:** individuals and operators can form reliable expectations about data processing.
- **Manageability:** data can be administered, corrected, deleted and selectively disclosed.
- **Disassociability:** processing avoids linking data to individuals/devices beyond operational requirements.

### 14.2 Privacy requirements

For every feature, document:
- data elements and subjects;
- purpose and necessity;
- applicable authority/lawful basis as reviewed by privacy/legal;
- notice and transparency;
- consent or preference behavior where applicable;
- collection and use boundaries;
- sharing and processor relationships;
- retention and deletion;
- rights handling;
- security controls;
- cross-border transfers;
- impact and residual risks.

### 14.3 Privacy impact assessment / DPIA

Perform a screening when processing changes. Escalate to a formal DPIA/PIA where required by law or internal risk criteria, especially for:
- large-scale sensitive data;
- systematic monitoring;
- profiling or automated decisions;
- biometric or health data;
- children or vulnerable individuals;
- novel technology or AI;
- cross-border transfers;
- large-scale linkage or enrichment;
- high-impact decisions;
- unexpected secondary use.

A DPIA is not a one-time checkbox. Reassess after material changes, incidents, new recipients, new purposes or changes in scale.

### 14.4 Data subject rights engineering

Design workflows to locate and act on an individual's data across:
- primary records;
- related objects and identifiers;
- processors and vendors;
- search indexes and analytics;
- exports and support tools;
- derived profiles and embeddings;
- backups and archives, subject to applicable law and technically defined expiry.

Support identity verification, request authentication, scope validation, exceptions/holds, response deadlines, audit and secure delivery. Avoid revealing one person's data to another requester through weak identity matching.

## 15. Retention, archival and deletion

### 15.1 Retention schedule

For each record class define:
- purpose and record owner;
- retention trigger (creation, last activity, contract end, account closure, transaction completion);
- duration and source of requirement;
- legal hold and exception;
- archive location and access;
- deletion method;
- downstream copy handling;
- verification evidence;
- review cadence.

Do not use “retain forever” as a default. Do not delete records subject to a valid legal hold without authorized release.

### 15.2 Deletion workflow

~~~mermaid
flowchart TD
    REQ[Deletion / expiry trigger] --> VERIFY[Verify request, identity and scope]
    VERIFY --> HOLD{Legal or regulatory hold?}
    HOLD -- Yes --> EXC[Restrict access and document exception]
    HOLD -- No --> MAP[Resolve data lineage and copies]
    MAP --> DEL[Delete or irreversibly transform primary data]
    DEL --> DER[Propagate to caches, indexes, replicas and processors]
    DER --> BACK[Apply backup expiry / crypto-erasure policy]
    BACK --> VERIFYDEL[Verify deletion and exceptions]
    VERIFYDEL --> EVID[Record evidence and close request]
~~~

### 15.3 Deletion edge cases

Explicitly handle:
- soft-deleted rows;
- database replicas and snapshots;
- object versions and lifecycle copies;
- CDN and application caches;
- search indexes;
- analytics and warehouse tables;
- logs and traces;
- queue messages and dead-letter queues;
- exports and local downloads;
- support attachments;
- vendor/processor copies;
- model training datasets, embeddings and derived features;
- backups and immutable archives.

For backups, deletion may require expiry at the end of a defined backup retention cycle rather than selective rewriting. Document the approach, prevent normal restoration from reintroducing deleted data, and reapply deletion events after restore.

### 15.4 Media sanitization

Use a documented sanitization program appropriate to media, sensitivity and reuse/disposal scenario. NIST SP 800-88 Rev. 2 (September 2025) supersedes Rev. 1. Consider clear, purge and destroy methods based on media and risk. Cryptographic erase is valid only when the relevant encryption and key-copy assumptions are met; deleting one key reference is not proof that all plaintext or key copies are gone.

## 16. Backup, recovery and resilience

- Encrypt backup data and protect keys separately.
- Separate backup administration from production administration.
- Use immutable/offline copies where risk requires.
- Apply least privilege and multi-party approval for destructive backup actions.
- Monitor backup deletion, policy changes and restore events.
- Test restoration of both data and key access.
- Validate restored data integrity and tenant isolation.
- Reapply retention/deletion tombstones after restore.
- Protect backup catalogs, metadata and manifests.
- Define recovery point and recovery time objectives with business owners.
- Test ransomware and key compromise scenarios.
- Ensure backup copies do not silently violate residency or transfer commitments.

## 17. Data loss prevention and exfiltration controls

DLP is a supporting control, not a substitute for secure architecture. Use:
- classification-aware endpoint, email, SaaS and cloud controls;
- outbound export controls;
- bulk download monitoring;
- unusual query and database extraction detection;
- clipboard/print/download controls where appropriate;
- egress policy and proxy inspection;
- sensitive-data discovery and fingerprinting;
- alerting on public storage exposure;
- incident workflow and exception management.

Tune to business use. Overblocking can cause unsafe workarounds; underblocking creates blind spots. Monitor both effectiveness and false-positive burden.

## 18. Data security testing methodology

### 18.1 Assessment preparation

- Obtain written authorization and scope.
- Identify synthetic or approved data sets.
- Map data stores, copies and processors.
- Confirm test environment and data residency.
- Define prohibited destructive actions.
- Establish backup/restore and stop conditions.
- Avoid extracting real personal data; prove access with minimal synthetic records.
- Define evidence handling, redaction and retention.

### 18.2 Assessment phases

1. Data inventory and classification.
2. Data flow and lineage verification.
3. Purpose, minimization and privacy requirement review.
4. Access and tenant isolation testing.
5. Encryption and TLS configuration review.
6. Key management and rotation review.
7. Database/storage hardening.
8. Logging and telemetry data review.
9. Masking, tokenization and anonymization assessment.
10. Retention, deletion and legal hold testing.
11. Backup and restore verification.
12. Processor and transfer assessment.
13. DLP and exfiltration monitoring review.
14. Incident response and breach readiness.
15. Remediation and regression.

### 18.3 Data test catalogue

| Test ID | Area | Procedure focus | Expected result |
|---|---|---|---|
| DATA-T-001 | Inventory | Compare catalog, DB schemas, object stores, logs and processors | Material data stores and owners are recorded |
| DATA-T-002 | Classification | Trace sensitive fields through API, logs, analytics and exports | Classification follows data to derived copies |
| DATA-T-003 | Minimization | Review collection and request schemas against feature purpose | Unnecessary fields are not collected |
| DATA-T-004 | Tenant isolation | Access synthetic foreign-tenant records through APIs, reports and jobs | No unauthorized cross-tenant data |
| DATA-T-005 | Privileged access | Review roles, support paths and bulk query permissions | Access is least-privilege, approved and audited |
| DATA-T-006 | At-rest encryption | Verify platform, database, volume, object and backup settings | Required data stores are encrypted with controlled keys |
| DATA-T-007 | In-transit encryption | Validate TLS, certificate identity and service connections | Secure transport and peer validation enforced |
| DATA-T-008 | Application encryption | Review AEAD, nonce, tag and context binding | Authenticated encryption is correctly implemented |
| DATA-T-009 | Key storage | Inspect code, config, build artifacts and runtime identity | No exposed keys; managed storage and least privilege |
| DATA-T-010 | Key rotation | Exercise non-production rotation and old-ciphertext read | Rotation works without loss or indefinite key retention |
| DATA-T-011 | Key compromise | Simulate test-key compromise and emergency revocation | Response, replacement and audit work |
| DATA-T-012 | Password storage | Inspect password storage configuration and samples safely | Adaptive salted password hashing; no reversible storage |
| DATA-T-013 | Logging | Trigger synthetic sensitive events and inspect telemetry | Secrets and unnecessary personal data are redacted |
| DATA-T-014 | Masking | Compare UI, API, export and support views | Unauthorized channels do not reveal raw values |
| DATA-T-015 | Tokenization | Review token vault and detokenization permission | Mapping and re-identification are tightly controlled |
| DATA-T-016 | Anonymization | Evaluate linkage and small-cell risk using synthetic data | Claim is supported by documented re-identification assessment |
| DATA-T-017 | Retention | Seed expired synthetic records and run lifecycle job | Records expire according to approved schedule |
| DATA-T-018 | Deletion propagation | Delete synthetic subject and inspect all mapped stores | Copies and derived records follow deletion policy |
| DATA-T-019 | Backup restore | Restore a backup containing a prior deletion marker | Deleted data is not silently reintroduced |
| DATA-T-020 | Legal hold | Apply/release synthetic hold and verify deletion workflow | Hold blocks deletion only within approved scope |
| DATA-T-021 | Object storage | Review public access, signed URLs and object enumeration | Access is scoped and no unintended public objects |
| DATA-T-022 | Cache isolation | Compare same key across tenants and roles | No cross-tenant cache disclosure |
| DATA-T-023 | Processor | Review vendor data flow, contract and deletion evidence | Processor controls and responsibilities are documented |
| DATA-T-024 | Residency/transfer | Trace region and transfer destinations | Transfers follow validated requirements and contracts |
| DATA-T-025 | DLP | Trigger approved synthetic sensitive-data policy test | Detection and response operate as designed |
| DATA-T-026 | Restore key availability | Restore encrypted backup using recovery procedure | Authorized recovery works and is auditable |
| DATA-T-027 | Data integrity | Modify synthetic critical data through unauthorized path | Integrity control detects or prevents change |
| DATA-T-028 | Data export | Request bulk export with low-privilege identity | Export authorization, minimization and audit enforced |
| DATA-T-029 | AI/derived data | Trace synthetic personal data into embeddings and retrieval | Data purpose, access, retention and deletion propagate |
| DATA-T-030 | Secure disposal | Review media sanitization certificate and method | Sanitization is appropriate and evidenced |

## 19. Monitoring and detection engineering

| Detection ID | Scenario | Signals | Response |
|---|---|---|---|
| DATA-D-001 | Unusual bulk extraction | Large reads, exports or query volume by identity/tenant | Validate purpose, suspend access if warranted |
| DATA-D-002 | Cross-tenant access anomaly | Repeated foreign tenant/resource references | Investigate isolation policy and identity |
| DATA-D-003 | Key misuse | Unusual decrypt volume, key export or denied key operations | Restrict identity and investigate compromise |
| DATA-D-004 | Public storage exposure | ACL/policy changes or public object access | Contain exposure and assess affected data |
| DATA-D-005 | Sensitive logging | Secret/PII patterns in logs or traces | Restrict access, purge where feasible, fix instrumentation |
| DATA-D-006 | Retention job failure | Expired records remain or job stops | Restore job and assess compliance/impact |
| DATA-D-007 | Deletion propagation failure | Downstream copies remain after deletion event | Quarantine processing and remediate lineage |
| DATA-D-008 | Backup tampering | Unexpected deletion, retention or immutability changes | Protect recovery copies and investigate |
| DATA-D-009 | Privileged data access | Support/admin access outside approved window | Validate ticket, approval and operator |
| DATA-D-010 | DLP exfiltration | Sensitive content sent to unapproved destination | Contain transfer and invoke response |
| DATA-D-011 | Key rotation failure | Old key remains active beyond approved window | Complete migration or document exception |
| DATA-D-012 | Processor anomaly | Unexpected transfer, region or API destination | Suspend integration and engage vendor owner |

Alert rules must be calibrated against normal business operations. Preserve enough evidence for investigation without collecting the sensitive payload itself.

## 20. Data breach and privacy incident response

1. Identify affected data classes, systems, tenants, individuals and jurisdictions.
2. Preserve relevant logs, access records, key events and data lineage.
3. Determine whether confidentiality, integrity or availability was affected.
4. Identify access, exfiltration, alteration, loss or unauthorized disclosure.
5. Contain compromised identities, endpoints, keys, integrations and destinations.
6. Determine copies, processors, backups and derived datasets affected.
7. Assess legal notification duties and deadlines with privacy/legal counsel.
8. Evaluate individual, customer, regulator, contractual and sector notifications.
9. Restore data from trusted sources and reconcile unauthorized changes.
10. Address key rotation, deletion, credential revocation and monitoring.
11. Record decision rationale, evidence, notifications and timelines.
12. Add regression controls and review the data map and privacy assessment.

Do not assume every security incident is a reportable personal data breach, or that a breach is not reportable because encryption was enabled. Determine the facts and applicable law.

## 21. Third-party processors and data sharing

Before sharing:
- identify the recipient and actual role;
- document purpose and minimum data;
- assess security, privacy and subprocessor chain;
- establish contract and instructions;
- confirm region, transfer and onward-sharing conditions;
- define access, encryption, retention and deletion;
- define breach notification and cooperation;
- review audit/evidence rights;
- test offboarding and data return/deletion;
- review material changes and reassess periodically.

A vendor security certificate is evidence for a defined scope and period, not proof that a particular integration is safe or lawful.

## 22. AI/ML and derived-data security

Treat prompts, retrieval context, training corpora, embeddings, fine-tuning sets, model outputs, evaluation data and feedback as data assets.

Controls:
- classify training and inference data;
- establish purpose and rights/authority to use data;
- prevent cross-tenant retrieval;
- apply access controls at retrieval and tool boundaries;
- avoid placing secrets and unnecessary personal data in prompts;
- define provider retention and training-use settings contractually;
- manage deletion across source data, indexes and derived artifacts;
- assess memorization and extraction risk;
- restrict model/debug telemetry;
- monitor exports and retrieval anomalies;
- document limitations where machine unlearning or selective deletion cannot be guaranteed.

Deleting a source row does not automatically remove information already learned by a trained model. Record the model/data lineage and approved remediation options.

## 23. Industry scenarios

### 23.1 SaaS learning management platform

Data includes learner identity, course progress, assessment results, confidence responses, documents, reports, tenant configuration and audit events.

Controls:
- tenant-scoped access at database, API, cache, export and reporting layers;
- minimize learner profile fields;
- separate assessment answers from analytics where possible;
- protect reports and downloadable documents;
- define retention for inactive learners and completed assessments;
- prevent production learner records from entering development environments;
- audit administrator access and bulk exports;
- propagate deletion/correction to analytics and search indexes.

### 23.2 Healthcare application

Potential data includes patient identity, clinical records, appointments, diagnoses and health-related communications. Applicable health privacy rules depend on jurisdiction and provider role.

Controls:
- heightened classification and role-based/attribute-based access;
- emergency/break-glass access with reason and review;
- strong audit and anomaly detection;
- encryption and key separation;
- minimum necessary disclosure;
- retention and legal hold aligned to applicable health-record requirements;
- tested breach response and processor oversight.

### 23.3 Financial services

Data may include account, transaction, identity verification, payment and fraud records.

Controls:
- tokenization and segregation for payment data;
- strong privileged access and transaction integrity;
- restricted export and monitoring;
- auditable retention and legal hold;
- secure key management and recovery;
- supplier and payment ecosystem controls;
- jurisdiction-specific financial and payment requirements.

### 23.4 Industrial and OT-adjacent systems

Asset inventory, operator identity, access logs, maintenance records, engineering files and telemetry may be sensitive even where they are not personal data.

Controls:
- segment business IT, data platform and control-system zones;
- do not introduce general-purpose cloud analytics or agents into OT zones without architecture and safety approval;
- minimize sensitive topology and operational data exposure;
- protect engineering backups and configuration files;
- restrict remote support and data export;
- align retention and incident response with operational safety and availability requirements.

### 23.5 AI-enabled customer support

Prompts, transcripts, customer records, retrieval documents and generated summaries may contain sensitive data.

Controls:
- redact unnecessary identifiers;
- isolate tenant retrieval;
- prevent prompt injection from bypassing data access;
- control provider retention and model training use;
- apply deletion and retention to transcripts and vector stores;
- log policy decisions without copying full sensitive prompts;
- human-review high-impact decisions.

## 24. Standards and framework mapping

Mappings below describe relevance, not automatic compliance. Use the edition and applicability decision current at the time of assessment.

### 24.1 NIST Privacy Framework 1.0

Use the Core functions:
- Identify-P: understand data processing and privacy risk.
- Govern-P: establish policies, roles and risk strategy.
- Control-P: enable data processing permissions and individual choices/rights.
- Communicate-P: provide transparency and communication.
- Protect-P: safeguard data processing.

The framework is a risk-management tool, not a law or certification.

### 24.2 NIST SP 800-57 Part 1 Rev. 5

Use for cryptographic key management lifecycle, key types, protection, cryptoperiod, compromise, recovery and destruction. Validate algorithm and key-management choices against current NIST publications and organizational policy.

### 24.3 NIST SP 800-88 Rev. 2

Finalized September 2025; supersedes Rev. 1. Use for media sanitization program design and clear/purge/destroy method selection. Do not use an old Rev. 1 checklist as the current baseline without a documented reason.

### 24.4 OWASP ASVS 5.0.0

Use applicable requirements for cryptography, data protection, secrets, logging and privacy-relevant application behavior. Exact requirement IDs must be imported from the official versioned ASVS release before publishing a formal requirement-to-test crosswalk. Do not invent identifiers.

### 24.5 ISO/IEC 27001:2022 Annex A relevance

| Control | Theme | Data security relevance |
|---|---|---|
| 5.9 | Inventory of information and other associated assets | Data asset inventory and ownership |
| 5.12 | Classification of information | Classification and handling |
| 5.13 | Labelling of information | Machine-readable labels and handling |
| 5.14 | Information transfer | Secure sharing and transfer |
| 5.15–5.18 | Access control and identity | Data access and privilege lifecycle |
| 5.19–5.23 | Supplier and cloud services | Processor and hosted data governance |
| 5.31 | Legal, statutory, regulatory and contractual requirements | Retention, privacy and transfer obligations |
| 5.33 | Protection of records | Integrity, retention and disposal |
| 5.34 | Privacy and protection of PII | Personal information lifecycle |
| 8.10 | Information deletion | Deletion and sanitization |
| 8.11 | Data masking | Masking and pseudonymization |
| 8.12 | Data leakage prevention | Exfiltration controls |
| 8.13 | Information backup | Backup confidentiality and recovery |
| 8.15–8.16 | Logging and monitoring | Sensitive-data telemetry and detection |
| 8.24 | Use of cryptography | Cryptographic architecture and key governance |
| 8.25–8.29 | Secure development and testing | Data protection by design and verification |
| 8.33 | Test information | Synthetic/masked test data |

This relevance mapping does not establish that a control is implemented or that an organization is certified.

## 25. Regulatory considerations and applicability workflow

### 25.1 Applicability decision

For each processing activity determine:
1. Which legal entities determine purposes and means?
2. Where are the entity, individuals, systems and processors located?
3. Which data subjects and data categories are involved?
4. Is processing digital, automated, paper-based or mixed?
5. What is the entity's role under the relevant law?
6. What lawful basis/authority and notice/consent requirements apply?
7. Are sensitive, child, financial, health, biometric or government data involved?
8. Are there localization, transfer or sector rules?
9. What rights, retention, security and breach duties apply?
10. What commencement dates, exemptions and transitional periods apply?

### 25.2 India — Digital Personal Data Protection Act, 2023 and Rules, 2025

The DPDP Rules, 2025 were notified in November 2025. The government described phased commencement, so obligations must be checked against the specific provision and commencement schedule rather than assuming every requirement became effective on notification day. Use the Act, final Rules, Gazette notifications, corrigenda and current MeitY/official materials for legal interpretation.

Engineering workstreams to assess:
- notices and consent/other permitted processing basis;
- Data Principal rights request workflows;
- Data Fiduciary accountability and processor contracts;
- reasonable security safeguards;
- personal data breach response and notification;
- retention and erasure when purpose ceases, subject to applicable exceptions;
- children's data and applicable restrictions;
- Significant Data Fiduciary obligations where designated;
- cross-border transfer restrictions/conditions as notified;
- records and evidence.

Do not copy draft Rules deadlines into production procedures. Record the provision, Gazette instrument, effective date and legal reviewer in the compliance register.

### 25.3 European Union — GDPR

Where GDPR territorial and material scope applies, assess:
- principles and lawful bases;
- controller/processor roles and contracts;
- data protection by design and default;
- records of processing;
- security of processing;
- DPIA where required;
- data subject rights;
- personal data breach notification and communication;
- international transfers and transfer tools;
- retention, minimization and accountability.

GDPR does not prescribe one universal encryption algorithm or retention period. Translate obligations into risk-based technical and organizational controls.

### 25.4 Qatar

Where Qatar's Personal Data Privacy Protection Law No. 13 of 2016 and applicable rules/guidance apply, assess notice/consent and processing conditions, data subject rights, controller/processor responsibilities, security safeguards, breach handling and cross-border transfer requirements. Confirm the current regulator guidance and sector-specific requirements before formal implementation.

### 25.5 Saudi Arabia

Where the Saudi Personal Data Protection Law and Implementing Regulations apply, assess controller/processor obligations, purpose and lawful basis, data subject rights, records, security, breach reporting, retention/destruction and cross-border transfer rules. Confirm the current SDAIA/National Data Management Office materials and amendments; do not rely on an outdated transfer regulation or draft.

### 25.6 United Arab Emirates

Determine whether the federal Personal Data Protection Law applies or whether a free-zone or sector-specific regime governs, such as DIFC or ADGM data protection rules. Map controller/processor roles, security, rights, transfers, breach handling and retention to the correct regime.

### 25.7 Other jurisdictions and sector rules

Depending on footprint, assess UK GDPR/Data Protection Act, US state privacy laws, HIPAA where applicable, GLBA, PCI DSS, financial regulator rules, telecom rules, critical infrastructure requirements, contractual obligations and local records laws. A law's existence does not prove applicability to a specific entity.

## 26. Evidence and assurance

A data security assurance pack should contain:
- approved data inventory and lineage;
- classification and handling standard;
- processing activity/ROPA where applicable;
- privacy notices and purpose records;
- DPIA/PIA and risk decisions;
- access matrix and privileged access reviews;
- encryption architecture and configuration evidence;
- key inventory and lifecycle evidence;
- certificate inventory;
- database/storage hardening records;
- masking and test-data procedures;
- retention schedule and deletion test results;
- backup/restore and sanitization evidence;
- processor register and contracts;
- transfer assessments;
- incident and breach exercises;
- monitoring rules and sampled alerts;
- exceptions, owners and expiry dates.

Evidence must be time-bound, attributable, scoped and protected. Screenshots without configuration context or system identity are weak evidence.

## 27. Roles and operating model

| Activity | Accountable role | Supporting roles |
|---|---|---|
| Data purpose and retention | Business data owner | Privacy, legal, records, product |
| Classification and lineage | Data steward | Architecture, engineering, analytics |
| Privacy assessment | Privacy owner | Legal, product, security, engineering |
| Cryptographic standards | Security architect | Platform, cloud, application teams |
| Key lifecycle | KMS/HSM owner | Security operations, application owners |
| Data access | System/data owner | IAM, DBA, application team |
| Deletion propagation | Data owner | Engineering, platform, processor owner |
| Processor assurance | Vendor owner | Legal, privacy, security, procurement |
| Incident response | Incident commander | Privacy, legal, security, system owner |
| Compliance mapping | Compliance/legal owner | Data owner, security, privacy |

## 28. Implementation roadmap

### Foundation (0–30 days)
- Identify critical data systems and owners.
- Define classification and handling.
- Inventory keys, secrets and certificates.
- Identify public storage and sensitive logging.
- Map critical data flows and processors.
- Establish retention owners and immediate high-risk gaps.

### Control implementation (30–90 days)
- Enforce least-privilege data access.
- Implement managed key storage and rotation.
- Encrypt required data stores and connections.
- Introduce test-data masking/synthetic data.
- Add deletion workflows and processor obligations.
- Implement bulk export and sensitive access monitoring.

### Assurance and maturity (90–180 days)
- Automate data discovery and lineage where feasible.
- Test deletion propagation and backup restore.
- Conduct privacy impact assessments for high-risk processing.
- Validate key compromise and recovery exercises.
- Measure DLP, access review and retention effectiveness.
- Review cross-border and AI-derived data flows.
- Complete exact standards and regulatory traceability.

This roadmap is a planning model; prioritize based on risk and legal deadlines.

## 29. Related chapters

- [01. AppSec Fundamentals](../01-fundamentals/APPSEC-FUNDAMENTALS.md)
- [02. Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [03. Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [04. Secure Coding and Code Review](../04-secure-coding/SECURE-CODING-AND-CODE-REVIEW.md)
- [05. Web Application Security Engineering](../05-web-application-security/WEB-APPLICATION-SECURITY-ENGINEERING.md)
- [06. API and Service Security Engineering](../06-api-service-security/API-AND-SERVICE-SECURITY-ENGINEERING.md)
- [07. Identity and Access Security](../07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY.md)
- [08. Data Security and Privacy Lab Pack](DATA-SECURITY-AND-PRIVACY-LAB-PACK.md)
- [09. Mobile Application Security Engineering](../09-mobile-application-security/MOBILE-APPLICATION-SECURITY-ENGINEERING.md)
- [10. Cloud-Native Application Security Engineering](../10-cloud-native-application-security/CLOUD-NATIVE-APPLICATION-SECURITY-ENGINEERING.md)
- [09. Mobile Application Security Lab Pack](../09-mobile-application-security/MOBILE-APPLICATION-SECURITY-LAB-PACK.md)
- [18. Standards Baseline and Mapping Method](../18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md)
- [19. Global Regulatory Register](../19-global-regulatory/GLOBAL-REGULATORY-REGISTER.md)

## 30. References

1. NIST Privacy Framework 1.0: https://www.nist.gov/privacy-framework
2. NIST Privacy Framework 1.0 to India DPDP Act/Rules 2025 crosswalk: https://www.nist.gov/privacy-framework/nist-privacy-framework-10-digital-personal-data-protection-act-2023-and-rules-2025
3. NIST SP 800-57 Part 1 Rev. 5: https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
4. NIST SP 800-88 Rev. 2: https://csrc.nist.gov/pubs/sp/800/88/r2/final
5. NIST SP 800-53 Rev. 5: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
6. OWASP Cryptographic Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
7. OWASP Key Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html
8. OWASP Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
9. NIST SP 800-218 SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
10. India DPDP Rules 2025 official notification summary: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190655
11. EU GDPR: https://eur-lex.europa.eu/eli/reg/2016/679/oj
12. Qatar Personal Data Privacy Protection Law: https://www.almeezan.qa/
13. Saudi Personal Data Protection Law: https://dgp.sdaia.gov.sa/
14. UAE Personal Data Protection Law: https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws

## 31. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial data security and privacy engineering playbook |
