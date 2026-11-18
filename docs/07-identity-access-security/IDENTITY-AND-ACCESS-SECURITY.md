# Identity and Access Security Engineering Playbook

| Field | Value |
|---|---|
| Document ID | UAPPSEC-07-001 |
| Status | Draft baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Human, workload, machine, application, privileged and agent identity across applications and services |
| Technologies | Web, API, cloud, Java/Spring, .NET, Node.js/TypeScript, Python, enterprise identity providers |
| Classification | Public |

## 1. Executive summary

Identity and access security establishes which subject is acting, how the system establishes confidence in that identity, what the subject is permitted to do, which resource and context the decision applies to, and how the organization creates, changes, monitors and removes that authority.

Identity security is broader than a login page. It includes identity proofing, registration, enrollment, authentication, authenticator lifecycle, federation, session continuity, resource and business-action authorization, human and non-human identities, privileged access, provisioning, deprovisioning, credential lifecycle, monitoring, investigation and recovery.

The fundamental rule is:

**A successful authentication establishes evidence about a subject. It does not, by itself, authorize that subject to access a particular object or perform a particular action.**

The enforcement decision must be made for the actual subject, action, resource and relevant context. It must remain correct across APIs, background workers, exports, administrative interfaces, integrations, caches and alternate execution paths.

The current NIST SP 800-63-4 suite was published in July 2025 and supersedes SP 800-63-3. RFC 9700 is the OAuth 2.0 Security Best Current Practice published in January 2025. These sources have different purposes and are not interchangeable. NIST 800-63 is written for digital identity services and federal information systems; it is a strong engineering reference but does not automatically impose a legal requirement on every private application.

## 2. Purpose, audience and applicability

### 2.1 Purpose

Provide an engineering reference to design, implement, integrate, assess and operate identity and access controls. Support architecture reviews, secure development, IAM programme design, application assessments, federation projects, access governance, incident response and audit evidence.

### 2.2 Audience

Application developers, IAM engineers, security architects, AppSec and product security engineers, cloud/platform engineers, DevSecOps teams, SOC analysts, identity governance teams, privileged access administrators, auditors and technical leaders.

### 2.3 Scope

In scope:
- Customer, employee, contractor, partner and administrator identities.
- Workload, service, machine, device and application identities.
- AI agents and automated identities acting through tools or APIs.
- Identity proofing and enrollment.
- Password, MFA, passkey, certificate and cryptographic authenticator use.
- OAuth 2.0, OpenID Connect (OIDC), Security Assertion Markup Language (SAML), JSON Web Tokens (JWT), SCIM and token-binding patterns.
- Authentication, authorization, sessions, federation, provisioning and deprovisioning.
- Role-based, attribute-based, relationship-based and policy-based access control.
- Privileged access, just-in-time access, break-glass and segregation of duties.
- Identity monitoring, threat detection, response and assurance.

Full application security, API protocol security, cryptographic engineering, endpoint hardening, cloud control-plane security and privacy law have separate coverage; their identity-related interfaces are included here.

### 2.4 Assumptions and limits

- The application has an identified owner and documented business purpose.
- Identity and access requirements derive from data classification, business risk, legal/contractual context and threat model.
- The organization can identify authoritative identity sources and owners.
- Exact product configuration depends on identity provider, protocol profile, application architecture and version.
- This document is not legal advice, an audit result or certification statement.
- Example code and patterns are illustrative. Confirm current framework APIs, library behavior and secure defaults before production use.

## 3. Core concepts and terminology

| Term | Meaning | Security significance |
|---|---|---|
| Subject / principal | Human or non-human entity requesting an action | Entity to which policy decisions are attributed |
| Digital identity | Representation of a subject within a defined service or trust domain | Not necessarily proof of a real-world civil identity |
| Identity proofing | Process establishing confidence in an applicant's claimed identity | Binds a digital account to a real-world or organizational identity |
| Enrollment | Registration of an identity and its authenticators | Establishes credentials and lifecycle records |
| Authenticator | Something used to prove control of an account | Must be bound, protected, monitored and recoverable |
| Authentication (AuthN) | Process verifying a claimant's control of one or more authenticators | Establishes confidence in a claimed identity |
| Authorization (AuthZ) | Decision whether a subject may perform an action on a resource | Controls access after identity is established |
| Entitlement | Specific permission or access right assigned to a subject or group | Requires owner, scope, purpose and lifecycle |
| Role | Named collection of permissions or responsibilities | Useful abstraction but can create role explosion or excessive privilege |
| Attribute | Property of a subject, resource or environment | Enables contextual and policy-driven decisions |
| Relationship | Defined link between subjects and resources | Enables ownership, membership, delegation and sharing policies |
| Federation | Trust relationship where one domain accepts identity assertions from another | Introduces issuer, audience, key, claim-mapping and replay risks |
| Identity Provider (IdP) | System that authenticates subjects and/or issues identity assertions | Compromise can affect many relying applications |
| Relying Party (RP) | Application that consumes an identity assertion | Must validate issuer, audience, signature, state and transaction binding |
| Authorization Server (AS) | OAuth component issuing tokens and managing authorization | Controls token issuance and client/grant policy |
| Resource Server (RS) | API or service accepting access tokens and enforcing access policy | Must validate token and authorize requested resource/action |
| Access token | Credential presented to a resource server | Usually bearer unless sender-constrained; scope and audience matter |
| ID token | OIDC assertion about an authentication event and subject for a client | Intended for OIDC client, not as API access token |
| Refresh token | Credential used to obtain new access tokens | High-value long-lived credential requiring rotation/reuse controls |
| Session | Server-recognized continuity of an authenticated interaction | Requires secure creation, storage, renewal, expiry and revocation |
| Workload identity | Identity assigned to a running workload or software component | Replaces static shared credentials where possible |
| Privileged identity | Identity with elevated or high-impact permissions | Requires stronger controls, monitoring and lifecycle governance |
| JIT access | Just-in-time grant of time-limited privilege | Reduces standing privilege when correctly implemented |
| PEP | Policy Enforcement Point | Enforces permit/deny at access boundary |
| PDP | Policy Decision Point | Evaluates applicable policy and context |
| PIP | Policy Information Point | Supplies trusted attributes and relationship data |
| PAP | Policy Administration Point | Defines and manages policy |
| Authentication assurance | Confidence in authentication process and authenticator properties | Must be selected based on risk and intended use |
| Identity assurance | Confidence in proofing and binding a real-world identity | Distinct from authentication strength |

Do not use authentication, authorization, identity proofing and account enrollment as synonyms.

## 4. Identity security architecture

### 4.1 Logical reference architecture

~~~mermaid
flowchart LR
    H[Human / Admin / Partner] --> C[Client or Browser]
    W[Workload / Service / Agent] --> API[Service Client]
    C --> RP[Relying Application]
    API --> AS[Authorization Server / IdP]
    RP --> AS
    AS --> ID[Identity Proofing and Lifecycle]
    AS --> TOK[Token / Assertion Issuance]
    TOK --> RP
    TOK --> RS[API / Resource Server]
    RP --> PEP[Policy Enforcement Point]
    RS --> PEP
    PEP --> PDP[Policy Decision Point]
    PDP --> PIP[Trusted Attributes / Relationship Data]
    PAP[Policy Administration] --> PDP
    ID --> GOV[IGA / Provisioning / Access Reviews]
    GOV --> APP[Applications and Directories]
    PEP --> AUD[Identity and Access Audit]
    AS --> AUD
    GOV --> AUD
    AUD --> DET[Detection / Response]
~~~

This is a logical model, not a mandatory product topology. In a small application, several functions may be implemented by one platform. In a large enterprise, they may be distributed across an IdP, identity governance and administration (IGA), privileged access management (PAM), policy engine, API gateway, application services, directories and security monitoring.

### 4.2 Trust boundaries

Identify explicitly:
- User device to application.
- Application to identity provider.
- Browser to authorization endpoint and callback.
- Application to token endpoint.
- Client to resource server.
- Service-to-service trust.
- Enterprise identity domain to partner/federation domain.
- Tenant to tenant.
- Standard user to privileged administration.
- Human operator to automation/agent.
- Production to non-production.
- Control plane to workload plane.
- Identity platform to logs, backups and key management.

Every boundary needs an explicit trust assumption, credential type, validation step, authorization decision, failure behavior and audit trail.

### 4.3 Identity decision sequence

~~~mermaid
sequenceDiagram
    participant S as Subject
    participant C as Client
    participant I as Identity Provider
    participant A as Application
    participant P as Policy Engine
    participant R as Resource
    S->>C: Start protected action
    C->>I: Authenticate or obtain assertion
    I->>I: Validate authenticator and risk
    I-->>C: Assertion / token / session result
    C->>A: Request with session or token
    A->>A: Validate session or token
    A->>P: Subject + action + resource + context
    P->>P: Evaluate policy and trusted attributes
    P-->>A: Permit / deny / step-up
    A->>R: Execute only if permitted
    A->>A: Record outcome and audit event
~~~

Authentication and authorization can occur at different points and may be repeated. Token validation is not a substitute for a resource-specific policy decision.

## 5. Identity inventory and lifecycle governance

### 5.1 Identity categories

