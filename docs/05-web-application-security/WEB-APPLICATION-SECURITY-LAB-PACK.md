# Web Application Security Lab Pack

| Field | Value |
|---|---|
| Document ID | UAPPSEC-05-LAB-001 |
| Status | Draft lab specifications |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Isolated browser and web application security exercises |
| Classification | Public |

## 1. Safety, authorization and lab setup

These exercises are for local applications, disposable containers and synthetic data. Do not perform them against public websites, customer environments, employee accounts or production services without explicit written authorization and a scoped rules-of-engagement document.

### Mandatory safety controls

- Run vulnerable targets on loopback or a private isolated lab network.
- Do not expose vulnerable containers to the public internet.
- Use synthetic accounts, tenants, documents and business records.
- Do not use real credentials, customer data, production API keys or private files.
- Do not perform destructive tests, uncontrolled fuzzing, denial of service or broad scanning.
- Do not access cloud metadata, internal enterprise services or third-party systems from a lab unless a separate controlled simulation explicitly provides them.
- Restrict container CPU, memory, disk, process count and network egress.
- Snapshot or rebuild the lab before each exercise.
- Keep test evidence sanitized.
- Stop immediately if traffic leaves the lab network or real data is encountered.

### Suggested lab components

A training environment may use:
- One vulnerable web application with intentionally insecure routes.
- One browser profile dedicated to training.
- One intercepting proxy configured for the local target.
- Browser developer tools.
- Local database with synthetic records.
- Local file storage and a test upload processor.
- Optional reverse proxy for host/header/cache exercises.
- Optional test DNS resolver and mock external service for SSRF allow-list exercises.
- A log viewer with request IDs.

Pin container image digests and dependency versions before declaring a lab reproducible. This document defines exercises; it does not claim that a container implementation has already been built or independently validated.

## 2. Common learner record

For every lab, record learner, date, lab ID, target version, isolated network confirmation, test account/role, preconditions, steps, expected result, observed result, root cause, security impact, remediation, regression tests, sanitized evidence, teardown and reviewer outcome.

Never include passwords, session cookies, bearer tokens, API keys, private keys, recovery codes or real personal data.

## 3. Lab 01: Host header and trusted proxy boundary

**Objective:** Verify that untrusted Host and forwarding headers cannot control security-sensitive absolute URLs or routing decisions.

**Weakness class:** Security misconfiguration / trust-boundary failure.

### Procedure

1. Start the local target behind the lab reverse proxy.
2. Record the canonical configured public origin.
3. Submit a normal request and inspect generated absolute links.
4. In the authorized local environment, submit a request with an alternate Host value.
5. Submit spoofed X-Forwarded-Host and X-Forwarded-Proto values from the untrusted client side.
6. Trigger a harmless link-generation feature such as a test invitation or preview URL.
7. Verify the generated origin remains the configured canonical origin.
8. Configure the proxy to strip untrusted forwarding headers and add trusted values.
9. Configure the application allowed-host list and explicit public origin.
10. Repeat the test and add regression coverage.

**Expected result:** Untrusted request headers cannot control password-reset/invitation origins, routing, tenant selection or cache behavior.

**Evidence:** Redacted requests/responses, proxy configuration and regression output.

**Teardown:** Remove test routes and proxy overrides.

## 4. Lab 02: Reflected and stored XSS output context

**Objective:** Demonstrate why output encoding must match the exact rendering context.

**Weakness class:** CWE-79, improper neutralization of input during web page generation.

### Procedure

1. Create two synthetic users and one test content record.
2. Identify a reflected search parameter and a stored profile/comment field.
3. Submit harmless marker strings containing characters meaningful to HTML.
4. Inspect the raw response and rendered DOM.
5. Determine whether the value is placed in HTML text, attribute, URL or script context.
6. Verify whether the browser interprets the value as markup or executable content; use a harmless local proof only.
7. Fix the output using context-appropriate encoding or a maintained sanitizer if rich HTML is required.
8. Replace unsafe DOM insertion with safe text APIs.
9. Test stored content in user, administrator, email-preview and export views.
10. Add regression tests for each output context.

**Expected result:** Untrusted input remains data and cannot execute as active browser content. Rich HTML is constrained to the documented allow-list.

**Evidence:** Before/after DOM, sanitized HTTP trace, code change and tests.

**Teardown:** Delete test content and accounts.

## 5. Lab 03: DOM-based XSS source-to-sink review

**Objective:** Trace browser-controlled data into DOM execution sinks.

**Prerequisites:** Local JavaScript application with a search/preview feature.

### Procedure

