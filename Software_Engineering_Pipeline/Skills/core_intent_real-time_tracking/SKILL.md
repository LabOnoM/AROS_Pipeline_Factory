---
name: core_intent_real-time_tracking
description: A policy and implementation for actively monitoring progress against a higher-order user intent and escalating if the critical path to that intent is blocked.
license: MIT
skill-author: AROS_code_generator
---

# Policy: Core Intent Real-Time Tracking

## 1. Core Principle

This policy ensures that an agent's execution path remains aligned with the user's primary, higher-order intent. The agent must not only execute individual sub-tasks but also actively monitor whether the sequence of tasks is making meaningful progress toward the overall goal. The primary directive is to detect and escalate situations where the core intent can no longer be satisfied due to repeated failures on a critical path.

## 2. GEPA Error Prevention Rule: Intent-Aligned Escalation

This policy codifies a critical GEPA rule for robust, intent-driven execution.

> **If a sub-task on the critical path to achieving the user's primary intent fails repeatedly, the agent MUST halt the current execution path and trigger an explicit escalation rather than continuing with a flawed or blocked plan.**

This rule prevents agents from wasting resources on retries that will not lead to success and ensures that the system can quickly pivot or report failure when the user's goal becomes unattainable through the current strategy.

### Key Definitions
-   **Higher-Order Intent:** The ultimate goal the user wants to achieve (e.g., "deploy the web application," not "run `docker build`").
-   **Critical Path:** A sequence of sub-tasks where the failure of any single task renders the final goal unachievable. For example, if the 'compile code' step fails, the 'deploy application' intent cannot be met.
-   **Repeated Failure:** A sub-task fails more than a configured number of times (e.g., 2 attempts), as inspired by the `gepa_error_prevention_patch` skill.

## 3. Mandatory Escalation Mechanism

When a critical path is determined to be blocked, the agent **MUST** raise a specific exception to interrupt the standard control flow. This makes the failure explicit and forces the parent orchestrator to handle the issue, aligning with the `robust-self-correction` policy.

-   **Primary Mechanism:** Raise the `CriticalPathBlockedError` exception. This provides a clear, machine-readable signal that the core intent has been compromised.
-   **Secondary Mechanism (Stateful Tracking):** For workflows that use a status dictionary (similar to `finalization_workflow_gate`), an alert flag (e.g., `intent_compromised: True`) should be set in addition to the exception.

## 4. Implementation Guide: `IntentTracker`

To implement this policy, agents should use the `IntentTracker` class. This class acts as a manager for executing tasks under the supervision of the user's core intent.

### Custom Exception
```python
class CriticalPathBlockedError(Exception):
    """
    Raised when a task on the critical path to the user's intent fails
    repeatedly, indicating the overall goal is likely unachievable.
    """
    def __init__(self, task_id, intent, message):
        self.task_id = task_id
        self.intent = intent
        self.message = message
        super().__init__(f"Critical path blocked for intent '{intent}'. Task '{task_id}' failed: {message}")

```

### Core `IntentTracker` Class
The `IntentTracker` monitors task executions, manages retries, and triggers escalation.

```python
from collections import defaultdict

class IntentTracker:
    def __init__(self, user_intent, critical_tasks, retry_threshold=2):
        self.user_intent = user_intent
        self.critical_tasks = set(critical_tasks)
        self.retry_threshold = retry_threshold
        self.failure_counts = defaultdict(int)
        self.status = {
            'intent': user_intent,
            'critical_path_status': 'OK',
            'completed_tasks': [],
            'failed_tasks': {}
        }
        print(f"INTENT_TRACKER: Initialized for intent: '{self.user_intent}'")
        print(f"INTENT_TRACKER: Critical tasks identified: {self.critical_tasks}")

    def execute_task(self, task_id, task_function, *args, **kwargs):
        """
        Executes a task, tracking its progress and handling failures.
        If a critical task fails repeatedly, it raises CriticalPathBlockedError.
        """
        print(f"INTENT_TRACKER: Attempting task '{task_id}'...")
        while self.failure_counts[task_id] < self.retry_threshold:
            try:
                result = task_function(*args, **kwargs)
                print(f"INTENT_TRACKER: Task '{task_id}' succeeded.")
                self.failure_counts[task_id] = 0 # Reset on success
                self.status['completed_tasks'].append(task_id)
                return result
            except Exception as e:
                self.failure_counts[task_id] += 1
                error_message = f"Attempt {self.failure_counts[task_id]}/{self.retry_threshold} failed: {e}"
                print(f"INTENT_TRACKER: ERROR in task '{task_id}'. {error_message}")
                self.status['failed_tasks'][task_id] = error_message

                if task_id in self.critical_tasks and self.failure_counts[task_id] >= self.retry_threshold:
                    self.status['critical_path_status'] = 'BLOCKED'
                    block_message = f"Retry threshold reached for critical task '{task_id}'."
                    print(f"INTENT_TRACKER: CRITICAL FAILURE. {block_message}")
                    raise CriticalPathBlockedError(task_id, self.user_intent, block_message)

        # This part is reached if a non-critical task exhausts its retries
        final_failure_msg = f"Task '{task_id}' failed after {self.retry_threshold} attempts."
        raise Exception(final_failure_msg)

```

## 5. Example Usage

```python
# --- Define some example tasks ---
def compile_code():
    print("Executing: compile_code")
    # Simulate failure
    raise ValueError("Syntax error in source file")

def run_unit_tests(compile_success):
    if not compile_success:
        return False
    print("Executing: run_unit_tests")
    return True

def generate_documentation():
    print("Executing: generate_documentation (non-critical)")
    return True

# --- Main workflow ---
USER_GOAL = "Build and test the software package"
CRITICAL_STEPS = ['compile', 'test']

tracker = IntentTracker(user_intent=USER_GOAL, critical_tasks=CRITICAL_STEPS)

try:
    compile_result = tracker.execute_task('compile', compile_code)
    # This line will not be reached in this example
    test_result = tracker.execute_task('test', run_unit_tests, compile_result)
    
    # Non-critical tasks can still be run
    tracker.execute_task('docs', generate_documentation)

except CriticalPathBlockedError as e:
    print(f"\\n--- WORKFLOW HALTED ---")
    print(f"Reason: {e}")
    print("Escalating to a higher-level recovery process or reporting to user.")
    print("Final Status:", tracker.status)

except Exception as e:
    print(f"\\n--- A non-critical task failed permanently ---")
    print(f"Reason: {e}")

```
