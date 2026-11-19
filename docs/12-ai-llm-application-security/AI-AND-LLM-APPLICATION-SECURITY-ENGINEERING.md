# AI and LLM Application Security Engineering

| Field | Value |
|---|---|
| Document ID | UAPPSEC-12-001 |
| Status | Draft engineering baseline |
| Version | 0.1 |
| Owner | Unfiltered AppSec maintainers |
| Created | 2026-11-19 |
| Last reviewed | 2026-11-19 |
| Review due | 2027-02-19 |
| Scope | LLM applications, RAG, vector search, agents, tool calling, model integrations, AI supply chain, evaluation and operations |
| Classification | Public |

## 1. Executive summary

AI-enabled applications introduce new trust boundaries, but they do not replace conventional application security requirements. A production AI feature may combine a browser or mobile client, API gateway, application backend, model provider, prompt templates, retrieval pipeline, vector database, document parsers, embeddings, tools, agent runtime, memory store, external APIs, observability platform and human approval workflow. Each component can hold sensitive data or authority. The model's probabilistic output is not a security control and must not be treated as an authorization decision.

The central security challenge is the interaction between untrusted content and privileged capabilities. A model may receive instructions from system configuration, developer prompts, user messages, retrieved documents, web pages, tool outputs, memory, conversation history and multimodal inputs. These sources can conflict. Prompt injection can influence model behavior, but the security impact becomes serious when an application allows that behavior to read protected data, call tools, modify records, execute code, send messages or cross tenant boundaries.

A secure design therefore:
- Treats user input, retrieved content, tool output, documents, web pages, OCR, audio transcripts and model output as untrusted data.
- Keeps authorization and policy enforcement outside the model.
- Gives each tool a narrow, explicit capability and validates every invocation server-side.
- Separates user identity, agent identity, tool identity and delegated authority.
- Enforces tenant and document access before retrieval and again before sensitive actions.
- Uses constrained output schemas and safe downstream handling.
- Limits model, retrieval, tool and agent resource consumption.
- Protects model, prompt, dataset, embedding, connector and deployment supply chains.
- Logs decisions and actions without exposing prompts, credentials or personal data unnecessarily.
- Tests the complete workflow, not only the model response.

**Core rule:** a model may recommend an action, but a trusted application component must authenticate the actor, authorize the exact action against current policy and state, validate arguments, enforce limits and record the outcome.

## 2. Purpose, audience and applicability

### 2.1 Purpose

Provide an engineering playbook to design, build, assess, test and operate secure AI-enabled applications. It covers traditional application security controls around model integrations and AI-specific threats such as prompt injection, unsafe retrieval, excessive agency, model/data poisoning, insecure tool use and output handling.

### 2.2 Audience

Application security engineers, AI/ML engineers, software architects, backend developers, platform and cloud engineers, data engineers, IAM teams, DevSecOps, red teams, SOC, privacy, product owners, risk teams and auditors.

### 2.3 Systems in scope

- LLM-backed chat, summarization, classification, extraction and content-generation features.
- Hosted model APIs and self-hosted/open-weight model serving.
- Retrieval-augmented generation (RAG), embeddings and vector databases.
- Agentic workflows, planners, memory and multi-agent systems.
- Tool/function calling and external connectors.
- Model Context Protocol (MCP) clients and servers.
- Document ingestion, OCR, parsing, chunking and indexing.
- Fine-tuning, adapters, model artifacts, datasets and evaluation pipelines.
- Multimodal inputs including image, audio and video where enabled.
- AI observability, tracing, prompt logging and evaluation systems.
- Human-in-the-loop review and high-impact automated decisions.

### 2.4 Out of scope and specialist dependencies

This chapter is not a model safety policy, model card, legal opinion, full ML engineering standard or guarantee that a model will behave deterministically. It does not prescribe one provider, framework, vector database or agent SDK. Provider-specific controls must be checked against the deployed model, API version, service tier and contract.

This chapter complements Chapters 02 Architecture and Threat Modeling, 03 Secure SDLC, 06 API and Service Security, 07 Identity and Access Security, 08 Data Security and Privacy, 10 Cloud-Native Security, 11 Distributed Systems and Integration Security, 13 Software Supply Chain Security, 14 Security Verification and Assessment and 16 AppSec Operations and Incident Response.

## 3. Terminology

| Term | Meaning |
|---|---|
| AI system | System that uses AI models to produce predictions, content, recommendations or actions |
| LLM | Large language model trained to process and generate language or related tokens |
| Foundation model | Broadly trained model adaptable to multiple downstream tasks |
| Prompt | Input context and instructions supplied to a model |
| System prompt | Application-controlled instructions intended to define model behavior |
| Prompt injection | Untrusted content attempts to alter model behavior or override intended instructions |
| Direct prompt injection | Injection supplied directly by a user |
| Indirect prompt injection | Injection embedded in content the model processes, such as retrieved documents or web pages |
| RAG | Retrieval-augmented generation; retrieves external information and supplies it to a model |
| Embedding | Numeric representation of content used for similarity search or related model tasks |
| Vector database | Store/index supporting vector similarity retrieval and associated metadata |
| Chunk | Segment of a document indexed or retrieved independently |
| Grounding | Supplying trusted contextual evidence to constrain or support a model response |
| Tool/function calling | Model proposes a structured invocation of an application-defined capability |
| Agent | Software workflow in which a model can plan, select tools or perform multi-step tasks |
| Agent runtime | Application component that manages model turns, tool execution, state and limits |
| Excessive agency | An AI component is granted more autonomy or authority than its task requires |
| Memory | Stored context or state reused across model interactions |
| MCP | Model Context Protocol for connecting AI applications to external context and tools |
| Model artifact | Model weights, tokenizer, configuration and related deployment files |
| Model poisoning | Manipulation of training, fine-tuning or adaptation data/artifacts to alter behavior |
| Data poisoning | Malicious or corrupted data introduced into training, retrieval or evaluation datasets |
| Model extraction | Attempt to reproduce or infer model behavior/parameters through queries or access |
| System prompt leakage | Disclosure of internal prompt content or configuration |
| Unbounded consumption | Excessive model, token, tool, retrieval or compute use leading to cost or availability impact |
| Human-in-the-loop | Human review or approval included in an AI-assisted workflow |
| Guardrail | Policy or mechanism intended to constrain model inputs, outputs or actions; not a substitute for authorization |

## 4. AI application reference architecture

### 4.1 Logical architecture

~~~mermaid
flowchart TB
    USER["User / Client"]
    EDGE["Gateway / Authentication / Rate Limit"]
    APP["Application Backend / Policy Enforcement"]
    ORCH["LLM Orchestrator / Agent Runtime"]
    MODEL["Model API / Self-hosted Inference"]
    INGEST["Document Ingestion / Parser / OCR"]
    EMBED["Embedding Service"]
    VDB["Vector Store + Metadata"]
    DOC["Source Documents / Object Storage"]
    TOOLS["Tool Gateway / MCP Client"]
    API["Business APIs / Connectors"]
    MEM["Conversation / Agent Memory"]
    HUMAN["Human Approval"]
    OBS["Logs / Traces / Evaluation"]
    USER --> EDGE --> APP --> ORCH
    ORCH <--> MODEL
    DOC --> INGEST --> EMBED --> VDB
    ORCH --> VDB
    ORCH <--> MEM
    ORCH --> TOOLS --> API
    TOOLS --> HUMAN
    APP --> OBS
    ORCH --> OBS
    TOOLS --> OBS
~~~

The diagram is conceptual. A production architecture must show actual model/provider boundaries, identity issuers, tenant context, retrieval authorization, document provenance, tool permissions, human approval, data residency, retention, logging destinations and external processors.

### 4.2 Trust boundaries

Identify at least:
1. User/client to AI application.
2. Application backend to model provider.
3. Application to prompt/template/configuration store.
4. Document source to ingestion/parser pipeline.
5. Parser/OCR output to chunking and embedding.
6. Embedding service to vector database.
7. Retrieval results to model context.
8. Model output to application parser.
9. Agent runtime to tool gateway.
10. Tool gateway to each business API or connector.
11. Agent memory to future conversations.
12. MCP client to MCP server and server-provided tools/resources.
13. Fine-tuning/evaluation data to model training pipeline.
14. Model registry to inference deployment.
15. AI telemetry to logging/evaluation provider.
16. Human approver to high-impact action.
17. Tenant A to Tenant B data and model context.
18. Production to development, testing and evaluation environments.

