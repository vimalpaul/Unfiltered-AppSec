# Mobile Application Security Lab Pack

| Field | Value |
|---|---|
| Document ID | UAPPSEC-09-LAB-001 |
| Status | Draft lab specifications |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Android, iOS, hybrid app, mobile backend and release assurance |
| Classification | Public |

## 1. Safety and environment requirements

These labs are for applications and devices owned by the learner or explicitly authorized for testing. Use synthetic data, dedicated test accounts and isolated backend environments. Do not intercept other users' traffic, extract real credentials, test public apps without authorization, or tamper with devices outside the agreed scope.

Baseline requirements:
- Dedicated Android emulator/test device and iOS simulator/test device as appropriate.
- A deliberately vulnerable training application or source-controlled lab app.
- Local mock API and synthetic identity provider.
- Test signing identities and certificates only.
- No production accounts, payment cards, health records or customer data.
- Network egress limited to lab endpoints.
- Snapshots or disposable environments for reset.
- Evidence redacted to remove tokens, keys and personal data.
- Record OS/build, app version, tool versions and artifact hashes.
- Never upload private client APK/IPA files to public scanning services without approval.

The labs below are specifications. Do not mark them validated until setup, execution, reset and independent reproduction have been recorded.

## 2. Common lab evidence template

For every exercise record: lab ID, learner, date, app package/bundle ID, version/build, device and OS, tool versions, test account/role, synthetic dataset, preconditions, exact steps, raw observation, expected result, pass/fail, root cause, remediation, regression evidence, teardown and reviewer.

## 3. Lab 01 — Mobile application reconnaissance and artifact inventory

**Objective:** Establish a reliable inventory before security testing.

**Prerequisites:** Training APK or IPA, package metadata, test device/simulator and authorized scope.

### Procedure

1. Record the application name, package/bundle identifier, version, build number and distribution channel.
2. Calculate an artifact hash and preserve the original package.
3. Record signing certificate/team identity and signing metadata.
4. Identify platform minimum/target versions and supported architectures.
5. Enumerate bundled frameworks, native libraries, plugins and third-party SDKs.
6. Record network destinations and documented backend endpoints.
7. Capture device model, OS version, install source and test configuration.
8. Compare package contents to the release manifest and SBOM.
9. Identify debug artifacts, source maps, test endpoints or unexpected assets.
10. Produce an inventory with evidence and unresolved questions.

**Expected result:** Every tested artifact is attributable, reproducible and linked to its release context.

**Evidence:** Artifact inventory, hash, signing metadata and dependency list.

**Teardown:** Retain only approved sanitized evidence; remove test package if required.

## 4. Lab 02 — Android manifest and exported component review

**Objective:** Identify and validate Android component exposure.

**Prerequisites:** Training APK and disposable Android emulator.

### Procedure

1. Decode or inspect the APK manifest.
2. Record all activities, services, receivers and providers.
3. Identify components with exported behavior or intent filters.
4. Review required permissions and protection levels.
5. Inspect merged manifest contributions from libraries.
6. Identify debug flags, cleartext policy and backup configuration.
7. Install the app and confirm runtime component behavior.
8. From a separate test app or approved shell workflow, attempt to invoke only lab-designated exported components.
9. Verify sensitive operations require appropriate authorization.
10. Correct unnecessary exposure and repeat the checks.

**Expected result:** Only intended components are externally reachable; sensitive operations enforce caller authorization.

**Evidence:** Component inventory, manifest excerpts and controlled invocation results.

**Teardown:** Uninstall both test apps.

## 5. Lab 03 — Android intent and PendingIntent safety

**Objective:** Verify that intents and PendingIntents cannot be manipulated to invoke unintended actions.

**Prerequisites:** Training app with a notification/action workflow.

### Procedure

