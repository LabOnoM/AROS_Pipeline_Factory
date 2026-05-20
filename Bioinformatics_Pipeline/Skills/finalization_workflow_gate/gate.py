# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import argparse
import sys

def main():
    """
    Acts as a conditional gate for workflows.
    This script checks boolean flags representing the success of previous
    workflow steps. If all required checks pass, it exits with code 0.
    If any check fails, it exits with code 1.
    """
    parser = argparse.ArgumentParser(
        description="A workflow gate to ensure prerequisite steps have completed successfully.",
        epilog="Example: python gate.py --generation-passed True --validation-passed True"
    )

    # Define the arguments that represent the state of the workflow
    parser.add_argument(
        '--generation-passed',
        type=lambda x: (str(x).lower() == 'true'),
        required=True,
        help="Set to 'true' if the content generation step was successful."
    )
    parser.add_argument(
        '--validation-passed',
        type=lambda x: (str(x).lower() == 'true'),
        required=True,
        help="Set to 'true' if the validation step (e.g., gtb-validator) was successful."
    )
    # Future checks can be added here, e.g., --unit-tests-passed

    try:
        args = parser.parse_args()

        # --- Gate Logic ---
        all_checks_passed = True
        error_messages = []

        if not args.generation_passed:
            all_checks_passed = False
            error_messages.append("CRITICAL: Generation phase did not pass.")

        if not args.validation_passed:
            all_checks_passed = False
            error_messages.append("CRITICAL: Validation phase did not pass.")

        # --- Exit based on outcome ---
        if all_checks_passed:
            print("SUCCESS: All prerequisite checks passed. Proceeding with finalization.", file=sys.stdout)
            sys.exit(0)
        else:
            print("--- WORKFLOW HALTED ---", file=sys.stderr)
            print("Reason(s):", file=sys.stderr)
            for msg in error_messages:
                print(f"- {msg}", file=sys.stderr)
            print("Deployment or finalization is blocked due to failed prerequisites.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error in gate script: {e}", file=sys.stderr)
        # Exit with a different code for script errors vs. gate failures
        sys.exit(2)

if __name__ == "__main__":
    main()
