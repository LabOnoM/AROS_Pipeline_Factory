# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SubTaskExecutionManager:
    """
    Manages sub-task execution with retry logic and dynamic fallbacks,
    implementing the GEPA error prevention rule.
    """
    def __init__(self, retry_threshold: int = 2):
        self.retry_threshold = retry_threshold
        self.task_retry_counts = {}
        logging.info(f"SubTaskExecutionManager initialized with retry threshold: {retry_threshold}")

    def execute_task(self, task_id: str, task_function, fallback_skill: str = None, *args, **kwargs) -> bool:
        """
        Executes a given task function with retry logic.

        Args:
            task_id: A unique identifier for the sub-task.
            task_function: The function to execute.
            fallback_skill: Optional. The name of an alternative skill to execute on failure.
            *args, **kwargs: Arguments to pass to the task_function.

        Returns:
            True if the task succeeded, False otherwise.
        """
        if task_id not in self.task_retry_counts:
            self.task_retry_counts[task_id] = 0

        logging.info(f"Attempting task '{task_id}'.")

        while self.task_retry_counts[task_id] <= self.retry_threshold:
            try:
                # Pass the current attempt number to the task function
                success = task_function(attempt=self.task_retry_counts[task_id], *args, **kwargs)
                if success:
                    logging.info(f"Task '{task_id}' succeeded on attempt {self.task_retry_counts[task_id] + 1}.")
                    self.task_retry_counts[task_id] = 0  # Reset on success
                    return True
                else:
                    raise Exception(f"Task '{task_id}' reported failure.")
            except Exception as e:
                logging.warning(f"Task '{task_id}' failed (attempt {self.task_retry_counts[task_id] + 1}): {e}")
                self.task_retry_counts[task_id] += 1
                if self.task_retry_counts[task_id] > self.retry_threshold:
                    self._trigger_fallback(task_id, fallback_skill)
                    return False
                logging.info(f"Retrying task '{task_id}'...")
        return False

    def _trigger_fallback(self, task_id: str, fallback_skill: str = None):
        """Triggers the fallback mechanism."""
        logging.error(f"Task '{task_id}' exceeded retry threshold. Triggering fallback.")
        if fallback_skill:
            logging.warning(f"Executing fallback skill: '{fallback_skill}'")
            print(f"DEBUG: Fallback skill '{fallback_skill}' would be invoked here.")
        else:
            logging.error("Escalating to larger model persona for deeper reasoning.")
            print("DEBUG: Escalation to larger model persona would occur here.")

if __name__ == "__main__":
    # Example Usage / Audit-Ready Command

    def flaky_task(should_fail_first_n_times: int, attempt: int):
        print(f"  --> Running flaky task. Attempt {attempt + 1}. Fails if attempt < {should_fail_first_n_times}")
        return attempt >= should_fail_first_n_times

    manager = SubTaskExecutionManager(retry_threshold=2)

    print("\n--- Scenario 1: Task succeeds on first attempt ---")
    manager.execute_task("task_A", flaky_task, should_fail_first_n_times=0)

    print("\n--- Scenario 2: Task succeeds after one retry ---")
    manager.execute_task("task_B", flaky_task, should_fail_first_n_times=1)

    print("\n--- Scenario 3: Task fails permanently, triggers fallback skill ---")
    manager.execute_task("task_C", flaky_task, fallback_skill="alternative-strategy-skill", should_fail_first_n_times=3)

    print("\n--- Scenario 4: Task fails permanently, escalates to larger model ---")
    manager.execute_task("task_D", flaky_task, should_fail_first_n_times=3)