1. Identify explicit and implicit intent flows.
2. Record actions, categories, data URIs and extras.
3. Identify mutable and immutable PendingIntents.
4. Review target component and fill-in behavior.
5. Use a separate lab app to send malformed or unexpected intent data to the test component.
6. Verify untrusted extras cannot change account, file path, destination or authorization state.
7. Verify sensitive actions use explicit targets and suitable permissions.
8. Test unique request-code and PendingIntent identity behavior.
9. Replace mutable PendingIntents when mutability is not needed.
10. Add regression tests for malformed and unauthorized invocation.

**Expected result:** External input cannot redirect privileged behavior or alter security-critical state.

**Evidence:** Intent flow diagram and test results.

**Teardown:** Remove test notification and apps.

## 6. Lab 04 — Android content provider and URI grant review

**Objective:** Verify provider access, URI permissions and file path handling.

**Prerequisites:** Training app with a content provider and synthetic documents.

### Procedure

1. Inventory provider authorities, paths, exported state and read/write permissions.
2. Identify query, insert, update, delete and file-open operations.
3. Create synthetic records and files.
4. Attempt access from an untrusted lab app without a grant.
5. Test URI grants with a narrow read-only permission.
6. Attempt path traversal and malformed URI segments using synthetic paths.
7. Verify callers cannot request arbitrary files or sensitive columns.
8. Test grant expiry/revocation and provider behavior after logout.
9. Review MIME type and file descriptor mode handling.
10. Fix overbroad access and rerun the matrix.

**Expected result:** Provider exposes only intended records and files with narrow, revocable permissions.

**Evidence:** Provider inventory and access matrix.

**Teardown:** Delete synthetic files and revoke grants.

## 7. Lab 05 — Android local storage and backup assessment

**Objective:** Find sensitive data in app-private files, preferences, databases, cache and backup paths.

**Prerequisites:** Training app with synthetic account and session data.

### Procedure

1. Sign in using a synthetic test identity.
2. Exercise profile, document, authentication and offline workflows.
3. Inspect app-private storage through authorized emulator/debug access.
4. Review SharedPreferences/DataStore, SQLite/Room, files and cache.
5. Search for synthetic marker strings representing access tokens, password, PII and session identifiers.
6. Review external/shared storage and exported documents.
7. Inspect backup/data extraction rules and test backup/restore in the lab.
8. Inspect logs and temporary files.
9. Determine which values should be stored, protected, excluded or deleted.
10. Implement platform-appropriate secure storage and verify again.

**Expected result:** No unnecessary plaintext secret or sensitive record remains in an unapproved location or backup.

**Evidence:** Sanitized storage inventory and backup configuration.

**Teardown:** Clear app data and delete synthetic backups.

## 8. Lab 06 — Android Keystore key lifecycle

**Objective:** Verify key generation, use, access controls, invalidation and deletion.

**Prerequisites:** Training app with a synthetic encryption feature and test device/emulator.

### Procedure

1. Identify the key aliases and intended purpose.
2. Review algorithm, mode, padding and digest constraints.
3. Determine whether the key is exportable and whether hardware backing is available.
4. Review user authentication requirements and validity duration.
5. Encrypt a synthetic record using the key.
6. Attempt access from an unauthorized app/process context.
7. Test behavior after screen lock and app restart.
8. In a disposable test profile, test invalidation behavior for supported enrollment/lock-screen changes.
9. Exercise key rotation and deletion.
10. Document fallback behavior on devices without the required hardware feature.

**Expected result:** Keys are non-exportable where required, use is purpose-limited and lifecycle behavior is documented.

**Evidence:** Redacted key metadata and functional tests. Never record raw key material.

**Teardown:** Delete aliases and synthetic ciphertext.

## 9. Lab 07 — Android network security configuration

**Objective:** Verify HTTPS-only behavior, certificate validation and debug/release separation.

**Prerequisites:** Training app, local TLS test server, test CA and emulator.

### Procedure

