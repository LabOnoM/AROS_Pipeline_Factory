# AROS Pipeline Factory

## Executive Summary
This repository serves as the central hub for AROS (Antigravity Research OS) automated pipelines. It houses the `Grant_Write_Pipeline`, `KAKENHI_Pipeline`, `Manuscript_Write_Pipeline`, and `workspace_management` module, along with their associated skills, policies, and knowledge items (KIs). It is an infrastructural project designed to enable multi-agent workflows for scientific writing and grant management.

> **⚠️ Agent Warning (Asset Forging Constraints)**: This repository is a Factory for forging AROS assets. Before modifying any Skill, Policy, KI, or Workflow, you MUST read `AGENTS.md` and `SPEC.md` to understand the CPCP constraints, SAMS audit rules, known failure modes (e.g., LaTeX truncation), and directory-structure requirements.

## 🔒 Shared Asset Governance (SUPREME RULE)

Multiple pipelines in this factory share KIs, Skills, Policies, and Workflows. The **Cross-Pipeline Compatibility Protocol (CPCP)** — defined in `AGENTS.md` as LAW 0 — ensures that any modification to a shared asset is evaluated, tested, and validated across ALL consuming pipelines before being committed.

📄 **Central Registry**: [`00.RawData/SHARED_ASSET_REGISTRY.md`](00.RawData/SHARED_ASSET_REGISTRY.md)

This registry must be consulted before modifying any shared asset. If a modification creates an unresolvable conflict between pipelines, a new pipeline-specific variant must be forked rather than overwriting the shared original.

## ⚠️ Architecture Constraints
**Cross-Platform Enabled (SAMS v1.1)**: This repository does not rely on POSIX symlinks. It is fully operable on Linux, macOS, and Windows. Do not re-introduce symlinks or platform-specific directory references.

## Chronological Timeline
- **[verified] 2026-05-11 01:24**: KAKENHI pipeline KIs (e.g., e_application_system PDFs, forms) initialized.
- **[verified] 2026-05-11 18:15**: Grant_Write_Pipeline skills requirements and assets initialized.
- **[verified] 2026-05-11 18:29**: Manuscript_Write_Pipeline assets and scripts established.
- **[verified] 2026-05-11 18:44**: Shared Asset Registry and CPCP governance established.
- **[verified] 2026-05-11 19:00**: Centralized Shared Asset Management System (SAMS) implemented with direct referencing and programmatic audit tools.
- **[verified] 2026-05-11 21:00**: Dual-VCS architecture (Git + re_gent) deployed for AI agent auditability.
- **[verified] 2026-05-11 22:00**: Replaced legacy `INDEX.csv` with `PIPELINE_REGISTRY.md`. Generalized all workflow templates for dynamic registry discovery.

## Hypothesis Evolution Table
| Phase | Hypothesis |
|-------|------------|
| H1 | Developing modular pipelines and agents for different writing tasks (grants, manuscripts, KAKENHI) significantly streamlines the academic drafting and submission process. |
| H2 | Shared assets across pipelines (KIs, policies, workflows) must be governed by a central registry and compatibility protocol to prevent cross-pipeline regressions. |

## Repository Structure Map
```
.
├── 00.RawData/                  # Central registry and experiment indices
│   ├── PIPELINE_REGISTRY.md    #   Pipeline catalog (replaced INDEX.csv)
│   ├── SHARED_ASSET_REGISTRY.md #   ⚠️ SUPREME: Cross-pipeline shared asset registry
│   └── Literature/              #   Standardized literature storage (PDFs, Markdown, metadata)
├── 01.Shared_Assets/            # Canonical repository for shared KIs, Policies, Skills, Scripts
│   ├── KIs/                     #   agentic_manuscript_publishing, markdown_first_manuscript_policy
│   ├── Policies/                #   gepa_protocol, output-truncation-management
│   ├── Skills/                  #   literature-ingestion (tiered PDF retrieval + conversion)
│   └── Scripts/                 #   Factory-level infrastructure tools (audit_shared_assets.py)
├── Grant_Write_Pipeline/        # Universal Scientific Grant Writing
│   ├── KIs/                     #   grant_funder_profiles
│   ├── Policies/                #   (references 01.Shared_Assets)
│   ├── Skills/                  #   18 skills (grant-mock-reviewer, medical-translation, etc.)
│   └── Workflows/               #   grant-write.md
├── KAKENHI_Pipeline/            # KAKENHI-specific reporting and management
│   ├── KIs/                     #   kakenhi_e_application_system, kakenhi_report_forms, etc.
│   ├── Policies/                #   fact_check_policy, grant_report_policy
│   ├── Skills/                  #   3 skills (kakenhi-form-completion, etc.)
│   └── Workflows/               #   kakenhi-annual-report.md
├── Manuscript_Write_Pipeline/   # Dual-agent manuscript drafting tools
│   ├── KIs/                     #   agentic_manuscript_publishing, markdown_first_manuscript_policy
│   ├── Policies/                #   (none yet)
│   ├── Skills/                  #   16 skills (peer-review, statistical-analysis, etc.)
│   └── Workflows/               #   manuscript-write.md
├── workspace_management/        # Cross-pipeline infrastructure
│   ├── KIs/                     #   AROS architecture references
│   ├── Skills/                  #   workflow-authoring, super-scientist
│   └── Workflows/               #   lab-commit, lab-reorganize, wiki-*, literature-ingest, etc.
├── .wiki/                       # LLM-Wiki knowledge base
├── AGENTS.md                    # Agent operational rules (includes CPCP as LAW 0)
├── SPEC.md                      # Architectural specification
└── README.md                    # This document
```

## Key Parameters
- **Scope**: Automation of scientific drafting and management tasks.
- **Components**: KIs, Skills, Policies, Workflows.
- **Governance**: Cross-Pipeline Compatibility Protocol (CPCP) via `SHARED_ASSET_REGISTRY.md`.

## Critical Notes and Caveats
- This repository is primarily code and templates, rather than raw biological data.
- Do not mix raw data directly into the Pipeline templates.
- **Any modification to shared assets MUST follow the CPCP** (see `AGENTS.md` LAW 0).

## Methods and Tools Inventory
- **Python / Scripts**: Included in the `scripts/` subdirectories of skills.
- **Knowledge Items**: Embedded in `KIs/` to support domain-specific intelligence.
- **Shared Asset Registry**: `00.RawData/SHARED_ASSET_REGISTRY.md` — the authoritative cross-pipeline dependency tracker.

