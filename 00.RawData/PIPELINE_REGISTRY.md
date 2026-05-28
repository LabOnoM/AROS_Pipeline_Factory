# AROS Pipeline Factory Registry

This file serves as the canonical registry for all pipelines maintained within the AROS Pipeline Factory. Agents should parse this table to discover available pipelines and their corresponding workflows.

| Pipeline Directory | Description | Status | Target Workflows |
| :--- | :--- | :--- | :--- |
| `Grant_Write_Pipeline` | Universal grant writing, funder profiling, and bilingual drafting | Active | `/grant-write` |
| `KAKENHI_Pipeline` | JSPS KAKENHI specific lifecycle, F-7 reports, and compliance | Active | `/kakenhi-annual-report` |
| `Manuscript_Write_Pipeline` | Dual-agent scientific manuscript writing and review | Active | `/manuscript-write` |
| `workspace_management` | Global workflows, project structure, and onboarding | Active | `/lab-reorganize`, `/science-project-onboarding`, `/wiki-*` |
| `Bioinformatics_Pipeline` | Scientific databases, sequence alignment, and molecular modeling | Active | `/proteomics-enrichment` |
| `Data_Analysis_Pipeline` | Data plotting, statistical analysis, and machine learning | Active | `/visualize-data` |
| `Software_Engineering_Pipeline` | Code validation, testing protocols, and agent quality gates | Active | `/qa-system-audit` |
| `System_Admin_Pipeline` | Server management, database administration, and AWS EC2 orchestration | Active | `/aws-dynamic-ec2-orchestration` |
| `UI_Development_Pipeline` | Frontend web interface development and browser automation | Active | - |
| `Web_Scraping_API_Pipeline` | Web crawling, HTTP clients, and data extraction | Active | - |
| `Writing_Publishing_Pipeline` | Scholarly publication formats, posters, and citation engines | Active | `/research-discovery` |
| `Project_Management_Pipeline` | Tasks breakdown, schedules, and roadmap planning | Active | - |
| `Uncategorized_Orphan_Pipeline` | Catch-all directory for untracked or unsorted system assets | Active | - |
| `Multimedia_Generation_Pipeline` | Programmatic video rendering and multimedia generation via Remotion | Active | - |
| `VPEP_PipeLine` | Video-to-Protocol Extraction Pipeline for automated SOP synthesis from experimental videos | Active | - |
