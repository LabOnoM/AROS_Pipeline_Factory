# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import os
import sys
import subprocess

def main():
    """
    Checks for the presence of the gtb-validator script and executes it.
    """
    validator_script = "/home/owner03/.gemini/skills/gtb-validator/validate.py"

    # Check if the validator script exists and is executable
    if not os.path.exists(validator_script):
        error_message = (
            f"Error: The required capability 'gtb-validator/validate.py' is missing.\n"
            f"Please ensure that the script exists at the following path:\n"
            f"{validator_script}"
        )
        print(error_message, file=sys.stderr)
        sys.exit(1)

    if not os.access(validator_script, os.X_OK):
        error_message = (
            f"Error: The required capability 'gtb-validator/validate.py' is not executable.\n"
            f"Please grant execute permissions to the script, for example:\n"
            f"chmod +x {validator_script}"
        )
        print(error_message, file=sys.stderr)
        sys.exit(1)


    # Execute the validator script with the provided arguments
    try:
        subprocess.run([sys.executable, validator_script] + sys.argv[1:], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing validator script: {e}", file=sys.stderr)
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