1. Inspect the effective network security configuration.
2. Identify cleartext traffic exceptions and trust anchors.
3. Configure a valid test certificate for the expected hostname.
4. Verify the app connects successfully.
5. Present an expired certificate and verify failure.
6. Present a certificate for the wrong hostname and verify failure.
7. Present an untrusted CA and verify failure.
8. Inspect debug-only trust overrides.
9. Build the release artifact and verify user-installed test CAs are not trusted unless explicitly required by approved policy.
10. Verify no fallback to HTTP occurs after TLS failure.

**Expected result:** Only expected valid server identities are accepted; debug trust configuration is not shipped to production.

**Evidence:** Configuration and sanitized connection outcomes.

**Teardown:** Remove test CA and certificates.

## 10. Lab 08 — Android WebView and JavaScript bridge

**Objective:** Verify that WebView content cannot invoke privileged native functions from an untrusted origin.

**Prerequisites:** Training app with a WebView and local benign test pages.

### Procedure

1. Identify all WebView instances and settings.
2. Determine whether JavaScript, file access, DOM storage and content access are enabled.
3. Inventory JavaScript interfaces and native bridge methods.
4. Load an approved first-party lab page and test required behavior.
5. Navigate to a separate untrusted local test origin.
6. Attempt to invoke exposed bridge methods with benign marker values.
7. Test redirects, iframe content and malformed navigation URLs.
8. Verify SSL errors cancel navigation.
9. Apply strict origin allowlists and minimize bridge methods.
10. Repeat tests with untrusted content and verify no privileged action occurs.

**Expected result:** Untrusted content cannot reach sensitive native functions or file resources.

**Evidence:** WebView configuration, bridge inventory and controlled test results.

**Teardown:** Clear WebView data and stop local pages.

## 11. Lab 09 — Android deep links and App Links

**Objective:** Validate incoming URI parsing, domain verification and server-side authorization.

**Prerequisites:** Training app with synthetic account routes and a verified lab domain.

### Procedure

1. Inventory URI schemes, hosts, paths and intent filters.
2. Identify routes carrying object identifiers or action parameters.
3. Verify App Links domain association in the lab.
4. Invoke a valid synthetic route.
5. Test unknown hosts, malformed encoding, duplicate parameters and unexpected schemes.
6. Test open redirect and WebView navigation behavior.
7. Attempt to access another synthetic user's object through a modified link.
8. Verify backend authorization rejects unauthorized access.
9. Remove unnecessary URL parameters and broad intent filters.
10. Add regression tests for route parsing and authorization.

**Expected result:** Links navigate only to intended destinations; all object access remains server-authorized.

**Evidence:** Route inventory, domain association and test results.

**Teardown:** Remove test domain association and app data.

## 12. Lab 10 — iOS Info.plist and entitlement review

**Objective:** Identify excessive capabilities and unsafe iOS configuration.

**Prerequisites:** Training IPA or Xcode archive and test signing profile.

### Procedure

1. Inspect Info.plist, bundle identifier and deployment target.
2. Extract effective signed entitlements from the built artifact.
3. Compare entitlements with the approved capability baseline.
4. Inventory URL schemes, document types and associated domains.
5. Review App Groups and Keychain access groups.
6. Review background modes and privacy usage descriptions.
7. Identify debug/development configuration and unexpected embedded frameworks.
8. Compare release artifact metadata with project settings.
9. Remove unnecessary entitlements and broad shared access.
10. Rebuild and compare the signed artifact.

**Expected result:** Release entitlements and metadata are minimal, intentional and attributable.

**Evidence:** Redacted entitlement diff and package inventory.

**Teardown:** Remove test provisioning material securely.

## 13. Lab 11 — iOS Keychain and Data Protection

**Objective:** Validate credential storage accessibility and file protection.

**Prerequisites:** Training iOS app with synthetic tokens and records.

### Procedure

