---
name: meta-protocol-writer
description: Generates a PROSPERO-compliant Meta-analysis protocol based on Title and PICOS. Use when the user wants to write a protocol for a systematic review or meta-analysis.
license: MIT
skill-author: AIPOCH
version: 2.0
---
# Meta Protocol Writer

This skill helps users generate a standard protocol for PROSPERO registration (without the registration number) for a Meta-analysis or Systematic Review.

## When to Use

- Use this skill when you need to generate a PROSPERO-compliant meta-analysis protocol based on title and PICOS.
- Use this skill when a protocol design task needs a packaged method instead of ad-hoc freeform output.
- Use this skill when the user expects a concrete deliverable, validation step, or file-based result.

## MANDATORY SKILL INSTRUCTIONS

This skill is subject to the `content-drafting-capability` and `agent-communication` policies.

### Policy V2.0 Update: Robust Execution
All actions, especially those involving file system operations or external script execution, MUST be wrapped in error handling blocks. Before any destructive action (like writing or moving a file), a final confirmation from the user is required.

#### 1. Error Handling
Every external command execution MUST be checked for a successful exit code. If a command fails, the agent MUST halt the workflow and report the specific error and command that failed, as per the `agent-communication` policy.

```bash
# Example of robust command execution
COMMAND="python /home/owner03/.gemini/skills/gtb-validator/validate.py \"/tmp/draft_protocol.md\" \"knowledge_retrieval\""
if ! output=$(eval $COMMAND); then
    echo "Error: The validation command failed to execute."
    echo "Command: $COMMAND"
    # Adhere to agent-communication policy by providing a reason for failure
    # EXIT and report failure to the user.
else
    # Check the JSON output for "passed": true
    echo "$output"
fi
```

#### 2. Confirmation Before Destructive Actions
Before writing the final file to the user-specified destination, you MUST ask for final confirmation. This prevents accidental overwrites.

```bash
# Example Confirmation
echo "The protocol has passed all validation checks."
read -p "I am ready to write the final protocol to </path/to/user/destination.md>. Shall I proceed? [y/N] " response
if [[ ! "$response" =~ ^[yY]$ ]]; then
    echo "Aborted. The final file was not written."
    # EXIT and report cancellation to the user.
fi
# Proceed with file write operation...
```

### Safety Gate: Unsafe Path Validation
Before writing the final protocol or any temporary file, you MUST validate the output file path.
- Resolve the absolute path of the target directory.
- Check if the resolved path is in the protected directories list: `/`, `/etc`, `/usr`, `/var`, `/root`.
- If the path is unsafe, the operation MUST be blocked, and you must report an error to the user, citing this policy.

### GEPA Quality Gate: GTB Validation
The generated protocol MUST pass the Golden Test Battery (GTB) validation before being finalized. The execution of the validator MUST follow the robust execution policy.

## Workflow

Follow these steps to generate the protocol.

### 1. Gather and Validate Inputs
(No change from previous version - Title and PICOS validation)

### 2. User Confirmation for Inputs
(No change from previous version - Confirm Title and PICOS)
Example: "I will now generate a meta-analysis protocol with the following details: [Summarize Title and PICOS]. Shall I proceed?"

### 3. Generate Protocol Sections
(No change from previous version - Use `references/prompts.md` for generation)

### 4. Validation and Final Output

1.  **Combine Sections**: Combine the generated sections into a single Markdown document.
2.  **Save to Temporary File**: Write the complete protocol to `/tmp/draft_protocol.md`. Handle potential write errors.
3.  **Perform GTB Validation**: Run the `gtb-validator` as described in the "Robust Execution" policy. If the script fails to run or if validation returns `"passed": false`, you must handle the error. For a validation failure, analyze the `reasoning` and loop back to Step 3 to regenerate the failing sections.
4.  **Final Confirmation**: Once validation passes, inform the user and request final confirmation before writing the file, as per the "Confirmation Before Destructive Actions" policy.
5.  **Finalize**: Upon confirmation, move the file from `/tmp/draft_protocol.md` to the user's desired final location. Verify the move was successful and report the final path to the user.
