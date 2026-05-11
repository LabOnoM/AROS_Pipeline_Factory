# Shared Asset Registry

> **GOVERNANCE AUTHORITY**: This document is the single source of truth for all shared assets across the AROS Pipeline Factory. Any asset listed here exists in multiple pipeline folders and is subject to the **Cross-Pipeline Compatibility Protocol** (see below).
>
> **Last Updated**: 2026-05-12

---

## 🔒 Cross-Pipeline Compatibility Protocol (CPCP)

> [!CAUTION]
> **SUPREME RULE — This is the highest-priority governance constraint in this repository.**
>
> When ANY modification is proposed to a shared asset listed in this registry:
>
> 1. **EVALUATE**: The agent MUST read the asset's usage context in ALL consuming pipelines listed in the "Consumers" column.
> 2. **ESTIMATE IMPACT**: The agent MUST produce a brief compatibility assessment for each consumer pipeline, identifying any breaking changes, behavioral shifts, or assumption violations.
> 3. **TEST**: The agent MUST verify that the modification does not break the workflows, KIs, or Skills of any consuming pipeline (e.g., by re-running workflow logic, checking cross-references, or validating output formats).
> 4. **RESOLVE OR FORK**: If a conflict cannot be resolved to satisfy all consumers, the agent MUST NOT overwrite the shared asset. Instead, a **new pipeline-specific variant** of the asset MUST be created (e.g., `fact_check_policy_kakenhi.md`) and registered in the consuming pipeline's own folder.
> 5. **UPDATE THIS REGISTRY**: After any modification or fork, this file MUST be updated to reflect the current state.

---

## 📋 Shared KIs (Knowledge Items)

| KI Name | Location (Canonical) | Consumers | Notes |
|---------|---------------------|-----------|-------|
| `agentic_manuscript_publishing` | `01.Shared_Assets/KIs/` | **Grant_Write_Pipeline**, **Manuscript_Write_Pipeline** | Identical copies confirmed 2026-05-11. Covers dual-agent workflow, LaTeX management, AI review strategies. |
| `markdown_first_manuscript_policy` | `01.Shared_Assets/KIs/` | **Grant_Write_Pipeline**, **Manuscript_Write_Pipeline** | Identical copies confirmed 2026-05-11. Hard institutional policy: Markdown-first authoring, no direct LaTeX. |
| `grant_funder_profiles` | `Grant_Write_Pipeline/KIs/` | **Grant_Write_Pipeline**, **KAKENHI_Pipeline** (implicit via grant workflows) | Funder constraint profiles (MEXT SPReAD, NIH R01, etc.). KAKENHI pipeline references funder-specific rules. |
| `kakenhi_management_pipeline` | `KAKENHI_Pipeline/KIs/` | **KAKENHI_Pipeline**, **workspace_management** | SPEC.md references `/lab-commit` and cross-pipeline workflows. |
| `publication_grant_map` | `KAKENHI_Pipeline/KIs/` | **KAKENHI_Pipeline**, **Grant_Write_Pipeline** (implicit) | Template for publication-to-grant attribution. Used in both grant reporting contexts. |
| `regent_integration_reference` | `workspace_management/KIs/` | **workspace_management** | Reference guide for the re_gent VCS audit layer, CLI commands, and hook protocols. |

---

## 📋 Shared Workflows

| Workflow | Location (Canonical) | Consumers | Notes |
|----------|---------------------|-----------|-------|
| `/lab-commit` | `workspace_management/Workflows/` | **ALL PIPELINES** | The canonical commit gateway. Referenced by `grant-write.md`, `kakenhi-annual-report.md`, `manuscript-write.md`, and all wiki workflows. |
| `/lab-reorganize` | `workspace_management/Workflows/` | **ALL PIPELINES** | File reorganization with git history preservation. |
| `/wiki-build` | `workspace_management/Workflows/` | **ALL PIPELINES** | Referenced by KAKENHI `fact_check_policy.md`. Compiles wiki pages into output documents. |
| `/wiki-ingest` | `workspace_management/Workflows/` | **ALL PIPELINES** | Ingests new papers/data into the LLM-Wiki. |
| `/wiki-query` | `workspace_management/Workflows/` | **ALL PIPELINES** | Wiki-grounded Q&A. |
| `/wiki-research` | `workspace_management/Workflows/` | **ALL PIPELINES** | External literature research into the wiki. |
| `/wiki-update` | `workspace_management/Workflows/` | **ALL PIPELINES** | Wiki structural linting and synthesis. |
| `/science-project-onboarding` | `workspace_management/Workflows/` | **ALL PIPELINES** | First-time project audit and setup. |
| `/audit-shared-assets` | `workspace_management/Workflows/` | **ALL PIPELINES** | SAMS structural audit workflow to enforce CPCP compliance. |