For each boundary, document the actor, identity, data classification, protocol, authorization point, provenance, integrity, resource limits, logging, retention and owner.

## 5. Threat model

### 5.1 Adversary profiles

- Malicious authenticated user crafting prompts or uploaded documents.
- Unauthenticated attacker targeting exposed AI endpoints.
- Malicious tenant attempting cross-tenant retrieval or tool access.
- Attacker controlling a web page, document, email or external source retrieved by RAG.
- Compromised connector, MCP server, plugin or tool provider.
- Malicious or compromised data supplier or fine-tuning dataset.
- Insider modifying prompts, model artifacts, access policies or evaluation data.
- Attacker abusing model endpoint, token budget or expensive tools for denial of service.
- Attacker attempting model extraction, system prompt disclosure or sensitive data inference.
- Compromised agent/tool credential used for lateral movement.

### 5.2 High-value assets

- System/developer prompts, policy configuration and safety rules.
- User conversations, uploaded files and retrieved enterprise documents.
- Personal data, credentials, API keys, secrets and regulated records.
- Model weights, adapters, tokenizer, training/fine-tuning datasets and evaluation corpus.
- Embeddings, vector indexes, metadata filters and document ACLs.
- Tool credentials, delegated tokens, connector permissions and MCP server configuration.
- Agent memory, task state, plans and action history.
- Business APIs, databases, files, email, ticketing and payment-like capabilities.
- Model provider account, quotas, keys, endpoint and deployment settings.
- Logs, traces, prompts, completions, tool arguments and evaluation records.

### 5.3 Attack-path catalogue

| Attack path | Preconditions | Potential impact | Primary controls |
|---|---|---|---|
| Direct prompt injection | User controls prompt | Policy manipulation, data disclosure, unsafe response | Treat input as untrusted, constrain capabilities, output validation |
| Indirect prompt injection | Model consumes attacker-controlled content | Tool misuse, exfiltration, workflow manipulation | Content provenance, retrieval isolation, tool authorization, human approval |
| System prompt disclosure | Prompt content included in model context | Internal logic/configuration disclosure | Do not store secrets in prompts; minimize prompt content; access control |
| Sensitive information disclosure | Model context contains protected data | PII, credentials or confidential data leakage | Data minimization, authorization before context assembly, redaction |
| RAG cross-tenant leakage | Weak metadata/ACL filtering | Unauthorized document retrieval | Server-side tenant filters, document ACL enforcement, negative tests |
| Vector poisoning | Attacker can alter indexed corpus | Retrieval manipulation and misinformation | Source validation, ingestion approval, provenance, quarantine |
| Unsafe document parsing | Complex or malicious files processed | Parser compromise, SSRF, resource exhaustion | Sandboxing, patching, file limits, no network by default |
| Tool/function abuse | Model can invoke privileged tool | Unauthorized action or data exfiltration | Tool gateway, least privilege, server-side authorization |
| Excessive agency | Broad autonomy and persistent credentials | Multi-step destructive actions | Narrow scopes, step limits, approvals, action allowlists |
| Output injection | Model output used as HTML/SQL/shell/code | XSS, SQLi, command injection | Contextual encoding, parameterization, no eval, strict schemas |
| MCP server compromise | Client trusts server/tool descriptions | Tool substitution, data theft, unauthorized action | Server trust, scoped permissions, consent, audit, version pinning |
| Agent memory poisoning | Persistent memory accepts untrusted content | Future workflow manipulation | Provenance, write authorization, expiry, user review |
| Model supply-chain compromise | Untrusted weights or dependencies | Backdoor, data theft, inference compromise | Provenance, signatures, scanning, isolated loading |
| Training/fine-tuning poisoning | Untrusted data or adapters | Targeted behavior change | Dataset lineage, review, deduplication, evaluation |
| Model extraction | Broad query access | IP/model capability leakage | Access control, rate limits, anomaly detection, contract controls |
| Denial of wallet | Unbounded token/tool usage | Unexpected spend and service degradation | Budgets, quotas, deadlines, circuit breakers |
| Multimodal injection | Image/audio/video carries instructions | Hidden instructions or sensitive extraction | OCR/transcript treated as untrusted, provenance and tool controls |
| Evaluation gaming | Benchmark or test data contaminated | False assurance | Holdout sets, independent red team, dataset controls |
| Telemetry leakage | Prompts and tool data logged broadly | Secret/PII disclosure | Redaction, access control, retention and processor review |
| Model denial of service | High concurrency/large context/expensive inference | Availability impact | Rate limits, queueing, context limits and graceful degradation |

### 5.4 Threat-modeling workflow

1. Define AI use case, intended users and prohibited outcomes.
2. Draw data-flow and trust-boundary diagrams.
3. Inventory models, providers, prompts, tools, connectors, MCP servers and datasets.
4. Identify sensitive data entering context, memory, retrieval and telemetry.
5. Identify every model-controlled or model-suggested action.
6. Separate model reasoning from trusted authorization and execution.
7. Analyze direct and indirect prompt injection paths.
8. Analyze tenant, document and object authorization.
9. Analyze supply-chain, poisoning and evaluation integrity.
10. Analyze cost, availability, abuse and fallback behavior.
11. Define negative tests and evidence.
12. Record residual risk, human oversight and release criteria.

## 6. Secure AI system design principles

### 6.1 Models are not policy enforcement points

A model can classify, summarize, reason and propose. It cannot reliably enforce authorization simply because a prompt says not to reveal data or call a tool. Authorization must be implemented by deterministic application components using trusted identity and policy inputs.

### 6.2 Separate planning from execution

The model may produce a proposed action. The application must:
1. Parse the proposal against a strict schema.
2. Resolve the actual authenticated actor and tenant from trusted context.
3. Verify the requested operation is in the allowed tool catalogue.
4. Validate every argument and resource identifier.
5. Evaluate current authorization and business state.
6. Apply quotas, rate limits and step budgets.
7. Require human approval for defined high-impact actions.
8. Execute using a narrowly scoped service identity.
9. Record the request, decision and outcome.
10. Return only the minimum result to the model.

### 6.3 Least privilege by default

- Separate read, write, delete, export, administrative and external communication tools.
- Avoid generic shell, SQL, browser, filesystem or HTTP tools where narrow domain tools are possible.
- Use short-lived credentials and per-tool service identities.
- Limit data scope, row count, file path, recipient, domain and operation.
- Do not give the model raw credentials or unrestricted network access.
- Disable tools not needed for a workflow.
- Re-authorize each action; do not rely on an earlier model turn.

### 6.4 Fail safely

When policy, identity, retrieval ACL, tool schema, human approval or model provider is unavailable, sensitive operations should fail closed. Read-only fallback may be allowed only if explicitly designed and does not expose protected data.

## 7. Prompt injection and instruction hierarchy

### 7.1 Direct prompt injection

Direct prompt injection is untrusted user content that attempts to change model behavior, override instructions, reveal protected context or cause an unintended action.

Testing should include:
- Attempts to override system/developer instructions.
- Requests to reveal hidden prompts or configuration.
- Role-play and instruction hierarchy manipulation.
- Encoded, obfuscated, multilingual and split-payload instructions.
- Requests to use tools outside the intended task.
- Requests to reveal prior user or tenant context.
- Attempts to cause unsafe output formats or hidden markup.
- Attempts to manipulate refusal or safety behavior.

A prompt-only defense is insufficient. The application must prevent unauthorized data and capabilities from entering the model context or becoming executable actions.

### 7.2 Indirect prompt injection

Indirect prompt injection can be embedded in:
- PDF, DOCX, spreadsheets, presentations and text files.
- HTML, comments, metadata, alt text and hidden page content.
- Emails, support tickets, chat messages and code repositories.
- Web pages and search results.
- OCR text from images and screenshots.
- Speech transcripts and video captions.
- Tool outputs and external API responses.
- Retrieved chunks, memory records and shared documents.

