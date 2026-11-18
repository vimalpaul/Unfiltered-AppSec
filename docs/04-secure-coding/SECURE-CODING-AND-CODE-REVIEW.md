# 04. Secure Coding and Code Review Engineering Playbook

| Field | Value |
|---|---|
| Document ID | UAPPSEC-04-001 |
| Status | Draft baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Secure implementation and review for web applications, APIs, services and supporting software |
| Technology examples | Java/Spring, .NET/C#, Node.js/TypeScript and Python |
| Classification | Public |

## 1. Executive summary

Secure coding is the implementation of software so that required security properties survive valid, malformed, unexpected and adversarial inputs. It is not merely code that passes a static analyzer, follows a style guide or uses a modern framework. Secure code makes trust assumptions explicit, enforces authorization at the correct boundary, ensures data is interpreted safely by downstream components, limits privileges and resource consumption, preserves business invariants and exposes sufficient evidence for verification.

This playbook establishes a language-independent engineering model and applies it to Java/Spring, C#/.NET, JavaScript/TypeScript with Node.js, and Python. Code examples are illustrative. Exact framework APIs, defaults and security patches vary by version. Confirm them against the deployed framework and its official documentation before adoption.

The central rule is:

**Untrusted data must not become authority, executable syntax, a resource locator or an unbounded workload without an explicit, validated and authorized transition.**

This explains why SQL injection, cross-site scripting, path traversal, server-side request forgery, mass assignment, broken object authorization, unsafe deserialization and denial of service are related engineering failures: attacker-influenced data crosses a boundary and gains meaning or power that the application did not intend.

## 2. Purpose, audience and applicability

Use this playbook to establish secure coding standards, review source changes, investigate vulnerability root causes, design SAST rules, build regression tests, review framework upgrades and train developers.

Audience: developers, senior engineers, reviewers, application security engineers, architects, DevSecOps and product security teams, technical auditors and engineering leaders.

In scope:
- Server-side application code, browser-facing code, APIs and background workers.
- Database access, identity, authorization, sessions and cryptography.
- File and document processing, outbound HTTP, message queues and integrations.
- Build-time code generation, plugins, package dependencies and configuration.
- Security-relevant business logic and transaction workflows.

Specialist chapters will expand browser security, API protocol security, mobile security, cloud platform hardening and incident response. This chapter addresses their implementation interfaces.

## 3. Secure coding mental model

### 3.1 Trust transition

~~~mermaid
flowchart LR
    U[Untrusted source] --> V[Parse and validate]
    V --> I[Establish identity and context]
    I --> Z[Authorize action and resource]
    Z --> B[Apply business invariants]
    B --> S[Use safe API and parameter binding]
    S --> O[Bounded operation]
    O --> R[Encode or serialize for destination]
    R --> E[Controlled output and audit]
    V -->|Invalid| D[Reject safely]
    Z -->|Denied| D
    B -->|Invariant fails| D
~~~

Not every operation requires authentication, but every protected operation requires an explicit authorization decision. Validation does not confer authority. Authentication does not grant access to every resource. Encoding does not repair authorization. Safe APIs reduce interpreter risk but do not prove business correctness.

### 3.2 Sources, transformations, sinks and authority

| Element | Definition | Examples | Review question |
|---|---|---|---|
| Source | Data entering a trust domain | HTTP body, URL, header, cookie, queue message, file, database field, partner response, model output | Who can influence it directly or indirectly? |
| Transformation | Parsing, decoding, normalization, mapping or enrichment | JSON parser, Unicode normalization, ORM mapping, template interpolation | Does the transformation change meaning or invalidate prior checks? |
| Sink | Component that interprets or acts on data | SQL engine, browser DOM, shell, filesystem, URL client, XML parser, template engine | Which grammar or authority does the sink apply? |
| Authority boundary | Point where identity or privilege is established | Authentication middleware, policy check, service identity, tenant resolver | Is authority derived from a trusted source? |
| Resource boundary | Point where compute, storage or external service use is consumed | Query, regex, upload, decompression, outbound request, report export | Are size, time, concurrency and cost bounded? |

Treat data as untrusted based on provenance, not variable name or transport. Database content may have originated from a user. A partner response may be compromised. A queue message may come from an over-privileged service. An administrator may enter unsafe content.

A taint review follows data from source to sink:
1. Identify direct and indirect sources.
2. Record parsing and decoding steps.
3. Identify validation and authorization checks.
4. Identify the destination interpreter or authority-bearing API.
5. Determine whether the control is valid for that destination.
6. Verify the path with a test or code-level evidence.

A generic sanitize helper is not proof. A value safe for an HTML text node may not be safe for JavaScript, URL, CSS, SQL identifier, shell argument or filesystem path.

## 4. Secure coding principles

### 4.1 Validate syntax and semantics

Syntax validation checks type, length, character set, format and encoding. Semantic validation checks whether a value makes sense for the business operation.

Examples:
- A date parses correctly but ends before its start date.
- An amount is numeric but exceeds the user's transaction limit.
- A tenant ID is syntactically valid but does not belong to the authenticated principal.
- A course exists but is not assigned to the user's organization.
- A file has an allowed extension but contains a different format or malicious content.

Validation must be server-side. Client-side validation improves usability but is not a security boundary. Prefer allow-lists for constrained domains, but do not use validation as a substitute for parameterization, output encoding or authorization.

### 4.2 Separate data from executable syntax

Use safe APIs that keep data separate from interpreter grammar:
- Parameterized SQL rather than string concatenation.
- Argument arrays and fixed executables rather than shell command strings.
- Context-aware output encoding rather than raw HTML insertion.
- Safe template APIs with auto-escaping.
- Structured logging rather than constructing log lines from untrusted strings.
- Fixed or allow-listed URL destinations rather than arbitrary outbound destinations.
- Safe deserialization into constrained data-transfer objects rather than arbitrary object graphs.

### 4.3 Enforce authorization at the resource boundary

The component performing the protected operation must enforce authorization or consume a trusted, verifiable authorization decision. A hidden UI button, gateway-only role check, random identifier, client-supplied tenant field or earlier page authorization does not prove access to the requested object.

For every sensitive operation ask:
- Who is the subject?
- What action is requested?
- What exact resource is affected?
- Which tenant or organizational boundary applies?
- Which relationship or policy grants the action?
- Which properties may be read or changed?
- Is the operation valid in the current workflow state?
- Is the decision still valid at execution time?

### 4.4 Use explicit data-transfer objects

Do not bind a request directly to a privileged domain or persistence object. Define input DTOs containing only caller-writable properties. Server-controlled properties such as role, tenant, approval status, ownership, price, account balance, assessment score and administrative flags must be assigned by trusted application logic after authorization and business validation.

