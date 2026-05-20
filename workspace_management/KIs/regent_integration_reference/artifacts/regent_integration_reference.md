---
description: Reference guide for the re_gent VCS audit layer, including architecture, CLI commands, hook protocols, and AROS bridge mechanics.
---

# Re_gent VCS Integration Reference

This Knowledge Item (KI) documents the architecture, constraints, and operational mechanisms of the `re_gent` Agent Version Control System as implemented in the AROS Pipeline Factory.

## 1. Architectural Model

`re_gent` tracks agent activity using a Git-like content-addressed Directed Acyclic Graph (DAG), stored in `.regent/objects/`.

There are four primary object types:
1. **Blob**: Raw file content.
2. **Tree**: Directory structure (maps paths to Blob hashes).
3. **Step**: A single atomic action (maps to a conversation turn). Contains:
   - `tree`: Reference to the root Tree.
   - `parent`: Reference to the previous Step.
   - `cause`: Metadata about what triggered the step (tool name, tool arguments, result).
   - `transcript`: The cumulative conversation state (messages) up to this step.
   - `timestamp_nanos`: When the step occurred.
4. **Ref**: A pointer to a Step (e.g., session head).

### Key Design Constraints
- **Derived Index**: The SQLite database (`.regent/index.db`) is purely an index for fast queries (lineage, blame maps, session lists). The source of truth is always the object store. If `index.db` is deleted, it can be rebuilt via `rgt reindex`.
- **Max File Size**: By default, `re_gent` skips files larger than 10MB during snapshotting to preserve performance.
- **Symlinks**: POSIX symlinks are intentionally skipped in Phase 1 implementations for cross-platform stability.

## 2. CLI Command Reference

The `rgt` binary provides the interface to the `.regent/` store:

- `rgt init [--skip-hook]`: Initializes the `.regent/` directory and creates the SQLite index.
- `rgt log [--conversation-only | --files-only | --graph] [session-id]`: Shows the step history, including the conversation transcript and tool inputs/outputs.
- `rgt blame <file>[:<line>]`: Shows per-line provenance (which step last modified each line).
- `rgt show <step-hash>`: Displays full details of a specific step (tool arguments, result, and conversation delta).
- `rgt rewind <step-hash>`: Non-destructively rolls back the workspace and conversation to a previous step. Creates an automatic backup in `.regent/backups/`.
- `rgt sessions`: Lists all tracked sessions and their active branches.

## 3. The Hook Protocol

`re_gent` captures activity via integration hooks, typically configured in an agent's settings (e.g., `.claude/settings.json` or `~/.gemini/settings.json`).

The integration relies on three primary hooks to record a single conversation turn:
1. `UserPromptSubmit` → `rgt message-hook user`: Captures the user's input message.
2. `PostToolBatch` → `rgt tool-batch-hook`: Captures the execution of one or more tools (arguments and results).
3. `Stop` → `rgt message-hook assistant`: Captures the assistant's final response and triggers the **Snapshot** mechanism to commit a new Step.

*Note: Older versions used a single `PostToolUse` hook (`rgt hook`), which was replaced by the 3-part message hook system to capture conversation context accurately.*

## 4. Exclusion Policies (`.regentignore`)

While `re_gent` skips files >10MB, scientific workspaces contain many large binary formats that should not be snapshotted. A `.regentignore` file is generated at the workspace root during `/science-project-onboarding`.

**Standard scientific exclusions:**
- Imaging: `*.tif`, `*.czi`, `*.nd2`, `*.ome.tif`
- Sequencing: `*.fastq`, `*.bam`, `*.vcf.gz`
- Mass Spec: `*.raw`, `*.mzML`
- Binaries: `*.h5`, `*.pkl`, `*.pt`, `*.pptx`, `*.xlsx`

## 5. AROS Bridge Mechanics (Session Export)

`re_gent` acts as the low-level audit trail. To feed this data into the AROS reasoning engine (`brain.db`), a bridge is required.

Future implementations of the `regent-governance` skill will extract completed `re_gent` session transcripts and summarize them into AROS `world_facts` and `experiences` via the `mcp_antigravity-brain_query_memory` and `dreamer` system, ensuring that lessons learned during an audited session become permanent AI knowledge.
