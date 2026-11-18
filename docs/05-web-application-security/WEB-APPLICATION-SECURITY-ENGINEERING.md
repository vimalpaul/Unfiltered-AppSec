# Web Application Security Engineering Playbook

| Field | Value |
|---|---|
| Document ID | UAPPSEC-05-001 |
| Status | Draft engineering baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Browser-based applications, web servers, application frameworks, web gateways and web-facing business workflows |
| Classification | Public |

## 1. Executive summary

Web application security is the engineering discipline of protecting the complete web request and response lifecycle, including browser execution, identity, sessions, application logic, APIs, data access, integrations, deployment infrastructure and operational response.

A web application is not secure merely because it has HTTPS, a WAF, a vulnerability scan or a clean penetration-test report. Security must be designed and enforced at the correct trust boundaries. Every request must be interpreted safely, authenticated where required, authorized for the exact action and resource, processed with constrained dependencies, and logged without exposing secrets.

The security objective is to preserve:
- **Confidentiality:** data is disclosed only to authorized subjects and services.
- **Integrity:** users and systems cannot alter data or workflows outside approved authority.
- **Availability:** application and dependencies remain resilient to misuse, faults and resource exhaustion.
- **Authenticity:** identities, origins, messages and transactions are verified as intended.
- **Accountability:** material security events can be reconstructed with trustworthy evidence.
- **Privacy:** personal data is collected, processed, retained and disclosed only for justified purposes.

This playbook turns architecture, requirements, secure implementation, testing, remediation and operational monitoring into one connected workflow.

## 2. Purpose, audience and applicability

### 2.1 Purpose

Provide an actionable reference to design, build, review, test and operate secure web applications. It supports application security reviews, secure design reviews, code review, web penetration testing, vulnerability management, architecture assessments, security acceptance, incident response and audit evidence.

### 2.2 Audience

Application developers, AppSec engineers, security architects, product security teams, QA engineers, DevSecOps/platform engineers, penetration testers, SOC analysts, technical product owners, technology leaders and auditors.

### 2.3 Scope

In scope:
- Traditional server-rendered applications and single-page applications (SPA).
- Browser-based portals, dashboards, administrative consoles and customer applications.
- Web servers, reverse proxies, API gateways, CDNs and web application firewalls.
- HTTP/1.1, HTTP/2 and HTTP/3 behavior relevant to application security.
- Browser security boundaries, DOM, JavaScript, storage, cookies and cross-origin controls.
- Authentication and session integration (full identity lifecycle is covered in Chapter 07).
- Authorization, business logic, workflow and tenant isolation.
- Input handling, output encoding, injection and deserialization.
- File upload, download, document rendering and media processing.
- CORS, CSP, CSRF, clickjacking and browser policy.
- WebSockets, server-sent events and real-time browser channels.
- Caching, proxy behavior, redirects, error handling and rate controls.
- Web application deployment, configuration and security telemetry.
- Application testing and verification.

Adjacent chapters:
- Chapter 04 owns secure coding principles and language-specific code review patterns.
- Chapter 06 will own API and service protocol security in depth.
- Chapter 07 owns identity, authentication, federation, session and IAM engineering.
- Chapter 02 owns architecture, data-flow and threat-model foundations.
This chapter references those areas and focuses on web-specific interaction and enforcement.

### 2.4 Assumptions and limitations

- The system owner has authorized the design review or test.
- The application has a defined business owner, data classification and deployment boundary.
- Examples are technology-neutral unless a stack is explicitly named.
- Exact behavior depends on browser, framework, proxy, server and version.
- This is an engineering baseline, not legal advice, certification, audit evidence or a guarantee of security.
- Testing must be performed in an authorized environment with synthetic data unless written scope explicitly allows otherwise.

## 3. Web application architecture and request lifecycle

### 3.1 Logical architecture

~~~mermaid
flowchart LR
    U[User / Browser] --> DNS[DNS and Domain]
    DNS --> CDN[CDN / Edge / WAF]
    CDN --> RP[Reverse Proxy / Load Balancer]
    RP --> WEB[Web Server / Front End]
    WEB --> APP[Application Services]
    APP --> AUTH[Identity and Policy Services]
    APP --> DB[(Database)]
    APP --> OBJ[(Object / File Storage)]
    APP --> Q[Queue / Background Workers]
    APP --> EXT[External APIs / Integrations]
    WEB --> TEL[Security Telemetry]
    APP --> TEL
    RP --> TEL
    AUTH --> TEL
    TEL --> SIEM[Monitoring / Detection / Response]
~~~

This is a logical view. Deployments may combine or split components. Each component has a separate trust boundary, identity, configuration and failure mode.

### 3.2 Typical browser request sequence

~~~mermaid
sequenceDiagram
    participant B as Browser
    participant E as Edge / WAF
    participant P as Reverse Proxy
    participant A as Application
    participant I as Identity / Policy
    participant D as Data Store
    B->>E: HTTPS request
    E->>E: TLS, edge policy, request limits
    E->>P: Forward request
    P->>P: Normalize and route request
    P->>A: Forward trusted request context
    A->>A: Parse, validate and classify request
    A->>I: Authenticate / authorize if required
    I-->>A: Identity and policy decision
    A->>D: Execute constrained data operation
    D-->>A: Result
    A->>A: Encode response and record event
    A-->>P: HTTP response
    P-->>E: Response
    E-->>B: HTTPS response
~~~

The actual order may vary. The security design must define which layer terminates TLS, which headers are trusted, where authentication occurs, where authorization is enforced, how request IDs are propagated and how errors are handled.

### 3.3 Request processing model

For every request, document:
1. Network and TLS acceptance.
2. Host and authority validation.
3. Proxy and forwarding-header trust.
4. HTTP parsing and request normalization.
5. Route and method selection.
6. Content type and body-size enforcement.
7. Authentication/session resolution.
8. CSRF/origin checks where applicable.
9. Input schema and business validation.
10. Function, object, property and tenant authorization.
11. Business workflow/state validation.
12. Data and external-service operations.
13. Output encoding and response shaping.
14. Security event generation and correlation.

Security checks must not exist only in the browser or only in one controller. They must apply at the server-side enforcement point and all alternate execution paths.

## 4. Asset inventory and attack surface

### 4.1 Inventory

Create a maintained inventory of:
- Domains, subdomains and DNS zones.
- Public and private web entry points.
- Applications, routes and HTTP methods.
- SPAs, static assets, server-side rendering and service workers.
- Authentication, SSO, recovery and administrative routes.
- APIs, GraphQL endpoints and WebSocket paths.
- Reverse proxies, ingress controllers, CDNs and WAF policies.
- Frameworks, runtimes, libraries and third-party scripts.
- Databases, object stores, caches, queues and search services.
- File upload, import, export, preview and document-processing features.
- External integrations, webhooks and OAuth clients.
- CI/CD workflows and deployment identities.
- Logging, analytics, telemetry and support tooling.
- Tenant boundaries, sensitive workflows and data classifications.

### 4.2 Attack surface discovery