### 4.5 Minimize privilege and capability

The application, database, file service, worker, build agent and integration should each receive only required permissions. Prefer capability-specific service identities over one shared administrative credential. Avoid using a database owner account for normal application requests.

### 4.6 Bound every expensive operation

Apply explicit limits to request body and upload size, collection length and nested depth, query result and execution time, pagination size and offset, regex complexity, decompression ratio, archive entry count, concurrent jobs, queue depth, outbound HTTP timeout and response size, login and report-generation rates, and AI prompt, context, tool and output budgets.

A valid request can still be abusive when repeated or when it triggers expensive downstream work.

### 4.7 Fail safely

If authorization, policy evaluation, token validation or integrity checks cannot be completed, do not silently permit the protected action. Availability-driven fallback must be documented, risk-approved, narrowly scoped, monitored and tested. Do not catch an exception and return a success-shaped default for security-critical logic.

## 5. Common implementation control catalogue

| Control ID | Control objective | Common weakness mapping | Primary implementation | Verification |
|---|---|---|---|---|
| SC-001 | Separate data from SQL syntax | CWE-89 | Parameterized queries; allow-listed identifiers | Review query and test metacharacters as data |
| SC-002 | Encode output for browser context | CWE-79 | Contextual encoding; safe DOM APIs | Test HTML, attribute, URL and DOM contexts |
| SC-003 | Enforce object and function authorization | CWE-862, CWE-863, CWE-639 | Server-side policy at resource operation | Cross-user, cross-tenant and role-negative tests |
| SC-004 | Restrict request-to-domain property mapping | CWE-915 | Explicit DTOs and property allow-lists | Attempt privileged and immutable fields |
| SC-005 | Prevent unsafe command execution | CWE-78, CWE-77 | Avoid shell; fixed executable and argument array | Static review and controlled argument tests |
| SC-006 | Constrain filesystem access | CWE-22 | Server-generated names, canonical path checks, isolated storage | Traversal and symlink tests in isolated lab |
| SC-007 | Validate outbound destinations | CWE-918 | Destination allow-list, DNS/IP validation and egress control | Test private, loopback, link-local and redirect paths |
| SC-008 | Constrain deserialization | CWE-502 | Data-only formats, strict schemas, type allow-lists | Malformed, unknown and deeply nested payloads |
| SC-009 | Protect file upload processing | CWE-434 | Size/type/content validation, quarantine and isolated scanning | Polyglot, oversized, archive and active-content tests |
| SC-010 | Bound resource consumption | CWE-770, CWE-400 | Quotas, timeouts, concurrency limits and back-pressure | Load, burst, timeout and exhaustion tests |
| SC-011 | Protect authentication secrets | CWE-521 and related password-storage weaknesses | Approved password hashing, MFA, secure recovery | Configuration and lifecycle tests |
| SC-012 | Prevent sensitive data exposure | CWE-200 | Minimize, authorize, redact and encrypt | Response, logs, errors and exports |
| SC-013 | Protect cryptographic keys | CWE-321 and related key-management weaknesses | Managed key store, rotation, scoped access | Key access, rotation and revocation test |
| SC-014 | Prevent unsafe redirects | CWE-601 | Relative path or strict destination allow-list | External and scheme-relative redirect tests |
| SC-015 | Protect XML processing | CWE-611 | Disable external entity resolution and restrict parser features | XXE regression tests in isolated environment |
| SC-016 | Preserve workflow integrity | CWE-841 and related business-logic weaknesses | Server-side state machine and atomic transitions | Replay, reorder, duplicate and illegal transition tests |
| SC-017 | Protect audit integrity | CWE-117, CWE-778 | Structured logging, CR/LF handling, access controls | Log injection and attribution tests |
| SC-018 | Validate token trust | CWE-345 and authentication-related weaknesses | Issuer, audience, signature, expiry and algorithm validation | Invalid issuer/audience/signature/expiry tests |

CWE mappings are descriptive relationships, not proof that every instance maps to one weakness only. Use the most specific applicable CWE and preserve the actual root cause.

## 6. Database access and SQL injection prevention

### 6.1 Root cause

SQL injection occurs when attacker-influenced data changes the structure or meaning of a SQL statement. Sources include HTTP input, queue messages, imported files, database content and partner responses. A query can remain vulnerable even if the outer call is prepared when dynamic SQL is assembled inside a stored procedure.

### 6.2 Correct implementation rules

1. Define SQL structure in code or a trusted query builder.
2. Bind all dynamic data values using the database driver's parameter API.
3. Never concatenate untrusted data into SQL syntax.
4. Map dynamic table names, column names and sort directions to fixed application-owned identifiers.
5. Use least-privilege database identities.
6. Separate read-only and write privileges where practical.
7. Constrain tenant and resource access independently of injection prevention.
8. Review stored procedures and dynamic SQL for internal concatenation.
9. Test actual query paths, including filters, sorting, search, exports, reports and administrative queries.

### 6.3 Unsafe pattern

~~~csharp
// UNSAFE: request input is incorporated into SQL syntax.
var sql = "SELECT * FROM Users WHERE Email = '" + email + "'";
var result = await connection.QueryAsync(sql);
~~~

### 6.4 Safer .NET pattern

~~~csharp
var result = await connection.QueryAsync(
    "SELECT Id, Email FROM Users WHERE Email = @Email",
    new { Email = email });
~~~

This uses a parameter-binding pattern supported by common .NET data-access libraries. Confirm exact behavior for the selected library and driver. Do not assume every ORM raw-SQL helper parameterizes interpolated strings.

### 6.5 Dynamic sorting

Parameter placeholders generally represent values, not SQL identifiers or keywords. Use a strict mapping:

~~~csharp
var sortColumn = requestedSort switch
{
    "created" => "CreatedAt",
    "name" => "DisplayName",
    _ => "CreatedAt"
};
var direction = requestedDirection == "desc" ? "DESC" : "ASC";
var sql = $"SELECT Id, DisplayName, CreatedAt FROM Users ORDER BY {sortColumn} {direction}";
~~~

This is acceptable only because both interpolated fragments are selected from fixed application-owned constants. Never interpolate raw request values. Apply authorization and pagination separately.

### 6.6 Java / Spring pattern

~~~java
String sql = "select id, email from users where email = ?";
List<UserSummary> rows = jdbcTemplate.query(
    sql,
    (rs, rowNum) -> new UserSummary(rs.getLong("id"), rs.getString("email")),
    email
);
~~~

Use parameterized JDBC methods or correctly parameterized repository APIs. Review native queries, dynamic sort expressions, JPQL construction and stored procedures. A repository abstraction does not automatically make every custom query safe.