---

## 📋 Shared Skills

| Skill Name | Location (Canonical) | Consumers | Notes |
|------------|---------------------|-----------|-------|
| `antigravity-workflow-authoring` | `workspace_management/Skills/` | **ALL PIPELINES** | Meta-skill for authoring new workflows. Governs workflow creation standards across the factory. |
| `super-scientist` | `workspace_management/Skills/` | **ALL PIPELINES** | Kosmos SuperScientist integration. Triggers research cycles applicable to any pipeline's domain. |
| `literature-ingestion` | `01.Shared_Assets/Skills/` | **ALL PIPELINES** | Tiered PDF retrieval (OA→LibGen→Sci-Hub) + opendataloader-pdf conversion. **Replaces deprecated `research-paper-downloader`.** |
| `retraction-watcher` | `~/.gemini/skills/` | **ALL PIPELINES** | Scans reference lists against Retraction Watch DB. MANDATORY in Phase 0.5 (pre-draft) and Phase 5 (post-review) of all writing workflows. |
| `content-proofreading` | `Grant_Write_Pipeline/Skills/` | **Grant_Write_Pipeline**, **Manuscript_Write_Pipeline** (implicit) | General-purpose proofreading applicable to both grant and manuscript drafting. |
| `scientific-brainstorming` | `Grant_Write_Pipeline/Skills/` | **Grant_Write_Pipeline**, **Manuscript_Write_Pipeline** (implicit) | Brainstorming skill used across research drafting contexts. |
| `medical-translation` | `Grant_Write_Pipeline/Skills/` | **Grant_Write_Pipeline**, **KAKENHI_Pipeline** (implicit) | Bilingual (EN/JP) translation used for both grant applications and KAKENHI reports. |
| `regent-governance` | `workspace_management/Skills/` | **workspace_management** | Manages re_gent deployment health checks, `.regentignore` generation, and session exports. |
| `md-html-docx-generator` | `workspace_management/Skills/` | **ALL PIPELINES** | Generates high-fidelity HTML/DOCX reports section-by-section to bypass LLM output token limits. Invoked in Phase 3 Step 7 (manuscript) and Phase 6 (grant). |
| `visualize-data` | `~/.gemini/skills/` | **ALL PIPELINES** | Upgraded orchestrator for all scientific diagrams (Mermaid, fireworks-tech-graph, SVG+PNG via cairosvg). Replaces deprecated `grant-gantt-chart-gen` and `text-to-technical-roadmap`. |

---

## 📋 Shared Policies

| Policy | Location (Canonical) | Consumers | Notes |
|--------|---------------------|-----------|-------|
| `gepa_protocol.md` | `01.Shared_Assets/Policies/` | **Grant_Write_Pipeline**, **workspace_management** (implicit via GEPA system) | Governs iterative agent refinement. The GEPA protocol is a factory-wide evolutionary mechanism. |
| `output-truncation-management.md` | `01.Shared_Assets/Policies/` | **ALL PIPELINES** | Data integrity policy for handling truncated outputs. Applicable universally. |
| `self_healing_environment_policy.md` | `01.Shared_Assets/Policies/` | **ALL PIPELINES** | MANDATORY: Three-phase Detect→Repair→Degrade pattern for all external tool dependencies. SPEC §4.4. |
| `fact_check_policy.md` | `KAKENHI_Pipeline/Policies/` | **KAKENHI_Pipeline**, **Grant_Write_Pipeline** (implicit for publications) | Publication fact-checking. References `/wiki-build`. Relevant whenever publications are cited in grant reports. |

---

## 📊 Consumer Dependency Matrix

