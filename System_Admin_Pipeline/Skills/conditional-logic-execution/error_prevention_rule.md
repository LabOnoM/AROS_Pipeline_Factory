---
name: error_prevention_rule
description: A mandatory GEPA policy that ensures all conditional logic explicitly verifies the success of antecedent steps before execution.
license: MIT
skill-author: AROS-Core
---

# Policy: Conditional Logic Error Prevention Rule

## 1. Core Principle

This policy enforces a critical error-prevention step in all conditional logic. The execution of a logic branch MUST be gated by an explicit verification of the success of all critical antecedent steps. This prevents the system from executing logic based on failed or incomplete precedent steps.

## 2. GEPA Error Prevention Rule

This policy is a core component of the GEPA (Genetic Evolution and Policy Adaptation) error prevention strategy.

**The rule dictates:** All conditional logic must explicitly verify the success of all critical antecedent steps before executing a subsequent logic branch. This prevents error cascades and ensures data integrity.

## 3. Mandatory Procedure

When designing any conditional logic, you MUST follow this structure:

1.  **Initialize a Status Tracker:** At the beginning of your workflow, create a dictionary to track the success or failure of each step.
2.  **Execute and Record:** After each critical step, update the status tracker with the outcome (`True` for success, `False` for failure).
3.  **Apply the Gate:** Before any conditional logic branch, check the status of the relevant antecedent steps in the status tracker.
4.  **Conditional Execution:** Only if the relevant antecedent steps have successfully completed, proceed with the execution of the logic branch. If any of the relevant antecedent steps have failed, the workflow should terminate and report the failure, including the status tracker for debugging.