### 6.7 Node.js pattern

~~~typescript
const result = await pool.query(
  "SELECT id, email FROM users WHERE email = $1",
  [email]
);
~~~

This example uses PostgreSQL-style positional parameters. Other drivers have different placeholder formats. Confirm that the driver binds values rather than interpolating strings.

### 6.8 Python pattern

~~~python
cursor.execute(
    "SELECT id, email FROM users WHERE email = %s",
    (email,)
)
~~~

Placeholder syntax is driver-specific. Never use Python string formatting, f-strings or concatenation to insert untrusted values into SQL.

### 6.9 Review and test procedure

**Authorization and prerequisites**
- Use an isolated test database with synthetic records.
- Obtain approval for the target application and test environment.
- Do not run destructive payloads against production data.
- Identify endpoints and jobs that construct SQL: search, filters, sorting, exports, reports, login and admin queries.

**Procedure**
1. Trace request and indirect data sources to database calls.
2. Identify concatenation, string formatting, dynamic SQL, ORM raw-query and stored-procedure paths.
3. Verify values are passed through driver parameter binding.
4. Identify identifiers or keywords that cannot be parameterized and verify strict mapping to constants.
5. Inspect database account privileges and ensure the application identity is not a DBA/owner account.
6. Use benign test strings containing quotes, delimiters and SQL metacharacters in synthetic records.
7. Verify input remains a data value and does not alter result scope or query structure.
8. Review error handling for database stack traces and schema leakage.
9. Verify authorization separately using another user's or tenant's synthetic record identifier.
10. Record code location, driver/API, query path, test inputs, observed behavior and remediation evidence.

**Expected result:** input is treated as data; query structure remains constant; only authorized records are returned; no database details leak.

**Stop conditions:** stop if testing affects a real database, changes non-test records, causes service degradation or reveals production secrets.

## 7. Output encoding, XSS and template safety

### 7.1 The context problem

Cross-site scripting is not solved by a universal HTML sanitizer. Encoding must match the destination context: HTML text node, HTML attribute, JavaScript string or data block, URL component, CSS value, DOM API or intentionally supported rich text.

Prefer framework template engines with contextual auto-escaping and safe DOM APIs. Avoid inserting untrusted strings using innerHTML, outerHTML, document.write or equivalent raw HTML sinks. When rich HTML is a business requirement, use a maintained allow-list sanitizer with a defined policy and tests.

### 7.2 Safer browser code

~~~typescript
const output = document.querySelector("#message");
if (output) {
  output.textContent = userSuppliedMessage;
}
~~~

This treats the string as text. If rich content is required, use a separate sanitization and policy process. Do not replace textContent with innerHTML merely to preserve formatting.

### 7.3 Server-rendered templates

- Keep auto-escaping enabled.
- Avoid raw/unescaped template expressions for user content.
- Treat stored content as untrusted; stored XSS can reach privileged users.
- Encode values for the exact output context.
- Validate URL schemes and destinations before rendering links.
- Review Markdown renderers, syntax highlighters, email templates and PDF/report generation separately.
- Use Content Security Policy as defense in depth, not as a substitute for safe output handling.

### 7.4 Testing procedure

1. Identify reflection and storage paths for user-controlled content.
2. Determine final browser context and template/DOM sink.
3. Use harmless marker strings and context-specific test values in a controlled environment.
4. Confirm content is rendered as text or processed by a reviewed sanitizer.
5. Test stored content through all roles that may view it, including administrators and support.
6. Review DOM-based flows where URL fragments, query parameters, postMessage and browser storage feed sinks.
7. Verify CSP and Trusted Types where adopted, without treating them as the primary fix.
8. Capture source, sink, context, role, browser, response/DOM evidence and regression test.

Expected result: untrusted content cannot execute as script or alter trusted page structure. A scanner's failure to execute a payload is not sufficient evidence if the source-to-sink path remains unsafe.

## 8. Authorization, mass assignment and business state

### 8.1 Object authorization

A user-supplied object identifier selects a resource; it does not grant access to it. Authorization must bind the authenticated subject, requested action, resource, tenant and business relationship.

A useful policy expression is:

**Permit(subject, action, resource, context)**

The decision must be enforced by the server-side service performing the operation. Database query scoping provides defense in depth but is not automatically a complete authorization model.

### 8.2 Property-level authorization

Do not deserialize a request directly into an entity with privileged fields. Define a request model:

~~~csharp
public sealed record UpdateProfileRequest(
    string DisplayName,
    string TimeZone
);
~~~

Then map only permitted properties:

~~~csharp
user.DisplayName = request.DisplayName;
user.TimeZone = request.TimeZone;
// Role, TenantId, IsAdmin and ApprovalState are not caller-controlled here.
~~~

For updates that legitimately allow different fields by role, use explicit policy and separate command models rather than a generic update-everything endpoint.

### 8.3 Workflow state and TOCTOU

A secure workflow validates state and authority at the time of the consequential transition. Consider an assessment:
- A learner may submit only an assigned assessment.
- A submission is accepted only during the allowed window.
- A completed submission cannot be modified through a generic update endpoint.
- Score and pass/fail status are computed or approved by trusted logic.
- A retry is idempotent or rejected, not silently accepted as a second submission.
- A tenant administrator cannot alter platform policy by changing a request property.

Time-of-check-to-time-of-use (TOCTOU) failures occur when an application checks a condition and later acts after the condition has changed. Use transactional state transitions, concurrency control, version checks and database constraints where appropriate.

### 8.4 Test matrix

| Test | Principal | Requested action | Expected result |
|---|---|---|---|
| AUTHZ-01 | Owner | Read own object | Permit |
| AUTHZ-02 | Other user, same tenant | Read object | Deny unless explicit sharing exists |
| AUTHZ-03 | User from another tenant | Read or update object | Deny |
| AUTHZ-04 | Learner | Set privileged role property | Ignore or reject; no privilege change |
| AUTHZ-05 | Tenant admin | Change platform setting | Deny |
| AUTHZ-06 | Authorized user | Repeat one-time transition | Idempotent or reject per business rule |
| AUTHZ-07 | User with revoked membership | Use stale session | Deny after policy-defined revocation propagation |
| AUTHZ-08 | Support user | Access customer data | Approved support workflow and audit required |

## 9. Command and interpreter injection

### 9.1 Preferred order of controls

1. Do not invoke an operating-system shell if a library or native API can perform the task.
2. If a process must be launched, use a fixed executable path and an argument-array API.
3. Never concatenate untrusted input into a shell command string.
4. Validate each argument according to its semantic role.
5. Use least-privilege process identity, restricted working directory and environment.
6. Apply timeout, output-size and process-count limits.
7. Treat output as untrusted and do not execute it.
8. Record the operation without logging secrets or sensitive arguments.

