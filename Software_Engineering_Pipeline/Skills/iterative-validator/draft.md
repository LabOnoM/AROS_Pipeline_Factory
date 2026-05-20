---
name: iterative-validator
description: A skill that programmatically enforces the GEPA policy of iterative validation and self-correction for all AROS artifacts, now with a multi-tiered feedback loop.
license: MIT
skill-author: AROS_code_generator
---

# Iterative Validation and Self-Correction

This skill implements the mandatory GEPA quality gate, providing a programmatic workflow to ensure all generated content meets a predefined quality threshold before being committed to the AROS filesystem. It now features a multi-tiered validation strategy involving automated self-correction and an external feedback loop.

## Core Principle

This skill enforces the policy: 'After generating or processing information, the agent must perform iterative validation and apply self-correction mechanisms until a predefined quality threshold is consistently met.' It includes a fail-safe mechanism to prevent infinite loops.

## Workflow

The logic is encapsulated in the `scripts/main.py` script and follows a multi-tiered approach:

### Tier 1: Automated Self-Correction Loop (2 Retries)

1.  **Initialization**: The script is called with the initial draft content, the final destination path, and the `task_type` for the GTB validator.
2.  **Validation**: The `gtb-validator` skill is executed on the draft content.
3.  **Analysis & Action**:
    *   **On Success (`"passed": true`)**: The content is saved to its final destination, and the process completes successfully.
    *   **On Failure (`"passed": false`)**: The script uses the feedback from the `gtb-validator` to automatically regenerate the content.
4.  This automated self-correction loop is attempted a maximum of **two** times.

### Tier 2: External Feedback Trigger

*   If the content still fails validation after two automated attempts, the script escalates to the external validation stage.
*   It invokes a mechanism to request a review from a separate, specialized entity (e.g., a "Peer Review Agent" or another designated validation service via the `_solicit_external_feedback` function).

### Tier 3: Externally-Informed Correction (1 Final Retry)

*   The feedback obtained from the external source is parsed.
*   This new, external feedback is used as the primary input for one final regeneration of the content.
*   The `gtb-validator` is run a final time on this improved draft.

### Fail-Safe / Escalation

*   If the content fails to pass validation after the third and final attempt, the loop terminates.
*   The script invokes an escalation protocol (`_escalate_for_review`), flagging the task for review by a larger, more capable model persona. This prevents infinite loops and ensures that difficult problems are handled by more powerful resources.

## How to Use

To use this skill, an agent should call the `main.py` script with the required arguments.

### Example Command:
```bash
python ~/.gemini/skills/iterative-validator/scripts/main.py \
    --content "# My New Knowledge Item..." \
    --destination "~/.gem