| Identity category | Examples | Main risks | Minimum governance |
|---|---|---|---|
| Workforce | Employee, contractor, temporary staff | Orphaned accounts, excessive access, phishing | HR source, manager, owner, joiner/mover/leaver process |
| Customer | Consumer, business customer | Account takeover, recovery abuse, privacy leakage | Verified contact channels, recovery controls, privacy safeguards |
| Partner / supplier | Vendor support, outsourced engineer | Federation trust, dormant access, scope creep | Contract owner, sponsor, expiration, federation review |
| Administrator | Tenant admin, platform admin, security admin | High-impact compromise, privilege escalation | Strong authentication, PAM/JIT, separate admin identity, audit |
| Service account | Scheduled job, legacy application | Static password, broad permissions, unknown owner | Named owner, purpose, vaulting, rotation, scope, expiry |
| Workload identity | Kubernetes workload, cloud function, VM | Token theft, metadata exposure, over-broad role | Platform-issued identity, short-lived credentials, workload binding |
| Device identity | Managed laptop, phone, gateway | Stolen device, cloned certificate, stale compliance | Enrollment, key protection, device posture and revocation |
| Machine / OT identity | PLC engineering station, HMI service, gateway | Shared credentials, unsafe rotation, availability impact | Asset owner, change control, compensating controls, maintenance window |
| AI agent identity | Agent calling approved tools/APIs | Confused deputy, prompt-driven privilege misuse, delegated token overreach | Distinct identity, scoped delegated authority, action approvals and traceability |

An identity must have a unique, stable internal identifier even if username, email address or display name changes. Do not use mutable email addresses as the sole permanent subject key.

### 5.2 Canonical identity record

A canonical identity record should include, where appropriate:
- Immutable identity ID.
- Identity category and authoritative source.
- Account status and lifecycle state.
- Owner, sponsor or manager.
- Organization, tenant and department.
- Employment/contract relationship and end date.
- Assigned roles and entitlements.
- Authentication methods and enrollment status.
- Privileged access status.
- Last authentication and last meaningful use.
- Creation, modification, approval and disable timestamps.
- Risk flags and review status.
- Linked service, device or workload identifiers.
- Retention and deletion policy.

Avoid collecting identity attributes without a defined purpose. Personal data must be minimized and protected.

### 5.3 Joiner, mover, leaver (JML)

**Joiner**
1. Receive an authoritative approved identity event.
2. Validate identity source, employment/contract status and sponsor.
3. Create a unique identity record.
4. Enroll authenticators using an approved proofing and verification process.
5. Assign baseline access through approved role/policy mapping.
6. Require separate approval for privileged access.
7. Notify the identity owner and record evidence.

**Mover**
1. Receive approved role, team, tenant or responsibility change.
2. Re-evaluate all existing entitlements.
3. Remove permissions no longer required before or alongside new grants, based on risk and transaction design.
4. Apply segregation-of-duties checks.
5. Re-evaluate delegated and group-derived permissions.
6. Revoke or refresh sessions/tokens if authority changes require it.
7. Record approval, effective time and completed changes.

**Leaver**
1. Receive authoritative termination or contract-end event.
2. Disable interactive authentication within the defined risk-based service level.
3. Revoke sessions, refresh tokens, API credentials, certificates and active federation grants as applicable.
4. Remove group membership and application entitlements.
5. Transfer ownership of scheduled jobs, files, secrets and business processes.
6. Preserve required audit records and evidence.
7. Delete or anonymize personal data according to retention policy and legal hold.
8. Confirm completion across connected systems and exceptions.

Deprovisioning must include non-human identities and credentials created by the person. Disabling the directory account alone may not revoke independent API keys, local application accounts, cloud keys or cached tokens.

### 5.4 Access review and recertification

Review frequency should be based on privilege, data sensitivity, threat exposure, regulatory/contractual requirements and change rate. A review must ask whether access remains required, appropriate, approved and used.

Review high-risk access more frequently, including privileged and emergency access, production database and cloud administration, financial approval, sensitive customer data, security tooling and audit log administration, external partner access, dormant/orphaned/non-human accounts and broad service principals.

A meaningful review includes entitlement list, business owner, reviewer, evidence of decision, removals, exceptions, expiry and follow-up validation. Bulk approve-all is not a control unless the reviewer receives sufficient context and the approval is attributable.

## 6. Identity proofing, registration and enrollment

### 6.1 Distinguish proofing from authentication

Identity proofing establishes confidence that an applicant is the person or organization they claim to be. Authentication later establishes that a claimant controls an authenticator bound to an enrolled identity.

A login challenge cannot repair weak account enrollment. Strong identity proofing does not prevent credential theft after enrollment.

### 6.2 Risk-based proofing

Select proofing strength based on consequence of impersonation, value and sensitivity of accessible resources, financial or safety impact, legal identity requirements, fraud prevalence, threat model and availability of authoritative records.

Do not collect government identity documents or biometrics by default. Define purpose, lawful basis where applicable, retention, access, vendor processing, deletion and alternatives. Identity proofing providers create supply-chain and privacy dependencies.

### 6.3 Enrollment controls

- Bind authenticators only after appropriate identity verification.
- Verify control of destination email or phone where used.
- Prevent unauthenticated account pre-claiming and identity collision.
- Protect invitation and enrollment tokens as short-lived, single-use secrets.
- Prevent users from enrolling an authenticator for another identity.
- Notify users of new authenticator enrollment and recovery changes.
- Require stronger verification for high-impact enrollment and reset events.
- Provide a secure recovery path that is not weaker than the primary authentication path.

## 7. Authentication engineering

### 7.1 Authentication factors

| Factor | Example | Strength considerations | Common failure |
|---|---|---|---|
| Knowledge | Password, PIN | Guessability, reuse, phishing, storage and reset design | Credential stuffing, brute force, phishing |
| Possession | Hardware key, authenticator app, device-bound key | Secure key storage, enrollment, device loss, protocol binding | OTP relay, SIM swap, stolen device |
| Inherence | Biometric unlock | Sensor, liveness, local matching, privacy and fallback | Spoofing, coercion, weak fallback, biometric exposure |
| Cryptographic possession | Passkey, smart card, client certificate | Private-key protection, relying-party binding, revocation/recovery | Key loss, enrollment abuse, device compromise |

The traditional factor categories are useful, but authentication assurance depends on actual protocol, authenticator properties, verifier behavior, phishing resistance, recovery and deployment context. Two values from the same category do not automatically form multifactor authentication.

### 7.2 Password policy

- Store passwords using a dedicated, maintained password-hashing scheme, not encryption or plaintext.
- Use unique salts managed by the password-hashing library.
- Select work factors by current authoritative guidance and performance testing.
- Block known compromised/common passwords where feasible.
- Avoid arbitrary composition rules that encourage predictable substitutions.
- Apply appropriate minimum length and permit password managers and paste.
- Avoid forced periodic password changes without evidence of compromise or another justified trigger.
- Rate-limit authentication attempts with controls that resist distributed attacks without enabling easy account denial of service.
- Use generic login failure messages while preserving useful internal telemetry.
- Protect password reset as a high-risk identity operation.
- Never log passwords or reset secrets.

NIST SP 800-63B-4 is the current NIST authentication and authenticator-management volume. Consult it directly for password length, blocklists, rate limiting, authenticator lifecycle and assurance-level decisions. Do not copy obsolete SP 800-63B-3 guidance as if it were current.

### 7.3 Multi-factor authentication

MFA combines independent factors or an appropriately defined cryptographic authentication method. The design must consider authenticator, protocol, enrollment, recovery and downgrade paths.

- Prioritize phishing-resistant methods for administrators and high-impact actions.
- Prefer WebAuthn/FIDO2 security keys or passkeys where supported and appropriate.
- Use authenticator-app TOTP as a risk-based option where phishing-resistant authentication is unavailable; recognize that codes can be phished or relayed.
- Treat SMS and voice OTP as weaker, higher-risk fallback methods due to SIM swap, number porting and interception risks.
- Do not allow an attacker to remove or replace MFA using only a password.
- Notify users of enrollment, removal, recovery and factor reset.
- Require reauthentication or step-up for sensitive changes.
- Rate-limit verification attempts and protect against push fatigue.
- Provide secure recovery with equivalent risk controls and audit.

MFA does not mean phishing resistance. A one-time code can still be relayed to a phishing proxy.

### 7.4 Passkeys and WebAuthn

WebAuthn uses public-key credentials scoped to a relying party. The authenticator retains the private key; the service stores corresponding public-key credential data. The browser mediates the interaction and the relying party validates the challenge response.

Security properties:
- Relying-party scoping helps prevent credential use on an impostor origin.
- The private key is not sent to the service during authentication.
- User verification can be performed by the authenticator.
- Credentials can be device-bound or synchronized depending on ecosystem and configuration.
- Attestation may provide authenticator provenance in some deployments, but introduces privacy, trust and operational considerations.

Implementation requirements:
1. Use a maintained WebAuthn server library.
2. Generate a high-entropy, single-use, short-lived challenge.
3. Bind the challenge to the user, transaction and session.
4. Validate challenge, origin, RP ID hash, signature, credential ownership and required user-verification flags.
5. Validate authenticator data and extension outputs according to selected policy.
6. Store credential ID, public key, user handle, sign counter where meaningful, transports and lifecycle state.
7. Protect credential registration with an authenticated and sufficiently assured session.
8. Notify the user and support revocation of lost credentials.
9. Avoid overly broad attestation collection; define privacy and trust requirements.
10. Test origin, RP ID, challenge replay, account binding, registration abuse and recovery.

