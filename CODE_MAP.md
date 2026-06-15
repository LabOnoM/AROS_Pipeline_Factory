# AROS Pipeline Factory - Topological Map (`CODE_MAP.md`)

This `CODE_MAP.md` serves as the master index for the **AROS Pipeline Factory**. It is designed to strictly guide AI agents, preventing context pollution and hallucinated architectures.

**Agents MUST use this map to locate the correct pipeline and then read its specific `CLAUDE.md` before executing any code changes.**

---

## 1. Root Structure Outline

| Directory | Purpose |
| :--- | :--- |
| `00.RawData/` | Central registries, experiment indices, and global configuration metadata (`PIPELINE_REGISTRY.md`, `SHARED_ASSET_REGISTRY.md`). |
| `01.Shared_Assets/` | The canonical shared layer governed by CPCP. Contains Shared KIs, Policies, Skills, and deployment Scripts. |
| `.wiki/` | The LLM-Wiki. The ultimate source of grounded truth, research history, and conceptual synthesis. |
| `.regent/` | The AROS internal AI Version Control System (re_gent) audit layer. **Do not modify directly.** |

---

## 2. Package Matrix (Domain Pipelines)

These are the primary execution domains. Each pipeline contains its own localized `CLAUDE.md` file governing specific constraints, tools, and workflows.

| Pipeline Directory | Description | Status |
| :--- | :--- | :--- |
| `workspace_management/` | Global workflows, project structure, `.wiki/` operations, and onboarding. | Active |
| `Grant_Write_Pipeline/` | Universal grant writing, funder profiling, and bilingual drafting. | Active |
| `KAKENHI_Pipeline/` | JSPS KAKENHI specific lifecycle, F-7 reports, and compliance. | Active |
| `Manuscript_Write_Pipeline/`| Dual-agent scientific manuscript writing and review. | Active |
| `Bioinformatics_Pipeline/` | Genomic, proteomic analysis, and string databases. | Active |
| `Data_Analysis_Pipeline/` | Data plotting, statistical modeling, and ML. | Active |
| `Software_Engineering_Pipeline/`| Code validation, testing protocols, and QA gates. | Active |
| `System_Admin_Pipeline/` | Infrastructure, databases, and EC2 orchestration. | Active |
| `UI_Development_Pipeline/` | Frontend web interface development and browser automation. | Active |
| `Writing_Publishing_Pipeline/`| Scholarly publication formats, posters, and citation engines. | Active |
| `Web_Scraping_API_Pipeline/` | Data acquisition and API integration. | Active |
| `Project_Management_Pipeline/`| Task orchestration and schedules. | Active |
| `Multimedia_Generation_Pipeline/`| Programmatic video rendering via Remotion. | Active |
| `VPEP_PipeLine/` | Video-to-Protocol Extraction for SOP synthesis. | Active |
| `Uncategorized_Orphan_Pipeline/`| Catch-all for untracked system assets. | Active |

---

## 3. External & Native Dependencies

The AROS Pipeline Factory interacts with the following external systems:
- **Google Antigravity SDK**: The core multi-agent execution framework.
- **AROS (Antigravity Research OS)**: The live runtime environment where factory assets are deployed (`~/.gemini/`).
- **re_gent**: The AROS CLI version control system handling auditing and time-travel for AI agents.
- **Conda (`aros-base`)**: The standard execution environment for scripts (see `01.Shared_Assets/Environments/aros-base.yml`).

---

## 4. Key Documentation Index

Before executing major operations, agents should consult:
1. **`AGENTS.md`**: Supreme operational laws (LAW -2 through LAW 3). Read this first.
2. **`SPEC.md`**: Architectural specification and constraints.
3. **`00.RawData/SHARED_ASSET_REGISTRY.md`**: The supreme SAMS v1.1 CPCP registry for modifying shared assets.
4. **`README.md`**: General project philosophy and human-readable context.
