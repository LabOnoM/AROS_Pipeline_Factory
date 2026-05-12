#!/usr/bin/env bash
# =============================================================================
# deploy_to_aros.sh — AROS Pipeline Factory → AROS Runtime Deployer
# =============================================================================
#
# PURPOSE:
#   Deploys Skills, KIs, Policies, and Workflows from the AROS Pipeline Factory
#   repository to the canonical AROS runtime directories under ~/.gemini/.
#   This is the ONLY authorized deployment mechanism (SPEC §4.5).
#
# CANONICAL AROS RUNTIME DIRECTORY MAP:
#   Skills    → ~/.gemini/skills/<skill-name>/SKILL.md
#   KIs       → ~/.gemini/antigravity/knowledge/<ki-name>/
#   Policies  → ~/.gemini/antigravity/policies/<policy-name>.md
#   Workflows → ~/.gemini/antigravity/global_workflows/<workflow-name>.md
#
# USAGE:
#   ./deploy_to_aros.sh              # Full deployment
#   ./deploy_to_aros.sh --dry-run    # Preview without copying
#   ./deploy_to_aros.sh --verbose    # Show detailed rsync output
#   ./deploy_to_aros.sh --skills     # Deploy only skills
#   ./deploy_to_aros.sh --kis        # Deploy only KIs
#   ./deploy_to_aros.sh --policies   # Deploy only policies
#   ./deploy_to_aros.sh --workflows  # Deploy only workflows
#
# CROSS-PLATFORM:
#   Designed for Linux/macOS. Windows users should use WSL or Git Bash.
#   No POSIX symlinks. No sudo. All paths use $HOME expansion.
#
# PART OF: AROS Pipeline Factory (01.Shared_Assets/Scripts/)
# SPEC:    §4.5 AROS Runtime Directory Mapping
# =============================================================================

set -euo pipefail

# ── Constants ────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FACTORY_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# AROS Runtime Targets (canonical, hardcoded per SPEC §4.5)
AROS_SKILLS_DIR="${HOME}/.gemini/skills"
AROS_KI_DIR="${HOME}/.gemini/antigravity/knowledge"
AROS_POLICY_DIR="${HOME}/.gemini/antigravity/policies"
AROS_WORKFLOW_DIR="${HOME}/.gemini/antigravity/global_workflows"

# Flags
DRY_RUN=false
VERBOSE=false
DEPLOY_SKILLS=false
DEPLOY_KIS=false
DEPLOY_POLICIES=false
DEPLOY_WORKFLOWS=false
DEPLOY_ALL=true  # Default: deploy everything

# ── Colors ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ── Counters ─────────────────────────────────────────────────────────────────
SKILLS_DEPLOYED=0
KIS_DEPLOYED=0
POLICIES_DEPLOYED=0
WORKFLOWS_DEPLOYED=0
ERRORS=0

# ── Argument Parsing ─────────────────────────────────────────────────────────
for arg in "$@"; do
    case "$arg" in
        --dry-run)   DRY_RUN=true ;;
        --verbose)   VERBOSE=true ;;
        --skills)    DEPLOY_SKILLS=true;    DEPLOY_ALL=false ;;
        --kis)       DEPLOY_KIS=true;       DEPLOY_ALL=false ;;
        --policies)  DEPLOY_POLICIES=true;  DEPLOY_ALL=false ;;
        --workflows) DEPLOY_WORKFLOWS=true; DEPLOY_ALL=false ;;
        --help|-h)
            echo "Usage: deploy_to_aros.sh [--dry-run] [--verbose] [--skills] [--kis] [--policies] [--workflows]"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown argument: $arg${NC}"
            exit 1
            ;;
    esac
done

if $DEPLOY_ALL; then
    DEPLOY_SKILLS=true
    DEPLOY_KIS=true
    DEPLOY_POLICIES=true
    DEPLOY_WORKFLOWS=true
fi

# ── Utility Functions ────────────────────────────────────────────────────────

log_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; ERRORS=$((ERRORS + 1)); }
log_dry()   { echo -e "${CYAN}[DRY]${NC}   $1"; }

