# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import os
import subprocess
import json
import argparse
import time

MAX_RETRIES = 3
DRAFT_FILE_PATH = "/tmp/draft_artifact.md"
GTB_VALIDATOR_SCRIPT = "/home/owner03/.gemini/skills/gtb-validator/validate.py"

def run_validation(task_type: str) -> dict:
    """Runs the GTB validator and returns the parsed JSON output."""
    try:
        command = [
            "python",
            GTB_VALIDATOR_SCRIPT,
            DRAFT_FILE_PATH,
            task_type
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=120
        )
        return json.loads(result.stdout)
    except FileNotFoundError:
        print(f"ERROR: GTB Validator script not found at {GTB_VALIDATOR_SCRIPT}")
        return {"passed": False, "reasoning": "GTB Validator script not found."}
    except subprocess.CalledProcessError as e:
        print(f"ERROR: GTB Validator script returned a non-zero exit code: {e.stderr}")
        return {"passed": False, "reasoning": f"Validator script execution failed: {e.stderr}"}
    except json.JSONDecodeError:
        print("ERROR: Failed to decode JSON from GTB Validator output.")
        return {"passed": False, "reasoning": "Invalid JSON output from validator."}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"passed": False, "reasoning": f"An unexpected error occurred: {e}"}

def attempt_self_correction(draft_content: str, reason: str) -> str:
    """
    Simulates a self-correction step by appending the reason for the last
    failure to the draft. In a real implementation, this would involve
    an LLM call to refine the content based on the feedback.
    """
    correction_header = "\\n\\n--- REFINEMENT ATTEMPT ---\\n"
    feedback = f"Automated Refinement Log: The previous validation failed. Reason: '{reason}'. Attempting to correct.\\n"
    return draft_content + correction_header + feedback

def main():
    """
    Main function to run the iterative validation and self-correction loop.
    """
    parser = argparse.ArgumentParser(description="GEPA Quality Gate: Iterative Validation Loop")
    parser.add_argument("--draft-content", required=True, help="The string content of the artifact to validate.")
    parser.add_argument("--final-filepath", required=True, help="The final destination path for the artifact if validation passes.")
    parser.add_argument("--task-type", required=True, help="The task type for the GTB validator (e.g., 'knowledge_retrieval').")
    args = parser.parse_args()

    current_draft_content = args.draft_content

    for i in range(MAX_RETRIES):
        attempt_num = i + 1
        print(f"--- Validation Attempt {attempt_num}/{MAX_RETRIES} ---")

        # 1. Write the current draft to the temporary file
        try:
            with open(DRAFT_FILE_PATH, "w") as f:
                f.write(current_draft_content)
        except IOError as e:
            print(f"FATAL: Could not write to temporary file {DRAFT_FILE_PATH}: {e}")
            exit(1)

        # 2. Run the GTB Validator
        validation_result = run_validation(args.task_type)
        print(f"Result: {'PASS' if validation_result.get('passed') else 'FAIL'}")

        # 3. Analyze & Action
        if validation_result.get("passed"):
            print(f"Validation PASSED. GTB Score >= 7.0.")
            try:
                # On success, move the file to its final destination
                os.rename(DRAFT_FILE_PATH, args.final_filepath)
                print(f"Successfully moved artifact to {args.final_filepath}")
                exit(0) # Success
            except OSError as e:
                print(f"FATAL: Could not move validated file to {args.final_filepath}: {e}")
                exit(1)

        else:
            reason = validation_result.get('reasoning', 'No reason provided.')
            print(f"Reason: {reason}")
            if attempt_num < MAX_RETRIES:
                print("Attempting self-correction...")
                current_draft_content = attempt_self_correction(current_draft_content, reason)
                time.sleep(1) # Simulate processing time for refinement
            else:
                break # Max retries reached

    # 4. Handle failure after max retries
    print(f"--- Escalation ---")
    print(f"Validation failed after {MAX_RETRIES} attempts. Aborting.")
    print("Escalating task to a larger model for manual review and resolution.")
    print(f"The failed draft remains at: {DRAFT_FILE_PATH}")
    exit(1)

if __name__ == "__main__":
    main()