Use authorized passive and active discovery:
- Review architecture diagrams, route registries and API specifications.
- Inspect application navigation and authenticated roles.
- Review JavaScript bundles and source maps where permitted.
- Inspect browser network traffic for hidden endpoints and parameters.
- Review robots.txt, sitemap.xml and public metadata without treating them as access control.
- Inspect DNS, certificate transparency and public asset inventory within scope.
- Identify default files, debug routes, health endpoints and administrative consoles.
- Review third-party scripts and externally hosted assets.
- Compare documented endpoints with observed routes and server logs.
- Identify legacy, versioned and alternate hostname entry points.

Do not brute-force unrelated infrastructure or enumerate systems outside the written scope.

### 4.3 Attack surface register

| Field | Purpose |
|---|---|
| Asset ID | Stable identifier |
| Hostname / route | Exact entry point |
| Environment | Development, test, staging, production |
| Owner | Accountable service owner |
| Function | Business capability |
| Authentication | Anonymous, session, SSO, service identity |
| Data classification | Public, internal, confidential, restricted |
| Tenant boundary | Tenant scope and isolation method |
| Methods / protocols | HTTP methods and WebSocket/SSE |
| Dependencies | Database, storage, queue, external service |
| Security controls | AuthZ, validation, rate limits, logging, CSP |
| Exposure | Internet, partner, VPN, internal |
| Test status | Not assessed, assessed, remediated, retested |
| Evidence | Traceable report, code, configuration or test reference |

## 5. Trust boundaries and web threat model

### 5.1 Trust boundary examples

- Browser to public web origin.
- Browser to a different origin or subdomain.
- Internet to CDN/WAF.
- CDN/WAF to origin server.
- Reverse proxy to application runtime.
- Application to database/cache/object storage.
- Application to external API or payment provider.
- Web application to identity provider.
- User-controlled file to parser/converter/preview service.
- Tenant A to tenant B.
- User content to privileged administrator interface.
- CI/CD pipeline to production deployment.
- Server-rendered HTML to browser DOM execution.
- Third-party JavaScript to first-party page context.

### 5.2 Threat modeling questions

For each feature:
- What assets and business outcomes must be protected?
- Who can initiate the request and from which trust zone?
- Which inputs are controlled by the browser, user, tenant or third party?
- What identity and permissions are required?
- Which resource and properties can be accessed or changed?
- What state transitions are allowed?
- Which server-side components interpret input?
- Does the feature fetch remote content, parse files or invoke commands?
- Can the action be repeated, parallelized or reordered?
- What happens if a dependency times out or returns malformed data?
- What information is returned in errors, headers, logs and caches?
- What evidence will demonstrate correct enforcement?

### 5.3 Threat model deliverables

A useful threat model includes system context, data-flow diagram, assets and classifications, actors and trust levels, entry points, trust boundaries, abuse cases, security requirements, mitigations, residual risks, owners, verification tests and review date.

Do not treat a threat-model workshop as complete when only a diagram exists. Every material threat should map to a control and a test or documented risk acceptance.

## 6. HTTP protocol and request handling security

### 6.1 HTTP fundamentals

HTTP is a stateless application protocol whose semantics are implemented across clients, proxies, servers and frameworks. Security defects often arise when two components parse, normalize or interpret the same message differently.

Review:
- Request method and method override behavior.
- Request target, path normalization and percent encoding.
- Host and authority handling.
- Header parsing, duplicates and ordering.
- Content-Length and Transfer-Encoding behavior.
- Content-Type and charset handling.
- Connection reuse and protocol translation.
- Redirect behavior and absolute URL construction.
- Cache directives and shared-cache behavior.
- HTTP/2 and HTTP/3 gateway translation.
- Error handling and parser disagreement.

### 6.2 Method controls

Allow only methods required by each route. Do not rely on hiding a button or omitting a method from the UI. Ensure authorization applies to every method and method-override mechanism. Treat OPTIONS and TRACE deliberately; OPTIONS may be needed for CORS preflight and is not automatically a vulnerability. Disable methods only where the architecture and application requirements permit.

### 6.3 Host header and forwarded headers

Host and forwarding headers can affect absolute URL generation, password-reset links, redirect destinations, cache keys, tenant resolution and security decisions.

Controls:
- Configure an explicit allowed-host list.
- Trust forwarding headers only from known proxy addresses or authenticated infrastructure.
- Strip client-supplied forwarding headers at the edge before adding trusted values.
- Avoid using unvalidated Host to construct password-reset or verification links.
- Configure canonical public origin explicitly.
- Test alternate hostnames and direct-origin reachability.
- Ensure caches key responses using the intended host and relevant variation.

### 6.4 Request smuggling and parser disagreement

Request smuggling occurs when front-end and back-end HTTP components disagree about message boundaries or normalization. It can lead to request desynchronization, cache poisoning, routing confusion or unauthorized request execution.

Engineering controls:
- Keep proxy, gateway and origin components patched.
- Use consistent HTTP parsing and protocol translation.
- Reject ambiguous or malformed framing.
- Avoid inconsistent duplicate Content-Length or Transfer-Encoding handling.
- Review HTTP/2-to-HTTP/1.1 downgrade behavior.
- Disable unsafe connection reuse patterns where required.
- Test only in a controlled environment with explicit permission and non-destructive requests.
- Verify mitigations at every intermediary, not only the origin.

### 6.5 Path normalization

Define one canonical path interpretation across CDN, proxy, router, framework and file store. Test encoded slash, dot segments, repeated separators, mixed case where relevant, Unicode normalization and double decoding. Never authorize one normalized path and execute a different representation.

## 7. Browser security model

### 7.1 Same-Origin Policy

The browser's Same-Origin Policy restricts how documents and scripts from one origin interact with resources from another. An origin is based on scheme, host and port. CORS selectively relaxes certain cross-origin read restrictions; it is not a general authorization system and does not stop every cross-site request.

### 7.2 Site, origin and cookie scope

Origin and site are different concepts. SameSite cookie behavior uses site context, while CORS and many DOM access decisions use origin. Subdomains may be same-site but cross-origin. Do not assume a sibling subdomain is trusted merely because it shares a registrable domain.

### 7.3 Browser storage

| Storage | JavaScript access | Typical lifetime | Security considerations |
|---|---|---|---|
| HttpOnly cookie | Not directly readable by script | Cookie/session policy | Still automatically attached; CSRF and session theft via XSS actions remain relevant |
| localStorage | Readable by same-origin script | Persistent | XSS can read values; avoid long-lived bearer tokens |
| sessionStorage | Readable by same-origin script | Tab/session lifecycle | XSS can read values; not a security boundary |
| IndexedDB | Readable by same-origin script | Persistent | Sensitive content exposed to same-origin script compromise |
| In-memory state | Readable by running script | Application runtime | Reduces persistence but not active XSS exposure |
| Service worker cache | Controlled by origin service worker | Persistent until cleared/expired | Cache poisoning, stale content and service-worker takeover risks |

Do not store secrets in browser-accessible storage merely because the application encrypts them with a key available to the same JavaScript runtime.

### 7.4 Service workers

Service workers can intercept requests and serve cached content. Review service-worker registration scope, script integrity and origin, update lifecycle, cache versioning, offline data sensitivity, logout cache clearing, compromised worker persistence and content security policy. A stale service worker may continue serving old application code after a deployment.

