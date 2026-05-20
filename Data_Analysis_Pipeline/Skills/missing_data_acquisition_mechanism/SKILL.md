---
name: missing_data_acquisition_mechanism
description: A meta-skill defining the protocol for actively acquiring missing data by prompting the user or querying internal systems, and escalating when acquisition is not possible.
license: MIT
skill-author: AROS_code_generator
---

# Missing Data Acquisition Mechanism

This is a meta-skill that defines a mandatory operational protocol for all AROS agents. It ensures that agents are resilient to missing information and actively seek to resolve data gaps, while providing a safe escalation path when resolution is not possible.

## GEPA Rules

### Active Data Acquisition

If input data required for a task is missing or incomplete, the agent **MUST NOT** fail or block silently. Instead, it **MUST** trigger an acquisition workflow to obtain the necessary information. This involves either prompting the user directly or querying an appropriate internal system (e.g., `brain.db`, KIs).

### Halt on Critical Input Failure

Before attempting any task, the agent **MUST** perform a pre-execution validation to ensure all critical inputs are present and valid. If a critical input is missing and cannot be recovered through autonomous means (e.g., querying `brain.db`), the agent **MUST** adhere to the following procedure:
1.  **Halt Progression:** Immediately halt the current task and any dependent downstream tasks.
2.  **Report to User:** Clearly and explicitly report to the user which critical inputs are missing and why they are essential for the task.
3.  **Request Guidance:** Request explicit user confirmation to proceed by providing the missing data.
4.  **Propose Alternatives:** If applicable, propose alternative strategies that can be pursued without the missing data.
5.  **Await Instruction:** Await direct instructions from the user before resuming, abandoning, or modifying the task. Proceeding without user confirmation is a critical policy violation.

## Reference Implementation

The GEPA rule for halting on critical input failure is implemented in the `task_executor.py` script within this skill's directory. This script provides a `TaskExecutor` class that performs the pre-execution validation and raises a `CriticalInputMissingError` to halt the workflow and signal the need for user intervention.

**Audit-Ready Command:**
This command demonstrates the functionality of the policy by running a simulation of a task with missing inputs, which triggers the halt and requests user guidance.
```bash
python ~/.gemini/skills/missing_data_acquisition_mechanism/task_executor.py
```

## Key Capabilities

- **Pre-Execution Validation**: Checks for the presence and validity of all critical inputs before a task begins.
- **Missing Data Detection**: Identifies when a critical piece of information is unavailable or insufficient.
- **Source Identification**: Determines the most likely source for the missing data (user input vs. internal system).
- **User Prompting**: Formulates clear, specific questions to the user to acquire the data.
- **Internal Querying**: Constructs and executes queries against internal AROS knowledge stores.
- **Mandatory Halt and Escalation**: Halts the current task, notifies the user, and awaits instructions when critical data cannot be acquired.
- **Alternative Strategy Formulation**: Suggests alternative paths forward when the primary path is blocked.

## Workflow

1.  **Task Initiation**: An agent begins a task that has specific data requirements (e.g., `api_key`, `user_id`, `filepath`).
2.  **Critical Input Validation**: The agent utilizes the `TaskExecutor` to validate the presence and sufficiency of all data designated as critical.
3.  **Halt or Proceed**:
    *   **If validation fails**, the `TaskExecutor` raises a `CriticalInputMissingError`. The agent's core logic must catch this exception, present the formatted message to the user, and wait for new instructions.
    *   **If validation passes**, the agent proceeds with task execution.
4.  **Data Acquisition (for non-critical data)**: If non-critical data is missing, the agent attempts to acquire it by querying internal systems or prompting the user, without halting the entire workflow unless necessary.
5.  **Task Completion**: The agent resumes and completes the task once all necessary data is available.
