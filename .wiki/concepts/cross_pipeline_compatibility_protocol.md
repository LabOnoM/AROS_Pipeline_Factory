# Cross-Pipeline Compatibility Protocol (CPCP)

> **Status**: ACTIVE — LAW 0 in `AGENTS.md`
> **Registry**: `00.RawData/SHARED_ASSET_REGISTRY.md`
> **Established**: 2026-05-11

## Summary

The CPCP is the supreme governance rule for the AROS Pipeline Factory. It ensures that shared KIs, Skills, Policies, and Workflows are never modified in isolation when they are consumed by multiple pipelines.

## Protocol Steps

1. **EVALUATE** — Read the asset's usage in all consuming pipelines
2. **ESTIMATE IMPACT** — Produce a compatibility assessment per consumer
3. **TEST** — Verify no breakage in any consuming pipeline
4. **RESOLVE OR FORK** — If conflict is unresolvable, create a pipeline-specific variant
5. **UPDATE REGISTRY** — Record all changes in `SHARED_ASSET_REGISTRY.md`

## Shared Assets (Current)

### Shared KIs
- [[agentic_manuscript_publishing]] → Grant_Write + Manuscript_Write
- [[markdown_first_manuscript_policy]] → Grant_Write + Manuscript_Write
- [[grant_funder_profiles]] → Grant_Write + KAKENHI (implicit)
- [[kakenhi_management_pipeline]] → KAKENHI + workspace_management
- [[publication_grant_map]] → KAKENHI + Grant_Write (implicit)

### Shared Workflows (via workspace_management)
- `/lab-commit` → ALL pipelines
- `/lab-reorganize` → ALL pipelines
- `/wiki-build`, `/wiki-ingest`, `/wiki-query`, `/wiki-research`, `/wiki-update` → ALL pipelines
- `/science-project-onboarding` → ALL pipelines

### Shared Policies
- `gepa_protocol.md` → Grant_Write + workspace_management
- `output-truncation-management.md` → ALL pipelines
- `fact_check_policy.md` → KAKENHI + Grant_Write (implicit)

## See Also
- [[system/lessons-learned]] — Operational evolution log
