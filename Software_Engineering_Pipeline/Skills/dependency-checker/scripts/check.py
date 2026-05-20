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

class MissingDependenciesError(Exception):
    """Custom exception for missing dependencies."""
    def __init__(self, missing_paths):
        self.missing_paths = missing_paths
        message = "The following required dependencies are missing:\n" + "\n".join(f"- {path}" for path in missing_paths)
        super().__init__(message)

def check_dependencies(paths):
    """
    Checks if all specified file paths exist.

    Args:
        paths: A list of file paths to check.

    Raises:
        MissingDependenciesError: If any of the specified paths do not exist.
    """
    missing_paths = []
    for path in paths:
        if not os.path.exists(path):
            missing_paths.append(path)

    if missing_paths:
        raise MissingDependenciesError(missing_paths)

def main():
    """
    Parses command-line arguments and checks for file dependencies.
    """
    parser = argparse.ArgumentParser(description="Check for the existence of file dependencies.")
    parser.add_argument(
        "--paths",
        nargs="+",
        required=True,
        help="A list of file or directory paths to check.",
    )
    args = parser.parse_args()

    try:
        check_dependencies(args.paths)
        print("All dependencies are satisfied.")
        sys.exit(0)
    except MissingDependenciesError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
