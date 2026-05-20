---
name: content-completeness-validator
description: Validates text content to ensure it is not truncated or incomplete. Checks for terminal punctuation, balanced brackets/quotes, and abrupt mid-sentence endings.
license: MIT
skill-author: AROS-Mutation-Sweeper
---

## When to Use

- Use this skill as a pre-validation step before committing generated text content (KIs, policies, skills) to the filesystem.
- Integrate this into workflows that generate prose or structured text to prevent common truncation errors.
- Use as a quality gate to ensure that AI-generated content meets a minimum standard of completeness.

## Key Features

- **Terminal Punctuation Check:** Verifies that the text ends with a standard terminal punctuation mark ('.', '!', '?').
- **Balanced Delimiters Check:** Ensures that all brackets '()', '[]', '{}' and quotes '""', "''" are properly opened and closed.
- **Abrupt Ending Detection:** Identifies content that likely ends mid-sentence (e.g., ending with 'and', 'because', or a trailing comma).

## Dependencies
- Python 3.x for script execution.

## Instructions
1. Save the content to be validated to a temporary file (e.g., `/tmp/content_to_validate.txt`).
2. Run the validator script:
   ```bash
   python ~/.gemini/skills/content-completeness-validator/validator.py "/tmp/content_to_validate.txt"
   ```
3. The script will exit with code 0 if the content is valid and a non-zero exit code if it fails. The script will print a JSON object with the validation results.

## Example Usage

### Input (saved to /tmp/content_to_validate.txt)
```
This is a complete sentence.
```

### Script Execution & Output
```bash
python ~/.gemini/skills/content-completeness-validator/validator.py "/tmp/content_to_validate.txt"
```
```json
{
  "passed": true,
  "checks": {
    "terminal_punctuation": {
      "passed": true,
      "details": "Content ends with a valid terminal punctuation mark."
    },
    "balanced_delimiters": {
      "passed": true,
      "details": "All brackets and quotes are balanced."
    },
    "abrupt_ending": {
      "passed": true,
      "details": "Content does not appear to end abruptly."
    }
  }
}
```

### Failing Example (saved to /tmp/content_to_validate.txt)
```
This sentence is not
```

### Script Execution & Output
```json
{
  "passed": false,
  "checks": {
    "terminal_punctuation": {
      "passed": false,
      "details": "Content is missing a terminal punctuation mark."
    },
    "balanced_delimiters": {
      "passed": true,
      "details": "All brackets and quotes are balanced."
    },
    "abrupt_ending": {
      "passed": false,
      "details": "Content ends with a connecting word ('not'), suggesting it is incomplete."
    }
  }
}
```