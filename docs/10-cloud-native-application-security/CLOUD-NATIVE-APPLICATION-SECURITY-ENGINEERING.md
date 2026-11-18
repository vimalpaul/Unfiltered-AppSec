# Cloud-Native Application Security Engineering

| Field | Value |
|---|---|
| Document ID | UAPPSEC-10-001 |
| Status | Draft engineering baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-18 |
| Last reviewed | 2026-11-18 |
| Review due | 2027-02-18 |
| Scope | AWS, Microsoft Azure, Google Cloud, containers, Kubernetes, serverless, cloud workloads and application-to-cloud trust |
| Classification | Public |

## 1. Executive summary

Cloud-native application security is the engineering discipline of protecting applications that use cloud control planes, managed services, container platforms, orchestration, serverless execution, identity federation, software delivery pipelines and dynamically provisioned infrastructure.

The attack surface is larger than the application's HTTP endpoints. It includes cloud organizations and accounts, management APIs, identity providers, service principals, workload identities, metadata services, build runners, registries, image layers, admission controllers, Kubernetes API servers, service accounts, secrets, storage buckets, event triggers, serverless permissions, managed databases, observability pipelines and recovery systems.

A cloud-hosted application can be compromised through a vulnerable application endpoint, a stolen CI credential, an overprivileged workload identity, a public object store, a malicious container image, an exposed orchestration API, a metadata-service request forgery, an unsafe deployment template or a weak cloud control-plane configuration. These paths often combine. A low-severity application weakness may become a cloud account compromise when the workload has broad permissions; a cloud identity compromise may become a data breach when the role can read multiple tenants' storage.

The engineering objective is to constrain authority, reduce exposed paths, isolate workloads and tenants, protect data and secrets, verify the software and infrastructure supply chain, detect control-plane and runtime abuse, and make recovery possible. Security must be implemented across organization, account/subscription/project, network, identity, workload, application, data, pipeline and operations layers.

This chapter deliberately separates:
- **Application security:** code, business logic, API authorization, input handling, session management and application-level data access.
- **Cloud platform security:** account governance, cloud IAM, management-plane configuration, network boundaries, managed service configuration and provider-native security controls.
- **Container and orchestration security:** image construction, runtime isolation, cluster API, workload admission, service accounts, node and control-plane configuration.
- **Delivery and supply-chain security:** source, dependencies, build runners, artifacts, registries, deployment identities, provenance and release approvals.
- **Operational security:** telemetry, detection, incident response, backup, recovery and continuous posture management.

These are connected responsibilities. They must not be collapsed into a vague statement that "the cloud provider secures the cloud." Shared responsibility varies by service model, configuration and contractual arrangement.

## 2. Purpose, audience and applicability

### 2.1 Purpose

Provide a reusable engineering reference for designing, implementing, reviewing, testing and operating cloud-native applications. It supports architecture reviews, product security programs, DevSecOps, cloud security engineering, penetration testing, platform engineering, vulnerability management, audits and incident response.

### 2.2 Audience

- Application security engineers and product security teams.
- Cloud security architects and engineers.
- Platform engineering, DevOps and SRE teams.
- Developers and software architects.
- Container and Kubernetes platform operators.
- SOC, detection engineering and incident response.
- Risk, compliance, privacy and audit professionals.
- Consultants and authorized assessors.

### 2.3 Systems in scope

- Public cloud workloads on AWS, Microsoft Azure and Google Cloud.
- Hybrid and multi-cloud application architectures.
- Containerized applications and registries.
- Kubernetes and managed Kubernetes services.
- Serverless functions and event-driven applications.
- Managed databases, queues, object stores, caches and API gateways.
- Cloud IAM, workload identity and secrets/key management.
- Infrastructure as Code (IaC) and deployment pipelines.
- Service mesh, ingress, egress and private connectivity.
- Cloud logging, monitoring, detection and recovery services.

### 2.4 Out of scope and specialist dependencies

This chapter is not a complete cloud provider configuration manual, cloud penetration testing authorization, digital forensics handbook, network engineering textbook or cloud legal opinion. Provider-specific implementation must be validated against current service documentation, region, SKU, API version, platform mode and organizational policy. Physical data-center security and provider internal control implementation are generally provider responsibilities, but customer assurance and contractual review remain necessary.

## 3. Core terminology

| Term | Meaning in this playbook |
|---|---|
| Cloud control plane | Provider management interfaces and APIs used to create, configure and govern resources |
| Data plane | Workload-facing execution and data processing path |
| Management plane | Identity, policy, organization and administrative operations that govern resources |
| Landing zone | Governed cloud foundation for identity, networking, logging, policy and workload deployment |
| Workload identity | Identity assigned to an application, service, pod or runtime rather than a human |
| Federation | Trust arrangement that allows an external identity to obtain scoped cloud credentials |
| Managed identity/service account | Provider-managed identity mechanism that avoids embedding long-lived credentials |
| Container image | Immutable or versioned package used to instantiate a container |
| Registry | Repository for container images and related artifacts |
| Admission control | Policy enforcement during Kubernetes API object creation or update |
| Pod Security Standards | Kubernetes security profiles for pod configuration |
| Runtime security | Controls and observations applied while workloads execute |
| IaC | Declarative or programmatic definition of infrastructure and cloud resources |
| SBOM | Software Bill of Materials describing software components |
| Provenance | Evidence describing where, how and from which inputs an artifact was built |
| CSPM | Cloud Security Posture Management |
| CWPP | Cloud Workload Protection Platform |
| CNAPP | Cloud-Native Application Protection Platform; product category combining cloud workload, posture and related capabilities |
| SSRF | Server-Side Request Forgery |
| IMDS | Instance Metadata Service |
| KMS | Key Management Service |
| HSM | Hardware Security Module |

## 4. Cloud-native reference architecture

### 4.1 Logical architecture

~~~mermaid
flowchart TB
    subgraph GOV["Organization / Cloud Governance"]
      IDP["Workforce IdP / SSO / MFA"]
      ORG["Org, Accounts, Subscriptions, Projects"]
      POL["Policy, Guardrails, Audit and Billing"]
      SEC["Central Security and Logging"]
    end
    subgraph DELIVERY["Software Delivery Trust Zone"]
      SCM["Source Control"]
      CI["CI Build Runners"]
      SCAN["SAST / SCA / IaC / Secret / Image Scans"]
      SIGN["Artifact Signing and Provenance"]
      REG["Private Artifact Registry"]
    end
    subgraph CLOUD["Workload Cloud Boundary"]
      EDGE["DNS / CDN / WAF / API Gateway"]
      NET["Network Segmentation / Private Endpoints"]
      K8S["Kubernetes / Container Platform"]
      FN["Serverless / Event Functions"]
      ID["Workload Identity / Federation"]
      DATA["Managed DB / Object Storage / Queues"]
      KMS["KMS / HSM / Secrets"]
      OBS["Logs / Metrics / Traces"]
    end
    USERS["Users / External Systems"] --> EDGE
    SCM --> CI --> SCAN --> SIGN --> REG
    REG --> K8S
    REG --> FN
    IDP --> ORG
    ORG --> POL
    POL --> CLOUD
    EDGE --> NET
    NET --> K8S
    NET --> FN
    K8S --> ID
    FN --> ID
    ID --> DATA
    ID --> KMS
    K8S --> OBS
    FN --> OBS
    DATA --> OBS
    OBS --> SEC
    GOV --> SEC
~~~

The diagram is conceptual. A production design must identify real accounts/projects, network boundaries, identity issuers, resource policies, private endpoints, cluster/API exposure, registry trust, deployment identities, logging destinations and data residency.

### 4.2 Control plane and data plane separation

Treat provider management APIs as a high-value control plane. A principal that can modify identity, policies, network routes, audit settings, cluster configuration, encryption keys or deployment roles may gain authority over many workloads.

Review separately:
- Human administrator access.
- CI/CD deployment access.
- Workload runtime access.
- Break-glass access.
- Provider support and delegated administration.
- Cross-account/project/subscription trust.
- Data-plane application access.

Do not grant application runtime identities permission to administer their own cloud environment unless a narrowly justified product requirement exists.

### 4.3 Trust boundaries

