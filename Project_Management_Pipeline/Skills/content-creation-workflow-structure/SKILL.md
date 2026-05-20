---
name: content-creation-workflow-structure
description: A mandatory policy defining the three-stage workflow (Draft, Validate, Refine) for all content creation tasks within AROS to ensure quality and robustness.
license: MIT
skill-author: AROS-System-Architect
version: 1.1
---

# Policy: Content Creation Workflow Structure

**Version:** 1.1
**ID:** AROS-POLICY-CCWS-V1.1

---

## 1. Preamble

This document establishes the mandatory workflow structure for all content creation and modification tasks within the Antigravity Research OS (AROS). It ensures that all system artifacts (Skills, KIs, Policies, Workflows) undergo a rigorous quality control process before being committed to the filesystem.

## 2. Core Principle

All content authoring and modification MUST follow a distinct three-stage process: **Drafting, Validation, and Refinement.** This is a non-negotiable, zero-tolerance policy to prevent the introduction of flawed, incomplete, or regressive logic into the AROS ecosystem.

## 3. GEPA Error Prevention Rule: Actionable Feedback & Anti-Loop Enforcement

To prevent infinite loops during the Draft-Validate-Refine cycle, a strict feedback requirement is enforced on both the evaluator and the author.

*   **Rule Rationale:** Early GEPA cycles exhibited logical loops where automated validators (like `gtb-validator`) or peer-review tasks returned `{"passed": false}` with empty or non-actionable reasoning. Without clear direction, the authoring agent would repeatedly submit the same draft, creating a locked loop.

*   **For Evaluators (Producing Feedback):** Any task or agent designed to provide critical review, validation, or feedback MUST generate specific, actionable feedback if the artifact fails. Vague critiques or empty reasoning fields are strictly prohibited.
*   **For Authors (Receiving Feedback):** Before initiating a Refinement loop, the agent MUST evaluate the validator's output.
    *   **Anti-Loop Check:** If the validation fails but the feedback is empty, missing, or lacks clear directives on *what* to fix, the agent MUST NOT blindly retry the drafting step.
    *   **Fallback Action:** The agent must treat non-actionable feedback as a tooling failure. It must apply the `robust-self-correction` policy: independently critique its own draft to generate the missing actionable feedback, or escalate the failure (maximum 3 attempts) rather than looping indefinitely.

## 4. The Three-Stage Workflow

The following workflow is mandatory for all agents and automated processes that create or modify AROS artifacts.

### 4.1. Stage 1: Drafting

The initial version of the content is created based on the given task, source data, and relevant context. The primary goal of this stage is to produce a complete, functional draft that is ready for evaluation.

*   **Action:** Generate the required Markdown, code, or other content.
*   **Output:** A candidate artifact saved to a temporary location (e.g., `/tmp/draft_<artifact_name>.md`). The permanent AROS directories MUST NOT be written to at this stage.

### 4.2. Stage 2: Validation

The draft artifact is subjected to a rigorous, automated quality gate to ensure it meets AROS standards for correctness, completeness, and safety.

*   **Action:** Execute the appropriate validation tool. For all standard AROS artifacts, this is the Golden Test Battery (GTB), accessed via the `gtb_validator` tool.
    ```python
    # Example for a new skill (must be invoked as a tool call, not a shell script)
    gtb_validator(draft_file_path="/tmp/draft_new_skill.md", task_type="skill_creation")
    ```
*   **Evaluation:** The outcome is assessed based on the validator's output. A successful validation is explicitly marked (e.g., `{"passed": true}`).

### 4.3. Stage 3: Refinement

The outcome of the validation stage dictates the next action. This stage creates a mandatory feedback loop for quality improvement.

*   **On Success:** If the validation is passed, the artifact is considered complete and correct.
    *   **Action:** The content is written from its temporary location to its final destination in the AROS filesystem. The workflow is complete.

*   **On Failure:** If the validation fails, the artifact MUST NOT be saved to its final destination.
    *   **Action:** The agent MUST parse the feedback or reasoning provided by the validator, subject to the **Anti-Loop Check** defined in Section 3.
    *   **Loop:** Using this actionable feedback, the agent MUST return to the **Drafting Stage (4.1)** to create a revised version of the artifact. This revised draft is then subjected to the **Validation Stage (4.2)** again.
    *   **Termination:** This loop continues until validation is successful, capped by the `robust-self-correction` policy limits (max 3 retries) to prevent indefinite cycles.

## 5. Relation to Other Policies

This policy is a meta-skill that provides the structural foundation for other quality control skills like `content-drafting-capability`