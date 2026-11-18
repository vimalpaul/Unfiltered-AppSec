# Data Security and Privacy Engineering Lab Pack

| Field | Value |
|---|---|
| Document ID | UAPPSEC-08-LAB-001 |
| Status | Draft lab specifications |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Data discovery, classification, encryption, key management, privacy, retention, deletion, backups and monitoring |
| Classification | Public |

## 1. Safety, scope and lab environment

These labs are designed for local, isolated systems and synthetic data. Do not test against production databases, customer datasets, real personal data, live payment data, actual encryption keys or third-party processors without explicit written authorization and a reviewed test plan.

Mandatory safeguards:
- Use synthetic identities, records, keys and certificates.
- Run disposable containers or isolated VMs on loopback/private lab networks.
- Disable public ingress and uncontrolled egress.
- Never upload real personal data or secrets to hosted scanners or public sandboxes.
- Use mock KMS, object storage, email, analytics and processor endpoints.
- Limit resource use and avoid destructive tests outside the disposable lab.
- Keep secrets out of shell history, logs, screenshots and evidence.
- Capture sanitized evidence and remove test data after completion.
- Record exact image tags/digests, runtime versions, configuration and test date before claiming reproducibility.

The document defines specifications only. A lab is not validated until the environment is implemented, reset, executed and independently reproduced.

## 2. Common evidence record

For every lab record: lab ID, learner, date, environment/build, synthetic data set, roles, preconditions, exact procedure, expected result, observed result, sanitized evidence, root cause, remediation, regression test, residual risk, teardown and reviewer outcome.

## 3. Lab 01: Data discovery and inventory

**Objective:** Identify data stores and shadow copies across a synthetic application estate.

**Prerequisites:** Local sample application, database, object store emulator, log sink, cache and mock analytics service.

### Procedure

1. Create a synthetic data flow with customer profile, transaction and audit records.
2. List all deployed components and storage services.
3. Inspect database schemas, object buckets, cache keys, log events and analytics tables.
4. Identify exports, temporary files, queue messages and backup snapshots.
5. Trace each synthetic data element from source to destination.
6. Assign a data asset ID, owner, steward and classification.
7. Record purpose, access roles, region, retention and deletion behavior.
8. Compare observed stores with the initial inventory.
9. Create remediation items for unknown copies and ownerless data.
10. Repeat after introducing a new feature to test change-driven inventory updates.

**Expected result:** Material data stores and copies are discovered, owned and classified.

**Evidence:** Data inventory and lineage map.

**Teardown:** Destroy synthetic data and environment.

## 4. Lab 02: Classification and handling enforcement

**Objective:** Convert sensitivity labels into enforceable storage, access, logging and export controls.

**Prerequisites:** Synthetic public, internal, confidential and restricted records.

### Procedure

1. Define the lab's four classification levels and handling matrix.
2. Tag synthetic data assets and fields.
3. Configure a policy for storage, access and export.
4. Attempt to write restricted records to an unapproved store.
5. Attempt to export confidential fields using a low-privilege role.
6. Generate logs containing synthetic sensitive values.
7. Verify redaction and access restrictions.
8. Test that classification propagates to derived reports and exports.
9. Add CI/schema checks or policy-as-code for required labels.
10. Review exception workflow and expiry.

**Expected result:** Labels influence actual technical controls; no high-sensitivity asset is treated as public because of missing metadata.

**Evidence:** Policy configuration and positive/negative tests.

**Teardown:** Remove tags and synthetic records.

## 5. Lab 03: Data minimization and purpose limitation

**Objective:** Identify unnecessary collection and prevent secondary use without approval.

**Prerequisites:** Local registration/profile feature with synthetic fields.

### Procedure

1. Document the feature's stated business purpose.
2. List all fields collected by the UI and API.
3. Trace fields stored in database, logs and analytics.
4. Mark each field necessary, optional, redundant or unjustified.
5. Remove a deliberately unnecessary synthetic field from the collection flow.
6. Verify that hidden or extra client-supplied fields are not silently stored.
7. Separate product operations from analytics fields where appropriate.
8. Document any new use as a purpose change requiring privacy review.
9. Add schema and data collection regression tests.
10. Confirm existing required business behavior remains intact.

**Expected result:** Only justified data is collected and use is bounded to documented purposes.

**Evidence:** Field-purpose matrix and before/after schema.

**Teardown:** Reset sample application.

## 6. Lab 04: Tenant isolation in database and cache

**Objective:** Verify that tenant separation survives direct API, database query, cache and background-job paths.

