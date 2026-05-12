---
cpcp_asset: true
description: Conda-gated self-healing environment pattern for all AROS workflows, skills, and KIs.
version: "2.0.0"
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
> **Version**: 2.0.0 — Conda-Gated Architecture

## 1. Core Principle

No AROS workflow, skill, or KI **MAY** assume that any external tool, runtime, or library is pre-installed at the correct version on the host machine. All environment repair **MUST** be routed through the **Conda-Gated Self-Healing Pattern**:

| Level | Phase | Action |
|-------|-------|--------|
| **L0** | Bootstrap | Ensure `conda`/`miniconda` exists on the machine |
| **L1** | Detect + Repair | Activate the `aros-base` environment; create it from `aros-base.yml` if missing |
| **L2** | Degrade Gracefully | If conda repair fails (network, missing package), log `[WARN]` and skip non-critical steps |

## 2. Mandatory Rules

### 2.1 No Bare `install` Commands
```bash
# ❌ PROHIBITED — ad-hoc binary download
curl -fsSL https://go.dev/dl/go1.22.4.linux-amd64.tar.gz | tar -C ~/.local -xz

# ❌ PROHIBITED — bare pip outside conda env
pip install --user some-package

# ❌ PROHIBITED — assumes Go is installed
go install github.com/some/tool@latest

# ✅ REQUIRED — Conda-gated installation
conda activate aros-base
mamba install -n aros-base some-package -c conda-forge -y
```

### 2.2 Minimum Version Requirements
- **Conda**: ≥ 23.0
- **Mamba**: ≥ 1.0 (RECOMMENDED for speed; fall back to `conda` if unavailable)
- **Python**: ≥ 3.10 (managed by `aros-base.yml`)

### 2.3 Mamba Preference
Mamba is a drop-in replacement for `conda` with 10–100× faster dependency resolution. All workflows **SHOULD** prefer `mamba` over `conda` for `create`, `install`, and `update` operations:
```bash
CMD=$(command -v mamba &>/dev/null && echo "mamba" || echo "conda")
$CMD install -n aros-base some-package -c conda-forge -y
```

### 2.4 User-Local Installation Paths
All tools managed by conda live inside the conda environment prefix:
- **Conda environments**: `$HOME/miniconda3/envs/aros-base/`
- **Conda binaries**: `$CONDA_PREFIX/bin/`
- **Compiled tools** (e.g., `rgt`): `GOBIN=$CONDA_PREFIX/bin go install ...`

Legacy paths (`~/.local/bin/`, `~/go/bin/`) are acceptable ONLY as a fallback when conda is unavailable.

### 2.5 Graceful Degradation Levels
Not all dependencies are equally critical. Workflows MUST classify each dependency:

| Level | Behavior on Failure | Example |
|-------|---------------------|---------|
| **CRITICAL** | HALT the workflow with a clear error message | `git` for `/lab-commit`, `pandoc` for conversion |
| **IMPORTANT** | Log `[WARN]`, skip the step, continue workflow | `rgt` for re_gent auditing, `tectonic` for PDF |
| **OPTIONAL** | Log `[INFO]`, silently skip | `obsidian` symlink, syntax highlighting tools |

### 2.6 Network Failure Resilience
Auto-installation steps that require network access MUST:
1. Set a reasonable timeout (e.g., `curl --max-time 120`)
2. Check the exit code of the download
3. Fall back to the existing conda environment if available
4. Never leave partial downloads or corrupted archives on failure

## 3. Canonical Bootstrap Snippets

### 3.1 Level 0: Ensure Conda Exists
```bash
# --- L0: Conda Bootstrap ---
if ! command -v conda &> /dev/null; then
    # Check common install paths (non-interactive shells may not source ~/.bashrc)
    if [ -f "$HOME/miniconda3/bin/conda" ]; then
        eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    elif [ -f "$HOME/anaconda3/bin/conda" ]; then
        eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
    else
        echo "  [WARN] Conda not found. Bootstrapping Miniconda3..."
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-$(uname -m).sh"
        curl -fsSL --max-time 120 "$MINICONDA_URL" -o /tmp/miniconda.sh && \
            bash /tmp/miniconda.sh -b -u -p "$HOME/miniconda3" && \
            eval "$($HOME/miniconda3/bin/conda shell.bash hook)" && \
            rm -f /tmp/miniconda.sh || {
                echo "  [WARN] Miniconda bootstrap failed. Falling back to legacy paths."
            }
    fi
fi
```

### 3.2 Level 1: Activate or Create `aros-base`
```bash
# --- L1: Activate aros-base ---
eval "$(conda shell.bash hook)"
if ! conda activate aros-base 2>/dev/null; then
    echo "  [WARN] aros-base environment missing. Creating..."
    AROS_YML="01.Shared_Assets/Environments/aros-base.yml"
    # Locate aros-base.yml in workspace or factory
    [ ! -f "$AROS_YML" ] && AROS_YML="$(find ~ -maxdepth 4 -name 'aros-base.yml' -print -quit 2>/dev/null)"
    CMD=$(command -v mamba &>/dev/null && echo "mamba" || echo "conda")
    if [ -n "$AROS_YML" ]; then
        $CMD env create -f "$AROS_YML" -y && conda activate aros-base
    else
        echo "  [WARN] aros-base.yml not found. Creating minimal environment..."
        $CMD create -n aros-base python=3.11 git pandoc -c conda-forge -y && conda activate aros-base
    fi
fi
```

### 3.3 Level 2: Installing Non-Conda Tools
```bash
# --- L2: Compiled tool (e.g., re_gent) into conda env ---
if ! command -v rgt &> /dev/null; then
    if command -v go &> /dev/null; then
        GOBIN="$CONDA_PREFIX/bin" go install github.com/regent-vcs/regent/cmd/rgt@latest 2>/dev/null || \
            echo "  [WARN] rgt compilation failed. Continuing without re_gent."
    else
        echo "  [WARN] Go not available. Skipping rgt installation."
    fi
fi
```

## 4. Compliance Checklist for New Assets

When creating or reviewing any new Workflow, Skill, KI, or Policy, verify:

- [ ] External tool dependencies are satisfied via `aros-base.yml` (not bare downloads)
- [ ] Workflow preflight includes L0 (conda bootstrap) and L1 (env activation)
- [ ] `mamba` is preferred over `conda` with automatic fallback
- [ ] Each dependency is classified as CRITICAL / IMPORTANT / OPTIONAL
- [ ] Failure of IMPORTANT/OPTIONAL deps does not halt the workflow
- [ ] Network-dependent steps have timeout and failure handling
- [ ] The step logs its self-healing actions with `[WARN]` / `[INFO]` prefixes
- [ ] No `sudo`, no system-wide package manager assumptions
- [ ] Compiled binaries target `$CONDA_PREFIX/bin` (not `~/.local/bin/`)

## 5. Reference Implementation

The canonical reference implementation is the `/wiki-update` workflow (Step 1.5), which demonstrates the full L0→L1→L2 pattern: conda bootstrap → `aros-base` activation → `rgt` compilation into `$CONDA_PREFIX/bin`.

## 6. Rationale

**v1.0** (2026-05-12): Created after `/wiki-update` and `/science-project-onboarding` failed on a machine with Go 1.14.12. Ad-hoc binary bootstrapping was fragile and non-reproducible.

**v2.0** (2026-05-12): Upgraded to Conda-gated architecture. All ad-hoc downloads replaced by a single `aros-base.yml` environment specification. Mamba preferred for speed. `$CONDA_PREFIX/bin` replaces `~/.local/bin/` as the canonical binary target.
