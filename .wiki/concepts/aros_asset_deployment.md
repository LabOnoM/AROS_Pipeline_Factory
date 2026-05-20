# AROS Asset Deployment Architecture

## Overview

The AROS Pipeline Factory uses a **source-of-truth → runtime deployment** model. Assets (Skills, KIs, Policies, Workflows) are authored and version-controlled in the factory Git repository, then deployed to the `~/.gemini/` runtime directory tree where the `antigravity-brain` MCP server can index and serve them.

## Canonical Directory Map

| Asset Type | Factory Source | AROS Runtime Target | Indexer |
|------------|---------------|---------------------|---------|
| **Skills** | `<Pipeline>/Skills/<name>/SKILL.md` | `~/.gemini/skills/<name>/SKILL.md` | `ki_workflow_index.py` |
| **KIs** | `<Pipeline>/KIs/<name>/` | `~/.gemini/antigravity/knowledge/<name>/` | `ki_workflow_index.py` |
| **Policies** | `<Pipeline>/Policies/<name>.md` | `~/.gemini/antigravity/policies/<name>.md` | `batch_evolver.py` |
| **Workflows** | `<Pipeline>/Workflows/<name>.md` | `~/.gemini/antigravity/global_workflows/<name>.md` | `ki_workflow_index.py` |

## Deployment Mechanism

The canonical synchronization tool is `01.Shared_Assets/Scripts/sync_with_aros.sh`. It handles bidirectional sync to ensure that autonomous GEPA (Generative Error-Patching Agent) mutations occurring in the Runtime are not overwritten, but instead pulled back into the Git-tracked Factory.

### Usage
```bash
# 1. Status Check (Always run this first to detect GEPA mutations)
./01.Shared_Assets/Scripts/sync_with_aros.sh status

# 2. Push (Deploy Factory → Runtime)
./01.Shared_Assets/Scripts/sync_with_aros.sh push

# 3. Pull (Import GEPA mutations Runtime → Factory)
./01.Shared_Assets/Scripts/sync_with_aros.sh pull

# 4. Diff (Show diverged changes)
./01.Shared_Assets/Scripts/sync_with_aros.sh diff <type> <name>
```

*(Note: `deploy_to_aros.sh` is maintained as a legacy wrapper for `sync_with_aros.sh push` to ensure backward compatibility).*

### How It Works
1. Scans all pipeline directories (Grant_Write_Pipeline, Manuscript_Write_Pipeline, KAKENHI_Pipeline, workspace_management, 01.Shared_Assets) for assets.
2. Uses content-based SHA-256 checksums (not mtime) to detect staleness and divergence.
3. Automatically routes pulled assets to their originating Pipeline directory in the Factory.
4. Handles legacy formats (flat `*_SKILL.md` files) by warning the user during pulls, preventing structural corruption.

## Concurrency Protection & Copy Safety
- **Exclusive Lock**: To prevent simultaneous execution of write commands (`push`/`pull`) that could corrupt runtime files, `sync_with_aros.sh` acquires an exclusive lock at `~/.gemini/knowledge.lock`.
- **Lock Fallback**: On platforms without POSIX `flock` (e.g. Windows Git Bash), it falls back to atomic directory creation (`mkdir`) at `/tmp/aros_knowledge.lock.dir`. Clean lock release is enforced via shell traps (`EXIT`, `INT`, `TERM`).
- **rsync Fallback**: The script copies assets using `rsync -a --delete` for efficiency. If `rsync` is missing, it falls back to a robust directory cleaning and copy sequence using native POSIX commands (`find` + `rm` + `cp -Rf`).

## Path & Formatting Enforcement Rules

Assets placed in wrong directories are **invisible** to AROS:

- ❌ A skill in `~/.gemini/antigravity/knowledge/` → NOT found by `find_helpful_skills`
- ❌ A KI in `~/.gemini/skills/` → NOT found by `find_helpful_ki`
- ❌ A policy in `~/.gemini/antigravity/global_workflows/` → NOT eligible for GEPA mutation
- ❌ Path contains literal backslashes (`\`) → Breaks cross-platform checkouts and syntax. Must be purged immediately.
- ✅ Only assets in the canonical directories above, using forward slashes (`/`), are indexed.

## Governance

- **SPEC §4.5**: Defines the directory map and bidirectional sync architecture.
- **AGENTS.md LAW 1**: Mandates use of `sync_with_aros.sh` for all deployments.
- **CPCP (LAW 0)**: Shared assets must still follow the Cross-Pipeline Compatibility Protocol before modification.


## Related

- [[conda_environment_standard]] — Conda-gated self-healing for environment management
- [[self_healing_environment_policy]] — L0/L1/L2 repair pattern
- [[cross_pipeline_compatibility_protocol]] — CPCP governance