A passkey does not eliminate account recovery risk. Attackers often target enrollment, recovery, device takeover and support processes rather than cryptographic verification itself.

### 7.5 Risk-based and step-up authentication

Risk signals can include new device, unusual location, impossible travel, unfamiliar network, anomalous behavior, high-risk action, compromised credential signal, session age, device posture and recent recovery.

Use signals carefully:
- Do not assume IP geolocation proves identity.
- Avoid discriminatory or opaque decisions without governance.
- Keep signals proportionate and privacy-aware.
- Define which actions require step-up and which risks cause denial.
- Ensure the step-up method is meaningfully stronger than current session.
- Avoid silently lowering assurance when a preferred factor is unavailable.
- Record reason and policy decision.

## 8. Authentication protocol and federation security

### 8.1 OAuth 2.0 and OpenID Connect: distinct purposes

OAuth 2.0 is an authorization framework that allows a client to obtain limited access to a protected resource. OAuth alone is not an authentication protocol.

OpenID Connect adds an identity layer on top of OAuth 2.0. It allows a client to verify an end-user's identity using an ID Token and claims from an OpenID Provider.

Do not:
- Treat an OAuth access token as proof of user authentication unless the token profile and trust model explicitly support that use.
- Send an ID Token to an API as though it were an access token.
- Accept a token solely because it is syntactically a JWT.
- Trust claims without validating issuer, signature, audience and relevant time/transaction values.

### 8.2 OAuth roles

| Role | Responsibility | Security responsibility |
|---|---|---|
| Resource owner | Entity able to authorize access to protected resources | Consent and authority according to application model |
| Client | Application requesting access | Secure redirect, PKCE, client authentication where applicable, token storage and least privilege |
| Authorization server | Issues tokens and handles grants | Authenticate/authorize, validate client and grant, issue appropriately scoped tokens |
| Resource server | Hosts protected resources | Validate token and enforce resource/action authorization |

### 8.3 Recommended authorization-code flow with PKCE

~~~mermaid
sequenceDiagram
    participant U as User
    participant C as Client
    participant AS as Authorization Server
    participant RS as Resource Server
    C->>C: Create state, nonce and PKCE verifier
    C->>AS: Authorization request + challenge + state
    AS->>U: Authenticate and obtain consent if needed
    U-->>AS: Authentication result
    AS-->>C: Authorization code + state
    C->>C: Validate returned state
    C->>AS: Code + PKCE verifier at token endpoint
    AS->>AS: Validate code, client and PKCE
    AS-->>C: Access token and, for OIDC, ID token
    C->>RS: API request with access token
    RS->>RS: Validate token and authorize resource/action
~~~

The diagram is simplified. Production deployments must implement the protocol's exact validation, error handling and browser/session protections.

### 8.4 OAuth implementation requirements

Use RFC 9700 (OAuth 2.0 Security Best Current Practice, January 2025) as the security baseline. Key design points:
- Use Authorization Code grant with PKCE for interactive authorization flows.
- Use exact redirect URI matching; do not permit arbitrary wildcard redirect destinations.
- Use transaction-specific, unpredictable state and bind it to the initiating browser/client transaction.
- Use OIDC nonce where applicable and validate it in the ID Token.
- Do not use the Resource Owner Password Credentials grant.
- Do not use the Implicit grant for new designs.
- Protect authorization responses against code injection and mix-up attacks.
- Validate issuer identification and authorization-server identity where multiple issuers are involved.
- Protect token endpoint client authentication according to client type.
- Keep scopes and resource/audience targeting minimal.
- Do not place access tokens in URLs or browser history.
- Protect refresh tokens with rotation/reuse detection or sender-constraining as appropriate.
- Keep tokens out of logs, analytics, referrers and crash reports.
- Apply sender-constrained tokens such as DPoP or mutual TLS where threat model and platform support justify them.
- Apply short lifetimes and revocation/continuous evaluation where architecture requires it.

A public client cannot safely keep a static client secret. A secret embedded in browser or mobile application code is extractable and must not be treated as confidential client authentication.

### 8.5 OIDC ID Token validation

A relying party must validate according to the OIDC profile and its chosen library:
- Signature using keys obtained from a trusted issuer configuration.
- Allowed signing algorithm policy; reject unexpected or disallowed algorithms.
- Exact issuer (iss) match to the configured trusted issuer.
- Audience (aud) includes the client ID; validate authorized party (azp) where required.
- Expiration (exp) and issued-at (iat) according to policy.
- Nonce binding when a nonce was sent.
- State and authorization response correlation in the client transaction.
- auth_time, acr and amr only when the application has a defined policy for them.
- Key rotation and JWKS refresh without accepting attacker-supplied key URLs.

Do not dynamically trust arbitrary jku, x5u or key material from a token header. Use issuer metadata and a trusted key-distribution process.

### 8.6 SAML 2.0 federation

SAML is widely used for enterprise browser-based single sign-on. Its security depends on correctly validating signed XML assertions and protocol messages, metadata, audience, recipient, destination, time conditions, request correlation and subject confirmation.

Review:
- Trusted IdP metadata and signing certificates.
- Metadata provenance, refresh, expiry and key rollover.
- Signature validation over the correct XML element and reference.
- XML signature-wrapping defenses and parser hardening.
- Issuer and audience restrictions.
- Recipient and destination validation.
- InResponseTo correlation for solicited responses.
- NotBefore and NotOnOrAfter conditions with carefully bounded clock skew.
- Assertion replay prevention and unique IDs.
- Subject confirmation method and recipient.
- RelayState integrity and open-redirect protection.
- Attribute/role mapping and default-deny behavior.
- Logout semantics and session invalidation.
- Safe handling of unsolicited IdP-initiated responses if supported.

Do not build SAML XML signature verification manually. Use a maintained, security-reviewed library and test the exact deployed profile.

### 8.7 Federation trust governance

Maintain business and technical owners, issuer/entity ID and expected endpoints, metadata source and verification method, signing/encryption certificate inventory and expiry, claim/attribute mapping, accepted authentication context and assurance, audience and recipient restrictions, provisioning/deprovisioning relationship, incident contact and emergency disable method, renewal, key rollover and annual review evidence.

Never accept an IdP solely because a user supplied a metadata URL or issuer string.

## 9. Tokens, JWT and credential handling

### 9.1 Token types are not interchangeable

| Artifact | Intended use | Common misuse |
|---|---|---|
| OIDC ID Token | Communicate authentication/identity claims to OIDC client | Used as API bearer credential |
| OAuth access token | Authorize access to a resource server | Accepted by unrelated API or wrong audience |
| Refresh token | Obtain new access tokens | Stored in logs/browser-accessible locations or not rotated |
| Session cookie | Reference server-side session or protected client session | Treated as safe because it is opaque or encrypted |
| API key | Identify/authorize an application or integration according to its design | Shared, unscoped, permanent key used as user identity |
| SAML assertion | Convey federated authentication/attributes to an RP | Accepted without audience, time, signature or replay validation |
| Client certificate | Authenticate a client or workload at transport/application layer | Trusted solely because any certificate chains to a broad CA |
| DPoP proof | Demonstrate possession of a key for a bound OAuth token | Treated as replacement for token validation or client authentication |

### 9.2 JWT validation

JWT is a token format, not a complete trust model. A robust validation policy includes:
- Expected token type and protocol profile.
- Trusted issuer.
- Correct audience and resource.
- Explicit algorithm allow-list.
- Signature validation with trusted keys.
- Expiration and not-before validation.
- Appropriate issued-at and maximum age checks.
- Subject and client identity validation.
- Scope/role/authorization claim semantics.
- Key rotation and issuer-key discovery controls.
- Replay protection or sender constraint where needed.
- Token size and claim limits.
- Safe error behavior.

Avoid:
- alg=none acceptance.
- Algorithm confusion between symmetric and asymmetric algorithms.
- Trusting a token's own jku, x5u or arbitrary jwk.
- Accepting tokens issued for another API/client.
- Treating arbitrary claims as trusted authorization policy.
- Long-lived tokens without a revocation strategy.
- Logging or storing tokens in source control.
- Reusing one signing key across unrelated environments or tenants without deliberate design.

A JWT signature proves integrity and signing-key possession under the selected algorithm. It does not prove the user is still employed, the permission remains valid, the session has not been revoked, or the requested object belongs to the caller.

### 9.3 Bearer token exposure and sender constraint

A bearer token can be used by whoever possesses it. Reduce exposure through secure storage, transport security, scope minimization, short lifetime, audience restrictions, rotation and revocation.

DPoP (RFC 9449) binds token use to proof of possession of a key at the application layer. Mutual TLS certificate-bound tokens are another sender-constraining approach. These mechanisms reduce replay utility after token theft but do not protect a compromised client that can access both token and private key. They also require correct nonce, proof, key and replay handling.

## 10. Session management

### 10.1 Session lifecycle

A session is a security state, not merely a cookie. Define creation after successful authentication, identifier rotation after login and privilege elevation, idle and absolute expiration, reauthentication and step-up rules, concurrent session policy, logout and revocation, password reset and authenticator-change effects, device loss and compromise response, and session storage/replication/invalidation across application nodes.

### 10.2 Cookie controls