Treat all such content as data, not trusted instruction. Delimiters and prompt labels can help model interpretation but are not a security boundary.

### 7.3 Context construction requirements

- Keep system/developer policy separate from retrieved content.
- Label content by source and trust level.
- Include only the minimum relevant retrieved text.
- Preserve document and tenant provenance.
- Avoid including secrets or unrelated conversation history.
- Do not let retrieved text modify tool permissions or authorization policy.
- Limit context size and number of retrieved documents.
- Apply content scanning and quarantine where appropriate.
- Validate that citations refer to retrieved source IDs actually provided to the model.
- Treat generated summaries of untrusted content as untrusted too.

### 7.4 System prompt protection

System prompts should not contain passwords, API keys, private keys, bearer tokens or other secrets. Prompt secrecy is not a security boundary. If prompt content is disclosed, the impact should be limited because access controls and secrets are enforced outside the prompt.

Store prompts in version control or controlled configuration, review changes, restrict production write access, identify the model/version and prompt version used for a decision, and test prompt changes with security evaluations.

## 8. RAG, document ingestion and vector database security

### 8.1 RAG data flow

1. Source document is submitted or synchronized.
2. File type, size and provenance are checked.
3. Parser/OCR extracts content in an isolated environment.
4. Content is classified and scanned.
5. Chunking preserves document and access-control metadata.
6. Embeddings are generated using an approved model.
7. Chunks and metadata are stored in a tenant-aware index.
8. At query time, user and tenant identity are resolved.
9. Retrieval applies authorization filters before results are returned.
10. Retrieved content is checked and assembled into model context.
11. The response is generated and citations are validated.
12. Access and retrieval events are audited.

### 8.2 Document ingestion controls

- Allowlist file types based on actual parser support.
- Validate MIME type and file signature; do not trust extension alone.
- Limit file size, page count, archive expansion, image dimensions and processing time.
- Scan for malware where appropriate.
- Run parsers and OCR in isolated, least-privileged workers.
- Disable outbound network access by default.
- Prevent parser access to cloud metadata, internal services and local secrets.
- Protect against archive bombs, malformed files and parser exploits.
- Preserve original source, uploader, tenant, classification, hash and ingestion time.
- Quarantine suspicious or untrusted sources.
- Define re-indexing and deletion propagation.

### 8.3 Chunk and embedding security

- Preserve source document ID, tenant ID, ACL reference, classification and version on every chunk.
- Do not rely on vector similarity to enforce access.
- Treat embeddings as potentially sensitive derived data.
- Restrict index, namespace, collection and metadata administration.
- Protect embedding APIs and model endpoints.
- Validate chunk provenance and prevent metadata substitution.
- Review cross-tenant nearest-neighbor behavior.
- Revoke or re-index chunks when source access is removed.
- Protect backups and replicas.
- Define retention and deletion for vectors, caches and derived indexes.

### 8.4 Retrieval authorization

Authorization must occur before content is supplied to the model. A secure query flow should:
1. Authenticate the user.
2. Resolve tenant and user identity from trusted server-side context.
3. Obtain allowed document scopes from the authoritative policy source.
4. Apply mandatory tenant and ACL filters in the retrieval layer.
5. Re-check access to returned document IDs where needed.
6. Exclude unauthorized chunks before prompt construction.
7. Validate citation IDs and source references.
8. Record document IDs and policy outcome without logging full content unnecessarily.

Do not rely on the model to ignore unauthorized documents after they have already been retrieved.

### 8.5 Vector database risks

Assess weak namespace isolation, missing metadata filters, filter injection, cross-tenant similarity leakage, index enumeration, unauthorized export, insecure backups, stale ACL metadata, poisoned vectors, embedding inversion/privacy exposure, excessive query volume and administrative API exposure.

## 9. Tool calling, agents and excessive agency

### 9.1 Tool execution architecture

The model should not directly possess broad infrastructure credentials. A trusted tool gateway should validate proposed calls and execute a specific capability using its own constrained identity.

### 9.2 Tool registry

For each tool define:
- Stable tool ID, owner and version.
- Business purpose and permitted users/workflows.
- Input and output schema.
- Data classification and sensitivity.
- Required actor, tenant and delegated scope.
- Read/write/delete/export/administrative capability.
- Allowed resources, domains, paths, recipients and operations.
- Rate, concurrency, size and timeout limits.
- Human approval requirements.
- Credential owner and rotation policy.
- Audit fields, failure behavior and emergency disablement.

### 9.3 Tool-call validation

- Treat model-generated tool name and arguments as untrusted.
- Match tool names against an explicit allowlist.
- Reject unknown fields and unexpected types.
- Enforce numeric, string, array and object bounds.
- Validate identifiers against current tenant and resource ownership.
- Prevent mass assignment and arbitrary URL/path selection.
- Use parameterized queries and safe API clients.
- Re-authorize at execution time.
- Bind idempotency keys to actor, action and resource.
- Apply per-tool budgets and deadlines.
- Return minimal, sanitized results.

### 9.4 Agent autonomy levels

| Level | Capability | Example | Required control |
|---|---|---|---|
| 0 | Answer only | Explain a policy | No external action |
| 1 | Read-only retrieval | Search approved knowledge base | Retrieval ACL and source validation |
| 2 | Draft action | Draft an email or ticket | User review before submission |
| 3 | Bounded execution | Create a low-risk ticket in assigned project | Scoped tool identity, schema and audit |
| 4 | High-impact execution | Change access, deploy, delete, approve payment | Strong approval, separation of duties, step-up controls |
| 5 | Broad autonomous operation | Multi-system planning and execution | Avoid by default; formal safety case and strict containment if justified |

Do not grant a higher autonomy level merely because the model appears reliable in demonstrations.

### 9.5 Human approval

Human approval must be meaningful:
- Show the exact action, target, data and consequences.
- Show the authenticated approver and approval time.
- Bind approval to a canonical action digest so arguments cannot change afterward.
- Expire approvals and prevent reuse.
- Require a separate approver for defined high-impact actions.
- Prevent the agent from approving its own action.
- Provide cancel and emergency stop.
- Re-check authorization and state after approval and before execution.

A generic "approve" button that does not display the actual action is not meaningful approval.

### 9.6 Multi-agent systems

- Assign each agent a distinct identity and narrow capability.
- Treat inter-agent messages as untrusted inputs.
- Validate sender identity, schema, task ID and tenant context.
- Prevent agents from passing broad credentials to each other.
- Define delegation depth and maximum agent hops.
- Bound recursive planning and total steps.
- Record parent/child agent lineage and tool actions.
- Prevent one agent from elevating another agent's permissions.
- Apply independent authorization at the final execution boundary.

## 10. MCP and connector security

MCP introduces a protocol boundary between AI clients and servers that expose tools, resources or prompts. Security depends on transport, authorization, server trust, user consent, tool implementation and deployment configuration.

Requirements:
- Use official protocol documentation for the exact deployed version.
- Authenticate and authorize remote connections.
- Validate issuer, audience, token scope and resource binding where OAuth is used.
- Do not pass a client token through to an unrelated downstream service.
- Treat tool descriptions, resource content and server responses as untrusted.
- Require explicit user consent for sensitive data access and actions.
- Maintain an approved server registry and owner.
- Pin and review server versions and dependencies.
- Restrict filesystem, network and process access of local MCP servers.
- Validate tool input/output schemas.
- Apply tool-level authorization, rate limits and audit.
- Protect server credentials and configuration.
- Revoke access when a server is removed or compromised.
- Test malicious tool descriptions, unexpected output and server substitution.

MCP connectivity does not itself make a tool safe. A connected server can still expose excessive permissions, vulnerable code or malicious behavior.

## 11. Model and AI supply-chain security

### 11.1 Model artifact governance

- Use approved model registries and providers.
- Record model name, version, source, license, hash and acquisition date.
- Verify artifact provenance and signatures where available.
- Scan model packages and loading dependencies.
- Avoid unsafe deserialization of untrusted model files.
- Isolate model loading and inference workers.
- Restrict access to model weights and adapters.
- Track quantization, conversion and fine-tuning changes.
- Record known limitations, evaluation results and intended use.
- Maintain rollback to a known-good model.

### 11.2 Dataset and fine-tuning security

