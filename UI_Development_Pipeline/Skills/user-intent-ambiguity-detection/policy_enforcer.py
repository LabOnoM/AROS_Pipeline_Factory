# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

#!/usr/bin/env python3
import re
import json

def extract_key_terms(prompt: str) -> list[str]:
    """
    Extracts key terms from a user prompt based on the GEPA policy.

    Key terms are identified as:
    1.  Strings enclosed in single or double quotes.
    2.  Capitalized phrases (e.g., 'Automated Discovery', 'Systematic Review').

    Args:
        prompt: The user's input prompt.

    Returns:
        A list of unique key terms found in the prompt.
    """
    # 1. Extract terms in double or single quotes
    quoted_terms = re.findall(r'"([^"]+)"|\'([^\']+)\'', prompt)
    # The regex returns a list of tuples, so we flatten it
    flat_quoted = [item for sublist in quoted_terms for item in sublist if item]

    # 2. Extract capitalized phrases of one or more words
    # This regex looks for sequences of words starting with a capital letter.
    capitalized_phrases = re.findall(r'\b(?:[A-Z][a-z\d]+(?:\s+|$))+', prompt)

    # Clean up trailing whitespace and filter out common words that might be
    # capitalized at the beginning of a sentence.
    common_sentence_starters = {
        'The', 'What', 'How', 'Why', 'When', 'Where', 'Is', 'A', 'An',
        'Please', 'Can', 'Could', 'Show', 'Tell', 'Me'
    }
    cleaned_capitalized = [
        p.strip() for p in capitalized_phrases
        if p.strip() not in common_sentence_starters
    ]

    # Combine all found terms and deduplicate while preserving order
    all_terms = list(dict.fromkeys(flat_quoted + cleaned_capitalized))

    return all_terms

def enforce_query_term_inclusion(prompt: str, response: str) -> dict:
    """
    Enforces the GEPA 'Query Term Inclusion Policy'.

    It checks if the key terms extracted from the prompt are present in the
    agent's response.

    Args:
        prompt: The user's input prompt.
        response: The agent's generated response.

    Returns:
        A dictionary containing the compliance status and details.
    """
    key_terms = extract_key_terms(prompt)

    if not key_terms:
        return {
            "compliant": True,
            "reason": "Policy PASSED. No specific key terms were identified in the prompt.",
            "terms_checked": []
        }

    missing_terms = []
    response_lower = response.lower()

    for term in key_terms:
        # Perform a case-insensitive check
        if term.lower() not in response_lower:
            missing_terms.append(term)

    if not missing_terms:
        return {
            "compliant": True,
            "reason": f"Policy PASSED. All identified key terms were included in the response.",
            "terms_checked": key_terms
        }
    else:
        return {
            "compliant": False,
            "reason": f"Policy FAILED. The response omitted the following required terms from the prompt: {missing_terms}",
            "terms_checked": key_terms,
            "missing_terms": missing_terms
        }

if __name__ == '__main__':
    # Example Usage
    example_prompt_pass = "Please create a 'Bioinformatics Pipeline' for 'Automated Discovery' using the 'Distiller' component."
    example_response_pass = "Certainly. Here is a 'Bioinformatics Pipeline' that leverages the 'Distiller' component for the specific purpose of 'Automated Discovery'."

    example_prompt_fail = "Compare methods for 'Automated Discovery' in genomics."
    example_response_fail = "There are many ways to find new things in genomic data. One common method is differential gene expression analysis."

    # --- Test Cases ---
    print("--- Running Test Cases for GEPA Policy Enforcement ---")

    # Test Case 1: Success
    print("\n[Test Case 1: Should Pass]")
    print(f"Prompt: {example_prompt_pass}")
    print(f"Response: {example_response_pass}")
    result_pass = enforce_query_term_inclusion(example_prompt_pass, example_response_pass)
    print(f"Result: {json.dumps(result_pass, indent=2)}")
    assert result_pass["compliant"] is True

    # Test Case 2: Failure
    print("\n[Test Case 2: Should Fail]")
    print(f"Prompt: {example_prompt_fail}")
    print(f"Response: {example_response_fail}")
    result_fail = enforce_query_term_inclusion(example_prompt_fail, example_response_fail)
    print(f"Result: {json.dumps(result_fail, indent=2)}")
    assert result_fail["compliant"] is False
    assert "Automated Discovery" in result_fail["missing_terms"]

    # Test Case 3: No Key Terms
    print("\n[Test Case 3: No Key Terms, Should Pass]")
    prompt_no_terms = "What is the weather today?"
    response_no_terms = "It is sunny."
    print(f"Prompt: {prompt_no_terms}")
    print(f"Response: {response_no_terms}")
    result_no_terms = enforce_query_term_inclusion(prompt_no_terms, response_no_terms)
    print(f"Result: {json.dumps(result_no_terms, indent=2)}")
    assert result_no_terms["compliant"] is True

    print("\n--- All test cases completed. ---")

