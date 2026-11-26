# Software Supply Chain Security Engineering

| Field | Value |
|---|---|
| Document ID | UAPPSEC-13-ENG-001 |
| Status | Draft engineering baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-19 |
| Review due | 2027-02-19 |
| Scope | Source, people, dependencies, build systems, CI/CD, artifacts, provenance, signing, SBOM, containers, releases, suppliers and AI assets |
| Classification | Public |

## 1. Purpose and security objectives

Software supply chain security protects the integrity, provenance, confidentiality and availability of software and the systems used to produce, distribute, install and operate it. The protected chain includes people, identities, source repositories, development workstations, dependencies, package registries, build runners, plugins, signing identities, artifact repositories, container registries, deployment systems, vendors and update channels.

The objective is not merely to scan dependencies. An organization must be able to establish:
- What source, dependencies, tools and build instructions produced a release.
- Who or what authorized each change, build, signing event and release.
- Whether source and artifacts were modified outside approved paths.
- Whether dependencies are authentic, maintained, supported and legally usable.
- Whether a consumer can verify artifact identity, integrity and provenance.
- Which released products contain an affected component and whether that component is reachable or exploitable.
- Whether a vulnerability is present, exploitable, mitigated, not affected or under investigation.
- Whether a supplier or build-system incident can be contained without losing evidence.
- Whether the organization can reproduce, rebuild, revoke, roll back and communicate safely.

A scan result, SBOM, signature, provenance statement or compliance attestation is one evidence item; none alone proves a software release is secure.

## 2. Scope and supply-chain model

### 2.1 Lifecycle scope

1. Product planning, architecture and supplier selection.
2. Developer identity, endpoint and workstation.
3. Source control, branches, pull requests and code review.
4. Third-party and first-party dependencies.
5. Package registries, mirrors, caches and artifact repositories.
6. Build definitions, CI runners, plugins, actions and reusable workflows.
7. Build secrets, workload identity and privileged credentials.
8. Compilation, testing, packaging and release automation.
9. SBOM, attestations, provenance and vulnerability statements.
10. Artifact signing, verification and trust-root management.
11. Container images, base images, registries and deployment manifests.
12. Release approval, distribution, installation and update channels.
13. Production inventory, vulnerability response and remediation.
14. Supplier assurance, incident response and end-of-life.

### 2.2 Trust boundaries

Treat these as distinct trust zones:
- Developer endpoint to source-control platform.
- Pull-request author to protected branch.
- Repository content to CI workflow execution.
- CI workflow to runner host and runner-to-runner state.
- Build job to secret manager and cloud identity provider.
- Build process to package registry and dependency mirror.
- Build output to artifact repository.
- Artifact repository to signing service.
- Signing identity to verifier trust policy.
- Release pipeline to production deployment identity.
- Organization to supplier and upstream maintainer.
- Production workload to telemetry, update and support channels.

A successful authentication does not establish that code or workflow content is trustworthy. A trusted repository can contain malicious commits; a valid signature can identify an untrusted signer; a valid SBOM can be incomplete; a passing scanner can miss an attack.

### 2.3 Threat actors and failure sources

Consider external attackers, compromised maintainers, malicious insiders, compromised developer endpoints, malicious or hijacked dependencies, registry compromise, typosquatting, dependency confusion, build-system compromise, stolen CI credentials, poisoned artifacts, signing-key compromise, supplier incidents, accidental configuration errors, unsupported components and malicious update channels.

## 3. Core principles

1. Verify every transition: authenticate actors and verify integrity, provenance and policy at each material handoff.
2. Least privilege: separate source write, workflow administration, build, signing, release and deployment privileges.
3. Isolate builds: use ephemeral, hardened, disposable runners with controlled egress and no shared untrusted state.
4. Pin inputs: pin actions, plugins, base images, dependencies and toolchains to immutable versions or digests where feasible.
5. Make provenance verifiable: produce authenticated build provenance tied to source revision, builder identity, build definition and artifact digest.
6. Generate SBOMs from the actual release: include direct and transitive components and preserve relationships and identifiers.
7. Sign and verify: sign artifacts and attestations with managed identities; verify identity, issuer, digest, policy and trust roots before promotion or deployment.
8. Manage vulnerabilities contextually: combine component identity, affected version ranges, reachability, exploitability, exposure, mitigations and business criticality.
9. Separate duties: developers must not unilaterally approve, sign and deploy high-risk releases where separation is required.
10. Assume suppliers can fail: maintain inventory, contact paths, alternate sources, incident clauses and exit plans.
11. Preserve evidence: retain immutable or tamper-evident source, build, signing, release and deployment records.
12. Rehearse response: test compromised dependency, maintainer, runner, signing identity and update channel scenarios.

## 4. Governance, roles and decision rights

| Role | Primary accountability |
|---|---|
| Product owner | Product risk, release acceptance and business impact |
| Engineering lead | Source, dependency and build control implementation |
| AppSec / Product Security | Threat model, security requirements, testing and exception review |
| DevSecOps / Platform | CI runners, workflow controls, artifact stores, signing and deployment guardrails |
| Repository owner | Branch protection, access, application integration and audit settings |
| Dependency owner | Component inventory, maintenance, upgrade and vulnerability disposition |
| Release manager | Release authorization, evidence completeness and rollback readiness |
| Security operations | Detection, triage, incident coordination and threat intelligence |
| Procurement / Vendor risk | Supplier due diligence, contractual requirements and reassessment |
| Legal / Compliance | License, privacy, contractual and regulatory interpretation |
| Incident commander | Containment, evidence preservation, recovery and communications |

Define RACI for repository administration, dependency exceptions, runner administration, secret access, signing policy, production promotion, emergency revocation and supplier acceptance. Critical production release controls should not depend on one individual or one credential.

## 5. Asset inventory and criticality

Maintain an inventory covering:
- Products, services, repositories and release channels.
- Source repositories, branches, owners and criticality.
- Build workflows, runner groups, reusable workflows and third-party actions.
- Direct and transitive dependencies, package coordinates and package sources.
- Compiler, SDK, runtime, build tools, plugins and container base images.
- Artifact digests, signatures, attestations, SBOMs and release identifiers.
- Registries, mirrors, caches and artifact repositories.
- Signing identities, key custodians, certificates and trust roots.
- Deployment environments and workloads consuming each artifact.
- Suppliers, maintainers, support status, contracts and incident contacts.
- AI models, datasets, tokenizers, adapters and other model assets where applicable.

Use stable identifiers: repository URL plus commit, package URL (purl), CPE where applicable, OCI digest, cryptographic hash, certificate identity, workflow identity and supplier legal entity. Names alone are not reliable identifiers.

Criticality should consider business impact, internet exposure, privilege, data sensitivity, safety impact, operational dependency, customer reach, recovery time and substitutability. Define criticality tiers and minimum evidence for each tier.

## 6. Threat modeling and attack paths

