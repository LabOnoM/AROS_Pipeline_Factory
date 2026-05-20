# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import argparse
import json
import sys
import time
import requests

def check_api_availability(url, timeout):
    """
    Checks the availability of an API endpoint.

    Args:
        url (str): The URL of the API endpoint to check.
        timeout (int): The timeout in seconds for the request.

    Returns:
        dict: A dictionary containing the status of the check.
    """
    result = {
        "url": url,
        "status": "unavailable",
        "status_code": None,
        "reason": None,
        "response_time_ms": None
    }

    start_time = time.perf_counter()

    try:
        # Using a HEAD request is more lightweight as we only need the status
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        result["status_code"] = response.status_code

        if 200 <= response.status_code < 300:
            result["status"] = "available"
            result["reason"] = response.reason
        else:
            result["status"] = "unavailable"
            result["reason"] = f"HTTP status code {response.status_code} indicates an issue: {response.reason}"

    except requests.exceptions.Timeout:
        result["status"] = "timeout"
        result["reason"] = f"The request timed out after {timeout} seconds."
    except requests.exceptions.RequestException as e:
        result["status"] = "unavailable"
        result["reason"] = f"A connection error occurred: {e}"
    
    end_time = time.perf_counter()
    result["response_time_ms"] = round((end_time - start_time) * 1000)

    return result

def main():
    """
    Main function to parse arguments and run the API availability check.
    """
    parser = argparse.ArgumentParser(description="Check the availability of an external API endpoint.")
    parser.add_argument("--url", required=True, help="The URL of the API endpoint to check.")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout for the request in seconds. Default is 10.")
    args = parser.parse_args()

    status = check_api_availability(args.url, args.timeout)
    print(json.dumps(status, indent=2))

if __name__ == "__main__":
    main()
