# Mobile Application Security Engineering Playbook

| Field | Value |
|---|---|
| Document ID | UAPPSEC-09-001 |
| Status | Draft engineering baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Android, iOS, hybrid applications, mobile client/backend trust, mobile assessment and release assurance |
| Classification | Public |

## 1. Executive summary

Mobile applications operate in an environment where the client device is not a trusted execution environment from the application's perspective. The device owner can inspect application packages, observe runtime behavior, control network conditions, install instrumentation, modify local state, invoke exported interfaces, restore backups and operate the application on a compromised or modified OS. The application must therefore treat the mobile client as an untrusted presentation and execution endpoint, not as the authority for identity, entitlement, transaction approval or data ownership.

Mobile security is not simply web security inside a smaller screen. The attack surface includes:
- Android APK/AAB packaging, manifest declarations, exported components, intents, content providers, services, receivers, permissions, Binder IPC and application sandbox.
- iOS IPA packaging, entitlements, URL schemes, Universal Links, app extensions, Keychain access groups, App Groups, pasteboard and inter-process communication.
- Local databases, preferences, files, caches, logs, screenshots, clipboard, backups and temporary files.
- Device-bound credentials, tokens, cryptographic keys, biometrics and platform keystore/keychain services.
- Network stack, TLS validation, certificate pinning decisions, proxy behavior and API integration.
- WebViews, JavaScript bridges, deep links, custom URL schemes and embedded browser authentication.
- Native libraries, dynamic loading, reflection, serialization and third-party SDKs.
- Application lifecycle, background tasks, notifications, widgets, extensions and share sheets.
- Reverse engineering, tampering, runtime instrumentation and repackaging.
- Backend APIs, OAuth/OIDC, device registration, session management, authorization and fraud controls.

The engineering objective is to minimize sensitive data and authority on the device, enforce security-critical decisions server-side, use platform security services correctly, make IPC and navigation boundaries explicit, verify release artifacts and monitor abuse without assuming anti-tamper controls make a compromised device trustworthy.

## 2. Scope and applicability

This playbook applies to:
- Native Android applications written in Kotlin or Java.
- Native iOS applications written in Swift or Objective-C.
- Cross-platform applications built with Flutter, React Native, .NET MAUI, Kotlin Multiplatform or similar frameworks.
- Hybrid applications using WebView or embedded browser components.
- Mobile SDKs, libraries, frameworks and third-party integrations.
- Companion apps, authenticator apps, enterprise apps and field-service applications.
- Mobile apps that access financial, identity, healthcare, enterprise, industrial or personal information.
- Backend services and APIs specifically consumed by mobile applications.

Out of scope for this chapter as primary subjects: mobile device management policy design, mobile operating system kernel exploitation, cellular baseband security and physical device hardware attack research. These may be dependencies or specialist assessments.

## 3. Threat model and trust boundaries

### 3.1 Adversary assumptions

Assume an attacker may:
- Own or control the device on which the app runs.
- Decompile and inspect the app package and resources.
- Modify local preferences, databases, files and application state.
- Hook application methods and observe runtime parameters.
- Intercept traffic through a local proxy where trust configuration permits.
- Invoke exported components, deep links, URL schemes and app extensions.
- Install malicious applications that target exposed IPC or shared resources.
- Replay requests and manipulate client-supplied identifiers, flags and prices.
- Use rooted/jailbroken devices, emulators, debuggers and dynamic instrumentation.
- Abuse a legitimate user's stolen credentials or session.
- Exploit weak backend authorization even if the mobile app appears secure.

Do not assume all users are malicious. The model must also cover lost devices, accidental disclosure, compromised SDKs, malicious accessibility overlays, supply-chain compromise and insecure operational configuration.

### 3.2 Trust boundaries

~~~mermaid
flowchart TD
    USER[User / Attacker] --> DEVICE[Mobile device and OS]
    DEVICE --> APP[Mobile application process]
    APP --> LOCAL[Local data stores / KeyStore / Keychain]
    APP --> IPC[OS components / Other apps / Extensions]
    APP --> NET[TLS / Network boundary]
    NET --> EDGE[API gateway / WAF]
    EDGE --> IDP[Identity provider]
    EDGE --> API[Backend API services]
    API --> DB[(Authoritative data stores)]
    API --> THIRD[Third-party services / SDK backends]
    APP --> WEB[WebView / Embedded browser]
    WEB --> NET
    SDK[Third-party SDKs] --> APP
~~~

The diagram is conceptual. A production threat model must identify actual process boundaries, signing identities, entitlements, exported components, API hosts, data stores, SDK destinations, tenant boundaries and device-management assumptions.

### 3.3 Trust rules

1. The device is not an authority for account ownership, price, role, entitlement, approval, transaction status or tenant identity.
2. Client-side validation improves user experience but is not a substitute for server-side validation.
3. Local storage is potentially observable on compromised devices and through backup, logs, instrumentation or app sharing paths.
4. Secrets embedded in APK/IPA files can be extracted. Obfuscation changes effort, not the trust boundary.
5. Biometrics authenticate a local user to a platform-protected operation; they do not automatically establish a server-side identity or transaction authorization.
6. Device integrity signals are risk signals, not proof of safety.
7. TLS protects a transport channel; it does not make the API's business logic or authorization correct.
8. A mobile application must not be the sole enforcement point for any security-critical rule.

## 4. Mobile security architecture

### 4.1 Architecture review inputs

Collect:
- Application IDs, bundle IDs, signing identities and distribution channels.
- Minimum and target OS versions and supported device classes.
- Framework/runtime and native dependency versions.
- Application entry points, exported components, URL routes and app extensions.
- Permissions, entitlements and privacy declarations.
- Data inventory, sensitivity and lifecycle.
- Local storage locations and backup behavior.
- Authentication, session and device registration design.
- API inventory and authorization model.
- SDK inventory and network destinations.
- Build pipeline, signing, provisioning and release process.
- Root/jailbreak and device integrity assumptions.
- Logging, crash reporting, analytics and support processes.

### 4.2 Mobile architecture requirements

- Keep business authorization and transaction decisions on trusted backend services.
- Use platform APIs for secure credential and key storage.
- Minimize persistent secrets and sensitive data on the device.
- Separate authentication tokens from general preferences and analytics.
- Use short-lived access tokens and controlled refresh-token lifecycle.
- Bind sensitive operations to server-side authorization and transaction state.
- Make app-to-app communication explicit and narrow.
- Restrict WebView navigation and JavaScript bridges.
- Validate all deep link and intent inputs.
- Use secure defaults for permissions, network security and exported components.
- Keep development-only trust overrides out of release artifacts.
- Protect signing keys and release credentials outside developer workstations where feasible.
- Verify final signed artifacts, not only source code.

## 5. Android security engineering

### 5.1 Application sandbox and process identity

Android applications normally run under distinct Linux UIDs and an OS-enforced application sandbox. Do not treat language/runtime isolation as the security boundary. Native code within the same app process shares the app's process authority. Avoid shared UIDs and privileged permissions unless a documented platform requirement exists.