## 8. Input handling, validation and canonicalization

### 8.1 Validation model

Validation must be server-side and specific to the business operation. Validate type, length, range, format, cardinality, encoding, allowed values and cross-field consistency. Reject invalid input rather than attempting to repair ambiguous data silently.

### 8.2 Canonicalization

Canonicalize input once at a well-defined boundary before validation and processing. Avoid repeated decode/encode cycles. Define Unicode normalization, path interpretation, case sensitivity, numeric parsing, date/time zones and content-type behavior. Different components must not validate one representation and execute another.

### 8.3 Allow-list validation

Prefer a schema or allow-list for structured fields:
- Known enum values.
- Bounded integer and decimal ranges.
- Explicit date/time format and timezone.
- Maximum string length.
- Allowed file extensions and independently verified file type.
- Expected JSON object structure.
- Explicitly permitted properties.
- Maximum collection size and nesting depth.

Validation is not a substitute for output encoding, parameterized database access or authorization.

### 8.4 Mass assignment

Do not bind an untrusted request directly to a persistence entity or privileged domain object. Use explicit input DTOs and assign server-controlled properties separately. Sensitive properties include tenant ID, owner ID, role, permission, price, discount, approval state, balance, account status and audit fields.

## 9. Output encoding and cross-site scripting (XSS)

### 9.1 XSS model

Cross-site scripting occurs when untrusted content is interpreted as executable browser content in a victim's origin. It may allow unauthorized actions, data access, session abuse, UI manipulation and persistence through stored content.

Common categories:
- Reflected XSS: input is returned in a response and executed in the victim's browser.
- Stored XSS: content is stored and later rendered to users.
- DOM-based XSS: client-side code uses attacker-controlled data in an unsafe DOM sink.
- Mutation-XSS: browser parsing or DOM mutation changes the security meaning of content.

### 9.2 Contextual output encoding

Encoding must match the output context:
- HTML text node: HTML entity encoding.
- HTML attribute: attribute-context encoding and quoted attributes.
- JavaScript: avoid dynamic script construction; use safe data serialization and non-executable data contexts.
- URL: validate destination and encode parameter components.
- CSS: avoid untrusted CSS construction; use safe property/value allow-lists.
- DOM: prefer textContent and safe DOM APIs over innerHTML.

HTML encoding is not universal protection for JavaScript, CSS, URL or HTML attribute contexts.

### 9.3 Rich text and HTML sanitization

If rich HTML is a business requirement:
1. Define supported tags, attributes, URL schemes and CSS properties.
2. Use a maintained HTML sanitizer.
3. Sanitize at a well-defined trust boundary.
4. Avoid post-sanitization string mutation that can reintroduce unsafe markup.
5. Keep sanitizer versions current.
6. Test SVG, MathML, event attributes, malformed markup, URL schemes and browser parser behavior.
7. Apply CSP as defense in depth.
8. Re-test all render contexts, including email previews, exports and admin screens.

Do not use regular expressions as a general HTML sanitizer.

### 9.4 DOM sinks and sources

Review sources such as location, query parameters, fragment, postMessage, referrer, storage, network responses and user-generated content. Review sinks such as innerHTML, outerHTML, insertAdjacentHTML, document.write, eval, Function, setTimeout with string input, dynamic script URLs and unsafe framework bypass APIs.

Use safe text APIs and trusted framework templates. Treat DOM-based data flow as a code-review requirement.

## 10. Cross-Site Request Forgery (CSRF)

### 10.1 Threat

CSRF abuses a browser's automatic credential attachment to cause a victim's authenticated browser to submit an unwanted state-changing request.

### 10.2 Controls

- Use framework-supported anti-forgery tokens for cookie-authenticated state-changing operations.
- Use SameSite cookies as defense in depth, not the only control where risk requires stronger protection.
- Validate Origin and, where appropriate, Referer as supplementary request-origin signals.
- Require non-simple content types or custom headers where suitable for API design, while retaining robust authorization and CSRF controls.
- Do not mutate state through GET or other safe methods.
- Protect login, logout, account recovery, email/MFA changes and privileged actions.
- Apply controls to JSON and form endpoints according to actual browser behavior.
- Ensure token validation is bound to the user/session and not reusable across unrelated contexts.
- Test cross-origin and sibling-subdomain scenarios.

CORS does not replace CSRF protection. A browser may send some cross-origin requests even when the attacker cannot read the response.

## 11. Cross-Origin Resource Sharing (CORS)

### 11.1 CORS behavior

CORS is a browser-enforced mechanism that controls whether scripts from one origin can read certain cross-origin responses. It is not a server-side access-control policy and does not stop non-browser clients.

### 11.2 Secure configuration

- Use an explicit allow-list of trusted origins.
- Avoid reflecting arbitrary Origin values.
- Do not combine wildcard origin with credentialed requests.
- Set Access-Control-Allow-Credentials only when required.
- Limit allowed methods and headers to the application requirement.
- Set a deliberate Access-Control-Max-Age.
- Include Vary: Origin when response behavior varies by Origin and shared caching is involved.
- Validate preflight behavior and actual request authorization separately.
- Avoid trusting null origin unless there is a specific reviewed use case.
- Test all production, preview and legacy origins.

A permissive CORS response does not by itself prove that sensitive data is exploitable; assess whether credentials are sent, whether the browser exposes the response and whether the resource has sensitive content.

## 12. Content Security Policy (CSP) and browser response headers

### 12.1 CSP design

CSP is a defense-in-depth policy that restricts which resources and execution contexts the browser may load or execute.

A deployment should:
- Begin with report-only observation where appropriate.
- Define default-src and explicit resource directives.
- Prefer nonce- or hash-based script execution.
- Avoid unsafe-inline and unsafe-eval unless a documented migration exception exists.
- Restrict object-src, base-uri and frame-ancestors.
- Define connect-src for API, WebSocket and telemetry destinations.
- Restrict form-action and frame-src where appropriate.
- Use report endpoints that resist abuse and avoid leaking sensitive URLs.
- Test all application features, browser versions and third-party scripts.
- Version and review CSP changes with the application.

CSP is not a replacement for safe output encoding or correct authorization. A policy that blocks core scripts can create an availability issue; roll out with measured monitoring.

### 12.2 Other security headers

| Header | Purpose | Engineering guidance |
|---|---|---|
| Strict-Transport-Security | Directs browsers to use HTTPS | Enable after HTTPS readiness; include subdomains only after inventory and readiness review |
| X-Content-Type-Options: nosniff | Prevents MIME sniffing in relevant contexts | Set for appropriate responses |
| Referrer-Policy | Controls referrer information | Choose privacy-preserving policy that supports application needs |
| Permissions-Policy | Restricts selected browser features | Disable unused capabilities and document required ones |
| frame-ancestors (CSP) | Controls embedding | Prefer CSP frame-ancestors over legacy X-Frame-Options for modern policy |
| Cache-Control | Controls caching | Prevent shared caching of sensitive authenticated responses |
| Cross-Origin-Opener-Policy | Isolates browsing context groups | Assess popup, SSO and payment integration impact |
| Cross-Origin-Resource-Policy | Restricts cross-origin resource loading | Set according to asset sharing requirements |
| Cross-Origin-Embedder-Policy | Enables cross-origin isolation when combined correctly | Test third-party resources and application compatibility |