Model attacker goals and paths, not just individual tools. Example paths include:
- Malicious pull request changes workflow behavior and exfiltrates a build secret.
- Compromised action or plugin executes in a privileged runner.
- Typosquatted package is introduced through a developer typo.
- Public dependency name is resolved from an attacker-controlled registry because source priority is misconfigured.
- Compromised maintainer publishes a malicious package release.
- Poisoned cache supplies an artifact different from the reviewed source.
- Build runner is compromised and emits a backdoored binary with otherwise clean source.
- Signing credential is stolen and used to sign an unauthorized artifact.
- Artifact is replaced after signing or the verifier checks the wrong digest.
- Release pipeline deploys an unsigned or unapproved image by mutable tag.
- Vulnerability is announced but organization cannot identify affected products due to incomplete SBOMs.
- Supplier update channel distributes a compromised update.
- CI workflow uses unpinned remote code or an over-privileged token.
- AI model, dataset or adapter is imported without provenance, license review or integrity verification.

For each path document threat actor, preconditions, trust boundary, asset, attack technique, preventive control, detection, response, evidence and residual risk.

## 7. Source control and repository security

### 7.1 Identity and access

- Enforce SSO and phishing-resistant MFA where supported for privileged accounts.
- Use unique named accounts; prohibit shared administrator identities.
- Apply least-privilege repository, organization and team permissions.
- Review external collaborators, deploy keys, personal access tokens, OAuth apps and GitHub Apps.
- Prefer short-lived, fine-grained tokens and workload identity over long-lived personal tokens.
- Restrict token permissions, resource scope and lifetime.
- Protect organization owners and repository administrators with stronger controls and break-glass procedures.
- Review access at onboarding, role change, offboarding and scheduled intervals.
- Alert on unusual permission grants, token creation, deploy-key changes and branch-protection changes.

### 7.2 Branch and review protections

- Protect default and release branches.
- Require pull requests and independent approvals for sensitive changes.
- Require status checks from trusted workflows.
- Require code-owner review for workflow, dependency, security policy and release configuration changes.
- Dismiss stale approvals when new commits change the reviewed diff.
- Restrict force pushes and deletion of protected branches.
- Apply signed-commit policy where it adds meaningful assurance; do not treat signed commits as proof that code is safe.
- Prevent bypass except for documented, monitored break-glass use.
- Use merge queues or equivalent serialization for high-change repositories where useful.
- Require explicit review for changes to workflow files, reusable workflows, dependency manifests, lockfiles, build scripts, container definitions and release scripts.

### 7.3 Repository configuration and audit

- Enable secret scanning, push protection and dependency alerts where available.
- Enable dependency graph and automated update mechanisms with review and test controls.
- Enable code scanning and policy checks appropriate to the language.
- Restrict repository creation, visibility changes and transfer.
- Review webhooks, GitHub Apps, Actions permissions and organization-level policy.
- Keep audit logs and alert on security-sensitive changes.
- Protect repository backups and export integrity.
- Document repository deletion, archival and ownership-transfer controls.

## 8. Developer workstation and local development

- Use managed, patched developer endpoints with disk encryption and endpoint detection.
- Separate daily-use identity from privileged administration.
- Protect browser sessions, SSH keys, signing credentials and local credential stores.
- Use approved IDE extensions and plugin sources; inventory extensions for high-risk development groups.
- Avoid running untrusted build scripts with administrator privileges.
- Use isolated development containers or VMs for untrusted repositories.
- Restrict local package installation sources and configure private registry authentication securely.
- Prevent secrets from entering source, shell history, logs, crash dumps and local test fixtures.
- Use pre-commit checks as an early warning, not as the only enforcement point.
- Provide a safe process to report suspicious packages, maintainer compromise and unexpected build behavior.

## 9. Dependency and package management

### 9.1 Dependency inventory

For every dependency capture:
- Name, ecosystem, namespace and package URL.
- Exact resolved version and integrity hash.
- Direct or transitive relationship and dependency path.
- Source registry, repository URL and publisher/maintainer identity.
- License expression and copyright/notice obligations.
- Known vulnerability identifiers and affected version range.
- Maintenance state, end-of-life and release activity.
- Whether the component is vendored, generated, optional, test-only or runtime.
- Whether the component is actually packaged and deployed.

Retain lockfiles and ensure CI uses deterministic installation commands. The manifest expresses intent; the lockfile captures the resolved graph. Review unexpected lockfile changes.

### 9.2 Registry and namespace controls

- Define approved registries and explicit source priority.
- Scope private package namespaces and credentials to the intended registry.
- Prevent public registry fallback for internal package names.
- Use namespace reservation and package-name verification.
- Verify package integrity hashes and signatures where available.
- Use curated proxies or mirrors with malware scanning, retention and quarantine.
- Restrict who can publish, overwrite, unpublish or administer packages.
- Protect package tokens and automation identities.
- Avoid installing dependencies from arbitrary URLs or mutable branches in production builds.
- Record provenance and origin for vendored dependencies.

### 9.3 Dependency selection and lifecycle

Evaluate maintenance, release integrity, security response, ownership concentration, transitive depth, install scripts, native extensions, runtime privileges, license, compatibility and alternatives. Prefer maintained components with a clear security policy. Establish review and replacement plans for abandoned or high-risk packages.

### 9.4 Dependency update policy

- Automate discovery and propose updates in controlled pull requests.
- Test updates with unit, integration, security and compatibility tests.
- Prioritize actively exploited vulnerabilities and reachable critical components.
- Apply risk-based service-level objectives for remediation.
- Do not auto-merge updates solely because a scanner reports low severity.
- Review major version changes and package ownership changes.
- Retain rollback versions and validate rollback integrity.

## 10. Dependency confusion, typosquatting and package takeover

Controls include:
- Explicit package source mapping and namespace ownership.
- Internal namespace reservation in public registries where supported.
- Lockfile and integrity enforcement.
- Review of newly introduced package names and publishers.
- Similarity and typo detection for high-value dependencies.
- Monitoring maintainer, ownership, repository and release-key changes.
- Registry quarantine for suspicious packages.
- Egress restrictions preventing arbitrary package downloads from build jobs.
- Reproducible dependency resolution and package provenance checks.

Investigate unexpected package name, version, source registry, install script, maintainer, release cadence or dependency tree changes. Preserve the exact package archive and metadata for analysis.

## 11. Software composition analysis and vulnerability intelligence

SCA should identify components and versions, map advisories, assess reachability where supported, and support remediation. It is not a substitute for code review, malware analysis, exploit validation or architecture review.

Correlate:
- CVE and ecosystem advisory identifiers.
- Package URL and exact version.
- Affected and fixed version ranges.
- CVSS and other severity information.
- Exploit prediction or known exploitation signals, where credible.
- Runtime reachability, attack surface and feature usage.
- Exposure, privileges and data sensitivity.
- Vendor advisory and compensating controls.
- Fix availability, upgrade risk and operational constraints.

Do not assume a CVE affects every version or every deployment. Do not mark a vulnerability not affected merely because a scanner did not find a call path. Record evidence and reviewer for every VEX-like disposition.

