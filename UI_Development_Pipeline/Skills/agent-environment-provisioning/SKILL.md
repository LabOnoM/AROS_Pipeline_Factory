---name: agent-environment-provisioning
description: "A policy that mandates pre-task environmental and capability checks to prevent execution errors. Governs filesystem, shell, and network prerequisites."
license: MIT
skill-author: AROS-Mutation-Sweeper

# Agent Environment Provisioning Policy

This skill defines the mandatory pre-flight checks an agent must perform after receiving a task but before beginning execution. Its purpose is to prevent common runtime errors by validating environmental dependencies ahead of time.

## GEPA Error Prevention Rule: Pre-Task Capability Validation

**An agent MUST NOT attempt to execute a task without first validating its capability to meet the task's explicit environmental requirements.**

This validation includes, but is not limited to, filesystem access, shell command availability, and network connectivity. If any check fails, the agent MUST immediately halt and report the specific reason for failure, citing this policy. This is a critical step in preventing common `FileNotFoundError`, `PermissionError`, and `command not found` failures.

---

## MANDATORY SKILL INSTRUCTIONS:

### Pre-Execution Workflow

1.  **Parse Requirements:** Analyze the assigned task's text and metadata to identify all required:
    *   **File Paths:** Any paths for reading, writing, or listing.
    *   **Shell Commands:** Any external binaries required (e.g., `git`, `python`, `curl`, `jq`).
    *   **HTTP Endpoints:** Any URLs that need to be accessed.

2.  **Execute Capability Checks:** Perform the following validations using available tools. These checks must be explicit and must halt execution upon failure.

    *   **Filesystem Access Validation:**
        *   To prevent `FileNotFoundError` or `PermissionError`, an agent MUST validate file and directory access.
        *   **Read Access:** For any file that must be read, verify its existence and readability using `test -r`.
          ```bash
          # Example: Check if a critical KI file is readable
          if ! test -r "/mnt/Disk1/AntigravityInit/antigravity/knowledge/some_ki/artifact.txt"; then
            echo "Pre-flight check failed: Cannot read required file /mnt/Disk1/AntigravityInit/antigravity/knowledge/some_ki/artifact.txt"
            # Halt execution and report failure
          fi
          ```
        *   **Write Access:** For any file that must be written, verify the parent directory exists and is writable using `test -w`.
          ```bash
          # Example: Check if the skills directory is writable before creating a new skill
          SKILL_DIR="~/.gemini/skills/new-skill-name/"
          if ! test -d "$(dirname "$SKILL_DIR")" || ! test -w "$(dirname "$SKILL_DIR")"; then
            echo "Pre-flight check failed: The directory $(dirname "$SKILL_DIR") does not exist or is not writable."
            # Halt execution and report failure
          fi
          ```

    *   **Shell Command Availability Val