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

## Structural Enforcement (SAMS v1.1)
As of 2026-05-11, the CPCP is programmatically enforced via the **Shared Asset Management System (SAMS)**:
1. **Centralization**: All shared assets live canonically in `01.Shared_Assets/`.
2. **Direct Referencing**: Pipeline-specific references to shared assets must point natively to `01.Shared_Assets/`. Physical duplicates are strictly banned to maintain Windows cross-platform compatibility.
3. **Pre-Commit Hook**: A `.git/hooks/pre-commit` script blocks commits that modify `01.Shared_Assets/` without also staging updates to `SHARED_ASSET_REGISTRY.md`.
4. **Audit Workflow**: The `/audit-shared-assets` workflow programmatically verifies deduplication, YAML frontmatter (`cpcp_asset: true`), and the pre-commit hook.

> **✅ CROSS-PLATFORM COMPATIBLE**
> SAMS v1.1 removed POSIX symlinks. This repository is fully operational on Windows, macOS, and Linux.

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