## 12. SBOM engineering

### 12.1 Generation

Generate an SBOM for each releasable software version from the resolved build inputs and actual packaged contents where possible. Include direct and transitive dependencies, component identifiers, versions, supplier/origin information where known, hashes, licenses and dependency relationships. Document omissions and blind spots such as statically linked code, vendored source, generated components, firmware, plugins or runtime downloads.

Generate the SBOM in a machine-readable format and validate it against the selected schema version. Retain it with the immutable artifact digest and release record.

### 12.2 Format selection

| Format | Strengths and use |
|---|---|
| SPDX | Broad license, provenance and software component information; useful for legal and supply-chain exchange |
| CycloneDX | Security-oriented BOM, dependency relationships, vulnerability and VEX-related capabilities, plus software, SaaS, hardware, cryptographic and ML BOM use cases |
| SWID | Software identification and inventory use cases where supported |

Select one primary exchange format per product or define a conversion/dual-format strategy. Do not assume two SBOM formats contain equivalent semantics. Pin schema version and validate producer/consumer interoperability.

As of this review, CycloneDX 1.7 is the specification/schema version captured for this chapter; 1.7.x release numbers refer to specification repository releases and should be checked independently. SPDX 3.0.1 is the inspected SPDX specification. Confirm exact schema and tool support at implementation time.

### 12.3 SBOM quality

Check:
- Unique and stable document serial/version.
- SBOM tool name/version and generation context, consistent with the CISA 2026 minimum-elements guidance.
- Creation timestamp and author/tool metadata.
- Product and release identity.
- Component name, supplier, version and purl/CPE where available.
- Component hashes and licenses where available.
- Direct/transitive relationships and dependency graph completeness.
- External references and source identifiers.
- Completeness for compiled, vendored and generated content.
- Consistency with package manifests, lockfiles, image layers and artifact contents.
- Schema validity and absence of fabricated component data.

An SBOM is a point-in-time inventory, not a security certificate. Keep it updated when the product is rebuilt or released.

## 13. VEX and vulnerability disposition

VEX communicates whether a product is affected by a vulnerability and the basis for that assessment. Define controlled states supported by the chosen format and consumer tooling, typically including affected, not affected, fixed and under investigation. The implementation profile in this repository uses OpenVEX v0.2.0; its status labels are `affected`, `not_affected`, `fixed` and `under_investigation`. CycloneDX uses its own vulnerability analysis state vocabulary; do not silently map values between formats without an explicit mapping.

A defensible not-affected decision should include:
- Product and component identity.
- Vulnerability identifier and affected version range.
- Technical justification, such as vulnerable code not present, code not reachable, feature not enabled or vulnerable configuration not used.
- Evidence source and test/build context.
- Decision owner, date, expiry/review trigger and approval.
- Residual risk and compensating controls.

Do not use VEX to suppress findings for convenience. Reassess when product features, dependencies, build flags, configuration or exploit knowledge changes. For OpenVEX, a `not_affected` statement must carry a recognized justification or an impact statement, while an `affected` statement must include an action statement. Keep incomplete assessments `under_investigation`. Never infer `not_affected` from an empty scanner result, missing call-graph data or an unverified mitigation.

The repository implementation profile and test evidence are maintained in [Chapter 13 VEX implementation](../../implementations/13-software-supply-chain-security/vex/README.md). The validator is a core-field/policy validator, not a full OpenVEX JSON-LD or official JSON Schema implementation. No production VEX statement has been issued from this repository.

## 14. Build system and CI/CD security

### 14.1 Workflow definition

- Treat workflow files as privileged code.
- Require independent review for workflow, runner, secret, permission and release changes.
- Pin third-party actions and reusable workflows to immutable commit references where supported.
- Minimize workflow token permissions; grant write access only to the job that needs it.
- Avoid executing untrusted pull-request code in privileged contexts.
- Do not interpolate untrusted input directly into shell commands.
- Use explicit input validation and safe argument handling.
- Restrict workflow triggers and protect deployment environments.
- Separate build, test, signing and deployment jobs where trust levels differ.
- Record workflow source revision and configuration.

### 14.2 Runner hardening

- Prefer ephemeral, single-job runners for sensitive builds.
- Separate runner pools by repository trust, environment and privilege.
- Do not share writable workspace, caches or credentials across mutually untrusted jobs.
- Patch runner OS, agents and installed tools.
- Restrict network egress to required registries, source and service endpoints.
- Prevent runner access to cloud metadata or unrelated internal services.
- Avoid privileged container mode and host socket mounts unless strictly required and isolated.
- Destroy runner state after job completion.
- Monitor runner registration, image changes, startup scripts and administrative access.
- Use hardened golden images and verify their provenance.

### 14.3 Secrets and workload identity

- Prefer OIDC federation and short-lived workload credentials.
- Scope identity to repository, branch, environment, workflow and job where supported.
- Use dedicated secret manager paths and narrow permissions.
- Do not expose signing or production deployment credentials to ordinary build/test jobs.
- Masking is not a security boundary; prevent secret access by untrusted code.
- Rotate credentials after suspected exposure and maintain revocation procedures.
- Prevent secrets from being copied into artifacts, caches, logs and build metadata.
- Review identity trust conditions and token audience.

### 14.4 Build isolation and reproducibility

Use controlled toolchains, declared inputs, deterministic dependency resolution and isolated build environments. Reproducibility is valuable evidence but can be limited by timestamps, nondeterministic compilers, network downloads, signing steps and environment differences. Document the level actually achieved and compare independent builds where feasible.

## 15. Build provenance and attestations

Build provenance should bind an artifact digest to verifiable information about the source, builder, build definition and resolved inputs. Use an established attestation model such as in-toto statements with SLSA provenance predicates. For SLSA v1.2 Build, use the predicate type `https://slsa.dev/provenance/v1`; the predicate type URI remains stable across minor specification revisions. The repository's synthetic implementation is documented in [the Chapter 13 provenance implementation](../../implementations/13-software-supply-chain-security/provenance/README.md).

Capture at minimum:
- Subject artifact name and cryptographic digest.
- Source repository and immutable revision.
- Build definition and workflow identity/revision.
- Builder identity and trusted build platform.
- Build invocation and parameters.
- Resolved dependencies and relevant materials.
- Build start/end time and invocation ID.
- Provenance predicate type and schema version.
- Signature/attestation bundle and transparency evidence where used.

Consumers must verify the attestation cryptographically and enforce policy over expected source, builder identity, workflow, repository, ref and artifact digest. A provenance document that is not authenticated or whose signer is not trusted is only an assertion.

### 15.1 SLSA v1.2 tracks and levels

SLSA v1.2 is the approved specification baseline captured for this review. It separates source integrity from build integrity. Do not confuse the current multi-track model with the earlier single SLSA 1–4 level numbering.

