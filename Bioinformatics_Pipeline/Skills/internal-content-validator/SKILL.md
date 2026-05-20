---
name: internal-content-validator
description: Validates drafted content for structural integrity, including YAML frontmatter and operational context, before external GTB validation.
license: MIT
skill-author: AROS
---
# Internal Content Validator Skill

This skill provides a preliminary check on drafted AROS components (Skills, Policies, KIs) to ensure they meet the basic structural requirements of the system. It is designed to be run *before* the `gtb-validator` to catch common structural errors early.

## Prerequisites
- Python 3.8+
- `pyyaml` package must be installed.
```bash
pip install pyyaml
```

## When to Use
Use this skill after drafting a new Skill, Policy, or KI but before submitting it for the more intensive Golden Test Battery (GTB) validation. This skill helps identify and fix common structural deficiencies quickly.

## Checks Performed
1.  **YAML Frontmatter:**
    *   Verifies the presence of a `---` delimited YAML frontmatter block.
    *   Ensures the frontmatter contains the required keys: `name` (or `title`), `description`, and `skill-author`.
2.  **Operational Context:**
    *   Checks that the document contains at least one standard operational context section to ensure usability.
    *   Required sections (at least one must be present): `## Workflow`, `## Instructions`, `## When to Use`, `## Core Capabilities`, or `## Example Usage`.

## Instructions

1.  Save your drafted markdown content to a temporary file (e.g., `/tmp/draft.md`).
2.  Run the validation script from the command line, passing the path to your draft file as an argument:
    ```bash
    python /home/owner03/.gemini/skills/internal-content-validator/validate_internal.py "/tmp/draft.md"
    ```
3.  Review the JSON output.
    *   If `"passed": true`, the draft meets the basic structural requirements and you can proceed to the `gtb-validator`.
    *   If `"passed": false`, read the `"reasoning"` array to understand the specific structural deficiencies. You MUST correct these issues before proceeding.

## Example Output (Failure)
```json
{
  "passed": false,
  "reasoning": [
    "Missing or empty required YAML frontmatter key: 'skill-author'.",
    "Missing operational context. Document must contain at least one of the following sections: ## Workflow, ## Instructions, ## When to Use, ## Core Capabilities, ## Example Usage."
  ]
}
```