- Record source, license, owner, collection method and purpose.
- Validate consent and permitted use.
- Scan for malicious, malformed and sensitive content.
- Detect duplicates, contamination and anomalous samples.
- Separate training, validation and test sets.
- Protect labels and annotation workflows.
- Restrict dataset write and export.
- Version datasets and preserve lineage.
- Review adapters and fine-tuning checkpoints.
- Evaluate for memorization, leakage, backdoors and targeted behavior changes.
- Define correction and removal workflows.

### 11.3 Model provider assessment

Review provider data retention and training use, regional processing, subprocessors, encryption and key management, endpoint isolation, identity and access controls, abuse monitoring, model/version changes, incident notification, availability, data deletion, export, contractual protections and exit plan. Verify actual product settings and contract; do not assume all providers have the same defaults.

## 12. Model output and downstream application security

Model output is untrusted input. It may contain incorrect, malicious, malformed or adversarially influenced content.

- Escape output for its destination context.
- Sanitize HTML/Markdown before rendering.
- Never execute generated code or shell commands without an isolated and explicitly authorized execution design.
- Use parameterized database operations.
- Validate JSON against strict schemas and reject unknown fields where appropriate.
- Do not use model output as SQL, shell, filesystem path, URL, access policy or authorization claim.
- Validate generated links and destinations.
- Prevent stored/reflected XSS in AI-generated content.
- Apply content security policy and safe rendering.
- Validate citations and references against actual retrieved source IDs.
- Separate factual claims from generated text and apply human review for high-impact use.
- Avoid treating confidence language as a calibrated probability unless validated.

## 13. Data protection and privacy

### 13.1 Data lifecycle

Map data at collection, upload, parsing, prompt construction, inference, retrieval, tool execution, memory, logging, evaluation, training/fine-tuning, backup, export and deletion.

### 13.2 Controls

- Minimize personal and confidential data sent to models.
- Use approved data classifications and handling rules.
- Mask or tokenize identifiers where feasible.
- Prevent secrets from entering prompts, memory and telemetry.
- Encrypt data in transit and at rest.
- Restrict conversation and document access.
- Define retention and deletion for prompts, completions, embeddings, caches and backups.
- Ensure tenant isolation in conversation history and memory.
- Review provider training/retention settings and contracts.
- Assess cross-border transfer and subprocessor processing.
- Provide appropriate transparency and user controls.
- Test data deletion across source, index, vector, cache and backup layers.

### 13.4 GenAI data security architecture patterns

Use the OWASP GenAI Data Security Best Practices v2 material as a companion for detailed data classification, governance and lifecycle implementation. Part 2, published 17 November 2026, describes reusable patterns including governed ingress, metadata propagation, retrieval boundaries, full-chain erasure, AI-BOM lineage and federated policy enforcement.

Engineering implications:
- Classify data before it enters a prompt, embedding, model context, tool or telemetry pipeline.
- Propagate tenant, owner, classification, source and retention metadata through parsing, chunking, embedding, retrieval, memory and export.
- Enforce retrieval boundaries before content enters model context.
- Maintain lineage from source document to chunks, embeddings, indexes and derived artifacts.
- Implement deletion across source, chunk, vector, cache, memory, evaluation and eligible downstream stores.
- Record model, prompt, dataset, embedding and connector dependencies in an AI bill of materials or equivalent inventory.
- Enforce policy consistently across services and providers rather than relying on per-prompt conventions.

Reference: https://genai.owasp.org/resource/genai-data-security-best-practices-v2-part2/

### 13.3 Memory security

Memory is a persistence layer and must be treated like a database:
- Define what can be stored and for what purpose.
- Separate user-owned memory from system instructions.
- Validate provenance and source trust.
- Restrict who can write, read and delete memory.
- Prevent one user's memory from entering another user's context.
- Expire stale memory and support correction/deletion.
- Avoid storing secrets and unnecessary sensitive data.
- Audit memory changes and access.
- Test memory poisoning and cross-session contamination.

## 14. Multimodal security

For image, audio, video and other modalities:
- Treat OCR text, subtitles, transcripts, captions and metadata as untrusted input.
- Check file type, size, duration, resolution, codec and decompression limits.
- Isolate media parsers and transcoding tools.
- Prevent remote media fetch from reaching internal networks.
- Preserve provenance and user/tenant access metadata.
- Test visible and hidden instruction content in images and documents.
- Test spoken instructions, background speech and transcript manipulation.
- Validate generated media and downstream metadata.
- Avoid assuming the model can reliably distinguish visible content from embedded instruction.
- Apply the same tool authorization and data controls regardless of modality.

## 15. AI endpoint, API and infrastructure security

- Apply standard API authentication, authorization and object-level checks.
- Separate model-provider keys from user credentials.
- Use secret manager and rotation; never embed keys in client code.
- Rate-limit by user, tenant, model, tool and endpoint.
- Limit prompt length, context window, output tokens, image/audio size and concurrency.
- Set request deadlines and cancellation.
- Protect inference endpoints and admin APIs.
- Restrict model server network egress.
- Isolate GPU/model workers and management planes.
- Patch runtime, model server, drivers, CUDA libraries and dependencies.
- Protect caches and shared inference state from cross-tenant leakage.
- Use quotas and cost alerts.
- Apply WAF/API protections where suitable, without assuming they understand semantic prompt attacks.
- Secure deployment manifests, model registry, container images and orchestration.

## 16. Evaluation, red teaming and continuous assurance

### 16.1 Evaluation dimensions

Evaluate security and quality separately:
- Prompt injection resistance.
- Sensitive data leakage.
- Retrieval authorization and grounding.
- Tool selection and argument validation.
- Unauthorized action refusal.
- Cross-tenant isolation.
- Output schema validity.
- Unsafe rendering and downstream injection.
- Model and data poisoning resilience.
- Robustness to multilingual, encoded and multimodal inputs.
- Resource consumption and availability.
- Human approval and workflow integrity.
- Privacy, retention and deletion behavior.

### 16.2 Test set governance

- Use representative and adversarial examples.
- Separate development, validation and held-out red-team sets.
- Prevent training/evaluation contamination.
- Version prompts, models, tools, datasets and policy.
- Measure false acceptance and false rejection.
- Record model stochasticity and repeat test runs where needed.
- Review test coverage with application owners.
- Do not claim security from a single benchmark score.
- Re-run evaluations after model, prompt, retrieval, tool or policy changes.

### 16.3 Release gates

A release should not proceed if:
- Unauthorized tool execution is possible.
- Cross-tenant retrieval or memory leakage is confirmed.
- Critical secrets or protected data can be exposed.
- Output can reach dangerous execution sinks without controls.
- Tool credentials are broader than approved.
- High-impact actions lack required approval.
- Unbounded consumption can materially affect service availability or cost.
- Model/data provenance is unknown for a high-risk deployment.
- Logging exposes secrets or sensitive data outside approved controls.
- Incident response and kill-switch procedures are absent for high-impact agents.

## 17. Security verification methodology

### 17.1 Assessment phases

1. Confirm authorization, system boundary and AI use case.
2. Inventory model, provider, prompts, tools, agents, datasets and connectors.
3. Map data flows and trust boundaries.
4. Review identity, tenant and authorization architecture.
5. Review prompt construction and injection handling.
6. Review RAG ingestion, retrieval and vector isolation.
7. Review tool calling, MCP and agent autonomy.
8. Review output handling and downstream sinks.
9. Review model/data supply chain.
10. Review privacy, memory, telemetry and retention.
11. Test API, infrastructure, rate and cost controls.
12. Test monitoring, incident response and emergency stop.
13. Record findings, remediation, residual risk and retest.

### 17.2 Rules of engagement

- Obtain written authorization from application, AI platform, data and tool owners.
- Use synthetic data and dedicated test tenants.
- Do not submit real secrets or personal records to public model endpoints.
- Do not invoke real destructive tools, external email, payment, production deployment or account deletion.
- Use mock tool servers and local sinks for exfiltration tests.
- Do not perform uncontrolled token floods or expensive inference tests.
- Do not poison production corpora or model artifacts.
- Do not test third-party model/provider systems outside contractual authorization.
- Define request, token, concurrency and cost ceilings.
- Preserve sanitized evidence and redact prompts or payloads containing sensitive data.
- Confirm tool revocation, test data cleanup and index cleanup after testing.

