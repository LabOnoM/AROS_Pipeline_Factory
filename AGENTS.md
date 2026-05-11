# AI Agent Operational Rules for AROS Pipeline Factory

This file defines the operational constraints, workflow triggers, and contextual rules for all AI agents operating within the `AROS_Pipeline_Factory` workspace.

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
- `/wiki-research`: **(CRITICAL)** Automatically trigger when the AI detects gaps in the local `.wiki/` knowledge base to perform literature research while adhering to Strict Grounding.
- `/wiki-ingest`: Ingest new experimental results, papers, or data into the project's LLM-Wiki.
- `/wiki-query`: Query the LLM-Wiki to synthesize answers or find specific facts based strictly on the ingested knowledge base.
- `/wiki-build`: Build a cohesive final output (manuscript, report, presentation script) compiled strictly from LLM-Wiki pages.
- `/wiki-update`: Maintain, lint, and synthesize the LLM-Wiki to ensure consistency.

### System & Maintenance Workflows
- `/science-project-onboarding`: First-time onboarding, audit, and timeline reconstruction (Self-Evolution rule).
- `/project-organize`: Audit and reorganize the project structure, enforce naming conventions, and maintain hierarchy.
- `/qa-system-audit`: Trigger automated QA system audits for rigorous health checks.
- `/research-discovery`: Clarify research objectives, brainstorm directions, and plan before running autonomous research.
