# AI and LLM Application Security Lab Pack

| Field | Value |
|---|---|
| Document ID | UAPPSEC-12-LAB-001 |
| Status | Draft lab specifications |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-19 |
| Review due | 2027-02-19 |
| Scope | Prompt injection, RAG, vector stores, tools, agents, MCP, output handling, supply chain, privacy and operations |
| Classification | Public |

## 1. Safety, authorization and environment controls

These labs are for local applications, synthetic datasets, mock tools and disposable environments. Do not connect exercises to production identity, customer data, payment systems, external email, live deployment pipelines or real enterprise document stores.

Before starting:
- Obtain written authorization from the lab owner.
- Use synthetic users, tenants, documents, secrets and business records.
- Use local/mock model endpoints where practical; otherwise use an approved sandbox account with a strict spend ceiling.
- Disable real outbound email, payment, deployment, deletion and administrative tool effects.
- Use mock MCP servers and mock connector APIs.
- Restrict network egress; do not target real internal services or cloud metadata.
- Set maximum prompt size, output tokens, tool calls, recursion depth, concurrency and test cost.
- Do not upload real personal data, source code secrets or confidential business documents to public models.
- Do not poison production indexes, datasets or model artifacts.
- Capture sanitized evidence only; never include actual credentials or private keys.
- Review teardown and verify deletion of synthetic vectors, memory, logs and tool state.

Each lab is a specification, not a claim that an environment has been independently implemented. A lab is validated only after commands, versions, expected behavior, teardown and evidence are reproduced by a reviewer.

## 2. Common reference environment

Recommended local topology:
- Synthetic user portal and application backend.
- LLM orchestrator with model adapter.
- Local model or approved test model endpoint.
- Prompt/template repository with versioning.
- Document ingestion worker and parser sandbox.
- Synthetic document corpus with at least two tenants.
- Embedding service and local vector database.
- Tool gateway with mock read-only and write tools.
- Local MCP server exposing synthetic resources/tools.
- Synthetic memory store.
- Local telemetry collector with redaction.
- Evaluation harness and held-out test set.

The test application should expose safe lab-only tools such as:
- **get_order_status(order_id)** — read-only and tenant-scoped.
- **create_support_ticket(project_id, title, body)** — synthetic record creation.
- **draft_email(recipient_id, subject, body)** — draft only; no external send.
- **delete_test_record(record_id)** — disabled by default; only enabled in an isolated disposable database with explicit instructor approval.

Do not create generic shell, unrestricted SQL, arbitrary filesystem, arbitrary URL fetch or real-world email tools for beginner labs.

## 3. Evidence record

For each exercise capture:
- Lab ID, learner, reviewer and authorization.
- Environment, model/provider and exact versions.
- Prompt, model, tool and policy version identifiers.
- Synthetic user/tenant and data IDs.
- Preconditions and expected result.
- Exact sanitized steps and commands.
- Model response and tool proposal separately.
- Server-side authorization decision and tool execution result.
- Relevant retrieval IDs, policy decision and telemetry.
- Finding, root cause, remediation and retest.
- Cost/usage counters where relevant.
- Cleanup verification.

Redact prompts or outputs that include secrets or personal data even if synthetic; use stable markers such as TEST_SECRET_DO_NOT_USE.

## 4. Lab 01 — AI application inventory and trust-boundary mapping

**Objective:** Identify every AI component, data flow, identity and tool capability.

**Prerequisites:** Synthetic AI chat/RAG application or architecture diagram.

### Procedure

1. Identify client, gateway, backend, model provider and orchestrator.
2. Identify prompt templates, configuration stores and model versions.
3. Identify document sources, parsers, OCR, embedding services and vector stores.
4. Identify tools, connectors, MCP servers and agent runtimes.
5. Identify memory, conversation history and evaluation systems.
6. Identify every data category entering prompt, retrieval, tool, memory and telemetry.
7. Identify user, tenant, agent, tool and provider identities.
8. Draw synchronous and asynchronous data flows.
9. Mark trust boundaries, authorization points and external processors.
10. Record component owner, environment, criticality and data retention.

**Expected result:** Complete AI component inventory and trust-boundary map.

**Evidence:** Component register, data-flow diagram, tool inventory and open-risk list.

**Teardown:** No infrastructure required.

## 5. Lab 02 — Direct prompt injection

**Objective:** Test whether user-controlled instructions can bypass intended behavior or expose protected information.