### 17.3 Red-team execution lifecycle

The OWASP GenAI Red Teaming Manual Version 1.0 describes an eight-phase methodology: planning, reconnaissance, attack surface mapping, exploitation, persistence, impact assessment, reporting and remediation. Use this as an assessment lifecycle overlay, not as a substitute for the detailed test cases in this chapter.

For each phase, record scope and authorization, test identity, target model/application/tool version, reproducible steps, observed behavior, security impact, evidence, containment and retest. Persistence testing must remain within explicitly authorized disposable environments. Do not establish persistence in production or third-party systems.

Reference: https://genai.owasp.org/resource/genai-red-teaming-manual-version-1-0/

### 17.4 AI and LLM security test catalogue

The IDs below are internal project identifiers, not external standard control IDs.

| Test ID | Domain | Test focus | Expected result |
|---|---|---|---|
| AI-T-001 | Architecture | Inventory models, prompts, tools, data stores and trust boundaries | Complete owner-backed AI component inventory |
| AI-T-002 | Direct injection | Attempt instruction override and policy bypass | No unauthorized data or capability is exposed |
| AI-T-003 | Indirect injection | Embed instructions in retrieved document | Content is treated as untrusted data |
| AI-T-004 | Prompt leakage | Request system/developer prompt and hidden configuration | No secrets or protected configuration disclosed |
| AI-T-005 | Secret handling | Search prompts/context/logs for synthetic secret markers | Secrets are not unnecessarily included or exposed |
| AI-T-006 | Context isolation | Attempt to access another user's conversation history | Access denied by backend authorization |
| AI-T-007 | RAG tenant isolation | Query for another tenant's known synthetic document | Unauthorized chunks never enter model context |
| AI-T-008 | Document ACL | Revoke source access and repeat retrieval | Revoked content is not returned from stale index/cache |
| AI-T-009 | Retrieval poisoning | Add a malicious synthetic document with false instructions | Provenance/approval and policy prevent unsafe action |
| AI-T-010 | Parser security | Submit malformed, oversized and archive-bomb-like files in isolated lab | Parser is bounded and isolated |
| AI-T-011 | SSRF in ingestion | Submit document/URL referencing local mock internal endpoints | Ingestion worker cannot access prohibited destinations |
| AI-T-012 | Vector isolation | Attempt namespace/metadata filter manipulation | Server-enforced tenant and ACL filters remain effective |
| AI-T-013 | Embedding privacy | Test whether restricted content can be inferred from exposed vector interfaces | Vector access is restricted and leakage risk assessed |
| AI-T-014 | Tool allowlist | Ask model to invoke unknown or disabled tool | Tool gateway rejects invocation |
| AI-T-015 | Tool argument validation | Supply unexpected fields, types, paths or resource IDs | Strict schema and authorization reject unsafe arguments |
| AI-T-016 | Tool authorization | Invoke valid tool against unauthorized object | Server-side authorization denies operation |
| AI-T-017 | Excessive agency | Request a multi-step destructive workflow | Autonomy, step budget and approval controls constrain action |
| AI-T-018 | Approval integrity | Modify tool arguments after human approval | Approval binding fails; action is not executed |
| AI-T-019 | Agent identity | Attempt cross-agent credential or context reuse | Distinct agent identities and scopes are enforced |
| AI-T-020 | Memory poisoning | Store malicious instruction in persistent memory | Memory provenance/write policy prevents future privilege change |
| AI-T-021 | Cross-session isolation | Attempt to retrieve another user's memory | Backend denies access |
| AI-T-022 | MCP trust | Connect unapproved or substituted MCP server in lab | Server registry/trust policy rejects or requires explicit approval |
| AI-T-023 | MCP tool abuse | Return malicious tool description/output | Tool response is treated as untrusted; policy remains external |
| AI-T-024 | Output XSS | Render generated HTML/Markdown with script payload in lab | Safe rendering prevents script execution |
| AI-T-025 | Output SQL/command | Feed generated string into downstream execution sink | Parameterization/allowlist prevents execution |
| AI-T-026 | Structured output | Return invalid schema, extra properties and boundary values | Strict schema validation rejects output |
| AI-T-027 | Citation integrity | Ask for citations not present in retrieval context | Application validates source IDs and rejects fabricated references |
| AI-T-028 | Model supply chain | Load untrusted model package in isolated lab | Provenance/scanning/isolation controls prevent unsafe deployment |
| AI-T-029 | Dataset poisoning | Add synthetic targeted examples to training/evaluation pipeline | Dataset review and evaluation detect or quarantine changes |
| AI-T-030 | Model extraction | Perform bounded query probing against test endpoint | Access/rate controls detect and constrain extraction behavior |
| AI-T-031 | API authorization | Access AI session, file or job belonging to another user | Object-level authorization denies access |
| AI-T-032 | Rate limiting | Exceed per-user and per-tenant request/token quotas | Requests are throttled and recorded |
| AI-T-033 | Cost control | Trigger bounded high-token and tool-heavy workflow | Budgets, deadlines and step limits stop runaway use |
| AI-T-034 | Multimodal injection | Embed synthetic instructions in image/audio input | Content remains untrusted and cannot bypass tool authorization |
| AI-T-035 | Telemetry privacy | Inspect prompt, completion, tool and trace logs | Sensitive values are redacted or excluded |
| AI-T-036 | Retention/deletion | Delete synthetic source and inspect indexes, vectors, caches and logs | Defined deletion workflow covers all applicable stores |
| AI-T-037 | Provider configuration | Review training/retention/region settings and keys | Actual settings match approved data handling |
| AI-T-038 | Human oversight | Trigger high-impact action without required approver | Action is blocked pending valid approval |
| AI-T-039 | Emergency stop | Disable agent/tool credentials during active workflow | New actions stop and state is safely recorded |
| AI-T-040 | Incident detection | Simulate injection, unauthorized tool call and quota abuse | Actionable alerts reach the assigned owner |
| AI-T-041 | Inter-agent communication | Send forged, replayed or schema-invalid message from a synthetic peer agent | Sender identity, message integrity, task scope and replay controls reject the message |
| AI-T-042 | Cascading failure | Simulate one dependent tool/agent becoming unavailable in a bounded lab workflow | Deadlines, retry budgets, circuit breakers and workflow isolation prevent cascade |
| AI-T-043 | Human-agent trust | Present a synthetic deceptive agent summary or altered action preview to an approver | Approver sees canonical action details and independently verifiable evidence |
| AI-T-044 | Rogue agent | Simulate unauthorized agent registration, configuration drift or tool activation | Inventory, runtime policy and kill switch detect and contain the agent |
| AI-T-045 | Data lineage and erasure | Trace a synthetic record through source, chunks, embeddings, caches and derived stores, then request deletion | Provenance is complete and deletion propagates to every applicable store within defined retention limits |
| AI-T-046 | Runtime control hooks | Attempt tool invocation when policy middleware is unavailable, bypassed or returns deny | Execution path fails closed and records the policy decision and enforcement outcome |

## 18. Detection engineering catalogue

