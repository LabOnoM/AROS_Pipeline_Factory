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

The canonical deployment tool is `01.Shared_Assets/Scripts/deploy_to_aros.sh`.

### Usage
```bash
# Full deployment (all asset types)
./01.Shared_Assets/Scripts/deploy_to_aros.sh

# Preview without modifying files
./01.Shared_Assets/Scripts/deploy_to_aros.sh --dry-run

# Selective deployment
./01.Shared_Assets/Scripts/deploy_to_aros.sh --skills
./01.Shared_Assets/Scripts/deploy_to_aros.sh --kis
./01.Shared_Assets/Scripts/deploy_to_aros.sh --policies
./01.Shared_Assets/Scripts/deploy_to_aros.sh --workflows
```

### How It Works
1. Scans all pipeline directories (Grant_Write_Pipeline, Manuscript_Write_Pipeline, KAKENHI_Pipeline, workspace_management, 01.Shared_Assets) for assets.
2. Uses idempotent `rsync` for directories and `cp` for flat files.
3. Handles legacy formats (flat `*_SKILL.md` files, flat `.md` KI files) by converting to the canonical directory structure.
4. Reports deployment counts and errors in a summary table.

## Path Enforcement Rules

Assets placed in wrong directories are **invisible** to AROS:

- ❌ A skill in `~/.gemini/antigravity/knowledge/` → NOT found by `find_helpful_skills`
- ❌ A KI in `~/.gemini/skills/` → NOT found by `find_helpful_ki`
- ❌ A policy in `~/.gemini/antigravity/global_workflows/` → NOT eligible for GEPA mutation
- ✅ Only assets in the canonical directories above are indexed

## Governance

- **SPEC §4.5**: Defines the directory map and deployment protocol.
- **AGENTS.md LAW 1**: Mandates use of `deploy_to_aros.sh` for all deployments.
- **CPCP (LAW 0)**: Shared assets must still follow the Cross-Pipeline Compatibility Protocol before modification.

## Related

- [[conda_environment_standard]] — Conda-gated self-healing for environment management
- [[self_healing_environment_policy]] — L0/L1/L2 repair pattern
- [[cross_pipeline_compatibility_protocol]] — CPCP governance