For browser sessions using cookies:
- Use Secure so cookies are sent only over HTTPS.
- Use HttpOnly to limit script access.
- Set an appropriate SameSite policy based on federation and application behavior.
- Use host-only cookies where possible; avoid broad Domain scope.
- Prefer __Host- cookie prefix where its requirements fit the design.
- Set deliberate Path and expiry policy.
- Do not put session IDs in URLs.
- Protect state-changing requests against CSRF.
- Use HTTPS and HSTS at the correct deployment boundary.

HttpOnly does not prevent XSS from performing actions as the user. SameSite is not a universal CSRF control for every cross-site flow. CSRF tokens and origin checks may still be required.

### 10.3 Session invalidation

Logout must invalidate server-side session or revoke the associated credential according to the architecture. Deleting a browser cookie alone does not invalidate a copied token. Password change, account disable, privilege removal and compromise response must trigger the appropriate session/token revocation path.

### 10.4 Session test cases

- Session ID changes after authentication.
- Session ID changes after privilege elevation.
- Expired session cannot access protected routes.
- Logout invalidates server-side state.
- Password reset triggers configured session revocation.
- Cookie attributes match intended deployment.
- CSRF controls reject cross-site state-changing requests.
- Session cannot be fixed by attacker-chosen identifier.
- Concurrent session behavior matches documented policy.
- Revoked access is consistent across nodes and APIs within the defined propagation objective.

## 11. Authorization engineering

### 11.1 Authorization is separate from authentication

For every protected action, evaluate:

**Permit(subject, action, resource, context)**

Context may include tenant, ownership, relationship, data classification, device state, authentication strength, time, location, approval, transaction amount and workflow state.

A role check alone may be insufficient. An authenticated user with report.read permission should not automatically read every tenant's report.

### 11.2 Enforcement architecture

| Component | Responsibility | Failure rule |
|---|---|---|
| Policy Administration Point (PAP) | Defines, versions and approves policies | Unauthorized policy changes denied |
| Policy Decision Point (PDP) | Evaluates request and context | Fail closed for protected actions when decision unavailable |
| Policy Enforcement Point (PEP) | Enforces permit/deny at application/resource boundary | No bypass through alternate route or worker |
| Policy Information Point (PIP) | Supplies identity, resource, relationship and environment attributes | Attribute freshness and provenance must be known |
| Audit/decision log | Records decision and relevant policy version | Must not leak secrets or become user-modifiable |

For distributed services, decide whether the PEP calls a central PDP, uses a local policy engine, or evaluates signed/cached policy. Define cache TTL, invalidation, outage behavior, policy versioning and consistency. A stale authorization cache can preserve revoked access.

### 11.3 Access control models

| Model | Decision basis | Suitable use | Risks / limits |
|---|---|---|---|
| DAC | Resource owner discretion | User-controlled sharing and file permissions | Permission propagation and ownership transfer complexity |
| MAC | Centrally assigned labels and clearances | High-assurance classified environments | Rigid classification and operational overhead |
| RBAC | Roles and role-permission assignments | Stable job functions and enterprise administration | Role explosion, inherited privilege, stale assignments |
| ABAC | Subject, resource, action and environment attributes | Fine-grained contextual policy | Attribute quality, policy complexity and explainability |
| ReBAC | Relationships between subject and resource | Ownership, team, group, delegated access and sharing | Relationship graph consistency and traversal performance |
| PBAC | Explicit policies evaluated by a policy engine | Centralized complex decisions | Policy lifecycle, testing and enforcement consistency |

Use the simplest model that satisfies real access rules. Hybrid RBAC + ABAC/ReBAC is common: roles establish broad capability, while resource relationship and context narrow access.

### 11.4 RBAC engineering

- Define roles from business responsibilities, not individual people.
- Use stable role names and documented permission sets.
- Avoid assigning roles directly from untrusted request properties.
- Separate platform roles from tenant roles.
- Prevent users from granting their own roles.
- Validate role hierarchy and inheritance.
- Identify toxic combinations and segregation-of-duties conflicts.
- Review group nesting and inherited permissions.
- Remove unused roles and duplicate entitlements.
- Test negative access and privilege escalation.

### 11.5 ABAC engineering

A policy can consider:
- Subject: department, employment status, clearance, tenant, role, risk.
- Resource: owner, tenant, classification, state, type.
- Action: read, update, approve, export, delete, administer.
- Environment: device posture, authentication strength, time, network risk.

Attributes must come from trusted, governed sources. A request body field named department, tenant or isManager is not a trusted attribute.

### 11.6 ReBAC engineering

Relationships can express user ownership of a document, membership of a project, group assignment to a course, manager supervision, approved temporary support access, or a service authorized to publish to a queue.

Define relationship creation, deletion, inheritance, delegation, cycle handling, consistency and cache invalidation. Test indirect paths and transitive relationships, not only direct ownership.

### 11.7 Object-, function- and property-level authorization

Every API and application feature must consider:
- Function-level: may this subject invoke the operation?
- Object-level: may this subject access this exact record?
- Property-level: may this subject read or modify each field?
- Tenant-level: does the resource belong to an authorized tenant?
- Workflow-level: is this transition permitted in the current state?

Use explicit request/response DTOs. Avoid binding arbitrary request properties directly to persistence entities. Do not expose hidden properties in API responses merely because the caller can access the record.

### 11.8 Deny-by-default and least privilege

Explicitly grant only necessary permissions. Deny when policy is missing, malformed or cannot be evaluated for a protected operation. Avoid wildcard scopes and admin shortcuts. Restrict bulk operations separately from single-record operations. Treat exports, search, analytics, backups and support tooling as protected resource paths. Reauthorize high-impact operations at execution. Review service-to-service permissions independently of human role assignments.

## 12. Multi-tenant identity and authorization

### 12.1 Tenant context

A tenant ID is a security boundary attribute. It must be derived from a trusted identity or verified relationship, not trusted simply because a caller supplies it.

For each request:
1. Validate the authenticated subject.
2. Resolve the subject's active tenant membership.
3. Determine the requested tenant context.
4. Verify the subject may act in that tenant.
5. Bind the tenant context to data access and policy evaluation.
6. Enforce tenant constraints in every query and write.
7. Record tenant context in security audit events.

### 12.2 Common multi-tenant failures

- IDOR/BOLA across tenant identifiers.
- User changes tenantId in request body.
- Shared cache key omits tenant or principal.
- Search and export endpoints omit tenant filtering.
- Background job trusts tenant value from queue payload without validating producer/ownership.
- Tenant admin can access platform-level controls.
- Global administrator is silently granted to tenant-scoped users.
- File storage paths or object keys can be guessed or substituted.
- Audit logs omit tenant attribution.
- Tenant deletion leaves active credentials, service principals or integrations.

### 12.3 Isolation design

Use layered controls: tenant-aware authorization policy, tenant-scoped repository/service methods, database row-level security where supported and correctly configured, tenant-aware cache keys, object storage access policy and opaque object IDs, queue message provenance and schema validation, separate encryption keys or key contexts where risk requires, tenant-aware audit and incident investigation, and automated cross-tenant negative tests.

Database row-level security is defense in depth, not permission to omit application authorization. Verify connection-pool/session context reset to prevent tenant context leakage between requests.

## 13. Privileged Access Management (PAM)

### 13.1 Privileged access principles

- Separate standard user and administrative identities for high-impact administration where practical.
- Require strong, phishing-resistant authentication for privileged access where feasible.
- Remove standing privilege when JIT elevation can safely meet operational needs.
- Require justification, approval and bounded duration for sensitive elevation.
- Use privileged credential vaulting and session management where appropriate.
- Record commands/actions and administrative session metadata proportionate to privacy and law.
- Restrict access to production secrets, signing keys and identity-provider configuration.
- Prevent privileged users from altering or deleting their own audit evidence.
- Revalidate privilege when role, employment or incident status changes.

### 13.2 JIT and approval workflow

~~~mermaid
flowchart TD
    R[User requests elevated access] --> V[Validate identity, device and request]
    V --> J{Justification and scope valid?}
    J -->|No| D[Deny and record]
    J -->|Yes| A[Independent approval if required]
    A --> P[Policy and SoD check]
    P -->|Fail| D
    P -->|Pass| G[Grant minimum role for bounded duration]
    G --> M[Monitor privileged activity]
    M --> E[Expire and revoke grant]
    E --> C[Verify revocation and record evidence]
~~~

### 13.3 Break-glass access

Break-glass is an emergency mechanism, not a permanent administrator account. Define trigger conditions and authorized custodians, protect credentials separately from normal authentication dependencies, require multi-person approval where feasible with a documented emergency exception, alert immediately on use, limit permissions and duration, record actions, rotate/invalidate credentials after use, review the event and test the process periodically. Ensure the emergency path does not become an unmonitored bypass.

## 14. Non-human, service and workload identity

### 14.1 Service identity risks

Non-human identities often have long lifetimes, unclear owners, embedded secrets, excessive permissions and poor monitoring. They may persist after the original application or employee has been retired.

Maintain an inventory of service accounts, OAuth clients, API keys, certificates, cloud service principals, Kubernetes service accounts, CI/CD identities, database users, scheduled jobs and automation identities.

### 14.2 Preferred patterns

