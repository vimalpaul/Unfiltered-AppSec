# SBOM Generation Baseline

## Scope

The companion workflow scans the repository filesystem using Anchore Syft and produces two machine-readable SBOMs:

- CycloneDX JSON 1.7
- SPDX JSON 2.3

Syft is pinned to **v1.57.1**. The Linux AMD64 release archive is pinned to SHA-256:

`bf52519eb57f675d47c07d43213cb6dff6449f3d6d1147ff6701ed91f44eef0c`

The digest is taken from the GitHub release metadata for the immutable v1.57.1 release. The workflow checks the downloaded archive against that literal digest before extracting the executable. This is an integrity pin; the workflow does not perform Sigstore signature verification of the checksum bundle. For higher assurance, verify the official checksum file's Sigstore bundle with Cosign as described in the Anchore verification guide.

## Run locally

Install Syft v1.57.1 using the official Anchore installation guidance and verify the release artifact before use. From the repository root:

```bash
syft scan dir:. --source-name vimalpaul/Unfiltered-AppSec --source-version "$(git rev-parse HEAD)" \
  -o cyclonedx-json@1.7=/tmp/unfiltered-appsec.cdx.json \
  -o spdx-json@2.3=/tmp/unfiltered-appsec.spdx.json

python implementations/13-software-supply-chain-security/sbom/validate_sbom.py \
  --cyclonedx /tmp/unfiltered-appsec.cdx.json \
  --spdx /tmp/unfiltered-appsec.spdx.json
```

## CI evidence\n\nThe main-branch SBOM workflow completed successfully on 2026-11-20: [run 44755935644](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44755935644). It uploaded both formats as artifact ID `14636948729` with artifact digest `sha256:295bd0d6cb116cd4f7c7cf1919664eff276efde802d1969284c629d193bd9446`. GitHub reported an expiry of 2026-12-04. This confirms the workflow completed generation, structural checks and upload; it does not establish independent schema conformance or product-release completeness.\n\n## What this SBOM means

This repository is primarily a documentation and engineering-reference repository. A directory scan catalogs recognized package manifests and software components that Syft can identify in the scanned filesystem. It does not automatically represent deployed products, cloud services, runtime-loaded dependencies, supplier services, or artifacts built from other repositories.

A zero-component SBOM can be a valid scan result for a repository with no recognizable package manifests. Do not interpret zero components as proof that a product has no dependencies.

The workflow uploads the generated SBOMs as a GitHub Actions artifact with a 14-day retention period. The artifacts are not committed to the repository. For a real application release, scan the actual build output or immutable container image, not merely the source directory, and bind the SBOM to that artifact digest.

## Limitations

- No SCA vulnerability analysis or VEX generation is performed.
- No package reachability or exploitability analysis is performed.
- No provenance statement, signature or release attestation is generated.
- The workflow does not enforce a vulnerability threshold.
- The workflow does not upload SBOMs to a registry or deployment platform.
- Schema structure is checked for essential fields; this is not a full external JSON Schema conformance test.
- The SBOM is untrusted evidence for pull-request commits until the change is reviewed and merged.
\n## References\n\n- [Syft v1.57.1 immutable release](https://github.com/anchore/syft/releases/tag/v1.57.1)\n- [Syft CLI reference](https://oss.anchore.com/docs/reference/syft/cli/)\n- [Syft output formats](https://oss.anchore.com/docs/guides/sbom/formats/)\n- [Anchore release verification guidance](https://oss.anchore.com/docs/installation/verification/)\n