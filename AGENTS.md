# AI Agent Operational Rules for AROS Pipeline Factory

This file defines the operational constraints, workflow triggers, and contextual rules for all AI agents operating within the `AROS_Pipeline_Factory` workspace.

---

## 🔒 LAW -2: Agent Version Control Awareness

> **This rule enforces the integrity of the re_gent audit layer, ensuring high-fidelity provenance for all AI actions.**

1. **Audit Layer Protection**: Agents MUST NOT modify the contents of the `.regent/` directory directly. The `rgt` binary is the only authorized interface to the version control store.
2. **Filesystem Awareness**: Agents MUST check for the presence of the `.regent/` directory before executing heavy filesystem operations or moving large batches of files.
3. **Session Context**: The agent's conversation and tool usage are automatically recorded via the hook system. Agents should assume their actions are continuously audited and traceable to their specific prompts.

---

## 🔒 LAW -1: Asset Forging & Debugging Constraints (Lessons Learned)

> **This rule codifies past architectural mistakes and enforces best practices for any agent modifying AROS factory assets.**

1. **The SAMS Basename Trap**: When auditing or creating Skills, agents MUST remember that skills use a directory-per-skill structure (`skill-name/SKILL.md`). Identity comparisons must use the *directory name*, not the filename, to avoid false duplicate flags.
2. **The Symlink Ban (CPCP)**: POSIX symlinks are strictly banned for sharing assets across pipelines to ensure Windows/macOS/Linux portability. Direct path referencing to `01.Shared_Assets/` is mandatory.
3. **The KI-Companion Pattern**: Workflow `.md` files have a hard size limit (~10KB). Heavy logic, tables, or code must be extracted into a KI and loaded at runtime via `read_ki_document()`.
4. **Workflow Frontmatter**: All workflows MUST have YAML frontmatter with a `description` field (≤ 250 chars), or the IDE will fail to register the slash command.
5. **Capability Hallucination Guard**: Agents MUST use `find_helpful_skills` before assuming a skill exists, preventing "No result produced" execution dead-ends.

---

## 🔒 LAW 0: Cross-Pipeline Compatibility Protocol (CPCP) — SUPREME RULE

> **This is the highest-priority governance constraint in this repository. It takes precedence over ALL other rules.**

The AROS Pipeline Factory contains multiple independent pipelines (`Grant_Write_Pipeline`, `KAKENHI_Pipeline`, `Manuscript_Write_Pipeline`, `workspace_management`) that share KIs, Skills, Policies, and Workflows. The authoritative registry of all shared assets is:

📄 **`00.RawData/SHARED_ASSET_REGISTRY.md`**

### Mandatory Modification Protocol

When ANY agent proposes a modification to an asset listed in the Shared Asset Registry:

1. **EVALUATE**: The agent MUST read the asset's usage context in ALL consuming pipelines listed in the registry's "Consumers" column.
2. **ESTIMATE IMPACT**: The agent MUST produce a brief compatibility assessment for each consumer pipeline, identifying any breaking changes, behavioral shifts, or assumption violations.
3. **TEST**: The agent MUST verify that the modification does not break the workflows, KIs, or Skills of any consuming pipeline (e.g., by re-running workflow logic, checking cross-references, or validating output formats).
4. **RESOLVE OR FORK**: If a conflict cannot be resolved to satisfy all consumers, the agent **MUST NOT** overwrite the shared asset. Instead, a **new pipeline-specific variant** of the asset MUST be created (e.g., `fact_check_policy_kakenhi.md`) and registered in the consuming pipeline's own folder.
5. **UPDATE THE REGISTRY**: After any modification or fork, `00.RawData/SHARED_ASSET_REGISTRY.md` MUST be updated to reflect the current state, including a new entry in the Change Log.

### OS Compatibility Constraint
- **Cross-Platform**: As of SAMS v1.1, the Shared Asset Management System (SAMS) relies on direct referencing instead of POSIX symlinks. This repository is fully supported on Windows, Linux, and macOS.

### Triggering Conditions

This protocol activates automatically whenever an agent:
- Edits any file inside a `KIs/`, `Skills/`, `Policies/`, or `Workflows/` directory
- Creates a new asset that overlaps in name or function with an existing shared asset
- Deletes or renames an asset that is referenced by another pipeline

---

## 🧠 LLM-Wiki Context Injection (Strict Grounding)
1. **Wiki-First Resolution**: Before answering any domain-specific or project-specific questions, agents MUST search the local `.wiki/` directory. External or pre-trained knowledge should only supplement, not replace, wiki-grounded answers.
2. **Automatic Workflow Routing**: When the user's message matches a wiki workflow pattern, automatically suggest or trigger the relevant `/wiki-*` workflow (e.g., "Research X" → `/wiki-research`, "What does the wiki say about X" → `/wiki-query`).

## 🧹 Workspace Hygiene
Agents must respect the repository structure and history.
- Diagnostic, ad-hoc, or one-off scratch scripts **MUST NOT** be generated in the root project directory or subdirectories.
- All temporary scripts and scratchpad data must be strictly isolated to the designated IDE scratch directory: `~/.gemini/antigravity/brain/<id>/scratch/`.

## ⚙️ Global Workflow Triggers
The following commands trigger specific autonomous pipelines within this workspace.

### Core Scientific & Data Workflows
- `/lab-commit`: The CANONICAL commit gateway for every workflow to safely apply, validate, and commit file changes.
- `/lab-reorganize`: Safely reorganize project files and folders while preserving git history.
- `/visualize-data`: Autonomous analysis and generation of technical diagrams based on experimental results.

### Manuscript & Grant Workflows
- `/manuscript-write`: **(CRITICAL)** Triggers the dual-agent pipeline for scientific manuscript writing, quantitative data extraction, and rigorous peer-review evaluation using Markdown-first authoring.
- `/grant-write`: Universal scientific grant writing pipeline orchestrating funder profiling, bilingual drafting, and peer review.
- `/kakenhi-annual-report`: KAKENHI grant lifecycle pipeline (report generation, figure integration, dual-agent review).

### LLM-Wiki & Knowledge Workflows
- `/literature-ingest`: Centralized pipeline for retrieving academic PDFs via tiered cascade (OA → LibGen → Sci-Hub) and batch-converting to Markdown/JSON using full-performance hybrid mode.
- `/wiki-research`: **(CRITICAL)** Automatically trigger when the AI detects gaps in the local `.wiki/` knowledge base to perform literature research while adhering to Strict Grounding.
- `/wiki-ingest`: Ingest new experimental results, papers, or data into the project's LLM-Wiki.
- `/wiki-query`: Query the LLM-Wiki to synthesize answers or find specific facts based strictly on the ingested knowledge base.
- `/wiki-build`: Build a cohesive final output (manuscript, report, presentation script) compiled strictly from LLM-Wiki pages.
- `/wiki-update`: Maintain, lint, and synthesize the LLM-Wiki to ensure consistency.

### System & Maintenance Workflows
- `/audit-shared-assets`: Verifies the integrity of the Shared Asset Management System (SAMS) and enforces CPCP compliance via the audit script.
- `/science-project-onboarding`: First-time onboarding, audit, and timeline reconstruction (Self-Evolution rule).
- `/project-organize`: Audit and reorganize the project structure, enforce naming conventions, and maintain hierarchy.
- `/qa-system-audit`: Trigger automated QA system audits for rigorous health checks.
- `/research-discovery`: Clarify research objectives, brainstorm directions, and plan before running autonomous research.