| Track | Level | High-level requirement | Main assurance focus |
|---|---|---|---|
| Source | L1 | Version-controlled source revisions | Immutable, identifiable source revisions |
| Source | L2 | Continuous history and source provenance | Reliable history, contributor and process evidence |
| Source | L3 | Continuous technical controls | Enforced repository controls with verifiable evidence |
| Source | L4 | Two-party review | Two trusted persons review changes to protected branches |
| Build | L0 | No guarantees | No SLSA build assurance |
| Build | L1 | Provenance exists | Provenance describes how artifact was built |
| Build | L2 | Hosted build platform and signed provenance | Provenance authenticity and protection against post-build tampering |
| Build | L3 | Hardened build platform | Strong isolation and protection against tampering during build |

Use the Source track for source-control system guarantees and the Build track for artifact production. A product may have different levels on each track. Record the exact track, level, source branch/revision, builder, artifact and evidence; never publish one ambiguous statement such as "SLSA Level 3" without naming the track and specification version.

For Build L3, verify the build platform prevents runs from influencing one another and prevents provenance-signing secrets from being accessible to user-defined build steps. For Source L4, verify two trusted reviewers are required for every change to the protected branch; a nominal pull-request rule that administrators can silently bypass is not equivalent.

SLSA levels are not a general product security rating and do not guarantee that source code is vulnerability-free. They provide scoped supply-chain assurances. Confirm the complete normative requirements and evidence with the official v1.2 specification before making a conformance claim.



## 16. Artifact signing and verification

### 16.1 Signing

- Sign release artifacts and container images after build and before promotion.
- Prefer short-lived workload identity or managed signing services over long-lived exportable private keys.
- Separate signing authority from source write and ordinary build execution.
- Protect signing workflows, identity issuer, trust roots and transparency log dependencies.
- Bind signatures to immutable artifact digests.
- Sign SBOMs and attestations where supported and policy requires.
- Maintain key/identity rotation, revocation and compromise procedures.

### 16.2 Verification

Before promotion, installation or deployment:
1. Resolve artifact by immutable digest, not mutable tag alone.
2. Verify signature cryptographically.
3. Verify signer identity and issuer against an explicit trust policy.
4. Verify the signed subject digest matches the exact artifact.
5. Verify attestation predicate and provenance.
6. Check source repository, commit/ref, builder and workflow identity.
7. Validate SBOM presence and schema where required.
8. Evaluate vulnerabilities, policy exceptions and release approval.
9. Record verification result and policy version.
10. Fail closed for protected production releases when required evidence is absent or invalid.

A valid signature proves control of a signing identity for a particular digest; it does not prove the artifact is benign or the source is trustworthy. The repository's synthetic implementation uses Cosign v3.1.6 keyless blob signing and is documented in [the Chapter 13 Cosign signing implementation](../../implementations/13-software-supply-chain-security/signing/README.md). Its signing job is separated from the build job, and verification constrains the certificate identity, issuer, repository, ref and source revision. This is a prototype, not production signing governance or a release gate.

## 17. Container and image supply-chain security

- Use trusted, maintained base images and pin by digest.
- Minimize image layers, packages, shells and runtime utilities.
- Build from controlled container definitions and reviewed build contexts.
- Use multi-stage builds to exclude compilers, credentials and development files from runtime images.
- Run as non-root and drop unnecessary Linux capabilities.
- Use read-only root filesystems and seccomp/AppArmor profiles where practical.
- Scan OS packages, language packages and image configuration.
- Generate image SBOMs and bind them to image digests.
- Sign images and verify signatures at admission/deployment.
- Restrict registry write access and protect tags from overwrite.
- Enforce image provenance and approved registries in Kubernetes admission.
- Rebuild promptly when base images reach end-of-life or critical fixes are published.
- Monitor deployed image digests rather than only tags.

## 18. Infrastructure as code and deployment artifacts

Treat Terraform, Bicep, CloudFormation, Helm, Kubernetes manifests, policy bundles, scripts and deployment templates as supply-chain artifacts.

- Require code review and policy validation.
- Pin providers, modules, charts and remote templates.
- Verify module and provider sources.
- Scan for secrets, public exposure, excessive permissions and unsafe defaults.
- Separate plan and apply identities.
- Require approval for production changes and preserve plan evidence.
- Sign or attest release bundles where supported.
- Prevent deployment of unverified or mutable artifacts.
- Monitor drift and reconcile deployed state to approved source.
- Protect state files, plan outputs and deployment credentials.

## 19. Release and distribution security

- Establish release criteria and authorized release managers.
- Promote the same immutable artifact across environments; do not rebuild separately for production without a documented reason.
- Use staged/canary deployment and health verification.
- Bind release notes, SBOM, VEX, provenance, signatures and approval to a release ID.
- Protect update manifests, metadata and package channels.
- Prevent downgrade attacks where product architecture supports anti-rollback controls.
- Verify update signatures and version policy on clients/devices.
- Provide safe rollback and emergency withdrawal.
- Preserve the exact released artifact for forensic analysis.
- Notify customers and downstream consumers when material vulnerability or compromise affects them.

## 20. Open-source governance and license compliance

- Maintain an approved open-source use policy and component intake process.
- Review license identifier, obligations, notices, source disclosure and distribution model.
- Review dual licensing, copyleft triggers, patents, trademarks and attribution with legal counsel where required.
- Record exceptions and commercial dependencies.
- Track abandoned projects, maintainer concentration and governance risks.
- Define criteria for forks, vendoring and replacement.
- Preserve license texts and notices in distributed products.
- Do not treat automated license scanners as legal advice.

## 21. Third-party and supplier assurance

Assess suppliers and critical open-source services based on:
- Software development and release security practices.
- Identity, access and MFA controls.
- Source and build-system protection.
- Dependency and vulnerability management.
- SBOM, provenance and signing capability.
- Security disclosure and incident response.
- Subprocessor and upstream dependency transparency.
- Data handling, residency and confidentiality obligations.
- Business continuity, support and end-of-life commitments.
- Right to audit, evidence availability and breach notification.
- Exit, data export, replacement and continuity arrangements.

Risk-tier suppliers based on privilege, data access, product criticality, update authority and substitutability. Contractual certifications are inputs, not substitutes for technical verification.

## 22. AI/ML and non-traditional software assets

Extend supply-chain inventory to model weights, adapters, tokenizers, datasets, evaluation corpora, embeddings, prompt templates, agent tools, MCP servers, plugins, model-serving runtimes and training code.

Record source, publisher, version, digest, license, provenance, training/evaluation lineage, intended use, known limitations and integrity verification. Isolate model loaders and parsers; avoid unsafe deserialization; review model download scripts and remote code execution options. Verify that AI assets are included in applicable BOM and release evidence. Coordinate with Chapter 12 for AI-specific risk analysis and data lineage.

## 23. Monitoring and detection

