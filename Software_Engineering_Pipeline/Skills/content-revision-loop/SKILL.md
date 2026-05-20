---
name: content-revision-loop
description: A mandatory policy and skill that implements the GEPA proposal for a feedback-driven content revision cycle.
license: MIT
skill-author: AROS_code_generator
version: 1.0
---

# Policy: Mandatory Content Revision Loop

## 1. Core GEPA Principle

This policy enforces a critical GEPA proposal: **All feedback resulting from a validation failure MUST be explicitly addressed and corrected before any subsequent validation attempt or processing can occur.** This prevents agents from repeatedly attempting validation with minor, superficial changes and ensures that the root cause of quality issues is resolved.

This skill provides the reference implementation and programmatic enforcement of this policy.

## 2. The Revision States

The content revision process is governed by a strict state machine. Bypassing these states or their entry/exit criteria is a critical policy violation.

*   **`DRAFTING`**: The initial state where content is first created.
*   **`PENDING_VALIDATION`**: The state where content is submitted for a quality check. This is the only state from which validation can be triggered.
*   **`REVISING`**: A mandatory state entered immediately upon validation failure.
    *   **Entry Criterion**: Validation returns a "failed" status with a list of specific, actionable issues.
    *   **Mandatory Action**: The agent MUST process the list of issues. For each issue, the agent must generate a specific correction in the content.
    *   **Exit Criterion**: The agent can only transition out of this state after it has programmatically confirmed that every identified issue has been addressed. The system must be able to trace each correction back to a specific feedback item.
*   **`COMMITTED`**: The final state, entered only after content successfully passes validation. The content is now considered finalized and can be saved or used by other processes.
*   **`ESCALATED`**: A terminal state reached if the content fails to pass validation after a predefined number of revision cycles (default: 3). The content and its revision history are flagged for review by a more capable persona or a human operator.

## 3. Workflow and Enforcement

The logic is implemented in the `scripts/main.py` script.

1.  **Initiation**: The process starts with content in the `DRAFTING` state.
2.  **Submission**: The content moves to `PENDING_VALIDATION`.
3.  **Validation**: An external validator (e.g., `gtb-validator`) is called.
4.  **On Success**: The state transitions to `COMMITTED`. The workflow ends.
5.  **On Failure**:
    *   The state immediately transitions to `REVISING`.
    *   The feedback items from the validator are logged and tracked.
    *   The script enters a mandatory revision phase where the agent MUST generate patches for the content that directly correspond to the feedback.
    *   The script **blocks** any attempt to re-validate until it verifies that all feedback items have been addressed.
    *   Once all issues are addressed, the state transitions back to `PENDING_VALIDATION` for another attempt.
6.  **Loop Termination**: If the number of revisions exceeds the configured limit, the state transitions to `ESCALATED`, and the process halts.

## 4. How to Use

To enforce this policy, agents should invoke the `main.py` script, which manages the state machine for a given piece of content.

### Example Command:
```bash
python ~/.gemini/skills/content-revision-loop/scripts/main.py \
    --content "Initial draft content..."
```