### 9.2 Safer process launch concept

~~~csharp
var start = new ProcessStartInfo
{
    FileName = "/usr/bin/approved-tool",
    UseShellExecute = false,
    RedirectStandardOutput = true,
    RedirectStandardError = true
};
start.ArgumentList.Add("--input");
start.ArgumentList.Add(validatedServerSideFilePath);
~~~

This avoids shell parsing, but does not make arbitrary executable selection or arbitrary file paths safe. The executable must be fixed and trusted; arguments still need semantic validation, resource limits and authorization.

### 9.3 Other interpreters

Apply the same data/syntax separation to LDAP filters, XPath/XQuery, NoSQL query operators, expression languages, dynamic evaluation, template engines, regular expressions, SMTP command construction, GraphQL query composition, search DSLs, spreadsheet formulas and CSV exports.

Do not assume JSON input is harmless. JSON can carry query operators, template expressions, serialized type metadata, file references or tool instructions that downstream components interpret.

## 10. Filesystem, upload and archive handling

### 10.1 Secure storage design

- Store uploads outside the web root or in private object storage.
- Generate server-side object identifiers; do not use the original filename as a storage path.
- Keep original names only as metadata and encode them when displayed.
- Enforce maximum size, file count, archive depth, entry count and decompressed size.
- Validate extension, declared content type and file signature; none alone proves safety.
- Use malware scanning or content disarm/reconstruction when required by risk and file type.
- Quarantine until processing and policy checks complete.
- Restrict parser privileges and network access.
- Do not execute uploaded content.
- Set download content disposition and content type safely.
- Authorize every download against the underlying object and tenant.
- Define retention, deletion, backup and audit behavior.

### 10.2 Path traversal and canonicalization

Do not construct paths by concatenating a user-controlled path fragment. Prefer an opaque object ID resolved to a server-side storage key. Where path operations are unavoidable:
1. Resolve a trusted base directory.
2. Normalize and canonicalize the candidate path.
3. Verify the resolved path remains beneath the permitted base.
4. Account for platform-specific separators, case rules, Unicode and symlinks.
5. Use APIs that avoid following attacker-controlled symlinks where supported.
6. Prevent race conditions between validation and file open.
7. Apply operating-system permissions as a second boundary.

A string-prefix test such as StartsWith(basePath) is not a robust path-containment check on its own. Separators, sibling names, case behavior and symlinks can defeat naive checks.

### 10.3 Archive extraction

Archive bombs can expand to very large output from a small compressed file. Enforce limits on compressed input size, total decompressed bytes, per-entry size, entry count, directory depth, compression ratio, extraction time and CPU, duplicate/conflicting paths, symlink and hardlink entries.

Extract to a new isolated directory with restricted permissions. Do not overwrite application files or shared directories. Reject paths that escape the extraction root after canonical resolution.

## 11. Server-side request forgery and outbound integrations

SSRF is an authority problem: a user-controlled value influences which network resource a server contacts. It can expose internal services, cloud metadata endpoints, administrative interfaces or data reachable only from the server's network.

### 11.1 Secure outbound request design

- Prefer a business-defined destination identifier mapped to a fixed server-side URL.
- Use strict scheme, hostname, port and path allow-lists.
- Reject loopback, private, link-local, multicast, reserved and internal ranges unless explicitly required.
- Resolve and validate DNS results; consider rebinding and resolution changes.
- Revalidate every redirect target or disable redirects.
- Control proxy behavior and environment-derived proxy settings.
- Apply egress network controls independent of application validation.
- Set connect/read/overall timeouts, response size and concurrency limits.
- Do not forward inbound cookies, Authorization headers or internal credentials.
- Avoid returning raw response bodies or internal network errors to users.
- Authenticate the destination service and validate its TLS identity.

DNS and address validation are subtle. A one-time string check does not establish the safety of the actual socket destination. Prefer a constrained egress proxy or destination service that enforces policy at connection time.

### 11.2 Procedure

1. Inventory every server-side HTTP client, webhook callback, URL preview, import-from-URL and document-fetch function.
2. Identify who controls the destination and whether redirects are followed.
3. Inspect DNS resolution, IP filtering, proxy settings and outbound network policy.
4. In an isolated environment, test only approved synthetic destinations representing public, loopback, private and link-local classes.
5. Verify disallowed destinations are rejected by the application and/or egress policy.
6. Verify redirects cannot escape the destination allow-list.
7. Confirm timeouts, response-size limits and safe error handling.
8. Capture client configuration, egress rule, destination decision and test evidence.

Never probe real internal infrastructure or cloud metadata endpoints without explicit authorization and a controlled test plan.

## 12. Deserialization, parser and content processing

Prefer formats and APIs that deserialize into data structures rather than instantiate arbitrary classes or execute constructors, callbacks or type resolution. Use strict schemas, allow-listed types, depth and size limits, and versioned contracts.

Review:
- Polymorphic type metadata.
- Java native serialization and gadget-capable libraries.
- .NET type-name handling and unsafe object serializers.
- Python pickle and unsafe YAML loaders.
- XML entity expansion and external resource resolution.
- Image, PDF, office document and archive parsers.
- Template and expression engines.
- Message queue payloads and event schemas.

Do not deserialize untrusted data with a general-purpose object serializer that permits arbitrary type instantiation. Python pickle must never be used as a trust-boundary interchange format.

### 12.1 XML

Disable external general entities and external parameter entities, prevent external DTD retrieval, restrict XInclude where applicable and apply parser limits. Exact secure configuration depends on parser and runtime version. Test effective behavior, not merely a configuration file entry.

### 12.2 Parser isolation

For complex or risky file types, use a dedicated low-privilege processing service with no unnecessary outbound network access, a read-only application filesystem, temporary isolated workspace, CPU/memory/time/file-size limits, sandboxing where feasible, explicit output schema and cleanup/quarantine workflow.

## 13. Authentication, passwords, sessions and cryptography

This chapter provides coding rules; the full protocol and identity architecture is covered by the Identity and Access Security chapter.

### 13.1 Password handling

- Never store plaintext or reversibly encrypted passwords.
- Use a maintained password-hashing library and a modern password-hashing scheme appropriate to the environment, such as Argon2id where supported by policy and platform.
- Use unique salts managed by the password-hashing library.
- Tune work factors against production hardware and availability requirements.
- Consider a separately protected pepper only where key lifecycle and recovery are engineered.
- Rehash on successful authentication when parameters become obsolete.
- Protect password-reset tokens as high-entropy, short-lived, single-use secrets.
- Avoid password hints and security questions as a substitute for strong recovery.
- Do not log passwords, reset links, one-time codes or session tokens.

