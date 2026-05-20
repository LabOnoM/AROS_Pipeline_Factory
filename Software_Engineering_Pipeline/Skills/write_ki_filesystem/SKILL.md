---
name: write_ki_filesystem
description: Finalizes the KI creation process by writing a validated draft KI to the permanent knowledge base. This skill strictly enforces the ki-creation-protocol by ensuring GTB validation has passed before committing the file.
license: MIT
skill-author: AROS_code_generator
---

# Write KI to Filesystem

This skill is the final, gated step in the Knowledge Item (KI) creation workflow. It is responsible for moving a validated KI draft from a temporary location to its permanent destination in the AROS knowledge base.

## Core Function

This skill acts as a gatekeeper. It programmatically enforces the `ki-creation-protocol` and the `finalization-prerequisite-check` policy. It will only write a KI to the filesystem if it receives explicit confirmation that the KI draft has passed the Golden Test Battery (GTB) validation.

## When to Use

- **ONLY** use this skill as the final action in a KI creation workflow.
- It MUST be preceded by the `gtb-validator` skill.
- The `--validation-passed` flag MUST be set based on the output of the `gtb-validator`.

## Workflow Logic

1.  A KI is drafted to `/tmp/draft_ki.md` by a skill like `knowledge-synthesizer`.
2.  The `gtb-validator` is run on `/tmp/draft_ki.md`.
3.  Based on the validator's output (`"passed": true`), this skill is invoked.
4.  **If `validation_passed` is `true`**: The skill creates the necessary KI directory and copies the draft from `/tmp/draft_ki.md` to its final destination at `~/.gemini/antigravity/knowledge/<ki_name>/<ki_name>.md`.
5.  **If `validation_passed` is `false`**: The skill prints an error message to stderr, does **NOT** write the file, and exits with a non-zero status code to halt the workflow. This prevents unvalidated or low-quality content from being saved.

## Example Invocation

```bash
# Given that gtb-validator returned "passed": true for /tmp/draft_ki.md

# This command will succeed
python ~/.gemini/skills/write_ki_filesystem/scripts/main.py \
  --ki-name "example-new-ki" \
  --validation-passed true

# This command will fail and prevent the file from being written
python ~/.gemini/skills/write_ki_filesystem/scripts/main.py \
  --ki-name "example-new-ki" \
  --validation-passed false
```