1. Identify Keychain items and their accessibility classes.
2. Review access control flags and access groups.
3. Determine which items synchronize or migrate.
4. Store a synthetic credential using the intended protection policy.
5. Test access while the device is locked/unlocked as applicable.
6. Test logout and account removal behavior.
7. Inspect app files, databases, temporary files and shared containers.
8. Verify file protection class on sensitive files.
9. Test backup/restore and app reinstall behavior where supported.
10. Correct overbroad accessibility and verify lifecycle behavior.

**Expected result:** Sensitive credentials use suitable Keychain controls; files use suitable Data Protection and deletion behavior.

**Evidence:** Redacted Keychain metadata and file protection results. Do not export secrets.

**Teardown:** Delete test Keychain items and app data.

## 14. Lab 12 — iOS URL schemes and Universal Links

**Objective:** Validate incoming URLs, domain association and route authorization.

**Prerequisites:** Training iOS app and lab domain.

### Procedure

1. Inventory registered custom URL schemes and Universal Link domains.
2. Review associated domain entitlement and apple-app-site-association file.
3. Invoke a valid test route.
4. Test malformed, duplicate, oversized and encoded parameters.
5. Test a route from an untrusted application context.
6. Verify the app does not trust URL-supplied account or role values.
7. Test fallback behavior when the app is not installed.
8. Verify backend object authorization for linked resources.
9. Remove unused schemes and broad routes.
10. Add route parsing and authorization regression tests.

**Expected result:** Only intended links are accepted and route input cannot bypass authorization.

**Evidence:** Entitlement, association file and route test results.

**Teardown:** Remove test domain configuration.

## 15. Lab 13 — iOS App Groups, extensions and pasteboard

**Objective:** Verify shared data is limited to intended app/extension processes and does not leak through clipboard.

**Prerequisites:** Training app with one extension and synthetic content.

### Procedure

1. Inventory App Groups and Keychain access groups.
2. Identify files and data shared between app and extension.
3. Attempt access from an unrelated test app.
4. Review extension input validation and shared file parsing.
5. Place a synthetic sensitive marker on the pasteboard through the app workflow.
6. Inspect pasteboard expiration/local-only policy where supported.
7. Test app backgrounding and app switcher snapshots.
8. Review notification previews and share-sheet behavior.
9. Restrict shared containers and sensitive clipboard behavior.
10. Retest access and lifecycle cleanup.

**Expected result:** Only authorized app components access shared data; clipboard and UI snapshots do not unnecessarily disclose secrets.

**Evidence:** Shared-container inventory and sanitized observations.

**Teardown:** Clear pasteboard and shared test data.

## 16. Lab 14 — iOS App Transport Security and trust evaluation

**Objective:** Validate secure transport and custom trust evaluation behavior.

**Prerequisites:** Training app, local TLS test server and test CA.

### Procedure

1. Inspect App Transport Security settings and exceptions.
2. Review URLSession delegate trust handling.
3. Connect to a valid lab endpoint.
4. Test invalid, expired and wrong-host certificates.
5. Verify connections fail closed.
6. Inspect redirects and credential forwarding.
7. Review pinning implementation if used.
8. Test a planned certificate/key rotation in the lab.
9. Confirm ATS exceptions are narrow and documented.
10. Remove unnecessary exceptions and repeat.

**Expected result:** Invalid server identities are rejected and custom trust code does not bypass platform validation.

**Evidence:** ATS configuration and sanitized handshake results.

**Teardown:** Remove test certificates.

## 17. Lab 15 — OAuth Authorization Code with PKCE

**Objective:** Validate native-app federated authentication and callback protections.

**Prerequisites:** Mock identity provider, training mobile app and test account.

### Procedure

