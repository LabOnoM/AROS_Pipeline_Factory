# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

# ~/.gemini/skills/finalization_workflow_gate/finalization_workflow_gate.py

from typing import Dict, Tuple

def check_finalization_prerequisites(task_statuses: Dict[str, str]) -> Tuple[bool, str]:
    """
    Evaluates the status of prerequisite tasks before allowing finalization.

    This function implements the GEPA error prevention rule by ensuring that
    critical preceding steps ('content_drafting', 'validation') have successfully
    completed before finalization actions are permitted.

    Args:
        task_statuses: A dictionary tracking the status of workflow tasks.
                       Expected keys: 'content_drafting', 'validation'.
                       Expected values: 'success', 'failure', 'skipped', 'pending'.

    Returns:
        A tuple containing:
        - bool: True if finalization can proceed, False otherwise.
        - str: A message explaining the outcome.
    """
    # Strict check for content drafting success
    content_drafting_status = task_statuses.get('content_drafting', 'pending')
    if content_drafting_status != 'success':
        return (False, f"Finalization blocked: Content drafting failed or was not completed (status: {content_drafting_status}).")

    # Strict check for validation success
    validation_status = task_statuses.get('validation', 'pending')
    if validation_status != 'success':
        return (False, f"Finalization blocked: Validation failed or was skipped (status: {validation_status}).")

    return (True, "All prerequisites met. Finalization can proceed.")

# Example Usage and Audit Trail
if __name__ == '__main__':
    print("--- Running Finalization Workflow Gate Audit ---")

    # Scenario 1: All tasks succeeded
    print("\n[SCENARIO 1: Ideal Path]")
    success_statuses = {
        'content_drafting': 'success',
        'validation': 'success'
    }
    can_finalize, reason = check_finalization_prerequisites(success_statuses)
    print(f"Task Statuses: {success_statuses}")
    print(f"Gate Check Passed: {can_finalize}")
    print(f"Reason: {reason}")
    assert can_finalize is True, "Scenario 1 Failed"

    # Scenario 2: Content drafting failed
    print("\n[SCENARIO 2: Content Drafting Failure]")
    drafting_failed_statuses = {
        'content_drafting': 'failure',
        'validation': 'skipped' # Validation wouldn't run if drafting failed
    }
    can_finalize, reason = check_finalization_prerequisites(drafting_failed_statuses)
    print(f"Task Statuses: {drafting_failed_statuses}")
    print(f"Gate Check Passed: {can_finalize}")
    print(f"Reason: {reason}")
    assert can_finalize is False, "Scenario 2 Failed"

    # Scenario 3: Validation failed
    print("\n[SCENARIO 3: Validation Failure]")
    validation_failed_statuses = {
        'content_drafting': 'success',
        'validation': 'failure'
    }
    can_finalize, reason = check_finalization_prerequisites(validation_failed_statuses)
    print(f"Task Statuses: {validation_failed_statuses}")
    print(f"Gate Check Passed: {can_finalize}")
    print(f"Reason: {reason}")
    assert can_finalize is False, "Scenario 3 Failed"

    # Scenario 4: A required key is missing (e.g., validation not run)
    print("\n[SCENARIO 4: Validation step missing]")
    missing_validation_statuses = {
        'content_drafting': 'success'
    }
    can_finalize, reason = check_finalization_prerequisites(missing_validation_statuses)
    print(f"Task Statuses: {missing_validation_statuses}")
    print(f"Gate Check Passed: {can_finalize}")
    print(f"Reason: {reason}")
    assert can_finalize is False, "Scenario 4 Failed"

    print("\n--- Audit Complete. The gate logic is behaving as expected. ---")