Headers must be set at the correct response boundary and verified on success, redirect, error and static asset responses.

## 13. Clickjacking and UI redress

An attacker may embed a target page in a frame and trick a user into interacting with hidden or misleading controls.

Controls:
- Set CSP frame-ancestors to approved framing origins or none.
- Use X-Frame-Options where legacy browser support requires it.
- Protect sensitive actions with explicit confirmation and step-up where appropriate.
- Avoid relying on JavaScript frame-busting as the primary control.
- Test login, payment, account change and administrative pages.
- Document legitimate partner embedding and exact allowed origins.

## 14. Injection vulnerabilities

### 14.1 Injection model

Injection occurs when untrusted data changes the intended structure or semantics of an interpreter input. The correct defense depends on the interpreter and operation.

### 14.2 SQL injection

- Use parameterized queries or safe ORM binding.
- Do not concatenate untrusted values into SQL structure.
- Use allow-lists for dynamic identifiers such as column names and sort directions.
- Apply least-privileged database accounts.
- Separate read and write privileges where practical.
- Avoid exposing raw database errors.
- Test search, filter, sort, report, export and stored-procedure paths.
- Verify second-order input paths where stored data is later used in a query.

### 14.3 NoSQL and query injection

Use typed query builders and explicit schemas. Do not pass arbitrary client JSON directly into query operators. Reject unexpected operators and object types. Test nested JSON, filter expressions, aggregation pipelines and regular-expression features. Apply least privilege and query time/resource limits.

### 14.4 OS command injection

Avoid invoking a shell with user-controlled strings. Prefer library APIs and argument arrays with fixed executable paths. Validate arguments by semantic allow-list, restrict process identity and filesystem access, apply timeouts and output limits, and isolate the worker. Do not assume shell escaping alone makes arbitrary command composition safe.

### 14.5 Template injection

Do not compile or evaluate user-controlled templates in a privileged application process. Use fixed templates and safe data binding. If user-authored templates are a requirement, isolate execution, restrict available objects and methods, limit CPU/memory/time and prevent filesystem/network access unless explicitly required.

### 14.6 LDAP, XPath and expression injection

Use safe query APIs and escaping specific to the target interpreter. Separate syntax from values. Apply least privilege to directory queries and constrain search base, attributes and result limits.

## 15. Server-Side Request Forgery (SSRF)

### 15.1 Threat

SSRF occurs when a server makes a network request influenced by an attacker. It can expose internal services, cloud metadata, control planes, local resources or trusted network endpoints.

### 15.2 Common features at risk

- URL preview and link unfurling.
- Image import and remote avatar.
- PDF/document conversion.
- Webhook testing and callback configuration.
- RSS/feed import.
- Proxy and fetch endpoints.
- External integration setup.
- File conversion and media processing.
- Server-side browser automation.

### 15.3 Defensive architecture

- Prefer destination allow-lists over arbitrary URLs.
- Restrict protocols to those required.
- Resolve hostnames and validate all resulting IP addresses.
- Block loopback, link-local, private, multicast, reserved and internal ranges unless explicitly required.
- Revalidate after every redirect and DNS resolution.
- Defend against DNS rebinding and time-of-check/time-of-use changes.
- Disable redirects or limit and validate each redirect hop.
- Use controlled egress proxies and network segmentation.
- Block cloud metadata endpoints at network level where possible.
- Apply connect/read timeouts, response size limits and content-type limits.
- Do not pass internal response bodies directly to users.
- Run fetchers in isolated low-privilege workers.
- Log destination and policy decision without recording sensitive response content.

A string-prefix check or single DNS lookup is not sufficient. IPv4, IPv6, mapped addresses, alternative encodings and redirect behavior must be considered.

## 16. File upload, download and document processing

### 16.1 Upload threat model

Uploaded content is untrusted even when the browser reports an expected MIME type or extension. Risks include malware, parser vulnerabilities, stored XSS, path traversal, archive bombs, resource exhaustion, overwrite, unauthorized disclosure and server-side code execution.

### 16.2 Upload controls

1. Require authorization for upload and destination resource.
2. Enforce maximum request size at edge, proxy and application.
3. Allow-list business-required extensions.
4. Validate content using file signature and parser-level inspection; do not trust filename or Content-Type alone.
5. Generate server-side opaque storage names.
6. Store outside the executable web root or in private object storage.
7. Prevent uploaded content from inheriting application cookies/origin privileges.
8. Scan or quarantine according to risk and business need.
9. Apply decompression limits and archive entry/path checks.
10. Protect against polyglot and active content formats.
11. Restrict image/document conversion in isolated workers.
12. Record uploader, tenant, resource, hash, size and scan result.
13. Reauthorize download and preview independently.
14. Define retention, deletion and incident handling.

### 16.3 Download controls

- Use opaque identifiers rather than direct filesystem paths.
- Enforce object and tenant authorization on every download.
- Set safe Content-Disposition and Content-Type.
- Use X-Content-Type-Options: nosniff.
- Avoid rendering untrusted HTML/SVG inline on the application's authenticated origin.
- Use a separate origin or attachment delivery for risky active content.
- Protect signed URLs with short expiry, scope and audience.
- Prevent cache leakage of private downloads.
- Ensure deletion and access revocation affect generated links where required.

### 16.4 Archive extraction

Defend against path traversal in archive entries, absolute paths, symbolic links, nested archives, decompression bombs, excessive file counts and overwrite. Extract to a dedicated temporary directory with strict quotas and canonical path checks. Do not trust the archive's declared uncompressed size.

## 17. Business logic and workflow security

### 17.1 Why business logic requires manual reasoning

Business logic flaws arise when an application technically accepts valid requests but fails to enforce the intended business rule, ownership, sequence, quantity, approval, uniqueness or transaction constraint.

A scanner may not understand that a learner should not complete a course without passing an assessment, a customer cannot approve their own refund, a user cannot reuse a one-time coupon, or a vendor cannot change another tenant's contract.

### 17.2 Workflow modeling

For each business process, define:
- Actors and roles.
- Resource ownership and tenant.
- Allowed states and transitions.
- Preconditions and postconditions.
- Approval and separation-of-duties rules.
- Quantity, value and frequency limits.
- One-time or idempotent actions.
- Time windows and expiry.
- Concurrency and transaction semantics.
- Reversal, cancellation and dispute behavior.
- Audit and notification requirements.

### 17.3 Workflow verification

Test direct access to later steps, skipped approval, repeated submission, replay, parallel requests, parameter tampering, client-side price changes, negative/zero/overflow quantities, stale object state, alternate endpoints, race conditions, privilege changes during a workflow, and cross-tenant references.

Use server-side state machines and database transaction constraints. A disabled button is not a business rule.

### 17.4 Race conditions and TOCTOU

Where multiple requests can change the same state, use atomic database operations, row/version locking, uniqueness constraints, optimistic concurrency or idempotency keys. Recheck authorization and business preconditions at the point of commit. Do not rely on a prior UI or API read as proof that a later write remains valid.

## 18. Caching and shared infrastructure

### 18.1 Cache risks