**Prerequisites:** Local chat application with synthetic system/developer instructions and no privileged tools.

### Procedure

1. Configure the assistant to answer only from a synthetic public knowledge set.
2. Add a synthetic marker in the application-controlled prompt, such as INTERNAL_TEST_POLICY_MARKER.
3. Submit normal questions and establish baseline behavior.
4. Submit a direct instruction asking the model to ignore prior instructions.
5. Ask it to disclose hidden prompt/configuration content.
6. Try role-play, translation, encoded text and multi-message instruction splitting.
7. Ask for data belonging to a synthetic second user.
8. Repeat with paraphrased and multilingual variations.
9. Record whether the model reveals the marker or changes task boundaries.
10. Confirm no real secrets or privileged tools were present.

**Expected result:** Prompt-only behavior may vary, but no protected data or executable capability should be exposed. Application authorization must remain independent of model behavior.

**Evidence:** Test prompts, sanitized responses, prompt version and server-side access logs.

**Teardown:** Reset test conversation and prompt marker.

## 6. Lab 03 — Indirect prompt injection in a retrieved document

**Objective:** Demonstrate that retrieved content can contain hostile instructions and must remain untrusted.

**Prerequisites:** Local RAG application and synthetic document corpus.

### Procedure

1. Create a benign synthetic policy document for tenant A.
2. Create a second document containing normal text plus a clearly marked lab instruction attempting to override the assistant.
3. Ingest both documents through the normal pipeline.
4. Ask a question that retrieves the second document.
5. Observe whether the model follows the embedded instruction.
6. Ask the model to invoke a mock tool if tool use is enabled; keep all tools disabled for execution in this lab.
7. Inspect the assembled context and confirm source provenance is retained.
8. Add explicit trust labels and context separation as a mitigation.
9. Re-run the same prompt and compare results.
10. Verify that no tool or data authorization decision relies on the model's interpretation.

**Expected result:** The test reveals whether indirect injection influences the model; trusted application controls prevent any unauthorized action.

**Evidence:** Synthetic document hash, retrieved chunk IDs, assembled context and response.

**Teardown:** Delete synthetic documents and vectors.

## 7. Lab 04 — System prompt leakage and secret placement

**Objective:** Verify that sensitive values are not stored in prompts and that prompt disclosure has limited impact.

**Prerequisites:** Local application with versioned prompt configuration.

### Procedure

1. Inspect prompt templates and configuration for synthetic secret markers.
2. Record whether any credential-like value is embedded in the prompt.
3. Ask the model to reveal system/developer instructions.
4. Test direct and indirect prompt extraction requests.
5. Inspect API responses and logs for hidden configuration.
6. Move any synthetic secret out of the prompt and into a server-side secret store.
7. Ensure the model never receives the secret unless absolutely required.
8. Repeat the test and inspect the effect.
9. Verify backend authorization is unchanged if prompt text becomes visible.
10. Document prompt disclosure as an information exposure, not an authorization bypass by itself.

**Expected result:** No usable secret is present in prompt content; application security does not depend on prompt secrecy.

**Evidence:** Prompt review, secret scan output and sanitized response.

**Teardown:** Remove test marker and reset prompt version.

## 8. Lab 05 — Cross-tenant RAG isolation

**Objective:** Confirm that retrieval cannot return another tenant's documents.

**Prerequisites:** Two synthetic tenants, separate document ACLs and a local vector store.

### Procedure

1. Create tenant A and tenant B.
2. Upload a unique synthetic document marker to tenant B.
3. Index both tenants' documents.
4. Authenticate as tenant A.
5. Ask a question designed to retrieve tenant B's unique marker.
6. Inspect retrieval filters, namespace and returned chunk IDs.
7. Attempt to modify a client-supplied tenant parameter.
8. Attempt retrieval using a guessed document ID.
9. Verify backend derives tenant from authenticated context and applies ACL filters before prompt construction.
10. Revoke tenant B document access and repeat retrieval after cache/index invalidation.

**Expected result:** Tenant A never receives tenant B chunks or document metadata.

**Evidence:** Authenticated principal, retrieval filter, result IDs, policy decision and negative response.

**Teardown:** Delete both tenants, documents and vector records.

## 9. Lab 06 — Revoked document access and stale vector cache

**Objective:** Verify that permission revocation propagates to vector indexes and caches.

**Prerequisites:** RAG system with synthetic document ACL and cache.

### Procedure

