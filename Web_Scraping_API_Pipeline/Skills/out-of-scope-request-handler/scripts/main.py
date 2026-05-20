# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import argparse
import json

# A predefined dictionary mapping supported function names to their descriptions.
# This represents the "ground truth" of what the system can do.
SUPPORTED_FUNCTIONS = {
    "predict_reagent_depletion": "Predicts when lab reagents will run out based on historical usage.",
    "monitor_co2_tank": "Monitors CO2 tank pressure and predicts depletion to prevent outages.",
    "check_image_dpi": "Checks if an image or a folder of images meets 300 DPI printing standards.",
    "upscale_image": "Restores or upscales low-resolution images using AI super-resolution.",
    "send_notification": "Sends a user notification, with a fallback to a secondary method on failure.",
    "query_database": "Executes a read-only SQL query against the internal database."
}

def handle_request(request: str):
    """
    Checks if a user request maps to a supported function and returns a
    graceful fallback message if it does not.

    Args:
        request: The user's requested function or action.

    Returns:
        A JSON string containing the status and a message.
    """
    if request in SUPPORTED_FUNCTIONS:
        response = {
            "status": "success",
            "message": f"Request '{request}' is valid and is being processed.",
            "function_description": SUPPORTED_FUNCTIONS[request]
        }
    else:
        # If the request does not match, construct a helpful error message
        # that lists the available alternatives.
        alternatives = "\n".join([f"- {key}: {desc}" for key, desc in SUPPORTED_FUNCTIONS.items()])
        fallback_message = (
            f"Error: The requested function '{request}' is out of scope.\n\n"
            "This system is designed for a specific set of tasks. "
            "Please choose from the following supported functions:\n"
            f"{alternatives}"
        )
        response = {
            "status": "error",
            "message": fallback_message,
            "supported_functions": SUPPORTED_FUNCTIONS
        }

    return json.dumps(response, indent=2)

def main():
    """Main function to parse arguments and handle the request."""
    parser = argparse.ArgumentParser(
        description="Handles user requests and provides a graceful fallback for out-of-scope tasks."
    )
    parser.add_argument(
        "request",
        type=str,
        help="The user's requested function. For example, 'monitor_co2_tank'."
    )
    args = parser.parse_args()

    result = handle_request(args.request)
    print(result)

if __name__ == "__main__":
    main()
