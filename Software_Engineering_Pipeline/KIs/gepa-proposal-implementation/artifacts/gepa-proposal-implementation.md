# Knowledge Item: gepa-proposal-implementation

## 1. Overview
This Knowledge Item (KI) documents the formal operational procedures of **GEPA**, the **Generative Error-Patching Agent**, within the **AROS** ecosystem. It establishes the protocol for creating, structuring, and implementing GEPA Proposals, which leverage **conversation-extracted facts** to advance systemic knowledge and structural blueprints. This KI provides the essential grounding for agents tasked with actioning these proposals.

## 2. Terminology and Scope
*   **GEPA (Generative Error-Patching Agent)**: The core autonomous mechanism in AROS responsible for error recovery and proposing system improvements.
*   **Knowledge Item (KI)**: The standard persistent artifact format in AROS.
*   **Conversation-Extracted Facts**: Evidence-based data points gathered during agent interactions that serve as the justification for proposals.
*   **GEPA Proposal**: A **structured, machine-readable artifact** that formally recommends a specific change (creation, update, or deletion) to a Knowledge Item. Proposals are not abstract requests; they are precise instructions.

## 3. GEPA Proposal Structure and Grounding
To ensure deterministic and reliable execution, all GEPA Proposals **MUST** adhere to a structured format. This structure eliminates ambiguity and transforms proposal implementation from an inference task into a direct, procedural operation.

### 3.1. Formal Proposal Structure
A proposal is a structured data object, typically represented in YAML or JSON. It must contain the following fields:

*   `proposal_id` (string, required): A unique identifier for the proposal (e.g., a UUID).
*   `target_ki` (string, required): The **exact, resolvable name** of the Knowledge Item to be created or modified. Example: `ki-policy-clarity-and-accessibility`.
*   `change_type` (string, required): The type of operation. Must be one of: `CREATE`, `UPDATE`, `APPEND`.
*   `patch_content` (string, required): The specific content to be written, updated, or appended. This is the literal patch.
*   `justification` (string, required): A brief explanation of why the change is needed, often referencing the conversation-extracted facts that triggered the proposal.

### 3.2. Example of a Well-Formed Proposal
This example demonstrates the correct structure for the proposal that failed in trace `636d2d7a-88df-4421-9a62-573aa0a95b35`.

```yaml
proposal_id: "prop-c9e3b1a2-4f0e-4a8b-9d1f-7c2a0b3e5d8f"
target_ki: "ki-policy-clarity-and-accessibility"
change_type: "APPEND"
patch_content: |
  ### 4. Error Prevention Rules
  - **Rule 4.1 (Jargon Reduction):** Use clear, concise language and avoid excessive jargon to ensure accessibility for a broad audience.
justification: "Conversation-extracted facts show that complex jargon in agent outputs is a recurring source of user confusion and task failure. This rule formalizes a preventative measure."
```

## 4. Operational Policies for Implementation
Agents handling GEPA proposals must adhere to the following policies to ensure robust execution.

### 4.1. Policy: Strict Target Resolution
The `target_ki` field is the **sole source of truth** for identifying the artifact to be modified. Agents **MUST NOT** attempt to infer or guess the target from the `justification` field or other natural language descriptions. If the `target_ki` does not resolve to an existing artifact and the `change_type` is not `CREATE`, the task must fail with an "Invalid Target KI" error.

### 4.2. Policy: Atomic and Literal Application
The agent must apply the `patch_content` literally as specified by the `change_type`. No transformations, summaries, or interpretations of the `patch_content` are permitted. The process is a direct mechanical application of the provided patch to the target KI.

### 4.3. Policy: Proposal Lifecycle
1.  **Parsing**: The agent first validates that the incoming proposal conforms to the structure defined in section 3.1.
2.  **Resolution**: The agent resolves the `target_ki` to a specific artifact within the AROS knowledge base.
3.  **Application**: The agent performs the `change_type` operation using the `patch_content`.
4.  **Verification**: The agent confirms that the change was successfully written and the resulting KI remains valid.