1. Create a synthetic document with access for user A.
2. Index the document and confirm user A can retrieve it.
3. Revoke user A's document permission in the authoritative source.
4. Query immediately through the RAG endpoint.
5. Inspect cache, vector metadata and retrieval service behavior.
6. Verify the system re-checks authoritative ACL or invalidates stale access before context construction.
7. Repeat after index refresh.
8. Inspect logs for stale cache hits.
9. Test document deletion and re-indexing.
10. Record maximum revocation propagation time and residual exposure.

**Expected result:** Revoked content is not returned based solely on stale vector metadata or cache.

**Evidence:** ACL before/after, cache state, retrieval results and revocation timing.

**Teardown:** Delete synthetic document, vector and cache entries.

## 10. Lab 07 — Malicious document ingestion and parser isolation

**Objective:** Verify ingestion safely handles malformed files and cannot access prohibited network destinations.

**Prerequisites:** Disposable parser worker and mock internal endpoint.

### Procedure

1. Establish allowed file types and size limits.
2. Upload a normal synthetic PDF or DOCX and verify parsing.
3. Upload a malformed file with a misleading extension.
4. Upload an oversized file within the lab's safe limits.
5. Upload a test archive with controlled nested content.
6. Submit a document containing a URL to a local mock-only blocked destination.
7. Observe parser network behavior in the isolated environment.
8. Verify worker has no unnecessary network or host filesystem access.
9. Confirm resource limits and timeout stop abnormal processing.
10. Review quarantine and error handling.

**Expected result:** Parser rejects unsupported/malformed inputs, resource use is bounded and no prohibited network access occurs.

**Evidence:** File metadata, sandbox policy, network log and parser result.

**Teardown:** Remove test files and worker resources.

## 11. Lab 08 — Vector metadata filter manipulation

**Objective:** Verify that tenant and document filters are enforced server-side, not accepted from the user.

**Prerequisites:** Local vector database with tenant metadata.

### Procedure

1. Index synthetic chunks for tenant A and tenant B.
2. Implement retrieval using server-side tenant context.
3. Query as tenant A and verify tenant A results only.
4. Attempt to submit tenant B in a client parameter.
5. Attempt filter injection using unexpected metadata fields and operators.
6. Attempt to omit the filter or pass an empty filter.
7. Verify the retrieval service rejects invalid requests or applies mandatory policy filters.
8. Inspect vector database credentials and ensure client cannot query it directly.
9. Verify returned document IDs are checked against authoritative ACLs.
10. Add negative regression tests.

**Expected result:** Client-controlled filters cannot widen the retrieval scope.

**Evidence:** Request/response, effective filter and access-control logs.

**Teardown:** Delete lab namespaces and credentials.

## 12. Lab 09 — Tool allowlist and strict argument validation

**Objective:** Ensure model-proposed tool calls cannot select arbitrary tools or malformed arguments.

**Prerequisites:** Local agent runtime and mock tool gateway.

### Procedure

1. Register one read-only tool with a strict JSON schema.
2. Register one draft-only tool; disable all external side effects.
3. Submit a normal request that requires the read-only tool.
4. Submit a request proposing an unknown tool name.
5. Add unexpected properties to a valid tool argument object.
6. Supply wrong types, oversized strings and boundary values.
7. Supply a path, URL or resource identifier outside the allowlist.
8. Verify tool gateway validates schema and rejects unsafe arguments.
9. Confirm the model cannot call the underlying API directly.
10. Record rejected proposal and policy decision separately from model text.

**Expected result:** Only explicitly registered tools and valid bounded arguments reach execution.

**Evidence:** Tool registry, schema, validation logs and rejected call examples.

**Teardown:** Remove mock tools and test state.

## 13. Lab 10 — Tool object authorization and tenant isolation

**Objective:** Confirm a valid tool cannot access an object outside the caller's authorization.

**Prerequisites:** Synthetic order API with two tenants and mock read-only tool.

### Procedure

1. Create order A for tenant A and order B for tenant B.
2. Authenticate synthetic user A.
3. Call get_order_status for order A.
4. Call the same tool with order B's ID.
5. Attempt to modify tenant ID in tool arguments.
6. Attempt to pass a different user ID in the request body.
7. Verify tool gateway resolves actor and tenant from trusted server-side identity.
8. Verify the underlying API enforces object-level authorization independently.
9. Repeat through a second agent workflow.
10. Record both gateway and API authorization decisions.

**Expected result:** Cross-tenant object access is denied even when the model proposes a syntactically valid tool call.