Do not invent a universal work-factor number. Benchmark the selected algorithm on the actual deployment class and revisit as hardware and threats change.

### 13.2 Session and token handling

- Generate unpredictable session identifiers using a cryptographically secure random generator.
- Rotate session identifiers after authentication and privilege changes.
- Enforce idle and absolute expiration.
- Revoke sessions on logout, credential reset and risk events according to policy.
- Use Secure, HttpOnly and an appropriate SameSite cookie value where cookies are used.
- Protect state-changing cookie-authenticated requests against CSRF.
- Validate token signature, issuer, audience, expiry, not-before and permitted algorithm.
- Do not accept unsigned tokens or let a token header choose an unsafe verification algorithm.
- Protect refresh-token rotation and reuse detection.
- Avoid storing long-lived bearer tokens in browser-accessible storage where a safer architecture is feasible.

### 13.3 Cryptographic implementation

- Use maintained cryptographic libraries and platform key-management services.
- Do not invent algorithms, modes, padding or random number generators.
- Separate encryption keys from encrypted data where practical.
- Define key ownership, access, rotation, revocation, backup and destruction.
- Use authenticated encryption where suitable and verify authentication tags before using plaintext.
- Do not reuse nonces where the algorithm prohibits it.
- Protect signing keys more strongly than ordinary application configuration.
- Plan algorithm agility and migration before deprecation becomes urgent.

## 14. Error handling, logging and privacy

### 14.1 Error handling

- Return stable, non-sensitive error responses to clients.
- Do not expose stack traces, SQL statements, filesystem paths, internal hostnames, tokens or configuration.
- Preserve detailed diagnostic context in protected internal telemetry.
- Ensure exception handling does not convert failed authorization into success.
- Distinguish validation errors from unexpected server errors without exposing internal state.
- Use correlation IDs to connect events without using them as authorization credentials.

### 14.2 Structured logging

Record security-relevant events with event type and outcome, synchronized timestamp, request/correlation ID, authenticated subject identifier in a privacy-appropriate form, tenant context, target resource and action, source service and environment, and reason or policy decision identifier where appropriate.

Do not log passwords, API keys, private keys, bearer tokens, full session cookies, reset links, full payment or identity data without a justified need, raw request bodies by default or secrets embedded in exception messages.

Prevent log injection with structured logging APIs and correct handling of CR/LF and delimiters. Protect log access, integrity, retention and export. Logging is itself a data-processing system and must follow privacy and retention requirements.

## 15. Concurrency, transactions and business logic

Secure code must preserve invariants under concurrency, retries and partial failure.

### 15.1 Common hidden defects

- Double spending or duplicate redemption caused by concurrent requests.
- Multiple assessment submissions accepted due to race conditions.
- Approval and payment state updated in separate non-atomic operations.
- Authorization checked before a long-running operation but not revalidated at commit.
- Queue message replay creates duplicate side effects.
- Cache entries outlive role revocation or tenant membership changes.
- Retry logic repeats a non-idempotent operation.
- A distributed workflow reports success before downstream commit is confirmed.

### 15.2 Engineering controls

- Use database transactions for invariants that must change atomically.
- Use unique constraints and conditional updates to enforce one-time transitions.
- Use optimistic concurrency/version checks where appropriate.
- Use idempotency keys bound to the authenticated principal and operation.
- Design outbox/inbox patterns for reliable event publication and deduplication where needed.
- Define state machines and allowed transitions.
- Make authorization and state checks part of the transaction boundary where possible.
- Treat caches as security-relevant stores; scope keys by principal/tenant and invalidate on permission changes.
- Define compensation and reconciliation for distributed operations.

### 15.3 Example conditional transition

~~~sql
UPDATE assessment_attempt
SET status = 'SUBMITTED',
    submitted_at = CURRENT_TIMESTAMP,
    version = version + 1
WHERE id = :attempt_id
  AND learner_id = :authorized_learner_id
  AND tenant_id = :authorized_tenant_id
  AND status = 'IN_PROGRESS'
  AND version = :expected_version;
~~~

The application must verify exactly one row changed. Zero rows means the operation did not satisfy the expected ownership, state or concurrency condition. Do not disclose sensitive existence details unnecessarily. Adapt the example to the actual database and transaction model.

## 16. Language and framework implementation guide

### 16.1 Java / Spring

Review:
- Spring Security filter chain and authorization configuration.
- Method-level security and service-layer enforcement.
- Request DTO validation and explicit entity mapping.
- JDBC/JPA native query construction and dynamic sorting.
- Jackson polymorphic deserialization and default typing configuration.
- File upload and multipart limits.
- Template escaping and unsafe raw HTML.
- HTTP client destination restrictions, redirects and timeouts.
- Exception handlers and error serialization.
- Dependency versions, actuator endpoints and production configuration.

Preferred patterns:
- Use Bean Validation for syntactic and semantic DTO constraints, while keeping authorization separate.
- Use prepared statements or correctly parameterized repository operations.
- Use explicit DTOs rather than binding directly to JPA entities.
- Use Spring Security authorization at request and method/service boundaries as appropriate.
- Keep actuator and management endpoints restricted to a separate administrative trust zone.
- Configure JSON polymorphism narrowly; do not enable broad class-name-based type resolution for untrusted input.

### 16.2 .NET / ASP.NET Core

Review:
- Authentication schemes and authorization policies.
- Resource-based authorization handlers.
- Model binding and DTO property exposure.
- EF Core parameterization and raw SQL APIs.
- Razor encoding and raw HTML helpers.
- Cookie authentication, antiforgery and CORS configuration.
- Data Protection key storage and rotation.
- Process launch and command construction.
- XML/JSON serializer options.
- Exception middleware and Problem Details output.
- Kestrel and reverse-proxy request limits.
- Secrets, connection strings and environment configuration.

Preferred patterns:
- Use policy/resource authorization, not only controller-level role attributes.
- Use request DTOs and explicit mapping.
- Prefer EF Core LINQ or parameterized raw SQL; review dynamic SQL carefully.
- Keep Razor's normal encoding behavior and avoid raw HTML helpers for untrusted content.
- Use antiforgery protection for cookie-authenticated state changes where applicable.
- Store Data Protection keys securely and share them appropriately across instances.
- Use ProcessStartInfo.ArgumentList with a fixed executable rather than shell concatenation when a process is unavoidable.

### 16.3 Node.js / TypeScript