Monitor events such as:
- New or modified repository administrators, collaborators, tokens, deploy keys and applications.
- Branch protection or ruleset weakening and bypass events.
- Unexpected workflow changes, unpinned actions and new external dependencies.
- CI runner registration, image changes, persistence or unusual egress.
- Secrets access outside expected job, branch or environment.
- New package names, versions, publishers, registries or maintainers.
- Dependency lockfile drift and suspicious install scripts.
- Artifact digest mismatch, tag overwrite and registry permission changes.
- Signing identity changes, unusual signing requests and revocation events.
- Missing, invalid or unexpected provenance/SBOM attestations.
- Deployment of unapproved images or artifacts.
- Vulnerability disclosures affecting inventoried components.
- Supplier security incidents and end-of-life notices.

Correlate source commit, workflow run, builder identity, artifact digest, signing event, release ID and deployment digest. Alert on broken lineage and unexpected trust transitions.

## 24. Incident response and recovery

### 24.1 Scenarios

Prepare playbooks for malicious dependency, package maintainer compromise, registry compromise, compromised developer account, malicious pull request, CI runner compromise, workflow poisoning, secret theft, signing identity compromise, artifact replacement, supplier compromise and malicious update distribution.

### 24.2 Response sequence

1. Declare incident and assign incident commander.
2. Identify affected repositories, workflows, identities, artifacts, versions and consumers.
3. Preserve source, workflow, runner, package, registry, signing and deployment evidence.
4. Suspend affected workflows and freeze risky releases without destroying evidence.
5. Revoke exposed tokens, workload identities, signing certificates and sessions as appropriate.
6. Quarantine suspect package versions and artifacts; block further promotion.
7. Determine whether compromise affected source, build, artifact, signature or distribution.
8. Use SBOM, provenance and deployment inventory to identify affected products and customers.
9. Rebuild from known-good source and trusted builders when required.
10. Verify new artifacts, attestations, signatures and deployment policy independently.
11. Coordinate supplier, customer, regulator and public disclosure through authorized functions.
12. Conduct root-cause analysis and implement preventive, detective and recovery improvements.

### 24.3 Recovery assurance

Do not resume solely because a package has been removed or a token rotated. Validate trust roots, runner images, workflows, source history, dependency graph, artifact digests, deployment state and downstream consumers. Re-establish provenance from a trusted build.

## 25. Metrics and management reporting

Use measures that indicate control effectiveness, not just tool volume:
- Percentage of production releases with complete, validated SBOM.
- Percentage of releases with authenticated provenance and verified signatures.
- Percentage of builds using ephemeral isolated runners.
- Percentage of dependencies pinned and resolved from approved sources.
- Percentage of repositories with enforced branch protections and review rules.
- Mean time to identify affected products after a new advisory.
- Mean time to remediate exploitable critical/high dependency issues.
- Percentage of critical suppliers assessed within review period.
- Number of unapproved artifacts or signature-verification failures blocked.
- Percentage of production workloads mapped to immutable artifact digests.
- Percentage of release exceptions with owner, expiry and compensating controls.
- Time to revoke compromised build/signing identities and contain releases.

Define denominators, scope, measurement source, owner and target. Do not compare teams using raw vulnerability counts without context.

## 26. Exception and risk acceptance

Every exception must record scope, affected product/repository/component, reason, evidence, impact, compensating controls, accountable risk owner, approver, expiry, remediation plan and review trigger. Exceptions must not silently disable organization-wide controls. Critical signing, provenance, identity or artifact-verification bypass requires explicit senior approval and time-bounded containment.

## 27. Tooling reference architecture

Select tools based on ecosystem support, integration, accuracy, licensing, data handling, scalability and operational ownership. Example categories include:

| Control area | Example tools / projects | Intended use and limitation |
|---|---|---|
| SCA / dependency | OSV-Scanner, OWASP Dependency-Check, Trivy, ecosystem-native tools | Identify known vulnerable dependencies; quality depends on package identification and advisory coverage |
| SBOM generation | Syft, cdxgen, SPDX tooling, language-native exporters | Generate component inventories; validate completeness against packaged artifact |
| SBOM analysis | Grype, Dependency-Track, OSV-Scanner | Correlate components and vulnerability intelligence; verify affected ranges and context |
| Secrets | Gitleaks, TruffleHog, platform secret scanning | Detect exposed credentials; false positives and historical leakage need triage |
| Static analysis | Semgrep, CodeQL, compiler/language analyzers | Find source patterns; not proof of dependency or build integrity |
| Container | Trivy, Grype, Dockle, image policy tooling | Scan image components and configuration; scan results need release-context interpretation |
| Signing / verification | Sigstore Cosign, notation, platform-native signing | Sign and verify artifacts and attestations; configure identity and trust policy securely |
| Provenance / attestations | SLSA tooling, in-toto, GitHub artifact attestations | Record build origin and materials; consumer policy must verify claims |
| Build hardening | Ephemeral runners, hardened images, isolated builders | Reduce persistence and cross-job compromise; requires platform governance |
| Repository governance | Branch protection, rulesets, CODEOWNERS, secret scanning, dependency alerts | Enforce review and access policy; platform defaults must be audited |
| Policy as code | OPA, Conftest, Kyverno, admission policy | Enforce release and deployment policy; policy lifecycle itself must be secured |

Tool output is evidence for triage, not a substitute for threat modeling, source review, release verification or incident response.

## 28. Standards and framework mapping

| Source | Relevant coverage | Application in this chapter | Mapping caveat |
|---|---|---|---|
| NIST SP 800-218 SSDF v1.1 | Prepare the Organization, Protect the Software, Produce Well-Secured Software, Respond to Vulnerabilities | Governance, source protection, build/release integrity, vulnerability response | Outcome/practice mapping must be made to exact task IDs in the published document |
| SLSA v1.2 | Source track L1–L4 and Build track L0–L3 | Source history/review/technical controls, provenance, hosted builder and hardened build isolation | Name track and level separately; verify all normative requirements and evidence before claiming conformance |
| in-toto | Supply-chain steps, layouts, links and attestations | Define and verify authorized supply-chain steps | Secure layout/key distribution and verifier policy |
| SPDX 3.0.1 | Software component, provenance and license exchange | SBOM and license inventory | Pin spec version and validate consumers |
| CycloneDX 1.7 | BOM, dependency graph, vulnerability, VEX and attestations | SBOM/VEX and software/AI asset inventory | Pin schema and validate implementation support |
| Sigstore | Artifact signatures, short-lived certificates and transparency | Artifact/attestation signing and verification | Trust identity and issuer constraints explicitly |
| OpenSSF Scorecard | Open-source project security posture signals | Supplier/dependency risk input | Heuristic score; not a certification or proof of safety |
| CISA SBOM Minimum Elements 2026 | Minimum SBOM content and exchange practices | SBOM quality and supplier expectations | Verify current guidance and sector/contract applicability |
| ISO/IEC 27001:2022 | Supplier, access, change, configuration, vulnerability and continuity controls | Governance and evidence integration | Map to exact Annex A controls in standards chapter |
| ISO/IEC 27036 series | Supplier relationship security | Supplier due diligence, contracts and monitoring | Confirm applicable part and current edition |
| PCI DSS v4.0.1 | Software development and security practices for applicable environments | Payment software and CDE supply-chain controls | Only where applicable; map exact requirements |
| EU Cyber Resilience Act | Secure product lifecycle, vulnerability handling and reporting | Product release and vulnerability response | Legal applicability and phased dates require counsel |
| OWASP SAMM | Secure build and deployment, defect management, governance | Maturity assessment | Maturity model, not certification |

