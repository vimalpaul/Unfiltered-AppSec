# Cosign Keyless Artifact Signing and Verification

| Field | Value |
|---|---|
| Scope | Direct detached signature of a synthetic artifact using Cosign keyless signing |
| Tool | Cosign v3.1.6 |
| Signature format | Sigstore bundle |
| Identity | GitHub Actions OIDC workflow identity |
| Status | Synthetic keyless signing and verification workflow executed successfully; production integration remains open |
| Production use | Not approved |

## 1. Why this is separate from SLSA provenance

The SLSA workflow creates a signed provenance attestation: a statement about how an artifact was built. Cosign `sign-blob` creates a detached cryptographic signature over the artifact bytes themselves.

These controls complement one another:
- Provenance answers: which source and builder produced this artifact?
- A blob signature answers: do these exact bytes match the signature from the expected signing identity?

A signature does not prove the artifact is safe, and provenance does not replace artifact integrity verification.

## 2. Trust separation

1. The build job has `contents: read` only and creates the same deterministic synthetic archive using the shared fixture builder.
2. The build job uploads the archive and metadata to the separate signing job.
3. The signing job has `id-token: write` but no repository write or attestation permission. It does not check out the repository or execute source-controlled scripts.
4. The signing job validates the artifact digest and exact source metadata.
5. It installs Cosign v3.1.6 using release asset SHA-256 pins, then verifies the Cosign binary's own Sigstore release bundle against the official release identity.
6. Cosign signs the synthetic archive with an ephemeral keyless identity. The signature bundle includes the signature, certificate and transparency-log evidence.
7. Cosign verifies the signature against an exact workflow identity, OIDC issuer, repository, source ref, source commit and event.
8. Negative tests require verification to fail for a modified artifact, incorrect signer identity, incorrect issuer and incorrect source commit.

## 3. Verification policy

Expected signer certificate identity:

```text
https://github.com/vimalpaul/Unfiltered-AppSec/.github/workflows/cosign-artifact-signing.yml@refs/heads/main
```

Expected OIDC issuer:

```text
https://token.actions.githubusercontent.com
```

The workflow also verifies the GitHub-specific certificate claims for repository, ref, source commit and trigger. The exact identity and issuer are checked by Cosign; the certificate claim checks further narrow the trust policy.

## 4. Run and inspect

The workflow runs on `main` when the synthetic build scripts, signing tests, verification policy or workflow itself change.

After a successful run, inspect the `cosign-signing-evidence` artifact and verify the detached signature independently:

```bash
cosign verify-blob dist/unfiltered-appsec-demo.tar.gz \
  --bundle dist/cosign-signature.sigstore.json \
  --certificate-identity 'https://github.com/vimalpaul/Unfiltered-AppSec/.github/workflows/cosign-artifact-signing.yml@refs/heads/main' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com'
```

## 5. Cosign release pin

The implementation pins Cosign v3.1.6 and checks the Linux AMD64 binary and its Sigstore release bundle against SHA-256 values recorded in GitHub release asset metadata. It then uses Cosign to verify the binary's Sigstore bundle with the official Sigstore release identity.

The release checksum pin is an integrity check against the recorded release metadata; it is not a substitute for verifying the Sigstore bundle. The binary verification step is the cryptographic check.

## 6. Limitations

- Only a synthetic archive is signed; no production binary, package or container is signed.
- The signing identity is an ephemeral GitHub Actions OIDC identity; no long-lived private signing key is created or stored.
- The signing workflow is repository-controlled. Protected branch/ruleset enforcement and a separately administered reusable signing workflow are not yet verified.
- A green signing workflow does not establish SLSA Build L2/L3, artifact safety, complete provenance or deployment enforcement.
- The Cosign release is pinned to the Linux AMD64 binary; other platforms require separately verified pins.
- This workflow does not publish the artifact to a package registry or release channel.

## 7. References

- [Cosign v3.1.6 release](https://github.com/sigstore/cosign/releases/tag/v3.1.6)
- [Sigstore keyless blob signing](https://docs.sigstore.dev/cosign/signing/signing_with_blobs/)
- [Cosign blob verification](https://github.com/sigstore/cosign/blob/main/doc/cosign_verify-blob.md)
- [Sigstore verification quickstart](https://docs.sigstore.dev/quickstart/quickstart-cosign/)
- [Cosign binary verification guidance](https://docs.sigstore.dev/cosign/system_config/installation/)


## 8. Execution evidence — 2026-11-26

The workflow passed: [GitHub Actions run 45791994671](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/45791994671), source commit `e04b39fdf72bc8ee4c51c8a6668cda3db302bcb1`.

- Cosign version: `v3.1.6`
- Synthetic artifact SHA-256: `efe0d00c0552e89029750baf35b7620842a9a447b188f0d50f25473e8d8c69ac`
- Evidence artifact ID: `15103446197`
- Evidence artifact digest: `sha256:bf1cc7ac71b2cea025133d660cb25392fe42dd48686c7dfce2140f7795941747`
- Evidence retention: through 2026-12-10.

The signing job verified the pinned Cosign binary and its official Sigstore release bundle, signed the synthetic archive with GitHub OIDC, and verified the signature against the exact workflow certificate identity, issuer, repository, ref, source SHA and event trigger. Four negative tests rejected a modified blob, wrong signer identity, wrong OIDC issuer and wrong source revision.

This is successful synthetic signing evidence, not production release signing, key-management governance, revocation/recovery validation or deployment enforcement.
