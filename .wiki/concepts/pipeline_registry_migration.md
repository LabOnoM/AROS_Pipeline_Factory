# Pipeline Registry Migration

## Summary
On 2026-05-11, the AROS Pipeline Factory migrated from the generic `00.RawData/INDEX.csv` (a biological assay tracking format inherited from the standard AROS project template) to a purpose-built `00.RawData/PIPELINE_REGISTRY.md`.

## Rationale
The Factory is not a biological laboratory workspace — it is a meta-project that forges AROS pipeline assets (Skills, Workflows, KIs, Policies). The `INDEX.csv` with columns like `Folder,Date,Phase,Assay,Conditions,CellLine,Status,Notes` was semantically irrelevant.

## Impact
- **Factory Level**: `INDEX.csv` was deleted; `PIPELINE_REGISTRY.md` was created.
- **Upstream Templates**: All 7 workflow templates in `workspace_management/Workflows/` and `Manuscript_Write_Pipeline/Workflows/` were generalized to reference "the Project Registry (e.g., INDEX.csv or PIPELINE_REGISTRY.md)" instead of hardcoding `INDEX.csv`.
- **Bash Scripts**: All bash scripts in `/project-organize` now use **Dynamic Registry Discovery** to detect the appropriate registry format at runtime.
- **Cross-Platform**: The `regent_to_aros_bridge.py` script was fixed to use `os.path.expanduser("~")` instead of a hardcoded absolute path.

## Dynamic Registry Discovery Pattern
```bash
if [ -f "00.RawData/INDEX.csv" ]; then
    REGISTRY_FILE="00.RawData/INDEX.csv"
elif [ -f "00.RawData/PIPELINE_REGISTRY.md" ]; then
    REGISTRY_FILE="00.RawData/PIPELINE_REGISTRY.md"
else
    REGISTRY_FILE=""
fi
```

## Related
- [[cross_pipeline_compatibility_protocol]]
- See: `SPEC.md` §9 — Pipeline Registry & Dynamic Discovery