A typical cloud-native system includes at least these boundaries:
1. Human workforce identity to cloud management plane.
2. Source repository to build runner.
3. Build runner to artifact registry.
4. Registry to deployment controller.
5. Cluster API to workload admission.
6. Workload to cloud service identity.
7. Workload to database/object store/queue.
8. Workload to metadata service.
9. Workload to external network and third-party APIs.
10. Tenant A to tenant B.
11. Production to non-production.
12. Workload telemetry to central security platform.
13. Cloud provider managed service boundary to customer-managed configuration.

Each boundary needs an owner, authentication model, authorization policy, data classification, telemetry and failure behavior.

## 5. Threat model

### 5.1 Adversary profiles

- External attacker exploiting an exposed application or service.
- Attacker using stolen workforce or cloud credentials.
- Malicious or compromised developer, contractor or supplier.
- Compromised CI runner, source repository, package or registry.
- Attacker with access to a container or pod.
- Malicious tenant or customer abusing shared infrastructure.
- Attacker exploiting cloud misconfiguration or public exposure.
- Insider abusing control-plane privileges.
- Ransomware or extortion operator targeting data and recovery systems.
- Opportunistic attacker chaining SSRF, metadata access and cloud IAM permissions.

### 5.2 High-value assets

- Organization root/management accounts and identity federation.
- Cloud IAM roles, service principals, service accounts and access tokens.
- CI/CD credentials and signing keys.
- Source code, build systems, artifacts and registries.
- Cluster API, control plane, nodes and admission configuration.
- Secrets, KMS keys, certificates and private keys.
- Customer records, object stores, databases and backups.
- Network topology, DNS, private endpoints and firewall policies.
- Logs, audit trails, detection rules and security tooling.
- Deployment manifests, Terraform state and environment variables.
- Tenant boundary enforcement and authorization policies.

### 5.3 Attack paths

| Attack path | Preconditions | Potential impact | Key controls |
|---|---|---|---|
| Public application SSRF to metadata | Reachable URL fetcher, weak egress/metadata protections | Workload credential theft and cloud API access | URL allowlist, egress control, metadata protections, least privilege |
| CI runner compromise | Untrusted build input or runner isolation failure | Source, artifact or cloud deployment compromise | Ephemeral isolated runners, scoped identity, provenance, approvals |
| Overprivileged workload identity | Broad role attached to app or pod | Cross-service data access or control-plane changes | Workload identity, resource-scoped roles, permission analysis |
| Public object storage | Misconfigured bucket/container policy | Data exposure or tampering | Block public access, policy guardrails, access logging |
| Container escape or host access | Vulnerable runtime/kernel or privileged container | Node/cluster compromise | Non-root, capabilities drop, sandboxing, patching, node isolation |
| Kubernetes API abuse | Exposed API or excessive RBAC | Workload creation, secret access, persistence | Private API, MFA/SSO, RBAC, admission, audit |
| Poisoned image | Untrusted registry or mutable tag | Malicious code execution | Trusted registry, digest pinning, signature/provenance verification |
| Secret leakage | Secret in image, env, logs or CI output | Credential compromise | Secret manager, short-lived credentials, scanning and rotation |
| Cross-tenant authorization flaw | Shared service or storage without strong isolation | Tenant data disclosure or modification | Server-side tenant authorization, isolation tests, resource policies |
| Log pipeline compromise | Broad write/admin access or unprotected telemetry | Evidence deletion or alert suppression | Separate security account/project, immutable retention, restricted writers |
| IaC state exposure | State file contains secrets or resource metadata | Credential and architecture disclosure | Encrypted remote state, strict access, locking, secret minimization |
| Serverless event injection | Public trigger or weak event validation | Privileged function invocation or data corruption | Trigger auth, schema validation, least privilege, idempotency |

### 5.4 Threat modeling procedure

1. Define workload purpose, business owner, environment and criticality.
2. Inventory cloud accounts/projects/subscriptions, services and regions.
3. Draw deployment and data-flow diagrams.
4. Identify human, machine, workload and provider identities.
5. Mark control-plane and data-plane boundaries.
6. Inventory sensitive data and keys.
7. Enumerate public ingress, egress, event triggers and management interfaces.
8. Enumerate trust relationships to CI/CD, registry, SaaS and third parties.
9. Apply STRIDE, abuse cases and attack-path reasoning.
10. Record threats with asset, precondition, path, impact, likelihood, controls, residual risk and owner.
11. Define testable requirements and detection signals.
12. Review when architecture, identity, service exposure or provider configuration changes.

## 6. Shared responsibility and service model

Shared responsibility must be documented per service, not copied from a generic cloud diagram.

| Layer | Typical provider responsibility | Typical customer responsibility |
|---|---|---|
| Physical facilities | Facilities, hardware, physical access | Provider assurance and contract review |
| Core cloud infrastructure | Provider platform, hypervisor and managed fabric | Correct service selection and configuration |
| Managed database | Service infrastructure and managed engine operations as defined by service | Network access, database users, data classification, encryption options, backup policy and application authorization |
| Managed Kubernetes control plane | Provider-operated control plane components for managed offering | Cluster identity, node/workload config, RBAC, admission, network policy, secrets, images and application security |
| Serverless runtime | Provider execution infrastructure | Function code, triggers, identity permissions, dependencies, secrets, data access and event validation |
| Containers | Provider infrastructure only where managed service applies | Image, process, runtime configuration, host/cluster mode and application |
| SaaS | Depends on product and contract | Tenant configuration, identity, data, users, integrations and usage |
| Identity | Provider may offer identity platform | Federation configuration, lifecycle, MFA, privileged roles and workload trust |

For each service record: service model, provider/customer control split, exact service documentation, configuration owner, inherited controls, customer evidence, residual risk and review date.

## 7. Cloud foundation and account governance

### 7.1 Landing-zone security

Establish a governed foundation before deploying production workloads.

Required design decisions:
- Organization hierarchy and account/subscription/project boundaries.
- Production/non-production and security/log archive separation.
- Central identity federation and privileged access.
- Network hub/spoke or equivalent connectivity model.
- Centralized logging and audit retention.
- Security policy and preventive guardrails.
- Approved regions and data residency decisions.
- Naming, tagging, ownership and asset inventory.
- Key management and secret-management standards.
- Backup and recovery architecture.
- Break-glass access and emergency operations.
- Cost and quota abuse controls.

### 7.2 Account separation

Use separate administrative boundaries for production, development, security tooling and log archive where feasible. Account separation reduces blast radius but does not automatically guarantee isolation if organization-level roles, shared identity, network routes, keys or CI deployment roles cross boundaries.

Review:
- Cross-account role trust.
- Organization management permissions.
- Subscription/project hierarchy inheritance.
- Shared VPC/network and DNS dependencies.
- Centralized key and logging permissions.
- Deployment automation and service connections.
- Break-glass access and support roles.

### 7.3 Guardrails

Use preventive policy where possible and detective monitoring where prevention is not feasible.

Examples:
- Deny public storage unless an approved exception exists.
- Restrict allowed regions for regulated workloads.
- Require encryption and approved key policies.
- Deny privileged container settings in standard namespaces.
- Require image provenance or signature policy for sensitive workloads.
- Prevent disabling audit logging.
- Require resource tags and ownership.
- Restrict internet-exposed management endpoints.
- Require approved backup and retention configuration.

Guardrails must have an exception process, expiry, owner, compensating controls and monitoring. A policy that silently blocks legitimate recovery or emergency response can itself create operational risk.

## 8. Cloud IAM and workload identity

### 8.1 Human identity

- Federate workforce identities through the approved identity provider.
- Require phishing-resistant MFA for high-impact administration where supported and proportionate.
- Avoid shared human accounts.
- Use just-in-time or time-bound privileged access where available.
- Separate read-only audit, operator, deployer and security administrator roles.
- Review role assignments and external guests periodically.
- Protect recovery and break-glass identities.
- Alert on privilege escalation, new trust relationships and policy changes.

### 8.2 Workload identity

Prefer short-lived federated or provider-managed workload credentials over long-lived static access keys embedded in code, images, environment files or pipeline variables.

Design:
1. Give each workload a distinct identity where practical.
2. Bind the identity to a specific runtime, namespace, service account, repository or deployment context.
3. Scope permissions to required actions and resources.
4. Limit token lifetime and audience.
5. Prevent arbitrary workloads from impersonating privileged identities.
6. Separate deployment identity from runtime identity.
7. Rotate/revoke credentials and trust when workloads or repositories are retired.
8. Monitor credential issuance and sensitive API use.

