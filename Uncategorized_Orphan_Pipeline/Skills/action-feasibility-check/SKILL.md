---
name: action-feasibility-check
description: Action Feasibility Check Skill
---

# Action Feasibility Check Skill

This skill evaluates a drafted Skill or KI against a set of feasibility rules before it is committed to the filesystem. It helps ensure that new components are complete, testable, and actionable.

## Instructions
1.  Save your drafted markdown or script to a temporary file, e.g., `/tmp/draft.md`.
2.  Run the python checker script against your draft:
    ```bash
    python ~/.gemini/skills/action-feasibility-check/scripts/check.py "/tmp/draft.md"
    ```
3.  Read the JSON output. If `"passed": true`, your draft meets the minimum feasibility requirements.
4.  If `"passed": false`, read the `"reasoning"` field and address the issues before committing the file.

## Feasibility Rules

### Rule 1: Mandatory Unit and Smoke Tests
For all developed skills and tools, rigorous unit and smoke tests MUST be implemented.
-   **Why**: This is to prevent regressions during GEPA mutations and ensure the long-term reliability and stability of the AROS ecosystem. Skills without tests are considered incomplete.
-   **Implementation**: Tests should be placed in a `tests/` subdirectory within the skill's directory (e.g., `~/.gemini/skills/your-new-skill/tests/`). The checker will verify the existence of this directory.

### Rule 2: Prohibited Placeholders
The check will FAIL if it finds any of the following placeholders in the content:
- `TODO`
- `FIXME`
- `implement here`
- `...`
- `your logic here`
- `to be implemented`

-   **Why**: These placeholders indicate incomplete or non-actionable instructions, which are not suitable for the AROS ecosystem.

### Rule 3: Mandatory Validation Section
For any skill or KI, the corresponding `SKILL.md` or `README.md` must include a "## Validation" section.
-   **Why**: This section must describe how to verify the output of the skill or the correctness of the knowledge. This ensures the validation process is repeatable.
-   **Implementation**: The checker will scan markdown files for the presence of a header with the exact text "Validation".