**Prerequisites:** Two synthetic tenants, database, cache and worker.

### Procedure

1. Create identical synthetic record identifiers in two tenants where the schema permits.
2. Read each tenant's record through its authorized API.
3. Attempt cross-tenant reads through a manipulated request context in the lab.
4. Inspect repository queries and database row-level policies.
5. Test pooled database connections for tenant context leakage.
6. Inspect cache key construction and try the same logical key across tenants.
7. Enqueue a background job and verify tenant context is preserved.
8. Test report/export and search-index paths.
9. Correct any missing tenant predicates or context propagation.
10. Add regression tests for each storage and processing path.

**Expected result:** No cross-tenant record or cache disclosure; worker jobs preserve the correct tenant scope.

**Evidence:** Sanitized requests, query policies and test output.

**Teardown:** Drop test tenants and clear cache.

## 7. Lab 05: Database least privilege and sensitive access audit

**Objective:** Separate runtime, migration, reporting and administrative database privileges.

**Prerequisites:** Disposable relational database and synthetic schema.

### Procedure

1. Create distinct runtime, migration, reporting and administrator identities.
2. Define the minimum tables and operations each identity needs.
3. Connect using runtime identity and attempt schema modification.
4. Connect using reporting identity and attempt a write.
5. Attempt restricted table access with a low-privilege role.
6. Enable audit for sensitive table reads and privileged changes.
7. Verify application connection strings do not use administrator credentials.
8. Review grants, default roles and inherited permissions.
9. Add automated privilege tests to deployment checks.
10. Rotate and revoke one synthetic service credential.

**Expected result:** Runtime and reporting identities cannot perform administrative or unauthorized operations; privileged access is attributable.

**Evidence:** Grants, connection identity and audit records.

**Teardown:** Drop database and users.

## 8. Lab 06: TLS and certificate validation

**Objective:** Verify secure transport and correct peer identity validation for data services.

**Prerequisites:** Local TLS service, test CA and disposable certificates.

### Procedure

1. Configure a local service with a certificate for its expected hostname.
2. Connect using a client configured to validate trust and hostname.
3. Test an expired certificate.
4. Test a certificate for the wrong hostname.
5. Test an untrusted CA.
6. Test a valid replacement certificate and rotation without disabling validation.
7. Review protocol and cipher configuration against current organizational baseline.
8. Verify service-to-service clients fail closed when peer validation fails.
9. Add certificate expiry monitoring and owner metadata.
10. Record renewal and emergency replacement procedures.

**Expected result:** Only trusted, valid certificates for the expected service identity are accepted.

**Evidence:** Sanitized TLS handshake and configuration.

**Teardown:** Destroy test CA and certificates.

## 9. Lab 07: Authenticated encryption and ciphertext context binding

**Objective:** Verify that application-level encryption authenticates data and binds ciphertext to the intended record/tenant/field context.

**Safety:** Use a standard library and synthetic test keys only. Do not invent a cryptographic primitive.

### Procedure

1. Implement a small local encryption wrapper using a maintained AEAD library.
2. Generate a unique test key and nonce according to the selected algorithm's requirements.
3. Encrypt a synthetic field with associated data containing tenant ID, record ID and field name.
4. Decrypt using the exact same context and verify the plaintext.
5. Attempt decryption with a different tenant ID.
6. Attempt decryption with a different record ID or field name.
7. Modify ciphertext and authentication tag in the test fixture.
8. Verify all altered-context and altered-ciphertext cases fail authentication.
9. Record key ID, algorithm version, nonce and tag metadata without exposing key material.
10. Add regression tests and document key rotation compatibility.

**Expected result:** Ciphertext cannot be moved between records/tenants/fields undetected; altered data fails authentication.

**Evidence:** Test output and code review. Never include raw keys.

**Teardown:** Destroy test key.

## 10. Lab 08: Key vault access and separation of duties

**Objective:** Verify that application workloads can use approved cryptographic operations without broad key administration or raw key export.

**Prerequisites:** Local mock KMS or approved cloud test vault and synthetic workload identities.

### Procedure

1. Create separate test keys for development and test environments.
2. Create a workload identity with permission to encrypt/decrypt only the designated test resource.
3. Create a separate key administrator identity.
4. Verify the workload can perform the intended operation.
5. Attempt key export, policy change and key deletion using the workload identity.
6. Attempt use of the development key from the test identity.
7. Review audit records for key operations and denied requests.
8. Configure key policy and environment separation.
9. Test emergency revocation and application behavior.
10. Document recovery and break-glass approval.