### 8.3 AWS implementation considerations

- Use IAM roles and temporary credentials for workloads.
- Review trust policies, principal scope, conditions and external IDs where relevant.
- Review service roles, instance profiles, task roles and pod identity mechanisms separately.
- Use permission boundaries, organization guardrails and resource policies where appropriate.
- Avoid long-lived IAM user access keys for application workloads.
- Review resource-based policies for public or cross-account access.
- Analyze effective permissions, including policy interactions and explicit denies.
- Restrict role passing and privilege delegation.

### 8.4 Microsoft Azure implementation considerations

- Prefer managed identities for supported workloads.
- Distinguish system-assigned and user-assigned identity lifecycle.
- Review service principals, app registrations, federated identity credentials and workload identity federation.
- Scope Azure role assignments at the narrowest suitable scope.
- Review directory roles separately from Azure resource roles.
- Protect service connection credentials and federated deployment identities.
- Review Key Vault data-plane permissions separately from management-plane permissions.
- Detect credential creation, consent grants and role assignment changes.

### 8.5 Google Cloud implementation considerations

- Prefer attached service accounts or Workload Identity Federation over service account key files.
- Restrict service account impersonation and token creation permissions.
- Avoid user-managed service account keys unless justified.
- Review project/folder/organization inheritance.
- Use least-privilege IAM roles and resource-level policies where supported.
- Review service account attachment and actAs-style delegation paths.
- Protect workload identity pools and provider trust conditions.
- Monitor service account key creation, policy changes and sensitive API calls.

Provider service names and capabilities evolve. Confirm current documentation and feature availability for the selected region, cluster mode and runtime before implementation.

## 9. Secrets, certificates and key management

### 9.1 Secret handling principles

- Do not commit secrets to source control, Dockerfiles, image layers, Terraform state or logs.
- Do not assume environment variables are secret storage; they may appear in process inspection, crash dumps or diagnostics.
- Retrieve secrets at runtime through an approved secrets manager or workload identity flow.
- Minimize secret lifetime and scope.
- Separate secret access from secret administration.
- Rotate after exposure and when ownership or trust changes.
- Record access and secret version changes.
- Avoid exposing secret values to build logs, tracing or support tools.

### 9.2 Key management

Define:
- Key owner and data owner.
- Purpose and allowed algorithms.
- Key hierarchy and envelope encryption model.
- Key creation and protection.
- Access policy and separation of duties.
- Rotation and versioning.
- Backup, recovery and regional resilience.
- Revocation, disablement and destruction.
- Audit and evidence.
- Migration and cryptographic agility.

Do not confuse encryption with authorization. A workload that can decrypt every tenant's data has a broad blast radius even if the data is encrypted at rest.

### 9.3 Secret exposure response

1. Identify secret type, owner, scope and last known exposure.
2. Revoke or rotate credentials using a tested process.
3. Determine whether the secret was used and by whom.
4. Review cloud audit and application logs.
5. Identify dependent services and cached tokens.
6. Remove secret from source, image, artifact and pipeline output where feasible.
7. Preserve evidence and investigate root cause.
8. Add preventive scanning and policy.
9. Retest and record closure.

## 10. Network and service exposure

### 10.1 Network design

- Use private subnets or equivalent private network placement for internal workloads where suitable.
- Expose only intended ingress through managed edge, WAF, API gateway or load balancer.
- Restrict management APIs and cluster control planes.
- Segment production, non-production, data and management traffic.
- Define egress policy and DNS controls.
- Use private endpoints/service endpoints where appropriate.
- Review peering, transit gateways, VPNs and private connectivity as trust relationships.
- Prevent accidental public IP assignment to sensitive workloads.
- Monitor route, firewall, security group and DNS changes.

### 10.2 Egress security

Unrestricted egress enables data exfiltration, command-and-control and SSRF pivoting.

For sensitive workloads:
1. Identify required outbound destinations and protocols.
2. Use controlled egress gateways or network policies.
3. Restrict metadata service access where the platform supports it.
4. Separate package/repository access from runtime egress.
5. Log denied and unusual destinations.
6. Define emergency update and incident-response egress paths.
7. Validate DNS rebinding and redirect behavior in application URL fetchers.

### 10.3 Application SSRF and metadata services

Cloud metadata endpoints can provide instance or workload identity information. SSRF vulnerabilities may become cloud credential exposure if an application can reach metadata services or internal management endpoints.

Controls:
- Do not accept arbitrary URLs for server-side fetches.
- Use strict scheme, hostname, port and resolved-address allowlists.
- Resolve and validate all A/AAAA records and redirects.
- Block link-local, loopback, private, reserved and internal ranges unless explicitly needed.
- Revalidate after redirects and DNS resolution.
- Apply network egress restrictions.
- Use provider-supported metadata protections and token requirements where available.
- Ensure workload identity has minimal permissions even if token exposure occurs.
- Test IPv4, IPv6, alternate encodings, redirects, DNS rebinding and proxy behavior in a controlled lab.

Network blocking is defense in depth; application URL validation remains necessary.

## 11. Container image security

### 11.1 Image construction

- Use minimal, maintained base images.
- Pin base images by digest for reproducibility.
- Avoid unnecessary packages, shells and diagnostic tools in production images where feasible.
- Use multi-stage builds to keep build tools out of runtime images.
- Run as non-root unless a documented requirement exists.
- Set an explicit working directory and file permissions.
- Use read-only filesystem where compatible.
- Drop Linux capabilities and add only required capabilities.
- Avoid privileged mode and host namespace sharing.
- Do not bake secrets into image layers.
- Generate SBOM and provenance.
- Scan base and final images.
- Rebuild when base images or dependencies are patched.

### 11.2 Image provenance and registry

- Restrict registry write access.
- Separate build, staging and production promotion.
- Promote immutable artifacts rather than rebuilding differently per environment.
- Prefer digest references over mutable tags for deployment.
- Sign artifacts and verify signatures/provenance at admission or deployment.
- Restrict public image pulls where private images are required.
- Scan for vulnerabilities, malware indicators and secret material.
- Retain release metadata and image digests.
- Define image deprecation and emergency block procedures.

A vulnerability scanner does not prove an image is safe. It can miss unknown vulnerabilities, malicious behavior, build compromise and runtime configuration weaknesses.

## 12. Container runtime security

- Run as non-root and use an unprivileged UID/GID.
- Set allowPrivilegeEscalation to false where supported.
- Drop all unnecessary Linux capabilities.
- Apply seccomp and AppArmor/SELinux profiles where available.
- Avoid privileged containers.
- Avoid host PID, IPC and network namespaces unless required.
- Avoid hostPath mounts; tightly constrain any approved mount.
- Use read-only root filesystem where feasible.
- Set CPU and memory requests/limits.
- Restrict device access.
- Use runtime isolation such as gVisor or Kata Containers for workloads with stronger isolation requirements where supported.
- Patch host OS, kernel, container runtime and orchestration components.
- Monitor process, file, network and syscall behavior proportionately.

Containers share the host kernel in common runtime models. They are not equivalent to separate virtual machines. Isolation assumptions must reflect the runtime and threat model.

## 13. Kubernetes security engineering

### 13.1 Control plane and API server

- Restrict API server network exposure.
- Use approved authentication and authorization.
- Apply least-privilege RBAC.
- Separate cluster administration from namespace operations.
- Enable audit logging and protect log destinations.
- Review admission controllers and policy.
- Keep control plane and nodes on supported versions.
- Restrict etcd access and protect data at rest according to provider and cluster architecture.
- Review API server flags and managed-cluster configuration.
- Protect cluster bootstrap and certificate authority material.

### 13.2 RBAC

- Avoid wildcard verbs/resources unless justified.
- Avoid broad cluster-admin bindings.
- Do not grant workload identities rights to create privileged workloads or modify RBAC without a strong reason.
- Review bindings to groups and external identity claims.
- Separate read, deploy, operate and administer roles.
- Monitor RoleBinding/ClusterRoleBinding changes.
- Test effective access, including impersonation and delegated rights.
- Review escalation paths through pods, secrets, exec, port-forward and workload creation.

Kubernetes RBAC controls API actions, not all authorization decisions inside an application. Application-level tenant and object authorization remain separate.

### 13.3 Service accounts and workload identity