| Detection ID | Scenario | Signals | Initial response |
|---|---|---|---|
| AI-D-001 | Prompt injection pattern | Repeated instruction override attempts or suspicious retrieved content | Review source and workflow; do not rely on text classifier alone |
| AI-D-002 | Sensitive data disclosure | Secret/PII detector in output, trace or model response | Restrict access, contain exposure and assess affected data |
| AI-D-003 | Cross-tenant retrieval | Retrieval result tenant differs from authenticated tenant | Block response, preserve evidence and investigate ACL/index path |
| AI-D-004 | Unusual tool invocation | Tool outside user's normal workflow or newly enabled tool | Suspend tool execution pending authorization review |
| AI-D-005 | Tool argument anomaly | Unexpected URL, path, recipient, resource or large argument | Reject call and inspect prompt/tool source |
| AI-D-006 | Excessive agent activity | Step count, tool calls or recursion exceeds baseline | Stop workflow and apply budget controls |
| AI-D-007 | High-impact action attempt | Delete, export, permission change or external send proposed | Require approval and verify actor/action digest |
| AI-D-008 | MCP server change | New server, version, tool list or permission scope | Verify owner and provenance; disable unapproved server |
| AI-D-009 | Memory poisoning | Unusual memory writes, instruction-like content or cross-user access | Quarantine memory item and review writer identity |
| AI-D-010 | Vector index change | Bulk ingestion, ACL metadata changes or unexpected source | Pause ingestion and validate provenance |
| AI-D-011 | Model artifact change | New model hash, adapter or serving configuration | Verify approval, provenance and evaluation status |
| AI-D-012 | Dataset anomaly | Unexpected source, label distribution or high-volume update | Quarantine dataset release and investigate |
| AI-D-013 | Model extraction pattern | High-volume systematic queries or unusual response probing | Rate-limit and review account behavior |
| AI-D-014 | Denial of wallet | Token usage, concurrency or tool cost spikes | Enforce quota, stop runaway jobs and alert owner |
| AI-D-015 | Parser abuse | Repeated parse failures, oversized files or outbound attempts | Quarantine input and isolate parser worker |
| AI-D-016 | Output injection | Generated content reaches unsafe HTML/SQL/shell sink | Block sink and investigate integration |
| AI-D-017 | Telemetry leakage | Prompt/tool fields contain credential or PII markers | Stop export, restrict logs and execute deletion/incident process |
| AI-D-018 | Provider key misuse | API key used from unexpected service, region or volume | Revoke/rotate key and inspect provider audit |
| AI-D-019 | Approval bypass | Tool action occurs without valid approval record | Stop workflow and investigate orchestration |
| AI-D-020 | Emergency stop failure | Tool continues after revocation or kill switch | Isolate agent runtime and revoke downstream credentials |
| AI-D-021 | Inter-agent trust anomaly | Unknown agent identity, invalid signature, unexpected delegation hop or replayed task ID | Reject message, suspend delegation and investigate peer identity |
| AI-D-022 | Agent cascade | Retry/agent-call fan-out, queue age, tool failure and workflow recursion rise together | Apply workflow circuit breaker and isolate failing dependency |
| AI-D-023 | Approval deception | Difference between agent summary, canonical action digest and executed arguments | Block execution and require fresh independent approval |
| AI-D-024 | Rogue agent behavior | Unregistered agent, altered tool manifest, unexpected capability or policy bypass | Quarantine agent and revoke runtime credentials |
| AI-D-025 | AI data lineage mismatch | Missing source metadata, tenant/classification drift or incomplete deletion acknowledgment | Pause affected ingestion/retrieval and reconcile derived data stores |
| AI-D-026 | Runtime policy hook failure | Agent/tool execution proceeds without a valid policy decision or middleware health | Stop action path, fail closed and alert platform owner |

A detection is not operational until telemetry source, query, thresholds, false-positive handling, owner, severity, runbook and test evidence are defined.

## 19. Incident response and recovery

### 19.1 Response principles

- Preserve model/provider, API, tool, MCP, vector, identity and orchestration evidence.
- Identify the affected model, prompt, version, tool, user, tenant and workflow.
- Determine what data entered context and what the model or agent returned.
- Determine which tools were invoked and whether external side effects occurred.
- Revoke compromised tool credentials and connector tokens.
- Disable affected tools, agents, MCP servers or ingestion sources.
- Quarantine malicious documents, memory entries, datasets or model artifacts.
- Revoke access to affected indexes and rebuild from trusted sources if needed.
- Assess prompt, completion, trace and provider retention exposure.
- Reconcile external actions with authoritative systems.
- Notify privacy, legal, customer, provider and regulator owners as required.
- Resume only after authorization, data isolation and monitoring are validated.

### 19.2 Scenario playbooks

**Indirect prompt injection causing tool misuse**
1. Stop the affected agent workflow and disable the implicated tool if needed.
2. Preserve prompt, retrieved source IDs, tool proposal, validated arguments and execution logs.
3. Identify the source document/page/email and ingestion lineage.
4. Determine whether data was read, exported or modified.
5. Revoke exposed credentials and invalidate active sessions where appropriate.
6. Quarantine the source and related chunks/memory.
7. Reconcile business actions and notify owners.
8. Add regression tests for the exact attack path and verify server-side authorization.

**Cross-tenant RAG disclosure**
1. Disable affected retrieval endpoint or isolate the index/namespace.
2. Preserve query, authenticated tenant, retrieval filter, returned document IDs and policy version.
3. Determine affected users, tenants, documents and response/log destinations.
4. Revoke cached/index access and repair ACL metadata.
5. Rebuild affected index from authoritative sources if required.
6. Assess provider and telemetry retention.
7. Follow applicable privacy/contract notification process.
8. Test negative access across tenants, roles and revoked documents.

**Compromised MCP server or tool**
1. Disable server registration and block its network path.
2. Revoke server and downstream credentials.
3. Identify tool list, server version, users, agent workflows and data accessed.
4. Inspect tool descriptions, schema and server package provenance.
5. Review all tool invocations and external side effects.
6. Quarantine server artifact and preserve evidence.
7. Reconcile actions and rotate dependent credentials.
8. Reintroduce only after code, permissions and trust are reviewed.

**Model or dataset poisoning**
1. Freeze affected model/dataset release and deployment pipeline.
2. Identify model hash, adapter, dataset version and lineage.
3. Compare with known-good artifact and source data.
4. Preserve training, evaluation, registry and deployment logs.
5. Roll back to known-good model where appropriate.
6. Re-run held-out security and quality evaluations.
7. Review supplier and pipeline permissions.
8. Require approval before retraining or redeployment.

**Denial of wallet or inference abuse**
1. Apply tenant/account quota and stop runaway workflows.
2. Disable expensive tools and bound concurrency.
3. Preserve request, token, model and billing telemetry.
4. Identify source identity, endpoint and abuse pattern.
5. Rotate exposed API keys if compromise is suspected.
6. Review quota bypass and shared-account behavior.
7. Restore service with revised budgets and alerts.
8. Reconcile costs and update abuse controls.

## 20. Standards and framework mapping

Mappings are relevance guidance, not compliance assertions. Use the exact edition and map requirements to the deployed system boundary and evidence.

### 20.1 OWASP GenAI LLM Top 10 2026

The OWASP GenAI Security Project published the **OWASP GenAI LLM Top 10 2026** on 3 August 2026. It is the current edition as of this chapter's review date. It updates the risk taxonomy and mappings using community research and real-world incident analysis. The complete 2026 taxonomy and mitigation wording must be taken from the official 2026 resource before claiming numbered control alignment. This chapter currently provides a broad engineering baseline across the risk domains; its internal test IDs are not OWASP control IDs.

- Current 2026 resource: https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
- Official initiative page: https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/

The 2025 list below is retained only as a historical cross-reference because many tools, reports and existing programs still use its identifiers. Do not present it as the latest edition.

| OWASP 2025 legacy category | Security concern | Chapter coverage |
|---|---|---|
| LLM01 Prompt Injection | Direct and indirect instruction manipulation | Sections 7, 8, 9, 17 |
| LLM02 Sensitive Information Disclosure | Confidential data exposure through context/output | Sections 8, 13, 17 |
| LLM03 Supply Chain | Models, datasets, dependencies and providers | Section 11 |
| LLM04 Data and Model Poisoning | Malicious training, fine-tuning or retrieval data | Sections 8, 11 |
| LLM05 Improper Output Handling | Unsafe downstream processing | Section 12 |
| LLM06 Excessive Agency | Over-privileged or autonomous tools | Section 9 |
| LLM07 System Prompt Leakage | Disclosure of internal instructions | Section 7 |
| LLM08 Vector and Embedding Weaknesses | Retrieval and embedding weaknesses | Section 8 |
| LLM09 Misinformation | Incorrect or fabricated output and unsafe reliance | Sections 12, 16 |
| LLM10 Unbounded Consumption | Cost, compute and availability abuse | Sections 15, 16 |

### 20.2 OWASP Top 10 for Agentic Applications 2026

The OWASP Agentic Security Initiative published the 2026 Agentic Applications Top 10 in December 2025. Its categories are particularly relevant when a model can plan, delegate, invoke tools, retain memory or act across systems.

