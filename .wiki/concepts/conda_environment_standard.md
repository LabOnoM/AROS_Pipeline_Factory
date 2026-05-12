# Conda Environment Standard

> **Type**: Infrastructure Standard
> **Applies To**: ALL AROS Pipeline Factory environments
> **Status**: MANDATORY
> **SPEC Reference**: §4.4
> **Last Updated**: 2026-05-12

## Summary
The `aros-base` conda environment is the canonical shared toolchain for all AROS workflows. It replaces ad-hoc binary downloads and ensures reproducible, portable environments across machines.

## Location
`01.Shared_Assets/Environments/aros-base.yml`

## Core Dependencies
- Python ≥ 3.10, Git ≥ 2.30, Pandoc ≥ 3.1, Go ≥ 1.22, Node.js ≥ 18
- Scientific Python: numpy, scipy, matplotlib, seaborn, pandas, openpyxl
- Document generation: python-docx, tectonic, cairosvg

## Usage
```bash
# First-time creation (prefer mamba for speed)
mamba env create -f 01.Shared_Assets/Environments/aros-base.yml

# Activation (auto-handled by workflow preflights)
conda activate aros-base

# Update after aros-base.yml changes
mamba env update -f 01.Shared_Assets/Environments/aros-base.yml --prune
```

## Architecture: L0 → L1 → L2
1. **L0**: Bootstrap conda/miniconda if absent
2. **L1**: Create and activate `aros-base` from `aros-base.yml`
3. **L2**: Install workflow-specific tools into `$CONDA_PREFIX/bin`

## Related
- [[self_healing_environment_policy]] — The governing policy (v2.0)
- [[cross_pipeline_compatibility_protocol]] — CPCP governs shared asset modifications
