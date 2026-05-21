
import argparse
import os
import sys

def validate_inputs(source_facts_path, conversation_extractions_path):
    """
    Pre-execution validation hook.
    Checks for the presence, readability, and non-empty status of input files.
    Injects a verification rule for 'extracted facts' and suggests a resolution.
    """
    print("--- Running Pre-Execution Validation Hook ---", file=sys.stderr)
    # Check 1: Source Facts File
    if not os.path.exists(source_facts_path):
        print(f"Error: Source facts file not found at '{source_facts_path}'", file=sys.stderr)
        return False
    if not os.access(source_facts_path, os.R_OK):
        print(f"Error: Source facts file is not readable at '{source_facts_path}'", file=sys.stderr)
        return False
    if os.path.getsize(source_facts_path) == 0:
        print(f"Error: Source facts file is empty at '{source_facts_path}'", file=sys.stderr)
        return False
    print(f"[✓] Source Facts: '{source_facts_path}' is valid.", file=sys.stderr)

    # Check 2: Conversation Extractions File (Modified based on new policy)
    if not conversation_extractions_path or not os.path.exists(conversation_extractions_path) or os.path.getsize(conversation_extractions_path) == 0:
        print("\n--- Input Validation Failed: Missing Extracted Facts ---", file=sys.stderr)
        print("Reason: The '--conversation-extractions' file is missing or empty. This is a mandatory input for the drafting process.", file=sys.stderr)
        print("\nResolution:", file=sys.stderr)
        print("As per policy, the fact extraction process should be invoked to acquire this missing data.", file=sys.stderr)
        print("Please run the appropriate fact extraction skill or workflow and provide the output path via the '--conversation-extractions' argument.", file=sys.stderr)
        print("--- Halting execution until input is provided. ---", file=sys.stderr)
        # This simulates the conditional invocation of another skill by providing a clear, actionable instruction.
        return False

    if not os.access(conversation_extractions_path, os.R_OK):
        print(f"Error: Conversation extractions file is not readable at '{conversation_extractions_path}'", file=sys.stderr)
        return False
    print(f"[✓] Conversation Extractions: '{conversation_extractions_path}' is valid.", file=sys.stderr)


    print("--- Validation Successful ---", file=sys.stderr)
    return True

def draft_content_generation(source_facts_path, conversation_extractions_path):
    """
    Main content generation logic.
    This is a placeholder for the actual KI drafting process.
    """
    print("\n--- Starting Content Generation ---")
    print(f"Reading from: {source_facts_path}")
    print(f"Reading from: {conversation_extractions_path}")
    # In a real scenario, this is where you would read the files
    # and use an LLM or other methods to synthesize the content.
    print("...")
    print("Content generation logic would execute here.")
    print("...")
    print("--- Content Generation Complete ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Draft a Knowledge Item with pre-execution validation."
    )
    parser.add_argument(
        "--source-facts",
        required=True,
        help="Path to the source facts file."
    )
    parser.add_argument(
        "--conversation-extractions",
        required=True,
        help="Path to the conversation extractions file."
    )
    args = parser.parse_args()

    # The validation hook is called *before* any core logic.
    if validate_inputs(args.source_facts, args.conversation_extractions):
        # If validation passes, proceed with the main task.
        draft_content_generation(args.source_facts, args.conversation_extractions)
        print("\nProcess finished successfully.")
        sys.exit(0)
    else:
        # If validation fails, report and exit.
        print("\nPre-execution validation failed. Halting process.", file=sys.stderr)
        sys.exit(1)