1. Record client type and redirect URI.
2. Verify the application uses Authorization Code with PKCE for the native public client.
3. Inspect state generation and callback validation.
4. Verify external browser/system authentication session use where applicable.
5. Initiate a login and capture sanitized protocol metadata.
6. Test a mismatched state in the lab.
7. Test an unexpected redirect URI or callback.
8. Verify authorization code cannot be reused and PKCE verifier is required.
9. Inspect token storage and refresh rotation.
10. Test logout and server-side revocation.

**Expected result:** Callback and token exchange are bound to the initiating request; tokens are protected and revocable.

**Evidence:** Redacted protocol flow and identity-provider configuration.

**Teardown:** Revoke test sessions and delete test credentials.

## 18. Lab 16 — Mobile biometric and device-bound key flow

**Objective:** Verify that biometrics gate a protected local key operation and are not treated as a standalone server identity.

**Prerequisites:** Test device with supported biometric/passcode capability and synthetic backend challenge.

### Procedure

1. Identify biometric API and fallback behavior.
2. Determine whether a platform-protected key operation is gated by user presence.
3. Register a synthetic public key with a test backend.
4. Request a fresh backend challenge.
5. Authorize the key operation using the OS biometric interface.
6. Submit the signature and challenge to the backend.
7. Test challenge expiry and replay.
8. Test biometric enrollment or lock-screen change behavior on a disposable device/profile where supported.
9. Test device removal and server-side key revocation.
10. Verify a local Boolean or cached flag cannot authorize a remote operation.

**Expected result:** Protected local key use requires the intended user-presence condition; backend verifies fresh challenge and key binding.

**Evidence:** Sanitized challenge/signature verification results; never capture biometric data or private keys.

**Teardown:** Revoke registered test key and clear app state.

## 19. Lab 17 — Cross-platform bridge and secure storage review

**Objective:** Verify that framework abstractions preserve native platform security semantics.

**Prerequisites:** Training React Native, Flutter or .NET MAUI app.

### Procedure

1. Identify framework version and native plugin inventory.
2. Locate platform channels/native modules.
3. Inspect local storage APIs and determine which data uses Keychain/Keystore.
4. Identify JavaScript/Dart bundle configuration and source maps.
5. Inspect deep link handling and WebView bridge.
6. Review debug menu and release build flags.
7. Test synthetic token storage and retrieval.
8. Inspect Android merged manifest and iOS signed entitlements.
9. Verify plugin updates do not add unexpected permissions or egress destinations.
10. Document framework-specific limitations and add native tests.

**Expected result:** No assumption of security based solely on a cross-platform API; native controls are verified on both platforms.

**Evidence:** Plugin inventory, build metadata and platform test results.

**Teardown:** Remove app and test credentials.

## 20. Lab 18 — Runtime analysis and tamper-resilience assessment

**Objective:** Evaluate defensive signals and confirm backend security remains effective under client manipulation.

**Safety:** Use only a purpose-built training app and disposable emulator/device. Do not instrument third-party apps or accounts.

### Procedure

1. Record baseline behavior of the unmodified lab app.
2. Identify client-side role, feature, integrity and transaction state checks.
3. Use an authorized lab instrumentation setup to observe a non-sensitive test method.
4. Modify a synthetic local preference or UI flag.
5. Attempt a sensitive backend operation using the modified client state.
6. Verify the backend independently checks authorization and transaction state.
7. Compare integrity/risk signal behavior on supported lab configurations.
8. Record false positives and unsupported-device behavior.
9. Remove reliance on client-only controls for security-critical decisions.
10. Add server-side regression tests.

**Expected result:** Client modification cannot grant unauthorized server-side privileges or alter authoritative transaction state.

**Evidence:** Baseline and modified-client results without sensitive tokens.

**Teardown:** Reset emulator and revoke test sessions.

## 21. Lab 19 — Mobile API authorization, replay and business logic

**Objective:** Validate the backend independently of the mobile UI.

**Prerequisites:** Local API, two synthetic users/tenants and mobile test client.

### Procedure

