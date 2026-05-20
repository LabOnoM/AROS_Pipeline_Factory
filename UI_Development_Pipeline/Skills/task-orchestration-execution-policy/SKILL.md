---
name: task-orchestration-execution-policy
description: "A policy that governs the execution of multi-step workflows, mandating an upfront check for all required tools and capabilities to prevent mid-task failures."
skill-author: AROS_code_generator
license: MIT
version: 2.0
---

# Policy: Task Orchestration & Execution (v2.0)

This policy defines the mandatory pre-flight checks an agent must perform before initiating any multi-step workflow. Its primary goal is to ensure that the execution environment is fully equipped with all necessary tools *before* the task begins, preventing common runtime failures.

## GEPA Error Prevention Rule: Upfront Tool Availability Check (GEPA-Rule-011)

**An agent MUST NOT initiate a multi-step workflow without first verifying the existence and executability of all required command-line tools, especially those needed for the finalization, validation, and notification stages.**

This rule is a direct extension of the `agent-environment-provisioning` and `agent-environment-capabilities` policies, but with a specific focus on the orchestration phase. A failure to confirm tool availability at the outset is a critical policy violation and a common cause of failed or incomplete tasks.

---

## MANDATORY SKILL INSTRUCTIONS:

### Execution Logic

1.  **Identify Tool Dependencies:** Before beginning execution, the agent must parse the entire workflow to compile a definitive list of all required shell commands and external tools.

2.  **Prioritize Finalization Tools:** The check must explicitly include tools required for the final steps of the workflow, as their absence often leads to the most critical failures (e.g., inability to save valid results).
    *   **Examples:** `gtb-validator`, `git`, `curl`, `python`, notification scripts, or any other tool used in the `finalization_workflow_gate`.

3.  **Perform Pre-flight Check:** The agent must execute a script to verify that each tool in the dependency list is available in the system's PATH.

4.  **Conditional Execution:**
    *   **If all tools are found:** Proceed with the workflow execution.
    *   **If one or more tools are missing:**
        *   HALT execution immediately.
        *   Report the specific missing tools as the reason for failure, citing this policy (GEPA-Rule-011).
        *   DO NOT attempt to proceed with a partial toolset.

### Implementation Guide: Python

The following Python function serves as a reference implementation for the pre-flight check. It is robust and should be used to validate the presence of required tools.

```python
import subprocess
import shutil

def check_tool_availability(required_tools: list[str]) -> None:
    """
    Verifies that all required command-line tools are available in the PATH.

    Args:
        required_tools: A list of tool names to check (e.g., ['git', 'gtb-validator']).

    Raises:
        FileNotFoundError: If a required tool is not found in the system's PATH.
    """
    print("GEPA-Rule-011: Performing upfront tool availability check...")
    missing_tools = []
    
    for tool in required_tools:
        if not shutil.which(tool):
            missing_tools.append(tool)
            
    if missing_tools:
        error_message = (
            "Pre-flight check failed: The following required tools are missing "
            f"from the environment: {', '.join(missing_tools)}. "
            "Aborting workflow to prevent mid-task failure."
        )
        print(f"ERROR: {error_message}")
        raise FileNotFoundError(error_message)
        
    print("All required tools are available. Proceeding with workflow.")

# --- Example Usage ---
# This check MUST be run before the main workflow logic begins.
try:
    # This list must be compiled from the specific workflow's requirements.
    workflow_tools = [
        "python",
        "git",
        "gtb-validator", # Critical for saving valid skills/policies
        "curl"
    ]
    check_tool_availability(workflow_tools)

    # If the check passes, the rest of the workflow logic would follow here.
    print("Workflow can now safely execute.")

except FileNotFoundError as e:
    # The workflow must be halted here.
    print(f"Workflow halted due to policy violation: {e}")

```

### Relationship to Other Policies

-   **Complements `finalization_workflow_gate`**: This policy ensures that the tools needed to *run* the finalization gate (like `gtb-validator`) are available from the very beginning. The `finalization_workflow_gate` then ensures the gate is used correctly at the end.
-   **Specializes `agent-environment-provisioning`**: While the provisioning policy is a general rule about checking the environment, this policy applies it specifically to the start of a complex task orchestration, adding the emphasis on finalization tools.
