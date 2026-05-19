---
description: The single, gated, transactional workflow to safely apply, validate, and commit file changes.
---

# Gated File Commit Workflow (`/lab-commit`)

// turbo-all

> **WARNING: FUNDAMENTAL SYSTEM CONSTRAINT**
>
> All agents operate in a strict I/O sandbox. **YOU CANNOT WRITE TO FILES.** Any plan that includes a direct `modify`, `edit`, `write`, `sed -i`, or `echo >` command will be rejected. This workflow is the **ONLY** sanctioned method for persisting changes.

---
## 1. Mandatory Usage Pattern

To modify any file, your plan **MUST** follow this exact three-task structure. Do not attempt to combine these steps.

### **✅ Required Plan Structure (Copy & Adapt This Template)**

```yaml
# -------------------- ✅ REQUIRED PLAN TEMPLATE ✅ --------------------
# GOAL: [Your goal to modify a file]
#
# - task_id: read_original_content
#   description: Read the current content of the target file to ensure the update is based on the latest version.
#   command: cat path/to/your/target_file.md
#
# - task_id: generate_updated_artifact
#   description: Generate the complete, new version of the file and save it to a temporary artifact. The artifact MUST contain the full desired file content.
#   command: <your_content_generation_logic> > ./artifacts/updated_content.md
#   dependencies: [read_original_content]
#
# - task_id: delegate_commit_to_workflow
#   description: Delegate the file writing operation to the sanctioned /lab-commit workflow for validation and safe application.
#   command: /lab-commit --target="path/to/your/target_file.md" --content_artifact="./artifacts/updated_content.md" --force
#   dependencies: [generate_updated_artifact]
# --------------------------------------------------------------------
```

---
## 2. Flags & Automation

This workflow can operate in two modes: interactive (default) or forced (for automation).

*   `--target="<path>"`: (Required) The path to the existing file you want to overwrite.
*   `--content_artifact="<path>"`: (Required) The path to the artifact file containing the new content.
*   `--force`: (Optional) Skips the interactive `diff` review and confirmation prompt. Use this flag for fully automated workflows where no human user is present to provide confirmation. **If this flag is omitted, the workflow will HALT and wait for user input.**

---
## 3. Internal Agent Logic (for `/lab-commit` agent only)

Your execution begins *after* another agent has invoked you with the required arguments.

### **Phase 1: Validation Gates**

1.  **Argument Parsing:**
    - Parse `--target`, `--content_artifact`, and `--force` flags.

2.  **Invocation Check:** Verify the command includes both `--target` and `--content_artifact`.
    - **HALT:** If missing, fail with error: "Commit Aborted: Invalid request. Both --target and --content_artifact arguments are mandatory."

3.  **Artifact Check:** Verify the content artifact file exists and is not empty (`test -s "$content_artifact"`).
    - **HALT:** If missing or empty, fail with error: "Commit Aborted: The content artifact '$content_artifact' is missing or empty."

4.  **Target Check:** Verify the target file exists (`test -f "$target"`). This workflow only modifies existing files.
    - **HALT:** If it does not exist, fail with error: "Commit Aborted: The target file '$target' does not exist. Use a file creation workflow instead."

4.5 **Pointer Tag Check (Advisory — Boy Scout Rule):**
    - If the target file has a `.py`, `.ts`, `.js`, or `.tsx` extension:
      - Check whether the file contains `AROS SPEC:` or `BDD Feature:` in its first 10 lines.
      - If MISSING: Log a **WARNING** (not a HALT): "Advisory: File '$target' is missing Pointer Tag headers (AROS SPEC / BDD Feature). Per the Boy Scout Rule, consider adding them while you are modifying this file."
    - This check is advisory-only and MUST NOT block the commit. It serves as a nudge for agents to maintain traceability. Urgent hotfixes MUST be able to proceed without Pointer Tags.

### **Phase 2: Confirmation & Execution**

5.  **Difference Analysis (HITL or Force Gate):**
    - **If `--force` is NOT provided:**
        - **Action:** Perform a `diff -u "$target" "$content_artifact"` to show proposed changes.
        - **Gate:** Report the `diff` output and HALT, awaiting explicit user confirmation. State clearly: "PROPOSED CHANGES for `$target` are shown above. Apply these changes? Respond with `confirm` to proceed or `abort` to cancel."
    - **If `--force` IS provided:**
        - **Action:** Log a message: "Skipping interactive confirmation due to --force flag."

6.  **Apply Change:** Upon receiving `confirm` or if `--force` was used, overwrite the target file.
    - **Command:** `cp "$content_artifact" "$target"`

7.  **Verify Staging:** Run `git status` to confirm the change is detected.
    - **HALT:** If `$target` is not listed as modified, fail with error: "Commit Failed: I/O error or no changes detected. The file on disk was not modified."

8.  **Commit with Rollback:** Stage changes and commit with a standardized message. The command is wrapped to ensure any commit failure triggers an immediate rollback.
    ```bash
    git add . && git commit -m "[System] [Workflow] [$(date +'%Y-%m-%d')] Applying changes via /lab-commit" || {
      echo "CRITICAL: COMMIT FAILED. Rolling back changes to prevent repository corruption." >&2
      git reset --hard HEAD
      exit 1 # Halt with a non-zero exit code
    }
    ```

### **Phase 3: Finalization**

9.  **Post-Commit Hook:** Run the symlink failsafe for repository tooling.
    - **Command:** `ln -sfn .wiki Wiki`

10. **Final Report:** Announce completion.
    - **Message:** "Commit successful. The changes to `$target` have been applied and committed."