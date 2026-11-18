# Secure Coding Lab Pack

| Field | Value |
|---|---|
| Document ID | UAPPSEC-LAB-04-001 |
| Status | Draft lab specification |
| Version | 0.1 |
| Owner | Unfiltered AppSec |
| Created | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Isolated, synthetic secure coding exercises |
| Classification | Public |

## 1. Safety rules

These exercises use intentionally vulnerable local applications. They are not instructions to test public websites or customer systems.

- Use synthetic data and disposable containers or virtual machines.
- Bind vulnerable services to loopback or a private isolated network.
- Do not expose vulnerable services to the public Internet.
- Do not use production credentials, databases, storage or cloud identities.
- Snapshot or rebuild the environment before each exercise.
- Stop if traffic reaches a non-lab address or a real secret is discovered.
- Keep resource limits in place during denial-of-service demonstrations.
- Record evidence without secrets or personal data.

The learner identifies the weakness, documents its root cause, implements the fix and proves the regression test fails before the fix and passes afterward.

## 2. Common lab record

Record learner, date, lab ID, application and image versions, environment isolation, scope, vulnerable source location, synthetic test identity, reproduction steps, expected and observed behavior, root cause, CWE, remediation diff, regression test, evidence, teardown and reviewer outcome.

## 3. Lab 01: SQL injection and parameter binding

**Objective:** Demonstrate why concatenating untrusted input changes SQL structure and why parameter binding preserves query grammar.

**Weakness:** CWE-89.

**Prerequisites:** Local SQLite or disposable PostgreSQL database, small test API, synthetic records.

**Seed data:** Create two synthetic users, alice@example.test and bob@example.test, with non-sensitive dummy values.

### Vulnerable example

~~~python
# Deliberately vulnerable lab code. Never use in a real application.
def find_user(cursor, email):
    query = "SELECT id, email FROM users WHERE email = '" + email + "'"
    return cursor.execute(query).fetchall()
~~~

### Procedure

1. Start the application on loopback only.
2. Read the function and identify the data source and SQL sink.
3. Submit a normal email and record the exact-match result.
4. In the lab only, submit a benign quote-containing test value designed to alter the predicate, not to modify or delete data.
5. Observe whether returned rows differ from intended exact-match behavior.
6. Record query construction and result. Do not use stacked statements, destructive statements or external systems.
7. Replace concatenation with driver parameter binding.
8. Repeat the exact test input.
9. Confirm it is treated as a literal value and query structure does not change.
10. Add unit tests for normal, empty, quote-containing and unusually long values.

### Secure example

~~~python
def find_user(cursor, email):
    return cursor.execute(
        "SELECT id, email FROM users WHERE email = ?",
        (email,)
    ).fetchall()
~~~

Placeholder syntax varies by database driver. Verify the selected driver's documented binding format.

**Expected result:** The vulnerable version demonstrates altered query semantics. The fixed version treats the same input as data and does not broaden results.

**Evidence:** Source diff, test output, query trace with synthetic data and regression test.

**Teardown:** Stop the service and destroy the disposable database.

## 4. Lab 02: Output encoding and stored XSS

**Objective:** Identify unsafe HTML insertion and replace it with context-safe output.

**Weakness:** CWE-79.

**Prerequisites:** Local browser application with a comment or profile field.

### Vulnerable example

~~~javascript
// Deliberately vulnerable lab code.
messageContainer.innerHTML = userComment;
~~~

### Procedure

1. Start the local application with synthetic users.
2. Submit a harmless HTML marker that changes page structure but does not contact external hosts or access browser secrets.
3. Observe whether the browser interprets supplied content as markup.
4. Record the source, transformation and DOM sink.
5. Replace raw HTML insertion with textContent for plain text.
6. If rich text is required, configure a maintained allow-list sanitizer and document allowed elements and attributes.
7. Repeat with text, attribute-like characters and stored content viewed by a second synthetic role.
8. Add regression tests for reflected and stored content.

### Secure example

~~~javascript
messageContainer.textContent = userComment;
~~~

**Expected result:** Untrusted content is displayed as text, not interpreted as markup. Stored content remains inert when viewed by another role.

**Evidence:** Browser DOM before/after, code diff, test case and sanitizer policy if applicable.

