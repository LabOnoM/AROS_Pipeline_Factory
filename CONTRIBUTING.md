# Contributing to AROS Pipeline Factory

Thank you for your interest in contributing! The AROS Pipeline Factory is an open ecosystem, and contributions from the research community help make it stronger.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Asset Structure](#asset-structure)
- [Critical Governance Rules (CPCP)](#critical-governance-rules-cpcp)
- [Contribution Types](#contribution-types)
- [Pull Request Process](#pull-request-process)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

---

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/AROS_Pipeline_Factory.git
   cd AROS_Pipeline_Factory
   ```
3. **Create a feature branch**:
   ```bash
   git checkout -b feat/my-new-skill
   ```
4. **Make your changes** (following the rules below)
5. **Open a Pull Request** against `master`

---

## Asset Structure

The factory uses strict directory conventions. All assets must follow these structures:

| Asset Type | Required Structure |
|------------|-------------------|
| **Skills** | `<Pipeline>/Skills/<skill-name>/SKILL.md` |
| **Knowledge Items** | `<Pipeline>/KIs/<ki-name>/artifacts/` + `metadata.json` |
| **Policies** | `<Pipeline>/Policies/<policy-name>.md` |
| **Workflows** | `<Pipeline>/Workflows/<workflow-name>.md` (must include YAML frontmatter with `description` ≤ 250 chars) |

> ⚠️ **Symlinks are strictly banned.** Use direct path references to `01.Shared_Assets/` instead.

---

## Critical Governance Rules (CPCP)

> **The Cross-Pipeline Compatibility Protocol (CPCP) is the supreme governance rule of this repository.**

Before modifying any asset listed in [`00.RawData/SHARED_ASSET_REGISTRY.md`](00.RawData/SHARED_ASSET_REGISTRY.md):

1. **EVALUATE** the asset's usage across all listed consumer pipelines
2. **ESTIMATE IMPACT** — identify any breaking changes
3. **TEST** that no consuming pipeline is broken
4. **RESOLVE OR FORK** — if a conflict is unresolvable, create a pipeline-specific variant instead
5. **UPDATE the Registry** — always update `SHARED_ASSET_REGISTRY.md` after any modification

**Failure to follow the CPCP will result in PR rejection.**

---

## Contribution Types

### ➕ Adding a New Skill

1. Create the directory: `<Pipeline>/Skills/<skill-name>/`
2. Write `SKILL.md` following the [AROS skill format](workspace_management/Skills/antigravity-workflow-authoring_SKILL.md)
3. Test that the skill can be indexed by the `antigravity-brain` MCP
4. If it overlaps with an existing shared skill, register it in `SHARED_ASSET_REGISTRY.md`

### ➕ Adding a New Workflow

1. Create `<Pipeline>/Workflows/<workflow-name>.md`
2. **Required frontmatter:**
   ```yaml
   ---
   description: One-line description of what this workflow does (max 250 chars)
   ---
   ```
3. If the workflow is used across pipelines, move it to `workspace_management/Workflows/`

### 🐛 Fixing a Bug / Improving an Existing Asset

1. Check `SHARED_ASSET_REGISTRY.md` to see if it is a shared asset
2. If shared, follow the full CPCP protocol
3. Document the fix clearly in your PR description

---

## Pull Request Process

1. Ensure your PR targets the `master` branch
2. Fill in the PR template completely, including the CPCP compliance checklist
3. A maintainer will review your PR. For shared asset modifications, two approvals are required.
4. Once merged, run the audit script to verify structural integrity:
   ```bash
   python3 01.Shared_Assets/Scripts/audit_shared_assets.py
   ```

---

## Questions?

Open a [Discussion](../../discussions) or file an [Issue](../../issues). We're happy to help!
