# Lab 02 — Branch protection and code-owner review

| Field | Value |
|---|---|
| Lab ID | UAPPSEC-13-LAB-02 |
| Version | 1.0 |
| Status | Offline policy auditor and synthetic CI baseline; live disposable-repository exercise pending |
| Control mapping | SSC-C-003, SSC-C-004 |
| Test mapping | SSC-T-002, SSC-T-003 |
| Detection mapping | SSC-D-002 |
| Safety | Live auditor is GET-only; it does not change repository settings |

## 1. Objective

Verify that sensitive source and release changes cannot bypass pull-request review, independent approvals, CODEOWNERS review and required status checks.

Two modes are implemented:
- Offline fixture mode evaluates synthetic GitHub API response data without network access.
- Live audit mode uses the authenticated GitHub CLI to read branch protection and CODEOWNERS. It makes GET requests only.

A passing fixture is not proof of live GitHub enforcement. A passing live audit verifies only the configuration fields implemented here. Direct-push, force-push, deletion and stale-review behavior must be tested separately in a disposable repository.

## 2. Learning outcomes

1. Require pull requests and at least two independent approvals.
2. Require CODEOWNERS review for workflow, dependency and release changes.
3. Require current status checks and dismissal of stale approvals.
4. Verify administrator enforcement, bypass allowances, force-push and deletion settings.
5. Distinguish configuration evidence from observed enforcement evidence.
6. Generate a sanitized machine-readable audit report.

## 3. Architecture

    Disposable GitHub test repository
       |-- protected default branch
       |    |-- pull request requirement
       |    |-- two approvals and stale-review dismissal
       |    |-- CODEOWNERS review and required status checks
       |    |-- admin enforcement and bypass governance
       |-- test identities: contributor, reviewer A/B, code owner
       |
       +---- read-only auditor ---- GitHub REST API (GET)
                                      |
                                      +---- JSON audit report

The auditor never applies branch protection or attempts a push. Use separate identities and a disposable repository for enforcement experiments.

## 4. Prerequisites

- A disposable private GitHub repository where branch protection can be configured.
- GitHub CLI (gh), installed and authenticated as an identity permitted to read repository administration settings and contents.
- Fine-grained token permissions, when used: Administration: read and Contents: read.
- Python 3.12.16; standard library only.
- Two independent reviewer identities and a code-owner team for the manual exercise.
- Do not use the Unfiltered-AppSec production repository as the test target. Do not add test identities or change its branch protection.

## 5. Repository contents

- audit_repository.py — offline policy evaluator and read-only GitHub API auditor.
- policy.json — explicit minimum branch and CODEOWNERS policy.
- fixtures/healthy-repository.json — synthetic passing GitHub API response.
- fixtures/codeowners.healthy — synthetic CODEOWNERS file.
- tests/test_audit_repository.py — positive and negative unit tests.

## 6. Policy requirements

| Control | Required state | Failure condition |
|---|---|---|
| Protected branch | Valid protection response | No protection or API error |
| Pull requests | Review policy configured | Review policy missing |
| Independent review | At least 2 approvals | Fewer than 2 |
| Stale approvals | Dismissal enabled | Disabled or absent |
| Code-owner review | Required | Disabled or absent |
| Status checks | Strict and at least one context | Missing, empty or non-strict |
| Admin enforcement | Enabled | Admin bypass possible |
| Bypass allowances | No users, teams or apps | Any bypass actor configured |
| Force pushes | Disabled | Enabled or state unknown |
| Branch deletion | Disabled | Enabled or state unknown |
| CODEOWNERS | Supported location and effective ownership | Missing, malformed or sensitive path uncovered |

The policy requires explicit evidence. A missing field is not silently treated as secure.

## 7. Execution procedure

### 7.1 Offline tests

From the repository root:

~~~bash
LAB_DIR="implementations/13-software-supply-chain-security/labs/lab-02-branch-protection"
python3 -m unittest discover -s "$LAB_DIR/tests" -p 'test_*.py' -v
python3 "$LAB_DIR/audit_repository.py" \
  --fixture "$LAB_DIR/fixtures/healthy-repository.json" \
  --output "$LAB_DIR/evidence/offline-audit.json"
~~~

Expected result: PASS for the synthetic fixture. This is not a live GitHub configuration result.

### 7.2 Prepare a disposable repository