**Evidence:** Synthetic object ownership, actor context and denial logs.

**Teardown:** Delete synthetic orders and test identities.

## 14. Lab 11 — Excessive agency and step-budget enforcement

**Objective:** Bound agent autonomy, recursion and multi-step tool use.

**Prerequisites:** Local agent with mock read-only and draft-only tools.

### Procedure

1. Configure a small maximum step count and tool-call budget.
2. Run a normal multi-step research task.
3. Request a workflow that repeatedly calls tools.
4. Request recursive agent delegation.
5. Attempt to call a disabled tool during the workflow.
6. Verify maximum step count and delegation depth are enforced by runtime.
7. Verify time and token budgets terminate the workflow.
8. Inspect partial state and ensure the user receives an accurate incomplete status.
9. Confirm retries do not reset the global workflow budget.
10. Test emergency stop while a workflow is active.

**Expected result:** Agent execution remains bounded and cannot bypass limits through recursion, retries or tool chaining.

**Evidence:** Workflow trace, step counter, token budget and stop event.

**Teardown:** Reset agent state and remove test workflow.

## 15. Lab 12 — Human approval binding and time-of-check/time-of-use

**Objective:** Ensure approval is tied to the exact action and cannot be reused after arguments change.

**Prerequisites:** Mock ticket creation tool; high-impact action simulated only.

### Procedure

1. Configure an action proposal with target, operation and argument digest.
2. Require approval from a synthetic authorized reviewer.
3. Display the exact action and target to the reviewer.
4. Approve the action and record approval ID and digest.
5. Modify one argument after approval but before execution.
6. Verify execution is blocked because the digest no longer matches.
7. Attempt to reuse the same approval for a second action.
8. Attempt approval after expiry.
9. Attempt self-approval by the initiating actor where separation of duties is required.
10. Verify the application re-checks authorization and resource state immediately before execution.

**Expected result:** Approval is specific, time-bounded, non-reusable and validated at execution.

**Evidence:** Approval record, action digest and blocked execution logs.

**Teardown:** Remove synthetic approvals and records.

## 16. Lab 13 — Agent memory poisoning and cross-session isolation

**Objective:** Protect persistent memory from untrusted writes and cross-user access.

**Prerequisites:** Local memory store with separate synthetic users.

### Procedure

1. Create user A and user B with isolated memory namespaces.
2. Store a benign preference for user A through the approved memory write path.
3. Submit untrusted content that attempts to create a privileged instruction in memory.
4. Inspect provenance and write authorization.
5. Query as user A and observe stored content handling.
6. Query as user B for user A's memory.
7. Attempt to modify memory using an unauthorized API path.
8. Test memory expiry, correction and deletion.
9. Verify secrets are rejected from memory storage.
10. Review memory audit records.

**Expected result:** Memory writes have provenance and authorization; one user's memory cannot influence another user's context.

**Evidence:** Memory record metadata, access decisions and deletion proof.

**Teardown:** Delete all synthetic memory and users.

## 17. Lab 14 — MCP server trust and tool response validation

**Objective:** Validate the trust boundary between an AI client and a connected MCP server.

**Prerequisites:** Local mock MCP server and client in an isolated environment.

### Procedure

1. Register an approved local MCP server with a synthetic tool.
2. Verify client displays the server identity and requested capabilities.
3. Connect an unapproved server in a separate test profile.
4. Return a tool description containing an instruction-like payload.
5. Return unexpected fields and malformed tool output.
6. Verify the client treats server-provided descriptions and results as untrusted data.
7. Verify the tool gateway still enforces authorization independently.
8. Change server version and confirm approval/review process.
9. Revoke the server and verify future tool calls stop.
10. Inspect connection, consent and tool invocation logs.

**Expected result:** Only approved servers are connected; tool output cannot change application authorization.

**Evidence:** Server registry, capability list, consent record and rejected tool output.

**Teardown:** Remove server registration and local credentials.

## 18. Lab 15 — MCP OAuth audience and confused deputy

**Objective:** Prevent a client or MCP server from forwarding a token to an unintended downstream resource.

**Prerequisites:** Local mock authorization server, MCP client/server and two resource APIs.

### Procedure