- Authenticated response disclosed to another user.
- Tenant-specific response cached under a shared key.
- Cache poisoning through unkeyed headers or host data.
- Stale authorization or role data.
- Sensitive content retained after logout or account change.
- CDN caching of private downloads.
- Inconsistent normalization between cache and origin.

### 18.2 Controls

- Use Cache-Control: no-store for highly sensitive responses where appropriate.
- Define private/public cache policy per route and data class.
- Include all security-relevant variation in cache keys.
- Avoid trusting unkeyed user-controlled headers.
- Set correct Vary behavior.
- Invalidate cache on permission changes, object updates and tenant changes.
- Test CDN and origin behavior independently.
- Avoid caching authorization decisions beyond defined freshness and revocation objectives.
- Ensure error and redirect responses do not leak sensitive content.

## 19. Rate limiting, abuse prevention and resource exhaustion

Rate controls must protect both application availability and business processes. Apply limits at multiple levels where appropriate:
- Source/network identity.
- Authenticated subject.
- Tenant.
- Session or device.
- API/client identity.
- Resource or expensive operation.
- Global system capacity.

Use separate policy for login, recovery, OTP, search, export, upload, password reset, invitation, report generation, expensive queries and business transactions.

Controls should include burst and sustained limits, concurrency caps, request/body limits, pagination ceilings, execution deadlines, queue limits, retry/backoff behavior, cost-aware quotas, abuse telemetry and safe error responses.

Avoid simplistic IP-only rate limits that punish users behind shared NAT or can be bypassed through distributed sources. Avoid account lockout designs that let an attacker deny service to a victim. Use 429 and Retry-After where appropriate, but do not reveal sensitive account state.

## 20. WebSockets and server-sent events

### 20.1 WebSocket

Review handshake origin validation, authentication at connection establishment, authorization for every message/action, tenant binding, message schema, payload size, rate limits, idle timeout, connection limits, reauthentication/revocation, subprotocol negotiation, compression behavior, logging and safe close handling.

A successful WebSocket handshake does not authorize every future message. Enforce action-level and resource-level policy within the message handler.

### 20.2 Server-Sent Events (SSE)

Review authorization on the event stream, origin and cookie behavior, cache headers, connection lifetime, tenant and resource scope, event filtering, reconnect behavior, Last-Event-ID validation, token exposure in URLs and revocation. Ensure one user's events cannot be replayed or delivered to another session.

## 21. Redirects, URL handling and open redirect

Validate redirect destinations against an allow-list or map a short internal destination key to a server-controlled URL. Reject protocol-relative, encoded, nested and alternate-scheme destinations unless explicitly intended. Do not assume a URL is safe because it shares a hostname substring. Use safe URL parsing and canonicalization. Protect post-login, logout, payment return and password-reset flows. Test redirects through proxies and identity callbacks.

## 22. Error handling and exceptional conditions

### 22.1 Secure error design

- Return generic client errors that do not expose stack traces, SQL, filesystem paths, secrets or internal topology.
- Preserve detailed diagnostics in access-controlled logs.
- Use stable error codes and correlation IDs.
- Avoid swallowing security-relevant failures and continuing with permissive defaults.
- Ensure authorization, validation and dependency failures fail safely.
- Prevent exception handlers from returning cached sensitive content.
- Avoid exposing framework debug pages in production.
- Keep error behavior consistent enough to reduce account and resource enumeration.
- Do not leak secrets in traces, crash dumps or analytics.

### 22.2 Fail-open versus fail-closed

Define behavior per dependency and operation. For access control, policy, tenant resolution and sensitive authorization, fail closed unless a carefully documented alternative is justified. For non-security-critical telemetry, a bounded asynchronous fallback may be acceptable. Do not let an identity, authorization or security-policy outage silently grant access.

## 23. Third-party scripts and client-side supply chain

Third-party JavaScript executes with significant privileges in the page origin. A compromised vendor script may read DOM data, invoke application actions and access browser-visible tokens.

Controls:
- Maintain an inventory of third-party scripts, owners, purpose and data access.
- Minimize scripts and avoid unnecessary tag managers.
- Pin versions and use Subresource Integrity where suitable for static cross-origin resources.
- Restrict script sources with CSP.
- Review vendor change and incident notification processes.
- Avoid placing sensitive data in the DOM when scripts do not need it.
- Separate high-risk administration from marketing/analytics scripts.
- Monitor unexpected script changes and outbound connections.
- Review privacy and consent requirements.
- Test CSP and SRI update/rotation procedures.

SRI is not a complete solution for dynamic scripts, same-origin resources or a compromised vendor that legitimately updates a trusted resource. The architecture must limit trust and privileges.

## 24. Web application deployment and configuration

### 24.1 Secure deployment baseline

- Remove development tools, debug routes, sample applications and default accounts.
- Disable verbose errors and production source maps unless deliberately protected.
- Restrict administrative interfaces by identity and network policy.
- Apply security patches to runtime, framework, proxy, OS and dependencies.
- Use non-root, least-privileged service identities.
- Separate development, test, staging and production credentials.
- Store secrets in managed secret stores.
- Restrict outbound network access.
- Use immutable or controlled deployment artifacts.
- Verify build provenance and artifact integrity.
- Harden TLS and certificate lifecycle.
- Protect configuration and deployment pipelines.
- Restrict access to logs, backups and snapshots.
- Test rollback and recovery.
- Document security-relevant configuration changes.

### 24.2 Environment separation

Never reuse production secrets in non-production. Use synthetic or masked data. Restrict production data exports. Ensure test accounts cannot authenticate to production unless explicitly authorized. Separate signing keys, OAuth clients, storage buckets, databases and deployment identities by environment.

### 24.3 Reverse proxy and origin protection

- Ensure origin cannot be accessed around the CDN/WAF if the design depends on edge controls.
- Restrict ingress to approved proxy sources.
- Normalize and sanitize headers at trust boundaries.
- Configure request size, timeout and connection limits.
- Prevent direct client control of trusted identity/tenant headers.
- Ensure TLS between proxy and origin when required by threat model.
- Monitor proxy bypass and configuration drift.

## 25. Framework-specific security review

### 25.1 React and browser front ends

Review:
- React rendering and escaping behavior.
- Dangerous HTML APIs and dangerouslySetInnerHTML usage.
- Unsafe URL schemes in href/src/navigation.
- Client-side route guards versus server authorization.
- Token and session storage.
- postMessage origin and schema validation.
- Dependency and build pipeline integrity.
- Source maps and debug artifacts.
- CSP compatibility and nonce handling.
- Service worker scope and cache behavior.
- Third-party scripts and analytics.
- SSR hydration and server/client trust differences.

Principles:
- React's default escaping is useful but not a complete XSS defense.
- Never use dangerouslySetInnerHTML with untrusted content without a reviewed sanitizer.
- Do not rely on client-side route guards to protect APIs or data.
- Validate postMessage origin and message schema.
- Avoid storing long-lived bearer tokens in localStorage.
- Treat build-time environment variables as public if bundled into client assets.

### 25.2 Node.js and Express