**Teardown:** Remove synthetic comments and stop the local application.

## 5. Lab 03: Mass assignment and tenant authorization

**Objective:** Show why requests must not overwrite privileged entity properties and why object authorization is separate from authentication.

**Weaknesses:** CWE-915, CWE-862, CWE-863 and CWE-639.

**Prerequisites:** Local API, disposable database, two tenants and three synthetic users.

| Identity | Tenant | Role |
|---|---|---|
| learner-a | tenant-a | learner |
| admin-a | tenant-a | tenant administrator |
| learner-b | tenant-b | learner |

### Vulnerable design

A generic update endpoint deserializes a request directly into a persistence entity containing displayName, tenantId, role, isAdmin and status. A separate result endpoint loads a record by ID and checks only whether the caller is authenticated.

### Procedure

1. Sign in as learner-a and update an ordinary profile field.
2. In the local lab, add a privileged property such as role or tenantId to the request.
3. Inspect the synthetic record and determine whether server-controlled state changed.
4. Request learner-b's synthetic result by identifier while authenticated as learner-a.
5. Record whether the service checks only authentication or the user's resource relationship.
6. Implement an explicit request DTO containing only permitted profile fields.
7. Derive tenant and role from server-side membership and policy, never request input.
8. Add object-level authorization before read, update and export.
9. Add a database query constraint as defense in depth.
10. Repeat negative cases and verify no data or state change occurs.

**Expected result:** Privileged fields cannot be mass-assigned. Cross-tenant data access is denied. Legitimate operations continue to work.

**Evidence:** Before/after records, API responses, authorization decision and audit event.

**Teardown:** Destroy synthetic tenant records.

## 6. Lab 04: Path traversal and upload isolation

**Objective:** Verify that an uploaded filename cannot choose a path outside the storage root.

**Weaknesses:** CWE-22 and CWE-434.

### Procedure

1. Configure a private upload directory outside the web root.
2. Identify how the service derives its storage path.
3. Upload a normal synthetic file and record its server-side object identifier.
4. Test filename normalization using harmless traversal-shaped names in the isolated lab.
5. Verify storage uses a server-generated identifier, not the supplied name as a path.
6. Review canonicalization and symlink behavior where path operations remain.
7. Add file size, count, type and content checks.
8. Verify a download requires authorization against the stored object and tenant.
9. Verify rejected files are quarantined or deleted according to policy.
10. Test cleanup and retention behavior.

**Expected result:** User input cannot select an arbitrary filesystem path. Stored objects are private, uniquely named and authorization-checked.

**Evidence:** Storage layout, request/response, path resolution log and regression tests.

**Teardown:** Delete synthetic uploads and temporary directories.

## 7. Lab 05: SSRF destination policy

**Objective:** Verify a URL-fetch feature accepts only permitted destinations and does not follow redirects into prohibited address ranges.

**Weakness:** CWE-918.

**Prerequisites:** Local application and synthetic destination services on a private lab network. Do not use real cloud metadata endpoints or customer infrastructure.

### Procedure

1. Inventory the URL-fetch function and outbound HTTP client configuration.
2. Configure a lab allow-list containing one local test service name.
3. Configure a second synthetic destination that must be denied.
4. Submit the permitted destination and confirm intended content is fetched.
5. Submit the denied destination and confirm rejection occurs before or at the controlled egress boundary.
6. Configure a synthetic redirect from an allowed lab destination to the denied destination.
7. Verify the redirect is disabled or the new destination is independently revalidated.
8. Verify connect/read/overall timeouts and response-size limits.
9. Confirm inbound Authorization and Cookie headers are not forwarded.
10. Add regression tests for scheme, host, port, DNS result, redirect and response-size policy.

**Expected result:** Only approved destinations are reachable; redirects cannot bypass policy; resource use and credential forwarding are bounded.

**Evidence:** Client configuration, egress policy, destination decision and test output.

**Teardown:** Stop synthetic destination services and remove allow-list entries.

## 8. Lab 06: Unsafe deserialization and parser limits

**Objective:** Identify unsafe polymorphic/object deserialization and enforce data-only schema validation.

**Weaknesses:** CWE-502; XML parser risks may include CWE-611.

### Procedure

