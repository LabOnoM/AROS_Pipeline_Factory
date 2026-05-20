# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import json
import sys
import argparse

# Heuristics for detecting incomplete sentences.
# This list can be expanded based on observed failure modes.
ABRUPT_ENDING_WORDS = [
    'and', 'or', 'but', 'so', 'because', 'while', 'if', 'although', 'though',
    'as', 'of', 'for', 'with', 'the', 'is', 'in', 'on', 'at', 'a', 'an', 'not'
]

def check_terminal_punctuation(content):
    """Checks if the content ends with a standard terminal punctuation mark."""
    stripped_content = content.strip()
    if not stripped_content:
        return {
            "passed": False,
            "details": "Content is empty."
        }
    if stripped_content.endswith(('.', '!', '?', '}', ']', ')', '\"', '\'')):
        # Check if the very last character is punctuation, allowing for closing delimiters.
        last_char = stripped_content[-1]
        if last_char in ['.', '!', '?']:
             return {
                "passed": True,
                "details": "Content ends with a valid terminal punctuation mark."
            }
        # Handle cases like `(some sentence.)`
        if last_char in ['}', ']', ')', '\"', '\''] and stripped_content.rstrip(')}]\"\'').endswith(('.', '!', '?')):
             return {
                "passed": True,
                "details": "Content ends with a valid terminal punctuation mark before closing delimiters."
            }


    return {
        "passed": False,
        "details": "Content is missing a terminal punctuation mark."
    }

def check_balanced_delimiters(content):
    """Ensures that all brackets and quotes are properly opened and closed."""
    stack = []
    pairs = {'(': ')', '[': ']', '{': '}'}
    quotes = {'"': 0, "'": 0}

    for char in content:
        if char in pairs.keys():
            stack.append(char)
        elif char in pairs.values():
            if not stack or pairs[stack.pop()] != char:
                return {
                    "passed": False,
                    "details": f"Mismatched or unopened closing delimiter: {char}"
                }
        elif char in quotes:
            quotes[char] += 1

    if stack:
        return {
            "passed": False,
            "details": f"Unclosed opening delimiter(s) remain: {stack}"
        }

    for q, count in quotes.items():
        if count % 2 != 0:
            return {
                "passed": False,
                "details": f"Unclosed quote: {q}"
            }

    return {
        "passed": True,
        "details": "All brackets and quotes are balanced."
    }


def check_abrupt_ending(content):
    """Identifies content that likely ends mid-sentence."""
    stripped_content = content.strip().rstrip('.,!?')
    if not stripped_content:
        return {
            "passed": False,
            "details": "Content is empty or contains only punctuation."
        }
    last_word = stripped_content.split()[-1].lower()

    if last_word in ABRUPT_ENDING_WORDS:
        return {
            "passed": False,
            "details": f"Content ends with a connecting word ('{last_word}'), suggesting it is incomplete."
        }
    if stripped_content.endswith(','):
        return {
            "passed": False,
            "details": "Content ends with a comma, suggesting it is incomplete."
        }

    return {
        "passed": True,
        "details": "Content does not appear to end abruptly."
    }


def main():
    """Main function to run the content completeness validation."""
    parser = argparse.ArgumentParser(description="Validate text content for completeness.")
    parser.add_argument("filepath", type=str, help="The path to the text file to validate.")
    args = parser.parse_args()

    try:
        with open(args.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(json.dumps({
            "passed": False,
            "error": f"File not found: {args.filepath}"
        }, indent=2))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "passed": False,
            "error": f"Failed to read file: {e}"
        }, indent=2))
        sys.exit(1)

    results = {
        "terminal_punctuation": check_terminal_punctuation(content),
        "balanced_delimiters": check_balanced_delimiters(content),
        "abrupt_ending": check_abrupt_ending(content)
    }

    overall_passed = all(check["passed"] for check in results.values())

    final_output = {
        "passed": overall_passed,
        "checks": results
    }

    print(json.dumps(final_output, indent=2))

    if not overall_passed:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