- Create dedicated service accounts for workloads.
- Avoid the default service account for application pods.
- Set automountServiceAccountToken to false unless API access is required.
- If a token is required, use projected, audience-bound, short-lived tokens where supported.
- Bind workload identity to the intended namespace/service account and external trust conditions.
- Avoid mounting broad cloud credentials into pods.
- Review impersonation and service account token creation permissions.
- Rotate/revoke identities when workload ownership changes.

### 13.4 Pod Security Standards

Use the Restricted profile as a target for general workloads where compatibility allows. Exceptions must be explicit and risk assessed.

Review:
- runAsNonRoot.
- allowPrivilegeEscalation.
- readOnlyRootFilesystem.
- capabilities.drop.
- seccompProfile.
- host namespace sharing.
- privileged mode.
- hostPath volumes.
- Linux user/group IDs.
- Windows host process settings where applicable.
- resource requests and limits.

Enforce through Pod Security Admission or an approved policy engine. Monitor policy violations and exception expiry.

### 13.5 Network policies

- Apply default-deny ingress and egress where supported and operationally appropriate.
- Allow only documented service-to-service flows.
- Restrict access to metadata endpoints and control-plane addresses.
- Separate namespaces and sensitive workloads.
- Verify the installed CNI actually enforces NetworkPolicy.
- Test DNS, health checks, telemetry and control dependencies.
- Use egress gateways or service mesh policy where needed.
- Review policy after every new dependency.

A NetworkPolicy object without an enforcing network plugin does not provide the intended isolation.

### 13.6 Secrets in Kubernetes

Kubernetes Secret objects are not automatically encrypted at rest in every cluster configuration. Base64 encoding is not encryption.

- Enable and verify encryption at rest for Kubernetes API data where applicable.
- Restrict Secret read/list/watch permissions.
- Avoid mounting all secrets into all containers.
- Prefer external secret managers and workload identity where appropriate.
- Use short-lived credentials.
- Avoid secrets in manifests, Helm values, ConfigMaps, Git and CI logs.
- Review etcd backup and access.
- Rotate and revoke after exposure.
- Monitor Secret reads and changes.

### 13.7 Admission control and policy as code

Use admission policies to enforce:
- Approved registries and image digest references.
- Signature/provenance verification for sensitive workloads.
- Non-root execution.
- No privileged containers.
- No host namespace or broad hostPath access.
- Resource limits.
- Required labels/ownership.
- Approved service accounts.
- No host ports unless approved.
- Restricted capabilities and security contexts.

Start with audit/warn modes where appropriate, measure compatibility, then enforce. Maintain break-glass policy and test admission changes in staging.

### 13.8 Multi-tenancy

Kubernetes namespaces are organizational boundaries, not strong isolation by themselves.

For hostile or highly regulated tenants, evaluate:
- Separate clusters or cloud accounts/projects.
- Dedicated node pools.
- Strong runtime isolation.
- Separate identities, secrets and storage.
- Network policy and egress controls.
- Resource quotas and noisy-neighbor protections.
- Admission restrictions.
- Control-plane and support access boundaries.

Choose isolation based on adversary capability, data sensitivity, regulatory obligations and business impact.

## 14. Serverless and event-driven application security

### 14.1 Function identity and permissions

- Use a distinct runtime identity for each function or trust domain.
- Restrict access to exact queues, buckets, topics, databases and secrets.
- Separate deployment permissions from execution permissions.
- Review invocation permissions and trigger policies.
- Avoid broad wildcard roles.
- Remove unused permissions and stale functions.
- Monitor role and trigger changes.

### 14.2 Event validation

Treat events from queues, object storage, webhooks, event buses and schedules as untrusted unless their origin and integrity are verified.

- Authenticate external event sources.
- Validate schema, size, encoding and required fields.
- Validate object ownership and tenant context.
- Enforce idempotency and replay controls.
- Handle duplicate, delayed and out-of-order events.
- Use dead-letter queues with restricted access.
- Avoid trusting event metadata as proof of authorization.
- Prevent recursive triggers and runaway invocation loops.
- Apply concurrency, timeout and resource limits.

### 14.3 Runtime and dependency security

- Pin runtime and dependency versions.
- Patch supported runtimes before end-of-life.
- Package only required libraries.
- Protect environment variables and secret references.
- Restrict network egress.
- Validate temporary storage lifecycle.
- Avoid sensitive payloads in logs.
- Monitor unusual invocation rate, errors, outbound calls and permission use.
- Test cold-start and warm execution behavior where state assumptions matter.

## 15. Managed services and data stores

For managed databases, queues, caches and object stores:
- Prefer private network access where available.
- Disable public endpoints unless justified.
- Enforce TLS and server identity validation.
- Use workload identity or managed authentication where supported.
- Restrict database users and service permissions.
- Separate management-plane and data-plane permissions.
- Encrypt at rest with approved key policy.
- Apply backup, retention and deletion controls.
- Enable access logging and data event auditing where available.
- Restrict cross-account/project access.
- Test tenant isolation at application and storage layers.
- Review snapshots, exports, replicas and analytics destinations.

A managed database does not automatically provide safe schema design, application authorization, tenant isolation or correct query construction.

## 16. Infrastructure as Code security

### 16.1 Secure IaC lifecycle

1. Define approved modules and provider versions.
2. Pin dependencies and module sources.
3. Review provider permissions and CI credentials.
4. Scan source for misconfiguration and secrets.
5. Validate policy as code.
6. Generate and review plans before apply.
7. Protect state and plan artifacts.
8. Require approvals for production changes.
9. Detect drift and unauthorized manual changes.
10. Record deployment identity and change evidence.

### 16.2 Terraform-specific considerations

- Protect remote state with encryption, access control and locking.
- Treat state as sensitive; it may contain secrets and resource attributes.
- Do not commit state or plan files.
- Use least-privilege provider credentials.
- Pin provider and module versions.
- Review plan output for destructive and public exposure changes.
- Use policy checks on planned values.
- Avoid secrets in plaintext variables and outputs.
- Restrict state workspace and backend access.
- Review import, destroy and replacement operations carefully.

### 16.3 CloudFormation, Bicep and Google Cloud deployment templates

Use approved modules, parameter validation, secure defaults, policy checks, least-privilege deployment identities and change review. Confirm that template scanning understands the provider resource types and current API versions. A clean scan is not proof that runtime access and data flows are safe.

## 17. CI/CD and software delivery trust

### 17.1 Pipeline threat model

The pipeline is a privileged production pathway. Threat model:
- Source branch and pull request permissions.
- Build runner host and isolation.
- Third-party actions/plugins/tasks.
- Dependency/package registries.
- Build secrets and identity tokens.
- Artifact storage and promotion.
- Signing and provenance.
- Deployment approvals and identities.
- Release workflow and rollback.

### 17.2 Secure pipeline requirements

- Use ephemeral or isolated runners for untrusted build inputs.
- Separate pull-request validation from privileged deployment.
- Pin third-party actions/tasks and dependencies to immutable versions or digests where supported.
- Restrict workflow token permissions.
- Use OIDC/federated deployment identity rather than static cloud keys where possible.
- Do not expose production secrets to untrusted forks or pull requests.
- Separate build and deployment roles.
- Generate SBOM and build provenance.
- Sign artifacts and verify them before deployment.
- Require approval for production and high-impact changes.
- Protect environment secrets and deployment branches.
- Retain logs and attestations.

### 17.3 Artifact promotion

Build once, verify once and promote the same immutable artifact through environments where feasible. Record:
- Source commit.
- Build workflow and runner identity.
- Dependency lockfiles and SBOM.
- Artifact digest.
- Signature and provenance.
- Scan results and exceptions.
- Approval identity.
- Deployment target and timestamp.
- Runtime version and configuration.

## 18. Cloud-native application security

Cloud platform controls do not replace application security.

For every service:
- Validate authentication and authorization at the application/API layer.
- Enforce tenant, object, property and function authorization.
- Validate input, output and serialized payloads.
- Protect sessions and tokens.
- Use secure headers and TLS.
- Prevent SSRF, injection, deserialization and business logic abuse.
- Apply rate limits and abuse detection.
- Protect secrets and personal data.
- Implement secure error handling and logging.
- Test service-to-service trust and identity propagation.
- Prevent confused-deputy behavior where one service exercises its authority on behalf of another.

## 19. Observability, monitoring and detection

### 19.1 Required telemetry sources