**Expected result:** Workloads can perform only required cryptographic operations; administration and key export are separated.

**Evidence:** Redacted key policies and audit events.

**Teardown:** Delete test keys and identities.

## 11. Lab 09: Key rotation and compromise response

**Objective:** Exercise routine key rotation and emergency compromise handling without losing access to synthetic data.

**Prerequisites:** Local encrypted data set, mock KMS and two test key versions.

### Procedure

1. Encrypt a synthetic data set with key version A.
2. Create key version B and configure new writes to use B.
3. Verify old data can be read under the approved migration strategy.
4. Re-encrypt selected synthetic records with B.
5. Simulate compromise of A by marking it compromised in the lab.
6. Disable new encryption use of A and restrict decrypt operations.
7. Re-encrypt or isolate remaining data according to the response plan.
8. Review backup and replica key dependencies.
9. Verify old key destruction is blocked until recovery and retention conditions are satisfied.
10. Record timeline, approvals and audit evidence.

**Expected result:** New writes use the replacement key; compromised key is contained; data remains recoverable under a documented plan.

**Evidence:** Key lifecycle events and migration report.

**Teardown:** Destroy both test keys after deleting data.

## 12. Lab 10: Password storage and verification

**Objective:** Confirm that user passwords are stored with an adaptive password hashing scheme, not reversible encryption or fast unsalted hashes.

**Prerequisites:** Local authentication service and synthetic users.

### Procedure

1. Register a synthetic user with a test password.
2. Inspect the stored password representation without exporting it into evidence.
3. Identify the password hashing algorithm and parameters.
4. Verify a unique salt is used.
5. Review cost parameters against current platform guidance and performance budget.
6. Verify login compares through the approved password verification function.
7. Test password reset and credential migration behavior.
8. Check logs and error telemetry for password leakage.
9. Add tests preventing plaintext/reversible password storage.
10. Document upgrade strategy for older hashes.

**Expected result:** Passwords use a suitable adaptive password KDF with unique salts and safe verification; plaintext and reversible storage are absent.

**Evidence:** Redacted algorithm/parameter report and tests.

**Teardown:** Delete synthetic users.

## 13. Lab 11: Sensitive logging and telemetry redaction

**Objective:** Prevent secrets and unnecessary personal data from leaking into logs, traces and crash reports.

**Prerequisites:** Local app, log collector and synthetic secrets/identifiers.

### Procedure

1. Create a test request containing synthetic email, access token, session cookie and API key markers.
2. Trigger normal and error paths.
3. Inspect application, gateway, trace, metric label and crash logs.
4. Identify sensitive values in URLs, headers, structured fields and exception messages.
5. Implement centralized redaction before telemetry leaves the process.
6. Replace identifiers with safe correlation tokens where required.
7. Restrict log search and export roles.
8. Apply retention and deletion to test logs.
9. Add automated log-leak tests.
10. Verify security investigations retain useful correlation without full sensitive payloads.

**Expected result:** Secrets are never logged; unnecessary personal data is redacted and telemetry access is controlled.

**Evidence:** Sanitized log samples and regression output.

**Teardown:** Purge synthetic logs.

## 14. Lab 12: Masking and tokenization

**Objective:** Verify masking and tokenization are applied consistently across UI, API, reports and support tooling.

**Prerequisites:** Local synthetic account/identity dataset and token vault mock.

### Procedure

1. Create synthetic records containing fake identifiers.
2. Define roles allowed to view full versus masked values.
3. Inspect UI rendering.
4. Inspect API responses and browser network payloads.
5. Generate report/export and support view.
6. Attempt detokenization with an unauthorized role.
7. Verify token mapping is stored separately and access is audited.
8. Apply masking at the server/API boundary rather than UI only.
9. Test token collision, invalid token and revoked mapping behavior.
10. Document re-identification risk and retention of token mappings.

**Expected result:** Unauthorized channels never expose raw values; token vault and detokenization are restricted.

**Evidence:** Redacted UI/API/export comparison and vault policy.

**Teardown:** Delete synthetic records and token mappings.

## 15. Lab 13: Anonymization and re-identification risk

**Objective:** Demonstrate why removing names alone does not establish anonymity.

**Prerequisites:** Synthetic dataset with quasi-identifiers and an auxiliary synthetic dataset.

### Procedure

