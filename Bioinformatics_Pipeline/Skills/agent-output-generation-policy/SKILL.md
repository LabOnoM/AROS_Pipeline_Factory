---
name: agent-output-generation-policy
description: "A mandatory policy to ensure that AROS agents always produce a final, conclusive output for every assigned task, preventing silent failures or incomplete executions."
license: MIT
skill-author: AROS-Core
---

# Agent Output Generation Policy

This skill establishes a zero-tolerance policy for incomplete agent executions. It mandates that every assigned task must conclude with a definitive, final output, whether it represents success or a well-documented failure.

## Core Principle

An agent's job is not complete until it has delivered a final output. Halting, crashing, or exiting without a conclusive result is a critical policy violation. The agent must always have the "last word" by providing a final status or artifact.

## MANDATORY SKILL INSTRUCTIONS:

### GEPA Rule: Mandatory Task Finalization

**For every assigned task, the agent MUST complete its execution and generate a final, conclusive output.**

This rule is designed to prevent two primary failure modes:
1.  **Silent Failure:** The agent encounters an error and halts execution without reporting a final status.
2.  **Incomplete Work:** The agent reports that it is about to perform the final step but never actually generates the final output.

**Execution Flow:**
- If the task is completed successfully, the final output MUST be the direct result of that task (e.g., the generated code, the requested file, the answer to the query).
- If the task cannot be completed due to an error, the final output MUST be a structured error report that complies with the `agent-communication` policy, explaining the reason for failure.

The agent is explicitly forbidden from ending its turn in a state where the task is partially complete or its status is ambiguous.

### GEPA Rule: Accurate Status Summarization

**The agent's high-level summary statement regarding project completion status MUST accurately reflect the detailed breakdown of completed and remaining tasks within the report.**

This is a critical quality-of-life rule to prevent misleading, overly-optimistic, or "mission accomplished" summaries that hide underlying failures. The summary must be a truthful representation of the detailed outcome.

**Examples of Compliant Behavior:**

*   **Mixed Outcome:** "Project complete with exceptions. 2 of 3 tasks succeeded. The 'database migration' task failed with a timeout error. See details below."
*   **Full Success:** "Project complete. All 3 tasks (schema creation, data insertion, and verification) were successful."

**Examples of Non-Compliant Behavior:**

*   **Hiding Failures:** The agent's final report details that a sub-task failed, but the top-level summary is "The project has been successfully completed."
*   **Ignoring Remaining Work:** The agent reports "The setup is complete" when only 2 of 4 necessary setup steps have actually been executed.

### GEPA Rule: Output File Transparency

**Ensure transparency by providing a comprehensive list of all generated output files.**

When a task results in the creation of multiple files, the agent's final output must include a clear and complete list of all the files that were generated. This ensures that the user can easily locate and identify all the artifacts produced by the agent.

**Examples of Compliant Behavior:**

*   **Success with multiple files:** The agent is asked to generate a report and a corresponding data file. The final output is:
    "I have successfully generated the report. The following files were created:
    - `/path/to/report.pdf`
    - `/path/to/data.csv`"

*   **Success with a single file:** The agent is asked to write a file, and its final output is the confirmation that the file has been written, along with the file path.

**Examples of Non-Compliant Behavior:**

*   **Incomplete file list:** The agent generates two files but only reports the path of one of them.
*   **Ambiguous output:** The agent reports "Task complete" without specifying the path or names of the generated files.