- Cloud control-plane audit events.
- Identity sign-in and token issuance.
- IAM role, policy and trust changes.
- Network flow, firewall, DNS and egress logs.
- Kubernetes API audit and admission events.
- Container runtime and node telemetry.
- Image registry and artifact provenance events.
- Serverless invocation, permission and trigger logs.
- Database/object access and administrative events.
- CI/CD workflow, runner and deployment logs.
- KMS and secret access.
- Backup, snapshot and restore events.

### 19.2 Detection catalogue

| Detection ID | Scenario | Signals | Initial response |
|---|---|---|---|
| CLOUD-D-001 | Privileged role creation or escalation | New admin role, policy attachment, trust change | Validate change ticket; suspend or revoke unauthorized grant |
| CLOUD-D-002 | Workload identity anomaly | New audience/issuer, unexpected token issuance or service identity use | Revoke trust/credential and isolate workload if needed |
| CLOUD-D-003 | Metadata/SSRF activity | Workload requests to metadata or unusual link-local destinations | Contain egress, inspect app path and rotate exposed credentials |
| CLOUD-D-004 | Public data exposure | Public bucket/container or permissive resource policy | Restrict access, preserve evidence and assess data impact |
| CLOUD-D-005 | Kubernetes privilege abuse | ClusterRoleBinding changes, exec, privileged pod or secret reads | Isolate namespace/node as appropriate and investigate identity |
| CLOUD-D-006 | Suspicious image deployment | Unapproved registry, digest/signature mismatch or critical image finding | Block rollout and revert to approved digest |
| CLOUD-D-007 | CI/CD compromise | Unusual runner, workflow permissions, secret access or deployment identity | Disable pipeline identity and preserve build evidence |
| CLOUD-D-008 | Logging tampering | Audit sink, retention, policy or collector changes | Protect independent logs and investigate control-plane actor |
| CLOUD-D-009 | Serverless abuse | Invocation spikes, unusual trigger, outbound destination or permission change | Disable trigger/function safely and investigate event source |
| CLOUD-D-010 | Data exfiltration | Unusual object reads, snapshots, exports or outbound volume | Contain access, preserve logs and assess affected records |
| CLOUD-D-011 | Key/secret misuse | Unusual decrypt, secret retrieval or key policy changes | Revoke identity, rotate credentials and review dependent services |
| CLOUD-D-012 | Backup tampering | Backup deletion, retention change or vault policy modification | Protect recovery copies and activate incident process |

Detection logic must be tuned to actual provider telemetry and workload behavior. A detection name is not a working alert until data source, query, thresholds, false-positive handling, owner, runbook and test evidence are defined.

## 20. Incident response and recovery

### 20.1 Cloud-native incident principles

- Preserve independent control-plane and identity logs.
- Identify compromised human, workload, pipeline and provider identities separately.
- Contain access without destroying evidence.
- Isolate affected workloads and network paths.
- Revoke or rotate credentials, tokens, keys and trust relationships.
- Identify artifact and image provenance.
- Determine data access and exfiltration scope.
- Preserve snapshots and forensic evidence under approved process.
- Rebuild from trusted source and verified artifacts rather than assuming a compromised runtime can be cleaned.
- Validate backup integrity and restore path.
- Review cross-account and cross-project blast radius.
- Coordinate legal, privacy, customer and regulator notification decisions with appropriate owners.

### 20.2 Scenario playbooks

**Cloud credential compromise:** identify identity and permissions; revoke sessions/keys; inspect token use; assess role assumption and resource access; rotate dependent secrets; review persistence; validate no new trust or policy remains.

**Container image compromise:** block digest; stop rollout; identify affected clusters and versions; preserve image and provenance; identify workload identity permissions; rotate secrets accessible to the workload; rebuild from trusted source; redeploy and verify.

**Kubernetes cluster compromise:** restrict API access; identify actor and RBAC path; preserve audit logs; assess node and control-plane scope; isolate affected workloads; rotate service account and cloud credentials; rebuild nodes/cluster if trust is lost; validate admission and network controls.

**Public storage exposure:** restrict access; preserve policy and access logs; identify object set and time window; assess reads/downloads; rotate exposed secrets; determine notification obligations with privacy/legal owners; verify replicas, snapshots and CDN caches.

**CI/CD compromise:** disable affected workflows and deployment identities; revoke tokens; preserve runner images and logs; inspect source, dependencies, artifacts and release history; invalidate compromised signatures/keys; rebuild and redeploy trusted artifacts.

## 21. Cloud-native security verification methodology

### 21.1 Assessment phases

1. Authorization, scope, cloud tenant/account identifiers and rules of engagement.
2. Architecture and service inventory.
3. Identity and access review.
4. Network and public exposure review.
5. Storage, data and key management review.
6. Container image and registry review.
7. Kubernetes control plane, RBAC, admission and pod configuration review.
8. Serverless trigger and execution identity review.
9. IaC and pipeline review.
10. Runtime and telemetry review.
11. Backup and recovery review.
12. Application/API authorization and SSRF review.
13. Threat detection and incident response validation.
14. Evidence, risk, remediation and retest.

### 21.2 Rules of engagement

- Obtain written authorization from the cloud tenant owner and relevant service owners.
- Confirm provider acceptable-use restrictions and any required provider approval.
- Identify exact accounts, subscriptions, projects, regions, clusters, namespaces, functions and APIs.
- Use dedicated test identities and synthetic data.
- Define whether production testing is allowed.
- Prohibit destructive resource deletion, uncontrolled load tests, credential spraying, public exploit deployment and data exfiltration.
- Define rate limits, testing windows, emergency contacts and stop conditions.
- Avoid modifying provider-managed control planes outside documented test methods.
- Preserve evidence securely and redact identifiers/secrets before reporting.
- Do not publish customer topology, account IDs, tokens, keys or internal addresses.

### 21.3 Test catalogue

The IDs below are internal project identifiers, not provider or standards control IDs.

| Test ID | Domain | Procedure focus | Expected result |
|---|---|---|---|
| CLOUD-T-001 | Asset inventory | Enumerate accounts, projects, subscriptions, regions and owners | All in-scope assets attributable |
| CLOUD-T-002 | Organization governance | Review hierarchy, guardrails and policy exceptions | Administrative boundaries and exceptions documented |
| CLOUD-T-003 | Human IAM | Review MFA, federation, privileged roles and stale identities | Human access is scoped and governed |
| CLOUD-T-004 | Workload identity | Trace runtime identity to exact permissions | No unnecessary static credentials or broad authority |
| CLOUD-T-005 | Cross-account trust | Review trust policies and external principals | Only intended trust relationships exist |
| CLOUD-T-006 | Public exposure | Identify public endpoints, IPs, storage and management interfaces | Exposure is intentional and approved |
| CLOUD-T-007 | Network segmentation | Validate route, firewall, security group and network policy behavior | Only intended traffic paths succeed |
| CLOUD-T-008 | Egress | Verify workload outbound allowlist and DNS controls | Unexpected egress is restricted and observable |
| CLOUD-T-009 | Metadata service | Test application URL fetchers and metadata protections in lab | SSRF cannot retrieve cloud credentials |
| CLOUD-T-010 | Secret hygiene | Inspect source, image, IaC, CI and logs for synthetic secrets | No exposed secrets; remediation/rotation works |
| CLOUD-T-011 | Key management | Review key policy, rotation, disable, recovery and audit | Key lifecycle and separation of duties defined |
| CLOUD-T-012 | Storage policy | Review public access, ACL/resource policy and cross-account access | Data access matches owner and classification |
| CLOUD-T-013 | Container image | Inspect base image, packages, user, layers and digest | Image is minimal, attributable and scanned |
| CLOUD-T-014 | Image provenance | Verify signature, SBOM and build attestation | Only approved artifacts are deployable |
| CLOUD-T-015 | Container runtime | Inspect privilege, capabilities, mounts, namespaces and resources | Workload is least-privileged and constrained |
| CLOUD-T-016 | Kubernetes API | Review exposure, authentication, authorization and audit | API access is restricted and traceable |
| CLOUD-T-017 | Kubernetes RBAC | Enumerate effective roles and escalation paths | No unjustified wildcard/admin permissions |
| CLOUD-T-018 | Pod security | Validate security context and Pod Security enforcement | Workloads meet approved baseline or exception |
| CLOUD-T-019 | Kubernetes secrets | Review encryption, RBAC, mounts and external secret integration | Secret exposure and read scope minimized |
| CLOUD-T-020 | NetworkPolicy | Verify CNI enforcement and allowed flows | Default-deny and required paths behave as designed |
| CLOUD-T-021 | Admission | Submit non-production policy-violating test workload | Disallowed workload is denied or reported per policy |
| CLOUD-T-022 | Multi-tenancy | Test namespace, storage and application tenant separation | Cross-tenant access denied |
| CLOUD-T-023 | Serverless identity | Review execution role and trigger permissions | Function authority is narrow and distinct |
| CLOUD-T-024 | Event security | Test schema, signature, replay and idempotency | Invalid or duplicate events safely rejected |
| CLOUD-T-025 | IaC | Scan templates, plan and state handling | Misconfiguration and sensitive state exposure controlled |
| CLOUD-T-026 | CI/CD | Review runner isolation, token permissions and deployment identity | Untrusted pipeline input cannot access production secrets |
| CLOUD-T-027 | Observability | Verify audit coverage, retention and tamper protection | Security events are captured and protected |
| CLOUD-T-028 | Detection | Simulate approved role, image and policy changes | Alerts reach owners with usable context |
| CLOUD-T-029 | Backup/recovery | Restore synthetic workload and data in isolated environment | Recovery meets defined integrity and RTO/RPO |
| CLOUD-T-030 | Application integration | Test API authorization, SSRF and secret access | App layer remains secure despite cloud hosting |
| CLOUD-T-031 | Vulnerability management | Compare images, hosts, services and dependencies to support status | Findings are prioritized by exposure and exploitability |
| CLOUD-T-032 | Release provenance | Trace deployed digest to source, build and approval | Production deployment is reproducible and attributable |
| CLOUD-T-033 | Configuration drift | Compare deployed state with approved IaC/policy | Drift is detected and resolved or accepted |
| CLOUD-T-034 | Incident readiness | Tabletop credential, image and public storage incidents | Containment and evidence process is executable |

