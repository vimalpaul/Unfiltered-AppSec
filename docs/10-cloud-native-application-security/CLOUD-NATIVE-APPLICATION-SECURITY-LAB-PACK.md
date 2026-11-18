# Cloud-Native Application Security Lab Pack

| Field | Value |
|---|---|
| Document ID | UAPPSEC-10-LAB-001 |
| Status | Draft lab specifications |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | Cloud IAM, container, Kubernetes, serverless, IaC, CI/CD, logging and recovery |
| Classification | Public |

## 1. Safety, authorization and cost controls

These labs are for cloud accounts, projects, subscriptions, clusters and applications owned by the learner or explicitly authorized for testing. Use a dedicated sandbox or local cluster, synthetic data, test identities and disposable resources.

Cloud labs can incur charges. Before starting:
- Use a dedicated sandbox subscription/account/project with budget alerts and quotas.
- Prefer local containers, kind, minikube or k3d for Kubernetes exercises where a managed cloud service is not essential.
- Set a maximum runtime and resource quota.
- Do not create public IPs, public storage, high-volume workloads or costly managed services unless the lab explicitly requires them and the owner approves.
- Never use production credentials, customer data or signing keys.
- Do not run destructive commands against shared or production resources.
- Use exact lab resource names and a unique prefix.
- Keep cloud audit logs enabled.
- Define cleanup commands and verify deletion.
- Stop if unexpected resources, costs, access or network exposure appear.

The lab pack intentionally avoids embedding provider account IDs, subscription IDs, project identifiers, credentials, private keys or real customer endpoints.

## 2. Common lab environment

Recommended baseline:
- A dedicated cloud sandbox or local container/Kubernetes environment.
- A test identity with limited permissions.
- A synthetic application and API.
- A private test registry or local image store.
- IaC examples in a disposable workspace.
- A local logging destination or isolated security workspace.
- Version-pinned CLI and scanner tools.
- Network isolation and egress controls.
- A cleanup script reviewed before execution.

For provider-specific exercises, record provider, region, service tier, cluster version, API versions, CLI version, runtime, identity type and applicable feature limitations. A local cluster is useful for learning Kubernetes behavior but does not reproduce every managed control-plane feature.

## 3. Evidence record

For each lab capture:
- Lab ID and title.
- Authorization and sandbox owner.
- Resource prefix and environment.
- Provider/platform versions.
- Start/end time and learner.
- Identity and permissions used.
- Initial configuration and preconditions.
- Exact steps and command outputs with secrets redacted.
- Expected and observed result.
- Evidence file hashes where appropriate.
- Finding, root cause and risk.
- Remediation and retest.
- Cost and cleanup verification.
- Reviewer and closure status.

Never place raw credentials, tokens, private keys, secret values or customer data in evidence.

## 4. Lab 01 — Cloud asset inventory and ownership

**Objective:** Establish a complete inventory of in-scope cloud resources and owners.

**Prerequisites:** Read-only inventory permissions in a sandbox.

### Procedure

1. Confirm the sandbox account, subscription or project and approved regions.
2. Enumerate organization hierarchy and workload boundaries.
3. Inventory compute, storage, databases, clusters, registries, functions, networks, identities and key services.
4. Identify public endpoints and internet-exposed resources.
5. Record owner, environment, criticality, data class and lifecycle status.
6. Identify orphaned resources and unknown ownership.
7. Compare inventory to IaC and service catalog records.
8. Record collection gaps and permission limitations.
9. Assign owners and remediation for unmanaged resources.
10. Repeat after cleanup to verify inventory accuracy.

**Expected result:** Every discovered resource is attributable or recorded as an ownership gap.

**Evidence:** Inventory CSV/worksheet, scope record and exception register.

**Teardown:** No resources should be created. Remove temporary inventory files containing sensitive metadata according to policy.

## 5. Lab 02 — Human IAM and privileged access review

**Objective:** Identify excessive human permissions and weak administrative access paths.

**Prerequisites:** Read-only identity and audit access.

### Procedure