1. Identify sources such as location.search, location.hash, postMessage and local storage.
2. Search client code for innerHTML, outerHTML, insertAdjacentHTML, document.write and dynamic script construction.
3. Trace whether untrusted data can reach a sink.
4. Reproduce only with a harmless local marker.
5. Replace unsafe rendering with textContent or a safe component/template.
6. If HTML rendering is required, apply a maintained sanitizer with a strict policy.
7. Validate postMessage origin and message schema if used.
8. Add a regression test for the source-to-sink path.
9. Review alternate routes and error states.

**Expected result:** Untrusted browser data cannot reach executable DOM contexts without validated, context-safe handling.

**Evidence:** Source-to-sink trace, before/after code and regression output.

**Teardown:** Remove test script and browser storage.

## 6. Lab 04: CSRF protection for cookie-authenticated state change

**Objective:** Verify that a browser cannot be induced to perform a protected state-changing action without the required anti-forgery proof.

**Prerequisites:** Local application with synthetic profile-change operation and cookie session.

### Procedure

1. Authenticate as a synthetic test user.
2. Identify a state-changing operation and its expected anti-forgery control.
3. Submit the operation normally and record the successful behavior.
4. In a local attacker-origin simulation, attempt the same state change without the anti-forgery token.
5. Repeat with a missing, invalid or session-mismatched token.
6. Inspect SameSite cookie policy and Origin validation.
7. Ensure GET does not change state.
8. Implement or enable framework anti-forgery protection.
9. Add tests for missing, invalid, reused and mismatched tokens.
10. Verify legitimate form/API behavior still works.

**Expected result:** Cross-site state-changing requests fail unless the application receives valid anti-forgery proof bound to the user/session.

**Evidence:** Redacted request/response, cookie metadata, server state and test output.

**Teardown:** Delete synthetic user and sessions.

## 7. Lab 05: CORS policy validation

**Objective:** Verify that only explicitly trusted origins can read credentialed cross-origin responses.

**Prerequisites:** Local app origin and separate local test origin.

### Procedure

1. Configure the intended trusted origin.
2. Send a preflight request from the trusted origin and record allowed methods/headers.
3. Send a request from an untrusted origin.
4. Test Origin: null in the local harness.
5. Inspect Access-Control-Allow-Origin, Access-Control-Allow-Credentials, Vary and preflight behavior.
6. Verify the server does not reflect arbitrary Origin values.
7. Verify wildcard origin is not combined with credentials.
8. Review actual request authorization independently of CORS.
9. Apply explicit origin, method and header allow-lists.
10. Add positive and negative tests for every configured origin.

**Expected result:** Only approved origins receive the intended browser-readable access. CORS is not used as the sole server-side authorization control.

**Evidence:** Preflight/actual response headers and regression tests.

**Teardown:** Remove test origins and local policy.

## 8. Lab 06: CSP rollout and script execution restriction

**Objective:** Build a restrictive CSP and verify it does not silently permit arbitrary script execution.

**Prerequisites:** Local application with first-party script and one approved third-party test resource.

### Procedure

1. Inventory scripts, styles, images, fonts, API connections and frame requirements.
2. Start with a report-only policy in the lab.
3. Collect violations from normal application use.
4. Identify required sources and remove unnecessary destinations.
5. Add nonce- or hash-based script execution where supported.
6. Avoid unsafe-inline and unsafe-eval unless a documented exception is required for the exercise.
7. Restrict object-src, base-uri, frame-ancestors and form-action.
8. Switch to enforcement in the lab.
9. Verify unapproved script loads are blocked.
10. Test login, SSO, payments, uploads and other legitimate flows.
11. Add a policy regression check to deployment validation.

**Expected result:** Only approved resources and script execution paths are permitted; policy changes are monitored and do not break essential functionality.

**Evidence:** Policy, report-only observations, enforcement results and compatibility tests.

**Teardown:** Restore baseline CSP.

## 9. Lab 07: SQL injection prevention

**Objective:** Verify that user input remains data in database operations.

**Prerequisites:** Local app and synthetic database with disposable records.

### Procedure

1. Identify search, filter, sort and report endpoints.
2. Review query construction and ORM/raw SQL use.
3. Submit benign test values containing SQL metacharacters to the local lab.
4. Observe whether query structure or result scope changes.
5. Inspect source for string concatenation and dynamic identifiers.
6. Replace unsafe value interpolation with parameterized queries.
7. For dynamic sort/column identifiers, use a fixed allow-list.
8. Ensure database identity has only required privileges.
9. Add regression tests for search, filter, sort, pagination and report paths.
10. Verify database errors are not exposed to clients.

**Expected result:** Input values cannot alter query structure or access unauthorized rows. Legitimate search behavior remains functional.

**Evidence:** Redacted request, query/code review, database test output and regression tests.

**Teardown:** Rebuild synthetic database.

## 10. Lab 08: SSRF allow-list and redirect handling

**Objective:** Verify a server-side URL-fetch feature cannot reach destinations outside its approved destination policy.