## 22. Standards and framework mapping

Mappings below identify relevant source families and control themes. They are not assertions of compliance. Exact control IDs must be pinned to the edition selected for the engagement and mapped to evidence.

### 22.1 NIST SP 800-190

NIST SP 800-190, Application Container Security Guide (2017), remains a foundational container risk reference. It covers image, registry, orchestrator, container and host concerns. It is not a current Kubernetes configuration benchmark and should be complemented by current Kubernetes guidance and provider-specific documentation.

### 22.2 CIS Benchmarks

Use the exact benchmark for the deployed platform and version. The CIS Kubernetes benchmark and managed-service benchmarks are separate profiles; do not assume a generic Kubernetes benchmark fully covers EKS, AKS, GKE, Autopilot or other managed offerings.

At research cut-off 2026-11-18, CIS lists Kubernetes Benchmark 2.1.0 and managed-service profiles including EKS 2.1.0, AKS 2.1.0 and GKE 2.0.0. Verify the live benchmark catalog before assessment and record the exact PDF/version.

### 22.3 Provider frameworks

| Framework | Relevant areas | Status handling |
|---|---|---|
| AWS Well-Architected Framework Security Pillar | Governance/operations, IAM, data protection, infrastructure and application protection | Use current official documentation; architecture review is not an audit or compliance certificate |
| Microsoft Cloud Security Benchmark | Network, identity, privileged access, data, assets, logging, incident response, DevOps | MCSB v2 is marked preview in current documentation; do not silently treat preview as final baseline |
| Google Cloud Well-Architected Security, Privacy and Compliance pillar | Cloud workload security, privacy, compliance and operations | Use current official guidance and enterprise foundation blueprint |

### 22.4 NIST CSF and SP 800-53

- NIST CSF 2.0 organizes cybersecurity outcomes and governance; use it for program-level cloud risk outcomes.
- NIST SP 800-53 Rev. 5 control families can support detailed cloud control selection, tailored to system boundary and control inheritance.
- NIST SP 800-190 is a container-focused publication, not a full cloud security framework.
- NIST SP 800-218 SSDF supports secure build, release and vulnerability handling.

### 22.5 ISO/IEC 27001:2022 relevance

| Annex A control | Cloud-native relevance |
|---|---|
| 5.8 | Security in project management |
| 5.9 | Inventory of information and associated assets |
| 5.15–5.18 | Access control, identity and authentication information |
| 5.19–5.23 | Supplier, cloud service and ICT supply-chain security |
| 5.24–5.28 | Incident management and evidence |
| 5.29–5.30 | Security during disruption and ICT readiness |
| 5.31 | Legal, statutory, regulatory and contractual requirements |
| 5.34 | Privacy and protection of PII |
| 8.8 | Technical vulnerability management |
| 8.9 | Configuration management |
| 8.13 | Information backup |
| 8.15–8.16 | Logging and monitoring |
| 8.20–8.23 | Network security, network services and web filtering |
| 8.24 | Cryptography |
| 8.25–8.29 | Secure development, architecture, coding and testing |
| 8.31–8.32 | Environment separation and change management |
| 8.33 | Test information |

This relevance mapping is not an ISO implementation statement or certification result.

### 22.6 CSA Cloud Controls Matrix

The Cloud Security Alliance Cloud Controls Matrix can support cloud control assessment and shared-responsibility analysis. Record the exact CCM release and applicable mappings at assessment time. Do not infer provider compliance from a framework mapping alone.

## 23. Global regulatory and sector considerations

Cloud location alone does not determine legal applicability. Determine the legal entity, service role, data subjects, data categories, processing purpose, sector, region, transfers, contracts and regulator scope.

### 23.1 India

Assess the Digital Personal Data Protection Act, 2023 and DPDP Rules, 2025 where applicable, including phased commencement. Cloud engineering implications may include processor governance, reasonable security safeguards, breach handling, purpose and retention controls, data principal rights and deletion propagation. Review sector-specific requirements for RBI-regulated entities, payment systems, insurance, securities, telecom, health and government services as applicable. CERT-In directions may impose incident reporting and log retention obligations on entities within scope. Verify exact current provisions, amendments and applicability with qualified counsel.

### 23.2 European Union and EEA

Assess GDPR, NIS2 where entity and sector scope apply, DORA for covered financial entities, eIDAS where relevant, and the Cyber Resilience Act for products with digital elements where applicable. Cloud engineering implications include processor/controller roles, transfer mechanisms, security of processing, resilience, incident reporting, supply-chain oversight, vulnerability handling and product security obligations. These instruments have different scopes and effective dates; do not combine them into a generic "EU cloud law."

### 23.3 United Kingdom

Assess UK GDPR, Data Protection Act 2018, NIS Regulations and sector-specific financial/telecom requirements where applicable. Cloud contracts, processor arrangements, transfer mechanisms, incident handling, resilience and supplier oversight require entity-specific analysis.

### 23.4 Qatar

Assess Qatar Personal Data Privacy Protection Law No. 13 of 2016, National Information Assurance Standard (NIA) where applicable to the entity/system, and relevant sector-specific requirements. Confirm regulator, government or critical-sector cloud requirements, data transfer conditions and current guidance. Do not assume NIA applies to every private cloud workload.

### 23.5 Saudi Arabia

Assess the Saudi Personal Data Protection Law and Implementing Regulations, applicable transfer rules, National Cybersecurity Authority Essential Cybersecurity Controls (ECC) and Cloud Cybersecurity Controls (CCC) where entity/service scope applies. Confirm current edition, regulator scope, cloud provider qualification and sector overlays before designing control deadlines or residency claims.

### 23.6 United Arab Emirates

Determine whether federal UAE Personal Data Protection Law, DIFC, ADGM, healthcare, financial, government or other sector-specific regimes apply. Assess cloud provider and processor roles, transfer requirements, data residency commitments, incident response and regulator-specific security controls.

### 23.7 United States

Depending on sector and data, assess state privacy laws, HIPAA and HITECH for covered healthcare entities/business associates, GLBA and applicable financial regulator rules, PCI DSS for cardholder data environments, FedRAMP/FISMA for relevant federal systems and CCPA/CPRA where scope applies. These are not universal cloud requirements for every US company.

### 23.8 Cross-border cloud engineering questions

For every deployment record:
- Data controller/processor and cloud provider roles.
- Primary, replica, backup and support-access locations.
- Subprocessor chain and onward transfer.
- Encryption and key ownership/control.
- Government access request process and contract commitments.
- Data deletion, backup expiry and legal hold behavior.
- Incident notification and evidence access.
- Resilience and exit/portability plan.
- Applicable sector regulator and supervisory requirements.