1. Register a synthetic MCP server and resource API.
2. Issue a token intended for the approved MCP resource.
3. Verify the resource validates issuer, audience, scope and expiry.
4. Attempt to use the same token against a different resource.
5. Verify wrong-audience use is rejected.
6. Configure a delegated flow for a downstream API.
7. Ensure the MCP server obtains an appropriately scoped token rather than forwarding the original token.
8. Attempt to request broader scopes than the client was granted.
9. Verify the authorization server and resource reject privilege escalation.
10. Record actor, client and resource identity separately.

**Expected result:** Tokens are resource-bound and the MCP server cannot become a confused deputy.

**Evidence:** Redacted token claims, authorization configuration and denial logs.

**Teardown:** Delete clients, resources and test keys.

## 19. Lab 16 — Unsafe output handling and XSS prevention

**Objective:** Ensure model-generated HTML/Markdown is treated as untrusted output.

**Prerequisites:** Local UI rendering AI-generated content.

### Procedure

1. Configure a test assistant to return normal Markdown.
2. Render output using the application's standard display path.
3. Submit synthetic HTML/script-like payloads in user input and retrieved content.
4. Observe whether the model returns active markup.
5. Verify the UI uses safe Markdown rendering and context-appropriate sanitization.
6. Test link schemes and external destinations.
7. Verify Content Security Policy and output encoding where applicable.
8. Confirm no unsafe DOM insertion or script execution occurs.
9. Test stored output viewed by a second synthetic user.
10. Record rendering behavior and remediation.

**Expected result:** Model output cannot execute script or create unsafe active content in the client.

**Evidence:** Sanitized payload, browser console/security behavior and renderer configuration.

**Teardown:** Clear synthetic conversations and cached output.

## 20. Lab 17 — Generated SQL/command and code execution sink

**Objective:** Verify generated text cannot reach execution sinks without a safe, constrained design.

**Prerequisites:** Local mock database and isolated disposable execution environment. No host shell access.

### Procedure

1. Identify application paths where model output is used in SQL, command, code or file operations.
2. Configure a synthetic query task using a structured query schema.
3. Submit a prompt requesting an unsafe raw query or command.
4. Verify application uses parameterized database operations or a restricted query builder.
5. Verify arbitrary SQL, shell and filesystem instructions are not executed.
6. Attempt unexpected table, column, path and operator values.
7. Verify allowlists and resource authorization.
8. Confirm any code execution occurs only in a disposable sandbox with no secrets and restricted network.
9. Inspect audit trail for rejected execution proposals.
10. Add regression tests for the identified sink.

**Expected result:** Generated text is never directly evaluated as privileged SQL, shell or code.

**Evidence:** Sink inventory, query builder policy and rejection logs.

**Teardown:** Destroy disposable database and execution environment.

## 21. Lab 18 — Structured output and citation integrity

**Objective:** Validate model output against strict schemas and confirm citations refer to real authorized sources.

**Prerequisites:** RAG app with synthetic documents and structured response schema.

### Procedure

1. Define a response schema with required fields and bounded values.
2. Ask a normal question and validate response.
3. Test missing fields, extra fields, wrong types and oversized values.
4. Ask for a citation to a document not in retrieval context.
5. Ask for a fabricated page number or source identifier.
6. Verify the application checks citations against retrieved source IDs and metadata.
7. Verify unauthorized source IDs are rejected.
8. Confirm malformed output does not trigger downstream action.
9. Record model output and application validation result separately.
10. Add schema and citation regression tests.

**Expected result:** Only validated output is consumed; citations are grounded in actual authorized retrieval results.

**Evidence:** Schema version, retrieved IDs, model output and validator result.

**Teardown:** Delete synthetic documents and response records.

## 22. Lab 19 — Dataset poisoning and evaluation integrity

**Objective:** Verify dataset changes are reviewed, versioned and evaluated before release.

**Prerequisites:** Synthetic evaluation dataset and controlled training/evaluation pipeline. No production model retraining.

### Procedure

1. Create a small synthetic dataset with benign examples.
2. Record dataset source, version, hash and owner.
3. Add a clearly marked synthetic anomalous/targeted sample.
4. Run dataset validation, duplicate and distribution checks.
5. Verify unapproved contributor cannot modify the release dataset.
6. Confirm held-out evaluation data is separate from training data.
7. Run baseline evaluation.
8. Compare results after the controlled dataset change.
9. Review lineage and approval records.
10. Verify release pipeline blocks unapproved dataset version.

**Expected result:** Dataset provenance and review controls detect or quarantine unauthorized changes; evaluation integrity is preserved.

**Evidence:** Dataset hashes, lineage, validation report and release gate.