Review:
- Application UID and shared process declarations.
- Debuggable and test-only build settings.
- App data directory permissions and backup behavior.
- Native libraries and JNI boundaries.
- Inter-process communication exposure.
- Runtime permissions and special app access.
- Device compatibility and minimum OS decisions.

### 5.2 AndroidManifest.xml review

Review each manifest declaration, including merged manifests contributed by libraries.

Important attributes and elements include:
- \`android:exported\` for activities, services and receivers.
- Intent filters and action/category/data matching.
- \`android:permission\` and permission protection levels.
- \`android:debuggable\`.
- \`android:allowBackup\` and data extraction/backup rules.
- \`android:usesCleartextTraffic\`.
- \`android:networkSecurityConfig\`.
- \`android:sharedUserId\` where legacy use remains.
- \`android:taskAffinity\`, launch modes and document/task behavior.
- \`android:grantUriPermissions\`.
- \`android:readPermission\` and \`android:writePermission\`.
- SDK version and component compatibility behavior.

Do not use a blanket manifest checklist without checking effective merged manifest, target SDK behavior and platform version.

### 5.3 Exported components and IPC

Activities, services, broadcast receivers and content providers may be reachable by other apps if exported or otherwise exposed. For each component:
1. Identify whether external access is required.
2. Set exported state explicitly where applicable.
3. Require the narrowest suitable permission.
4. Validate caller identity and authorization where sensitive operations are exposed.
5. Validate all intent extras, URIs, MIME types and serialized objects.
6. Avoid relying on package name supplied by the caller as proof of identity.
7. Prevent arbitrary file paths and URI traversal.
8. Restrict content provider query, insert, update, delete and file-open operations.
9. Apply URI grants with narrow scope and duration.
10. Test from a separate untrusted test app.

Use signature-level permissions for trusted apps under the same signing authority when that is the correct design. A normal permission is not equivalent to a signature permission.

### 5.4 Intent and PendingIntent security

- Validate action, component, data URI, categories and extras.
- Prefer explicit intents for sensitive internal component invocation.
- Do not pass bearer tokens, private data or privileged commands in broadly accessible broadcasts.
- Use immutable PendingIntents unless mutability is explicitly required.
- When mutable PendingIntents are necessary, constrain the target and fill-in behavior.
- Use unique request codes and appropriate identity semantics.
- Prevent intent redirection by validating destination components and data.
- Do not assume an intent originated from a trusted app because its action string looks familiar.

### 5.5 Content providers and URI permissions

- Set export state deliberately.
- Enforce read/write permissions separately.
- Use narrow URI grants.
- Validate path segments and query parameters.
- Prevent arbitrary file access and path traversal.
- Avoid exposing raw filesystem paths.
- Check file descriptor modes and MIME types.
- Test query, insert, update, delete and openFile paths independently.
- Confirm grant revocation and lifecycle behavior.

### 5.6 Android permissions

- Request only permissions needed for a user-visible feature.
- Request at point of use where appropriate.
- Handle denial and revocation safely.
- Avoid requesting broad storage, location, contacts, camera or microphone access where a scoped platform picker/API is sufficient.
- Review background location and notification access separately.
- Do not infer consent or authorization from a permission grant.
- Review special permissions and role APIs.
- Explain sensitive permission use in product UX and privacy notices.

### 5.7 Android local storage

Review:
- Internal app-private files.
- Shared/external storage.
- SharedPreferences and DataStore.
- SQLite/Room databases.
- Cache and temporary files.
- WebView cookies, local storage and caches.
- Download directories and media collections.
- Logs, crash reports and analytics events.
- Clipboard and screenshots.
- Backup and device transfer.
- Files exposed through FileProvider or content providers.

Controls:
- Keep sensitive information in app-private storage where possible.
- Encrypt sensitive fields when the threat model requires it, with keys protected by Android Keystore.
- Do not store access tokens or passwords in plaintext preferences.
- Avoid sensitive content in external/shared storage.
- Use scoped storage and Storage Access Framework appropriately.
- Exclude secrets and sensitive data from backups unless a designed protected restore mechanism exists.
- Delete temporary data and caches on lifecycle events where appropriate.
- Avoid storing full identity documents or payment credentials when a token/reference suffices.

### 5.8 Android Keystore

Use Android Keystore for cryptographic key generation and operations where suitable. Keys can be non-exportable and, on supported devices/configurations, hardware-backed or StrongBox-backed.

Review:
- Key purpose, algorithm, mode, padding and digest restrictions.
- User authentication requirements and validity duration.
- Hardware backing and attestation assumptions.
- Key invalidation behavior after lock-screen changes or biometric enrollment changes.
- Backup/restore and device migration behavior.
- Key alias naming, rotation and deletion.
- Whether app code exports key material through unsafe wrappers.
- Fallback behavior on devices without the desired hardware security feature.

Do not assume every Android device supports StrongBox or that hardware-backed key storage protects plaintext while the app process is compromised.

### 5.9 Android network security

- Enforce HTTPS for production endpoints.
- Disable cleartext traffic unless a narrow, documented exception is necessary.
- Use Network Security Configuration for trust and cleartext policy where appropriate.
- Validate certificate chains and hostnames.
- Keep user-installed debug trust anchors limited to debug builds.
- Do not implement permissive TrustManagers or HostnameVerifiers.
- Do not silently fall back to HTTP.
- Review proxy behavior and certificate pinning design.
- Verify redirects cannot downgrade or leak credentials.
- Ensure WebView and native HTTP clients follow compatible policies.

Certificate pinning is a risk-based defense-in-depth control. It creates certificate/key rotation and availability risks; it must have a documented pin lifecycle, backup pins where appropriate, release process and recovery plan. Pinning does not replace normal certificate validation or server-side controls.

### 5.10 Android WebView

- Disable JavaScript unless required.
- Restrict navigation to an explicit allowlist.
- Validate scheme, host, port and path, not substring matches.
- Do not load untrusted content in a privileged WebView.
- Avoid JavaScript interfaces for untrusted origins.
- Expose the minimum bridge methods and validate every argument.
- Avoid file access and universal file URL access unless a reviewed use case requires it.
- Handle SSL errors by cancelling; never instruct users to proceed through invalid certificates.
- Review mixed content, content access, cookies and DOM storage.
- Use safe browsing support where available.
- Prevent external content from invoking privileged native functionality.
- Separate authenticated first-party content from arbitrary browsing.

### 5.11 Android deep links and App Links

- Declare supported routes narrowly.
- Use verified App Links for domain association where appropriate.
- Validate all route parameters and identifiers.
- Require server-side authorization after navigation.
- Prevent open redirects and unsafe WebView destinations.
- Do not embed secrets in link URLs.
- Define behavior when app is not installed, domain verification fails or a link is malformed.
- Test link handling with malicious schemes, duplicate parameters, encoded separators and unexpected hosts.

### 5.12 Android code and package hardening

- Remove debug code, test endpoints and verbose logging from release builds.
- Review R8/ProGuard configuration and keep rules.
- Avoid insecure dynamic code loading.
- Verify downloaded modules or code with authenticated provenance and integrity before execution.
- Review JNI/native libraries for memory safety and unsafe parsing.
- Use compiler and platform hardening features supported by the toolchain.
- Maintain dependency inventory and patch process.
- Do not embed reusable service credentials, private signing keys or backend secrets in the package.

## 6. iOS security engineering

### 6.1 iOS sandbox and code signing

iOS applications run under platform sandboxing and code-signing controls. Review:
- Bundle identifier and signing team.
- Entitlements and provisioning profile.
- App container and shared container access.
- App extensions and associated processes.
- Debug/development distribution settings.
- Keychain access groups.
- Associated Domains.
- URL schemes and document types.
- Network and privacy permissions.
- Dynamic frameworks and embedded libraries.

The signed app's effective entitlements must be inspected in the distributed artifact. Source project settings alone are not sufficient evidence.

### 6.2 iOS entitlements

Review each entitlement for necessity and scope, including:
- Keychain access groups.
- App Groups.
- Associated Domains.
- Push Notifications.
- iCloud containers and key-value storage.
- Network extensions and VPN-related entitlements.
- Data protection and managed capabilities.
- Background modes.
- Sign in with Apple and authentication capabilities.
- Shared web credentials where used.

Unexpected entitlements expand application authority. Compare release entitlements against an approved baseline and investigate additions.

### 6.3 Keychain services

Use Keychain Services for credentials, tokens and small secrets. Choose accessibility class based on the required device state and access lifecycle, not convenience alone.

Review:
- \`kSecAttrAccessible\` selection.
- \`WhenUnlocked\`, \`AfterFirstUnlock\` and \`ThisDeviceOnly\` semantics as applicable.
- Access control flags and user-presence/biometric requirements.
- Access groups and app sharing.
- Synchronization/iCloud Keychain behavior.
- Backup and migration behavior.
- Keychain item update/delete lifecycle.
- Error handling and fallback paths.

Avoid storing secrets in UserDefaults, plist files, ordinary SQLite rows or app bundle resources. Keychain use is not a complete authorization model: the app must still validate account/session state with the backend.

### 6.4 Secure Enclave and CryptoKit

Use Secure Enclave-backed key operations when supported and appropriate to the use case. The Secure Enclave is not a general-purpose storage location for arbitrary application data. It protects supported private-key operations and hardware-bound secrets.

Review:
- Key type and supported algorithm.
- Access control and user-presence policy.
- Device compatibility and fallback.
- Key backup/migration limitations.
- Enrollment changes and invalidation.
- Server registration and public-key binding.
- Recovery and revocation.
- Whether a private key operation actually authorizes the intended transaction.

Use platform cryptographic APIs and maintained libraries. Do not invent custom cryptography.

### 6.5 iOS Data Protection

Review file protection class and data availability while the device is locked. Sensitive files should use an appropriate Data Protection class based on background access requirements and threat model. Verify:
- Protection attributes on created files.
- Temporary file handling.
- Database and WAL/journal files.
- Downloads and document exports.
- App Group shared files.
- Backup behavior.
- Crash recovery and background tasks.

Do not assume a file is protected merely because it resides inside the app sandbox.

### 6.6 iOS URL schemes and Universal Links

- Register only required custom URL schemes.
- Validate scheme, host, path and parameters.
- Prefer Universal Links for verified domain association where appropriate.
- Treat all incoming URLs as attacker-controlled.
- Avoid embedding tokens or personal data in URLs.
- Require server-side authorization after navigation.
- Prevent route confusion and open redirects.
- Test multiple apps claiming the same custom scheme.
- Test malformed, encoded, duplicate and oversized parameters.
- Review associated domain entitlements and apple-app-site-association behavior.

### 6.7 iOS pasteboard, screenshots and app switching

- Avoid placing secrets or authentication tokens on the general pasteboard.
- Use local-only/expiration options where supported and appropriate.
- Consider screenshots and app switcher snapshots when sensitive screens background.
- Redact or hide highly sensitive content during app transition snapshots where justified.
- Avoid exposing sensitive content in notification previews.
- Do not treat screenshot blocking as a complete data loss prevention control.
- Define screen recording and external display behavior for sensitive workflows.

### 6.8 iOS App Extensions and shared containers

- Minimize data shared through App Groups.
- Restrict Keychain access groups.
- Validate data exchanged with extensions.
- Treat extension inputs and shared files as untrusted.
- Avoid broad shared-container access.
- Review extension lifecycle and authentication assumptions.
- Test stale data, concurrent access and privilege confusion.
- Ensure deletion and logout propagate across app and extensions.

### 6.9 iOS App Transport Security and networking

- Preserve App Transport Security defaults unless a documented exception is necessary.
- Avoid broad ATS exceptions.
- Validate server identity and certificate chain.
- Review custom URLSession delegates and trust evaluation.
- Ensure invalid certificates fail closed.
- Review redirect handling and credential forwarding.
- Test TLS configuration and certificate renewal.
- Document pinning, if used, with rotation and recovery strategy.

### 6.10 iOS WebKit

- Restrict navigation and message handlers.
- Validate origins and message payloads.
- Do not expose privileged native handlers to arbitrary web content.
- Review cookie sharing and persistent website data.
- Prevent arbitrary file URL access.
- Use secure authentication flows and external user agents where appropriate.
- Handle universal link navigation and callback validation.
- Review content process termination and state restoration behavior.

## 7. Cross-platform and hybrid frameworks

### 7.1 General requirements

Cross-platform frameworks do not remove native platform security responsibilities. Review generated manifests, entitlements, plugins, native modules, platform channels, bridge interfaces and package dependencies.

For each framework:
- Identify native code and plugin boundary.
- Review plugin permissions and exported components.
- Check secure storage plugin implementation and platform configuration.
- Inspect build-time and runtime configuration separation.
- Ensure secrets are not bundled in JavaScript/Dart assets or configuration.
- Review deep link and navigation handlers.
- Test WebView or browser components independently.
- Verify release minification/obfuscation does not remove security checks or create unsafe reflection behavior.
- Keep framework, runtime and plugin versions supported and patched.

### 7.2 React Native

Review:
- JavaScript bundle and source map exposure.
- Native module bridge surface.
- AsyncStorage and other local persistence.
- Secure storage library implementation and Keychain/Keystore configuration.
- Deep link event handling.
- WebView origin allowlists and message bridges.
- Debugging and developer menu availability in release builds.
- OTA update signature, integrity, rollback and authorization.
- Hermes/JS engine and native dependency versions.
- Secrets accidentally bundled into JS constants or build-time variables.

### 7.3 Flutter

Review:
- Dart AOT/release configuration and debug artifacts.
- Platform channels and method-call authorization.
- Plugin code and permissions.
- SharedPreferences versus secure storage choices.
- Deep link handling and route validation.
- WebView plugin settings and JavaScript bridges.
- Native Android/iOS configuration generated by Flutter build.
- Crash reporting and analytics.
- Obfuscation symbols and artifact handling.
- Runtime update and asset delivery mechanisms.

### 7.4 .NET MAUI and other frameworks

Review platform-specific storage APIs, SecureStorage implementation, WebView settings, permissions, platform handlers, deep links, signing, trimming/linking, native dependency versions and release configuration. Verify platform security semantics rather than assuming a cross-platform abstraction provides identical guarantees on every OS.

## 8. Mobile authentication and session management

### 8.1 Authentication architecture

- Prefer OAuth 2.0 Authorization Code flow with PKCE for native public clients when using an external identity provider.
- Use an external system browser or platform authentication session rather than an embedded WebView for federated login where applicable.
- Validate redirect URI and state; use nonce where required by the identity protocol.
- Treat mobile applications as public clients; do not embed a client secret and call it confidential.
- Use platform-backed secure storage for refresh credentials where appropriate.
- Keep access tokens short-lived based on risk and operational requirements.
- Rotate refresh tokens and detect reuse where supported by the identity platform.
- Revoke sessions on logout, account compromise and device loss.
- Do not trust local role claims without server-side authorization and current policy.
- Protect account recovery and device re-enrollment.

### 8.2 Biometric authentication

Biometrics can unlock a local key or authorize a local user-presence check. They do not automatically prove the user to a remote server.

Review:
- Whether the biometric operation is OS-mediated.
- Whether key use is bound to biometric/user presence.
- Enrollment change and fallback behavior.
- Device passcode fallback.
- Lockout and retry semantics.
- Transaction binding and server challenge design.
- Session expiry and revocation.
- Accessibility and recovery.
- Risk of treating a Boolean local flag as proof of authentication.

### 8.3 Device binding and attestation

Device registration and attestation may add risk signals, but do not turn the device into a trusted authority. Define:
- What identity is being attested (app, device, key or environment).
- Issuer and validation chain.
- Challenge freshness and replay resistance.
- Backend verification and failure behavior.
- Device replacement and recovery.
- Privacy impact and data minimization.
- False-positive and false-negative handling.
- Fallback for unsupported devices.
- Abuse response and revocation.

Do not hard-code a trust decision solely on a client-reported “rooted = false” value.

## 9. Mobile API and transaction security

- Enforce authorization on every API operation and object.
- Treat all identifiers, role flags, account IDs and transaction values from the client as untrusted.
- Validate transaction state transitions server-side.
- Bind approvals to transaction details, not only a generic login session.
- Apply replay protection and idempotency for sensitive operations.
- Rate-limit login, OTP, recovery, payment and high-cost operations.
- Detect device/session anomalies without relying on one signal.
- Ensure logout and token revocation are enforced by backend services.
- Avoid placing access tokens in URL parameters, logs or analytics.
- Restrict API responses to necessary fields.
- Test object-, property-, function- and tenant-level authorization.
- Verify the backend cannot be accessed with a mobile API key alone where that key is public in the package.

## 10. Privacy and mobile data protection

Review all collection and disclosure paths:
- Runtime permissions and OS privacy indicators.
- Analytics and crash reporting SDKs.
- Advertising identifiers and tracking.
- Location, contacts, photos, microphone and camera.
- Clipboard and keyboard interactions.
- Notifications and lock-screen previews.
- Local and cloud backups.
- App Store/Play disclosures and privacy labels.
- Data export and account deletion.
- Third-party SDK destinations and sub-processors.

Minimize data collection, disclose purposes, apply appropriate legal basis/consent requirements and propagate retention/deletion to backend and processor systems. A mobile OS permission is not automatically a legal basis for all subsequent processing.

## 11. Third-party SDK and mobile supply-chain security

Maintain a software bill of materials or equivalent dependency inventory for:
- Native libraries and frameworks.
- CocoaPods, Swift Package Manager and Gradle/Maven dependencies.
- Flutter/Dart packages.
- npm/JavaScript packages.
- Analytics, advertising, attribution and crash SDKs.
- Authentication, payment, maps and messaging SDKs.
- OTA update and feature-flag providers.

Assess:
- Publisher and provenance.
- Version and support status.
- Known vulnerabilities.
- Transitive dependencies.
- Data collection and network destinations.
- Permissions and entitlements introduced.
- Native code and runtime behavior.
- License and redistribution requirements.
- Update and incident notification practices.

Do not assume a vendor SDK is safe because it is widely used. Pin versions where appropriate, monitor advisories and review manifest/entitlement changes after dependency updates.

## 12. Reverse engineering, tampering and resilience

### 12.1 Threat and defensive posture

Attackers can inspect and modify mobile packages and runtime state. Obfuscation, anti-debugging, root/jailbreak detection, integrity checks and certificate pinning can raise attacker cost or provide risk signals, but are bypassable and must not replace server-side controls.

### 12.2 Defensive controls

- Remove debug symbols and development interfaces from production artifacts where appropriate.
- Obfuscate sensitive code paths where justified.
- Detect unexpected package/signature changes as a risk signal.
- Protect critical operations with server-side authorization.
- Use platform integrity/attestation services as one signal in a layered decision.
- Detect suspicious instrumentation or runtime modifications where proportionate.
- Avoid destructive behavior or bricking devices based solely on a heuristic.
- Monitor abnormal transaction patterns server-side.
- Define response for false positives and unsupported devices.
- Keep emergency disable and recovery paths.

### 12.3 Root/jailbreak detection

- Define the risk scenario detection is intended to reduce.
- Use multiple signals rather than one filesystem path or package name.
- Expect bypass, spoofing and OS-version variation.
- Avoid collecting unrelated device data.
- Do not rely on detection for authorization.
- Apply proportional step-up or transaction restrictions.
- Ensure legitimate accessibility, testing and enterprise-managed scenarios are not silently broken.
- Record false-positive rates and review decisions.

### 12.4 Runtime instrumentation and dynamic analysis

Authorized assessment may use debuggers, emulators, runtime instrumentation and method tracing to understand application behavior. Testing must remain within the approved test device, application build and backend scope. Do not deploy instrumentation to third-party devices or intercept accounts without authorization.

## 13. Build, signing and release security

### 13.1 Build pipeline

- Use protected source control and reviewed changes.
- Protect CI runner identities and secrets.
- Pin dependencies and verify package provenance.
- Separate debug, QA, staging and production configuration.
- Generate signed artifacts in controlled build infrastructure.
- Protect Android signing keys and Apple signing credentials.
- Restrict signing access and record release approvals.
- Produce artifact hashes and provenance.
- Scan dependencies and native binaries.
- Inspect final APK/AAB/IPA and effective manifest/entitlements.
- Preserve build logs and release evidence.
- Verify distribution channel and version mapping.

### 13.2 Android release checks

- Release build is not debuggable.
- No test endpoints, debug trust anchors or verbose sensitive logs.
- Effective merged manifest reviewed.
- Exported component inventory approved.
- Cleartext traffic disabled or narrowly justified.
- Backup/data extraction rules reviewed.
- APK/AAB signature and signing configuration verified.
- Dependencies and native libraries inventoried.
- Play Integrity use, if any, is server-verified and threat-modelled.
- Version code, target SDK and supported OS are recorded.

### 13.3 iOS release checks

- Distribution certificate and provisioning profile valid and expected.
- Effective entitlements match approved baseline.
- Debugger/development capabilities absent where inappropriate.
- URL schemes and associated domains reviewed.
- ATS exceptions documented.
- Keychain groups and App Groups minimized.
- Embedded frameworks and privacy manifests reviewed as applicable.
- App privacy disclosures match actual SDK behavior.
- Archive and IPA hashes recorded.
- Notarization/distribution requirements are met for the relevant channel.

## 14. Mobile application security testing methodology

### 14.1 Rules of engagement

- Obtain written authorization for application, backend, accounts, devices and test windows.
- Confirm whether testing includes rooted/jailbroken devices, emulators, production APIs or payment flows.
- Use dedicated test accounts and synthetic data.
- Define rate limits and prohibited destructive actions.
- Do not bypass production controls or access real user data beyond explicit scope.
- Protect signing materials and test credentials.
- Record app version, OS version, device model, install source and network configuration.
- Keep evidence sanitized and encrypted.
- Agree stop conditions and escalation contacts.

### 14.2 Assessment phases

1. Scope, application identification and threat model.
2. Package acquisition and integrity verification.
3. Static package and manifest/entitlement analysis.
4. Source review where available.
5. Dependency and SDK inventory.
6. Local storage and backup analysis.
7. Cryptography and key storage review.
8. Authentication and session testing.
9. Network and TLS testing.
10. IPC, intents, deep links and app extension testing.
11. WebView and native bridge testing.
12. Runtime behavior and instrumentation-assisted analysis.
13. Backend/API authorization and business logic testing.
14. Privacy and data disclosure review.
15. Resilience and integrity signal assessment.
16. Release pipeline and signing review.
17. Evidence, severity, remediation and regression.

### 14.3 Static analysis

Static review should inspect:
- APK/AAB/DEX, manifest, resources and native libraries.
- IPA, Info.plist, entitlements, provisioning metadata and frameworks.
- Hardcoded secrets, endpoints and feature flags.
- Insecure storage APIs and cryptographic patterns.
- Exported components and URL handling.
- WebView settings and bridge exposure.
- Debug flags, logging and test code.
- Dependency versions and SDK declarations.
- Obfuscation and symbol leakage.
- Native code memory safety and unsafe parsing.

Static findings require runtime or configuration validation where behavior depends on OS version, server policy or deployment configuration.

### 14.4 Dynamic analysis

Dynamic review should inspect:
- Application startup and lifecycle.
- Authentication, logout, recovery and token refresh.
- Local storage before and after sensitive workflows.
- Network requests, redirects and error paths.
- Deep links, intents and app-to-app handoff.
- WebView navigation and JavaScript bridge behavior.
- Backgrounding, screenshots, notifications and clipboard.
- Permission grant/deny/revoke behavior.
- Offline mode and reconnection.
- Device integrity signal behavior.
- Runtime exception and crash handling.

### 14.5 Backend-aware mobile testing

A mobile assessment is incomplete if it only tests the client. Validate:
- Server-side authorization.
- Token validation, audience, issuer and expiry.
- Device registration and session revocation.
- Object/property/function authorization.
- Tenant isolation.
- Replay, idempotency and race conditions.
- Rate limiting and abuse prevention.
- Transaction binding.
- API response minimization.
- Business logic and workflow state.

## 15. Test catalogue

The following IDs are internal project test identifiers, not official MASTG IDs.

| Test ID | Area | Procedure focus | Expected result |
|---|---|---|---|
| MOB-T-001 | Package inventory | Identify package, version, signing identity and dependencies | Artifact is attributable and inventoried |
| MOB-T-002 | Android manifest | Inspect merged manifest and exported components | No unintended exposure; permissions justified |
| MOB-T-003 | iOS entitlements | Compare release entitlements to approved baseline | Only necessary capabilities present |
| MOB-T-004 | Debug configuration | Inspect release flags, debug endpoints and trust overrides | No production debug behavior |
| MOB-T-005 | Local storage | Exercise sensitive workflows and inspect app files/preferences/DB | Secrets and sensitive data protected appropriately |
| MOB-T-006 | Backup | Inspect Android/iOS backup and restore behavior | Sensitive data excluded or protected by design |
| MOB-T-007 | Logs | Trigger auth/error flows and inspect logs/crash telemetry | No secrets or unnecessary personal data |
| MOB-T-008 | Clipboard/screenshots | Exercise sensitive screens, copy and background app | Disclosure is minimized and policy matches risk |
| MOB-T-009 | Android Keystore | Review key generation, access, invalidation and backup | Keys are appropriately protected and lifecycle-defined |
| MOB-T-010 | iOS Keychain | Review accessibility, access groups and item lifecycle | Secrets use suitable Keychain protection |
| MOB-T-011 | Crypto usage | Inspect algorithms, nonce/IV, authentication and error paths | Standard cryptography used correctly |
| MOB-T-012 | TLS validation | Test valid, invalid, expired and wrong-host certificates | Invalid server identity fails closed |
| MOB-T-013 | Cleartext | Inspect app traffic and config | No unintended cleartext traffic |
| MOB-T-014 | Pinning | Review pinning, rotation, fallback and recovery | Pinning does not disable PKI validation or create unmanaged outage risk |
| MOB-T-015 | Deep links | Send malformed, encoded and unauthorized route inputs | Inputs validated; server authorization enforced |
| MOB-T-016 | Android IPC | Test exported activities/services/receivers/providers from test app | Only intended callers can invoke sensitive operations |
| MOB-T-017 | PendingIntent | Review mutability, target and fill-in behavior | No unintended intent substitution |
| MOB-T-018 | iOS URL schemes | Invoke custom schemes and Universal Links with hostile parameters | Route and parameters validated |
| MOB-T-019 | App extensions | Test shared containers and extension inputs | Shared data access is narrow and validated |
| MOB-T-020 | WebView | Test untrusted navigation, JS bridge, file access and SSL errors | No untrusted content gains privileged native access |
| MOB-T-021 | Authentication | Test login, recovery, MFA and federated callback | Secure protocol flow and correct identity binding |
| MOB-T-022 | Token lifecycle | Inspect access/refresh token storage, rotation and revocation | Tokens protected, rotated and revocable |
| MOB-T-023 | Biometric | Test enrollment changes, fallback and key gating | Local biometric state is not treated as remote identity proof |
| MOB-T-024 | Backend authorization | Manipulate object, role and tenant identifiers | Server rejects unauthorized operations |
| MOB-T-025 | Replay/idempotency | Repeat sensitive synthetic transaction requests | Replay and duplicate processing controlled |
| MOB-T-026 | Permissions/privacy | Deny/revoke permissions and inspect data collection | App degrades safely and minimizes collection |
| MOB-T-027 | SDK inventory | Inspect dependencies, permissions and network destinations | Third-party data flows are known and approved |
| MOB-T-028 | Root/jailbreak signals | Compare supported and modified lab devices | Signals are proportionate and not sole authorization |
| MOB-T-029 | Tampering | Compare modified test artifact and integrity response | Detection is risk signal; backend remains authoritative |
| MOB-T-030 | Signing/release | Verify signature, artifact hash, build provenance and release config | Artifact is authentic and traceable |
| MOB-T-031 | Update mechanism | Test update signature, rollback and configuration | Only authorized updates/configuration accepted |
| MOB-T-032 | Notifications | Inspect lock-screen previews and notification payloads | Sensitive content is minimized |
| MOB-T-033 | Offline mode | Modify local state and reconnect | Server reconciles authoritative state safely |
| MOB-T-034 | Session lifecycle | Background, restore, logout and device-loss scenarios | Session policy is enforced consistently |
| MOB-T-035 | Privacy disclosure | Compare actual SDK/data collection with published disclosures | Disclosures accurately reflect processing |

## 16. Monitoring and detection engineering

| Detection ID | Scenario | Signals | Response |
|---|---|---|---|
| MOB-D-001 | Credential/session abuse | New device, unusual refresh, token reuse or impossible workflow | Revoke/step-up and investigate |
| MOB-D-002 | Automated transaction abuse | High-rate or repeated sensitive actions | Rate-limit, challenge and review |
| MOB-D-003 | Device integrity anomaly | Verified attestation failure or risk signal | Apply proportionate policy, not automatic universal denial |
| MOB-D-004 | App version abuse | Unsupported or vulnerable app versions | Restrict high-risk actions and prompt update |
| MOB-D-005 | API authorization anomalies | Cross-tenant/object access attempts | Investigate backend policy and account |
| MOB-D-006 | Token replay | Repeated refresh/token use from inconsistent contexts | Revoke token family and investigate |
| MOB-D-007 | Suspicious deep-link flow | Unexpected route, malformed callback or redirect pattern | Reject route and inspect client/backend |
| MOB-D-008 | Sensitive export | Unusual downloads or bulk data access | Verify purpose and contain if unauthorized |
| MOB-D-009 | SDK egress drift | New network destination or unexpected data volume | Block/contain and review SDK change |
| MOB-D-010 | Release integrity | Artifact/signature/provenance mismatch | Stop distribution and invoke release incident |

Avoid collecting invasive device telemetry without a documented need, privacy review and retention limit.

## 17. Common mobile security failure patterns

1. Treating hidden buttons or client-side role checks as authorization.
2. Embedding backend secrets in app assets or native binaries.
3. Storing refresh tokens in ordinary preferences or unprotected files.
4. Assuming sandbox means local data cannot be extracted from a compromised device.
5. Exporting Android components without a clear caller/permission model.
6. Trusting intent extras, deep link parameters or URL schemes.
7. Exposing privileged native functions through a WebView JavaScript bridge.
8. Accepting all certificates in a custom trust manager.
9. Shipping development CA trust anchors in production.
10. Using a generic API key in the app as the only backend access control.
11. Treating biometric success as proof of a server-side identity.
12. Relying on root/jailbreak detection to protect business authorization.
13. Forgetting logs, screenshots, backups, crash reports and clipboard.
14. Trusting third-party SDKs without data-flow and dependency review.
15. Testing only the app UI and ignoring backend object/property authorization.
16. Failing to inspect merged manifests and final signed entitlements.
17. Applying certificate pinning without key rotation and emergency recovery.
18. Assuming an obfuscated binary cannot be reverse engineered.
19. Failing to propagate logout/deletion to extensions, caches and backend sessions.
20. Shipping update mechanisms without signature, provenance and rollback protection.

## 18. Mobile-specific architecture patterns

### 18.1 Secure token flow

~~~mermaid
sequenceDiagram
    participant U as User
    participant A as Native App
    participant B as System Browser / Auth Session
    participant I as Identity Provider
    participant S as Backend API
    U->>A: Start sign-in
    A->>A: Generate PKCE verifier/challenge and state
    A->>B: Open authorization request
    B->>I: Authorization Code + PKCE
    I->>B: Redirect with code and state
    B->>A: Verified callback
    A->>A: Validate state
    A->>I: Exchange code with verifier
    I->>A: Tokens
    A->>A: Store refresh credential securely
    A->>S: API request with access token
    S->>S: Validate issuer, audience, expiry and authorization
    S-->>A: Authorized response
~~~

The identity provider and backend must enforce protocol and resource authorization. The mobile client cannot keep a confidential OAuth client secret.

### 18.2 Device-bound key registration

~~~mermaid
sequenceDiagram
    participant A as Mobile App
    participant K as Platform Keystore / Keychain
    participant S as Backend
    A->>K: Generate device-bound key pair
    K-->>A: Public key / key reference
    A->>S: Register public key with authenticated challenge
    S->>S: Verify user, device policy and challenge
    S-->>A: Registration result
    A->>K: Sign fresh server challenge
    K-->>A: Signature
    A->>S: Signature + challenge identifier
    S->>S: Verify signature, freshness and account binding
~~~

This pattern requires replay protection, device lifecycle management, revocation, key invalidation and recovery. It does not prove that every action performed by the app is safe.

## 19. Tooling and assessment workbench

Choose tools based on authorized scope, platform version and reproducibility.

| Tool | Primary use | Important limitations |
|---|---|---|
| Android Studio / SDK tools | Build, manifest, emulator, logcat, platform inspection | Build tooling is not a complete security assessment |
| JADX | DEX decompilation and code review | Decompiled output can be incomplete or misleading |
| apktool | APK resources, manifest and smali inspection | Does not replace runtime validation |
| MobSF | Static/dynamic mobile assessment automation | Findings require manual validation; protect uploaded artifacts |
| Frida | Authorized runtime instrumentation and method observation | Requires controlled test environment and compatible device/app |
| Objection | Mobile runtime exploration built around Frida | Automation may not cover all app/platform behaviors |
| Burp Suite / OWASP ZAP | API and mobile traffic assessment | TLS pinning and app trust configuration may affect capture; never weaken production controls |
| mitmproxy | Controlled traffic inspection | Certificate trust must be configured safely in test devices |
| apksigner / bundletool | Android package/signature inspection | Validate correct artifact and signing lineage |
| adb | Android package, device and component interaction | Device access and OS behavior vary |
| Xcode / Instruments | iOS build, runtime and platform analysis | Requires suitable Apple tooling and authorized device setup |
| codesign / security / plutil | iOS signature, entitlement and metadata inspection | Interpret the final distributed artifact |
| otool / nm / strings | Native binary inspection | Output may include noise and stripped symbols |
| simctl | iOS Simulator management | Simulator does not reproduce all device hardware security behavior |
| SCA/SBOM tools | Dependency inventory and vulnerability monitoring | Package metadata can miss vendored/native components |

Tool versions, commands and exact test procedures should be pinned in the lab implementation records. Do not run untrusted binaries on production devices.

## 20. Industry scenarios

### 20.1 Banking and payment application

Threats include account takeover, transaction manipulation, overlay abuse, credential theft, API replay and sensitive data leakage.

Controls:
- Server-side transaction authorization and state validation.
- Step-up authentication for high-risk operations.
- Transaction-bound approval and anti-replay.
- Device/key registration with revocation and recovery.
- Tokenization and minimized local payment data.
- Risk-based integrity signals.
- Strong API authorization, rate limiting and fraud monitoring.
- Secure notification and lock-screen handling.

### 20.2 Enterprise field-service application

Threats include lost devices, offline data exposure, shared devices, privileged support access and stale offline authorization.

Controls:
- Minimize cached enterprise records.
- Use OS-supported device encryption and managed-device policies where appropriate.
- Enforce server-side role and tenant authorization.
- Define offline access duration and data expiry.
- Protect local database and attachments.
- Restrict screenshots/export where proportionate.
- Support remote session revocation and credential rotation.
- Test managed/unmanaged device differences.

### 20.3 Healthcare mobile application

Threats include disclosure through notifications, local records, analytics SDKs, shared devices and insecure exports.

Controls:
- Minimize patient data cached on device.
- Apply strong local access and session controls.
- Protect files with platform data protection.
- Restrict notification content.
- Validate access at the backend for every patient/resource.
- Assess processor SDKs and telemetry.
- Support data rights and deletion workflows.
- Align retention and breach response with applicable jurisdiction and sector law.

### 20.4 Industrial/OT companion application

Threats include unauthorized remote operation, exposure of engineering data, unsafe commands and compromised field devices.

Controls:
- Separate monitoring from command capability.
- Do not rely on a mobile client as the safety interlock.
- Require server-side authorization and command validation.
- Use explicit approvals for high-impact operations.
- Segment mobile access from control-system networks.
- Use secure gateways and monitored remote access.
- Log commands and operator identity with tamper-resistant audit.
- Apply operational safety review before any mobile-to-OT control path is introduced.

### 20.5 Consumer app with social and location features

Threats include excessive location collection, account enumeration, deep-link abuse, privacy leakage and SDK tracking.

Controls:
- Request location only when needed and use coarse location where sufficient.
- Validate link ownership and route access.
- Minimize analytics identifiers.
- Protect account recovery.
- Enforce object authorization for user content.
- Provide retention and deletion workflows.
- Review tracking SDKs and disclosures.

## 21. Standards and framework mapping

### 21.1 OWASP Mobile Application Security project

The OWASP Mobile Application Security project provides three linked resources:
- MASVS: mobile application security verification requirements.
- MASWE: mobile-specific security weakness enumeration.
- MASTG: tests, techniques and demos used to verify requirements.

The current project uses the stable MASTG v2.0.0 structure and MASWE v1.0.0 baseline as captured on 2026-11-18. Check the official project for later point releases before assessments. Do not copy test IDs from older MASTG v1 material into v2 records without verifying the current canonical ID and test content.

The traceability model for a mobile finding is:

**MASVS control → MASWE weakness → MASTG test → MASTG technique/demo → project test evidence → remediation.**

Use the official mobile security checklist and pinned release/commit to record exact control and test identifiers. This chapter intentionally does not fabricate MASVS or MASTG IDs.

### 21.2 MASVS control themes

Map each mobile requirement to the applicable current MASVS control group, including:
- Storage.
- Cryptography.
- Authentication.
- Network.
- Platform.
- Code quality.
- Resilience.
- Privacy.

Verify current group naming and control identifiers in the official MASVS release used by the engagement.

### 21.3 OWASP ASVS and API Security

Use ASVS for applicable backend web/API controls such as authentication, authorization, session management, cryptography, input validation, business logic and logging. Use OWASP API Security Top 10 as a risk taxonomy, not as a substitute for mobile platform testing or a complete verification standard.

### 21.4 NIST SSDF and CSF

- NIST SP 800-218 SSDF: secure development, build, release and vulnerability response processes.
- NIST CSF 2.0: governance and risk outcomes for mobile product security.
- Use these to organize product lifecycle controls, not as mobile test case identifiers.

### 21.5 ISO/IEC 27001:2022 relevance

| Annex A control | Mobile security relevance |
|---|---|
| 5.8 | Security in project management |
| 5.9 | Inventory of information and associated assets |
| 5.15–5.18 | Access control and identity |
| 5.19–5.23 | Supplier and cloud service security |
| 5.31 | Legal, statutory, regulatory and contractual requirements |
| 5.34 | Privacy and protection of PII |
| 8.4 | Access to source code |
| 8.5 | Secure authentication |
| 8.7 | Protection against malware |
| 8.8 | Management of technical vulnerabilities |
| 8.9 | Configuration management |
| 8.15–8.16 | Logging and monitoring |
| 8.24 | Use of cryptography |
| 8.25–8.29 | Secure development, architecture, coding and testing |
| 8.31 | Separation of development, test and production |
| 8.32 | Change management |
| 8.33 | Test information |

This is a relevance mapping, not a declaration of implementation or certification.

## 22. Regulatory and jurisdiction considerations

Mobile applications inherit the obligations of the data controller/operator, service provider, sector and jurisdictions in which they operate. App store policy compliance is not a substitute for legal compliance.

For each deployment determine:
- Entity and role (controller, processor, fiduciary, service provider or local equivalent).
- Data subjects and locations.
- Personal, sensitive, child, biometric, health, financial or government data.
- Collection purposes, lawful basis and notice.
- SDK/processor relationships and onward transfers.
- Data residency and cross-border access.
- Retention, deletion and rights workflows.
- Breach notification and regulator obligations.
- Sector-specific rules and contractual commitments.

### 22.1 India

Assess the Digital Personal Data Protection Act, 2023 and DPDP Rules, 2025 where applicable. The Rules were notified with phased commencement; verify the exact provision and effective date before translating requirements into a deadline. Mobile-specific engineering implications include transparent notices, purpose-limited permission and data collection, rights request workflows, processor governance, reasonable safeguards, breach handling and deletion when applicable conditions are met. Consider sector-specific RBI, SEBI, IRDAI, health, telecom and CERT-In obligations where the entity and service fall within scope.

### 22.2 European Union and EEA

Assess GDPR applicability, ePrivacy requirements where relevant, national implementation and sector rules. Mobile engineering implications include data minimization, consent/choice where required, transparency, privacy by design, rights handling, DPIA where required, processor governance, transfer safeguards and security of processing. App tracking and device identifiers require context-specific review.

### 22.3 United Kingdom

Assess UK GDPR, Data Protection Act 2018, PECR and relevant regulator guidance. Review mobile analytics, advertising identifiers, location, consent, transparency, retention and international transfers.

### 22.4 Qatar

Assess Qatar Personal Data Privacy Protection Law No. 13 of 2016 and relevant sector-specific requirements. Confirm current regulator guidance, entity scope, cross-border transfer conditions and applicable notices/consent/security obligations with qualified local counsel.

### 22.5 Saudi Arabia

Assess the Saudi Personal Data Protection Law and Implementing Regulations, including current transfer regulations and amendments. Review app telemetry, location, biometrics, identity data, processors, retention, rights and breach handling. Confirm current SDAIA/National Data Management Office requirements before setting operational deadlines.

### 22.6 United Arab Emirates

Determine whether the federal UAE Personal Data Protection Law or a free-zone/sector regime such as DIFC or ADGM applies. Map mobile collection, tracking, processors, rights, security and transfers to the correct legal framework.

### 22.7 United States and other markets

Depending on footprint, assess applicable state privacy laws, children's privacy rules, health/financial/consumer protection requirements and sector obligations. App store privacy labels and SDK disclosures must be accurate, but do not replace statutory analysis.

## 23. Mobile security governance and operating model

| Activity | Accountable owner | Supporting roles |
|---|---|---|
| Mobile threat model | Product security architect | Product, mobile, backend |
| Platform configuration | Mobile engineering lead | Platform engineer, AppSec |
| API authorization | Backend/API owner | IAM, AppSec |
| Secure storage and crypto | Security architect | Mobile engineers, platform team |
| SDK approval | Product/security owner | Privacy, legal, procurement |
| Signing and release | Release engineering owner | Mobile lead, security |
| Vulnerability intake | PSIRT/vulnerability owner | AppSec, product, vendor |
| Privacy assessment | Privacy owner | Product, legal, mobile team |
| Mobile incident response | Incident commander | SOC, IAM, platform, privacy |
| App store release | Product/release owner | Security, QA, legal |

## 24. Mobile release security gate

A release should not be approved until:
- Threat model and data inventory are reviewed.
- Manifest/entitlements and permissions are approved.
- No unresolved critical/high risk exists without explicit risk acceptance.
- Static and dynamic tests have recorded results.
- API authorization and transaction controls are tested.
- Sensitive storage and token lifecycle are verified.
- TLS and deep link behavior are verified.
- SDK and dependency inventory is current.
- Privacy disclosures reflect actual behavior.
- Signing, provenance and artifact hashes are recorded.
- Rollback and emergency disable paths are understood.
- Known limitations and exceptions have owners and expiry dates.

## 25. Maturity model

| Level | Characteristics |
|---|---|
| 1 — Ad hoc | Mobile security testing is irregular; release controls depend on individual knowledge |
| 2 — Repeatable | Baseline platform checklist, dependency inventory and manual security review exist |
| 3 — Defined | Threat modeling, secure defaults, MASVS-aligned requirements and release gates are standardized |
| 4 — Measured | Automated tests, artifact inspection, telemetry and vulnerability metrics are tracked |
| 5 — Adaptive | Continuous risk analysis, verified provenance, robust response and feedback into architecture are established |

Do not assign a maturity level based solely on tool deployment. Require evidence of process execution and effectiveness.

## 26. Implementation roadmap

### Foundation: 0–30 days
- Inventory mobile apps, platforms, package IDs and release channels.
- Identify data classes, SDKs, API endpoints and signing owners.
- Inspect manifests, entitlements, permissions and debug settings.
- Identify sensitive local storage and token risks.
- Establish a mobile threat model and test authorization.

### Control implementation: 30–90 days
- Enforce secure storage and token lifecycle.
- Harden IPC, deep links and WebViews.
- Validate TLS and certificate handling.
- Introduce dependency/SBOM review and SDK approval.
- Add mobile-specific static and dynamic tests to release pipeline.
- Verify backend authorization and abuse controls.

### Assurance: 90–180 days
- Align requirements to pinned MASVS release.
- Map weaknesses to MASWE and atomic MASTG v2 tests.
- Automate repeatable tests and artifact inspection.
- Exercise mobile incident and signing compromise scenarios.
- Measure release-gate coverage and remediation time.
- Review privacy disclosures and processor data flows.

## 27. Evidence and assessment deliverables

A professional mobile assessment pack should include:
- Scope and rules of engagement.
- App and artifact inventory.
- Device/OS/test environment matrix.
- Threat model and data-flow diagrams.
- Manifest and entitlement review.
- Dependency and SDK inventory.
- MASVS control mapping with pinned version.
- MASWE weakness references where applicable.
- MASTG v2 test IDs and technique references where applicable.
- Internal test cases and reproducible steps.
- Evidence with sensitive data redacted.
- Findings with impact, likelihood, root cause and remediation.
- API/backend authorization evidence.
- Release and signing review.
- Privacy and regulatory applicability notes.
- Retest and residual risk record.

## 28. Related chapters

- [02. Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [03. Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [04. Secure Coding and Code Review](../04-secure-coding/SECURE-CODING-AND-CODE-REVIEW.md)
- [06. API and Service Security](../06-api-service-security/API-AND-SERVICE-SECURITY-ENGINEERING.md)
- [07. Identity and Access Security](../07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY.md)
- [08. Data Security and Privacy Engineering](../08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-ENGINEERING.md)
- [09. Mobile Application Security Lab Pack](MOBILE-APPLICATION-SECURITY-LAB-PACK.md)
- [13. Software Supply Chain Security](../13-software-supply-chain/SOFTWARE-SUPPLY-CHAIN-SECURITY.md)
- [14. Security Verification and Assessment](../14-security-verification-assessment/SECURITY-VERIFICATION-AND-ASSESSMENT.md)
- [18. Standards Baseline and Mapping Method](../18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md)
- [19. Global Regulatory Register](../19-global-regulatory/GLOBAL-REGULATORY-REGISTER.md)

## 29. Authoritative references

1. OWASP Mobile Application Security project: https://owasp.org/projects/mobile-application-security
2. OWASP MAS project portal: https://mas.owasp.org/
3. OWASP MASVS repository: https://github.com/OWASP/masvs
4. OWASP MASTG releases: https://github.com/OWASP/MASTG/releases
5. OWASP MASWE project resources: https://mas.owasp.org/MASWE/
6. Android security best practices: https://developer.android.com/privacy-and-security/security-best-practices
7. Android security tips: https://developer.android.com/privacy-and-security/security-tips
8. Android app security best practices: https://source.android.com/docs/security/best-practices/app
9. Apple Platform Security: https://support.apple.com/guide/security/welcome/web
10. Apple Keychain Services: https://developer.apple.com/documentation/security/keychain_services
11. Apple App Transport Security: https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity
12. NIST SP 800-218 SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
13. OWASP Mobile Application Security Testing Guide developer guide: https://devguide.owasp.org/en/06-verification/01-guides/02-mastg/

## 30. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial mobile application security engineering playbook |
