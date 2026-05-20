# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import argparse
import os
import sys

def read_critical_data(filepath):
    """
    Attempts to read data from a specified file, explicitly handling
    potential failure states and articulating the exact reason for failure.

    This function is an implementation of the GEPA rule for "Explicit Reason
    for Failure".

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file if successful.

    Raises:
        Exception: An exception with a detailed, specific failure report string.
    """
    try:
        # Failure State 1: The file does not exist.
        if not os.path.exists(filepath):
            failure_report = (
                f"Operation failed: Cannot read file at '{filepath}'. "
                f"Reason: The file does not exist at the specified path."
            )
            raise FileNotFoundError(failure_report)

        # Failure State 2: The agent lacks read permissions.
        if not os.access(filepath, os.R_OK):
            failure_report = (
                f"Operation failed: Cannot read file at '{filepath}'. "
                f"Reason: Insufficient permissions. The agent does not have "
                f"the required read access to this file or its parent directory."
            )
            raise PermissionError(failure_report)

        # Attempt the core operation
        with open(filepath, 'r') as f:
            content = f.read()

        # Failure State 3: The file exists and is readable, but is empty.
        if not content:
            failure_report = (
                f"Operation failed: The file at '{filepath}' was read successfully, "
                f"but it is empty. Reason: No content found to process."
            )
            raise ValueError(failure_report)

        return content

    except (FileNotFoundError, PermissionError, ValueError) as e:
        # These are the specific, articulated failures. Re-raise them.
        raise e
    except Exception as e:
        # Catch any other unexpected I/O errors and articulate them clearly.
        failure_report = (
            f"An unexpected error occurred while trying to read '{filepath}'. "
            f"This was not a standard file existence or permission issue. "
            f"Underlying System Error: {str(e)}"
        )
        raise IOError(failure_report)

def main():
    """
    Main function to parse arguments and demonstrate the failure
    articulation mechanism.
    """
    parser = argparse.ArgumentParser(
        description="A skill to demonstrate articulating specific failure reasons "
                    "as per AROS communication policy."
    )
    parser.add_argument(
        "--file-path",
        required=True,
        help="The path to the file that the skill should attempt to read."
    )
    args = parser.parse_args()

    try:
        print(f"Attempting to perform critical read operation on: {args.file_path}")
        content = read_critical_data(args.file_path)
        print("\n✅ --- Operation Successful ---")
        print("Successfully read and validated file content:")
        print(content)
    except Exception as e:
        print("\n❌ --- Failure Report ---", file=sys.stderr)
        # The exception 'e' now contains the detailed, articulated failure report.
        print(str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