- Prefer platform-issued workload identity and short-lived credentials over static shared secrets.
- Use mutual TLS or signed workload identity tokens where architecture supports them.
- Bind identity to workload, environment, namespace, audience and intended service.
- Use separate identities per application and environment.
- Limit scopes and permissions.
- Store unavoidable secrets in a managed vault or secrets manager.
- Rotate and revoke secrets with an owner and tested procedure.
- Prevent credentials from entering source control, images, logs and build artifacts.
- Monitor identity use and detect unexpected source, audience, scope or timing.
- Remove identities when workloads are decommissioned.

### 14.3 API keys

An API key is not automatically a user identity and should not be used as a universal authorization mechanism. Generate high-entropy keys using a cryptographically secure generator, display secret material only at creation where feasible, store a verifier/hash or protected secret representation according to key design, scope keys to client/tenant/resource/operations, apply expiration/rotation/revocation and last-used tracking, support multiple active keys during controlled rotation, rate-limit and monitor, never place keys in URLs, avoid reuse across environments, and treat leaked keys as compromised even if removed from repository history.

### 14.4 Machine-to-machine OAuth

For client credentials:
- Authenticate the client with an appropriate confidential-client mechanism.
- Prefer asymmetric client authentication such as private-key JWT or mutual TLS where supported and operationally justified.
- Issue tokens for a specific resource/audience and minimal scope.
- Do not use a human user token to represent an unattended workload unless delegated-user semantics are intentionally designed.
- Store private keys in a protected key store, not source code.
- Rotate credentials and support revocation.
- Ensure resource servers validate client identity and token audience.
- Separate client identity from end-user identity in audit records.

### 14.5 Workload identity federation

Where a cloud or platform can exchange a trusted workload assertion for short-lived credentials:
- Restrict trusted issuer, subject, audience and repository/environment claims.
- Avoid wildcard subject matching.
- Bind deployment identity to approved repository, branch, workflow and environment.
- Require protected branches and reviewed workflows.
- Restrict token lifetime and permissions.
- Prevent pull-request-controlled code from obtaining production deployment identity.
- Audit federation configuration and trust-policy changes.

## 15. Identity governance, provisioning and SCIM

### 15.1 Provisioning principles

Provisioning synchronizes identity and group data across systems. Synchronization is a high-impact privilege path: a compromised or misconfigured source can create accounts, assign groups or disable users across many applications.

Controls:
- Identify the authoritative source for each attribute.
- Define precedence when sources conflict.
- Authenticate and authorize provisioning clients.
- Validate schemas and reject unsafe or unexpected attributes.
- Apply group and role mapping through reviewed policy.
- Prevent user-controlled fields from becoming privileged entitlements.
- Log create, update, disable, delete and group membership operations.
- Detect mass changes, unusual source and privilege expansion.
- Support reconciliation and drift detection.
- Define retry, idempotency and partial-failure handling.

### 15.2 SCIM

System for Cross-domain Identity Management (SCIM) provides HTTP-based provisioning and management of identity resources such as Users and Groups. RFC 7643 defines core schemas and RFC 7644 defines the protocol.

Review authenticated and authorized provisioning clients, TLS and credential rotation, tenant and resource scoping, user and group attribute allow-lists, PATCH semantics and immutable attributes, filter and pagination limits, duplicate identity handling, soft disable versus deletion semantics, group membership and role mapping, audit, reconciliation and rate limits.

Do not treat SCIM active state or group membership as a complete authorization decision. The application must define how provisioning state maps to account status and permissions.

## 16. Zero Trust and continuous access evaluation

Zero Trust is an architectural approach, not a product or a single MFA control. NIST SP 800-207 emphasizes protecting resources and avoiding implicit trust based only on network location or ownership.

Identity-related principles:
- Authenticate subject and device as distinct signals where appropriate.
- Authorize each access request based on current policy and context.
- Apply least privilege and resource-specific decisions.
- Reassess access as risk and context change.
- Avoid broad implicit trust based on VPN, subnet or office location.
- Use service identity and workload context for machine access.
- Monitor and revoke access when identity, device or resource state changes.

Continuous access evaluation can reduce the window between revocation and token expiry, but requires consistent event propagation, resource-server support and defined failure behavior. A token with a long validity period and no revocation path is difficult to reconcile with rapid access removal.

## 17. AI agent and delegated identity security

AI agents introduce a distinct identity and authority problem. An agent may interpret untrusted instructions, retrieve sensitive data and invoke tools. Do not let model-generated text become an authorization decision.

Requirements:
- Assign each agent/service a distinct identity and owner.
- Use a narrowly scoped tool identity rather than a human administrator token.
- Bind delegated authority to initiating user, tenant, task, allowed tools and duration.
- Preserve the chain of delegation in audit records.
- Separate read, write, approve and execute capabilities.
- Require human approval for high-impact or irreversible actions.
- Validate tool arguments and resource identifiers independently of model output.
- Reauthorize at the tool or service boundary.
- Limit token audience, scope and lifetime.
- Prevent untrusted retrieved content from changing identity policy or tool permissions.
- Provide immediate revocation and emergency disable.
- Test confused-deputy, cross-tenant, prompt-injection and privilege-escalation scenarios.

An agent identity does not inherit unlimited authority from the user who started it. Delegation must be explicit, bounded and independently enforced.

## 18. Common identity attacks and failure modes

| Threat / weakness | Root cause | Potential impact | Primary controls |
|---|---|---|---|
| Credential stuffing | Password reuse and weak abuse controls | Account takeover | MFA/passkeys, compromised-password screening, rate controls, risk detection |
| Password spraying | Low-rate attempts across accounts | Workforce compromise | Smart throttling, MFA, identity telemetry, detection |
| Phishing / adversary-in-the-middle | User submits credentials/OTP to impostor site | Session/token theft | Phishing-resistant authentication, origin-bound credentials, secure session handling |
| MFA fatigue | Repeated push requests exploit user approval | Unauthorized approval | Number matching/context, throttling, risk controls, user education |
| SIM swap | Phone number takeover | OTP interception and recovery compromise | Avoid SMS for high assurance; stronger recovery and carrier-risk signals |
| Account enumeration | Different responses or timing disclose account existence | Targeted attacks and privacy exposure | Consistent responses, careful timing, rate controls |
| Weak recovery | Reset process weaker than login | Account takeover | Equivalent proofing, single-use tokens, notifications, delay/hold for high risk |
| Session fixation | Attacker-controlled/pre-auth session retained | Session takeover | Rotate identifiers after authentication and privilege change |
| Session hijacking | Token theft via malware, XSS or leakage | Impersonation | Secure storage, TLS, HttpOnly, CSP, short lifetime, revocation |
| JWT validation bypass | Wrong algorithm/key/issuer/audience handling | Forged or misdirected token acceptance | Strict profile and trusted key validation |
| OAuth redirect abuse | Weak redirect matching or state binding | Code/token theft | Exact redirect URI, PKCE, state, issuer validation |
| OAuth mix-up | Client confuses authorization servers | Code sent to wrong issuer/token endpoint | Issuer identification and RFC 9700 controls |
| SAML signature wrapping | XML signature validated against wrong node | Forged assertion acceptance | Maintained library, exact element binding, hardened parser |
| IDOR/BOLA | Authentication without object authorization | Cross-user or cross-tenant access | Resource-level policy enforcement |
| Mass assignment | Request binds privileged properties | Role/tenant/ownership manipulation | DTO allow-list and server-side property assignment |
| Privilege escalation | Role inheritance or policy gap | Admin access or data compromise | Least privilege, SoD, negative tests, access reviews |
| Orphaned service account | Lifecycle lacks owner and leaver cleanup | Persistent unauthorized access | Inventory, ownership, expiry, disable and credential rotation |
| Token replay | Bearer token theft and reuse | Unauthorized API calls | Short lifetime, rotation, DPoP/mTLS, replay detection |
| Workload identity abuse | Over-broad federation trust or role | Cloud or CI/CD compromise | Subject/audience constraints, protected workflows, short-lived tokens |
| Confused deputy | Service uses its own privilege on caller's behalf | Cross-tenant or unauthorized action | Preserve caller context, delegated scope, per-resource authorization |
| Break-glass misuse | Emergency account remains active or unmonitored | Unaccountable privilege | Vault, dual control, alert, time limit and post-use review |
| Identity provider compromise | Central IdP/key/admin compromise | Broad federation and application compromise | Tiered admin, key protection, resilient recovery, monitoring and isolation |

## 19. Secure implementation patterns by ecosystem

### 19.1 Java / Spring

Review Spring Security filter chain ordering and matcher specificity, authentication provider and password encoder configuration, method/service-level authorization, resource-based authorization handlers, OAuth2 client/resource-server configuration and issuer/audience validation, JWT decoder algorithm and trusted issuer configuration, session fixation protection, CSRF and cookie settings, CORS and redirect URI behavior, SAML library configuration and metadata trust, actuator and management endpoints, async/background job identity propagation and error handling.

Implementation principles:
- Use maintained Spring Security components rather than custom token parsing.
- Validate issuer, audience and algorithm explicitly for each resource server.
- Keep authorization at service boundary so alternate controllers and jobs cannot bypass it.
- Use DTOs and explicit policy checks for object/property access.
- Treat SecurityContext propagation into async work as an explicit design decision; do not assume a thread-local identity automatically follows background tasks.
- Test proxy and reverse-proxy configuration because forwarded headers can affect redirect and origin decisions.

### 19.2 .NET / ASP.NET Core