1. Inventory human users, groups, federated identities and external guests.
2. Identify privileged roles at organization, account, subscription, project and service levels.
3. Review MFA and federation configuration.
4. Identify shared, stale, dormant and non-person accounts.
5. Review permanent administrator grants and time-bound access mechanisms.
6. Inspect role inheritance and nested group membership.
7. Identify break-glass accounts and recovery procedures.
8. Review recent role assignment and privilege changes in audit logs.
9. Compare each privileged grant to a named owner and business purpose.
10. Propose least-privilege role changes through approved change management; do not modify shared sandbox identities without approval.

**Expected result:** Privileged access is attributable, protected and periodically reviewed.

**Evidence:** Role matrix, stale identity list and access review decision log.

**Teardown:** Revoke only temporary lab access created for this exercise.

## 6. Lab 03 — Workload identity and static credential elimination

**Objective:** Replace an embedded or long-lived test credential with a scoped workload identity.

**Prerequisites:** Synthetic application and test cloud resource, such as a dedicated object container/bucket.

### Procedure

1. Create a test workload that accesses only a synthetic resource.
2. Record the initial credential mechanism without displaying the secret value.
3. Identify the permissions granted to that credential.
4. Create a dedicated workload identity with only the required read or write operation.
5. Configure the approved provider-native identity attachment or federation mechanism.
6. Remove the static test credential from application configuration and deployment artifacts.
7. Run the workload and verify the intended operation succeeds.
8. Attempt a different operation that should be denied.
9. Review token lifetime, audience, trust conditions and audit events.
10. Revoke the old credential and verify the workload still works using the new identity.

**Expected result:** Workload uses short-lived, scoped identity and cannot access unrelated resources.

**Evidence:** Identity trust configuration, effective permission review and successful/denied operation logs.

**Teardown:** Delete the test identity and resource; revoke the old test credential.

## 7. Lab 04 — Cross-account or cross-project trust analysis

**Objective:** Review federation and delegated role trust paths.

**Prerequisites:** Two disposable test accounts/projects or a mocked policy environment.

### Procedure

1. Draw the source and target trust relationship.
2. Identify principal, issuer, subject, audience and external condition.
3. Review role trust or federation policy.
4. Identify whether an untrusted repository, namespace, branch or tenant could satisfy the trust condition.
5. Check whether trust allows wildcard principals or broad subjects.
6. Create a narrow test trust condition for one known workload.
7. Verify the intended workload can assume the role.
8. Verify a different workload, repository or subject is denied.
9. Inspect audit logs for assumption and token issuance.
10. Record revocation and ownership transfer steps.

**Expected result:** Only the intended workload context can obtain the target identity.

**Evidence:** Trust policy, positive/negative test results and audit events.

**Teardown:** Remove test trust relationship and temporary roles.

## 8. Lab 05 — Public storage exposure and resource policy

**Objective:** Verify public access controls for object storage.

**Prerequisites:** Dedicated test bucket/container with synthetic non-sensitive files.

### Procedure

1. Create a private test storage resource.
2. Record account-level and resource-level public access settings.
3. Review ACLs, identity policy, resource policy and inherited organization guardrails.
4. Confirm unauthenticated access is denied.
5. Create a deliberate public-access misconfiguration only in the disposable lab and within approved rules.
6. Confirm the lab object becomes accessible through the expected test path.
7. Reapply block-public-access or equivalent policy.
8. Verify anonymous access is denied again.
9. Review object access logs and policy-change events.
10. Add a preventive IaC/admission/organization policy to stop recurrence.

**Expected result:** Public access is denied by default and policy prevents accidental exposure.

**Evidence:** Before/after policy and anonymous access test results.

**Teardown:** Delete test objects and bucket/container; verify no public policy remains.

## 9. Lab 06 — Network segmentation and egress controls

**Objective:** Validate intended workload ingress and egress paths.

**Prerequisites:** Local container network or disposable cloud network with two synthetic services.

### Procedure

1. Draw expected traffic flows between frontend, API, database and external service.
2. Deploy synthetic services in separate network segments.
3. Record routes, security groups/firewall rules and DNS behavior.
4. Verify required application traffic succeeds.
5. Verify direct access to the database from an untrusted segment fails.
6. Apply default-deny egress where supported.
7. Allow only required destinations and ports.
8. Test DNS, health checks and telemetry dependencies.
9. Generate a denied egress event and confirm it is logged.
10. Review whether the control is enforced by the actual network dataplane.