### 28.1 NIST SSDF v1.1 practice-to-chapter mapping

NIST SP 800-218 SSDF v1.1 is the published baseline used here. The following is this project's informative mapping of relevant SSDF task identifiers to chapter sections and evidence. It is not a NIST-endorsed crosswalk, a complete mapping of every SSDF task, or a certification checklist. Applicability must be assessed for the software and supplier model.

| SSDF practice/task | NIST task intent (summary) | Chapter sections | Example evidence |
|---|---|---|---|
| PO.1.1 | Define security requirements for development infrastructure and processes | 4, 7, 8, 14, 26 | Supply-chain policy, toolchain security requirements and exception register |
| PO.1.2 | Define security requirements for organization-developed software | 2, 3, 19, 31 | Release integrity requirements, archive policy and release criteria |
| PO.1.3 | Define and address requirements for third-party software | 9, 10, 20, 21 | Component intake criteria, supplier requirements and exceptions |
| PO.2.1 | Define and maintain SDLC roles and responsibilities | 4, 21, 24 | RACI, repository owner and incident roles |
| PO.2.2 | Provide role-based secure development training | 4, 8, 14, 24 | Developer, reviewer, platform and release training records |
| PO.3.1 | Specify toolchain tools and integration requirements | 14, 27 | Approved toolchain architecture and data-flow definitions |
| PO.3.2 | Securely deploy, operate and maintain toolchains | 8, 14, 23 | Tool hardening, provenance checks, patching and monitoring records |
| PO.5.1 | Separate and protect software development environments | 14, 18 | Environment segmentation, access and egress policy |
| PS.1.1 | Restrict access to all code forms and protect from tampering | 7, 14, 18 | Repository ACLs, protected branches, workflow and configuration controls |
| PS.2.1 | Make software integrity verification information available to acquirers | 16, 19, 31 | Artifact digest, signature and consumer verification instructions |
| PS.3.1 | Securely archive release files and supporting data | 19, 24, 31 | Immutable release archive, retention and access evidence |
| PS.3.2 | Collect, protect, maintain and share provenance for release components, including SBOM | 12, 15, 31 | Release SBOM, provenance, component lineage and integrity verification |
| PW.4.1 | Acquire and maintain well-secured third-party components | 9, 10, 11, 20, 21 | Component approval, provenance, maintenance and vulnerability assessment |
| PW.4.4 | Analyze third-party components for known vulnerabilities and maintenance status | 9, 11, 20 | SCA reports, advisory triage and end-of-life decisions |
| PW.6.1 / PW.6.2 | Securely configure compiler, interpreter and build processes | 14, 15 | Pinned toolchain, hardened build flags and build configuration review |
| RV.1.1 | Gather and investigate vulnerability reports for product and third-party components | 11, 23, 24 | Advisory monitoring, triage record and affected-product analysis |
| RV.1.2 | Review and test code to identify or confirm vulnerabilities | 11, 14, 17, 18 | SCA/SAST/image scan and controlled validation evidence |
| RV.1.3 | Establish vulnerability disclosure and remediation policy and roles | 21, 24 | Supplier notification, PSIRT workflow and response playbook |
| RV.2.1 / RV.2.2 | Assess risk and plan/implement vulnerability response | 11, 13, 24, 26 | Risk decision, VEX, remediation plan and approved exception |
| RV.3.1–RV.3.4 | Analyze root causes and improve the SDLC to prevent recurrence | 24, 25 | Root-cause report, systemic fix and regression-control evidence |

NIST describes SSDF practices as outcome-focused and risk-based. The chapter therefore maps only the tasks directly relevant to software supply-chain controls; other SSDF tasks are covered in the broader Secure SDLC and Secure Coding chapters.

### 28.2 SLSA v1.2 track-to-control mapping

The SLSA v1.2 specification has separate Source and Build tracks. The mapping below translates those track outcomes into this chapter's control IDs. It is an implementation guide, not an assertion that the listed controls alone establish conformance.

| SLSA track/level | Main assurance outcome | Chapter control IDs | Required evidence before claiming the level |
|---|---|---|---|
| Source L1 | Source revisions are version controlled | SSC-C-001, SSC-C-002 | Repository and immutable revision inventory |
| Source L2 | Continuous history and source provenance | SSC-C-001, SSC-C-003, SSC-C-019 | Protected history, source provenance attestations and continuity evidence |
| Source L3 | Organizational technical controls continuously enforced | SSC-C-002, SSC-C-003, SSC-C-004, SSC-C-019 | Enforced branch/repository policy and verifiable control evidence |
| Source L4 | Two trusted persons review protected-branch changes | SSC-C-003, SSC-C-004 | Technical enforcement of independent two-person review, including bypass governance |
| Build L1 | Provenance exists and identifies artifact and build | SSC-C-011 | Provenance for artifact digest and build process |
| Build L2 | Hosted build platform produces signed provenance | SSC-C-009, SSC-C-010, SSC-C-011, SSC-C-012, SSC-C-013 | Hosted builder identity, signed provenance and consumer verification |
| Build L3 | Hardened build platform protects runs and signing secrets | SSC-C-009, SSC-C-010, SSC-C-011, SSC-C-012, SSC-C-013 | Strong isolation, non-exposure of signing secrets to user-defined build steps and verified provenance |

Before making a SLSA claim:
1. Pin the approved specification version and the applicable track.
2. Read the normative requirements for the exact level.
3. Identify which controls are implemented by the organization and which are inherited from the build/source platform.
4. Collect platform documentation and independently verifiable attestations.
5. Test bypass, identity, continuity and isolation assumptions.
6. Record gaps and do not claim a higher level based on partial implementation.

### 28.3 CISA 2026 SBOM minimum-elements alignment

CISA and international partners announced updated 2026 SBOM Minimum Elements on 29 July 2026. The announcement identifies refined fields including component hash, license, SBOM tool name and SBOM generation context, and calls out additional considerations for AI and SaaS software.

| CISA 2026 element / practice | Chapter implementation |
|---|---|
| Component hash | Sections 12.1 and 12.3; bind components to release/artifact digests |
| License | Sections 9.1 and 20; record license metadata and legal review |
| SBOM tool name | Section 12.3; capture generator identity and version |
| SBOM generation context | Section 12.3; record source, build, artifact, environment and configuration context |
| AI and SaaS considerations | Sections 5, 12, 21 and 22; extend inventory for model assets, services and dependencies |
| Machine-processable exchange | Sections 12.2 and 31; pin format/schema and validate consumers |

Use the official 2026 guidance for the complete required field definitions. This table is a concise chapter mapping, not a substitute for the complete CISA publication.