Review authentication scheme selection and default scheme behavior, JWT bearer issuer/audience/signing key/algorithm validation, policy and resource-based authorization handlers, cookie settings/session behavior/antiforgery, OpenID Connect correlation/nonce/callback handling, Data Protection key storage and sharing, claims transformation and role mapping, impersonation/delegated access, background worker identity, authorization fallback policy and anonymous endpoint inventory.

Implementation principles:
- Use explicit AddAuthentication scheme configuration; avoid accidental fallback to an unintended scheme.
- Use named authorization policies and resource authorization.
- Validate JWT issuer and audience for each API.
- Do not assume a claim named role or tenant is trustworthy without validating its issuer and mapping semantics.
- Keep admin endpoints in a distinct policy and preferably a distinct administrative access path.
- Use antiforgery for cookie-authenticated state-changing browser operations.
- Protect Data Protection keys; inconsistent key rings can cause session/authentication failures, while overly shared keys broaden trust.

### 19.3 Node.js / TypeScript

Review Passport/OIDC middleware or equivalent maintained protocol libraries, OAuth state/nonce/PKCE handling, JWT verification configuration and key source, session middleware store/cookie/rotation behavior, route-level and service-level authorization, async context and background job principal propagation, multi-tenant middleware and request context binding, prototype pollution in claims/role mapping objects, API key lifecycle and scope, token leakage in logs/traces and error reports.

Implementation principles:
- Do not decode JWT and treat decoded claims as verified.
- Use maintained libraries that validate the intended token profile.
- Validate runtime request and claims schema; TypeScript compile-time types do not validate external tokens.
- Keep a server-side session store for browser session architectures where appropriate.
- Use explicit authorization middleware and repeat checks in service methods for sensitive operations.
- Do not trust req.user fields without knowing which middleware populated them and what validation it performed.

### 19.4 Python

Review Django/Flask/FastAPI authentication and authorization integration, session and CSRF middleware ordering, OAuth/OIDC client and resource-server libraries, JWT algorithm/issuer/audience validation, permission decorators and object-level policy, async context and background task identity propagation, tenant context binding and database session reuse, password hashing configuration and upgrade path, admin interface exposure and recovery workflows.

Implementation principles:
- Use framework-maintained password and session mechanisms where suitable.
- Do not implement JWT signature validation manually.
- Apply object-level authorization in service/query paths, not only view decorators.
- Use explicit Pydantic or equivalent schemas for external identity and request data.
- Bind a background task to an explicit service/delegation identity rather than serializing a live user session.
- Ensure tenant context is reset when database connections or workers are reused.

## 20. Identity security verification methodology

### 20.1 Assessment authorization and scope

Before testing:
- Obtain written authorization from application and identity-platform owners.
- Identify test tenants, accounts, IdP, federation connections and environments.
- Use synthetic users with distinct roles and tenant memberships.
- Define permitted login, recovery, token and privilege tests.
- Confirm no production user lockout, MFA reset, email/SMS flood or real account takeover is possible.
- Define test window, emergency contact and stop conditions.

Do not test real employee accounts or attempt to bypass production identity controls without explicit authorization.

### 20.2 Evidence collection

Capture application and identity-provider version/configuration, test identity and role (synthetic identifier only), protocol flow and relevant redacted request/response, token metadata without exposing bearer token values, authorization decision and resource context, before/after entitlement state, audit event and correlation ID, reproduction steps, expected/observed result, remediation and retest evidence.

Never include passwords, private keys, client secrets, raw session cookies, access tokens, refresh tokens or recovery codes in reports.

### 20.3 Authentication test procedure

1. Inventory all authentication entry points: UI, API, mobile, SSO, admin, support, recovery and machine endpoints.
2. Identify accepted authentication schemes and assurance requirements.
3. Review enrollment, password reset, MFA reset and account recovery.
4. Verify rate controls and abuse detection with low-impact synthetic tests.
5. Test session rotation, expiry and logout.
6. Verify MFA enforcement and downgrade paths for privileged roles.
7. Review device and risk policy behavior.
8. Confirm disabled, locked, expired and terminated identities cannot authenticate according to policy.
9. Inspect audit events and alerting for failed/suspicious attempts.
10. Document all alternate paths and residual risk.

### 20.4 Authorization test procedure

For each sensitive function:
1. Identify subject, action, resource, tenant and workflow state.
2. Build an access matrix for allowed and denied combinations.
3. Test unauthenticated access.
4. Test authenticated user without required function permission.
5. Test another user's object in the same tenant.
6. Test an object from another tenant.
7. Test property-level read and update restrictions.
8. Test role changes and stale sessions.
9. Test bulk/export/search/background job paths.
10. Test workflow state and replay.
11. Verify server-side enforcement and audit.
12. Repeat after remediation and across alternate endpoints.

### 20.5 Federation and token verification

1. Inventory issuer, client, redirect URI, audience, metadata and key sources.
2. Verify exact redirect URI registration and client type.
3. Confirm PKCE and state/nonce transaction binding where applicable.
4. Verify ID Token and access token are used for intended recipient.
5. Test invalid issuer, audience, signature, algorithm and expiry using synthetic tokens in isolated environment.
6. Verify key rotation and unknown key handling.
7. Review refresh token rotation/reuse detection.
8. Verify SAML signature element binding, issuer, audience, recipient, time and replay checks.
9. Review logout and revocation behavior.
10. Record evidence with token values redacted.

### 20.6 Privileged access verification

- Inventory privileged roles and standing assignments.
- Confirm separate admin identities and stronger authentication.
- Verify JIT approval, duration and automatic expiry.
- Test denial for unauthorized role self-assignment.
- Confirm break-glass alerts and post-use review.
- Verify privileged users cannot alter their own audit trail.
- Review access to signing keys, IdP configuration, vaults and backup credentials.
- Confirm deprovisioning removes privilege across connected systems.

## 21. Identity security test catalogue

| Test ID | Area | Test | Expected result |
|---|---|---|---|
| IAM-T-001 | Enrollment | Attempt to bind authenticator to another account | Denied; ownership preserved |
| IAM-T-002 | Recovery | Use expired or reused reset token | Denied |
| IAM-T-003 | Recovery | Reset MFA using only a password | Denied or additional approved proof required |
| IAM-T-004 | Authentication | Low-rate repeated failed login in synthetic account | Throttled/risk-handled without easy global lockout |
| IAM-T-005 | MFA | Privileged account attempts password-only access | Denied or approved step-up required |
| IAM-T-006 | Passkey | Replay an old WebAuthn challenge | Denied |
| IAM-T-007 | Passkey | Use credential at wrong RP/origin | Denied |
| IAM-T-008 | Session | Session identifier before and after login | Rotated |
| IAM-T-009 | Session | Reuse session after logout | Denied |
| IAM-T-010 | Session | Use expired session | Denied |
| IAM-T-011 | CSRF | Cross-site state-changing request | Denied without valid CSRF proof |
| IAM-T-012 | OAuth | Authorization request with unregistered redirect URI | Rejected |
| IAM-T-013 | OAuth | Authorization code redemption without valid PKCE verifier | Rejected for public client |
| IAM-T-014 | OAuth | Authorization response with mismatched state | Rejected |
| IAM-T-015 | OAuth/OIDC | Wrong issuer or audience in ID Token | Rejected |
| IAM-T-016 | JWT | Disallowed algorithm or invalid signature | Rejected |
| IAM-T-017 | JWT | Token intended for another API | Rejected |
| IAM-T-018 | Token | Expired/revoked refresh token reuse | Rejected and security event recorded |
| IAM-T-019 | SAML | Wrong audience/recipient or expired assertion | Rejected |
| IAM-T-020 | SAML | Replayed assertion ID | Rejected |
| IAM-T-021 | Authorization | User accesses another user's record | Denied unless explicit sharing policy permits |
| IAM-T-022 | Authorization | Tenant A accesses Tenant B object | Denied |
| IAM-T-023 | Property | Learner attempts to change role/tenant/approval field | Rejected or ignored; no state change |
| IAM-T-024 | Role | User attempts self-assignment to admin role | Denied and audited |
| IAM-T-025 | Workflow | User repeats one-time approval/submission | Idempotent or rejected per policy |
| IAM-T-026 | Provisioning | SCIM client submits unauthorized privileged group change | Rejected |
| IAM-T-027 | Lifecycle | Leaver event is processed | Account, sessions, credentials and entitlements revoked within policy SLA |
| IAM-T-028 | Workload | Workload requests token for unauthorized audience | Denied |
| IAM-T-029 | Workload | Unapproved repository/workflow attempts cloud federation | Denied |
| IAM-T-030 | PAM | JIT role exceeds approved duration | Automatically expires and is revoked |
| IAM-T-031 | Break-glass | Emergency identity is used | Immediate alert, bounded access and review record |
| IAM-T-032 | Audit | Identity action attempts to inject log fields or expose token | Structured audit; secret redacted |
| IAM-T-033 | Cache | Role revoked while authorization cache exists | Revocation effective within documented propagation objective |
| IAM-T-034 | Agent | Agent attempts tool action outside delegated scope | Denied at tool/resource enforcement point |

## 22. Detection, monitoring and incident response

### 22.1 High-value telemetry

Collect and correlate authentication success/failure, method and assurance context, new device and authenticator enrollment/removal, recovery changes, password reset and MFA reset, new sessions and revocation, token issuance, OAuth client registration and scope changes, federation metadata and signing certificate changes, privilege grants and group membership, service-account creation and key rotation, workload token issuance and audience/subject, SCIM mass update, break-glass use, authorization denials, cross-tenant attempts and sensitive exports, identity-provider administrator changes and policy modifications.

