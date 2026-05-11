---
name: comprehensive-task-completion
description: "A meta-protocol skill that defines the mandatory workflow for robust and verifiable task execution. Its primary objective is to: Successfully execute all required sub-tasks for a given request within any specified constraints. This skill integrates error-prevention rules to ensure all generated artifacts are complete, tested, and reliable before finalization."
license: MIT
skill-author: AROS-Core
---

# Comprehensive Task Completion Meta-Protocol

This skill defines the standard operating procedure for executing any complex request within the AROS ecosystem. It is a meta-protocol designed to ensure that all tasks are completed thoroughly, verifiably, and in accordance with system-wide quality and safety standards.

## Core Objective

The primary goal of this meta-protocol is to: **Successfully execute all required sub-tasks for a given request within any specified constraints.**

## When to Use

This meta-protocol is implicitly active for all agent tasks that involve the creation or modification of system artifacts, code, or knowledge bases. It serves as the guiding framework for task execution.

## Core Execution Workflow

1.  **Deconstruct Request:** Break down the user's goal into a sequence of discrete, actionable sub-tasks. Identify all explicit and implicit constraints, including deadlines, resource limitations, and quality requirements.
2.  **Execute Sub-Tasks:** Address each sub-task systematically using the most appropriate skills, tools, or workflows. Maintain a clear record of actions taken and intermediate results.
3.  **Apply GEPA Quality Gate:** Before finalizing the task and committing any artifacts, subject all outputs to the mandatory GEPA Quality Gate for validation. This is a non-negotiable step to prevent errors and ensure quality.
4.  **Verify and Finalize:** Confirm that all sub-tasks have been completed, the quality gate has passed, and the primary objective has been met. Report the final status accurately, as per the `agent-communication` policy.

---

## GEPA Quality Gate: Error Prevention Rules

This section contains mandatory, non-negotiable rules designed to prevent common errors that can lead to incomplete, untestable, or flawed system artifacts. All generated content must adhere to these rules before a task can be considered complete.

### Rule 1: Overall Goal Success Validation

For any task that generates a tangible artifact (e.g., a script, a KI, a policy, a configuration file), the artifact's success is contingent on passing a rigorous, automated validation check. This rule ensures that the final output robustly and verifiably meets the overall goal.

*   **Rationale:** To prevent silent failures, incomplete outputs, or the commitment of low-quality artifacts into the AROS ecosystem. Success is not the absence of errors during generation; it is the presence of a positive validation signal.
*   **Mandatory Workflow:**
    1.  **Draft Generation:** The agent MUST generate the output artifact and save it to a temporary location.
    2.  **Validation via GTB:** The agent MUST use the `gtb-validator` skill to assess the quality and correctness of the draft artifact. The `task_type` parameter (e.g., `code_generation`, `knowledge_retrieval`, `system_configuration`) MUST be chosen appropriately based on the artifact's content and purpose.
    3.  **Iterative Refinement:** If the `gtb-validator` returns `"passed": false`, the agent MUST analyze the `reasoning` provided, modify the draft to address the identified issues, and re-run the validation. This refinement loop MUST continue until the validation passes. A maximum of **3** attempts are permitted.
    4.  **Escalation on Failure:** If the artifact fails to pass validation after 3 attempts, the agent MUST NOT commit the file. The task MUST be halted, and the failure—along with the final validator feedback—MUST be escalated for review according to the `critical_task_output_guarantee` policy.
    5.  **Success Condition:** The task is only considered complete and the goal achieved when the `gtb-validator` returns `"passed": true`.