```
                            Grant_Write  KAKENHI  Manuscript_Write  workspace_mgmt
                            ───────────  ───────  ────────────────  ──────────────
agentic_manuscript_pub KI       ✅          -           ✅               -
markdown_first_policy KI        ✅          -           ✅               -
grant_funder_profiles KI        ✅          ◐           -                -
kakenhi_mgmt_pipeline KI        -           ✅          -                ✅
publication_grant_map KI        ◐           ✅          -                -
/lab-commit WF                  ✅          ✅          ✅               ✅
/lab-reorganize WF              ✅          ✅          ✅               ✅
/wiki-* WFs (6 total)           ✅          ✅          ✅               ✅
/science-project-onboarding WF  ✅          ✅          ✅               ✅
/audit-shared-assets WF         ✅          ✅          ✅               ✅
literature-ingestion SKL        ✅          ✅          ✅               ✅
regent-governance SKL           -           -           -                ✅
regent_integration_ref KI       -           -           -                ✅
gepa_protocol POL               ✅          ◐           ◐               ✅
output-truncation POL           ✅          ✅          ✅               ✅
self-healing-env POL             ✅          ✅          ✅               ✅
fact_check_policy POL           ◐           ✅          -                -

Legend: ✅ = Direct consumer  ◐ = Implicit/indirect consumer  - = Not consumed
```

---

## 🔄 Change Log

| Date | Asset | Action | Pipelines Affected | Outcome |
|------|-------|--------|-------------------|---------|
| 2026-05-11 | *Initial Registry* | Created | ALL | Baseline established. All shared assets audited and confirmed identical where duplicated. |
| 2026-05-11 | *SAMS v1.0 Migration* | Centralized KIs/Policies | ALL | Centralized multiple KIs and Policies into `01.Shared_Assets/` replacing pipeline instances with symlinks. |
| 2026-05-11 | `literature-ingestion` | Created | ALL | New shared skill for automated literature retrieval and PDF-to-Markdown conversion. Replaces `research-paper-downloader`. |
| 2026-05-11 | `audit_shared_assets.py` | Relocated | ALL | Moved from `workspace_management/Scripts/` to `01.Shared_Assets/Scripts/` as factory-level infrastructure. Fixed basename-only duplicate detection bug. |
| 2026-05-11 | `TempScript4Testing/` | Removed | NONE | Redundant prototype scripts absorbed into `literature-ingestion` skill. |
| 2026-05-11 | `regent-governance` & KI | Created | `workspace_management` | Integrated re_gent VCS audit layer into workspace_management workflows, added corresponding KI and governance skill. |
| 2026-05-11 | `PIPELINE_REGISTRY.md` | Created | ALL | Replaced `INDEX.csv` with `PIPELINE_REGISTRY.md`. All workflow templates generalized for dynamic registry discovery. `project-organize` bash scripts updated. `regent_to_aros_bridge.py` cross-platform path fix applied. |
| 2026-05-11 | `md-html-docx-generator` | Created | ALL | Added new skill to dynamically build high-fidelity interactive HTML reports (and DOCX exports) from chunked markdown, avoiding LLM token limits. |
| 2026-05-11 | `visualize-data` | Upgraded | ALL | Consolidated all fragmented diagram skills into a unified scientific-diagram-generator using fireworks-tech-graph and cairosvg. Deprecated `text-to-technical-roadmap` and `grant-gantt-chart-gen`. |
| 2026-05-11 | `literature-ingestion` & Global Workflows | Upgraded | ALL | Enforced Dual-Format Extraction (Markdown+JSON). Added Citation-Before-Claim Protocol to `/manuscript-write` and `/grant-write` utilizing `literature-close-read` to eliminate hallucinations. |
| 2026-05-12 | `/grant-write` & `/manuscript-write` (Global + Local) | Hardened | ALL | Added Phase 0.5 mandatory reference retrieval, `retraction-watcher` in pre-draft and review phases, minimum 3 review rounds with `REVIEW_LOG.md` path specified, `md-html-docx-generator` for interactive HTML output, `visualize-data` for workflow diagrams in both pipelines, graphical abstract phase (A1.5) in manuscript pipeline. Local pipeline copies synced with global via Option A. Deprecated `grant-gantt-chart-gen` and `text-to-technical-roadmap` with DEPRECATED.md markers. |
| 2026-05-12 | `self_healing_environment_policy` + 4 workflows | Created + Hardened | ALL | New MANDATORY policy (SPEC §4.4). Fixed fragile `go install`/`pip install`/`pandoc` calls in `/wiki-update`, `/science-project-onboarding`, `/manuscript-write`, and `/proteomics-enrichment` with full Detect→Repair→Degrade pattern. Updated `AROS-POLICY-TOOL-PREFLIGHT-V1` with cross-reference. |
