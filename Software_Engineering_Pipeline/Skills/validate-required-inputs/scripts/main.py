import argparse
import json
import os
import sys

def validate_paths(paths):
    """
    Validates a list of file paths for existence and read access.

    Args:
        paths (list): A list of strings representing file paths.

    Returns:
        tuple: A tuple containing two lists: (valid_paths, invalid_paths).
               invalid_paths is a list of dictionaries with 'path' and 'reason'.
    """
    valid_paths = []
    invalid_paths = []

    for path in paths:
        # Expand user- and environment-specific path variables
        expanded_path = os.path.expanduser(os.path.expandvars(path))
        
        if not os.path.exists(expanded_path):
            invalid_paths.append({
                "path": path,
                "reason": "Path does not exist."
            })
        elif not os.access(expanded_path, os.R_OK):
            invalid_paths.append({
                "path": path,
                "reason": "Path is not readable (check permissions)."
            })
        else:
            valid_paths.append(path)

    return valid_paths, invalid_paths

def print_human_readable_report(valid_paths, invalid_paths):
    """Prints a human-readable validation report."""
    print("--- Input Validation Report ---")
    print("\n[✔] Valid Paths:")
    if valid_paths:
        for path in valid_paths:
            print(f"  - {path}")
    else:
        print("  (None)")

    print("\n[✖] Invalid Paths:")
    if invalid_paths:
        for item in invalid_paths:
            print(f"  - {item['path']}: {item['reason']}")
    else:
        print("  (None)")

    print("\n-----------------------------")

def print_json_report(valid_paths, invalid_paths):
    """Prints a JSON-formatted validation report."""
    report = {
        "valid": valid_paths,
        "invalid": invalid_paths
    }
    print(json.dumps(report, indent=2))

def main():
    """
    Main function to parse arguments and run the validation.
    """
    parser = argparse.ArgumentParser(
        description="Performs robust pre-execution checks on file paths to ensure they exist and are readable.",
        epilog="Exits with status 0 if all paths are valid, 1 otherwise."
    )
    parser.add_argument(
        "paths",
        nargs='*',
        help="One or more file or directory paths to validate."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the report in JSON format for machine consumption."
    )
    args = parser.parse_args()

    if not args.paths:
        parser.print_help(sys.stderr)
        sys.exit(1)

    valid_paths, invalid_paths = validate_paths(args.paths)

    if args.json:
        print_json_report(valid_paths, invalid_paths)
    else:
        print_human_readable_report(valid_paths, invalid_paths)

    if invalid_paths:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