Review:
- Middleware ordering and route-level authorization.
- Trust proxy configuration and IP-based controls.
- Request schema validation and type coercion.
- ORM raw queries and driver parameterization.
- Prototype pollution and unsafe object merges.
- Dynamic evaluation and template compilation.
- Path handling, archive extraction and file upload.
- child_process APIs, especially shell-enabled execution.
- SSRF through fetch, HTTP clients, URL preview and webhook features.
- Unhandled promise rejection and error serialization.
- Dependency lifecycle, install scripts and lockfile integrity.
- Event-loop blocking, regex complexity and unbounded concurrency.

Preferred patterns:
- Use strict request schemas and reject unknown privileged fields.
- Do not assume TypeScript types validate runtime data. Parse external values at runtime.
- Avoid eval, Function, unsafe template compilation and object merge into privileged prototypes.
- Prefer safe child-process APIs without a shell and fixed executables.
- Bound body parsing, upload size, concurrency and outbound request behavior.
- Avoid blocking synchronous operations in request paths.
- Use a maintained ORM/driver with parameter binding and review every raw-query escape hatch.

### 16.4 Python

Review:
- Web framework authentication and authorization dependencies.
- Pydantic or equivalent runtime validation and coercion settings.
- SQLAlchemy/raw cursor parameterization.
- Unsafe pickle, YAML loaders and dynamic imports.
- subprocess with shell=True.
- Pathlib/path normalization and symlink handling.
- Template auto-escaping and safe-string bypasses.
- Requests/httpx destination, redirect and timeout behavior.
- XML parser features.
- Logging configuration and exception disclosure.
- Async task concurrency, timeouts and cancellation.
- Dependency pinning, virtual environments and package provenance.

Preferred patterns:
- Use explicit schemas for external payloads and reject unexpected fields where practical.
- Use DB-API parameter binding or SQLAlchemy bound parameters.
- Avoid pickle for untrusted data.
- Use subprocess with a fixed executable and argument list, not shell=True with user input.
- Use a maintained safe YAML loader and restrictive XML parser configuration.
- Set explicit timeouts and response-size limits for outbound calls.
- Do not rely on type hints as runtime validation.

## 17. Secure code review methodology

### 17.1 Review scope and authorization

A code review is authorized by repository owner and project policy. Review only the specified branch, commit, service and supporting components. Do not copy secrets or customer data into public tickets or reports. If a real credential is discovered, stop sharing it, notify the owner and initiate rotation/revocation.

### 17.2 Review preparation

Collect repository and commit SHA, application/component inventory, change purpose and affected workflows, data classification and trust boundaries, authentication and authorization model, API and integration inventory, relevant security requirements and threat model, build/dependency context, and test evidence and deployment environment.

### 17.3 Review procedure

1. **Understand the change.** Read the full diff and identify changed behavior, not just changed lines.
2. **Map data flow.** Identify untrusted sources, transformations, validation, authorization and sinks.
3. **Map privilege.** Identify user, service, database, filesystem and cloud permissions used by the change.
4. **Review business invariants.** Determine valid state transitions, tenant boundaries, ownership, transaction rules and idempotency.
5. **Review interpreters.** Inspect SQL, browser DOM, shell, filesystem, URL, XML, template and expression-language boundaries.
6. **Review sensitive data.** Inspect secrets, tokens, PII, logs, exports, caches and error responses.
7. **Review dependencies.** Check package changes, versions, lifecycle scripts, transitive dependencies and known advisories.
8. **Review failure behavior.** Check timeouts, exceptions, retries, partial failure and fail-open conditions.
9. **Review tests.** Confirm positive and negative security cases and regression coverage.
10. **Run analysis tools.** Execute approved SAST, SCA and secret checks; triage findings with code context.
11. **Record findings.** State root cause, attack preconditions, impact, affected code, remediation and verification.
12. **Retest.** Review the fix and run regression cases before closure.

### 17.4 Questions that reveal hidden defects

- Does the code trust a value because it came from the database or an internal queue?
- Can an ordinary request set an administrative or ownership field through object binding?
- Does a check happen in the controller but not in the service used by another route or worker?
- Can a cached response cross user or tenant boundaries?
- Does a retry duplicate a payment, submission, email or approval?
- Can an attacker choose a URL, file path, template, sort field, class name or executable?
- Does a redirect create a second trust boundary?
- Does the code check a resource before a long-running operation but not at commit?
- Can malformed Unicode, duplicate JSON keys, alternate encodings or ambiguous parsing change meaning?
- Does an error handler swallow a security exception and return a default success?
- Can a feature be abused at scale even when every individual request is valid?
- Does the test suite prove forbidden operations fail, not only that valid operations work?

## 18. Security verification and regression test catalogue

| Test ID | Control | Test input or action | Expected result | Evidence |
|---|---|---|---|---|
| SC-T-001 | SQL binding | Quotes and SQL metacharacters in synthetic search value | Treated as data; query scope unchanged | Query/code review and test log |
| SC-T-002 | SQL identifier mapping | Unknown sort key or direction | Rejected or safe default selected | Response and mapping test |
| SC-T-003 | Output encoding | HTML/script-like marker in user profile | Rendered inert in correct context | DOM and browser evidence |
| SC-T-004 | Stored XSS | Store marker then view as another role | No script execution; correct encoding | Stored record and view evidence |
| SC-T-005 | Object authorization | User A requests User B resource | Denied unless explicit policy permits | Response and audit event |
| SC-T-006 | Tenant isolation | Tenant A requests Tenant B record/export | No disclosure or side effect | Test data and response/export |
| SC-T-007 | Mass assignment | Submit role, tenantId, isAdmin, status fields | Privileged state unchanged | Before/after record and response |
| SC-T-008 | Command injection | Shell metacharacters in benign test parameter | No shell interpretation | Process invocation and logs |
| SC-T-009 | Path traversal | Encoded traversal and alternate separators in isolated test | No access outside storage root | File access evidence |
| SC-T-010 | Upload limits | Oversized file and disallowed content | Rejected or quarantined | Server response and quarantine record |
| SC-T-011 | Archive limits | Synthetic high-ratio or excessive-entry archive | Processing stops at configured bound | Resource metrics and rejection event |
| SC-T-012 | SSRF | Synthetic loopback/private destination and redirect | Rejected by app and/or egress control | Destination decision and network policy log |
| SC-T-013 | Deserialization | Unknown type, deep nesting and malformed payload | Rejected without unsafe object construction | Parser error and resource metrics |
| SC-T-014 | XML parser | Synthetic external-entity document in isolated lab | External entity not resolved | Parser config and result |
| SC-T-015 | Resource bounds | Excessive page size, regex input or concurrency | Bounded response; service remains stable | Latency and resource telemetry |
| SC-T-016 | Session rotation | Authenticate and elevate privilege | Session identifier rotates | Cookie/session evidence |
| SC-T-017 | CSRF | Cross-site state-changing request in cookie session | Rejected without valid anti-CSRF proof | Browser request and server response |
| SC-T-018 | Error disclosure | Trigger controlled invalid request | Generic external error; no stack trace | Response and protected server log |
| SC-T-019 | Log injection | CR/LF and delimiter characters in test field | One structured event; no forged event | Parsed log record |
| SC-T-020 | Workflow replay | Repeat one-time action with same/different idempotency keys | Defined idempotent or rejected outcome | Database state and event record |
| SC-T-021 | Race condition | Concurrently submit same one-time transition | Exactly one valid transition | Transaction and row-count evidence |
| SC-T-022 | Token validation | Wrong issuer/audience, expiry or signature | Rejected | Authentication log and response |

