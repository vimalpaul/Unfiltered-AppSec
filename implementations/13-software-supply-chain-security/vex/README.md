# Vulnerability Exploitability eXchange (VEX) and Disposition

| Field | Value |
|---|---|
| Format | OpenVEX v0.2.0 JSON-LD |
| Canonical control | SSC-C-008 — assess dependency vulnerabilities and disposition |
| Canonical test | SSC-T-011 — reject a VEX not-affected disposition without evidence |
| Status | Validator and policy prototype implemented; no production VEX statement issued |
| CI | `.github/workflows/vex-validation.yml` |

## 1. Purpose and boundary

A scanner match is a vulnerability candidate, not an approved product impact decision. VEX records a time-bounded assertion about the relationship between a vulnerability and a specific product. The decision must be supported by component identity, product identity, analysis evidence, reviewer and lifecycle metadata.

This implementation uses OpenVEX v0.2.0. It validates the core OpenVEX document and statement fields used by this repository. The validator is a project-specific structural and policy validator; it is **not** a complete JSON-LD processor or a full official OpenVEX JSON Schema validator.

## 2. OpenVEX statuses

| Status | Meaning | Default release-gate behavior |
|---|---|---|
| `not_affected` | Product is not affected; machine-readable justification or impact statement is mandatory | May pass only with required product SHA-256 identity and justification |
| `affected` | Product is affected; action statement is mandatory | Block |
| `fixed` | Product version contains a fix | May pass only with required product SHA-256 identity and remediation evidence outside this VEX-only check |
| `under_investigation` | Impact is not yet known | Block |

The release-gate behavior is this repository's policy overlay, not a change to OpenVEX semantics. A `fixed` status must still be supported by a verified fixed artifact, regression tests and release evidence before production promotion.

For `not_affected`, OpenVEX machine-readable justifications include:
- `component_not_present`
- `vulnerable_code_not_present`
- `vulnerable_code_not_in_execute_path`
- `vulnerable_code_cannot_be_controlled_by_adversary`
- `inline_mitigations_already_exist`

Do not select a justification merely because it is available in the enumeration. Attach concrete evidence, the assessed product/build context and an accountable reviewer. In particular, absence of a detected call path is not, by itself, proof that code cannot be reached.

## 3. Required assessment workflow

1. Ingest scanner finding and preserve original scanner output, database version and scan timestamp.
2. Normalize vulnerability identity (CVE/GHSA/vendor advisory) and package identity (prefer PURL; include CPE where useful).
3. Identify the exact product, release, SBOM and artifact digest containing the component.
4. Confirm affected version range using authoritative advisory and vendor sources.
5. Assess whether the vulnerable component is present in the exact product artifact.
6. Analyze code path, feature/configuration state, attacker-controlled input, execution context, privilege, network exposure and compensating controls.
7. Record evidence references, confidence, limitations and any assumptions.
8. Assign one OpenVEX status. Use `under_investigation` when evidence is incomplete.
9. Require peer review by an authorized security/product owner. The person who creates a `not_affected` assertion must not be its sole approver for a production release.
10. Publish versioned VEX, retain prior statements and update timestamps when the assessment changes.
11. Reassess when code, configuration, deployment topology, dependency version, exploit intelligence or mitigation changes.

## 4. Internal decision record

Use `decision-record-template.json` as the internal case record. It is not an OpenVEX document. Keep:
- finding ID, advisory IDs and original scanner evidence;
- product name/version, artifact SHA-256, SBOM digest and component PURL;
- advisory affected range and fixed version;
- CVSS version/vector/score and severity source;
- reachability, exposure, attacker control and runtime/configuration analysis;
- status, justification, evidence, confidence and residual risk;
- remediation/mitigation action, owner, approver and review dates;
- exception ID/expiry and re-evaluation triggers.

Do not publish confidential evidence or internal hostnames in public VEX documents. Reference controlled evidence IDs where necessary.

## 5. Validation and release policy

Run:

```bash
python implementations/13-software-supply-chain-security/vex/validate_openvex.py \
  --document implementations/13-software-supply-chain-security/vex/examples/synthetic-under-investigation.json

python -m unittest discover \
  -s implementations/13-software-supply-chain-security/vex -p 'test_*.py' -v
```

Use `--release-gate` only against a VEX document bound to the exact candidate product artifact. The gate requires SHA-256 product hashes and rejects `affected` or `under_investigation` statements. It is not yet wired into a product release pipeline.

The CI example is explicitly synthetic. No VEX statement has been issued for Unfiltered-AppSec itself, and no production component has been declared affected, fixed or not affected.

## 6. Known limitations

- No automated mapping from Grype findings into OpenVEX statements is performed. Scanner output must be reviewed and normalized before VEX authoring.
- No CVE/advisory enrichment, exploitability scoring or reachability analysis is performed.
- No full OpenVEX JSON Schema or JSON-LD semantic validation is performed.
- No cryptographic signing or identity verification of VEX documents is implemented.
- No production artifact release gate consumes VEX yet.
- The local release-gate evaluator checks statuses and SHA-256 product identity only; it does not independently verify remediation evidence, approval identity or evidence contents.
- VEX does not replace the internal vulnerability register, remediation tickets, exceptions, or SBOM.

## 7. References

- [OpenVEX v0.2.0 specification](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md)
- [OpenVEX JSON schema](https://github.com/openvex/spec/blob/main/openvex_json_schema.json)
- [CISA Minimum Requirements for VEX](https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf)
- [CycloneDX 1.7 JSON reference — vulnerability analysis](https://cyclonedx.org/docs/1.7/json/)