### 22.2 Detection scenarios

| Detection ID | Scenario | Signal | Initial response |
|---|---|---|---|
| IAM-D-001 | Password spraying | Many accounts targeted from related source patterns with low attempts per account | Validate campaign; throttle and protect affected accounts |
| IAM-D-002 | Credential stuffing | High volume of credential pairs and elevated success anomalies | Rate controls, risk-based challenge and account protection |
| IAM-D-003 | MFA fatigue | Repeated push prompts followed by approval | Contact user, revoke sessions, investigate sign-in context |
| IAM-D-004 | New authenticator abuse | New MFA/passkey registered followed by sensitive action | Verify user, review enrollment source and revoke if unauthorized |
| IAM-D-005 | Recovery takeover | Email/phone/MFA changes followed by password reset or data export | Place account under review and revoke sessions |
| IAM-D-006 | Privilege escalation | Role/entitlement grant outside approved workflow | Disable grant, preserve evidence and investigate actor |
| IAM-D-007 | Dormant service identity | Old service identity suddenly authenticates or accesses new resource | Suspend safely, identify owner and validate workload |
| IAM-D-008 | Token anomaly | Unexpected issuer, audience, client, scope, location or replay pattern | Reject token, revoke affected credentials and inspect clients |
| IAM-D-009 | Federation trust change | IdP metadata, certificate or redirect URI changed unexpectedly | Validate approval; disable malicious trust if confirmed |
| IAM-D-010 | Cross-tenant access attempts | Repeated denied access to foreign tenant objects | Investigate probing, logic flaw or compromised account |
| IAM-D-011 | Break-glass use | Emergency identity login or privilege activation | Immediate on-call escalation and post-use review |
| IAM-D-012 | Workload federation anomaly | Token request from unapproved repo, branch, environment or audience | Revoke trust and inspect CI/CD pipeline |
| IAM-D-013 | Mass provisioning change | Unusual SCIM create/disable/group update burst | Pause provisioning integration and reconcile authoritative source |
| IAM-D-014 | Agent scope violation | Agent attempts tool outside delegated task scope | Block tool, revoke delegation and inspect prompt/tool context |

Tune detections to the organization's baseline. A source IP or geographic change alone is not proof of compromise.

### 22.3 Identity compromise response

1. Confirm affected subject, identity type, tenant, client and resources.
2. Preserve relevant identity-provider, application, endpoint and audit evidence.
3. Disable or restrict compromised identity where safe.
4. Revoke sessions, access/refresh tokens, API keys, certificates and active grants as appropriate.
5. Rotate secrets and signing credentials if exposure is suspected.
6. Review authenticator enrollment, recovery changes and delegated access.
7. Identify accessed resources, data exports and downstream service calls.
8. Search for persistence: new users, OAuth clients, federation trust, service accounts and access policies.
9. Restore identity from authoritative source and re-enroll authenticators securely.
10. Validate authorization and tenant boundaries.
11. Notify stakeholders and regulators where legally required, through appropriate process.
12. Record root cause, timeline, impact, corrective actions and lessons learned.

Do not rotate a shared identity-provider signing key without assessing all relying parties and coordinating key rollover. A poorly coordinated emergency change can cause broad service outage.

## 23. Operational procedures

### 23.1 New application onboarding to enterprise SSO

**Purpose:** onboard an application to a trusted enterprise IdP.

**Prerequisites:** application owner, data classification, approved redirect/ACS endpoints, protocol selection, test tenant, security contact and rollback plan.

**Steps:**
1. Identify application users, roles, tenant model and sensitive actions.
2. Choose OIDC or SAML based on supported architecture and business requirement.
3. Register exact client identifier, redirect URI or ACS URL.
4. Configure issuer, audience, signing algorithms, keys/certificates and metadata source.
5. Define claim/attribute mapping using trusted IdP attributes.
6. Define default-deny behavior and application-side authorization.
7. Configure session, logout and revocation semantics.
8. Test invalid issuer, audience, signature, state/nonce, expired response and replay.
9. Test account provisioning, deprovisioning and role removal.
10. Complete owner approval, evidence capture and production change control.
11. Monitor first production authentication and keep rollback path available.

**Stop conditions:** unverified metadata, wildcard redirect, unexpected issuer, unbounded role mapping, missing app owner or unresolved authorization bypass.

### 23.2 Privileged role grant

1. Confirm requester identity and employment/contract status.
2. Identify requested resource, permission, duration and business justification.
3. Check segregation-of-duties and existing entitlements.
4. Obtain independent approval where required.
5. Verify strong authentication and device/security posture.
6. Grant minimum role with expiry.
7. Notify requester and owner.
8. Monitor activity and alert on prohibited actions.
9. Revoke automatically at expiry.
10. Verify removal and preserve evidence.

### 23.3 Service account creation and retirement

**Creation:** document owner, application, purpose, environment, required resources, authentication method, scopes, expiry, rotation, monitoring and emergency contact. Obtain approval and create a unique identity. Store credentials in an approved vault or use workload identity. Test only intended permissions.

**Retirement:** identify dependent jobs and integrations, schedule safe migration, disable the identity, revoke credentials and certificates, remove permissions, verify no unexpected dependency, preserve required audit evidence and delete according to policy.

### 23.4 Identity-provider signing-key rotation

1. Inventory all relying parties and token/assertion validation dependencies.
2. Confirm key algorithm, key ID, certificate validity and trust distribution.
3. Generate/store new key in approved protected environment.
4. Publish new public key or metadata according to protocol and vendor procedure.
5. Support controlled overlap of old and new keys where safe.
6. Validate relying-party cache refresh and signature verification.
7. Begin issuance with new key.
8. Monitor validation failures and unknown-key events.
9. Retire old key after all dependent tokens/assertions and cache windows are addressed.
10. Preserve approval, key custody and rollover evidence.

Do not expose private signing keys in source control, ticketing systems or application logs.

## 24. Metrics and effectiveness

| Metric | Definition | Interpretation |
|---|---|---|
| Orphan identity rate | Active identities without verified owner or authoritative source | Inventory and lifecycle weakness |
| Leaver deprovisioning time | Time from authoritative termination event to effective revocation | Measure end-to-end, not directory disable alone |
| Privileged standing access | Number/percentage of privileged assignments without expiry | Indicates standing privilege exposure |
| MFA/passkey coverage | Coverage by identity class and risk tier | Segment privileged, workforce, customer and workload identities |
| Phishing-resistant coverage | Eligible high-risk identities using phishing-resistant authentication | More meaningful than generic MFA percentage |
| Access review completion | Reviews completed with attributable decision and evidence | Avoid counting bulk approvals without context |
| Stale entitlement rate | Permissions unused or not revalidated beyond defined threshold | Requires usage and business context |
| Service identity ownership | Non-human identities with owner, purpose and expiry | Inventory quality |
| Credential rotation compliance | Credentials rotated/revoked within policy and on risk events | Include keys/certs/API tokens |
| Authorization test coverage | Sensitive endpoints with positive and negative tests | Include object, property and tenant checks |
| Revocation propagation | Time until access is denied across dependent systems | Detect stale token/cache exposure |
| Identity incident rate | Confirmed identity-related incidents by root cause | Use for trend analysis, not blame |
| Federation trust hygiene | Connections with owner, valid metadata/certificates and current review | Measures federation governance |
| JIT usage and expiry | Temporary grants automatically expired and verified | Shows whether privilege is time-bounded |

Do not optimize only for MFA adoption, password reset count or number of access reviews. Measure control effectiveness and residual exposure.

## 25. Standards and framework traceability

### 25.1 NIST SP 800-63-4 Digital Identity Guidelines

NIST SP 800-63-4 was published in July 2025 and supersedes SP 800-63-3. It is a four-part suite:
- SP 800-63-4: overarching digital identity guidelines and risk management.
- SP 800-63A-4: identity proofing and enrollment.
- SP 800-63B-4: authentication and authenticator management.
- SP 800-63C-4: federation and assertions.

The suite defines identity assurance level (IAL), authenticator assurance level (AAL) and federation assurance level (FAL) concepts. Select levels through the documented risk process and applicable profile. Do not assign a level based on product marketing or the number of login factors alone.

### 25.2 Protocol references

| Reference | Publisher / version | Primary use | Limitation |
|---|---|---|---|
| OAuth 2.0 Security BCP | IETF RFC 9700, January 2025 | Current OAuth security best practices | Does not replace application authorization design |
| OAuth 2.0 Authorization Framework | IETF RFC 6749 | Core OAuth framework | Read with RFC 9700 and relevant extensions |
| OAuth 2.0 Bearer Token Usage | IETF RFC 6750 | Bearer token transport and usage | Bearer tokens require careful leakage protection |
| PKCE | IETF RFC 7636 | Authorization code interception protection | Must be correctly bound to transaction |
| OpenID Connect Core 1.0 | OpenID Foundation, errata set 2 | Identity layer on OAuth 2.0 | Requires strict profile validation |
| DPoP | IETF RFC 9449 | Sender-constrained OAuth token proof | Does not replace token validation or secure client |
| SAML 2.0 | OASIS SAML 2.0 specifications | Enterprise federation and SSO | XML signature/profile implementation is complex |
| SCIM | IETF RFC 7643 and RFC 7644 | Cross-domain identity provisioning | Provisioning is not the same as authorization |
| WebAuthn Level 3 | W3C Recommendation, 25 August 2026 | Web public-key credential API | Deployment behavior depends on browser/authenticator ecosystem |
| Zero Trust Architecture | NIST SP 800-207, August 2020 | Resource-centric access architecture | Not a product certification or one-control solution |

