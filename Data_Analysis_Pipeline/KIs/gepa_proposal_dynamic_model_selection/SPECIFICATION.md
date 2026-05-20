---
ki_name: gepa_proposal_dynamic_model_selection
ki_author: mutation_sweeper
ki_version: 1.0
related_skill: gepa_error_prevention_patch
---

# GEPA Proposal: Dynamic Model Selection Rule

## 1. Overview

This document specifies the requirements for enhancing the `gepa_error_prevention_patch` skill. The goal is to evolve the existing "Model Escalation" fallback into a more intelligent **Dynamic Model Selection** mechanism. This rule mandates that tasks utilize the most cost-effective computational model capable of achieving a satisfactory output, implementing a tiered "model cascade" to balance cost, latency, and quality.

## 2. Proposed GEPA Rule

All AROS agents and skills executing tasks that leverage large language models MUST adhere to the following principle:

> **Tasks MUST utilize the most cost-effective (i.e., fastest and cheapest) computational model that can achieve a satisfactory output quality. If an initial model fails to produce a valid output, the system MUST dynamically escalate to a more powerful model in a predefined, ordered sequence. The determination of output validity MUST be performed by a concrete validation function.**

## 3. Core Component Update: `SubTaskExecutionManager`

The `SubTaskExecutionManager` within the `gepa_error_prevention_patch` skill must be updated to manage a sequence of models based on their capabilities and cost.

### 3.1. New and Updated Parameters

The `execute_task` method signature will be updated to include the following:

-   **`task_id` (String):** *[No change]* Unique identifier for the task instance.
-   **`task_function` (Callable):** *[No change]* The function to be executed.
-   **`model_selection_policy` (List[String]):** *[New]* An ordered list of model identifiers, ranked from lowest to highest cost/capability (e.g., `['gemini-1.5-flash', 'gemini-1.5-pro', 'claude-3-opus']`). This replaces the generic "larger model persona" concept.
-   **`validation_function` (Callable):** *[New]* A function that accepts the output of the `task_function` and returns a boolean (`True` for valid, `False` for invalid). This function is the gatekeeper for model escalation.
-   **`max_retries_per_model` (Integer):** *[Update]* The number of times to attempt the `task_function` *with the same model* before escalating to the next model in the policy. Defaults to `1`.
-   **`fallback_skill` (Callable):** *[No change]* An optional alternative skill to execute if the entire model selection cascade fails.

### 3.2. Updated Workflow Logic

1.  **Initiation:** The `execute_task` method is called with the new parameters. The manager selects the first model from the `model_selection_policy`.
2.  **Execution Attempt:** The `task_function` is executed using the currently selected model.
3.  **Output Validation:** The output of the `task_function` is passed to the `validation_function`.
4.  **On Valid Output:** If the `validation_function` returns `True`, the task is considered successful. The process terminates and returns the result.
5.  **On Invalid Output:** If the `validation_function` returns `False` or the task fails, the retry counter for the *current model* is incremented.
6.  **Intra-Model Retry:** If the `max_retries_per_model` limit has not been reached, the system re-attempts the task with the **same model**.
7.  **Model Escalation:** If the `max_retries_per_model` limit is reached, the manager selects the **next model** from the `model_selection_policy` and resets the retry counter. The process repeats from Step 2.
8.  **Cascade Failure:** If all models in the `model_selection_policy` have been attempted and have failed, the system triggers the optional `fallback_skill`. If no `fallback_skill` is provided, a critical failure is logged, indicating that the task could not be completed even with the most powerful model available.

## 4. Constraints & System Impact

-   **Cost-Efficiency:** The `model_selection_policy` parameter is the primary mechanism for enforcing cost control. Policies must be constructed with the lowest-cost model listed first.
-   **Computational Requirements:** This design requires the AROS environment to have access to multiple models. The model identifiers in the policy must correspond to valid, accessible model endpoints.
-   **Output Quality:** The `validation_function` is critical. It must be a robust, deterministic function to prevent unnecessary escalations. It can be a simple format check, a linter, or a call to a more complex validation skill like `gtb-validator`.
-   **Logging:** The execution manager MUST log which model was used for each attempt and the reason for any escalation. This is crucial for auditing, cost analysis, and performance tuning.

## 5. Pseudocode Example

```python
# Define the task and validation logic
def generate_code_task(model):
    # aros.llm_call(prompt="...", model=model) -> returns generated_code
    pass

def is_code_valid(generated_code):
    # linter.check(generated_code) -> returns True or False
    pass

# Define the model cascade
model_policy = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.5-pro-large_context']

# Instantiate the manager and execute the task
execution_manager = SubTaskExecutionManager()
result = execution_manager.execute_task(
    task_id="complex_code_gen_abc123",
    task_function=generate_code_task,
    model_selection_policy=model_policy,
    validation_function=is_code_valid,
    max_retries_per_model=1
)
```