**Teardown:** Delete synthetic dataset and pipeline artifacts.

## 23. Lab 20 — Model artifact provenance and safe loading

**Objective:** Verify model artifacts are approved and loaded in an isolated environment.

**Prerequisites:** Local test model artifact and isolated inference worker.

### Procedure

1. Select a permitted test model artifact.
2. Record source, license, version, hash and acquisition date.
3. Verify available signature/checksum or registry provenance.
4. Review package and loading dependencies.
5. Inspect model loader for unsafe deserialization behavior.
6. Load the model in an isolated worker without host secrets or broad network access.
7. Attempt to load an unapproved test artifact in a separate disposable environment.
8. Verify registry policy blocks unapproved artifact deployment.
9. Record runtime, tokenizer and adapter versions.
10. Test rollback to the known-good artifact.

**Expected result:** Model artifacts have traceable provenance and are loaded with least privilege and isolation.

**Evidence:** Model registry record, hash, approval and worker policy.

**Teardown:** Remove downloaded artifacts and worker.

## 24. Lab 21 — Rate limiting, token budgets and denial of wallet

**Objective:** Ensure model and tool usage cannot exceed configured budgets.

**Prerequisites:** Sandbox model endpoint with low explicit spend ceiling and mock tools.

### Procedure

1. Configure per-user and per-tenant request limits.
2. Configure prompt size, context, output token, concurrency and workflow step limits.
3. Run normal requests and record usage.
4. Submit a bounded series of requests that approach the quota.
5. Verify requests beyond the limit are throttled.
6. Trigger a synthetic tool-heavy workflow.
7. Verify tool-call and total workflow budgets are enforced.
8. Test cancellation and timeout.
9. Confirm retries do not reset the budget.
10. Verify cost alerts and graceful error behavior.

**Expected result:** Resource and spend limits are enforced server-side with observable throttling.

**Evidence:** Usage counters, quota decisions, alerts and billing estimate.

**Teardown:** Stop test requests and reset quotas.

## 25. Lab 22 — Multimodal prompt injection

**Objective:** Treat OCR, transcripts and media metadata as untrusted content.

**Prerequisites:** Local multimodal model or approved sandbox, synthetic image/audio files.

### Procedure

1. Create a benign synthetic image with ordinary text.
2. Create a second image containing a clearly marked instruction-like test string.
3. Submit both images to the application.
4. Observe OCR and model interpretation.
5. Create a short synthetic audio clip with benign speech and a test instruction.
6. Submit the audio and inspect transcript/context construction.
7. Verify multimodal content cannot change tool authorization or system policy.
8. Test file size, duration, codec and parser limits.
9. Inspect whether metadata and hidden text are passed to the model.
10. Record modality-specific limitations and mitigation.

**Expected result:** OCR/transcript/media-derived content remains untrusted and cannot independently authorize tool actions.

**Evidence:** Test files, transcript/OCR output, model context and policy decisions.

**Teardown:** Delete test media and transcripts.

## 26. Lab 23 — Telemetry privacy and data deletion

**Objective:** Prevent prompt, completion, tool and vector telemetry from exposing sensitive values and verify deletion behavior.

**Prerequisites:** Local telemetry collector, synthetic secret markers and test vector store.

### Procedure

1. Configure a synthetic prompt containing a marker that must not be logged.
2. Trigger a model request and mock tool call.
3. Inspect application logs, traces, provider metadata and evaluation records.
4. Verify redaction or exclusion of the marker and other sensitive attributes.
5. Check access permissions and retention configuration for telemetry.
6. Delete a synthetic source document and conversation.
7. Verify deletion from source store, vector index, cache and applicable memory store.
8. Review backup/retention behavior and documented deletion limits.
9. Confirm no unapproved telemetry exporter receives prompt content.
10. Record residual retention and provider dependencies.

**Expected result:** Sensitive data is minimized in telemetry and deletion covers all stores within the documented retention model.

**Evidence:** Redaction policy, access matrix, deletion logs and store verification.

**Teardown:** Delete synthetic logs, vectors and conversations where permitted.

## 27. Lab 24 — AI incident response tabletop and emergency stop

**Objective:** Practice containment of an agent that has been manipulated into unauthorized tool use.

**Scenario:** An uploaded synthetic document contains indirect prompt injection. An agent proposes an unauthorized tool call and the tool gateway detects an out-of-scope target.

### Procedure

