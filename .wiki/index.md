# AROS Pipeline Factory - Wiki Index

Welcome to the knowledge base for the AROS Pipeline Factory. This wiki catalogs all multi-agent writing workflows.

## 📚 Domains
- [[Grant_Write_Pipeline]]
- [[KAKENHI_Pipeline]]
- [[Manuscript_Write_Pipeline]]

## 🔒 Governance
- [[cross_pipeline_compatibility_protocol]] — **SUPREME RULE**: The Cross-Pipeline Compatibility Protocol (CPCP)
- [[citation_before_claim_protocol]] — **MANDATORY**: Strict Grounding to prevent AI hallucinations during drafting
- [[self_healing_environment_policy]] — **MANDATORY**: Three-phase Detect→Repair→Degrade pattern for all external tool dependencies (SPEC §4.4)
- [[pipeline_registry_migration]] — Migration from INDEX.csv to PIPELINE_REGISTRY.md (Dynamic Registry Discovery)
- [[unified_diagramming]] — Standardized use of `visualize-data` for all scientific diagram generation
- `/audit-shared-assets` — Workflow to programmatically verify CPCP compliance

## 📖 Literature Ingestion
- `literature-ingestion` — Shared Skill: Tiered PDF retrieval (OA → LibGen → Sci-Hub) + opendataloader-pdf conversion
- `/literature-ingest` — Workflow: End-to-end pipeline (Download → Convert → Wiki Ingest → Commit)
- Raw data stored in `00.RawData/Literature/`

## ⚙️ System
- [[lessons-learned]]
