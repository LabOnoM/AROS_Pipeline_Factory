---
name: system_command_environmental_pre_check
description: "A policy that mandates pre-execution checks for system-level commands, especially for GUI applications, to ensure the environment is capable of running them."
license: MIT
skill-author: AROS-Core
---

# System Command Environmental Pre-Check Policy

This skill defines the mandatory pre-flight checks an agent must perform before executing system-level commands that may have specific environmental dependencies, such as a graphical user interface (GUI).

## GEPA Error Prevention Rule: GUI Capability Validation

**An agent MUST NOT attempt to execute a command identified as a graphical user interface (GUI) utility without first verifying the presence of a valid graphical session (e.g., X11 or Wayland).**

This policy prevents common runtime errors where a command fails because it was invoked in an environment that cannot support its graphical requirements (e.g., a headless server or an SSH session without X11 forwarding).

---

## MANDATORY SKILL INSTRUCTIONS:

### Pre-Execution Workflow

1.  **Identify Command Type:** Before executing any system command, determine if it is likely to require a graphical interface. While a perfect list is impossible, agents MUST check against a list of common GUI utilities.

    *   **Examples of GUI Commands:** `gedit`, `gimp`, `nautilus`, `firefox`, `gnome-terminal`, `kate`, `docker-desktop`.
    *   **Examples of CLI Commands:** `ls`, `grep`, `curl`, `docker`, `git`, `python`.

2.  **Execute GUI Environment Check (If Applicable):** If the command is identified as a GUI utility, the agent MUST perform the following shell check to verify a display is available.

    ```bash
    if [ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ]; then
      echo "GEPA FAIL: Cannot execute GUI command. No active display session found. Neither \$DISPLAY nor \$WAYLAND_DISPLAY is set."
      exit 1
    else
      echo "GEPA SUCCESS: Display session found. Proceeding with command."
      exit 0
    fi
    ```

3.  **Report or Proceed:**

    *   **On Success:** If the check passes (or is not required for a CLI tool), proceed with command execution.
    *   **On Failure:** If the GUI check fails, halt execution. Use the `agent-communication` skill to formulate a precise error message.
        *   **Example:** "I cannot complete this task because the pre-task capability check failed: The command 'nautilus' requires a graphical display, but the execution environment has neither `$DISPLAY` nor `$WAYLAND_DISPLAY` set."