1. Assign incident commander, AI application owner, AppSec, IAM, data owner, SOC and business owner.
2. Establish incident scope and timeline.
3. Disable the implicated tool and pause active agent workflows.
4. Preserve prompt version, model version, retrieved source IDs and tool proposal.
5. Identify whether any tool call executed or data was accessed.
6. Revoke affected tool credentials if compromise or exposure is suspected.
7. Quarantine the source document and related chunks/memory.
8. Assess user, tenant, data and provider/telemetry impact.
9. Reconcile any external side effects with authoritative systems.
10. Validate emergency stop and credential revocation.
11. Add regression tests and update detection logic.
12. Approve controlled resumption only after trust boundaries are validated.

**Expected result:** Team can stop the agent, preserve evidence, determine impact and recover without relying on model self-report.

**Evidence:** Timeline, tool audit, revocation record, source quarantine and recovery approval.

**Teardown:** Revoke exercise identities and reset synthetic data.

## 28. Lab 25 — Secure inter-agent communication

**Objective:** Verify that messages exchanged between agents preserve sender identity, task scope, integrity and replay protection.

**Prerequisites:** Two or more local agents with separate synthetic identities and a message broker or in-process message bus.

### Procedure

1. Register agent A and agent B with distinct workload identities.
2. Define a strict message schema containing sender, recipient, task ID, parent task ID, tenant, requested capability, expiry and correlation ID.
3. Configure agent B to accept only approved senders and task types.
4. Send a valid request from agent A and verify processing.
5. Attempt a message with a forged sender name but no valid identity.
6. Attempt a replay of a previously accepted task ID.
7. Attempt to change tenant, recipient or requested capability in transit.
8. Attempt to delegate a task outside agent A's permitted scope.
9. Verify the receiver independently authorizes the requested operation and does not trust natural-language claims of authority.
10. Review message audit and delegation lineage.

**Expected result:** Only authenticated, authorized, integrity-protected and in-scope agent messages are accepted; replay and privilege escalation are rejected.

**Evidence:** Agent identity matrix, message schema, rejected message logs and delegation trace.

**Teardown:** Revoke agent identities and delete synthetic task records.

## 29. Lab 26 — Cascading failure containment

**Objective:** Verify that agent/tool dependency failures do not create runaway retries, recursive delegation or uncontrolled side effects.

**Prerequisites:** Local orchestrator, two mock tools and a synthetic dependent agent.

### Procedure

1. Configure explicit workflow deadline, retry budget, concurrency ceiling and maximum delegation depth.
2. Run a normal workflow and record baseline calls and latency.
3. Configure one mock tool to return bounded transient errors.
4. Observe retries and verify exponential backoff and global workflow budget.
5. Configure a second tool to time out.
6. Verify circuit breaker and bulkhead behavior.
7. Simulate a child agent failing while the parent continues.
8. Verify the parent does not recursively create replacement agents without policy approval.
9. Confirm partial workflow state is durable and the user is not told the task succeeded.
10. Restore dependencies and verify controlled recovery without a retry burst.

**Expected result:** Failure is contained within the workflow budget; no uncontrolled agent fan-out or duplicate action occurs.

**Evidence:** Workflow trace, retry counters, circuit-breaker state and partial-state record.

**Teardown:** Restore mock tools and delete fault-injection configuration.

## 30. Lab 27 — Human-agent trust exploitation and action preview integrity

**Objective:** Ensure human reviewers are not induced to approve an action different from the canonical operation that will execute.

**Prerequisites:** Mock approval UI and draft-only synthetic tool.

### Procedure

1. Create a synthetic action with target, operation, arguments, impact summary and canonical digest.
2. Configure the agent to produce both a human-readable summary and machine-readable action.
3. Compare the displayed summary with the canonical action fields.
4. In a controlled test, make the summary omit a material argument or describe a different target.
5. Verify the approval UI presents the actual target, permissions, data and consequences independently of the agent's summary.
6. Attempt to alter action arguments after approval.
7. Verify the digest mismatch blocks execution.
8. Attempt to reuse an approval or use an expired approval.
9. Verify high-impact operations require a separate approver where policy requires.
10. Record what evidence the approver saw and what action the server executed.

**Expected result:** Approval is based on the canonical action, not a potentially deceptive agent-generated summary.

**Evidence:** UI capture with synthetic data, action digest, approval record and execution log.

**Teardown:** Delete approval and synthetic action.

## 31. Lab 28 — Rogue agent discovery, quarantine and kill switch

