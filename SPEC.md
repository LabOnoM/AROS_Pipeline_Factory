# AROS Pipeline Factory Specification v2.0
**Author**: Antigravity AI  
**Status**: PRODUCTION  
**Last Updated**: 2026-05-12  

## 1. Executive Summary
The AROS Pipeline Factory is the canonical source-of-truth for the Antigravity Research OS (AROS) runtime environment. This specification defines the modular domain pipeline architecture, the Shared Asset Management System (SAMS), and the Cross-Pipeline Compatibility Protocol (CPCP).

## 2. System Architecture
The repository is organized into discrete domain pipelines, each containing specialized Skills, KIs, and Workflows.

### 2.1 Domain Pipelines
- **Bioinformatics_Pipeline**: Genomic and proteomic analysis.
- **Data_Analysis_Pipeline**: Statistical modeling and visualization.
- **Image_Processing_Pipeline**: CV and scientific imaging.
- **Writing_Publishing_Pipeline**: Academic manuscript and grant authoring.
- **[Full list in 00.RawData/PIPELINE_REGISTRY.md]**

### 2.2 Shared Assets (SAMS)
Assets located in \`01.Shared_Assets/\` are governed by SAMS. These are common utilities (e.g., \`pptx\`, \`word-read-write\`) used across multiple pipelines.

## 3. Governance Protocols
### 3.1 LAW 0: CPCP (Cross-Pipeline Compatibility Protocol)
Any modification to a shared asset REQUIRES:
1. Impact assessment across all consumer pipelines.
2. Logging in \`00.RawData/SHARED_ASSET_REGISTRY.md\`.
3. Forking if a breaking change is required for a specific pipeline.

### 3.2 LAW 1: Asset Deployment
All production deployments MUST use \`01.Shared_Assets/Scripts/deploy_to_aros.sh\`. Manual file movement to \`~/.gemini/\` is prohibited.

## 4. Self-Healing Environment (SHE)
The repository implements a SHE pattern using shell-based audits (\`audit_shared_assets.py\`) to ensure metadata integrity and path consistency.