Review:
- Express version and middleware order.
- Trust proxy configuration.
- Host validation.
- Session middleware and cookie configuration.
- CSRF protection for cookie-authenticated actions.
- CORS allow-list and credentials behavior.
- Body parser limits and content-type handling.
- Route and method authorization.
- Async error handling and unhandled rejections.
- Template escaping and safe view helpers.
- File upload and static-file path controls.
- SSRF-prone URL fetch features.
- Security headers and CSP.
- Production debug and stack-trace exposure.

Principles:
- Set trust proxy only for known proxy hops.
- Use explicit route-level authorization and service-layer object checks.
- Bound JSON and multipart request sizes.
- Avoid shell execution and unsafe dynamic evaluation.
- Keep secrets out of client bundles and logs.

### 25.3 .NET and ASP.NET Core

Review:
- Middleware ordering and exception handling.
- Forwarded headers and trusted proxies.
- HTTPS redirection and HSTS.
- Authentication scheme and authorization policy.
- Antiforgery for cookie-authenticated browser actions.
- CORS policy and endpoint mapping.
- Data Protection key storage and sharing.
- Static file and upload handling.
- Model binding and over-posting.
- Output encoding and Razor safe/unsafe HTML APIs.
- Path and file provider configuration.
- Kestrel and reverse proxy limits.
- Detailed errors and developer exception page.
- SignalR hub authorization and per-message access.

Principles:
- Use explicit authorization policies and resource handlers.
- Keep antiforgery enabled for relevant browser form flows.
- Avoid returning entity objects directly when property-level control matters.
- Protect Data Protection keys and configure environment-specific key rings.
- Validate tenant and ownership in service/repository logic.

### 25.4 Java and Spring

Review:
- Spring Security filter chain order and request matchers.
- CSRF and CORS configuration.
- Session fixation and cookie settings.
- Method and object-level authorization.
- MVC binding and validation.
- Thymeleaf/JSP output escaping and raw HTML.
- File upload and multipart limits.
- Jackson polymorphic deserialization configuration.
- Error pages and actuator/management endpoints.
- Proxy headers and forwarded host handling.
- WebSocket/STOMP authorization.
- Database query binding and transaction semantics.

Principles:
- Use maintained Spring Security components.
- Apply authorization at service boundaries for sensitive operations.
- Validate DTOs and avoid mass assignment.
- Keep actuator and management endpoints separately protected.
- Avoid unsafe polymorphic deserialization of untrusted content.

### 25.5 Python, Django, Flask and FastAPI

Review:
- Middleware ordering and trusted host configuration.
- CSRF and session cookie settings.
- Template autoescape and safe-marking APIs.
- ORM parameterization and raw SQL.
- Object-level authorization.
- File upload and media serving.
- Debug mode and exception output.
- CORS and proxy configuration.
- Async task identity propagation.
- Request schema and body limits.
- Dependency and package integrity.

Principles:
- Keep Django DEBUG disabled in production and configure ALLOWED_HOSTS.
- Use framework CSRF protections for cookie-authenticated browser actions.
- Do not mark untrusted content safe.
- Use explicit Pydantic or equivalent request schemas.
- Enforce resource authorization in service/query paths, not only route decorators.

Framework defaults change. Verify the actual version, configuration and deployment topology before treating a feature as enabled.

## 26. Security testing methodology

### 26.1 Engagement authorization

Before testing:
- Obtain written authorization from the application and infrastructure owners.
- Confirm exact hostnames, routes, APIs, tenants and environments in scope.
- Define excluded systems, accounts, data and techniques.
- Use dedicated synthetic users for each role.
- Define testing window, rate limits, contact and emergency stop.
- Confirm whether file upload, email, SMS, payment, destructive workflows and third-party integrations are permitted.
- Agree evidence storage and retention.
- Ensure no customer data or unrelated systems are accessed.

### 26.2 Assessment phases

1. Scope and rules of engagement.
2. Architecture and asset understanding.
3. Passive discovery and technology identification.
4. Application mapping and role-based navigation.
5. Authentication and session integration review (detailed identity controls in Chapter 07).
6. Authorization and tenant boundary tests.
7. Input, output and injection tests.
8. Browser and client-side tests.
9. File handling and SSRF tests.
10. Business logic and workflow tests.
11. Configuration, headers and deployment review.
12. Error, rate and availability behavior.
13. Evidence validation and impact assessment.
14. Reporting, remediation guidance and retest.

### 26.3 Manual testing versus automated scanning

Automated tools are useful for repeatable discovery and common patterns. They cannot reliably determine every business rule, ownership relationship, approval boundary, workflow sequence, data sensitivity or real impact.

Use a combination of:
- Browser developer tools for request, response, DOM, storage and console analysis.
- Intercepting proxy for controlled request inspection and replay.
- DAST for broad automated checks.
- SAST for source-level data flow and unsafe API usage.
- SCA for dependency and package risk.
- Secret scanning for exposed credentials.
- Infrastructure/configuration review.
- Manual authorization and business logic tests.
- Targeted fuzzing and protocol tests.
- Code review and remediation verification.

### 26.4 Evidence requirements

Capture:
- Test ID and scope.
- Environment and version.
- Synthetic account and role.
- Preconditions and exact steps.
- Redacted request and response.
- Expected and observed behavior.
- Resource/tenant context.
- Impact and exploitability reasoning.
- Root cause and affected component.
- Sanitized screenshot or log reference.
- Remediation and retest result.

Do not include live credentials, session cookies, bearer tokens, private keys, personal identity documents or customer data in reports.

## 27. Web security test catalogue