**Expected result:** Only documented flows succeed; denied traffic is visible.

**Evidence:** Network diagram, policy and connectivity matrix.

**Teardown:** Remove test network and services.

## 10. Lab 07 — SSRF and cloud metadata defense

**Objective:** Verify a server-side URL fetcher cannot access metadata or internal cloud endpoints.

**Prerequisites:** Purpose-built vulnerable training application and local mock metadata service. Do not test public cloud metadata endpoints in this lab.

### Procedure

1. Deploy the training URL-fetching feature in an isolated network.
2. Confirm it accepts only documented URLs in the baseline.
3. Add a local mock metadata endpoint that returns a synthetic token marker.
4. Attempt access using loopback, link-local, private IPv4 and IPv6 test addresses.
5. Test redirects to blocked destinations.
6. Test DNS resolution that changes between validation and connection.
7. Test encoded address formats and alternate URL parsing forms.
8. Implement scheme/host/port allowlists and resolved-address validation.
9. Add egress rules that block metadata and internal management ranges.
10. Verify all unauthorized destinations are rejected and logged.

**Expected result:** URL validation and network policy prevent access to metadata/internal services.

**Evidence:** Sanitized request results, URL validation decisions and egress logs.

**Teardown:** Stop mock metadata service and delete lab network.

## 11. Lab 08 — Container image build hardening

**Objective:** Create a minimal and attributable container image.

**Prerequisites:** Sample application source and local container builder.

### Procedure

1. Inspect the original Dockerfile and base image.
2. Build the baseline image and record its digest.
3. Inspect packages, layers, user, exposed ports and filesystem.
4. Search the build context and image layers for synthetic secret markers.
5. Refactor to multi-stage build and a maintained minimal runtime image.
6. Pin the base image by digest.
7. Create a non-root runtime user.
8. Remove unnecessary packages and build tools.
9. Rebuild and compare image size, packages and attack surface.
10. Scan the final image and record findings with package context.

**Expected result:** Runtime image contains only required components and no embedded secrets.

**Evidence:** Dockerfile diff, image digest, package inventory and scan results.

**Teardown:** Remove local images and build cache containing synthetic data.

## 12. Lab 09 — Container runtime hardening

**Objective:** Verify a workload runs without unnecessary privileges.

**Prerequisites:** Local Docker/Podman or isolated Kubernetes cluster.

### Procedure

1. Deploy a simple synthetic web service with baseline settings.
2. Inspect UID/GID, capabilities, mount points and namespace configuration.
3. Identify privileged mode, host namespace and hostPath use.
4. Apply non-root execution and drop unnecessary capabilities.
5. Disable privilege escalation.
6. Apply read-only root filesystem where compatible.
7. Add CPU/memory requests and limits.
8. Apply seccomp and AppArmor/SELinux policy where supported.
9. Verify the application still performs its intended function.
10. Verify a prohibited write or privileged operation fails.

**Expected result:** The workload has only the runtime privileges required for the application.

**Evidence:** Deployment spec, runtime inspection and positive/negative behavior.

**Teardown:** Remove test container and volumes.

## 13. Lab 10 — Kubernetes RBAC and privilege escalation paths

**Objective:** Identify overprivileged Kubernetes identities.

**Prerequisites:** Disposable local cluster and synthetic namespaces.

### Procedure

1. Create separate deployer, operator and read-only test identities.
2. Inventory Roles, ClusterRoles and bindings.
3. Identify wildcard permissions and cluster-admin grants.
4. Review permissions to create pods, exec, port-forward, read secrets, create bindings and impersonate users.
5. Test intended read and deploy operations.
6. Test a prohibited role-binding or secret-read operation.
7. Create a minimal Role for the synthetic application.
8. Bind it only to the required service account or group.
9. Repeat positive and negative tests.
10. Record escalation paths and owner-approved exceptions.

**Expected result:** Workload and user identities have only required Kubernetes API permissions.

**Evidence:** RBAC matrix and authorization test output.

**Teardown:** Delete test roles, bindings, users and namespaces.

