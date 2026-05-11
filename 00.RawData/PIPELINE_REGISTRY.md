# AROS Pipeline Factory Registry

This file serves as the canonical registry for all pipelines maintained within the AROS Pipeline Factory. Agents should parse this table to discover available pipelines and their corresponding workflows.

| Pipeline Directory | Description | Status | Target Workflows |
| :--- | :--- | :--- | :--- |
| `Grant_Write_Pipeline` | Universal grant writing, funder profiling, and bilingual drafting | Active | `/grant-write` |
| `KAKENHI_Pipeline` | JSPS KAKENHI specific lifecycle, F-7 reports, and compliance | Active | `/kakenhi-annual-report` |
| `Manuscript_Write_Pipeline` | Dual-agent scientific manuscript writing and review | Active | `/manuscript-write` |
| `workspace_management` | Global workflows, project structure, and onboarding | Active | `/lab-reorganize`, `/science-project-onboarding`, `/wiki-*` |