| Test ID | Area | Test | Expected result |
|---|---|---|---|
| WEB-T-001 | Host | Send unapproved Host header to test environment | Request rejected or canonical host used; no attacker-controlled absolute links |
| WEB-T-002 | Forwarded headers | Supply spoofed X-Forwarded-Host/Proto from untrusted client | Untrusted values ignored/stripped |
| WEB-T-003 | Methods | Invoke unneeded method on protected route | Rejected; no alternate method bypass |
| WEB-T-004 | Path | Compare encoded and normalized route variants | Same policy and resource interpretation |
| WEB-T-005 | XSS | Submit harmless context-specific test string in authorized lab | Output encoded or sanitized; no script execution |
| WEB-T-006 | DOM XSS | Trace user-controlled source into DOM sink | Safe DOM API or reviewed sanitization |
| WEB-T-007 | CSRF | Cross-site state-changing request in controlled browser | Rejected without valid anti-forgery proof |
| WEB-T-008 | CORS | Request with untrusted Origin | No unauthorized origin reflection or credentialed access |
| WEB-T-009 | CSP | Inspect policy on success, error and static responses | Intended policy consistently present and effective |
| WEB-T-010 | Clickjacking | Attempt to frame sensitive page from untrusted origin | Framing blocked unless explicitly allowed |
| WEB-T-011 | SQLi | Test parameterized search/filter paths using benign lab payloads | Input remains data; no query structure change |
| WEB-T-012 | NoSQL | Submit unexpected operator/object shape to filter endpoint | Schema rejects or safely handles input |
| WEB-T-013 | SSRF | Test allow-listed and disallowed destinations in isolated fetch feature | Only approved destinations reachable |
| WEB-T-014 | Upload | Upload disallowed extension/content mismatch in lab | Rejected or quarantined; not served as active content |
| WEB-T-015 | Download | Change file identifier to another user's file | Denied by object authorization |
| WEB-T-016 | Archive | Upload archive with traversal-like entry in isolated lab | Extraction remains inside dedicated directory or archive rejected |
| WEB-T-017 | Business logic | Repeat one-time operation | Idempotent or rejected per business rule |
| WEB-T-018 | Workflow | Skip required approval step | Server rejects invalid state transition |
| WEB-T-019 | Race | Submit concurrent requests against limited inventory/test resource | Atomic constraints prevent over-allocation |
| WEB-T-020 | Cache | Compare authenticated response across synthetic users | No cross-user or cross-tenant cache disclosure |
| WEB-T-021 | Rate | Exceed configured test quota within approved limits | Bounded response and observable throttling |
| WEB-T-022 | WebSocket | Send unauthorized action after successful handshake | Message-level authorization denies action |
| WEB-T-023 | Redirect | Supply external redirect destination | Untrusted destination rejected or mapped to approved URL |
| WEB-T-024 | Errors | Trigger controlled validation/dependency error | No stack trace, secret or internal detail in client response |
| WEB-T-025 | Source maps | Inspect production static assets | No unintended source disclosure or embedded secrets |
| WEB-T-026 | Third party | Review external script inventory and CSP | Only approved scripts and destinations execute |
| WEB-T-027 | Session | Verify session invalidation after logout | Replayed session is rejected |
| WEB-T-028 | Tenant | Change tenant/resource identifier in request | Server enforces trusted tenant membership and object policy |
| WEB-T-029 | Static files | Request backup, config, repository or debug artifacts | Sensitive artifacts not exposed |
| WEB-T-030 | TLS | Review certificate, protocol and redirect behavior | Approved TLS policy and HTTPS-only access |
| WEB-T-031 | Error handling | Cause dependency timeout or malformed upstream response | Safe bounded failure; no permissive authorization fallback |
| WEB-T-032 | Service worker | Verify logout and deployment cache behavior | Sensitive cache cleared/controlled; stale worker cannot bypass policy |

## 28. Finding classification and remediation

### 28.1 Finding record

Each finding should contain:
- Unique finding ID.
- Title and affected asset.
- Severity and priority with rationale.
- CWE or relevant weakness category where supportable.
- OWASP Top 10 / ASVS / WSTG mapping with exact edition.
- Preconditions and attack path.
- Reproduction steps.
- Evidence and sanitized request/response.
- Security impact and business context.
- Root cause.
- Remediation options.
- Compensating controls and residual risk.
- Owner, due date and status.
- Retest steps and closure evidence.

### 28.2 Severity

Use a documented risk method. Consider attack complexity, required privilege, user interaction, confidentiality/integrity/availability impact, tenant scope, affected population, business criticality, exploitability, exposure and compensating controls.

Do not assign severity solely from a scanner label. A missing header is not automatically High; an authorization flaw exposing restricted financial or personal data may be Critical depending on impact and scope.

### 28.3 Remediation lifecycle

1. Validate finding and eliminate false positives.
2. Identify root cause and affected paths.
3. Agree owner and risk-based target date.
4. Design fix and regression coverage.
5. Review code/configuration.
6. Deploy through change control.
7. Retest original reproduction and adjacent variants.
8. Validate no regression in legitimate behavior.
9. Close with evidence or record explicit risk acceptance.
10. Trend recurring root causes and feed lessons into secure SDLC.

## 29. Detection and operational monitoring

### 29.1 High-value telemetry

Log security-relevant events including authentication and authorization outcomes, suspicious request patterns, validation failures, upload and download actions, sensitive exports, role and tenant changes, admin operations, rate-limit events, WAF actions, SSRF policy denials, CSP reports, application exceptions, dependency failures, configuration changes and deployment events.

Use correlation IDs across edge, proxy, application, identity and downstream services. Record actor, action, resource, tenant, outcome, policy context and timestamp where appropriate. Avoid logging secrets, full session tokens, passwords, sensitive query strings or unnecessary personal data.

### 29.2 Detection scenarios

| Detection ID | Scenario | Signal | Response |
|---|---|---|---|
| WEB-D-001 | Repeated authorization denials | One identity probes many object IDs or tenants | Review account and access path |
| WEB-D-002 | Suspicious upload pattern | Repeated type mismatch, archive expansion or scanner detections | Quarantine and investigate |
| WEB-D-003 | SSRF policy violations | Requests to blocked internal/metadata destinations | Block and inspect feature abuse |
| WEB-D-004 | Web exploitation pattern | Repeated malformed requests, injection signatures and unusual errors | Correlate WAF and application events |
| WEB-D-005 | Sensitive export anomaly | Unusual volume, tenant scope or time | Verify user intent and authorization |
| WEB-D-006 | Rate-limit abuse | Sustained high request/concurrency or costly endpoint use | Throttle and investigate automation |
| WEB-D-007 | CSP violation surge | Unexpected script or connection destination | Investigate injection or deployment change |
| WEB-D-008 | Cache isolation anomaly | Same cache key serves distinct principal/tenant response | Purge cache and investigate leakage |
| WEB-D-009 | Admin workflow abuse | Unexpected role, approval or configuration change | Restrict account and preserve evidence |
| WEB-D-010 | Dependency failure abuse | Repeated upstream timeouts or parser failures | Inspect resource exhaustion and fail-safe behavior |

Tune thresholds to baseline. A WAF signature alone is not proof of compromise; correlate with application outcomes and resource access.

## 30. Incident response for web application compromise

1. Identify affected application, route, tenant and deployment version.
2. Preserve edge, proxy, application, identity and infrastructure evidence.
3. Determine whether the event involves account takeover, injection, authorization bypass, file processing, dependency compromise or data exposure.
4. Contain the affected feature or route without unnecessarily disabling unrelated critical services.
5. Revoke sessions, tokens, API keys or integration credentials when exposure warrants it.
6. Block malicious egress or destinations if SSRF or command execution is suspected.
7. Quarantine uploaded content and isolate affected processing workers.
8. Determine accessed records, exports and tenant scope.
9. Inspect persistence, changed accounts, web shells, modified static assets and CI/CD artifacts.
10. Restore from trusted artifacts and rotate compromised secrets.
11. Validate the root cause and adjacent attack paths.
12. Notify stakeholders and regulators through the approved legal/incident process where required.
13. Complete post-incident review, remediation and regression tests.

Do not destroy evidence by immediately rebuilding every host before logs, snapshots and relevant artifacts are preserved.

## 31. Practical architecture scenarios

### 31.1 Multi-tenant learning management system

**Classification:** Composite scenario.

A browser-based LMS has React front end, .NET API, MySQL database, Azure hosting, course catalogue, cyber labs, documents, assessment engine and administrative roles.

Threats include learner-to-learner record access, tenant leakage, role manipulation, assessment answer disclosure, repeated submissions, unsafe file upload, stored XSS in course content, insecure lab links, IDOR in reports and cross-tenant exports.

