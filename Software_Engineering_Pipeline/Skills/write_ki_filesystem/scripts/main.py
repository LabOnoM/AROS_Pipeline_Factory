
import os
import sys
import argparse
import shutil

def main():
    """
    Main function to handle the gated writing of a KI to the filesystem.
    """
    parser = argparse.ArgumentParser(
        description="Writes a validated KI draft to the permanent knowledge base. This script enforces a prerequisite check."
    )
    parser.add_argument(
        "--ki-name",
        type=str,
        required=True,
        help="The name of the Knowledge Item (e.g., 'elastix-overview')."
    )
    parser.add_argument(
        "--validation-passed",
        type=lambda x: (str(x).lower() == 'true'),
        required=True,
        help="Boolean flag (true/false) indicating if the GTB validation prerequisite was met."
    )
    args = parser.parse_args()

    # --- The Logic Patch ---
    # Enforce the finalization prerequisite check.
    if not args.validation_passed:
        print(
            "ERROR: Prerequisite check failed. GTB validation for the KI draft did not pass.",
            file=sys.stderr
        )
        print("HALTING: The KI will not be written to the filesystem.", file=sys.stderr)
        sys.exit(1)

    # --- Proceed with writing if the check passed ---
    print("Prerequisite check passed. Proceeding with KI finalization.")

    source_path = "/tmp/draft_ki.md"
    ki_name = args.ki_name
    
    # Expand user home directory
    home_dir = os.path.expanduser("~")
    permanent_ki_dir = os.path.join(home_dir, ".gemini", "antigravity", "knowledge", ki_name)
    permanent_ki_path = os.path.join(permanent_ki_dir, f"{ki_name}.md")

    try:
        # Check if the source draft file exists
        if not os.path.exists(source_path):
            print(f"ERROR: Source draft file not found at '{source_path}'.", file=sys.stderr)
            sys.exit(1)

        # Create the permanent directory if it doesn't exist
        print(f"Creating directory: {permanent_ki_dir}")
        os.makedirs(permanent_ki_dir, exist_ok=True)

        # Move the file from the temporary location to the permanent location
        print(f"Writing final KI to: {permanent_ki_path}")
        shutil.copy(source_path, permanent_ki_path)
        
        # Optional: Clean up the temporary file after successful copy
        # os.remove(source_path)

        print("\nSUCCESS: KI successfully written to the knowledge base.")
        print(f"  - KI Name: {ki_name}")
        print(f"  - Path: {permanent_ki_path}")

    except Exception as e:
        print(f"An unexpected error occurred during file operation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