Adapt tests to the actual data model and test environment. A passing test for one endpoint does not prove the same control is applied to every route, worker, export or alternate interface.

## 19. Static analysis and developer tooling

| Category | Examples | Useful for | Important limitation |
|---|---|---|---|
| SAST | Semgrep, CodeQL, SonarQube, Fortify, Checkmarx | Source patterns, data flow, dangerous APIs | Findings depend on language support, rules, configuration and reachability |
| SCA | Dependabot, OSV-Scanner, Snyk, Trivy, Grype | Dependency inventory and known vulnerable components | Does not automatically prove exploitability or runtime reachability |
| Secret scanning | GitHub secret scanning, Gitleaks, TruffleHog | Credential patterns and leaked secrets | Detectors can miss custom formats; rotate exposed credentials |
| IaC scanning | Checkov, KICS, tfsec (verify maintenance status) | Infrastructure configuration weaknesses | Does not prove deployed runtime state |
| Container scanning | Trivy, Grype and registry-native scanners | Image package and configuration issues | Does not prove application authorization |
| DAST / API testing | OWASP ZAP, Burp Suite, API clients | Runtime behavior and request/response validation | Coverage depends on authentication and workflow state |
| Fuzzing | Jazzer, libFuzzer, AFL++ and language-specific tools | Parser, boundary and unexpected-input defects | Requires harness, safe corpus and resource limits |
| Provenance | SBOM tools, build provenance and signature verification | Component traceability and artifact integrity | Metadata must be accurate and protected |

Tool names are examples, not endorsements or claims of current feature parity. Check official documentation, supported language/runtime versions, licensing, data handling and maintenance before selection.

### 19.1 SAST rollout procedure

1. Identify languages, frameworks, repositories and build systems.
2. Establish a baseline scan and record tool version, ruleset and commit.
3. Classify findings by weakness, severity, reachability and business context.
4. Validate a sample of true and false positives with developers.
5. Tune rules without suppressing entire weakness classes.
6. Add high-confidence rules to pull-request feedback.
7. Route lower-confidence results to scheduled review.
8. Require suppression rationale, owner, expiry and compensating control for security-relevant rules.
9. Track rule performance, recurrence and remediation time.
10. Reassess rules after framework upgrades and new attack techniques.

A clean scan means only that the configured tool and ruleset reported no findings in the analyzed scope. It is not evidence that the application is free of vulnerabilities.

## 20. Standards, weakness and regulatory traceability

### 20.1 Technical mapping

| Internal control | CWE relationship | OWASP source | Mapping interpretation |
|---|---|---|---|
| SC-001 SQL data/syntax separation | CWE-89 | SQL Injection Prevention Cheat Sheet; ASVS applicable input/data-access requirements | Direct control objective |
| SC-002 Contextual output encoding | CWE-79 | XSS Prevention and DOM-based XSS Cheat Sheets; ASVS output encoding requirements | Direct control objective |
| SC-003 Server-side authorization | CWE-862, CWE-863, CWE-639 | ASVS access control requirements; API Security Top 10 API1/API3/API5 | Direct for authorization outcomes |
| SC-004 Explicit property mapping | CWE-915 | Mass Assignment Cheat Sheet; API3:2023 | Direct for mass-assignment risk |
| SC-005 Safe process invocation | CWE-78, CWE-77 | OS Command Injection Defense Cheat Sheet | Direct for command injection |
| SC-006 Safe path handling | CWE-22 | OWASP path/file handling guidance | Direct for traversal prevention |
| SC-007 Controlled outbound requests | CWE-918 | SSRF Prevention Cheat Sheet | Direct for SSRF control objective |
| SC-008 Constrained deserialization | CWE-502 | Deserialization Cheat Sheet | Direct for unsafe deserialization |
| SC-010 Resource limits | CWE-770, CWE-400 | API4:2023 and resource-consumption guidance | Direct for bounded resource use |
| SC-015 Safe XML parsing | CWE-611 | XXE Prevention Cheat Sheet | Direct for XXE control objective |
| SC-016 Workflow integrity | CWE-841 and related weaknesses | API6:2023 sensitive business flows | Supporting; requires domain-specific business rules |

Exact ASVS requirement identifiers must be selected from the official 5.0.0 machine-readable release for each application's technology and feature. This chapter deliberately does not invent requirement IDs.

### 20.2 Regulatory relationship

Secure coding contributes to regulatory outcomes but rarely satisfies a legal obligation alone:
- GDPR Articles 25 and 32, where applicable, require privacy by design/default and risk-appropriate security of processing. Secure coding supports these outcomes alongside governance and operational controls.
- Qatar NIA v2.1 Software Security SS 6 calls for secure programming practices including least privilege, deny-by-default and input validation. Entity applicability must be established.
- Saudi NCA ECC 2:2024 controls 2-15-1 and 2-15-2 require applicable entities to identify, document, approve and implement external web application security requirements. Secure coding is one implementation layer, not the whole control.
- India DPDP Rules 2025 Rule 6 includes reasonable security safeguards after its applicable commencement. Secure coding supports safeguards but does not alone satisfy processor, logging, retention, governance or breach obligations.

## 21. Real-world use cases

### 21.1 Multi-tenant learning platform

**Classification:** Composite industry scenario.

A learning platform exposes APIs for assessment submission, report export and course administration. A developer binds JSON directly to an ORM entity containing tenantId, role, score and status. The user interface hides these fields, but a caller can include them in the request. Separately, an assessment-result query filters by result ID but not by the user's membership.

Root causes:
- Request-to-entity mass assignment.
- Missing object-level authorization.
- Trusting client-side control visibility.
- Lack of negative tests for cross-tenant operations.

