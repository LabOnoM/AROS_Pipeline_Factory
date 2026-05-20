# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import os
import json
import csv
import argparse
import sys

def check_file(filepath):
    """
    Validates a single file for existence, accessibility, and integrity.
    """
    results = {
        'filepath': filepath,
        'exists': False,
        'accessible': False,
        'integrity': {
            'non_empty': False,
            'format_valid': None, # Can be True, False, or 'skipped'
            'error': None
        }
    }

    # 1. Existence Check
    if not os.path.exists(filepath):
        results['integrity']['error'] = "File does not exist."
        return results
    results['exists'] = True

    # 2. Accessibility Check
    if not os.access(filepath, os.R_OK):
        results['integrity']['error'] = "File is not accessible for reading."
        return results
    results['accessible'] = True

    # 3. Integrity Check: File size
    try:
        if os.path.getsize(filepath) > 0:
            results['integrity']['non_empty'] = True
        else:
            results['integrity']['error'] = "File is empty."
            return results
    except OSError as e:
        results['integrity']['error'] = f"Could not get file size: {e}"
        return results


    # 4. Integrity Check: File format (JSON, CSV)
    file_ext = os.path.splitext(filepath)[1].lower()

    if file_ext == '.json':
        try:
            with open(filepath, 'r') as f:
                json.load(f)
            results['integrity']['format_valid'] = True
        except json.JSONDecodeError as e:
            results['integrity']['format_valid'] = False
            results['integrity']['error'] = f"Invalid JSON format: {e}"
        except Exception as e:
            results['integrity']['format_valid'] = False
            results['integrity']['error'] = f"Error reading JSON file: {e}"

    elif file_ext == '.csv':
        try:
            with open(filepath, 'r', newline='') as f:
                # Try to read the first row to check structure
                reader = csv.reader(f)
                next(reader)
            results['integrity']['format_valid'] = True
        except StopIteration: # File is empty, but we already checked for size > 0
             results['integrity']['format_valid'] = True # CSV with only a header is valid
        except csv.Error as e:
            results['integrity']['format_valid'] = False
            results['integrity']['error'] = f"Invalid CSV format: {e}"
        except Exception as e:
            results['integrity']['format_valid'] = False
            results['integrity']['error'] = f"Error reading CSV file: {e}"
    else:
        results['integrity']['format_valid'] = 'skipped' # Not a supported format for deep validation

    return results

def main():
    parser = argparse.ArgumentParser(
        description="""
        Performs a pre-check on dependent task input files.
        Validates existence, read accessibility, and basic integrity (non-empty, valid JSON/CSV).
        """
    )
    parser.add_argument(
        'files',
        metavar='FILE',
        type=str,
        nargs='+',
        help='One or more file paths to validate.'
    )
    parser.add_argument(
        '--json-output',
        action='store_true',
        help='Output the results in JSON format.'
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    all_results = [check_file(f) for f in args.files]
    overall_success = all(
        r['exists'] and r['accessible'] and r['integrity']['non_empty'] and r['integrity']['format_valid'] != False
        for r in all_results
    )

    output = {
        'overall_passed': overall_success,
        'results': all_results
    }

    if args.json_output:
        print(json.dumps(output, indent=2))
    else:
        for res in output['results']:
            status = "PASSED" if res['exists'] and res['accessible'] and res['integrity']['non_empty'] and res['integrity']['format_valid'] != False else "FAILED"
            print(f"[{status}] {res['filepath']}")
            if status == "FAILED":
                print(f"  - Reason: {res['integrity']['error']}")


if __name__ == '__main__':
    main()