| ID | Agentic risk | Chapter coverage |
|---|---|---|
| ASI01 | Agent Goal Hijack | Sections 7, 9, 17 |
| ASI02 | Tool Misuse and Exploitation | Sections 9, 10, 17 |
| ASI03 | Identity and Privilege Abuse | Sections 6, 9, 10 |
| ASI04 | Agentic Supply Chain Vulnerabilities | Sections 10, 11 |
| ASI05 | Unexpected Code Execution (RCE) | Sections 12, 15, 17 |
| ASI06 | Memory and Context Poisoning | Sections 7, 8, 13 |
| ASI07 | Insecure Inter-Agent Communication | Sections 9, 10 |
| ASI08 | Cascading Failures | Sections 9, 15, 18 |
| ASI09 | Human-Agent Trust Exploitation | Sections 9, 16 |
| ASI10 | Rogue Agents | Sections 9, 16, 19 |

The agentic taxonomy emphasizes least agency, tool-level least privilege, action-level authentication and approval, execution isolation, egress control, policy enforcement middleware, adaptive tool budgets, ephemeral access, semantic tool validation and observable agent behavior. Use the original document for detailed definitions, attack scenarios and mitigations: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/

### 20.3 OWASP Agent Control Standard (ACS)

The OWASP Agent Control Standard provides a runtime-oriented approach to making agents inspectable, traceable and instrumentable, with middleware hooks through which policies can be enforced across agent frameworks. It is relevant to the tool gateway, approval, agent identity, telemetry and emergency-stop controls in Sections 9, 10, 18 and 19.

Reference: https://genai.owasp.org/resource/agent-control-standard-acs/

Treat ACS as a control implementation resource; verify its current version, implementation maturity and compatibility with the deployed agent framework before adopting it.


### 20.4 NIST AI Risk Management Framework

NIST AI RMF 1.0 organizes AI risk management around Govern, Map, Measure and Manage. Apply the functions across:
- Govern: ownership, accountability, policies, third-party and lifecycle oversight.
- Map: context, intended use, affected parties, data flows and risk identification.
- Measure: evaluation, testing, monitoring and documented limitations.
- Manage: prioritization, response, mitigation, residual risk and ongoing monitoring.

### 20.5 NIST Generative AI Profile

NIST AI 600-1, Generative Artificial Intelligence Profile, is a companion resource to the AI RMF. Use it to structure generative AI risk identification, measurement and management. It is not a technical control checklist or a certification.

### 20.6 MITRE ATLAS

MITRE ATLAS provides a knowledge base of adversary tactics and techniques targeting AI-enabled systems. Use it to expand threat scenarios, red-team hypotheses and detection coverage. Map each technique to the actual architecture and do not treat technique presence as proof of exploitability.

### 20.7 MCP official security guidance

Use the official MCP specification and security best-practice documentation for the exact protocol version. Review authorization, token audience/resource binding, confused deputy risks, local server trust, consent and tool security. MCP protocol conformance is not equivalent to application authorization.

### 20.8 OWASP API Security Top 10

AI endpoints remain APIs. Relevant categories include broken object-level authorization, broken authentication, broken object property-level authorization, unrestricted resource consumption, broken function-level authorization, SSRF, security misconfiguration, improper inventory management and unsafe consumption of APIs.

### 20.9 ISO/IEC 42001 and ISO/IEC 27001

ISO/IEC 42001 provides an AI management system framework. ISO/IEC 27001 provides an information security management system framework. Neither should be reduced to a list of AI attack tests. Establish scope, context, roles, risk treatment, operational controls, evaluation and continual improvement. Map AI-specific technical controls into the organization's broader ISMS and AIMS where applicable.

### 20.10 Secure development and privacy

Use NIST SSDF SP 800-218 for secure development practices; use applicable privacy laws and organizational policies for lawful purpose, minimization, transparency, retention, data-subject rights and cross-border processing. The relevant law depends on entity, data subject, processing, jurisdiction and sector.

## 21. Regulatory and jurisdiction considerations

Applicability depends on the legal entity, sector, data subjects, purpose, deployment, model role, provider, transfer and contractual obligations. AI features may create new processors, sub-processors, data flows and automated decision risks.

### 21.1 India

Assess the Digital Personal Data Protection Act, 2023 and DPDP Rules, 2025, including commencement provisions, current amendments and applicability. Review notices, purpose, consent or other applicable lawful basis, processor arrangements, safeguards, retention/deletion, breach response and cross-border processing. Sector rules may also apply. Obtain qualified legal review for the actual deployment.

### 21.2 Qatar

Assess Qatar Personal Data Privacy Protection Law No. 13 of 2016 and applicable sector, government, contractual and national assurance requirements. Review model provider locations, subprocessors, prompt and telemetry retention, access by support personnel and cross-border transfers.

### 21.3 Saudi Arabia

Assess Saudi PDPL and implementing/transfer regulations, NCA controls where the entity and service are in scope, and sector-specific requirements. Review AI provider processing, data residency, access, retention, transfer and incident obligations.

### 21.4 UAE

Determine whether federal UAE personal data law, DIFC, ADGM, healthcare, financial, government or sector-specific regimes apply. Review data flows to model providers, analytics and observability services.

### 21.5 EU/EEA and UK

Assess GDPR/UK GDPR, EU AI Act and sector requirements where applicable. Determine provider/deployer roles, risk classification, transparency, human oversight, data governance, technical documentation, logging, accuracy/robustness/cybersecurity and applicable implementation dates. Do not assume every AI feature is high-risk or prohibited; classify the actual intended purpose and use.

### 21.6 Cross-border AI data-flow checklist

For each model, embedding, OCR, vector, telemetry and connector provider record legal entity, controller/processor role, purpose, data categories, region, subprocessors, retention/training use, support access, transfer mechanism, encryption/key ownership, deletion and backup behavior, incident contact, contractual restrictions and exit plan.

## 22. Industry use cases

### 22.1 Banking and financial services

Risks include sensitive financial data in prompts, unauthorized account retrieval, fabricated financial advice, agent execution of transfers, prompt injection from uploaded statements and third-party provider retention.

Controls:
- Strong customer and account authorization before context construction.
- Read-only tools by default.
- Human approval and separation of duties for high-impact actions.
- Explicit disclosure and review of generated recommendations.
- Strict transaction limits and idempotency.
- Provider and telemetry data governance.
- Independent audit and reconciliation.

### 22.2 Healthcare

Risks include wrong-patient context, sensitive record leakage, hallucinated clinical output, unreviewed recommendations and broad access to clinical tools.

Controls:
- Patient identity and record authorization at retrieval.
- Minimum necessary context.
- Clinical human oversight for decisions.
- Source-grounded output and clear limitations.
- Audit of access and action.
- Privacy and retention controls across provider, vector and telemetry layers.

### 22.3 Enterprise knowledge assistant

Risks include cross-department document leakage, stale ACLs, malicious documents, prompt injection in shared files and disclosure through conversation memory.

Controls:
- ACL-aware retrieval.
- Source provenance and document versioning.
- Revalidation after permission changes.
- Tenant/user memory isolation.
- Safe citation validation.
- Controlled ingestion and deletion.

### 22.4 Software engineering agent

Risks include malicious repository instructions, secret disclosure, unsafe code execution, dependency poisoning and unauthorized commits or deployments.

Controls:
- Read-only repository access by default.
- Isolated ephemeral execution environment.
- No unrestricted network or host filesystem.
- Secret scanning and output review.
- Protected branch and CI approval.
- Separate code suggestion from merge/deploy authority.
- Dependency and artifact provenance.

### 22.5 Customer support agent

Risks include account takeover through social engineering, unauthorized refunds, disclosure of another customer's records and prompt injection in tickets or attachments.

Controls:
- Verify customer identity outside the model.
- Enforce object-level authorization in tools.
- Use bounded refund/credit capabilities.
- Human approval for defined thresholds.
- Treat ticket and attachment text as untrusted.
- Record tool action and customer-visible outcome.

### 22.6 OT and industrial integration

Risks include an AI assistant interpreting malicious maintenance instructions, exposing plant documentation or triggering unsafe control actions through connected tools.

