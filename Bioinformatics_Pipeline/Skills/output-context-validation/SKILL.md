---
name: output-context-validation
description: A pre-presentation hook that validates if a proposed output is contextually aligned with the active task, preventing context drift.
license: MIT
skill-author: AROS-Core-Dev
---

# Output Context Validation Skill

This skill acts as a critical quality gate to ensure that the final output of a task is directly relevant to the original goal. It intercepts a proposed output, evaluates its alignment with the active task description, and either approves it or flags a context mismatch.

## When to Use

- **Final Answer Check:** Use this skill as the very last step before presenting a final answer or result to the user.
- **Preventing Context Drift:** In long or complex workflows with multiple steps, use this to ensure the final output hasn't deviated from the initial objective.
- **Workflow Integrity:** Integrate into any automated workflow that generates content (code, reports, analysis) to validate that the output is on-topic.

## Instructions

1.  **Save the proposed output** to a temporary file.
    ```bash
    # Example
    # ACTION: write_local_file(filepath="/tmp/proposed_output.txt", content="...")
    ```

2.  **Identify the active task description.** This is the original goal or instruction that initiated the current workflow.

3.  **Run the validator script**, providing the path to the output file and the task description as arguments.
    ```bash
    python ~/.gemini/skills/output-context-validation/validator.py "/tmp/proposed_output.txt" "The active task description goes here"
    ```

4.  **Analyze the result.** The script will print a JSON object.
    *   If `"passed": true`, the output is contextually aligned and can be presented.
    *   If `"passed": false`, the output has drifted from the task. You **MUST NOT** present the output. Instead, analyze the `"reasoning"` field and re-generate the output to better align with the task.

## Example Usage

### Scenario: Task is to write a Python script.

**Active Task:** "Develop a Python script that lists all files in a given directory."

**Proposed Output (saved to `/tmp/output.txt`):**
```python
import os

def list_files(directory):
  """Lists all files in a given directory."""
  for filename in os.listdir(directory):
    print(filename)

list_files('.')
```

**Validation Command:**
```bash
python ~/.gemini/skills/output-context-validation/validator.py "/tmp/output.txt" "Develop a Python script that lists all files in a given directory."
```

**Expected Result:**
```json
{
  "passed": true,
  "reasoning": "The output provides a Python script that directly addresses the task of listing files in a directory."
}
```

### Scenario: Context has drifted.

**Active Task:** "What is the capital of Canada?"

**Proposed Output (saved to `/tmp/output.txt`):**
"Canada is the second-largest country in the world. It has a robust economy and is known for its natural beauty, including the Rocky Mountains and Niagara Falls."

**Validation Command:**
```bash
python ~/.gemini/skills/output-context-validation/validator.py "/tmp/output.txt" "What is the capital of Canada?"
```

**Expected Result:**
```json
{
  "passed": false,
  "reasoning": "The output provides general facts about Canada but fails to answer the specific question about its capital city."
}
```
