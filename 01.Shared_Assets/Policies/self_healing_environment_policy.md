---
cpcp_asset: true
description: Mandatory self-healing environment pattern for all AROS workflows, skills, and KIs that depend on external tools.
version: "1.0.0"
date: "2026-05-12"
status: MANDATORY
consumers:
  - ALL PIPELINES
---

# Self-Healing Environment Policy

> **Type**: Institutional Policy / Infrastructure Standard
> **Applies To**: ALL Workflows, Skills, KIs, and Policies that invoke external CLI tools
> **Status**: MANDATORY
> **SPEC Reference**: §4.4

## 1. Core Principle

No AROS workflow, skill, or KI **MAY** assume that any external tool, runtime, or library is pre-installed at the correct version on the host machine. Every dependency invocation MUST follow the **three-phase Self-Healing Environment Pattern**:

| Phase | Action | Behavior |
|-------|--------|----------|
| **Detect** | Check if the tool exists AND if its version meets the minimum requirement | Use `command -v`, version parsing, and semantic comparison |
| **Repair** | If missing or incompatible, auto-install to a user-local directory (`~/.local/`) | No `sudo`, no system-wide changes, no package manager assumptions |
| **Degrade Gracefully** | If repair fails (e.g., no network, compilation error), log `[WARN]` and skip the non-critical step | Never halt an entire workflow for an optional dependency |

## 2. Mandatory Rules

### 2.1 No Bare `install` Commands
```bash
# ❌ PROHIBITED — assumes Go is installed AND is modern enough
go install github.com/some/tool@latest

# ❌ PROHIBITED — assumes pip is the right pip
pip install some-package

# ✅ REQUIRED — Detect → Repair → Degrade
if ! command -v tool &> /dev/null; then
    echo "  [WARN] tool not found. Attempting installation..."
    # ... version-aware bootstrap logic ...
fi
```

### 2.2 Version-Aware Checks
When a tool requires a minimum version (e.g., Go ≥ 1.16 for `io/fs`), the workflow MUST parse the installed version and compare it semantically:
```bash
_version_gte() {
    [ "$(printf '%s\n%s' "$1" "$2" | sort -V | head -n1)" = "$2" ]
}
TOOL_VER=$(tool --version 2>/dev/null | grep -oP '[0-9]+\.[0-9]+(\.[0-9]+)?' || echo "0.0")
if ! _version_gte "$TOOL_VER" "$MIN_VERSION"; then
    echo "  [WARN] tool $TOOL_VER is too old (need >= $MIN_VERSION). Bootstrapping..."
    # ... auto-install logic ...
fi
```

### 2.3 User-Local Installation Paths
All auto-installed tools MUST use user-writable directories:
- **Go toolchains**: `~/.local/go/`
- **Go binaries**: `~/go/bin/`
- **Python tools**: `~/.local/bin/` via `pip install --user`
- **Node.js tools**: `npx -y` (ephemeral) or `~/.local/share/npm/`
- **Downloaded binaries**: `~/.local/bin/`

### 2.4 Graceful Degradation Levels
Not all dependencies are equally critical. Workflows MUST classify each dependency:

| Level | Behavior on Failure | Example |
|-------|---------------------|---------|
| **CRITICAL** | HALT the workflow with a clear error message | `git` for `/lab-commit`, `pandoc` for manuscript conversion |
| **IMPORTANT** | Log `[WARN]`, skip the step, continue workflow | `rgt` for re_gent auditing, `cairosvg` for PNG rendering |
| **OPTIONAL** | Log `[INFO]`, silently skip | `obsidian` symlink, syntax highlighting tools |

### 2.5 Network Failure Resilience
Auto-installation steps that require network access MUST:
1. Set a reasonable timeout (e.g., `curl --max-time 30`)
2. Check the exit code of the download
3. Fall back to cached binaries if available (e.g., `~/.local/go/bin/go`)
4. Never leave partial downloads or corrupted archives on failure

## 3. Compliance Checklist for New Assets

When creating or reviewing any new Workflow, Skill, KI, or Policy, verify:

- [ ] Every `command -v` / `which` check is followed by version validation
- [ ] Every `install` command is wrapped in detection + repair logic
- [ ] Installation targets are user-local (`~/.local/`, `~/go/bin/`)
- [ ] Network-dependent steps have timeout and failure handling
- [ ] Each dependency is classified as CRITICAL / IMPORTANT / OPTIONAL
- [ ] Failure of IMPORTANT/OPTIONAL deps does not halt the workflow
- [ ] The step logs its self-healing actions with `[WARN]` / `[INFO]` prefixes

## 4. Reference Implementation

The canonical reference implementation is `/wiki-update` Step 1.5 (re_gent deployment), which demonstrates the full three-phase pattern for a Go-compiled tool on a machine with an outdated Go compiler.

## 5. Rationale

This policy was created after the `/wiki-update` and `/science-project-onboarding` workflows failed silently on a machine running Go 1.14.12 (2020), which lacks the `io/fs` package required by `re_gent`. The `go install ...@latest` command failed with a cryptic compiler error, halting the entire workflow without any recovery attempt.

The Self-Healing Environment Pattern ensures that AROS workflows are **portable across machines** with varying tool installations, without requiring manual environment setup by the researcher.