# copy_dir: Idempotent directory copy using rsync
# Args: $1=source_dir, $2=target_dir
copy_dir() {
    local src="$1"
    local dst="$2"

    if [ ! -d "$src" ]; then
        log_warn "Source directory does not exist: $src"
        return 1
    fi

    mkdir -p "$dst"

    if $DRY_RUN; then
        log_dry "Would rsync: $src → $dst"
        if $VERBOSE; then
            rsync -av --dry-run "$src/" "$dst/" 2>/dev/null || true
        fi
        return 0
    fi

    local rsync_flags="-a --delete"
    if $VERBOSE; then
        rsync_flags="-av --delete"
    fi

    # shellcheck disable=SC2086
    rsync $rsync_flags "$src/" "$dst/" 2>/dev/null
    return $?
}

# copy_file: Idempotent single-file copy
# Args: $1=source_file, $2=target_file
copy_file() {
    local src="$1"
    local dst="$2"

    if [ ! -f "$src" ]; then
        log_warn "Source file does not exist: $src"
        return 1
    fi

    mkdir -p "$(dirname "$dst")"

    if $DRY_RUN; then
        log_dry "Would copy: $src → $dst"
        return 0
    fi

    cp -f "$src" "$dst"
    return $?
}

# ── Banner ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║       AROS Pipeline Factory → Runtime Deployment Engine        ║${NC}"
echo -e "${CYAN}╠══════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║  Factory Root:  ${NC}${FACTORY_ROOT}"
echo -e "${CYAN}║  Skills:        ${NC}${AROS_SKILLS_DIR}"
echo -e "${CYAN}║  KIs:           ${NC}${AROS_KI_DIR}"
echo -e "${CYAN}║  Policies:      ${NC}${AROS_POLICY_DIR}"
echo -e "${CYAN}║  Workflows:     ${NC}${AROS_WORKFLOW_DIR}"
if $DRY_RUN; then
    echo -e "${CYAN}║  Mode:          ${YELLOW}DRY RUN (no files will be modified)${NC}"
fi
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ── Validate Factory Root ────────────────────────────────────────────────────
if [ ! -f "${FACTORY_ROOT}/SPEC.md" ]; then
    log_error "SPEC.md not found in factory root: ${FACTORY_ROOT}"
    log_error "This script must be run from within the AROS Pipeline Factory."
    exit 1
fi