1. Generate synthetic records with age band, postcode region, event date and occupation category.
2. Remove direct names and email fields.
3. Count unique combinations of quasi-identifiers.
4. Join against a separate synthetic auxiliary dataset.
5. Identify records that become distinguishable.
6. Apply generalization, suppression or aggregation.
7. Re-run uniqueness and linkage tests.
8. Evaluate small-group and longitudinal disclosure.
9. Document assumptions, adversary model and residual risk.
10. Approve the term “anonymized” only if the defined legal/technical assessment supports it.

**Expected result:** The team identifies linkage risk and does not equate direct identifier removal with anonymization.

**Evidence:** Synthetic uniqueness/linkage report.

**Teardown:** Destroy both synthetic datasets.

## 16. Lab 14: Retention and deletion propagation

**Objective:** Verify a deletion request or retention expiry reaches all mapped copies.

**Prerequisites:** Local app with database, cache, search index, object store, analytics and mock processor.

### Procedure

1. Create one synthetic subject and linked records across every store.
2. Record lineage and retention trigger.
3. Trigger a deletion request using a synthetic request identity.
4. Verify identity/scope and check legal-hold state.
5. Execute the deletion workflow.
6. Inspect primary database, cache, object store, search index, analytics and processor mock.
7. Verify queue/dead-letter and export paths.
8. Confirm a deletion marker is available to prevent restore/re-ingestion.
9. Record copies awaiting backup expiry and their expiry dates.
10. Generate a deletion completion report with explicit exceptions.

**Expected result:** Deletion reaches all in-scope stores and processors; backup exceptions are bounded, documented and access-restricted.

**Evidence:** Store-by-store deletion ledger.

**Teardown:** Destroy lab environment and test records.

## 17. Lab 15: Backup restore and deletion tombstones

**Objective:** Prevent a restore from silently reintroducing previously deleted synthetic data.

**Prerequisites:** Disposable database, backup snapshot and deletion ledger.

### Procedure

1. Create synthetic subject and records.
2. Take a lab backup.
3. Delete the subject and record a durable deletion tombstone.
4. Restore the pre-deletion backup into a separate isolated environment.
5. Apply the deletion ledger/tombstones before exposing restored data.
6. Search for the deleted subject and linked objects.
7. Verify downstream caches and indexes are rebuilt without deleted records.
8. Test backup access and key recovery controls.
9. Document immutable backup expiry and restore procedure.
10. Add a restore regression test.

**Expected result:** Deleted synthetic data is not reintroduced into active systems after recovery.

**Evidence:** Restore log and post-restore verification.

**Teardown:** Destroy restored environment and backup.

## 18. Lab 16: Legal hold and retention exception

**Objective:** Ensure a valid hold blocks deletion only for the approved scope and is released safely.

**Prerequisites:** Synthetic records and mock legal-hold workflow.

### Procedure

1. Create two synthetic records for separate data subjects.
2. Apply a hold to one record using an approved mock legal workflow.
3. Run retention expiry.
4. Verify the held record is preserved and the unrelated record is deleted.
5. Inspect access restrictions and audit of held data.
6. Release the hold through an authorized approval.
7. Re-run the deletion process.
8. Verify the record is deleted under the normal retention policy.
9. Review exception scope, owner and review date.
10. Add regression tests for hold creation, scope and release.

**Expected result:** Holds are narrow, authorized, audited and not used as indefinite blanket retention.

**Evidence:** Hold approvals, deletion results and audit.

**Teardown:** Delete all synthetic data.

## 19. Lab 17: Object storage exposure and signed URL controls

**Objective:** Verify private storage, scoped access and short-lived download links.

**Prerequisites:** Local object storage emulator and synthetic files.

### Procedure

1. Create private buckets/containers for two synthetic tenants.
2. Upload synthetic documents with tenant-specific object keys.
3. Verify anonymous access is denied.
4. Attempt cross-tenant object retrieval.
5. Generate a short-lived signed URL with narrow object and method scope.
6. Test after expiry and with a different HTTP method.
7. Test object key manipulation and unexpected content type.
8. Review public ACL and bucket policy changes.
9. Add access logging and expiry tests.
10. Verify delete covers object versions and replicas according to policy.

**Expected result:** Objects remain private; signed URLs are scoped, short-lived and revocable through the documented design.

**Evidence:** Policy and sanitized access tests.

**Teardown:** Delete buckets and test objects.

## 20. Lab 18: Processor and cross-border data flow review

**Objective:** Create a technically grounded processor and transfer assessment for a synthetic integration.

**Prerequisites:** Mock SaaS processor, data flow diagram and synthetic data contract.

### Procedure

