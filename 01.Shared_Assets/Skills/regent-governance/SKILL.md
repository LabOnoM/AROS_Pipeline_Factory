---
cpcp_asset: true
description: Perform health checks on the re_gent VCS audit layer, generate missing .regentignore files, and bridge session data to the AROS Brain.
allowed-tools: Bash, read_file
argument-hint: "check | ignore | bridge"
---

# Re_gent Governance Skill

This skill allows an AI agent to interact with and manage the `re_gent` version control system within a workspace.

## Usage

```bash
# To perform a health check on the current workspace
rgt log --limit 1

# To check if .regentignore exists and has basic patterns
cat .regentignore
```

## Available Actions

### 1. `check` (Health Check)
Verifies that the `.regent/` directory exists, the SQLite index is accessible, and the hook system is functioning.

**Execution:**
```bash
if [ -d ".regent" ]; then
    echo "re_gent is initialized."
    rgt log --limit 1 || echo "Error reading log."
else
    echo "re_gent is NOT initialized."
fi
```

### 2. `ignore` (.regentignore Generation)
Generates or updates the `.regentignore` file with standard scientific data exclusions to prevent massive binaries from bloating the agent audit trail.

**Execution:**
Ensure the `.regentignore` contains patterns like `*.tif`, `*.czi`, `*.fastq`, `*.h5`, etc. Refer to the `regent_integration_reference.md` KI for the exact list.

### 3. `bridge` (Session-to-Brain Bridge)
Extracts the summary of the latest `re_gent` session and formats it for ingestion into the AROS `brain.db` via the `dreamer` pipeline. This transforms audited conversation logs into permanent, searchable `world_facts` and `mental_models`.

**Execution:**
```bash
# Execute the Python adapter to bridge the latest session
python3 01.Shared_Assets/Scripts/regent_to_aros_bridge.py
```
*Note: To perform a dry run without modifying the database, append the `--dry-run` flag.*