**Safety:** Use only a mock destination service and synthetic internal-address simulator inside the isolated lab. Do not probe real metadata endpoints or enterprise internal networks.

### Procedure

1. Configure a local URL preview/fetch feature.
2. Define one approved mock hostname and one denied mock destination.
3. Submit the approved URL and verify expected content retrieval.
4. Submit a disallowed hostname and verify denial.
5. Test a hostname that resolves to a denied address in the local DNS simulator.
6. Test a redirect from an approved mock host to a denied mock destination.
7. Test alternate IPv4/IPv6 representations within the simulator.
8. Implement scheme and hostname allow-lists, DNS/IP validation, redirect revalidation, egress restrictions, timeout and response-size limits.
9. Re-run all positive and negative cases.
10. Verify logs record policy decisions without leaking sensitive response bodies.

**Expected result:** The fetcher contacts only explicitly approved destinations and revalidates every redirect/resolution.

**Evidence:** Mock DNS configuration, redacted requests, egress logs and tests.

**Teardown:** Stop mock DNS and fetch services.

## 11. Lab 09: Secure file upload and download

**Objective:** Verify uploaded content is treated as untrusted and downloads enforce resource authorization.

**Prerequisites:** Local file service, two synthetic users and a private storage directory.

### Procedure

1. Upload an allowed synthetic document as user A.
2. Verify the application generates an opaque server-side storage name.
3. Attempt a disallowed extension and content-type mismatch using a harmless test file.
4. Verify rejection or quarantine.
5. Review storage location and confirm uploads are not executable from the application web root.
6. Attempt to download user A's file as user B using its synthetic identifier.
7. Verify object authorization denies access.
8. Verify Content-Disposition, Content-Type and nosniff behavior.
9. Add size limits, parser isolation and archive extraction constraints if relevant.
10. Add tests for type mismatch, oversized file, unauthorized download and deletion.

**Expected result:** Upload policy is enforced server-side, files are stored safely and every download is authorized independently.

**Evidence:** Sanitized file metadata, storage configuration, response headers and test results.

**Teardown:** Delete test files and accounts.

## 12. Lab 10: Business logic, replay and idempotency

**Objective:** Verify one-time or limited business actions cannot be repeated or reordered to violate business rules.

**Prerequisites:** Local synthetic order, coupon, assessment or approval workflow.

### Procedure

1. Document allowed states and transitions.
2. Complete one normal synthetic transaction.
3. Repeat the same request using the same idempotency key or transaction reference.
4. Submit a request with stale state/version.
5. Attempt to skip a required workflow step.
6. Submit concurrent requests against a one-unit synthetic inventory or one-time entitlement.
7. Inspect database state and audit events.
8. Implement atomic constraints, idempotency, version checks and server-side state transitions.
9. Add positive, replay, stale-state and concurrent regression tests.
10. Verify failed operations do not partially mutate state.

**Expected result:** Business invariants hold under replay, concurrency and out-of-order requests. A UI control is not the enforcement mechanism.

**Evidence:** State diagram, redacted requests, transaction records and regression results.

**Teardown:** Reset synthetic workflow data.

## 13. Lab 11: Cache isolation between users and tenants

**Objective:** Verify that shared caches do not disclose authenticated content across synthetic identities.

**Prerequisites:** Local reverse proxy/cache and two test users or tenants.

### Procedure

1. Create distinct synthetic private responses for user A and user B.
2. Request user A's response and record cache behavior.
3. Request user B's response through the same cache path.
4. Compare body, headers, cache status and cache key behavior.
5. Repeat with a tenant-specific resource.
6. Review Cache-Control, Vary and cache key configuration.
7. Apply private/no-store policy where appropriate and ensure tenant/principal variation is correct.
8. Purge stale test entries.
9. Repeat requests in both orders.
10. Add automated isolation tests and cache invalidation tests.

**Expected result:** No authenticated or tenant-specific response is served to a different principal or tenant.

**Evidence:** Redacted response comparisons, cache configuration and tests.

**Teardown:** Purge all lab cache entries.

## 14. Lab 12: WebSocket message-level authorization

**Objective:** Demonstrate that a successful WebSocket handshake does not authorize every message or resource.

**Prerequisites:** Local WebSocket application with two synthetic users and tenant-scoped channels.

### Procedure

1. Connect user A using the normal authenticated flow.
2. Subscribe to a channel user A is authorized to access.
3. Attempt to subscribe to user B's synthetic private channel.
4. Send a message/action outside user A's role.
5. Test a malformed or oversized message within safe lab limits.
6. Verify per-message authorization, schema validation, tenant binding and rate controls.
7. Add connection expiry/revocation handling.
8. Add regression tests for allowed and denied channel/action combinations.
9. Inspect audit events for actor, channel, action and decision.