## 14. Lab 11 — Pod Security Standards and admission control

**Objective:** Enforce a secure pod baseline.

**Prerequisites:** Disposable Kubernetes cluster supporting Pod Security Admission or an approved policy engine.

### Procedure

1. Create a dedicated lab namespace.
2. Record its current Pod Security configuration.
3. Submit a compliant non-root pod specification.
4. Submit a test pod requesting privileged mode.
5. Submit a pod with hostPath or host namespace sharing.
6. Observe whether the API server warns, audits or denies each request.
7. Configure the approved restricted baseline for the lab namespace.
8. Re-submit the non-compliant test manifests.
9. Verify they are denied with a clear reason.
10. Document exception process and test a narrowly scoped approved exception if the lab owner permits.

**Expected result:** Non-compliant workloads are blocked or reported according to the intended policy.

**Evidence:** Namespace labels/policy, admission result and audit event.

**Teardown:** Delete namespace and policy resources.

## 15. Lab 12 — Kubernetes service account and cloud workload identity

**Objective:** Remove unnecessary default service-account token use and validate workload identity binding.

**Prerequisites:** Disposable cluster and local mock service or provider sandbox with synthetic resource.

### Procedure

1. Inventory service accounts and pod token automount settings.
2. Identify workloads using the default service account.
3. Create a dedicated service account for the test application.
4. Disable automatic token mounting when Kubernetes API access is not required.
5. If cloud API access is required, configure the provider's supported workload identity federation mechanism.
6. Bind trust to the exact cluster, namespace and service account subject.
7. Grant only the required resource permission.
8. Test intended access and unrelated-resource denial.
9. Review token audience and expiration behavior.
10. Remove unused service-account bindings and verify logs.

**Expected result:** Application receives only the identity and access it requires.

**Evidence:** Service account spec, trust policy and positive/negative access logs.

**Teardown:** Delete test identity, trust and synthetic resources.

## 16. Lab 13 — Kubernetes secrets and encryption at rest

**Objective:** Verify secret exposure paths and API datastore protection.

**Prerequisites:** Disposable cluster with synthetic secret marker.

### Procedure

1. Create a synthetic secret in a lab namespace.
2. Review who can get, list and watch secrets.
3. Inspect which pods mount the secret.
4. Confirm secret is not stored in Git, Helm values, ConfigMaps or image layers.
5. Review cluster documentation/configuration for encryption at rest of API data.
6. Review external secret manager integration if present.
7. Restrict secret access to the intended service account.
8. Test access from an unrelated namespace identity and confirm denial.
9. Rotate the synthetic value and verify application reload behavior.
10. Delete the secret and verify dependent workloads no longer use it.

**Expected result:** Secret read scope is minimal and encryption/configuration claims are supported by evidence.

**Evidence:** RBAC, mount map, encryption configuration and access tests. Do not capture secret value.

**Teardown:** Delete synthetic secret and test namespace.

## 17. Lab 14 — Kubernetes NetworkPolicy enforcement

**Objective:** Confirm the network plugin enforces namespace and pod traffic policy.

**Prerequisites:** Local cluster with a CNI that supports NetworkPolicy.

### Procedure

1. Deploy synthetic frontend, API and database pods in separate namespaces.
2. Verify baseline connectivity.
3. Apply default-deny ingress and egress policy to the database namespace.
4. Add an allow rule for the API pod only.
5. Verify API-to-database traffic succeeds.
6. Verify frontend-to-database traffic fails.
7. Verify an unrelated namespace cannot reach the database.
8. Add required DNS/telemetry flows where needed.
9. Remove the NetworkPolicy in the lab and observe whether behavior changes, proving the CNI enforces it.
10. Document any unsupported policy behavior.

**Expected result:** Only explicitly permitted service flows succeed.

**Evidence:** NetworkPolicy manifests and connectivity matrix.

**Teardown:** Delete namespaces and policies.

## 18. Lab 15 — Container registry and image provenance

**Objective:** Verify production deployment accepts only trusted image artifacts.

**Prerequisites:** Local registry or dedicated private registry and synthetic image.

### Procedure