1. Inventory mobile API endpoints and roles.
2. Create synthetic objects for two users or tenants.
3. Capture a normal authorized request using the test client.
4. Change a synthetic object identifier and verify object-level authorization.
5. Change property fields such as role, owner or approval state.
6. Attempt a function intended for a higher role.
7. Repeat a synthetic transaction request to test idempotency/replay behavior.
8. Modify a client-supplied price/status/entitlement field.
9. Test rate limits for a low-volume approved scenario.
10. Confirm server-side authorization and state validation reject all unauthorized actions.

**Expected result:** The backend remains authoritative for identity, object access, field permissions, business state and replay control.

**Evidence:** Sanitized request/response pairs and authorization matrix.

**Teardown:** Delete synthetic data and revoke test tokens.

## 22. Lab 20 — SDK and mobile software supply-chain review

**Objective:** Identify third-party code, data flows and build-time risk.

**Prerequisites:** Training app with a known set of dependencies and one mock analytics SDK.

### Procedure

1. Generate dependency inventory for native and framework packages.
2. Identify direct and transitive dependencies.
3. Record versions, publishers, licenses and support status.
4. Review permissions, entitlements and manifest changes introduced by SDKs.
5. Inspect network destinations in a controlled lab.
6. Identify data sent to analytics/crash services.
7. Check for known vulnerabilities using approved offline or controlled scanners.
8. Review source maps, symbols and debug assets.
9. Update a deliberately outdated lab dependency to a fixed supported release.
10. Compare artifact and behavior before/after update.

**Expected result:** Dependencies and data flows are attributable; unexpected permissions, destinations and vulnerable components are identified.

**Evidence:** SBOM/dependency inventory and SDK data-flow matrix.

**Teardown:** Remove test SDK credentials and data.

## 23. Lab 21 — Mobile release signing and artifact provenance

**Objective:** Verify that the distributed artifact is signed by an approved identity and traceable to a controlled build.

**Prerequisites:** Training Android APK/AAB and iOS IPA/archive; disposable signing identities.

### Procedure

1. Record source commit and CI build identifier.
2. Generate the training release artifact in the controlled pipeline.
3. Calculate artifact hash.
4. Verify Android package signature and signing certificate.
5. Inspect iOS code signature and effective entitlements.
6. Compare build configuration with approved release profile.
7. Confirm signing secrets are not present in source or logs.
8. Verify artifact provenance and approval record.
9. In a disposable lab, modify a copy of the artifact and verify signature validation fails.
10. Document release recovery and signing-key compromise response.

**Expected result:** Release artifacts are attributable, signed and verifiable; modified artifacts do not pass signature checks.

**Evidence:** Hash, signature verification and build provenance record.

**Teardown:** Destroy test signing material according to lab policy.

## 24. Lab 22 — Mobile privacy and sensitive disclosure

**Objective:** Identify personal data exposure through permissions, analytics, notifications, clipboard and crash reporting.

**Prerequisites:** Training app, synthetic personal data and mock telemetry endpoints.

### Procedure

1. Inventory requested OS permissions and user-facing purpose.
2. Deny and later revoke each optional permission.
3. Exercise app flows and observe whether data collection continues unexpectedly.
4. Inspect analytics and crash events for synthetic identifiers and secrets.
5. Review notification preview content.
6. Test clipboard and screenshot behavior for sensitive screens.
7. Review third-party SDK network destinations.
8. Compare actual processing with privacy disclosure.
9. Remove unnecessary fields and redact telemetry.
10. Repeat with a clean install and fresh synthetic account.

**Expected result:** Collection is minimized, permissions are handled correctly and sensitive data is not unintentionally disclosed.

**Evidence:** Data-flow matrix and redacted telemetry.

**Teardown:** Purge synthetic telemetry.

## 25. Lab 23 — Mobile offline state and lifecycle integrity

**Objective:** Verify that local state manipulation and offline operation cannot bypass server policy.

