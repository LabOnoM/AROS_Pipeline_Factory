# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import argparse
import sys
import json
import os

def get_llm_evaluation(output_content, task_description):
    """
    Generates a prompt to be sent to an LLM for evaluating context alignment.
    In a real system, this would make an API call to a model. For this skill,
    the prompt logic itself is the deliverable. A simple keyword check is
    used as a placeholder for the actual LLM call.
    """
    prompt = f"""
    You are an expert context alignment evaluator for an advanced AI system. Your role is to determine if a proposed output is a direct and relevant response to a given task.

    **Active Task:**
    "{task_description}"

    **Proposed Output:**
    ---
    {output_content}
    ---

    **Evaluation Criteria:**
    1.  **Directness:** Does the output directly address the core request of the task?
    2.  **Relevance:** Is all the information in the output relevant to the task? Does it contain extraneous or off-topic information?
    3.  **Completeness:** Does the output fulfill all aspects of the task?

    **Your Task:**
    Analyze the "Proposed Output" against the "Active Task". Respond with a JSON object ONLY, with no other text or explanation. The JSON object should have two keys:
    - "passed": boolean (true if the output is well-aligned, false otherwise)
    - "reasoning": string (a brief, one-sentence explanation for your decision)

    **Example 1 (Good Alignment):**
    Active Task: "Write a Python function to calculate the factorial of a number."
    Proposed Output: "```python\\ndef factorial(n):\\n    if n == 0:\\n        return 1\\n    else:\\n        return n * factorial(n-1)\\n```"
    Your JSON Response:
    {{
        "passed": true,
        "reasoning": "The output provides a Python function that correctly calculates the factorial as requested."
    }}

    **Example 2 (Bad Alignment):**
    Active Task: "What is the capital of France?"
    Proposed Output: "France is a country in Western Europe known for its cuisine and culture. The Eiffel Tower is a famous landmark."
    Your JSON Response:
    {{
        "passed": false,
        "reasoning": "The output describes France but fails to directly answer the question about its capital city."
    }}

    Now, evaluate the provided task and output.
    """
    # This is a placeholder for the real LLM call.
    # A simple heuristic is used to simulate the evaluation for this script.
    task_words = set(task_description.lower().split())
    output_words = set(output_content.lower().split())
    common_words = task_words.intersection(output_words)

    # If there's very little word overlap, it's likely a mismatch.
    # This is a crude simulation. The real power is in the prompt for a real LLM.
    if len(common_words) < 2 and "error" not in output_content.lower():
        return {
            "passed": False,
            "reasoning": "The output appears to have very little semantic overlap with the task description, suggesting a potential context mismatch."
        }
    else:
        return {
            "passed": True,
            "reasoning": "The output appears to be contextually aligned with the active task."
        }


def main():
    """Main function to parse arguments and run the validation."""
    parser = argparse.ArgumentParser(description="Validate output context against an active task.")
    parser.add_argument("output_filepath", type=str, help="The path to the file containing the proposed output.")
    parser.add_argument("task_description", type=str, help="A description of the active task.")

    args = parser.parse_args()

    if not os.path.exists(args.output_filepath):
        print(json.dumps({
            "passed": False,
            "reasoning": f"Error: The file '{args.output_filepath}' does not exist."
        }, indent=2))
        sys.exit(1)

    try:
        with open(args.output_filepath, 'r', encoding='utf-8') as f:
            output_content = f.read()
    except Exception as e:
        print(json.dumps({
            "passed": False,
            "reasoning": f"Error reading file: {e}"
        }, indent=2))
        sys.exit(1)


    if not output_content.strip():
        print(json.dumps({
            "passed": False,
            "reasoning": "Error: The output file is empty."
        }, indent=2))
        sys.exit(1)

    result = get_llm_evaluation(output_content, args.task_description)
    print(json.dumps(result, indent=2))

    if not result["passed"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