1. Build a synthetic application image.
2. Record source commit, image digest and build identity.
3. Generate an SBOM and provenance statement using approved tooling.
4. Sign the image or artifact with a test signing identity.
5. Configure a verification step before deployment.
6. Deploy the signed digest and record success.
7. Create a different unsigned test image.
8. Attempt deployment of the unsigned image in a disposable namespace.
9. Verify policy denies or flags the artifact according to enforcement mode.
10. Rotate the test signing identity and verify revocation behavior.

**Expected result:** Artifact identity and provenance are verified, not inferred from a mutable tag.

**Evidence:** Digest, SBOM, attestation, signature verification and admission result.

**Teardown:** Delete images, registry credentials and test signing keys.

## 19. Lab 16 — Serverless function identity and event validation

**Objective:** Ensure function execution authority and event trust are narrowly scoped.

**Prerequisites:** Local function emulator or disposable cloud function with synthetic queue/bucket.

### Procedure

1. Deploy a function that processes a synthetic event.
2. Inventory its trigger, invocation permission and runtime identity.
3. Review permissions to queues, storage, databases and secrets.
4. Create a distinct runtime identity with only required resource access.
5. Submit a valid event and confirm processing.
6. Submit malformed, oversized and unauthorized event payloads.
7. Replay the same event and verify idempotency.
8. Test duplicate, delayed and out-of-order events.
9. Review dead-letter queue access and sensitive logging.
10. Remove unused trigger and permissions.

**Expected result:** Function accepts only valid events and cannot access unrelated cloud resources.

**Evidence:** Trigger policy, role permission matrix and event processing logs.

**Teardown:** Delete function, trigger, queue and synthetic data.

## 20. Lab 17 — Infrastructure as Code misconfiguration and state protection

**Objective:** Detect insecure infrastructure definitions and protect deployment state.

**Prerequisites:** Local IaC workspace or disposable cloud sandbox.

### Procedure

1. Create a sample template with a private storage resource and least-privilege identity.
2. Add controlled misconfigurations such as public access, broad network ingress or unencrypted storage.
3. Run an approved IaC scanner and record findings.
4. Review scanner coverage and false positives manually.
5. Generate a plan and inspect destructive changes.
6. Configure remote state with encryption, access control and locking where supported.
7. Confirm state and plan files are excluded from source control.
8. Introduce a synthetic sensitive value and inspect how it appears in state/output.
9. Remove secret material from IaC inputs and use a secure secret reference.
10. Re-run scans and plan review before apply.

**Expected result:** Misconfigurations are detected and state/plan data is protected.

**Evidence:** IaC diff, scan results, plan review and backend configuration.

**Teardown:** Destroy only resources created by this lab; verify state and backend cleanup.

## 21. Lab 18 — CI/CD workload identity and runner isolation

**Objective:** Validate that untrusted build inputs cannot access production credentials.

**Prerequisites:** Training repository and isolated CI environment.

### Procedure

1. Draw source, pull request, runner, artifact and deployment trust boundaries.
2. Inventory workflow token permissions and secrets.
3. Separate untrusted pull-request validation from privileged deployment.
4. Use an ephemeral or isolated runner for untrusted code.
5. Configure a federated deployment identity restricted to the approved repository/workflow/environment.
6. Remove long-lived cloud keys from pipeline variables.
7. Attempt to access production secrets from the untrusted validation workflow in the lab.
8. Verify the workflow has no deployment authority.
9. Generate artifact digest and provenance from the trusted build.
10. Require an approved environment promotion before deployment.

**Expected result:** Untrusted build inputs cannot obtain production secrets or deployment privileges.

**Evidence:** Workflow permission diff, federation trust, runner lifecycle and denied access logs.

**Teardown:** Revoke test federation and delete runner registration.

## 22. Lab 19 — Cloud audit logging and tamper protection

**Objective:** Verify that control-plane and workload audit records reach an independently protected destination.

**Prerequisites:** Sandbox account/project and central test log destination.

### Procedure