## 24. Industry use cases

### 24.1 SaaS multi-tenant platform

Threats: cross-tenant object access, shared database query flaws, overly broad workload identity, public storage, noisy-neighbor abuse and backup leakage.

Controls:
- Server-side tenant context derived from authenticated identity, not client-supplied tenant IDs.
- Tenant-aware authorization in every API and data access path.
- Database row/schema/database isolation selected by risk.
- Tenant-scoped storage and encryption design.
- Separate administrative access and audited support tooling.
- Per-tenant rate limits and quotas.
- Cross-tenant regression tests.
- Data export, retention and deletion workflows.

### 24.2 Banking and payment workloads

Threats: cloud credential theft, transaction manipulation, key misuse, data exfiltration, CI compromise and resilience failure.

Controls:
- Strong privileged identity and approval.
- Workload-specific identities and narrow key permissions.
- Segmented production and security accounts.
- Immutable audit and transaction evidence.
- Controlled release and signed artifacts.
- Data encryption and key lifecycle.
- Resilient backups and tested recovery.
- Payment API authorization and idempotency.

### 24.3 Healthcare and health SaaS

Threats: sensitive data leakage through storage, analytics, support access, backups and logs; ransomware; weak tenant boundaries.

Controls:
- Data classification and minimization.
- Private access and least-privilege workload identities.
- Encryption and controlled key access.
- Audit access to sensitive records.
- Processor and subprocessor governance.
- Tested recovery and incident procedures.
- Retention and deletion aligned with applicable law and contracts.

### 24.4 Industrial and OT companion services

Threats: compromise of cloud analytics/API layer leading to unsafe remote connectivity or unauthorized command path toward industrial networks.

Controls:
- Separate cloud analytics from control-plane actuation.
- No direct public cloud-to-PLC/SCADA reachability by default.
- Use monitored, authenticated industrial DMZ/gateway patterns.
- Enforce command authorization, safety interlocks and operator approval in appropriate control layers.
- Segment IT, cloud and OT trust zones.
- Record commands and identity with protected audit.
- Test failure and disconnection behavior with OT operations and safety owners.

### 24.5 Public sector and government SaaS

Threats: data residency violations, privileged support access, supply-chain compromise, weak audit and shared tenant exposure.

Controls:
- Map exact government cloud classification and approved service requirements.
- Isolate tenant and administrative paths.
- Review provider certifications and contract scope.
- Enforce key, logging and data location policy.
- Maintain exit, portability and incident cooperation provisions.

## 25. Metrics and control effectiveness

| Metric | Definition | Use |
|---|---|---|
| Cloud asset ownership coverage | In-scope assets with verified owner / total discovered assets | Accountability |
| Privileged identity review coverage | Privileged identities reviewed within policy interval / total privileged identities | IAM governance |
| Static credential prevalence | Workloads/pipelines using long-lived static credentials / total assessed | Credential risk |
| Public exposure exception rate | Public resources with valid approved exception / total public resources | Exposure governance |
| Workload policy compliance | Workloads meeting approved runtime baseline / total assessed | Runtime hardening |
| Image provenance coverage | Production images with verifiable provenance / total production images | Supply-chain assurance |
| Critical image remediation time | Time from validated critical finding to fixed deployed digest | Vulnerability response |
| IaC policy violation rate | Failed or excepted changes / evaluated changes | Preventive control quality |
| Audit telemetry coverage | Critical services sending protected audit events / total critical services | Detection readiness |
| Restore test success | Successful recovery tests / planned recovery tests | Resilience |
| Cross-tenant test coverage | Critical tenant paths with negative authorization tests / identified paths | SaaS isolation |
| Exception expiry compliance | Exceptions reviewed/closed by expiry / exceptions due | Governance |

Metrics require defined numerator, denominator, scope, source, owner, frequency and target. Do not report a high percentage without showing excluded assets and stale inventory risk.

## 26. Maturity model

| Level | Characteristics |
|---|---|
| 1 — Ad hoc | Cloud resources and workloads are deployed without consistent ownership, identity or configuration baselines |
| 2 — Repeatable | Inventory, IAM baseline, image scanning, logging and basic network controls exist |
| 3 — Defined | Landing zones, workload identity, IaC policy, admission controls and release gates are standardized |
| 4 — Measured | Continuous posture, runtime detection, provenance verification, access analytics and recovery tests are measured |
| 5 — Adaptive | Risk-based policy, automated containment, continuous assurance and architecture feedback are integrated with governed human override |

Tool deployment alone does not establish maturity. Require operating evidence and control effectiveness.

## 27. Implementation roadmap

### 0–30 days: discover and reduce exposure
- Inventory accounts/projects/subscriptions, clusters, registries, functions and managed services.
- Identify public endpoints, public storage and privileged identities.
- Review static credentials and CI/CD secrets.
- Enable and protect control-plane audit logs.
- Identify critical workloads and data stores.
- Establish ownership and exception register.

### 30–90 days: establish secure foundations
- Implement account/landing-zone guardrails.
- Federate human and workload identity.
- Remove unnecessary long-lived keys.
- Restrict public network and storage exposure.
- Harden container images and Kubernetes baseline.
- Protect secrets, keys and IaC state.
- Add CI/CD identity and artifact provenance controls.
- Implement baseline detection use cases.

### 90–180 days: operationalize assurance
- Enforce admission and policy-as-code.
- Implement workload egress restrictions.
- Verify runtime telemetry and incident playbooks.
- Test backup restoration and recovery.
- Perform cross-tenant and cloud attack-path testing.
- Map controls to exact standards/regulatory requirements.
- Measure control effectiveness and remediate exceptions.

## 28. Evidence and professional deliverables

A cloud-native security assessment pack should include:
- Scope, authorization and rules of engagement.
- Cloud account/project/subscription and resource inventory.
- Shared-responsibility matrix by service.
- Architecture and data-flow diagrams.
- Identity and trust relationship register.
- Network exposure and segmentation map.
- Data classification and key/secret inventory.
- Container and registry inventory, SBOM and provenance.
- Kubernetes configuration and RBAC assessment.
- Serverless trigger and identity map.
- IaC and pipeline review evidence.
- Logging and detection coverage matrix.
- Backup and recovery test records.
- Standards and jurisdiction mapping with exact versions.
- Findings, risk, remediation, exception and retest records.

## 29. Limitations and assumptions

- Cloud services, APIs, feature names, defaults and regional availability change frequently.
- Managed-service responsibility varies by offering, tier, deployment mode and contract.
- Scanner output may be incomplete or inaccurate and requires manual validation.
- Provider posture scores do not prove application security.
- Kubernetes namespaces alone are not a strong hostile-tenant boundary.
- Container isolation depends on runtime, kernel and host configuration.
- Policy-as-code can create outages if not tested and staged.
- Regulatory applicability requires entity-, sector- and processing-specific legal analysis.
- This chapter is an engineering baseline, not a cloud provider certification, legal opinion or compliance attestation.

## 30. Related chapters

