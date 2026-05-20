# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import json
import argparse
import sys
import os
import time

class ToolAvailabilityChecker:
    """
    Checks if a tool/skill is available in the skill registry.
    Incorporates a simple retry mechanism for reading the registry file.
    """

    def __init__(self, registry_path='~/.gemini/skills/skill_registry.json', max_retries=2, retry_delay=1):
        self.registry_path = os.path.expanduser(registry_path)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.retries = {}

    def _read_registry(self):
        """Reads the skill registry file with a retry mechanism."""
        attempt = 0
        while attempt < self.max_retries:
            try:
                with open(self.registry_path, 'r') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                # Log error and wait before retrying
                time.sleep(self.retry_delay)
                attempt += 1
        return None # Return None if all retries fail

    def check_tool(self, tool_name):
        """
        Validates the availability of a specific tool.

        Args:
            tool_name (str): The name of the tool to check.

        Returns:
            dict: A dictionary containing the validation result.
        """
        task_id = f"read_registry_{self.registry_path}"
        self.retries.setdefault(task_id, 0)

        registry_data = self._read_registry()

        if registry_data is None:
            self.retries[task_id] += 1
            # GEPA Fallback: If reading the registry fails after retries
            return {
                "tool_name": tool_name,
                "available": False,
                "confirmed": False,
                "error": f"Failed to read or parse skill registry at '{self.registry_path}' after {self.max_retries} attempts. Execution halted.",
                "gepa_rule": "GEPA Error Prevention Patch activated. Fallback: Halt execution due to persistent file read error."
            }

        available_skills = registry_data.get("skills", [])
        is_available = tool_name in available_skills

        if is_available:
            # Reset retry count on success
            self.retries[task_id] = 0
            return {
                "tool_name": tool_name,
                "available": True,
                "confirmed": False, # IMPORTANT: This must be set to True by a separate confirmation step
                "message": f"Tool '{tool_name}' is available. Awaiting execution confirmation."
            }
        else:
            return {
                "tool_name": tool_name,
                "available": False,
                "confirmed": False,
                "error": f"Tool '{tool_name}' is not listed in the skill registry. Execution forbidden.",
                "gepa_rule": "Tool not found in registry. Fallback: Halt execution."
            }

def main():
    parser = argparse.ArgumentParser(description="Check for tool/method availability and mandate confirmation.")
    parser.add_argument("tool_name", type=str, help="The name of the tool/skill to check.")
    args = parser.parse_args()

    checker = ToolAvailabilityChecker()
    result = checker.check_tool(args.tool_name)
    print(json.dumps(result, indent=2))
    if not result["available"]:
        sys.exit(1)

if __name__ == "__main__":
    main()
