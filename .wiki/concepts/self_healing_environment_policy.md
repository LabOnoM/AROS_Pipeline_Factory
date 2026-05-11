# Self-Healing Environment Policy

> **Type**: Institutional Policy / Infrastructure Standard
> **Applies To**: ALL Workflows, Skills, KIs, and Policies
> **Status**: MANDATORY
> **SPEC Reference**: §4.4
> **Last Updated**: 2026-05-12

## Summary
The Self-Healing Environment Policy mandates that no AROS workflow, skill, or KI may assume any external tool is pre-installed at the correct version. Every dependency invocation must follow the three-phase pattern:

1. **Detect** — Check tool existence AND version compatibility
2. **Repair** — Auto-install to user-local paths (`~/.local/`) without `sudo`
3. **Degrade Gracefully** — Log `[WARN]` and skip non-critical steps on failure

## Dependency Classification

| Level | Behavior on Failure | Examples |
|-------|---------------------|---------|
| CRITICAL | HALT workflow | `git`, `pandoc`, `python3` |
| IMPORTANT | Skip step, continue | `rgt`, `cairosvg`, `tectonic` |
| OPTIONAL | Silently skip | Obsidian symlink, syntax highlighting |

## Canonical Reference
Full policy with compliance checklist: `01.Shared_Assets/Policies/self_healing_environment_policy.md`

## Rationale
Created after `/wiki-update` and `/science-project-onboarding` failed on a machine running Go 1.14.12 (2020), which lacks the `io/fs` package required by `re_gent`. The bare `go install ...@latest` call crashed without recovery, halting the entire workflow.

## Related
- [[cross_pipeline_compatibility_protocol]] — CPCP governs shared asset modifications
- [[citation_before_claim_protocol]] — Another mandatory institutional policy
