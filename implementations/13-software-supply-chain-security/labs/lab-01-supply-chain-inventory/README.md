# Lab 01 — Supply-chain asset inventory and data-flow map

| Field | Value |
|---|---|
| Lab ID | UAPPSEC-13-LAB-01 |
| Version | 1.0 |
| Status | Executable synthetic lab baseline; independent learner reproduction pending |
| Control mapping | SSC-C-001 |
| Test mapping | SSC-T-042 |
| Detection mapping | SSC-D-031 |
| Safety classification | Synthetic data only; no credentials, live targets or production integrations |

## 1. Objective

Create a reviewable inventory of a synthetic product's source repositories, source revisions, dependencies, registries, CI/CD workflows, runners, identities, build outputs, release artifacts, suppliers and deployment targets. Model relationships between those assets and make trust-boundary crossings visible.

This lab converts the Chapter 13 Lab 01 specification into a deterministic, executable evidence-generation exercise. It does not scan GitHub, cloud accounts, package registries or a live organization. The supplied fixture is synthetic and must not be mistaken for an inventory of this repository or any real product.

## 2. Learning outcomes

1. Distinguish an asset inventory from an SBOM, source-integrity manifest and provenance.
2. Assign stable identifiers, owners, criticality and trust zones to supply-chain assets.
3. Represent producer/consumer relationships and trust-boundary crossings.
4. Identify missing owners, orphan assets, dangling relationships and unsafe secret handling.
5. Generate deterministic JSON, CSV, Mermaid and Markdown evidence from one source record.
6. Explain inventory coverage and residual limitations to an engineering reviewer.

## 3. Architecture and trust boundaries

The synthetic scenario contains a source repository and protected branch, dependency/registry path, CI workflow and hosted runner, OIDC identity, release artifact, artifact registry, supplier and deployment target.

The data-flow map is a directed relationship graph. A relationship marked crosses_trust_boundary=true is a review point, not proof of a vulnerability. The generated graph distinguishes external supplier/registry boundaries from internal workflow transitions.

## 4. Prerequisites

- Python 3.10 or later; standard library only.
- A local clone or exported copy of this repository.
- No Docker daemon, cloud subscription, GitHub token or network access is required.
- Use the supplied synthetic fixture; do not add customer or production data.

## 5. Repository contents

- inventory.schema.json — JSON Schema Draft 2020-12 contract for the input record.
- fixtures/synthetic-product-inventory.json — synthetic product and asset graph.
- build_inventory.py — validation, normalization and deterministic evidence generator.
- tests/test_build_inventory.py — positive and negative unit tests.
- outputs/reference/ — checked-in reference outputs generated from the fixture.
- outputs/reference/SHA256SUMS — integrity hashes for the reference outputs.

## 6. Execution procedure

From the repository root:

~~~bash
LAB_DIR="implementations/13-software-supply-chain-security/labs/lab-01-supply-chain-inventory"
python3 -m unittest discover -s "$LAB_DIR/tests" -p 'test_*.py' -v
python3 "$LAB_DIR/build_inventory.py" \
  --input "$LAB_DIR/fixtures/synthetic-product-inventory.json" \
  --output-dir "$LAB_DIR/outputs/generated"
~~~

Review the generated files:

| Output | Purpose |
|---|---|
| inventory.normalized.json | Canonical inventory with stable identifiers and summary counts |
| assets.csv | Flat asset register across all asset categories |
| relationships.csv | Directed dependency/data-flow relationships |
| risk-register.csv | Explicit scenario-based risks from the input fixture |
| trust-boundary-map.mmd | Mermaid flowchart source for a compatible viewer |
| assessment-summary.md | Coverage counts, trust-boundary count and limitations |

The generator rejects malformed records instead of silently dropping or inventing assets. It does not infer completeness from the number of records.

## 7. Validation and expected results

The supplied fixture is expected to contain 12 assets across 10 asset categories, 11 directed relationships and 5 documented risk scenarios.

Expected test behavior:
- Valid fixture: accepted and deterministic outputs generated.
- Duplicate asset identifier: rejected.
- Relationship referencing an unknown asset: rejected.
- Self-referential relationship: rejected.
- Missing owner or criticality: rejected.
- Invalid criticality or trust-zone value: rejected.
- Inline credential-like attribute: rejected; only opaque secret-manager references may be recorded.
- Duplicate risk identifier or risk referencing an unknown asset: rejected.
- Repeated generation from the same input: byte-identical output files.

A passing result validates the input contract and generator behavior only. It does not prove that the inventory contains every asset in a real environment.

## 8. Analyst exercise

After the baseline succeeds, make a copy of the fixture and perform these controlled exercises:

1. Remove the owner from the release artifact. Confirm validation fails.
2. Add an unregistered public package registry and connect it to the dependency. Confirm the graph and counts change.
3. Change the dependency-to-registry relationship to cross a trust boundary. Confirm the Mermaid edge is marked as a boundary crossing.
4. Add a critical supplier with no evidence reference. Explain why the inventory is not review-ready.
5. Add a risk scenario for a compromised build runner and map it to the affected runner and release artifact.
6. Compare the resulting inventory with the expected architecture and record missing assets.

Do not edit the checked-in reference fixture during the exercise. Keep analyst variants in a separate working directory.

## 9. Evidence record

Retain the Lab ID, operator, reviewer and authorization record; host OS and Python version; input fixture SHA-256 and source revision; unit-test output; generated asset, relationship and risk counts; SHA-256 checksums of all generated outputs; rendered trust-boundary diagram or a note that Mermaid rendering was not tested; analyst observations; and cleanup confirmation.

## 10. Teardown

No persistent infrastructure or credentials are created. Remove the generated output directory and analyst fixture copies when evidence has been retained. Verify that no tokens, credentials or production identifiers were added to the input.

## 11. Limitations and next maturity gate

This lab is an inventory-modeling exercise, not automated discovery. The schema does not connect to GitHub, cloud control planes, package managers, registries or CMDBs. Mermaid source generation is tested; rendering is not tested by the Python unit tests. Independent learner reproduction and practitioner review are still required before the lab can be marked independently validated.

## 12. Traceability

| Reference | Relationship |
|---|---|
| SSC-C-001 | Maintain product, repository, dependency, build and artifact inventory |
| SSC-T-042 | Validate required inventory coverage, unique identifiers and graph integrity |
| SSC-D-031 | Detect missing ownership, criticality or dangling asset relationships |
| Chapter 13 §3 | Supply-chain asset and trust-boundary model |
| Chapter 13 §29 | Control and test catalogue |
| Chapter 13 §30 | Detection catalogue |

## 13. Revision history

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-26 | First executable synthetic asset-inventory lab baseline |