## 29. Control and test catalogue

The IDs below are internal project identifiers, not external standard control IDs.

| Control ID | Control objective | Minimum implementation evidence |
|---|---|---|
| SSC-C-001 | Maintain product/repository/dependency/build/artifact inventory | Owned inventory with immutable identifiers |
| SSC-C-002 | Enforce least privilege and MFA for source and CI administration | Access policy and access-review evidence |
| SSC-C-003 | Protect release branches and require independent review | Rulesets, CODEOWNERS and bypass audit |
| SSC-C-004 | Review privileged workflow changes | Workflow ownership and protected review rules |
| SSC-C-005 | Pin third-party workflow actions and build inputs | Lock/pin evidence and exception record |
| SSC-C-006 | Use approved dependency registries and namespace controls | Registry configuration and resolution logs |
| SSC-C-007 | Generate and validate release SBOM | SBOM attached to immutable release digest |
| SSC-C-008 | Assess dependency vulnerabilities and disposition | Advisory triage and approved VEX/equivalent |
| SSC-C-009 | Isolate build runners and prevent cross-job persistence | Runner image, lifecycle and egress evidence |
| SSC-C-010 | Protect build secrets and workload identity | OIDC/trust conditions and secret access logs |
| SSC-C-011 | Generate authenticated build provenance | Attestation tied to source, builder and artifact digest |
| SSC-C-012 | Sign release artifacts and attestations | Signature bundle and signing policy |
| SSC-C-013 | Verify artifacts before promotion/deployment | Verification policy and blocked-deploy evidence |
| SSC-C-014 | Secure container base images and registry | Digest pinning, scan and registry access evidence |
| SSC-C-015 | Protect IaC and deployment artifacts | Review, policy and plan/apply separation |
| SSC-C-016 | Enforce release approval and rollback readiness | Release record and rollback test |
| SSC-C-017 | Govern open-source licenses and supplier risk | Component/license review and supplier record |
| SSC-C-018 | Extend inventory to AI/ML assets | Model/dataset/adapter provenance and digest |
| SSC-C-019 | Monitor supply-chain trust transitions | Alerts for identity, workflow, registry and signing events |
| SSC-C-020 | Rehearse compromise and recovery | Tabletop or technical exercise evidence |
| SSC-C-021 | Enforce source-track controls and source provenance | Source history, review and technical-control attestations |
| SSC-C-022 | Enforce build-track provenance and hardened builder requirements | SLSA track/level evidence, builder identity and isolation tests |
| SSC-C-023 | Meet SBOM minimum metadata and generation-context requirements | Component hashes, licenses, tool identity and generation context |

| Test ID | Test objective | Expected result |
|---|---|---|
| SSC-T-001 | Review repository identity and privileged access | No unauthorized or shared privileged identities |
| SSC-T-002 | Attempt unauthorized protected-branch change in test repo | Change blocked and logged |
| SSC-T-003 | Modify a workflow without required owner review | Merge blocked |
| SSC-T-004 | Introduce an unpinned action in test workflow | Policy flags or blocks it |
| SSC-T-005 | Resolve a private package name from an unapproved registry | Resolution blocked |
| SSC-T-006 | Introduce a synthetic typo package in isolated registry | Detection/quarantine process activates |
| SSC-T-007 | Compare manifest, lockfile and resolved dependency graph | Drift is identified and reviewed |
| SSC-T-008 | Generate SBOM for release artifact | Valid SBOM matches packaged components |
| SSC-T-009 | Validate SBOM schema and completeness | Invalid or incomplete SBOM fails release gate |
| SSC-T-010 | Introduce synthetic vulnerable dependency | Finding maps to exact component/version |
| SSC-T-011 | Create a VEX not-affected disposition without evidence | Review rejects unsupported disposition |
| SSC-T-012 | Run untrusted PR on privileged runner in simulation | Privileged secrets and deployment identity unavailable |
| SSC-T-013 | Attempt cross-job workspace/cache access | Isolation prevents data reuse |
| SSC-T-014 | Attempt to read unrelated secret from workflow | Access denied |
| SSC-T-015 | Request workload identity with wrong repository/ref/audience | Identity provider denies token |
| SSC-T-016 | Generate provenance for controlled build | Source, builder, workflow and digest are recorded |
| SSC-T-017 | Alter artifact after provenance creation | Digest verification fails |
| SSC-T-018 | Sign artifact using approved identity | Signature validates against expected identity |
| SSC-T-019 | Verify artifact signed by untrusted identity | Verification fails |
| SSC-T-020 | Attempt deployment of unsigned artifact | Production policy blocks deployment |
| SSC-T-021 | Attempt deployment using mutable tag where digest required | Admission/release policy rejects |
| SSC-T-022 | Introduce untrusted container base image | Policy flags or blocks image |
| SSC-T-023 | Modify IaC to expose a test service publicly | Policy check blocks or requires approval |
| SSC-T-024 | Simulate registry tag overwrite | Digest pinning detects mismatch |
| SSC-T-025 | Revoke test signing identity | New signatures rejected and incident process triggered |
| SSC-T-026 | Simulate compromised dependency release | Affected product inventory is identified |
| SSC-T-027 | Simulate supplier incident notification | Owner, scope and response workflow are exercised |
| SSC-T-028 | Verify AI model/dataset asset provenance | Unapproved or mismatched asset is rejected |
| SSC-T-029 | Verify release record contains all required evidence | Release gate reports missing evidence |
| SSC-T-030 | Exercise compromise recovery and rebuild | Trusted rebuild, re-sign, redeploy and evidence chain completed |
| SSC-T-031 | Verify source revision history and source provenance attestation | Source revision, actor, parent and change-control evidence are verifiable |
| SSC-T-032 | Attempt change to protected source ref without required technical controls | Source control system blocks change and records evidence |
| SSC-T-033 | Attempt protected-branch change without two trusted reviewers | Change is blocked by technical enforcement |
| SSC-T-034 | Verify Build L3 isolation between concurrent/untrusted runs | Runs cannot influence one another and signing secrets are inaccessible to user-defined steps |
| SSC-T-035 | Validate CISA 2026 SBOM metadata and generation context | Required component hashes, licenses, tool identity and generation context are present or documented as unavailable |

## 30. Detection catalogue