**Prerequisites:** Training app with an offline workflow and mock backend.

### Procedure

1. Sign in with a synthetic user and load permitted offline data.
2. Disconnect network connectivity.
3. Exercise permitted offline actions.
4. Modify local synthetic state in the test environment.
5. Reconnect and observe synchronization behavior.
6. Attempt replay of queued actions.
7. Test logout while offline and reconnect.
8. Test expired session and revoked device.
9. Verify backend revalidates all security-critical state.
10. Add conflict and revocation regression tests.

**Expected result:** Offline mode has bounded authority; stale or manipulated state cannot override backend truth.

**Evidence:** State transition log and API responses.

**Teardown:** Reset local state and revoke test sessions.

## 26. Lab 24 — Mobile incident response tabletop

**Objective:** Practice response to a mobile release or credential incident.

**Prerequisites:** Mock incident involving a leaked test signing credential, vulnerable SDK or exposed mobile token.

### Procedure

1. Assign incident commander, mobile owner, backend owner, SOC, privacy and legal contacts.
2. Introduce the scenario and timestamp.
3. Identify affected app versions, platforms, distribution channels and user cohorts.
4. Determine whether signing key, token, source code, SDK or backend is affected.
5. Contain by revoking test credentials, disabling vulnerable API paths or pausing release in the lab.
6. Preserve build logs, artifact hashes, identity logs and API telemetry.
7. Determine data and tenant impact.
8. Assess user/regulator/vendor notification decisions with legal/privacy owners.
9. Define remediation, forced update or session revocation strategy.
10. Conduct lessons learned and update release gates.

**Expected result:** Team can contain, scope, preserve evidence and coordinate a mobile-specific response.

**Evidence:** Timeline, decision log and corrective action register.

**Teardown:** Close mock incident and reset credentials.

## 27. Assessment rubric

| Criterion | Points |
|---|---:|
| Threat model and artifact inventory | 10 |
| Android platform controls | 15 |
| iOS platform controls | 15 |
| Secure storage and cryptography | 10 |
| Network, WebView and deep link security | 10 |
| Authentication, backend authorization and business logic | 15 |
| Privacy and SDK supply chain | 10 |
| Signing, release and resilience | 5 |
| Evidence, remediation and regression | 5 |
| Safe teardown and scope compliance | 5 |
| **Total** | **100** |

Suggested training interpretation: 90–100 strong independent engineering; 75–89 competent with review; 60–74 guided remediation required; below 60 repeat the exercise. These thresholds are for training, not certification.

## 28. Instructor review checklist

- Was authorization explicit and limited to the lab assets?
- Were only synthetic accounts, data and signing keys used?
- Were Android merged manifests and iOS signed entitlements reviewed?
- Were IPC and deep links tested from an untrusted caller context?
- Were Keychain/Keystore controls reviewed beyond API name recognition?
- Did invalid TLS certificates fail closed?
- Were WebView native bridges constrained by origin?
- Was OAuth PKCE and callback validation reviewed?
- Did backend tests verify object/property/function and tenant authorization?
- Were SDK destinations and data disclosures inspected?
- Was tampering treated as a client threat rather than the only security boundary?
- Were artifacts and signing provenance verified?
- Was evidence redacted and the environment safely reset?

## 29. References

1. OWASP Mobile Application Security: https://owasp.org/projects/mobile-application-security
2. OWASP MASTG releases: https://github.com/OWASP/MASTG/releases
3. OWASP MASVS: https://github.com/OWASP/masvs
4. Android security best practices: https://developer.android.com/privacy-and-security/security-best-practices
5. Android security tips: https://developer.android.com/privacy-and-security/security-tips
6. Apple Platform Security: https://support.apple.com/guide/security/welcome/web
7. Apple Keychain Services: https://developer.apple.com/documentation/security/keychain_services
8. NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final

## 30. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial mobile application security lab specifications |