- [02. Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [03. Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [04. Secure Coding and Code Review](../04-secure-coding/SECURE-CODING-AND-CODE-REVIEW.md)
- [06. API and Service Security](../06-api-service-security/API-AND-SERVICE-SECURITY-ENGINEERING.md)
- [07. Identity and Access Security](../07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY.md)
- [08. Data Security and Privacy Engineering](../08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-ENGINEERING.md)
- [09. Mobile Application Security](../09-mobile-application-security/MOBILE-APPLICATION-SECURITY-ENGINEERING.md)
- [10. Cloud-Native Application Security Lab Pack](CLOUD-NATIVE-APPLICATION-SECURITY-LAB-PACK.md)
- [13. Software Supply Chain Security](../13-software-supply-chain/SOFTWARE-SUPPLY-CHAIN-SECURITY.md)
- [14. Security Verification and Assessment](../14-security-verification-assessment/SECURITY-VERIFICATION-AND-ASSESSMENT.md)
- [17. DevSecOps and Security Tooling](../17-devsecops-tooling/DEVSECOPS-AND-SECURITY-TOOLING.md)
- [18. Standards Baseline and Mapping Method](../18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md)
- [19. Global Regulatory Register](../19-global-regulatory/GLOBAL-REGULATORY-REGISTER.md)

## 31. Authoritative references

1. AWS Well-Architected Framework, Security Pillar: https://docs.aws.amazon.com/wellarchitected/latest/framework/security.html
2. AWS Well-Architected Framework release notes: https://docs.aws.amazon.com/wellarchitected/latest/framework/
3. Microsoft Cloud Security Benchmark: https://learn.microsoft.com/en-us/security/benchmark/azure/
4. Google Cloud Well-Architected Framework, Security, Privacy and Compliance: https://docs.cloud.google.com/architecture/framework/security
5. Google Cloud Enterprise Foundations Blueprint: https://docs.cloud.google.com/architecture/blueprints/security-foundations
6. Kubernetes Security Concepts: https://kubernetes.io/docs/concepts/security/
7. Kubernetes Application Security Checklist: https://kubernetes.io/docs/concepts/security/application-security-checklist/
8. Kubernetes Security Checklist: https://kubernetes.io/docs/concepts/security/security-checklist/
9. CIS Kubernetes Benchmarks: https://www.cisecurity.org/benchmark/kubernetes
10. NIST SP 800-190, Application Container Security Guide: https://csrc.nist.gov/pubs/sp/800/190/final
11. NIST SP 800-218, Secure Software Development Framework: https://csrc.nist.gov/pubs/sp/800/218/final
12. NIST Cybersecurity Framework 2.0: https://www.nist.gov/cyberframework
13. Cloud Security Alliance Cloud Controls Matrix: https://cloudsecurityalliance.org/research/cloud-controls-matrix



## 32. Concrete implementation reference patterns

The following snippets are reference patterns for controlled engineering review. They are not drop-in production configurations. Pin provider/API versions, validate against the deployed Kubernetes version and CNI, review workload compatibility and run policy tests before enforcement.

### 32.1 Multi-stage container build

~~~dockerfile
# Replace the illustrative image reference with an approved immutable digest.
FROM node:22-alpine@sha256:REPLACE_WITH_APPROVED_DIGEST AS build
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine@sha256:REPLACE_WITH_APPROVED_DIGEST AS runtime
ENV NODE_ENV=production
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
COPY --from=build --chown=app:app /src/dist ./dist
COPY --from=build --chown=app:app /src/package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
USER app
EXPOSE 8080
CMD ["node", "dist/server.js"]
~~~

Review notes:
- Replace the placeholder digest with a verified digest from an approved registry.
- Ensure build dependencies are not copied into the runtime image.
- Confirm the runtime actually needs npm at startup; a production build may copy only required runtime files.
- Add a health check appropriate to the application and orchestrator.
- Scan the final image, generate an SBOM and record provenance.
- Do not pass secrets through build arguments or bake them into layers.

### 32.2 Kubernetes restricted pod baseline

~~~yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-example
  namespace: app-namespace
  labels:
    app.kubernetes.io/name: app-example
spec:
  serviceAccountName: app-example
  automountServiceAccountToken: false
  securityContext:
    runAsNonRoot: true
    runAsUser: 10001
    runAsGroup: 10001
    fsGroup: 10001
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: registry.example.invalid/team/app@sha256:REPLACE_WITH_APPROVED_DIGEST
      ports:
        - name: http
          containerPort: 8080
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 512Mi
      volumeMounts:
        - name: tmp
          mountPath: /tmp
      readinessProbe:
        httpGet:
          path: /health/ready
          port: http
      livenessProbe:
        httpGet:
          path: /health/live
          port: http
  volumes:
    - name: tmp
      emptyDir:
        sizeLimit: 64Mi
~~~

Review notes:
- Replace the example namespace, registry and digest.
- Verify the chosen UID/GID is supported by the image and mounted volumes.
- Do not add a service account token unless the workload requires Kubernetes API access.
- Probes must not expose sensitive diagnostics or become an unauthenticated expensive endpoint.
- Requests and limits require workload-specific performance testing.
- This pod specification does not establish cluster-wide admission, network or identity security.

### 32.3 Kubernetes namespace default-deny network policy

~~~yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: app-namespace
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
~~~

Add explicit allow policies for required ingress, DNS and service-to-service traffic. Do not copy a broad allow-all egress rule into a supposedly restricted namespace. Verify that the installed CNI enforces NetworkPolicy and test actual traffic paths.

### 32.4 Kubernetes workload-specific RBAC

~~~yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app-example
  namespace: app-namespace
automountServiceAccountToken: false
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-example-config-reader
  namespace: app-namespace
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    resourceNames: ["app-example-config"]
    verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-example-config-reader
  namespace: app-namespace
subjects:
  - kind: ServiceAccount
    name: app-example
    namespace: app-namespace
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: app-example-config-reader
~~~

This is a narrow example for a workload that must read one named ConfigMap. It does not grant access to Secrets and does not require automatic token mounting. If the application does not call the Kubernetes API, omit the Role and RoleBinding entirely.

### 32.5 Terraform AWS storage baseline example

~~~hcl
resource "aws_s3_bucket" "app_data" {
  bucket = var.unique_bucket_name
}

resource "aws_s3_bucket_public_access_block" "app_data" {
  bucket                  = aws_s3_bucket.app_data.id
  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = var.approved_kms_key_arn
    }
    bucket_key_enabled = true
  }
}
~~~

Review notes:
- Pin the AWS provider version and test the configuration against the provider documentation for that version.
- Apply organization-level and resource-level controls; resource configuration alone is not a complete public-access guarantee.
- Define KMS key policy, rotation, recovery, cross-account use and deletion protection separately.
- Do not put credentials in Terraform variables, source, plan output or state. Terraform state is sensitive even when remote and encrypted.
- Add lifecycle, versioning, logging, backup and retention requirements according to the data classification and service design.

### 32.6 CI workflow permission minimization

~~~yaml
name: validate
on:
  pull_request:
  push:
    branches: ["main"]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
        with:
          persist-credentials: false
      - name: Run tests
        run: npm ci && npm test
~~~

This validation-only example intentionally has no cloud deployment permission and no identity-token permission. Production deployment must be a separate protected workflow/environment with narrowly scoped OIDC trust, pinned third-party actions, approval and a distinct deployment role. Pin actions to reviewed immutable commit SHAs in a production workflow; a major-version tag is shown here only to keep the example readable.

### 32.7 Workload identity design record

For each cloud workload identity, record:

| Field | Required value |
|---|---|
| Workload name | Unique service/function/pod identity |
| Identity issuer | Provider or external identity issuer |
| Subject binding | Exact account, repository, namespace, service account or runtime subject |
| Audience | Expected token audience |
| Permissions | Exact actions and resource scope |
| Credential lifetime | Shortest compatible duration |
| Deployment identity | Separate from runtime identity |
| Secret fallback | Explicit exception, owner and expiry if static secret is unavoidable |
| Audit source | Token issuance and resource access event source |
| Revocation | Tested disable/revoke procedure |
| Owner | Named team and escalation contact |

### 32.8 Policy rollout decision sequence

~~~mermaid
flowchart TD
    A[Write policy and threat rationale] --> B[Unit test policy with compliant and non-compliant fixtures]
    B --> C[Run in audit or warn mode]
    C --> D[Measure violations and false positives]
    D --> E{Exceptions understood and approved?}
    E -- No --> F[Fix workload or refine policy]
    F --> C
    E -- Yes --> G[Stage enforcement in non-production]
    G --> H[Validate rollback and emergency path]
    H --> I[Enforce in production with monitoring]
    I --> J[Review drift, exceptions and policy changes]
~~~

### 32.9 Production readiness questions

Before accepting a cloud-native workload, reviewers should be able to answer:
1. Which identity deploys the workload and which identity does it run as?
2. What exact resources can the runtime identity access?
3. Can a compromised application reach metadata, control-plane or unrelated internal services?
4. Which image digest is deployed and where is its provenance?
5. What prevents an untrusted image or privileged pod from entering the cluster?
6. Which network flows are necessary and actually enforced?
7. Where are secrets stored, how are they retrieved and how are they revoked?
8. Which logs remain available if the workload or account administrator is compromised?
9. How is tenant identity enforced in every API, data and event path?
10. Can the service be rebuilt and restored from trusted source, artifacts and backups?
11. Which legal, contractual and sector obligations apply to the data and service?
12. Which exceptions remain open, who owns them and when do they expire?


## 33. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-18 | Initial cloud-native application security engineering playbook |
