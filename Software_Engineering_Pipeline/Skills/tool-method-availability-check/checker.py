# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import json
import argparse
import shutil
import os

def check_tool_availability(tool_name):
    """
    Checks if a tool is registered and available in the system PATH.
    It also enforces a confirmation step by returning a structured JSON
    that dictates whether execution is permitted.
    """
    # Correctly expand the user home directory
    registry_path = os.path.expanduser('~/.gemini/skills/tool-method-availability-check/tool_registry.json')
    result = {
        "tool_name": tool_name,
        "registered": False,
        "executable": False,
        "execution_permitted": False,
        "reason": ""
    }

    try:
        with open(registry_path, 'r') as f:
            registry = json.load(f)
        
        if tool_name in registry.get("tools", []):
            result["registered"] = True
        else:
            result["reason"] = f"Tool '{tool_name}' is not listed in the tool registry. Execution is forbidden as per GEPA policy."
            # The function will return here, execution_permitted remains False
            return result

        if shutil.which(tool_name):
            result["executable"] = True
        else:
            result["reason"] = f"Tool '{tool_name}' is registered but not found in the system PATH. Execution is forbidden."
            # The function will return here, execution_permitted remains False
            return result
        
        # If both checks pass, explicitly permit execution
        result["execution_permitted"] = True
        result["reason"] = f"Tool '{tool_name}' is registered and available. Execution is permitted."

    except FileNotFoundError:
        result["reason"] = f"Critical error: The tool registry at {registry_path} was not found. Cannot verify any tools."
    except json.JSONDecodeError:
        result["reason"] = f"Critical error: The tool registry at {registry_path} is corrupted. Cannot verify any tools."
    except Exception as e:
        result["reason"] = f"An unexpected error occurred: {str(e)}"

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check for tool/method availability and mandate confirmation before execution, as per GEPA policy."
    )
    parser.add_argument("tool_name", type=str, help="The name of the tool to check.")
    args = parser.parse_args()
    
    validation_result = check_tool_availability(args.tool_name)
    
    # Print the JSON result, which contains the explicit execution permission flag
    print(json.dumps(validation_result, indent=2))