Required controls:
- Server-side role, object, property and tenant authorization.
- Separate platform and tenant administration.
- Assessment state and submission integrity enforced transactionally.
- Correctly scoped short-lived lab access credentials.
- File storage outside executable web origin.
- Content sanitization for user-authored descriptions and comments.
- Audit events for role, course, assessment and export operations.
- Negative tests across learner, trainer, analyst, admin and tenant boundaries.

### 31.2 Enterprise customer portal

**Classification:** Composite scenario.

A customer portal supports profile changes, invoices, service requests and document downloads. Key risks are IDOR, account recovery abuse, sensitive cache leakage, workflow bypass, unsafe PDF preview and third-party script compromise. Apply object authorization, secure document delivery, session and recovery controls, anti-CSRF, cache isolation, rate controls and auditable approval workflows.

### 31.3 Remote industrial support portal

**Classification:** Composite scenario.

An industrial operator uses a web portal to request support sessions for HMI/SCADA-related assets. The portal is not itself a control-system authorization boundary. It must verify named user identity, asset scope, sponsor approval, time-bound access, jump-host policy and audit. OT network segmentation and safety/change-control remain separate required controls. Do not expose control networks directly to the public web application.

### 31.4 Financial approval workflow

**Classification:** Composite scenario.

A web application supports payment/refund approval. The design must enforce transaction limits, separation of duties, idempotency, atomic state changes, strong step-up for sensitive actions, audit integrity and independent approval. Client-side amount values and disabled buttons are not trusted.

## 32. Standards and framework mapping

### 32.1 OWASP Top 10:2025

The current OWASP Top 10 release is 2025. It is an awareness document, not a complete test specification. The categories are:
- A01:2025 Broken Access Control.
- A02:2025 Security Misconfiguration.
- A03:2025 Software Supply Chain Failures.
- A04:2025 Cryptographic Failures.
- A05:2025 Injection.
- A06:2025 Insecure Design.
- A07:2025 Authentication Failures.
- A08:2025 Software or Data Integrity Failures.
- A09:2025 Security Logging and Alerting Failures.
- A10:2025 Mishandling of Exceptional Conditions.

Map each risk to the actual application threat model and verification cases. Do not infer that an application is secure because it has no obvious Top 10 finding.

### 32.2 OWASP ASVS 5.0.0

ASVS 5.0.0 is the stable release published 30 May 2025. Use it as a requirements and verification baseline. Select the verification level according to application risk and assurance need. Record exact requirement identifiers and version in assessment plans and contracts. Do not invent requirement IDs or copy identifiers from older ASVS versions without verifying the 5.0.0 catalogue.

### 32.3 OWASP Web Security Testing Guide

The WSTG v4.2 is the latest stable version identified in the OWASP project pages reviewed for this baseline; version 5.0 is in development. Use versioned WSTG references in reports. WSTG is a testing methodology and technique guide, not a compliance standard. Adapt test depth to application risk and authorization.

### 32.4 ISO/IEC 27001:2022 and 27002:2022 relationship

| Annex A control | Theme | Web application contribution |
|---|---|---|
| 5.8 | Information security in project management | Security requirements and gates in web delivery |
| 5.15 | Access control | Application and resource authorization |
| 5.16 | Identity management | User and service identity integration |
| 5.17 | Authentication information | Credential and secret protection |
| 5.18 | Access rights | Grant, review and removal |
| 8.5 | Secure authentication | Secure login and session integration |
| 8.8 | Management of technical vulnerabilities | Framework, runtime and dependency remediation |
| 8.9 | Configuration management | Secure baseline and drift control |
| 8.20 | Network security | Edge, proxy, origin and egress boundaries |
| 8.21 | Security of network services | Securely configured hosting and web services |
| 8.25 | Secure development life cycle | Web security throughout SDLC |
| 8.26 | Application security requirements | Security requirements and acceptance criteria |
| 8.28 | Secure coding | Safe input, output, query and file handling |
| 8.29 | Security testing in development and acceptance | DAST, SAST, manual verification and retest |
| 8.32 | Change management | Controlled security configuration and deployment |

This is a relevance map, not a statement of implementation or certification.

### 32.5 Regulatory and sector context

Web controls may support obligations under privacy, cybersecurity, financial, payment, critical infrastructure and product-security regimes. Applicability depends on jurisdiction, entity, processing activity, sector, contractual role and effective dates. Use the repository's Global Regulatory Register and confirm the current official instrument before making a compliance claim.

## 33. Limitations and unresolved work

- Exact ASVS 5.0.0 requirement-to-test IDs must be imported from the official release and reviewed before publication as a complete crosswalk.
- WSTG test references should be added per test case using versioned v4.2 IDs; the current WSTG 5.0 development branch must not be treated as stable.
- Framework examples are engineering review guidance, not version-pinned implementation recipes.
- HTTP request smuggling testing is highly proxy/version dependent and requires dedicated isolated test infrastructure.
- Browser behavior differs across engines and versions; compatibility testing is required.
- CSP and third-party script policies require application-specific rollout and monitoring.
- Regulatory applicability and control mapping require entity-specific legal and compliance review.
- Composite scenarios are illustrative, not claims about a real organization or incident.
- This playbook does not replace Chapter 06 API security or Chapter 07 identity engineering.

## 34. Related chapters

- [01. AppSec Fundamentals](../01-fundamentals/APPSEC-FUNDAMENTALS.md)
- [02. Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [03. Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [04. Secure Coding and Code Review](../04-secure-coding/SECURE-CODING-AND-CODE-REVIEW.md)
- [05. Web Application Security Lab Pack](WEB-APPLICATION-SECURITY-LAB-PACK.md)
- [07. Identity and Access Security](../07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY.md)
- [18. Standards Baseline and Mapping Method](../18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md)
- [19. Global Regulatory Register](../19-global-regulatory/GLOBAL-REGULATORY-REGISTER.md)

## 35. References

1. OWASP Top 10:2025: https://owasp.org/Top10/2025/
2. OWASP ASVS 5.0.0: https://asvs.owasp.org/
3. OWASP ASVS downloads and release data: https://asvs.owasp.org/downloads/
4. OWASP Web Security Testing Guide v4.2 and project status: https://owasp.org/www-project-web-security-testing-guide/
5. OWASP WSTG stable guide: https://wstg.owasp.org/
6. OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
7. OWASP Dependency-Check: https://owasp.org/www-project-dependency-check/
8. MDN Web Security: https://developer.mozilla.org/en-US/docs/Web/Security
9. IETF HTTP Semantics, RFC 9110: https://www.rfc-editor.org/rfc/rfc9110.html
10. IETF HTTP/1.1, RFC 9112: https://www.rfc-editor.org/rfc/rfc9112.html
11. IETF HTTP/2, RFC 9113: https://www.rfc-editor.org/rfc/rfc9113.html
12. IETF HTTP/3, RFC 9114: https://www.rfc-editor.org/rfc/rfc9114.html
13. IETF Content Security Policy Level 3: https://www.w3.org/TR/CSP3/
14. W3C Fetch Standard: https://fetch.spec.whatwg.org/
15. NIST SP 800-218 Secure Software Development Framework: https://csrc.nist.gov/pubs/sp/800/218/final
16. ISO/IEC 27001 and 27002 official catalogue: https://www.iso.org/standards.html

## 36. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial web application security engineering playbook |
