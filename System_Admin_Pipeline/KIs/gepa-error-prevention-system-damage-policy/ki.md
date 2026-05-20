
# KI: GEPA Error Prevention for System Damage Policy

**Identifier:** `gepa-error-prevention-system-damage-policy`
**Version:** 1.0
**Status:** Proposal
**Author:** mutation_sweeper

## 1. Overview

This document defines the specific error prevention rules proposed under the Global Evolution & Policy Architecture (GEPA) to enhance the "Prevent Accidental System Damage" policy. The primary goal is to establish hard operational boundaries and explicitly block destructive file system and system-level actions that could compromise the integrity and stability of the AROS.

These rules are designed to be enforced by the core execution validation layer, preventing any agent from performing high-risk actions in protected zones without explicit, multi-layered override and confirmation.

## 2. Protected Operational Boundaries

The following paths are designated as **Protected Operational Boundaries**. Any automated action categorized as destructive is strictly forbidden within these paths and their subdirectories.

### 2.1. AROS Core Components

These paths contain the essential operating components of the AROS. Modification or deletion would lead to immediate functional degradation.

-   **AROS Root:** `[WORKSPACE_ROOT]/`
-   **Skills Directory:** `~/.gemini/skills/`
-   **Knowledge Items (KIs):** `~/.gemini/antigravity/knowledge/`
-   **Global Workflows:** `~/.gemini/antigravity/global_workflows/`
-   **Core Database:** `~/.gemini/antigravity/brain.db`
-   **System Logs:** `~/.gemini/antigravity/logs/`
-   **Dashboard Application:** `[WORKSPACE_ROOT]/antigravity-dashboard/`

### 2.2. Critical Host System Components

These are standard Linux system paths critical for the underlying host's operation. While AROS agents may need to read from them, write/delete operations are forbidden.

-   **/etc/** (System-wide configuration files)
-   **/boot/** (Bootloader and kernel files)
-   **/root/** (Home directory for the root user)
-   **/var/log/** (System-level logs)
-   **/usr/bin/**, **/bin/**, **/sbin/** (Essential system binaries)
-   **/lib/**, **/usr/lib/** (System libraries)

## 3. Categorization of Destructive Actions

The following actions and their associated shell commands are explicitly blocked when targeted at Protected Operational Boundaries.

### 3.1. Unrecoverable Deletion

Actions that permanently remove files or directories.

-   **Commands:** `rm`, `shred`, `wipe`, `find ... -delete`

### 3.2. Data Overwriting & Corruption

Actions that overwrite or corrupt existing data, including file content and metadata.

-   **Commands:**
    -   `mv` (when the destination file exists)
    -   `cp` (when the destination file exists and the `-n` flag is not used)
    -   `dd` (direct disk/file writing)
    -   Redirects: `>` (overwrite), `>>` (potential corruption if misused)

### 3.3. Filesystem & Partition Manipulation

Actions that alter the structure of the disk. These are universally forbidden for automated agents.

-   **Commands:** `fdisk`, `mkfs`, `parted`, `gparted`, `cfdisk`

### 3.4. Reckless Permission Changes

Actions that recursively or insecurely alter file and directory permissions, potentially exposing the system.

-   **Commands:**
    -   `chmod -R 777 ...`
    -   `chown -R <non-root-user> ...` on system directories.

### 3.5. System State Control

Actions that can halt or destabilize the running system. These should only be executed through approved, supervised workflows.

-   **Commands:** `shutdown`, `reboot`, `halt`, `systemctl stop`, `systemctl disable` on critical services.

## 4. Policy Enforcement Mechanism

-   **Pre-Execution Validation:** Before any `run_shell_command` is executed, the command string and its target paths MUST be validated against these rules.
-   **Explicit Halting:** If a command violates a rule (e.g., `rm -rf ~/.gemini/skills/`), the execution MUST be halted, and a critical policy violation error must be logged.
-   **No Exceptions:** There are no automated exceptions to these rules. Overrides require manual intervention through a secure administrative interface.
