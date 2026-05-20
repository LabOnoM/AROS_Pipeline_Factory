# Knowledge Item Authoring Standard

## Summary

This document defines the mandatory, programmatically verifiable completeness criteria for all new Knowledge Items (KIs) created within the AROS ecosystem. Adherence to this standard ensures that all KIs are robust, complete, and useful, in accordance with the GEPA error prevention and quality assurance policies.

## Key Concepts

To be considered complete and valid, every new KI must satisfy the following structural and content requirements. These criteria are designed to be checkable by an automated validation script.

### 1. File Format and Naming
- **Format**: All KIs must be written in Markdown. The primary content file should have an `.md` extension.
- **Directory**: Each KI must reside in its own subdirectory within `~/.gemini/antigravity/knowledge/`.
- **Example**: `~/.gemini/antigravity/knowledge/my-new-ki/my-new-ki.md`

### 2. Minimum Content Length
- **Requirement**: The Markdown content of the KI must have a minimum length of **250 characters** (excluding whitespace and Markdown syntax).
- **Reasoning**: This prevents the creation of empty, stub, or trivial KIs that provide no value.

### 3. Prohibited Placeholders
- **Requirement**: The content must be final and complete. It must NOT contain any of the following development placeholders:
  - `TODO`
  - `FIXME`
  - `implement here`
  - `...` (as a placeholder, not punctuation)
  - `your logic here`
  - `to be implemented`
- **Reasoning**: These placeholders indicate incomplete work and are not permissible in the permanent knowledge base.

### 4. Mandatory Markdown Sections
- **Requirement**: The KI Markdown file must contain the following H2 (`##`) headers, in any order:
  - `## Summary`: A concise (1-3 sentence) overview of the KI's purpose and content.
  - `## Key Concepts`: The main body of the KI, detailing the specific knowledge, concepts, or procedures.
  - `## Validation`: A clear, explicit description of the steps an agent or user can take to verify the accuracy and correctness of the information presented. This could involve running a command, checking a file, or querying an API.
- **Reasoning**: This standardized structure ensures that KIs are easy to parse, understand, and verify.

### 5. Content Integrity Checks
- **Requirement**: The KI content must pass basic linguistic completeness checks:
  - It must end with a valid terminal punctuation mark (`.`, `!`, `?`).
  - All brackets `()`, `[]`, `{}` and quotes `""`, `''` must be balanced (an equal number of opening and closing delimiters).
  - It must not end abruptly with a connecting word (e.g., `and`, `because`, `if`).
- **Reasoning**: This prevents truncated or syntactically incorrect content from being saved, which often happens due to generation errors.

### 6. Mandatory Metadata File
- **Requirement**: Each KI directory must contain a `metadata.json` file. This file must contain, at a minimum, the following keys:
  ```json
  {
    "ki_name": "unique-ki-name",
    "summary": "A brief, one-line description of the KI."
  }
  ```
- **Reasoning**: The metadata file provides essential, machine-readable information about the KI for indexing, searching, and management.

## Validation

To validate this standard itself:
1.  **Check File Path**: Confirm this file is located at `~/.gemini/antigravity/knowledge/ki-authoring-standard/ki-authoring-standard.md`.
2.  **Check Section Presence**: Verify that the headers `## Summary`, `## Key Concepts`, and `## Validation` are present in this document.
3.  **Check for Placeholders**: Scan this document's source to ensure no prohibited placeholders are used.
4.  **Run Content Completeness Validator**: Execute the `content-completeness-validator` skill on this file and confirm it passes.
5.  **Check for metadata.json**: Ensure a `metadata.json` file exists alongside this markdown file.