### 25.3 ISO/IEC 27001:2022 / 27002:2022 relationship

The following Annex A control themes are relevant to identity and access governance. Verify exact applicability and evidence against the licensed standard and the organization's statement of applicability.

| Control ID | Control theme | Identity engineering contribution |
|---|---|---|
| 5.15 | Access control | Access policy, business requirements and enforcement |
| 5.16 | Identity management | Identity lifecycle, unique identity and provisioning |
| 5.17 | Authentication information | Protection and lifecycle of passwords, secrets and authenticators |
| 5.18 | Access rights | Grant, review, change and removal of access rights |
| 8.2 | Privileged access rights | Elevated access governance and monitoring |
| 8.3 | Information access restriction | Resource and data access enforcement |
| 8.5 | Secure authentication | Authentication mechanisms and secure configuration |

This is a relationship map, not a declaration that these controls are implemented or that certification follows.

### 25.4 OWASP relationship

- OWASP ASVS 5.0.0: use applicable verification requirements for authentication, session management and access control. Select exact requirement IDs from the official machine-readable release for the target application and version.
- OWASP Top 10:2025: use relevant categories as risk awareness, not as a complete identity verification specification.
- OWASP API Security Top 10:2023: especially API1 Broken Object Level Authorization, API2 Broken Authentication, API3 Broken Object Property Level Authorization, API5 Broken Function Level Authorization and API6 Unrestricted Access to Sensitive Business Flows.
- OWASP Cheat Sheet Series: Authentication, Authorization, Session Management, Password Storage, Multifactor Authentication, OAuth2 and JSON Web Token guidance.

### 25.5 Regulatory relationship

| Jurisdiction / framework | Relevant identity concern | Mapping status and limitation |
|---|---|---|
| India DPDP Act 2023 / DPDP Rules 2025 | Access control and safeguards supporting personal-data protection | Supporting technical control; applicability and phased commencement must be confirmed |
| India CERT-In Directions 2022 | Incident logging, reporting, time synchronization and point of contact | Identity telemetry can support evidence; determine entity and incident scope |
| Qatar NIA v2.1 | Identity/access, secure development and security management controls | Relevant national assurance reference; confirm entity/sector applicability |
| Saudi NCA ECC 2:2024 | Identity and access control across governance and technical domains | Determine whether entity is in mandatory scope; not universally binding on every Saudi business |
| EU GDPR | Article 25 privacy by design/default and Article 32 security of processing | Identity controls support risk-appropriate security; no single control proves compliance |
| PCI DSS v4.0.1 | User identification, authentication, access restriction and privileged access in in-scope environments | Applies only where cardholder-data environment and contractual/assessment scope require it |

## 26. Real-world and composite use cases

### 26.1 Enterprise SSO with multiple applications

**Classification:** Composite industry scenario.

A company uses one enterprise IdP for HR, finance, customer support and engineering applications. A compromised IdP administrator could affect every relying application. The design separates standard and privileged identity, requires phishing-resistant authentication for administrators, restricts federation clients, uses exact redirect URIs, validates issuer/audience, maps claims through approved policies, and independently enforces application roles. Signing-key rollover, emergency disable and access review are tested.

### 26.2 Multi-tenant SaaS identity

**Classification:** Composite industry scenario.

A customer tenant administrator manages users and groups within one organization. The platform administrator manages global service configuration. These roles must be distinct. Tenant context comes from trusted membership and is checked at every data and API boundary. Tenant administrators cannot set global roles or access another tenant's exports. SCIM provisioning is scoped to the tenant and uses an integration identity with narrow permissions.

### 26.3 OT engineering access

**Classification:** Composite industry scenario.

An external engineering supplier requires temporary access to an industrial HMI/SCADA support environment. The design uses a named individual identity, sponsor approval, MFA at the remote access boundary, managed jump host, time-bounded access, session recording where legally and operationally appropriate, network segmentation and explicit asset authorization. Shared vendor accounts are avoided. Emergency access and safe revocation are tested without disrupting control processes. Identity policy must be coordinated with OT availability, safety and change-management requirements.

### 26.4 CI/CD workload identity

**Classification:** Composite industry scenario.

A build workflow obtains cloud deployment credentials through federation. Trust is restricted to an approved repository, protected branch, workflow and production environment. Pull-request-controlled code cannot request production deployment authority. Tokens are short-lived and scoped to a specific resource. Pipeline changes and trust-policy updates are audited.

### 26.5 AI assistant with delegated access

**Classification:** Composite industry scenario.

A support agent can retrieve a ticket and propose a refund, but cannot approve or execute a refund above its delegated limit. The agent uses a dedicated identity, receives a task-scoped token, passes tool calls through a policy enforcement service and requires human approval for financial actions. Retrieved ticket content cannot grant additional permissions. Audit records link the initiating user, agent identity, tool call, policy decision and approval.

## 27. Limitations and unresolved questions

- Identity assurance and authenticator requirements must be selected for the actual service, user population and risk.
- NIST SP 800-63-4 is a strong reference but is not automatically mandatory for every private organization.
- OAuth, OIDC and SAML libraries differ in protocol profile, supported features and secure defaults.
- Token revocation and continuous access evaluation are constrained by architecture and resource-server support.
- Passkey synchronization, attestation and recovery require privacy and threat-model decisions.
- Centralized IdP availability and compromise create enterprise-wide dependencies.
- Attribute and relationship policies can become difficult to test and explain.
- Service and workload identity inventories are often incomplete.
- OT identity changes require safety and availability coordination.
- Agentic identity governance is evolving; product-specific controls need independent verification.
- Regulatory applicability requires jurisdiction- and entity-specific legal analysis.
- Exact ASVS requirement identifiers and complete regulator clause-level mappings remain to be added in a dedicated traceability artifact.

## 28. Related chapters

- [01. Application Security Fundamentals](../01-fundamentals/APPSEC-FUNDAMENTALS.md)
- [02. Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [03. Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [04. Secure Coding and Code Review](../04-secure-coding/SECURE-CODING-AND-CODE-REVIEW.md)
- [05. Web Application Security Engineering](../05-web-application-security/WEB-APPLICATION-SECURITY-ENGINEERING.md)
- [05. Web Application Security Lab Pack](../05-web-application-security/WEB-APPLICATION-SECURITY-LAB-PACK.md)
- [06. API and Service Security Engineering](../06-api-service-security/API-AND-SERVICE-SECURITY-ENGINEERING.md)
- [06. API and Service Security Lab Pack](../06-api-service-security/API-AND-SERVICE-SECURITY-LAB-PACK.md)
- [08. Data Security and Privacy Engineering](../08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-ENGINEERING.md)
- [08. Data Security and Privacy Lab Pack](../08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-LAB-PACK.md)
- [Identity and Access Security Lab Pack](IDENTITY-AND-ACCESS-SECURITY-LAB-PACK.md)
- [Standards Baseline and Mapping Method](../18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md)
- [Global Regulatory Register](../19-global-regulatory/GLOBAL-REGULATORY-REGISTER.md)
- Web Application Security (Chapter 05, draft baseline and lab specifications)
- API and Service Security (Chapter 06, draft baseline and lab specifications)
- Identity and Access Security (Chapter 07, this chapter)

## 29. References

1. NIST SP 800-63-4, Digital Identity Guidelines, July 2025: https://csrc.nist.gov/pubs/sp/800/63/4/final
2. NIST SP 800-63A-4, Identity Proofing and Enrollment, July 2025: https://csrc.nist.gov/pubs/sp/800/63/A/4/final
3. NIST SP 800-63B-4, Authentication and Authenticator Management, July 2025: https://csrc.nist.gov/pubs/sp/800/63/B/4/final
4. NIST SP 800-63C-4, Federation and Assertions, July 2025: https://csrc.nist.gov/pubs/sp/800/63/C/4/final
5. NIST SP 800-207, Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
6. IETF RFC 9700, OAuth 2.0 Security Best Current Practice, January 2025: https://www.rfc-editor.org/rfc/rfc9700.html
7. OpenID Connect Core 1.0 incorporating errata set 2: https://openid.net/specs/openid-connect-core-1_0.html
8. IETF RFC 9449, OAuth 2.0 Demonstrating Proof of Possession (DPoP): https://www.rfc-editor.org/rfc/rfc9449.html
9. IETF RFC 7644, SCIM Protocol: https://www.rfc-editor.org/rfc/rfc7644.html
10. W3C Web Authentication Level 3, Recommendation 25 August 2026: https://www.w3.org/TR/webauthn-3/
11. OWASP Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
12. OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
13. OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
14. OWASP Multifactor Authentication Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
15. OWASP OAuth 2.0 Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html
16. OWASP JSON Web Token Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html
17. MITRE CWE: https://cwe.mitre.org/
18. ISO/IEC 27001:2022 and ISO/IEC 27002:2022 catalogues: https://www.iso.org/standards.html

## 30. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial identity and access security engineering playbook |
