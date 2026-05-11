---
description: The single, gated, transactional workflow to safely apply, validate, and commit file changes. This is the CANONICAL commit gateway for every workflow, especially after collecting new experimental data (qPCR run, Western blot, imaging session, etc.), ensuring a consistent commit format and index-update logic across the entire project. All other workflows MUST delegate their final commit step to this workflow instead of implementing inline `git add / git commit` commands, including specific logic for committing new experimental data to the local Git repository.
---

# Gated File Commit Workflow (`/lab-commit`)

// turbo-all

> **WARNING: FUNDAMENTAL SYSTEM CONSTRAINT**
>
> All agents operate in a strict I/O sandbox. **YOU CANNOT WRITE TO FILES DIRECTLY.** Any plan that includes a direct `modify`, `edit`, `write`, `sed -i`, or `echo >` command will be rejected. This workflow is the **ONLY** sanctioned method for persisting changes, whether for individual files or for Git repository updates.

---
## 1. Mandatory Usage Pattern for Other Agents (Single File Update)

To modify any single file, your plan **MUST** follow this exact three-task structure. Do not attempt to combine these steps. This pattern delegates the actual file writing to the `/lab-commit` workflow.

### **✅ Required Plan Template (Copy & Adapt This Template)**

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
## 2. Flags & Automation (for Single File Update Mode)

This mode of the workflow can operate in two sub-modes: interactive (default) or forced (for automation).

*   `--target="<path>"`: (Required) The path to the existing file you want to overwrite, or a new file to create.
*   `--content_artifact="<path>"`: (Required) The path to the artifact file containing the new content.
*   `--force`: (Optional) Skips the interactive `diff` review and confirmation prompt. Use this flag for fully automated workflows where no human user is present to provide confirmation. **If this flag is omitted, the workflow will HALT and wait for user input.**

---
## 3. Internal Agent Logic (for `/lab-commit` agent only)

Your execution begins *after* another agent has invoked you with the required arguments.

### **Phase 1: Invocation & Direct File Application Gates**

1.  **Argument Parsing:**
    - Parse `--target`, `--content_artifa