| Detection ID | Signal | Response |
|---|---|---|
| SSC-D-001 | Privileged repository access or owner change | Validate request and review account/session |
| SSC-D-002 | Branch protection or ruleset weakened/bypassed | Freeze sensitive merges and investigate |
| SSC-D-003 | New or modified workflow/action reference | Review diff, pin and assess execution context |
| SSC-D-004 | Unexpected package registry or namespace | Block resolution and investigate dependency source |
| SSC-D-005 | New package publisher/maintainer or ownership transfer | Quarantine update pending validation |
| SSC-D-006 | Suspicious install script or package behavior | Isolate build and preserve package archive |
| SSC-D-007 | Lockfile changes outside approved update | Require dependency review |
| SSC-D-008 | Build runner registration or image drift | Quarantine runner and rebuild from trusted image |
| SSC-D-009 | Unusual runner egress or metadata access | Terminate job, isolate runner and rotate exposed identity |
| SSC-D-010 | Secret access from untrusted PR/job | Revoke credential and investigate execution path |
| SSC-D-011 | Workload identity request outside expected subject/audience | Deny token and alert IAM owner |
| SSC-D-012 | Missing or malformed provenance | Block promotion and investigate build process |
| SSC-D-013 | Artifact digest differs across stages | Stop release and investigate tampering |
| SSC-D-014 | Signature from unexpected identity | Reject artifact and investigate signer |
| SSC-D-015 | Signing activity outside release workflow | Revoke/disable identity and start incident response |
| SSC-D-016 | Registry tag overwrite or permission change | Preserve registry logs and verify all consumers |
| SSC-D-017 | Deployment of unapproved/unsigned image | Block or roll back workload |
| SSC-D-018 | SBOM missing or inconsistent with image | Quarantine release and regenerate inventory |
| SSC-D-019 | New critical advisory affects production component | Identify products, owners and remediation deadline |
| SSC-D-020 | Supplier reports compromise or malicious release | Trigger supplier incident workflow and freeze updates |
| SSC-D-021 | Unexpected package download from public internet | Block egress and review dependency source |
| SSC-D-022 | Release evidence or approval missing | Stop release promotion |
| SSC-D-023 | Signing key/certificate nearing expiry or revoked | Rotate trust material and verify consumer readiness |
| SSC-D-024 | AI model/dataset digest or publisher mismatch | Quarantine asset and prevent model deployment |
| SSC-D-025 | Rebuild differs from expected artifact without explanation | Investigate nondeterminism, toolchain and possible compromise |
| SSC-D-026 | Source provenance missing or control-continuity claim cannot be verified | Block source-level assurance claim and investigate repository control gap |
| SSC-D-027 | Build isolation or signing-secret boundary is violated | Stop affected builds, revoke credentials and quarantine artifacts |
| SSC-D-028 | SBOM lacks required metadata or generation context | Quarantine release evidence and regenerate/validate SBOM |

## 31. Minimum release evidence package

For each production release retain:
- Product, version, release ID and owner.
- Repository, immutable commit and reviewed pull request.
- Build workflow and builder identity.
- Dependency lockfiles and resolved component inventory.
- SBOM and schema validation result.
- Vulnerability assessment and VEX/exception decisions.
- Build provenance and attestation verification.
- Artifact digest, signature and signer identity.
- Container image digest and base-image evidence where applicable.
- Test, code scanning and policy gate results.
- Release approval and separation-of-duties evidence.
- Deployment target and deployed digest.
- Rollback plan and verification.
- Supplier/license review where relevant.
- Exception register and expiry.
- Retention location and evidence integrity control.

## 32. Related chapters
- [13. Software Supply Chain Security Lab Pack](SOFTWARE-SUPPLY-CHAIN-SECURITY-LAB-PACK.md)

- [03. Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [10. Cloud-Native Application Security](../10-cloud-native-application-security/CLOUD-NATIVE-APPLICATION-SECURITY-ENGINEERING.md)
- [11. Distributed Systems and Integration Security](../11-distributed-systems-integration-security/DISTRIBUTED-SYSTEMS-AND-INTEGRATION-SECURITY-ENGINEERING.md)
- [12. AI and LLM Application Security](../12-ai-llm-application-security/AI-AND-LLM-APPLICATION-SECURITY-ENGINEERING.md)
- [18. Standards Baseline and Mapping Method](../18-standards-frameworks/STANDARDS-BASELINE-AND-MAPPING-METHOD.md)

## 33. References

1. NIST SP 800-218 SSDF v1.1: https://csrc.nist.gov/pubs/sp/800/218/final
2. NIST SP 800-204D: https://csrc.nist.gov/pubs/sp/800/204/d/final
3. SLSA v1.2 specification: https://slsa.dev/spec/v1.2/
4. SLSA v1.2 Source track requirements: https://slsa.dev/spec/v1.2/source-requirements
5. SLSA v1.2 Build track requirements: https://slsa.dev/spec/v1.2/build-requirements
6. SLSA v1.2 Build provenance: https://slsa.dev/spec/v1.2/build-provenance
7. in-toto: https://in-toto.io/
8. SPDX 3.0.1 specification: https://spdx.github.io/spdx-spec/v3.0.1/
9. CycloneDX 1.7 specification: https://cyclonedx.org/specification/overview/
10. CISA 2026 Minimum Elements for an SBOM announcement: https://content.govdelivery.com/accounts/USDHSCISA/bulletins/422a7eb
11. Sigstore documentation: https://docs.sigstore.dev/
12. Cosign quickstart: https://docs.sigstore.dev/quickstart/quickstart-cosign/
13. GitHub artifact attestations: https://docs.github.com/en/actions/concepts/security/artifact-attestations
14. GitHub attestation generation and verification: https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations
15. OpenVEX v0.2.0 specification: https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md
16. CISA Minimum Requirements for VEX: https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf
17. OpenSSF Scorecard: https://scorecard.dev/
18. OpenSSF Best Practices: https://www.bestpractices.dev/
19. OSV database: https://osv.dev/
20. OSV-Scanner: https://google.github.io/osv-scanner/
21. OWASP Dependency-Track: https://dependencytrack.org/
22. Syft: https://github.com/anchore/syft
23. Grype: https://github.com/anchore/grype
24. in-toto attestation framework: https://github.com/in-toto/attestation
25. NIST CSF 2.0: https://www.nist.gov/cyberframework
26. ISO/IEC 27001:2022: https://www.iso.org/standard/27001
27. ISO/IEC 27036 supplier relationship security: https://www.iso.org/standard/82905.html
28. PCI DSS v4.0.1: https://www.pcisecuritystandards.org/document_library/
29. EU Cyber Resilience Act: https://eur-lex.europa.eu/eli/reg/2024/2847/oj
30. OWASP SAMM: https://owaspsamm.org/

## 34. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-19 | Initial software supply-chain security engineering baseline |
| 0.2 | 2026-11-19 | Add NIST SSDF task mappings, SLSA v1.2 Source/Build tracks and CISA 2026 SBOM alignment |
| 0.3 | 2026-11-20 | Clarify VEX status semantics, OpenVEX requirements and implementation profile |
| 0.4 | 2026-11-20 | Add executable VEX validator profile and link SSC-C-008 / SSC-T-011 implementation evidence |
| 0.5 | 2026-11-20 | Add isolated GitHub signed SLSA build-provenance implementation profile |
| 0.6 | 2026-11-26 | Record successful synthetic signed provenance workflow and negative verification evidence |
| 0.7 | 2026-11-26 | Add successful Cosign keyless artifact-signing prototype and verification profile |
| 0.8 | 2026-11-26 | Add Cosign execution evidence and Lab 15 implementation cross-reference |
