# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import sys
import platform
import os
import json
import subprocess

# Define custom exceptions to simulate the target errors as per the design
class ToolNotFoundError(Exception):
    """Custom exception for when a required tool is not found."""
    pass

class PreconditionUnmetError(Exception):
    """Custom exception for when a precondition for an operation is not met."""
    pass

def get_installed_packages():
    """Gets a list of installed pip packages in JSON format."""
    try:
        # Using sys.executable ensures we're using the pip of the current python environment
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'list', '--format', 'json'],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired) as e:
        return [{"error": f"Could not list pip packages: {str(e)}"}]


def gather_diagnostics():
    """Gathers system and environment diagnostic details into a dictionary."""
    return {
        "system": {
            "os_platform": platform.system(),
            "os_version": platform.version(),
            "python_version": sys.version.replace('\n', ' '),
        },
        "environment": {
            "path": os.environ.get("PATH"),
            "pythonpath": os.environ.get("PYTHONPATH"),
            "user": os.environ.get("USER"),
            "cwd": os.getcwd(),
        },
        "installed_packages": get_installed_packages(),
    }


def handle_execution_error(goal, failing_tool_name, exception):
    """
    Constructs a structured error report based on the caught exception.

    This function is the core of the diagnostic reporting, matching the schema
    defined in the SKILL.md.

    Args:
        goal (str): The original goal that was being attempted.
        failing_tool_name (str): The name of the tool or function that failed.
        exception (Exception): The caught exception object.

    Returns:
        dict: A dictionary containing the structured error report.
    """
    error_type = type(exception).__name__
    error_message = str(exception)
    diagnostics = gather_diagnostics()

    # Generate a specific, actionable recommendation based on the error type
    if isinstance(exception, ToolNotFoundError):
        remediation_request = f"Requesting installation of tool: '{failing_tool_name}'. Please make it available in the environment's PATH."
    elif isinstance(exception, PreconditionUnmetError):
        remediation_request = f"Requesting verification of preconditions for tool: '{failing_tool_name}'. The following condition was not met: {error_message}"
    else:
        remediation_request = "No specific remediation suggestion available. Please review the error details and system diagnostics."

    error_report = {
        "error_type": error_type,
        "error_message": error_message,
        "original_goal": goal,
        "failing_tool": failing_tool_name,
        "diagnostics": diagnostics,
        "actionable_recommendations": [remediation_request],
    }

    return error_report


def execute_critical_task(goal, task_function):
    """
    Executes a task and handles specific errors by generating a diagnostic report.

    Args:
        goal (str): A description of the high-level objective.
        task_function (function): The function to execute.

    Returns:
        A dictionary containing either a success status or a detailed error report.
    """
    try:
        print(f"Attempting to execute task for goal: '{goal}'")
        task_function()
        print("Task executed successfully.")
        return {"status": "SUCCESS"}
    except (ToolNotFoundError, PreconditionUnmetError) as e:
        print(f"Caught a recoverable error: {type(e).__name__}")
        # Assume the function's name is the failing tool
        failing_tool_name = task_function.__name__
        report = handle_execution_error(goal, failing_tool_name, e)
        print("Generated Diagnostic Report:")
        print(json.dumps(report, indent=2))
        return report
    except Exception as e:
        print(f"Caught an unexpected critical error: {e}")
        report = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "original_goal": goal,
            "status": "CRITICAL_FAILURE"
        }
        print("Generated Generic Error Report:")
        print(json.dumps(report, indent=2))
        return report

# --- Simulation Functions ---

def simulate_tool_not_found():
    """A dummy function that simulates a tool not being found."""
    raise ToolNotFoundError("The tool 'gtb_validator' was not found in the current environment.")

def simulate_precondition_unmet():
    """A dummy function that simulates a precondition failure."""
    raise PreconditionUnmetError("Mandatory input file '/tmp/draft.md' does not exist.")


if __name__ == "__main__":
    """
    Main execution block to run the audit-ready commands and demonstrate
    the skill's functionality.
    """
    print("--- Scenario 1: ToolNotFoundError ---")
    goal1 = "Validate the new 'my_new_skill.md' against the Golden Test Battery."
    execute_critical_task(goal1, simulate_tool_not_found)

    print("\n" + "="*50 + "\n")

    print("--- Scenario 2: PreconditionUnmetError ---")
    goal2 = "Process the bioinformatics data from the latest run."
    execute_critical_task(goal2, simulate_precondition_unmet)