**Objective:** Detect and contain an agent that is unregistered, misconfigured or operating outside its declared capabilities.

**Prerequisites:** Disposable agent runtime, approved agent registry and mock tool gateway.

### Procedure

1. Register one approved synthetic agent with a declared identity, owner, model, prompt version and tool manifest.
2. Start the agent and verify it appears in inventory and telemetry.
3. In a separate lab namespace, launch an unregistered agent with a synthetic identity.
4. Attempt to access a tool using an undeclared capability.
5. Modify a test agent's tool manifest or runtime configuration without an approved change.
6. Verify inventory/configuration monitoring detects the drift.
7. Trigger quarantine and revoke the rogue agent's tool credentials.
8. Confirm active workflows stop or enter a safe suspended state.
9. Verify the agent cannot re-register itself or obtain new credentials without approval.
10. Review forensic records and recovery approval.

**Expected result:** Unregistered or policy-drifting agents are discovered, quarantined and prevented from continuing privileged actions.

**Evidence:** Agent registry, configuration diff, alert, revocation record and workflow stop event.

**Teardown:** Remove rogue agent, revoke all test identities and clean up namespace.

## 32. Assessment rubric

| Criterion | Points |
|---|---:|
| Architecture, inventory and trust boundaries | 10 |
| Direct/indirect prompt injection and prompt protection | 10 |
| RAG, document ingestion, vector and tenant isolation | 15 |
| Tool gateway, authorization, agent autonomy and approval | 15 |
| MCP, identity/delegation and inter-agent communication security | 10 |
| Output handling and downstream sinks | 10 |
| Model/data supply chain and evaluation integrity | 10 |
| Privacy, memory, multimodal and telemetry | 10 |
| Rate limits, cascading failure, rogue-agent containment, detection, incident response and cleanup | 10 |
| **Total** | **100** |

Suggested training interpretation: 90–100 strong independent engineering; 75–89 competent with review; 60–74 guided remediation required; below 60 repeat the exercises. These are educational thresholds, not a certification.

## 33. Instructor review checklist

- Was the environment authorized and isolated?
- Were all models, prompts, datasets, tools and connectors inventoried?
- Were user, tenant, agent and tool identities separated?
- Were direct and indirect prompt injection paths tested?
- Were secrets kept out of prompts and model context?
- Were RAG ACLs enforced before context construction?
- Was stale vector/cache access tested after revocation?
- Were parsers isolated and network restricted?
- Were tool names and arguments validated server-side?
- Did tools enforce object and tenant authorization?
- Were agent steps, recursion, tokens and costs bounded?
- Was human approval bound to the exact action?
- Were memory writes and cross-session access controlled?
- Were MCP server trust and token audience validated?
- Were inter-agent identities, task scope, integrity and replay protection tested?
- Were cascading failures and agent fan-out contained?
- Was human approval based on canonical action details rather than agent summaries?
- Were rogue agent registration, configuration drift and quarantine tested?
- Was output safely rendered and prevented from reaching execution sinks?
- Were citations checked against real authorized source IDs?
- Were model artifacts and datasets traceable and approved?
- Were multimodal inputs treated as untrusted?
- Were prompts, completions and tool telemetry redacted?
- Was deletion tested across source, vector, cache and memory stores?
- Was the emergency stop and credential revocation tested?
- Was evidence sanitized and teardown verified?

## 34. References

1. OWASP GenAI LLM Top 10 2026: https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
2. OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
3. OWASP Agent Control Standard: https://genai.owasp.org/resource/agent-control-standard-acs/
4. OWASP GenAI Red Teaming Manual v1.0: https://genai.owasp.org/resource/genai-red-teaming-manual-version-1-0/
5. OWASP GenAI Security Project: https://genai.owasp.org/
6. NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
7. NIST AI 600-1: https://doi.org/10.6028/NIST.AI.600-1
8. MITRE ATLAS: https://atlas.mitre.org/
9. MCP specification: https://modelcontextprotocol.io/specification/
10. MCP security best practices: https://modelcontextprotocol.io/specification/draft/basic/security_best_practices
11. OWASP API Security: https://owasp.org/API-Security/
12. NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final
13. ISO/IEC 42001: https://www.iso.org/standard/81230.html
14. OWASP AI Exchange: https://owaspai.org/
15. OWASP Machine Learning Security Top 10: https://owasp.org/www-project-machine-learning-security-top-10/

## 35. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-19 | Initial AI and LLM application security lab specifications |
