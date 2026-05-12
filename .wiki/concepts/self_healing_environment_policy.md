# Self-Healing Environment Policy

> **Type**: Institutional Policy / Infrastructure Standard
> **Applies To**: ALL Workflows, Skills, KIs, and Policies
> **Status**: MANDATORY
> **SPEC Reference**: §4.4
> **Version**: 2.0.0 — Conda-Gated Architecture
> **Last Updated**: 2026-05-12

## Summary
The Self-Healing Environment Policy mandates that no AROS workflow, skill, or KI may assume any external tool is pre-installed at the correct version. All environment repair MUST be routed through the **Conda-Gated Self-Healing Pattern**:

| Level | Phase | Action |
|-------|-------|--------|
| **L0** | Bootstrap | Ensure `conda`/`miniconda` exists on the machine |
| **L1** | Detect + Repair | Activate `aros-base` environment; create from `aros-base.yml` if missing |
| **L2** | Degrade Gracefully | Log `[WARN]` and skip non-critical steps on failure |

## Key Rules
- **Mamba preferred** (≥ 1.0) over conda (≥ 23.0) for speed
- **No bare installs**: No `pip install --user`, `go install`, or `curl` downloads outside conda
- **Binary target**: `$CONDA_PREFIX/bin` replaces `~/.local/bin/`
- **Environment file**: `01.Shared_Assets/Environments/aros-base.yml`

## Dependency Classification

| Level | Behavior on Failure | Examples |
|-------|---------------------|---------|
| CRITICAL | HALT workflow | `git`, `pandoc`, `python3` |
| IMPORTANT | Skip step, continue | `rgt`, `cairosvg`, `tectonic` |
| OPTIONAL | Silently skip | Obsidian symlink, syntax highlighting |

## Canonical Reference
Full policy with compliance checklist: `01.Shared_Assets/Policies/self_healing_environment_policy.md`

## History
- **v1.0** (2026-05-12): Created after Go 1.14.12 failures with ad-hoc binary bootstrapping
- **v2.0** (2026-05-12): Upgraded to Conda-gated L0/L1/L2 architecture

## Related
- [[conda_environment_standard]] — The aros-base environment definition
- [[cross_pipeline_compatibility_protocol]] — CPCP governs shared asset modifications
- [[citation_before_claim_protocol]] — Another mandatory institutional policy
