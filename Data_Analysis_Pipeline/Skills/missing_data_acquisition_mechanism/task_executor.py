# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

# ~/.gemini/skills/missing_data_acquisition_mechanism/task_executor.py

import sys

class CriticalInputMissingError(Exception):
    """Custom exception raised when a critical input for a task is missing."""
    def __init__(self, missing_inputs, task_name, available_strategies=None):
        self.missing_inputs = missing_inputs
        self.task_name = task_name
        self.available_strategies = available_strategies or []
        super().__init__(self.formatted_message())

    def formatted_message(self):
        """Generates a user-friendly message detailing the missing inputs and requesting guidance."""
        missing_list = ", ".join(f"'{item}'" for item in self.missing_inputs)
        message = (
            f"Execution HALTED for task: '{self.task_name}'.\n"
            f"Reason: Critical input(s) missing: {missing_list}.\n\n"
            "Please provide the missing information to proceed.\n"
        )
        if self.available_strategies:
            message += "\nAlternatively, you can select one of the following strategies:\n"
            for i, strategy in enumerate(self.available_strategies, 1):
                message += f"{i}. {strategy}\n"
        message += "\nAwaiting user confirmation or alternative strategy selection."
        return message

class TaskExecutor:
    """
    Implements the GEPA rule for pre-execution validation of critical inputs.
    It halts progression and requests user confirmation if critical inputs are missing.
    """
    def __init__(self, task_definition):
        """
        Initializes the executor with a task definition.
        
        Args:
            task_definition (dict): A dictionary containing task details, including
                                    'name', 'critical_inputs', and optional 'alternative_strategies'.
        """
        if not all(k in task_definition for k in ['name', 'critical_inputs']):
            raise ValueError("Task definition must include 'name' and 'critical_inputs' keys.")
        self.task_definition = task_definition

    def pre_execution_check(self, provided_inputs):
        """
        Performs the pre-execution validation check for critical inputs.
        
        Args:
            provided_inputs (dict): A dictionary of inputs provided for the task.
        
        Returns:
            list: A list of missing critical inputs.
        """
        critical_inputs = set(self.task_definition.get('critical_inputs', []))
        provided_keys = set(provided_inputs.keys())
        missing = list(critical_inputs - provided_keys)
        return missing

    def execute_task(self, provided_inputs):
        """
        Executes the task after performing the critical input validation.
        
        Args:
            provided_inputs (dict): A dictionary of inputs provided for the task.
        
        Raises:
            CriticalInputMissingError: If any critical inputs are missing.
        """
        task_name = self.task_definition.get('name', 'Unnamed Task')
        print(f"--- Initiating pre-execution check for task: '{task_name}' ---")
        
        missing_inputs = self.pre_execution_check(provided_inputs)
        
        if missing_inputs:
            print("VALIDATION FAILED: Critical inputs are missing.")
            # Halt progression and request user confirmation
            raise CriticalInputMissingError(
                missing_inputs,
                task_name,
                self.task_definition.get('alternative_strategies')
            )
        
        print("Pre-execution check PASSED. All critical inputs are present.")
        print(f"Executing task '{task_name}'...")
        # In a real scenario, the actual task logic would go here.
        print(f"--- Task '{task_name}' completed successfully. ---")
        return {"status": "success", "task": task_name}

def demonstration():
    """Demonstrates the TaskExecutor's functionality."""
    
    # 1. Define a task with critical inputs and alternative strategies
    task_def = {
        'name': 'GenerateUserReport',
        'critical_inputs': ['user_id', 'database_connection_string'],
        'alternative_strategies': [
            'Generate a generic report for all users.',
            'Cancel report generation.'
        ]
    }
    
    executor = TaskExecutor(task_def)
    
    # --- SCENARIO 1: FAILURE - Missing one critical input ---
    print("\n>>> SCENARIO 1: Simulating failure with missing 'database_connection_string'.\n")
    inputs_missing = {'user_id': 'user-123'}
    try:
        executor.execute_task(inputs_missing)
    except CriticalInputMissingError as e:
        print("\nCaught expected exception:")
        print("===========================")
        print(e)
        print("===========================")
        # Here, the system would block and wait for user feedback.
        print("System would now wait for user to provide the missing input or choose a strategy.")

    # --- SCENARIO 2: SUCCESS - All critical inputs provided ---
    print("\n\n>>> SCENARIO 2: Simulating success with all inputs provided.\n")
    inputs_complete = {
        'user_id': 'user-123',
        'database_connection_string': 'postgresql://user:pass@host:port/db'
    }
    try:
        result = executor.execute_task(inputs_complete)
        print("\nExecution Result:", result)
    except CriticalInputMissingError as e:
        print(f"Caught unexpected exception: {e}", file=sys.stderr)

if __name__ == "__main__":
    demonstration()