1. Identify required control-plane, identity, network and data access logs.
2. Enable supported audit sources for the lab.
3. Route logs to a separate security/log archive boundary where feasible.
4. Restrict workload identities to write-only or narrowly scoped log ingestion.
5. Restrict log deletion and retention changes to a separate administrator role.
6. Generate known test events such as role assignment, policy change and resource access.
7. Verify event completeness, timestamps, principal and resource context.
8. Attempt a prohibited log deletion using the workload identity and confirm denial.
9. Generate an alert for audit sink or retention policy changes.
10. Document gaps and retention constraints.

**Expected result:** Security-relevant events are collected and protected from ordinary workload administrators.

**Evidence:** Log source matrix, event samples and access policy.

**Teardown:** Remove only test resources; preserve approved audit evidence until retention expiry.

## 23. Lab 20 — Cloud secret exposure and rotation response

**Objective:** Practice containing a synthetic exposed cloud credential.

**Prerequisites:** Disposable test identity with low-risk permissions and a synthetic secret.

### Procedure

1. Create a test credential with minimal access to one synthetic resource.
2. Store it in a controlled test repository or configuration path as the exercise trigger.
3. Run approved secret scanning and record detection.
4. Revoke or rotate the credential using the documented process.
5. Review audit logs for use during the exposure window.
6. Identify dependent workloads and cached tokens.
7. Move the application to workload identity or approved secret manager.
8. Verify the old credential no longer works.
9. Verify the workload continues to perform its required operation.
10. Record time to detection, revocation and full remediation.

**Expected result:** Credential exposure can be detected, contained and remediated without leaving stale access.

**Evidence:** Redacted finding, revocation event and successful workload retest.

**Teardown:** Delete test identity and resource.

## 24. Lab 21 — Cloud detection engineering tabletop

**Objective:** Validate detection and response for privilege escalation, image compromise and public storage exposure.

**Prerequisites:** Mock telemetry or controlled sandbox events.

### Procedure

1. Define the three scenarios and expected alert owners.
2. Record required event sources and data fields.
3. Generate an approved test role assignment or policy change.
4. Deploy an unapproved synthetic image digest in a disposable namespace.
5. Change a test storage policy to simulate public exposure.
6. Verify alerts contain principal, resource, action, timestamp and environment.
7. Route each alert to the correct owner/runbook.
8. Measure detection latency and triage completeness.
9. Record false positives and missing telemetry.
10. Update rules and repeat the simulation.

**Expected result:** Alerts are actionable, routed and linked to containment procedures.

**Evidence:** Detection rule, sanitized events, alert screenshots/export and response timeline.

**Teardown:** Revert test policies, remove image and close mock incidents.

## 25. Lab 22 — Backup integrity and recovery test

**Objective:** Verify recovery of a synthetic application and data set from protected backups.

**Prerequisites:** Disposable application, database and approved backup target.

### Procedure

1. Define synthetic data, RTO and RPO for the exercise.
2. Create a known-good application release and database snapshot.
3. Verify backup encryption, access policy and retention.
4. Simulate logical data corruption in the disposable environment.
5. Restore to an isolated recovery environment.
6. Verify artifact provenance and database integrity.
7. Confirm secrets and identities are re-established through approved process, not restored blindly from compromised state.
8. Test application startup and access controls.
9. Measure recovery time and data loss against RTO/RPO.
10. Record gaps in backup isolation, immutability and recovery automation.

**Expected result:** Recovery produces a trusted, functioning application with validated data and access controls.

**Evidence:** Restore log, integrity checks and RTO/RPO measurement.

**Teardown:** Delete temporary recovery environment after evidence approval.

## 26. Lab 23 — Multi-tenant cloud application isolation

**Objective:** Validate tenant separation across API, database, object storage and workload identity.

**Prerequisites:** Synthetic multi-tenant application with two test tenants.

### Procedure

1. Create two synthetic tenants and separate test users.
2. Map tenant identity through authentication to backend authorization.
3. Identify database, storage and queue isolation design.
4. Execute valid tenant A operations.
5. Modify client-supplied tenant and object identifiers.
6. Attempt cross-tenant object reads and writes.
7. Test background jobs and event consumers for tenant context confusion.
8. Review workload identity permissions and storage policies.
9. Inspect logs for unauthorized cross-tenant attempts.
10. Add regression tests for all discovered trust boundaries.

