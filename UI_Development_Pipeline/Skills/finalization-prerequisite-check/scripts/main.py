# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import argparse
import sys
import os

class PrerequisiteError(Exception):
    """Custom exception for prerequisite failures."""
    pass

def check_gtb_validation(validation_passed_str: str):
    """Checks if the GTB validation flag is true."""
    if validation_passed_str is None:
        raise PrerequisiteError("Argument --validation-passed is required for 'gtb_validation' check.")
    if validation_passed_str.lower() != 'true':
        raise PrerequisiteError("GTB validation did not pass. Prerequisite failed.")
    print("OK: GTB validation passed.", file=sys.stderr)

def check_user_auth(user_auth_str: str):
    """Checks if the user authentication flag is true."""
    if user_auth_str is None:
        raise PrerequisiteError("Argument --user-auth is required for 'user_auth' check.")
    if user_auth_str.lower() != 'true':
        raise PrerequisiteError("User is not authenticated. Prerequisite failed.")
    print("OK: User is authenticated.", file=sys.stderr)

def check_file_exists(filepath: str):
    """Checks if the specified file exists."""
    if filepath is None:
        raise PrerequisiteError("Argument --filepath is required for 'file_exists' check.")
    if not os.path.exists(filepath):
        raise PrerequisiteError(f"File does not exist at path: '{filepath}'. Prerequisite failed.")
    print(f"OK: File exists at '{filepath}'.", file=sys.stderr)

def check_file_not_empty(filepath: str):
    """Checks if the specified file is not empty. Implies existence check."""
    if filepath is None:
        raise PrerequisiteError("Argument --filepath is required for 'file_not_empty' check.")
    
    # First, ensure it exists
    check_file_exists(filepath)
    
    # Then, check its size
    if os.path.getsize(filepath) == 0:
        raise PrerequisiteError(f"File is empty at path: '{filepath}'. Prerequisite failed.")
    print(f"OK: File is not empty at '{filepath}'.", file=sys.stderr)


def main():
    """Main function to parse arguments and run checks."""
    parser = argparse.ArgumentParser(
        description="A mandatory logical gate to verify that all critical prerequisites have been met."
    )
    parser.add_argument(
        '--checks',
        nargs='+',
        required=True,
        choices=['gtb_validation', 'user_auth', 'file_exists', 'file_not_empty'],
        help="A list of one or more checks to perform."
    )
    parser.add_argument(
        '--validation-passed',
        type=str,
        help="The result of a gtb-validator run (e.g., 'true' or 'false')."
    )
    parser.add_argument(
        '--user-auth',
        type=str,
        help="The status of user authentication (e.g., 'true' or 'false')."
    )
    parser.add_argument(
        '--filepath',
        type=str,
        help="The path to a file for 'file_exists' or 'file_not_empty' checks."
    )

    args = parser.parse_args()

    check_map = {
        'gtb_validation': (check_gtb_validation, args.validation_passed),
        'user_auth': (check_user_auth, args.user_auth),
        'file_exists': (check_file_exists, args.filepath),
        'file_not_empty': (check_file_not_empty, args.filepath),
    }

    try:
        for check_name in args.checks:
            if check_name in check_map:
                check_func, check_arg = check_map[check_name]
                check_func(check_arg)
        
        print("\nAll prerequisites passed successfully.", file=sys.stderr)

    except PrerequisiteError as e:
        print(f"\nERROR: A prerequisite check failed!", file=sys.stderr)
        print(f"REASON: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