Corrective actions:
- Define separate learner and administrator request DTOs.
- Assign tenant and role from trusted server-side membership and policy.
- Compute or approve score through trusted workflow logic.
- Authorize every read, update and export against the resource.
- Enforce atomic state transitions for submission.
- Add tests for property tampering, tenant isolation and replay.
- Audit privileged changes and report exports.

### 21.2 Document conversion service

**Classification:** Composite industry scenario.

A service accepts a URL or file, downloads content and converts it to PDF. Risks include SSRF, malicious parser input, archive bombs, path traversal, command injection and resource exhaustion. The secure design separates fetch, quarantine, parsing and output delivery; restricts outbound network access; uses a sandboxed converter; limits input/output size and processing time; assigns opaque object identifiers; and authorizes output downloads.

### 21.3 Administrative reporting

**Classification:** Composite industry scenario.

An administrator exports a report across several customer organizations. A generic endpoint accepts a filter object and uses it directly in ORM expressions. The service must enforce the administrator's actual scope, allow-list reportable fields, limit row count, protect exports, record the request and avoid returning hidden fields. Authorization must be checked when the export is generated and when it is downloaded.

## 22. Metrics and effectiveness

| Metric | Definition | Interpretation |
|---|---|---|
| Secure pattern adoption | Use of approved parameterization, DTO, authorization and output APIs | Sample code; imports alone are insufficient |
| Critical sink coverage | High-risk interpreter and authority sinks with review/test coverage | Requires source-to-sink inventory |
| Security regression coverage | Security defects with automated regression tests | Test quality and completeness matter |
| Recurrence by root cause | Repeated defects in the same weakness class or component | Indicates systemic engineering gaps |
| SAST precision | Confirmed actionable findings / reviewed findings | Track per language and ruleset |
| Remediation lead time | Confirmed finding to verified fix | Segment by severity and exploitability |
| Authorization negative-test coverage | Protected operations with prohibited-access tests | Endpoint and workflow coverage |
| Secret exposure response | Time to revoke/rotate and close leaked credential | Repository deletion is not revocation |
| Dependency remediation | Time to update vulnerable or unsupported packages | Include reachability and exploitation context |
| Secure review completion | Material changes with recorded security review | Quality sampling required |

Do not optimize for a low number of findings or low release-block rate in isolation. Those metrics may reflect weak detection. Measure coverage, recurrence, remediation and control effectiveness together.

## 23. Procedure: establish a secure code review programme

### Purpose and authorization

Establish a repeatable review process for source changes. Obtain engineering leadership approval and identify repositories, branches, applications and reviewers in scope.

### Prerequisites

- Source repository access with least privilege.
- Application and data-flow documentation.
- Secure coding policy and vulnerability severity criteria.
- SAST/SCA/secret scanning tools or a documented manual alternative.
- Test environment and synthetic data.
- Finding tracker and remediation ownership.

### Steps

1. Inventory repositories, languages, frameworks and criticality.
2. Define review triggers: authentication, authorization, data access, file handling, cryptography, external integrations, dependency changes, admin functions and security configuration.
3. Establish a pull-request template with security impact and test evidence.
4. Train reviewers in source-to-sink and authority-flow analysis.
5. Configure high-confidence static checks and dependency/secret scanning.
6. Require human review for security-sensitive changes.
7. Apply the procedure in Section 17.
8. Record findings with root cause and reproducible evidence.
9. Require regression tests for fixed security defects.
10. Sample closed pull requests to assess missed issues and review quality.
11. Review rules, false-positive rates and recurring defects quarterly or after a material incident.
12. Feed findings into developer training, architecture patterns and security requirements.

### Stop and escalation conditions

- A real credential or private key appears in the diff or repository.
- The change creates a bypass of authentication, authorization or audit.
- The code handles sensitive production data outside approved controls.
- The reviewer cannot establish intended security behavior.
- A suspected active compromise is discovered.

Escalate credential exposure for rotation and incident assessment. Do not paste secrets into review comments or public tickets.

### Closure criteria

The programme is operating when sampled changes show reviewers can identify high-risk sources and sinks, findings have owners, fixes have regression tests, security-sensitive exceptions expire, and recurring weaknesses feed back into engineering controls.

## 24. Lab roadmap and safe exercises

The companion lab pack is a separate deliverable so exercises can be executed and assessed independently. Initial exercises should use synthetic records and isolated containers:
- SQL injection caused by concatenation versus parameter binding.
- Stored and reflected XSS with context-specific output encoding.
- Mass assignment and object-level authorization in a multi-tenant API.
- Path traversal and safe upload storage.
- SSRF destination allow-list and egress controls.
- Unsafe deserialization and parser resource limits.
- Race condition in a one-time assessment submission.
- Log injection and secret redaction.

Each lab must include exact runtime versions, setup, network isolation, seeded data, step-by-step learner procedure, expected result, remediation, teardown, evidence and scoring rubric. No exercise should target a public service or real customer environment.

## 25. Limitations and unresolved engineering questions

- Framework defaults and APIs change. Verify against exact deployed versions.
- ORM use does not guarantee safe query construction.
- Static-analysis coverage is incomplete and rule quality varies.
- Secure coding cannot compensate for insecure architecture or missing business requirements.
- Authorization policy must reflect actual product relationships and delegated roles.
- Cryptographic parameters require algorithm and hardware-specific review.
- SSRF prevention requires application and network-layer controls.
- File and document processing may require sandboxing and specialist review.
- Regulatory applicability must be determined for the legal entity, product and processing context.
- Exact ASVS requirement identifiers should be linked to the official 5.0.0 release in a later traceability workbook.

## 26. Related chapters

- [AppSec Fundamentals](../01-fundamentals/APPSEC-FUNDAMENTALS.md)
- [Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- Identity and Access Security (planned Chapter 05)
- Web Application Security (planned Chapter 06)
- API Security (planned Chapter 07)
- Software Supply Chain and DevSecOps (planned specialist chapter)

## 27. References

1. OWASP ASVS 5.0.0, stable release published 2025-05-30: https://asvs.owasp.org/
2. OWASP SQL Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
3. OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
4. OWASP Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html
5. OWASP Secure Code Review Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html
6. OWASP Proactive Controls: https://top10proactive.owasp.org/
7. MITRE CWE 2025 Top 25: https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25
8. MITRE CWE 2025 methodology: https://cwe.mitre.org/top25/archive/2025/2025_methodology.html
9. SEI CERT Coding Standards: https://cmu-sei.github.io/secure-coding-standards/
10. NIST SP 800-218 SSDF v1.1: https://csrc.nist.gov/pubs/sp/800/218/final

## 28. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial secure coding and code review engineering playbook |
