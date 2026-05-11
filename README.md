# AROS Pipeline Factory

## Executive Summary
This repository serves as the central hub for AROS (Antigravity Research OS) automated pipelines. It houses the `Grant_Write_Pipeline`, `KAKENHI_Pipeline`, and `Manuscript_Write_Pipeline`, along with their associated skills, policies, and knowledge items (KIs). It is an infrastructural project designed to enable multi-agent workflows for scientific writing and grant management.

## Chronological Timeline
- **[verified] 2026-05-11 01:24**: KAKENHI pipeline KIs (e.g., e_application_system PDFs, forms) initialized.
- **[verified] 2026-05-11 18:15**: Grant_Write_Pipeline skills requirements and assets initialized.
- **[verified] 2026-05-11 18:29**: Manuscript_Write_Pipeline assets and scripts established.

## Hypothesis Evolution Table
| Phase | Hypothesis |
|-------|------------|
| H1 | Developing modular pipelines and agents for different writing tasks (grants, manuscripts, KAKENHI) significantly streamlines the academic drafting and submission process. |

## Repository Structure Map
```
.
├── 00.RawData/                  # Directory for specific experiment indices
│   └── INDEX.csv
├── Grant_Write_Pipeline/        # Universal Scientific Grant Writing skills and policies
├── KAKENHI_Pipeline/            # KAKENHI-specific reporting and management KIs/skills
├── Manuscript_Write_Pipeline/   # Dual-agent manuscript drafting tools
├── TempScript4Testing/          # Diagnostic and ad-hoc scripts
└── README.md                    # This registry
```

## Key Parameters
- **Scope**: Automation of scientific drafting and management tasks.
- **Components**: KIs, Skills, Policies, Workflows.

## Critical Notes and Caveats
- This repository is primarily code and templates, rather than raw biological data.
- Do not mix raw data directly into the Pipeline templates.

## Methods and Tools Inventory
- **Python / Scripts**: Included in the `scripts/` subdirectories of skills.
- **Knowledge Items**: Embedded in `KIs/` to support domain-specific intelligence.