1. Create a private repository dedicated to this exercise.
2. Add synthetic source files and the supplied CODEOWNERS example.
3. Create separate contributor, reviewer A and reviewer B identities. Add a code-owner team with the required reviewers.
4. Ensure the contributor is not an administrator and is not a member of the code-owner team.
5. Protect the default branch using Section 6. Use GitHub's branch protection UI or an equivalent reviewed configuration process.
6. Require status checks from a trusted workflow that actually runs on pull requests.
7. Enable administrator enforcement, disable force pushes and branch deletion, and remove pull-request bypass actors.
8. Replace fictional team names with actual teams/users in the disposable organization.

### 7.3 Run the read-only live audit

Authenticate gh as a read-only audit identity:

~~~bash
python3 "$LAB_DIR/audit_repository.py" \
  --repo "YOUR-ORG/YOUR-DISPOSABLE-REPOSITORY" \
  --branch "main" \
  --output "$LAB_DIR/evidence/live-audit.json"
~~~

The script reads the branch protection endpoint and searches .github/CODEOWNERS, CODEOWNERS and docs/CODEOWNERS. It reports the file path and SHA-256 digest, relevant branch settings, findings and policy decision. It does not include credentials or token values.

A non-zero exit means the policy failed or the live audit could not be completed. An API permission error is ERROR, not PASS.

### 7.4 Manual enforcement tests

Use the non-admin contributor identity and disposable repository only.

1. Attempt a direct push to the protected default branch. Expected: GitHub rejects it because the branch requires pull requests.
2. Open a pull request changing a workflow file without code-owner approval. Expected: merge is blocked.
3. Obtain one approval from reviewer A. Expected: merge remains blocked because two approvals are required.
4. Obtain a second approval from reviewer B. Expected: approval count is satisfied, subject to other required checks.
5. Push another commit after approval. Expected: stale approvals are dismissed or made stale; new approvals are required.
6. Attempt a force-push to the protected branch. Expected: GitHub rejects it.
7. Attempt branch deletion. Expected: GitHub rejects it.
8. Inspect bypass configuration and audit events. Confirm no unexpected bypass actor exists and administrative changes are attributable.

Do not test force-push or deletion against a production branch. Do not use an administrator identity for contributor attempts.

### 7.5 Capture evidence

Retain, with secrets and personal data redacted:

- Branch protection settings export or sanitized API response.
- CODEOWNERS file and SHA-256 digest.
- Required status-check names and workflow run links.
- Test identity role matrix using role labels, not personal account details.
- Direct-push, insufficient-review, stale-approval, force-push and deletion outcomes.
- Relevant audit-log event IDs and timestamps.
- Read-only auditor JSON report.
- Deviations, exceptions, owner, expiry and remediation ticket.

A configuration screenshot is not proof that a negative enforcement attempt was performed. Record each observed test separately.

## 8. Expected results and failure interpretation

- Configuration PASS + enforcement PASS: retain both evidence sets.
- Configuration FAIL: do not claim the branch meets this lab's standard.
- Configuration PASS + enforcement FAIL: investigate ruleset precedence, actor privileges, bypass permissions, repository feature behavior and the exact branch tested.
- Audit ERROR: the auditor could not establish state, for example due to insufficient API permission or a non-404 API error. This is not PASS.
- CODEOWNERS pattern ambiguity: verify GitHub's actual matching behavior and confirm the last matching rule does not override the intended owner.

The matcher implements the constrained glob subset used by this lab, not every GitHub CODEOWNERS edge case. Actual GitHub enforcement remains authoritative.

## 9. Teardown

1. Export evidence and confirm secrets are redacted.
2. Remove test collaborators and temporary teams/permissions.
3. Delete the disposable repository if no longer required.
4. Revoke temporary tokens and sessions.
5. Remove local temporary evidence if it contains personal or organization-specific information.
6. Record teardown completion and evidence-retention owner.

## 10. Limitations

- Live auditor is read-only and uses GitHub's classic branch-protection endpoint. Repository rulesets and organization-level policy inheritance are not evaluated.
- CODEOWNERS matching implements the lab's constrained glob subset, not every GitHub pattern edge case.
- Offline fixtures validate policy logic, not GitHub enforcement.
- Live audit does not enumerate collaborator identities or prove reviewer independence.
- Manual negative tests and audit-log review are required before claiming effective enforcement.
- No repository settings are modified automatically.

## 11. References

- GitHub REST API — Get branch protection: https://docs.github.com/en/rest/branches/branch-protection#get-branch-protection
- GitHub Docs — About code owners: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- GitHub Docs — Managing protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- GitHub CLI manual: https://cli.github.com/manual/gh_api

## 12. Revision history

| Version | Date | Change | Evidence / status |
|---|---|---|---|
| 1.0 | 2026-11-27 | Initial offline policy auditor, read-only live GitHub audit, synthetic fixture and negative tests | CI validation pending; live disposable-repository exercise pending |
