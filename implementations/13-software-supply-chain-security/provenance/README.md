# SLSA v1.2 Build Provenance Implementation

| Field | Value |
|---|---|
| Scope | Synthetic archive build, GitHub-hosted signed provenance, digest verification and negative tests |
| Format | in-toto Statement with SLSA provenance predicate `https://slsa.dev/provenance/v1` |
| Attestation service | GitHub Artifact Attestations / Sigstore |
| Attestation action | `actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6` (v4.2.2) |
| Status | Implementation committed; workflow execution pending |
| Production use | Not approved |

## 1. What this implementation proves

This is a deliberately synthetic, non-production build. It demonstrates an end-to-end trust chain:

1. A low-privilege build job fetches the exact event commit and creates a deterministic demo archive.
2. The build job produces a metadata record binding the archive SHA-256 to the repository and source revision.
3. A separate job downloads the artifact and metadata, then independently checks repository, revision and digest.
4. The signing job uses GitHub Artifact Attestations to create a Sigstore-signed in-toto SLSA build-provenance attestation.
5. The workflow verifies the attestation using GitHub CLI, constrained to this repository and this exact workflow file.
6. Negative tests confirm that a modified artifact and an unapproved signer workflow are rejected.
7. The artifact, build metadata and Sigstore bundle are retained as workflow evidence.

The build job has only `contents: read`. The attestation job alone receives `id-token: write` and `attestations: write`; no user-controlled build script is executed in that job.

## 2. Trust boundaries

```text
Source commit on main
       |
       v
Build job (contents: read only)
       |
       | deterministic synthetic archive + SHA-256 metadata
       v
GitHub Actions artifact transport
       |
       v
Attestation job (no source checkout, no build script)
       |
       +--> independently check repository / commit / digest
       |
       +--> GitHub OIDC identity
       |
       +--> actions/attest (Sigstore signing)
       |
       v
Signed SLSA provenance attestation
       |
       v
gh attestation verify
       |
       +--> repository identity allow-list
       +--> signer workflow allow-list
       +--> artifact subject digest check
       |
       v
Negative tests: tampered subject and wrong signer must fail
```

## 3. Run and inspect

The workflow runs on pushes to `main` when the provenance implementation or its workflow changes. It can also be started manually on `main`.

After a successful run:
- Inspect the job summary and attestation URL.
- Inspect the `slsa-provenance-evidence` artifact.
- Verify the downloaded artifact independently:

```bash
gh attestation verify dist/unfiltered-appsec-demo.tar.gz \
  --repo vimalpaul/Unfiltered-AppSec \
  --signer-workflow vimalpaul/Unfiltered-AppSec/.github/workflows/slsa-build-provenance.yml
```

The exact signer workflow path is part of the verifier policy. A repository-wide trust statement such as “trust any workflow from this repository” is intentionally avoided.

## 4. SLSA v1.2 interpretation

SLSA v1.2 separates Source and Build tracks. This implementation focuses only on the Build track and uses the SLSA provenance predicate v1 URI. Do not confuse the predicate URI with a claimed SLSA level.

| Build level | Relevant property | Current implementation assessment |
|---|---|---|
| Build L0 | No guarantees | Not the target |
| Build L1 | Provenance exists and identifies the artifact and build | Demonstrated for this synthetic artifact if the workflow succeeds |
| Build L2 | Authenticated provenance from a hosted build platform | GitHub-signed attestation is exercised; full level assessment remains open |
| Build L3 | Strong resistance to tenant-controlled build tampering, including trusted control-plane provenance and isolation | Not claimed; this prototype is not a complete hardened builder assessment |

A successful attestation is not itself proof of a SLSA level. Level claims require assessing all applicable requirements, builder guarantees, provenance completeness and consumer verification policy. The split-job design reduces signing authority exposure but does not alone establish Build L3.

## 5. Security limitations

- The archive is synthetic and contains no production application.
- GitHub's signed attestation authenticates the provenance assertion; it does not prove the application is safe or that the build instructions are benign.
- The synthetic build metadata is a project test record. It is not itself trusted provenance until the signed GitHub attestation is independently verified.
- The workflow uses GitHub-hosted runners. Self-hosted runner security is outside this implementation.
- The workflow does not prove complete dependency capture, reproducible production builds, protected-branch enforcement or deployment admission.
- The negative tests validate digest and signer policy. They do not simulate a compromised GitHub control plane or compromised GitHub OIDC trust root.
- The workflow does not claim SLSA Build L2 or L3 certification/assurance for the repository or any product.

## 6. References

- [SLSA v1.2 specification](https://slsa.dev/spec/v1.2/)
- [SLSA v1.2 Build track basics](https://slsa.dev/spec/v1.2/build-track-basics)
- [SLSA v1.2 Build requirements](https://slsa.dev/spec/v1.2/build-requirements)
- [SLSA v1.2 Build provenance](https://slsa.dev/spec/v1.2/build-provenance)
- [GitHub artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations)
- [GitHub attestation generation](https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations)
- [GitHub attestation verification](https://cli.github.com/manual/gh_attestation_verify)
- [actions/attest v4.2.2](https://github.com/actions/attest/releases/tag/v4.2.2)