1. Identify data sent to the mock processor.
2. Record purpose, data elements, subjects and classification.
3. Identify entity roles under the selected mock legal scenario.
4. Record hosting region, support access region and subprocessors.
5. Review encryption, access, logging, retention and deletion capabilities.
6. Test that only required fields are transmitted.
7. Test deletion and export response from the processor mock.
8. Document transfer mechanism/conditions for privacy/legal review.
9. Record breach notification and audit evidence obligations.
10. Create a reassessment trigger for region, purpose, subprocessor or service changes.

**Expected result:** The transfer has an owner, purpose, data minimization, technical safeguards, contractual controls and legal review.

**Evidence:** Processor assessment and data flow.

**Teardown:** Remove integration and synthetic records.

## 21. Lab 19: DLP and bulk export detection

**Objective:** Verify that unusual synthetic data exports are detected and handled.

**Safety:** Use a small, conservative number of synthetic records. Do not conduct bulk extraction from real systems.

### Procedure

1. Configure a local DLP or export-monitoring rule.
2. Create a synthetic dataset with marked test identifiers.
3. Perform an approved small export as an authorized analyst.
4. Perform a denied export as an unauthorized role.
5. Trigger a synthetic unusual-volume event within safe limits.
6. Verify alert includes identity, tenant, operation and data classification without full payload.
7. Test the incident workflow and containment action.
8. Tune false positives using normal lab activity.
9. Record policy exceptions and expiry.
10. Add regression test for alert generation and secret redaction.

**Expected result:** Unauthorized or anomalous exports are detected with actionable, data-minimizing telemetry.

**Evidence:** Synthetic alert and response record.

**Teardown:** Delete test export and alerts.

## 22. Lab 20: Data breach tabletop and technical response

**Objective:** Practice containment and impact analysis for a synthetic data exposure.

**Prerequisites:** Mock incident scenario, data inventory, logs, key inventory and processor register.

### Procedure

1. Introduce a scenario involving a synthetic exposed object-storage container or compromised service identity.
2. Identify the incident commander and privacy/legal escalation roles.
3. Preserve relevant access, key and configuration logs.
4. Determine data classes, tenants, processors and copies affected.
5. Revoke the synthetic credential or close the exposed access path.
6. Assess whether encryption keys or plaintext copies were exposed.
7. Determine affected jurisdictions and applicable notification decision owners.
8. Validate recovery, key rotation and deletion/containment steps.
9. Draft a factual incident timeline and notification decision record.
10. Conduct a lessons-learned review and create corrective actions.

**Expected result:** The team can scope, contain, preserve evidence and route legal notification decisions without guessing deadlines.

**Evidence:** Timeline, containment log and after-action report.

**Teardown:** Close mock incident and reset lab credentials.

## 23. Assessment rubric

| Criterion | Points |
|---|---:|
| Discovers and classifies data stores and lineage | 15 |
| Applies minimization, purpose and access controls | 15 |
| Correctly implements encryption and key lifecycle | 20 |
| Handles retention, deletion and backup edge cases | 20 |
| Assesses privacy, processors and transfer context | 10 |
| Captures evidence and monitoring outcomes | 10 |
| Completes safe teardown and documents limitations | 10 |
| **Total** | **100** |

Suggested training interpretation: 90–100 strong independent engineering; 75–89 competent with review; 60–74 guided remediation required; below 60 repeat the exercise. These are training thresholds, not certification.

## 24. Instructor review checklist

- Were only synthetic data and disposable keys used?
- Did the learner map secondary copies and derived data?
- Did classification drive enforcement?
- Was tenant isolation tested beyond the API/UI?
- Were encryption and key management reviewed separately?
- Was key rotation tested without premature destruction?
- Were logs, traces and crash data inspected?
- Was masking distinguished from anonymization?
- Did deletion cover processors, indexes, caches and backup restore?
- Were legal holds scoped and released correctly?
- Were legal applicability and deadlines escalated to qualified reviewers?
- Was all evidence sanitized and the environment destroyed?

## 25. References

1. NIST Privacy Framework: https://www.nist.gov/privacy-framework
2. NIST SP 800-57 Part 1 Rev. 5: https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
3. NIST SP 800-88 Rev. 2: https://csrc.nist.gov/pubs/sp/800/88/r2/final
4. OWASP Cryptographic Storage Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
5. OWASP Key Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html
6. India DPDP Rules 2025 official information: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190655
7. EU GDPR: https://eur-lex.europa.eu/eli/reg/2016/679/oj

## 26. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial data security and privacy lab specifications |
