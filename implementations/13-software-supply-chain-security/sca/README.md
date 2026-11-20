# Software Composition Analysis (SCA) Baseline

## Scope

This baseline adds Grype vulnerability matching against the generated SPDX 2.3 SBOM. It uses the current immutable Anchore Grype release **v0.122.1**, published 2026-11-18. The Linux AMD64 archive is pinned to SHA-256:

`f1ba7e2917ee1395618de20a98da0aa7c0fb1788927797651047c50502a37538`

The workflow checks the downloaded archive against that digest before executing it. As with the Syft pin, this is an integrity pin sourced from immutable GitHub release metadata; the workflow does not independently verify the Sigstore signature of the checksum bundle.

## Run locally

Generate an SPDX SBOM first, then install the pinned Grype release using the official Anchore installation and verification guidance.

```bash
grype sbom:/path/to/unfiltered-appsec.spdx.json -o json > grype-results.json
python implementations/13-software-supply-chain-security/sca/validate_grype_report.py \
  --report grype-results.json
```

Grype consumes SPDX, CycloneDX and Syft SBOM formats. The vulnerability database is maintained separately from the scanner binary and is automatically checked/updated by Grype by default. Database freshness, schema and provider metadata must be retained with the scan record.

## CI evidence

The main-branch workflow completed on 2026-11-20: [run 44757253987](https://github.com/vimalpaul/Unfiltered-AppSec/actions/runs/44757253987). Syft identified 2 SPDX package records. Grype v0.122.1 scanned the SPDX SBOM using a valid vulnerability database (schema 6.1.10, built 2026-11-20T06:21:00Z) and reported 0 vulnerability matches. The four-file evidence artifact is ID `14639231729`, digest `sha256:cbdd4aa9592920fc044be122e2e62ab7a16a668fb3154a1f04b9d5bb824c1d7f`, with GitHub retention through 2026-12-04. This run proves the configured workflow executed; it does not establish that a deployed application is free of vulnerabilities.

## Current policy mode: report-only

The repository workflow generates a machine-readable report but does not set `--fail-on`. It runs Grype only when the SPDX SBOM contains package records; otherwise it records an explicit not-run disposition rather than a clean scan. A release-blocking severity threshold has not been approved or tuned for a real application. This repository is documentation-first and may contain no recognizable runtime packages; a scan with zero matches or zero packages must not be misrepresented as evidence that a product is vulnerability-free.

Before enabling a production gate, define:
- affected product and artifact digest;
- package identity and version (prefer PURL, include CPE where relevant);
- vulnerability identifier and authoritative advisory source;
- severity and scoring system/version;
- fixed/affected version range and fix state;
- exploitability, reachability, exposure and business impact;
- compensating controls and VEX disposition where justified;
- exception approver, expiry and retest/closure evidence.

A vulnerability scanner match is a lead for triage, not an automatic statement of exploitability. False positives, distro backports, unreachable code, mitigations and product-specific exposure require evidence-based disposition.

## References

- [Grype v0.122.1 immutable release](https://github.com/anchore/grype/releases/tag/v0.122.1)
- [Grype CLI reference](https://oss.anchore.com/docs/reference/grype/cli/)
- [Grype SBOM scan targets](https://oss.anchore.com/docs/guides/vulnerability/scan-targets/)
- [Grype vulnerability database](https://oss.anchore.com/docs/guides/vulnerability/database/)
- [Anchore release verification guidance](https://oss.anchore.com/docs/installation/verification/)