# ── Phase 1: Deploy Skills ──────────────────────────────────────────────────
if $DEPLOY_SKILLS; then
    log_info "═══ Phase 1: Deploying Skills ═══"
    mkdir -p "$AROS_SKILLS_DIR"

    # Collect all pipeline skill directories
    PIPELINE_DIRS=(
        "${FACTORY_ROOT}/01.Shared_Assets/Skills"
        "${FACTORY_ROOT}/Grant_Write_Pipeline/Skills"
        "${FACTORY_ROOT}/Manuscript_Write_Pipeline/Skills"
        "${FACTORY_ROOT}/KAKENHI_Pipeline/Skills"
        "${FACTORY_ROOT}/workspace_management/Skills"
    )

    for pipeline_dir in "${PIPELINE_DIRS[@]}"; do
        if [ ! -d "$pipeline_dir" ]; then
            continue
        fi

        # Skills are directories containing SKILL.md
        for skill_dir in "$pipeline_dir"/*/; do
            [ -d "$skill_dir" ] || continue
            skill_name="$(basename "$skill_dir")"

            # Validate: must contain a SKILL.md
            if [ ! -f "${skill_dir}/SKILL.md" ]; then
                # Some skills use <name>_SKILL.md at the parent level (legacy format)
                log_warn "Skipping ${skill_name}: no SKILL.md found"
                continue
            fi

            if copy_dir "$skill_dir" "${AROS_SKILLS_DIR}/${skill_name}"; then
                log_ok "Skill: ${skill_name}"
                SKILLS_DEPLOYED=$((SKILLS_DEPLOYED + 1))
            else
                log_error "Failed to deploy skill: ${skill_name}"
            fi
        done

        # Handle legacy flat SKILL.md files (e.g., super-scientist_SKILL.md)
        for flat_skill in "$pipeline_dir"/*_SKILL.md; do
            [ -f "$flat_skill" ] || continue
            skill_basename="$(basename "$flat_skill" _SKILL.md)"
            target_dir="${AROS_SKILLS_DIR}/${skill_basename}"

            mkdir -p "$target_dir"
            if copy_file "$flat_skill" "${target_dir}/SKILL.md"; then
                log_ok "Skill (flat): ${skill_basename}"
                SKILLS_DEPLOYED=$((SKILLS_DEPLOYED + 1))
            else
                log_error "Failed to deploy flat skill: ${skill_basename}"
            fi
        done
    done
    echo ""
fi

# ── Phase 2: Deploy KIs ─────────────────────────────────────────────────────
if $DEPLOY_KIS; then
    log_info "═══ Phase 2: Deploying Knowledge Items ═══"
    mkdir -p "$AROS_KI_DIR"

    KI_DIRS=(
        "${FACTORY_ROOT}/01.Shared_Assets/KIs"
        "${FACTORY_ROOT}/Grant_Write_Pipeline/KIs"
        "${FACTORY_ROOT}/Manuscript_Write_Pipeline/KIs"
        "${FACTORY_ROOT}/KAKENHI_Pipeline/KIs"
        "${FACTORY_ROOT}/workspace_management/KIs"
    )

    for ki_source in "${KI_DIRS[@]}"; do
        if [ ! -d "$ki_source" ]; then
            continue
        fi

        # KIs are directories containing metadata.json and artifacts/
        for ki_dir in "$ki_source"/*/; do
            [ -d "$ki_dir" ] || continue
            ki_name="$(basename "$ki_dir")"

            if copy_dir "$ki_dir" "${AROS_KI_DIR}/${ki_name}"; then
                log_ok "KI: ${ki_name}"
                KIS_DEPLOYED=$((KIS_DEPLOYED + 1))
            else
                log_error "Failed to deploy KI: ${ki_name}"
            fi
        done

        # Handle flat KI files (legacy: e.g., research_discovery_templates.md)
        for flat_ki in "$ki_source"/*.md; do
            [ -f "$flat_ki" ] || continue
            ki_basename="$(basename "$flat_ki" .md)"

            # Skip if this is already deployed as a directory KI
            if [ -d "${AROS_KI_DIR}/${ki_basename}" ]; then
                continue
            fi

            # Create KI directory structure for flat files
            target_ki_dir="${AROS_KI_DIR}/${ki_basename}"
            mkdir -p "${target_ki_dir}/artifacts"

            if copy_file "$flat_ki" "${target_ki_dir}/artifacts/${ki_basename}.md"; then
                # Create minimal metadata.json if it doesn't exist
                if [ ! -f "${target_ki_dir}/metadata.json" ] && ! $DRY_RUN; then
                    cat > "${target_ki_dir}/metadata.json" <<EOF
{
    "name": "${ki_basename}",
    "summary": "Knowledge item imported from AROS Pipeline Factory",
    "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "source": "AROS_Pipeline_Factory",
    "artifacts": ["artifacts/${ki_basename}.md"]
}
EOF
                fi
                log_ok "KI (flat→structured): ${ki_basename}"
                KIS_DEPLOYED=$((KIS_DEPLOYED + 1))
            else
                log_error "Failed to deploy flat KI: ${ki_basename}"
            fi
        done

        # Handle flat KI Python/SPEC files (legacy: e.g., aros_batch_evolver.py)
        for flat_file in "$ki_source"/*.py "$ki_source"/*_SPEC.md; do
            [ -f "$flat_file" ] || continue
            file_basename="$(basename "$flat_file")"
            ki_name="${file_basename%.*}"

            # Skip if already deployed
            if [ -d "${AROS_KI_DIR}/${ki_name}" ]; then
                # Just add the file to existing KI artifacts
                if copy_file "$flat_file" "${AROS_KI_DIR}/${ki_name}/artifacts/${file_basename}"; then
                    log_ok "KI artifact: ${ki_name}/${file_basename}"
                fi
                continue
            fi

            target_ki_dir="${AROS_KI_DIR}/${ki_name}"
            mkdir -p "${target_ki_dir}/artifacts"

            if copy_file "$flat_file" "${target_ki_dir}/artifacts/${file_basename}"; then
                if [ ! -f "${target_ki_dir}/metadata.json" ] && ! $DRY_RUN; then
                    cat > "${target_ki_dir}/metadata.json" <<EOF
{
    "name": "${ki_name}",
    "summary": "Knowledge item imported from AROS Pipeline Factory",
    "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "source": "AROS_Pipeline_Factory",
    "artifacts": ["artifacts/${file_basename}"]
}
EOF
                fi
                log_ok "KI (flat→structured): ${ki_name}"
                KIS_DEPLOYED=$((KIS_DEPLOYED + 1))
            fi
        done
    done
    echo ""
fi

# ── Phase 3: Deploy Policies ────────────────────────────────────────────────
if $DEPLOY_POLICIES; then
    log_info "═══ Phase 3: Deploying Policies ═══"
    mkdir -p "$AROS_POLICY_DIR"

    POLICY_DIRS=(
        "${FACTORY_ROOT}/01.Shared_Assets/Policies"
        "${FACTORY_ROOT}/Grant_Write_Pipeline/Policies"
        "${FACTORY_ROOT}/Manuscript_Write_Pipeline/Policies"
        "${FACTORY_ROOT}/KAKENHI_Pipeline/Policies"
        "${FACTORY_ROOT}/workspace_management/Policies"
    )

    for policy_source in "${POLICY_DIRS[@]}"; do
        if [ ! -d "$policy_source" ]; then
            continue
        fi

        for policy_file in "$policy_source"/*.md; do
            [ -f "$policy_file" ] || continue
            policy_name="$(basename "$policy_file")"

            if copy_file "$policy_file" "${AROS_POLICY_DIR}/${policy_name}"; then
                log_ok "Policy: ${policy_name}"
                POLICIES_DEPLOYED=$((POLICIES_DEPLOYED + 1))
            else
                log_error "Failed to deploy policy: ${policy_name}"
            fi
        done
    done
    echo ""
fi

# ── Phase 4: Deploy Workflows ───────────────────────────────────────────────
if $DEPLOY_WORKFLOWS; then
    log_info "═══ Phase 4: Deploying Workflows ═══"
    mkdir -p "$AROS_WORKFLOW_DIR"

    WORKFLOW_DIRS=(
        "${FACTORY_ROOT}/workspace_management/Workflows"
        "${FACTORY_ROOT}/Grant_Write_Pipeline/Workflows"
        "${FACTORY_ROOT}/Manuscript_Write_Pipeline/Workflows"
        "${FACTORY_ROOT}/KAKENHI_Pipeline/Workflows"
    )

    for wf_source in "${WORKFLOW_DIRS[@]}"; do
        if [ ! -d "$wf_source" ]; then
            continue
        fi

        for wf_file in "$wf_source"/*.md; do
            [ -f "$wf_file" ] || continue
            wf_name="$(basename "$wf_file")"

            if copy_file "$wf_file" "${AROS_WORKFLOW_DIR}/${wf_name}"; then
                log_ok "Workflow: ${wf_name}"
                WORKFLOWS_DEPLOYED=$((WORKFLOWS_DEPLOYED + 1))
            else
                log_error "Failed to deploy workflow: ${wf_name}"
            fi
        done
    done
    echo ""
fi

# ── Summary Report ───────────────────────────────────────────────────────────
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                     Deployment Summary                         ║${NC}"
echo -e "${CYAN}╠══════════════════════════════════════════════════════════════════╣${NC}"
echo -e "${CYAN}║${NC}  Skills deployed:    ${GREEN}${SKILLS_DEPLOYED}${NC}"
echo -e "${CYAN}║${NC}  KIs deployed:       ${GREEN}${KIS_DEPLOYED}${NC}"
echo -e "${CYAN}║${NC}  Policies deployed:  ${GREEN}${POLICIES_DEPLOYED}${NC}"
echo -e "${CYAN}║${NC}  Workflows deployed: ${GREEN}${WORKFLOWS_DEPLOYED}${NC}"
echo -e "${CYAN}║${NC}  Errors:             ${RED}${ERRORS}${NC}"
if $DRY_RUN; then
    echo -e "${CYAN}║${NC}  Mode:               ${YELLOW}DRY RUN — no files modified${NC}"
fi
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"

if [ "$ERRORS" -gt 0 ]; then
    log_error "Deployment completed with ${ERRORS} error(s)."
    exit 1
fi

log_ok "Deployment complete! All assets synchronized to AROS runtime."