**Expected result:** Every message and resource action is authorized independently; tenant and user isolation is preserved.

**Evidence:** Sanitized WebSocket trace, policy code and tests.

**Teardown:** Close sockets and delete test channels.

## 15. Lab 13: Redirect and URL validation

**Objective:** Prevent untrusted destinations from controlling post-login, callback or navigation redirects.

**Prerequisites:** Local application with a redirect parameter.

### Procedure

1. Identify all redirect inputs and destinations.
2. Test a valid internal destination.
3. Test an unapproved external destination in the local lab.
4. Test protocol-relative and alternate-scheme forms.
5. Test encoded and nested URL representations.
6. Review URL parsing and canonicalization.
7. Replace arbitrary redirect URLs with an allow-list or server-side destination key.
8. Test login, logout and recovery flows.
9. Add regression tests for each rejected form.

**Expected result:** Redirects resolve only to approved destinations; no user-controlled external navigation occurs.

**Evidence:** Redacted request/response, URL policy and tests.

**Teardown:** Remove test redirect routes.

## 16. Lab 14: Error handling and security telemetry

**Objective:** Verify that client errors are safe while operational telemetry remains useful and secret-free.

**Prerequisites:** Local application with controlled validation and mock dependency errors.

### Procedure

1. Trigger a known validation error.
2. Trigger a controlled mock dependency timeout.
3. Trigger a controlled malformed upstream response.
4. Inspect client responses for stack traces, internal paths, query text and secrets.
5. Inspect server logs for correlation ID, route, actor, tenant, outcome and error category.
6. Verify passwords, tokens, cookies, API keys and personal data are not logged.
7. Ensure authorization dependency failure does not result in permissive access.
8. Add structured logging and redaction rules.
9. Add tests for response safety and log redaction.
10. Verify alerting can distinguish expected validation failures from suspicious repeated behavior.

**Expected result:** Client responses reveal no sensitive internals; logs support investigation without retaining credentials or unnecessary personal data.

**Evidence:** Sanitized response, log sample and regression results.

**Teardown:** Delete lab logs and test data.

## 17. Lab 15: Production configuration and exposed artifacts

**Objective:** Verify a web deployment does not expose development files, debug endpoints or unsafe default configuration.

**Prerequisites:** Local staging-like deployment built from a disposable application artifact.

### Procedure

1. Inventory routes and static asset directories.
2. Review production debug settings and error pages.
3. Check for sample applications, default accounts and test endpoints.
4. Review source map exposure and confirm no embedded secrets.
5. Review security headers on success, redirect, error and static responses.
6. Verify administrative routes require the intended access policy.
7. Verify origin access cannot bypass required edge controls in the lab topology.
8. Remove unnecessary artifacts and restrict management interfaces.
9. Add deployment checks for debug flags, exposed files and security headers.
10. Rebuild from a clean artifact and repeat.

**Expected result:** No unintended debug, backup, configuration or repository artifacts are exposed; administrative surfaces are restricted.

**Evidence:** Route inventory, deployment configuration and test output.

**Teardown:** Destroy staging artifact and test credentials.

## 18. Assessment rubric

| Criterion | Points |
|---|---:|
| Identifies asset, trust boundary and business requirement | 10 |
| Explains vulnerability root cause and attack preconditions | 15 |
| Reproduces safely using synthetic data | 15 |
| Captures clear and sanitized evidence | 10 |
| Implements a root-cause remediation | 20 |
| Adds positive and negative regression tests | 15 |
| Explains residual risk and operational monitoring | 10 |
| Completes teardown and records limitations | 5 |
| **Total** | **100** |

Suggested interpretation: 90–100 strong independent engineering; 75–89 working competence with review; 60–74 guided remediation required; below 60 repeat the exercise. These are training thresholds, not certification.

## 19. Instructor review checklist

- Was the target owned or explicitly authorized?
- Was the environment isolated?
- Were accounts and data synthetic?
- Did the learner identify the correct trust boundary?
- Did the test validate impact rather than rely on a scanner label?
- Did the fix address root cause and all relevant paths?
- Were positive and negative regression tests added?
- Were secrets and personal data excluded from evidence?
- Were version and configuration details recorded?
- Was teardown completed?
- Were residual risks documented?

## 20. References

1. OWASP Top 10:2025: https://owasp.org/Top10/2025/
2. OWASP ASVS 5.0.0: https://asvs.owasp.org/
3. OWASP Web Security Testing Guide v4.2: https://owasp.org/www-project-web-security-testing-guide/
4. OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
5. MDN Web Security: https://developer.mozilla.org/en-US/docs/Web/Security
6. IETF HTTP Semantics, RFC 9110: https://www.rfc-editor.org/rfc/rfc9110.html
7. NIST SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final

## 21. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial web application security lab specifications |
