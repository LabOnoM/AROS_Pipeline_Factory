---
name: content-drafting-capability
description: A meta-skill governing the creation and modification of AROS system artifacts (Skills, KIs, Policies, Workflows) to ensure they meet quality and safety standards.
license: MIT
skill-author: AROS-Mutation-Sweeper
---

# Content Drafting Capability

This is a mandatory meta-skill that defines the standard operating procedure for authoring and modifying AROS artifacts. It ensures all new content is validated, safe, and adheres to system-wide quality standards before being committed to the filesystem.

## When to Use

- ALWAYS use this capability when creating or editing any AROS Markdown artifact, including:
    - Skills (`~/.gemini/skills/`)
    - Knowledge Items (`~/.gemini/antigravity/knowledge/`)
    - Workflows (`~/.gemini/antigravity/global_workflows/`)
    - Policies

## Core Drafting Workflow

1.  **Synthesize Draft:** Generate the required Markdown content based on the task, source data, and other relevant skills.
2.  **Apply Quality Gate:** Before writing the content to its destination, subject it to the mandatory GEPA Quality Gate for validation.
3.  **Commit or Escalate:** Based on the validation outcome, either write the file to the filesystem or initiate the escalation protocol.

---
## MANDATORY SKILL INSTRUCTIONS

### GEPA Rule: Precise Proposal Execution
- The agent must precisely execute the agreed-upon proposal and achieve its stated objective for the task.

### GEPA Rule: User-Defined Content Completeness Adherence
- The agent must adhere to the user's explicit definition of complete content, ensuring all specified components or criteria are fully present, rather than relying on an internal, potentially flawed, or ambiguous definition.

---

## GEPA Quality Gate: Golden Test Battery (GTB) Validation

This is a **non-negotiable** error prevention rule. All new or modified Markdown artifacts MUST pass GTB validation before being written to the filesystem. This prevents the introduction of flawed, incomplete, or regressive logic into the AROS ecosystem.

---
### GEPA Error Prevention Rule: Mandatory Output Diversity and Structure

To prevent monolithic, unorganized, or incomplete outputs, all agent-generated content, especially code and instructional text, MUST be broken down into logical, well-structured components. This is a non-negotiable rule for clarity, validation, and reuse.

-   **Why:** This rule ensures that outputs are easy to parse, validate, and reuse. It prevents ambiguity and forces a clear separation of concerns. Monolithic blocks of code or text are prone to errors and are difficult to debug or modify.
-   **Implementation Guidelines:**
    -   **Code Generation:** Decompose scripts into smaller, single-responsibility functions. Accompany code with explanatory comments for complex logic and provide clear, runnable usage examples.
    -   **Instructional Content:** Utilize numbered lists, bullet points, and Markdown headers (`##`, `###`) to create a clear, hierarchical structure for plans and procedures.
    -   **Configuration:** Employ structured data formats like JSON, YAML, or INI for clarity and machine-readability.
    -   **File Modifications:** When modifying an existing file, you MUST include a `diff` of the changes in your output. This provides a clear, auditable record of the modification and is essential for review and traceability. A `diff -u` (unified diff) is the preferred format.

---
### GEPA Error Prevention Rule: Maintain Persona Drafting Capability
Ensure agent personas maintain the capability to generate well-structured and relevant initial content drafts based on implicit or explicit task instructions.


---
### GEPA Error Prevention Rule: Mandatory Proxy-Aware LLM Client Instantiation

All new or modified Skills that make LLM API calls (via `genai.Client`, `genai.configure`, 
`dspy.LM`, or any Google AI SDK) **MUST** respect the AROS Cloud Federation proxy
environment variables (`AROS_CLOUD_URL`, `AROS_CLOUD_KEY`) before falling back to 
direct API keys (`GEMINI_API_KEY`, `GOOGLE_AI_API_KEY`).

**Prohibited Pattern:**
```python
# ❌ NEVER do this — bypasses AROS proxy routing
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
```

**Required Pattern:**
```python
# ✅ Always check for AROS proxy first
cloud_url = os.environ.get("AROS_CLOUD_URL", "").rstrip("/")
cloud_key = os.environ.get("AROS_CLOUD_KEY", "")
if cloud_url and cloud_key:
    client = genai.Client(api_key=cloud_key, http_options={"base_url": cloud_url})
else:
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
```

- **Why:** Hardcoded direct API keys bypass token metering, cost attribution, and 
  Vertex AI optimizations provided by the Cloud Federation proxy.
- **Enforcement:** The `gtb-validator` SHOULD flag Skills containing `genai.Client(api_key=` 
  without an adjacent `AROS_CLOUD_URL` check as a quality gate failure.

## Progressive Disclosure (Merged from Pocock)

- Lead with the most common, critical paths.
- Bury edge cases, theory, and configuration options further down the document.
- Use explicit visual hierarchy (headings, bolding) to help agents and humans scan.
