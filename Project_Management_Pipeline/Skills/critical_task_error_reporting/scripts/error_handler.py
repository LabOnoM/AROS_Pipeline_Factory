# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import os
import sys
import traceback
import logging
import time
from functools import wraps

# --- Configuration ---
LOG_FILE = os.path.expanduser("~/.gemini/antigravity/logs/critical_errors.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

# In-memory store for retry counts. In a real system, this might be a more persistent store like Redis.
retry_counts = {}

def critical_task_handler(retry_threshold=2, fallback_skill=None):
    """
    A decorator that fuses detailed error reporting with the GEPA error prevention rule.
    It retries a function up to a threshold and, upon final failure, logs a
    detailed report and triggers a fallback.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # A unique ID for the task, essential for tracking retries.
            task_id = kwargs.get('task_id', func.__name__)
            
            if task_id not in retry_counts:
                retry_counts[task_id] = 0

            for attempt in range(retry_threshold + 1):
                try:
                    logging.info(f"Attempt {attempt + 1}/{retry_threshold + 1} for task '{task_id}'...")
                    result = func(*args, **kwargs)
                    # If successful, reset counter and return result
                    retry_counts[task_id] = 0
                    logging.info(f"Task '{task_id}' succeeded.")
                    return result
                except Exception as e:
                    retry_counts[task_id] += 1
                    logging.warning(f"Task '{task_id}' failed on attempt {retry_counts[task_id]}. Error: {e}")
                    
                    if retry_counts[task_id] > retry_threshold:
                        # --- Final Failure: Detailed Reporting ---
                        logging.error(f"Task '{task_id}' has failed permanently after {retry_threshold + 1} attempts. Generating detailed report.")
                        
                        # Capture rich context
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                        
                        # Gather environment details
                        env_details = {
                            "python_version": sys.version,
                            "os_platform": sys.platform,
                            "cwd": os.getcwd(),
                        }
                        
                        report = f"""
======================================================================
CRITICAL TASK FAILURE REPORT
======================================================================
Task ID:          {task_id}
Timestamp:        {time.ctime()}
Error Type:       {exc_type.__name__}
Error Details:    {exc_value}

------------------ Traceback ------------------
{tb_str}
------------------ Environment ------------------
{env_details}
----------------------------------------------------------------------
"""
                        # Write detailed report to the log
                        logging.critical(report)

                        # --- Trigger Fallback Mechanism ---
                        if fallback_skill:
                            logging.info(f"Triggering fallback skill: '{fallback_skill}' for task '{task_id}'.")
                            # In a real implementation, this would involve calling the skill execution engine.
                            # For this simulation, we just log the action.
                            print(f"FALLBACK: Executing skill '{fallback_skill}'.")
                        else:
                            logging.info(f"No fallback skill defined. Escalating '{task_id}' to a larger model persona.")
                            print("FALLBACK: Escalating to larger model persona.")

                        # Reset counter after final failure and fallback
                        retry_counts[task_id] = 0
                        # Re-raise the exception so the caller knows the task ultimately failed
                        raise e
                    else:
                        logging.info(f"Retrying task '{task_id}'...")
                        time.sleep(1) # Simple backoff

        return wrapper
    return decorator

# --- Audit-Ready Demonstration ---

# A mock task that always fails
@critical_task_handler(retry_threshold=2, fallback_skill="alternative_file_processor")
def persistently_failing_task(task_id="file_processing_job"):
    print("Executing 'persistently_failing_task'...")
    raise ValueError("Could not access the required data source")

# A mock task that fails once, then succeeds
flaky_task_state = {"calls": 0}
@critical_task_handler(retry_threshold=2, fallback_skill="handle_flaky_task")
def flaky_but_successful_task(task_id="flaky_api_call"):
    print("Executing 'flaky_but_successful_task'...")
    flaky_task_state["calls"] += 1
    if flaky_task_state["calls"] < 2:
        raise ConnectionError("Network timed out")
    print("Flaky task finally succeeded!")
    return True

if __name__ == "__main__":
    print("--- Running Audit Simulation ---")
    
    print("\n1. Demonstrating persistent failure and fallback:")
    try:
        persistently_failing_task()
    except ValueError as e:
        print(f"Caught expected final exception: {e}\n")

    print("-" * 20)
    
    print("\n2. Demonstrating flaky task that succeeds on retry:")
    flaky_but_successful_task()

    print("\n--- Audit Simulation Complete ---")
    print(f"Check the log file for detailed reports: {LOG_FILE}")