Controls:
- Default to read-only advisory use.
- No direct model-to-PLC/SCADA control path.
- Place integrations behind an industrial DMZ and approved gateway.
- Require authorized operator approval and safety interlocks.
- Enforce asset-specific allowlists and change windows.
- Validate commands independently of model output.
- Test with digital twins or isolated simulators, not live processes.

## 23. Metrics and control effectiveness

| Metric | Definition | Use |
|---|---|---|
| AI component inventory coverage | Production AI components with owner, purpose and risk record / total known components | Governance |
| Prompt version traceability | Decisions linked to approved prompt/model version / sampled decisions | Change control |
| Retrieval authorization coverage | Retrieval paths enforcing server-side ACL/tenant policy / total retrieval paths | Data isolation |
| Cross-tenant test pass rate | Passed negative tenant tests / total planned tests | Tenant security |
| Tool authorization coverage | Tool actions with server-side authorization / total tool actions | Agent safety |
| High-impact approval coverage | High-impact actions with valid bound approval / total high-impact actions | Human oversight |
| Tool scope compliance | Tools whose scopes match approved matrix / total active tools | Least privilege |
| Sensitive data leakage rate | Confirmed unauthorized disclosures / tested interactions | Privacy/security |
| Injection regression pass rate | Passed injection test cases / total active cases | Robustness |
| Output schema validation rate | Validated structured outputs / outputs used by application | Output safety |
| Model artifact provenance coverage | Production models with recorded source/hash/approval / total models | Supply chain |
| Dataset lineage coverage | Production datasets with source and version lineage / total datasets | Data governance |
| Budget enforcement coverage | Workflows with token/tool/cost budgets / total agent workflows | Abuse resistance |
| Telemetry redaction coverage | AI services with approved prompt/tool telemetry policy / total services | Privacy |
| Deletion completion rate | Deletion requests propagated to applicable source/index/vector/cache stores / total requests | Lifecycle |

Metrics require scope, data source, owner, frequency, target and exceptions. A high refusal rate or benchmark score alone does not establish security.

## 24. Maturity model

| Level | Characteristics |
|---|---|
| 1 — Ad hoc | Prompts and tools are developed without inventory, formal authorization or AI threat modeling |
| 2 — Repeatable | AI component inventory, basic API controls, provider review, prompt testing and manual tool review exist |
| 3 — Defined | Retrieval ACLs, tool gateway, least privilege, output validation, data lifecycle and versioned evaluations are implemented |
| 4 — Measured | Continuous red-team tests, policy telemetry, cost budgets, provenance and incident exercises are measured |
| 5 — Adaptive | Automated policy enforcement, continuous supply-chain assurance, risk-based approvals and monitored containment operate with governed human override |

Tool adoption or a model provider's security statement does not establish maturity.

## 25. Implementation roadmap

### 0–30 days: inventory and containment
- Inventory all AI features, models, prompts, tools, agents, MCP servers and data stores.
- Identify sensitive data entering prompts, memory, retrieval and logs.
- Disable broad tools and unnecessary autonomous actions.
- Identify cross-tenant retrieval and object authorization gaps.
- Establish token, cost, context and concurrency limits.
- Assign owners and document provider data handling.

### 30–90 days: enforce trust boundaries
- Implement server-side retrieval authorization.
- Deploy tool gateway with strict schemas and least privilege.
- Separate user, agent and tool identities.
- Add human approval for high-impact actions.
- Secure ingestion, vector indexes, memory and telemetry.
- Add output validation and safe rendering.
- Version prompts, models, datasets and evaluations.

### 90–180 days: operationalize assurance
- Implement continuous injection and tool abuse regression tests.
- Establish model/dataset provenance and artifact review.
- Add detection for cross-tenant access, tool anomalies and cost abuse.
- Test emergency stop, credential revocation and recovery.
- Review provider, privacy and cross-border obligations.
- Run independent AI red-team and incident exercises.
- Map controls to exact framework requirements and evidence.

## 26. Evidence and professional deliverables

An AI application security assessment pack should include:
- Scope, authorization and rules of engagement.
- AI system and provider inventory.
- Architecture, trust-boundary and data-flow diagrams.
- Model, prompt, dataset and artifact register.
- Tool, connector and MCP server register.
- Agent autonomy and capability matrix.
- Identity, tenant and authorization matrix.
- RAG source, chunk, vector and ACL design.
- Prompt injection and context construction review.
- Tool-call schema and server-side authorization tests.
- Human approval and workflow integrity evidence.
- Output handling and downstream sink review.
- Privacy, retention, deletion and provider assessment.
- Evaluation dataset and red-team coverage.
- Detection and incident response playbooks.
- Findings, remediation, exceptions and retest records.

## 27. Limitations and assumptions

- Prompt engineering alone cannot guarantee resistance to prompt injection.
- Model behavior is probabilistic and can change with model, provider, prompt, sampling and context.
- A refusal or safety classifier is not authorization.
- A RAG citation does not prove the answer is correct or the user was authorized to see the source.
- Embeddings may encode sensitive information and require protection.
- Tool calling is a proposal mechanism; the application remains responsible for execution authorization.
- MCP protocol support does not establish that a server or tool is trustworthy.
- Human approval is ineffective if the approved action can change afterward.
- Model benchmark performance does not prove application security.
- Provider retention, training and regional behavior vary by service, contract and configuration.
- Regulatory applicability depends on intended use, entity, sector, data and jurisdiction.
- This chapter is an engineering baseline, not a legal opinion, model certification or compliance attestation.

## 28. Related chapters

- [02. Application Architecture and Trust Boundaries](../02-architecture-threat-modeling/APP-ARCHITECTURE-AND-TRUST-BOUNDARIES.md)
- [03. Secure SDLC and Product Security](../03-secure-sdlc-product-security/SECURE-SDLC-AND-PRODUCT-SECURITY.md)
- [06. API and Service Security](../06-api-service-security/API-AND-SERVICE-SECURITY-ENGINEERING.md)
- [07. Identity and Access Security](../07-identity-access-security/IDENTITY-AND-ACCESS-SECURITY.md)
- [08. Data Security and Privacy Engineering](../08-data-security-privacy/DATA-SECURITY-AND-PRIVACY-ENGINEERING.md)
- [10. Cloud-Native Application Security](../10-cloud-native-application-security/CLOUD-NATIVE-APPLICATION-SECURITY-ENGINEERING.md)
- [11. Distributed Systems and Integration Security](../11-distributed-systems-integration-security/DISTRIBUTED-SYSTEMS-AND-INTEGRATION-SECURITY-ENGINEERING.md)

## 29. Authoritative references

1. OWASP GenAI LLM Top 10 2026: https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/
2. OWASP Top 10 for Agentic Applications 2026: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
3. OWASP Agent Control Standard (ACS): https://genai.owasp.org/resource/agent-control-standard-acs/
4. OWASP GenAI Red Teaming Manual Version 1.0: https://genai.owasp.org/resource/genai-red-teaming-manual-version-1-0/
5. OWASP Securing Agentic Applications V2: https://genai.owasp.org/initiative_name/agentic-security/
6. OWASP GenAI Security Project: https://genai.owasp.org/
7. OWASP Top 10 for LLM Applications 2025 (historical cross-reference): https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
8. NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
9. NIST AI 600-1, Generative Artificial Intelligence Profile: https://doi.org/10.6028/NIST.AI.600-1
10. MITRE ATLAS: https://atlas.mitre.org/
11. Model Context Protocol specification: https://modelcontextprotocol.io/specification/
12. MCP security best practices: https://modelcontextprotocol.io/specification/draft/basic/security_best_practices
13. OWASP API Security Top 10: https://owasp.org/API-Security/
14. NIST SP 800-218, Secure Software Development Framework: https://csrc.nist.gov/pubs/sp/800/218/final
15. ISO/IEC 42001, Artificial intelligence management systems: https://www.iso.org/standard/81230.html
16. ISO/IEC 27001, Information security management systems: https://www.iso.org/standard/27001
17. OWASP AI Exchange: https://owaspai.org/
18. OWASP Machine Learning Security Top Ten: https://owasp.org/www-project-machine-learning-security-top-10/
14. OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/

## 30. Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-11-19 | Initial AI and LLM application security engineering playbook |
