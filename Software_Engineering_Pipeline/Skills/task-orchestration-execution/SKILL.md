---
name: task-orchestration-execution
description: A policy that governs the breakdown and execution of multi-step tasks, including mandatory pre-flight checks for tool availability.
license: MIT
skill-author: AROS-Core
version: 2.0
---

# Policy: Task Orchestration/Execution (v2.0)

## 1. Core Principle

This policy defines the standard procedure for an agent to break down a complex goal into a sequence of executable steps. It ensures that workflows are logical, efficient, and robust against common environment-related failures. It governs the entire lifecycle of a workflow, from initial validation to final execution.

## 2. GEPA Error Prevention Rules

This policy incorporates the following GEPA rules to prevent common workflow failures.

### GEPA-Rule-011: Pre-Workflow Tool Validation

Before initiating the first step of any multi-step workflow, the agent **MUST** verify the availability of all required external shell tools. This check is especially critical for tools required for the workflow's finalization steps, such as publishing, saving, validation, or user notification (e.g., `gtb-validator`). This rule prevents workflows from executing significant work only to fail at the final step due to a missing dependency.

### GEPA-Rule-005: Sequenced Execution Verification

An agent must verify the successful completion of a preceding step before initiating the next step in a sequence. This prevents error cascades where a task continues despite a critical failure in an early step.

## 3. Mandatory Procedure

All agents executing multi-step workflows MUST follow this sequence precisely.

### Step 1: Pre-Flight Tool Check (Implementation of GEPA-Rule-011)

1.  **Identify Required Tools:** Before beginning execution, the agent must parse the entire planned workflow to build a list of all required shell commands and external tools. Special attention must be paid to tools used for validation (`gtb-validator`), saving, and notification.

2.  **Verify Tool Availability:** The agent MUST use the `command -v` utility (or an equivalent internal capability check) to confirm the existence of each required tool in the environment's PATH.

3.  **Halt on Failure:** If any required tool is not found, the workflow **MUST NOT** begin. The agent must halt immediately and report the specific missing tool as the reason for failure, citing this policy.

#### Example Implementation:
```bash
# An agent planning to generate and save a new skill must first check for the validator tool.
echo "Performing pre-flight tool check..."
REQUIRED_TOOL="gtb-validator"

if ! command -v $REQUIRED_TOOL &> /dev/null; then
    # CRITICAL: Halt execution and report failure to the user/orchestrator.
    echo "GEPA Pre-Flight Check FAILED: The required tool '$REQUIRED_TOOL' is not available in the environment. Halting workflow as per Task Orchestration/Execution policy."
    exit 1 # Terminate the workflow
fi

echo "Pre-flight check passed. All required tools are available."
```

### Step 2: Task Decomposition

Break down the goal into a linear sequence of discrete, verifiable steps. Each step should represent a single logical action.

### Step 3: State Tracking

Maintain a state tracker for the workflow, marking each step as 'pending', 'in_progress', 'success', or 'failure'. This is essential for implementing GEPA-Rule-005.

### Step 4: Conditional Sequential Execution

Execute steps in the planned order. Before starting a new step, the agent MUST verify that all of its prerequisite steps in the state tracker are marked as 'success'.

### Step 5: Halt on Mid-Workflow Failure

If any step fails during execution, the entire workflow must be halted immediately. The agent should report the failure, including the step that failed and the reason. Bypassing a failed step is a policy violation unless an explicit error handling and retry mechanism is defined for that specific step.