1. Identify the serializer, type metadata settings and allowed input schema.
2. Submit a normal documented data object.
3. Submit an object containing an unknown property or type marker.
4. Submit a deeply nested but small synthetic object.
5. Verify the parser rejects unknown types and enforces depth and size limits.
6. Review whether deserialization can instantiate arbitrary classes or invoke side-effecting behavior.
7. Replace unsafe object serialization with a data-only format and explicit DTO/schema.
8. For XML, verify external entity and external DTD resolution are disabled.
9. Add regression tests for malformed input, unknown types, excessive nesting and oversized payloads.

**Expected result:** Untrusted input cannot cause arbitrary type instantiation, external entity retrieval or unbounded parser resource use.

**Evidence:** Serializer configuration, rejected test payload metadata and regression results. Do not include dangerous serialized gadget payloads in public evidence.

**Teardown:** Delete payload fixtures and stop the parser service.

## 9. Lab 07: Race condition and idempotency

**Objective:** Ensure a one-time workflow transition can occur only once under concurrent requests.

**Prerequisites:** Local transactional database and synthetic assessment or coupon workflow.

### Procedure

1. Create one synthetic record in an eligible state.
2. Implement a test harness that sends two concurrent submissions for the same record.
3. Observe the vulnerable implementation if it checks state before a separate non-atomic update.
4. Record final state, duplicate events and duplicate side effects.
5. Implement a transaction with a conditional state update and version check, or equivalent atomic mechanism.
6. Require the application to verify exactly one row was updated.
7. Add an idempotency key bound to principal and operation if retries are part of the interface.
8. Repeat concurrent requests and retry tests.
9. Verify exactly one business transition and one associated side effect occur.

**Expected result:** Concurrent and repeated requests cannot create duplicate submissions or side effects.

**Evidence:** Test harness output, transaction log, final row state and event count.

**Teardown:** Rebuild the synthetic database.

## 10. Lab 08: Log injection and secret redaction

**Objective:** Ensure untrusted text cannot forge a separate log event and secrets are not emitted.

**Weaknesses:** CWE-117 and CWE-200.

### Procedure

1. Identify application logs for a synthetic login or profile update.
2. Submit a field containing newline and delimiter characters.
3. Inspect whether the logger creates one structured event or forged event lines.
4. Submit a synthetic token-like value and inspect logs, traces and exception output.
5. Replace string-built log lines with structured logging fields.
6. Add redaction for credentials, tokens, cookies and reset secrets.
7. Restrict log viewer access and verify retention and integrity controls.
8. Repeat the tests.

**Expected result:** One structured event is emitted; secrets are redacted; attribution fields remain parseable.

**Evidence:** Sanitized log record, logger configuration and access policy.

**Teardown:** Remove test logs from the disposable environment.

## 11. Assessment rubric

| Criterion | Points |
|---|---:|
| Identifies source, transformation, sink and trust boundary | 15 |
| Explains root cause rather than only naming a vulnerability | 15 |
| Reproduces issue safely with synthetic data | 15 |
| Implements correct and maintainable fix | 20 |
| Adds meaningful regression test | 15 |
| Captures evidence and explains expected/observed results | 10 |
| Completes teardown and records limitations | 10 |
| **Total** | **100** |

Suggested interpretation: 90–100 demonstrates strong independent engineering; 75–89 demonstrates working competence with review; 60–74 requires guided remediation; below 60 requires repeating the exercise. These are training thresholds, not professional certification.

## 12. Instructor review checklist

- Was the environment isolated and synthetic?
- Did the learner identify the actual trust boundary?
- Did the learner distinguish validation from authorization?
- Did the fix address root cause rather than merely block one payload?
- Was the fix tested through the real application code path?
- Were negative and positive behaviors both tested?
- Did the learner record framework and driver versions?
- Were logs and evidence sanitized?
- Was the lab destroyed or reset?
- Were limitations and untested paths recorded?

## 13. References

1. OWASP SQL Injection Prevention: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
2. OWASP Input Validation: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
3. OWASP Secure Code Review: https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
4. MITRE CWE 2025 Top 25: https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25
5. OWASP ASVS 5.0.0: https://asvs.owasp.org/

## 14. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial secure coding lab specifications |
