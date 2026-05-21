
import argparse
import sys

def main():
    """
    Acts as a gate for a workflow, checking the status flags of preceding steps.
    This script enforces the GEPA error prevention rule by providing a strict
    conditional check before a finalization step is executed.
    
    It exits with a code of 0 only if all required status flags are 'true'.
    Otherwise, it prints an error message to stderr and exits with a code of 1.
    """
    parser = argparse.ArgumentParser(
        description="A gate to ensure critical workflow steps have passed before finalization."
    )
    parser.add_argument(
        '--content-drafting-status',
        required=True,
        type=str,
        choices=['true', 'false'],
        help="The success status of the content drafting step ('true' or 'false')."
    )
    parser.add_argument(
        '--validation-status',
        required=True,
        type=str,
        choices=['true', 'false'],
        help="The success status of the validation step ('true' or 'false')."
    )

    args = parser.parse_args()

    # Convert string arguments to booleans for evaluation
    drafting_success = args.content_drafting_status == 'true'
    validation_success = args.validation_status == 'true'

    # Strict conditional check
    if drafting_success and validation_success:
        print("Gate passed: All critical steps succeeded. Finalization is authorized.", file=sys.stdout)
        sys.exit(0)
    else:
        error_messages = []
        if not drafting_success:
            error_messages.append("Gate failed: Content drafting step did not succeed.")
        if not validation_success:
            error_messages.append("Gate failed: Validation step did not succeed.")
        
        # Print all collected errors to stderr and exit with a failure code
        for msg in error_messages:
            print(msg, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