**Expected result:** Tenant identity is derived from authenticated server-side context and enforced in every data path.

**Evidence:** Tenant data-flow map, negative test matrix and sanitized logs.

**Teardown:** Delete synthetic tenants and records.

## 27. Lab 24 — Cloud-native incident response exercise

**Objective:** Practice coordinated response to a combined CI credential and workload identity compromise.

**Prerequisites:** Mock incident timeline and sandbox audit events.

### Scenario

A build runner token is suspected to be compromised. A new deployment appears in a cluster, and the workload begins accessing an unexpected object storage path.

### Procedure

1. Assign incident commander, cloud owner, platform owner, AppSec, SOC and privacy/legal roles.
2. Establish incident scope and timeline.
3. Identify source repository, runner, workflow, artifact digest and deployment identity.
4. Revoke affected pipeline and workload credentials.
5. Preserve cloud audit, identity, registry, cluster and application logs.
6. Determine whether the image is trusted and whether provenance is valid.
7. Isolate the affected workload without destroying evidence.
8. Determine data access and tenant impact.
9. Rebuild from trusted source and redeploy a verified artifact.
10. Rotate secrets and review cross-account trust.
11. Validate that unauthorized identity and image paths are closed.
12. Record lessons learned and control improvements.

**Expected result:** Team can contain the incident, preserve evidence, determine blast radius and restore from trusted artifacts.

**Evidence:** Timeline, decision log, identity revocation, artifact provenance and recovery record.

**Teardown:** Revoke all exercise identities and reset sandbox resources.

## 28. Assessment rubric

| Criterion | Points |
|---|---:|
| Cloud inventory, ownership and threat model | 10 |
| Human and workload IAM | 15 |
| Network, storage and metadata protections | 10 |
| Container build and runtime security | 15 |
| Kubernetes API, RBAC, admission and network policy | 15 |
| Serverless, events and managed services | 5 |
| IaC, CI/CD and artifact provenance | 10 |
| Monitoring, incident response and recovery | 10 |
| Evidence quality and remediation | 5 |
| Safe cleanup and cost control | 5 |
| **Total** | **100** |

Suggested training interpretation: 90–100 strong independent engineering; 75–89 competent with review; 60–74 guided remediation required; below 60 repeat the exercises. These are educational thresholds, not a certification.

## 29. Instructor review checklist

- Was the scope explicitly authorized and isolated?
- Were cloud costs and resource cleanup controlled?
- Were account/project/subscription boundaries identified?
- Were human and workload identities assessed separately?
- Were long-lived credentials removed from the workload?
- Were network and egress policies actually enforced?
- Was metadata access tested only against a local mock endpoint or explicitly authorized sandbox?
- Were images pinned, scanned and tied to provenance?
- Were Kubernetes RBAC and pod policies tested with positive and negative cases?
- Was NetworkPolicy enforcement verified with the deployed CNI?
- Were Kubernetes secrets treated as sensitive rather than base64-protected?
- Were serverless triggers and event replay handled?
- Were IaC state and CI/CD identities protected?
- Were audit logs independently protected?
- Was recovery tested from a trusted artifact and backup?
- Were cross-tenant tests performed with synthetic data?
- Was evidence sanitized and cleanup verified?

## 30. References

1. AWS Well-Architected Security Pillar: https://docs.aws.amazon.com/wellarchitected/latest/framework/security.html
2. Microsoft Cloud Security Benchmark: https://learn.microsoft.com/en-us/security/benchmark/azure/
3. Google Cloud Security, Privacy and Compliance pillar: https://docs.cloud.google.com/architecture/framework/security
4. Kubernetes Security Concepts: https://kubernetes.io/docs/concepts/security/
5. Kubernetes Application Security Checklist: https://kubernetes.io/docs/concepts/security/application-security-checklist/
6. CIS Kubernetes Benchmarks: https://www.cisecurity.org/benchmark/kubernetes
7. NIST SP 800-190: https://csrc.nist.gov/pubs/sp/800/190/final
8. NIST SP 800-218 SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
9. Google Cloud Enterprise Foundations Blueprint: https://docs.cloud.google.com/architecture/blueprints/security-foundations

## 31. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial cloud-native application security lab specifications |
