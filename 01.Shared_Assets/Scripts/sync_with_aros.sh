#!/usr/bin/env bash
# =============================================================================
# sync_with_aros.sh — Bidirectional AROS Pipeline Factory ↔ AROS Runtime Sync
# =============================================================================
#
# PURPOSE:
#   Synchronizes Skills, KIs, Policies, and Workflows bidirectionally between 
#   the Git-tracked Pipeline Factory and the live AROS runtime (~/.gemini/).
#
# V2 ARCHITECTURE COMPATIBILITY:
#   Supports the dual-backend design of Google Antigravity v2:
#     - IDE Workspace (Screener): ~/.gemini/antigravity-ide/knowledge/
#     - Agent Workspace (Runtime): ~/.gemini/antigravity/knowledge/
#   Legacy flat Policies and Workflows are automatically wrapped into valid V2
#   Knowledge Item (KI) structured directories (metadata.json + artifacts/)
#   upon push to satisfy ambient workspace policies.
#
# USAGE:
#   ./sync_with_aros.sh status           # Show staleness report
#   ./sync_with_aros.sh push             # Factory → Runtime
#   ./sync_with_aros.sh pull             # Runtime → Factory (GEPA mutations)
#   ./sync_with_aros.sh diff <type> <name> # Show diverged changes
#
# FLAGS:
#   --dry-run      Preview without modifying files
#   --import-all   (pull only) Pull runtime assets not tracked in Factory
#   --skills       Only process skills
#   --kis          Only process KIs
#   --policies     Only process policies
#   --workflows    Only process workflows
#
# PART OF: AROS Pipeline Factory (01.Shared_Assets/Scripts/)
# SPEC:    §4.5 AROS Runtime Directory Mapping
# =============================================================================

set -euo pipefail

# ── Constants ────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FACTORY_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

AROS_SKILLS_DIR="${HOME}/.gemini/skills"
AROS_KI_DIR="${HOME}/.gemini/antigravity-ide/knowledge"
AROS_KI_DIR_AGENT="${HOME}/.gemini/antigravity/knowledge"

PIPELINE_DIRS=(
    "${FACTORY_ROOT}/01.Shared_Assets"
    "${FACTORY_ROOT}/Grant_Write_Pipeline"
    "${FACTORY_ROOT}/Manuscript_Write_Pipeline"
    "${FACTORY_ROOT}/KAKENHI_Pipeline"
    "${FACTORY_ROOT}/workspace_management"
)

# ── Colors ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ── Globals ──────────────────────────────────────────────────────────────────
COMMAND=""
DRY_RUN=false
VERBOSE=false
IMPORT_ALL=false
FILTER_SKILLS=false
FILTER_KIS=false
FILTER_POLICIES=false
FILTER_WORKFLOWS=false
FILTER_ALL=true

declare -A ASSET_MAP_FACTORY
declare -A ASSET_MAP_RUNTIME
declare -A ASSET_MAP_STATUS # IN_SYNC, RUNTIME_MISSING, FACTORY_MISSING, FACTORY_STALE, RUNTIME_STALE
declare -A ASSET_MAP_LEGACY

# ── Argument Parsing ─────────────────────────────────────────────────────────
if [ $# -eq 0 ]; then
    echo "Usage: $0 {status|push|pull|diff} [options]"
    exit 1
fi

COMMAND="$1"
shift

for arg in "$@"; do
    case "$arg" in
        --dry-run)   DRY_RUN=true ;;
        --verbose)   VERBOSE=true ;;
        --import-all) IMPORT_ALL=true ;;
        --skills)    FILTER_SKILLS=true;    FILTER_ALL=false ;;
        --kis)       FILTER_KIS=true;       FILTER_ALL=false ;;
        --policies)  FILTER_POLICIES=true;  FILTER_ALL=false ;;
        --workflows) FILTER_WORKFLOWS=true; FILTER_ALL=false ;;
        *)
            if [[ "$COMMAND" == "diff" && -z "${DIFF_TYPE:-}" ]]; then
                DIFF_TYPE="$arg"
            elif [[ "$COMMAND" == "diff" && -z "${DIFF_NAME:-}" ]]; then
                DIFF_NAME="$arg"
            else
                echo -e "${RED}Unknown argument: $arg${NC}"
                exit 1
            fi
            ;;
    esac
done

if $FILTER_ALL; then
    FILTER_SKILLS=true
    FILTER_KIS=true
    FILTER_POLICIES=true
    FILTER_WORKFLOWS=true
fi

# ── Utility Functions ────────────────────────────────────────────────────────
log_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_dry()   { echo -e "${CYAN}[DRY]${NC}   $1"; }

get_sha256() {
    local target="$1"
    if [ -f "$target" ]; then
        sha256sum "$target" | cut -d' ' -f1
    elif [ -d "$target" ]; then
        # For directories, hash the content of all files inside sorted. Use relative paths!
        (cd "$target" && find . -type f -exec sha256sum {} + | sort | sha256sum | cut -d' ' -f1)
    else
        echo "MISSING"
    fi
}

compare_assets() {
    local id="$1"
    local f_path="$2"
    local r_path="$3"
    local is_legacy="${4:-false}"
    
    # Prevent overwriting if already mapped (e.g. duplicate in another pipeline dir)
    if [[ -n "${ASSET_MAP_STATUS[$id]:-}" ]]; then
        return
    fi
    
    local f_hash
    local r_hash
    f_hash=$(get_sha256 "$f_path")
    r_hash=$(get_sha256 "$r_path")
    
    ASSET_MAP_FACTORY["$id"]="$f_path"
    ASSET_MAP_RUNTIME["$id"]="$r_path"
    ASSET_MAP_LEGACY["$id"]="$is_legacy"
    
    if [[ "$f_hash" == "MISSING" && "$r_hash" == "MISSING" ]]; then
        return
    elif [[ "$f_hash" == "MISSING" ]]; then
        ASSET_MAP_STATUS["$id"]="FACTORY_MISSING"
    elif [[ "$r_hash" == "MISSING" ]]; then
        ASSET_MAP_STATUS["$id"]="RUNTIME_MISSING"
    elif [[ "$f_hash" == "$r_hash" ]]; then
        ASSET_MAP_STATUS["$id"]="IN_SYNC"
    else
        # Diverged. Compare mtime to determine staleness direction.
        # For directories, get newest mtime.
        local f_ts r_ts
        if [ -d "$f_path" ]; then
            f_ts=$(find "$f_path" -type f -printf '%T@\n' | sort -n | tail -1 | cut -d. -f1)
        else
            f_ts=$(stat -c '%Y' "$f_path")
        fi
        
        if [ -d "$r_path" ]; then
            r_ts=$(find "$r_path" -type f -printf '%T@\n' | sort -n | tail -1 | cut -d. -f1)
        else
            r_ts=$(stat -c '%Y' "$r_path")
        fi
        
        # Ensure we have defaults if find returns empty
        f_ts=${f_ts:-0}
        r_ts=${r_ts:-0}
        
        if [ "$f_ts" -gt "$r_ts" ]; then
            ASSET_MAP_STATUS["$id"]="RUNTIME_STALE"
        else
            ASSET_MAP_STATUS["$id"]="FACTORY_STALE"
        fi
    fi
}

# ── Asset Discovery Engine ───────────────────────────────────────────────────
discover_skills() {
    local type_id="SKL"
    
    # 1. Discover from Factory
    for pipeline_dir in "${PIPELINE_DIRS[@]}"; do
        [ -d "$pipeline_dir/Skills" ] || continue
        
        # Structured skills
        for skill_dir in "$pipeline_dir/Skills"/*/; do
            [ -d "$skill_dir" ] || continue
            local name
            name=$(basename "$skill_dir")
            local f_path="${skill_dir}SKILL.md"
            [ -f "$f_path" ] || continue
            local r_path="${AROS_SKILLS_DIR}/${name}/SKILL.md"
            compare_assets "${type_id}:${name}" "$f_path" "$r_path" "false"
        done
        
        # Legacy flat skills
        for flat_skill in "$pipeline_dir/Skills"/*_SKILL.md; do
            [ -f "$flat_skill" ] || continue
            local name
            name=$(basename "$flat_skill" _SKILL.md)
            local r_path="${AROS_SKILLS_DIR}/${name}/SKILL.md"
            compare_assets "${type_id}:${name}" "$flat_skill" "$r_path" "true"
        done
    done
    
    # 2. Discover from Runtime (catch FACTORY_MISSING)
    [ -d "$AROS_SKILLS_DIR" ] || return
    for skill_dir in "$AROS_SKILLS_DIR"/*/; do
        [ -d "$skill_dir" ] || continue
        local name
        name=$(basename "$skill_dir")
        local id="${type_id}:${name}"
        if [[ -z "${ASSET_MAP_STATUS[$id]:-}" ]]; then
            compare_assets "$id" "/dev/null" "${skill_dir}SKILL.md" "false"
        fi
    done
}

discover_kis() {
    local type_id="KI"
    
    # 1. Discover from Factory
    for pipeline_dir in "${PIPELINE_DIRS[@]}"; do
        [ -d "$pipeline_dir/KIs" ] || continue
        
        # Structured KIs
        for ki_dir in "$pipeline_dir/KIs"/*/; do
            [ -d "$ki_dir" ] || continue
            local name
            name=$(basename "$ki_dir")
            local r_path="${AROS_KI_DIR}/${name}"
            compare_assets "${type_id}:${name}" "$ki_dir" "$r_path" "false"
        done
        
        # Legacy flat KIs (simplification for hash mapping)
        # We flag them, but hash comparison for flat vs dir is hard.
        for flat_ki in "$pipeline_dir/KIs"/*.md; do
            [ -f "$flat_ki" ] || continue
            local name
            name=$(basename "$flat_ki" .md)
            local id="${type_id}:${name}"
            if [[ -z "${ASSET_MAP_STATUS[$id]:-}" ]]; then
                ASSET_MAP_FACTORY["$id"]="$flat_ki"
                ASSET_MAP_RUNTIME["$id"]="${AROS_KI_DIR}/${name}"
                ASSET_MAP_LEGACY["$id"]="true"
                # Always mark legacy as diverged if runtime exists to force user migration
                if [ -d "${AROS_KI_DIR}/${name}" ]; then
                    ASSET_MAP_STATUS["$id"]="RUNTIME_STALE" # Legacy always needs factory fix
                else
                    ASSET_MAP_STATUS["$id"]="RUNTIME_MISSING"
                fi
            fi
        done
    done
    
    # 2. Discover from Runtime
    [ -d "$AROS_KI_DIR" ] || return
    for ki_dir in "$AROS_KI_DIR"/*/; do
        [ -d "$ki_dir" ] || continue
        local name
        name=$(basename "$ki_dir")
        local id="${type_id}:${name}"
        if [[ -z "${ASSET_MAP_STATUS[$id]:-}" ]]; then
            compare_assets "$id" "/dev/null" "$ki_dir" "false"
        fi
    done
}

discover_policies() {
    local type_id="POL"
    
    # Factory
    for pipeline_dir in "${PIPELINE_DIRS[@]}"; do
        [ -d "$pipeline_dir/Policies" ] || continue
        for p_file in "$pipeline_dir/Policies"/*.md; do
            [ -f "$p_file" ] || continue
            local name
            name=$(basename "$p_file")
            local bare_name="${name%.md}"
            local r_path="${AROS_KI_DIR}/policy_${bare_name}/artifacts/${name}"
            compare_assets "${type_id}:${name}" "$p_file" "$r_path" "false"
        done
    done
    
    # Runtime
    [ -d "$AROS_KI_DIR" ] || return
    for p_dir in "$AROS_KI_DIR"/policy_*; do
        [ -d "$p_dir" ] || continue
        local name="${p_dir##*/policy_}"
        name="${name}.md"
        local id="${type_id}:${name}"
        if [[ -z "${ASSET_MAP_STATUS[$id]:-}" ]]; then
            compare_assets "$id" "/dev/null" "${p_dir}/artifacts/${name}" "false"
        fi
    done
}

discover_workflows() {
    local type_id="WF"
    
    # Factory
    for pipeline_dir in "${PIPELINE_DIRS[@]}"; do
        [ -d "$pipeline_dir/Workflows" ] || continue
        for w_file in "$pipeline_dir/Workflows"/*.md; do
            [ -f "$w_file" ] || continue
            local name
            name=$(basename "$w_file")
            local bare_name="${name%.md}"
            local r_path="${AROS_KI_DIR}/workflow_${bare_name}/artifacts/${name}"
            compare_assets "${type_id}:${name}" "$w_file" "$r_path" "false"
        done
    done
    
    # Runtime
    [ -d "$AROS_KI_DIR" ] || return
    for w_dir in "$AROS_KI_DIR"/workflow_*; do
        [ -d "$w_dir" ] || continue
        local name="${w_dir##*/workflow_}"
        name="${name}.md"
        local id="${type_id}:${name}"
        if [[ -z "${ASSET_MAP_STATUS[$id]:-}" ]]; then
            compare_assets "$id" "/dev/null" "${w_dir}/artifacts/${name}" "false"
        fi
    done
}

populate_asset_maps() {
    $FILTER_SKILLS && discover_skills
    $FILTER_KIS && discover_kis
    $FILTER_POLICIES && discover_policies
    $FILTER_WORKFLOWS && discover_workflows
}

# ── Commands ─────────────────────────────────────────────────────────────────

cmd_status() {
    local sync=0
    local push=0
    local pull=0
    local f_only=0
    local r_only=0
    
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║             AROS Sync Status Report                              ║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════════════════════════════════╣${NC}"
    
    # Group by status to print cleanly
    for id in "${!ASSET_MAP_STATUS[@]}"; do
        local st="${ASSET_MAP_STATUS[$id]}"
        if [[ "$st" == "IN_SYNC" ]]; then sync=$((sync + 1)); fi
        if [[ "$st" == "RUNTIME_MISSING" ]]; then push=$((push + 1)); f_only=$((f_only + 1)); fi
        if [[ "$st" == "RUNTIME_STALE" ]]; then push=$((push + 1)); fi
        if [[ "$st" == "FACTORY_MISSING" ]]; then r_only=$((r_only + 1)); fi
        if [[ "$st" == "FACTORY_STALE" ]]; then pull=$((pull + 1)); fi
    done
    
    echo -e "║ ${GREEN}✅ IN_SYNC:        ${sync}${NC}"
    echo -e "║ ${YELLOW}⬆️  PUSH needed:    ${push}${NC} (Factory newer or missing in Runtime)"
    echo -e "║ ${RED}⬇️  PULL needed:    ${pull}${NC} (Runtime newer, likely GEPA-mutated)"
    echo -e "║ ${BLUE}🆕 Runtime-only:   ${r_only}${NC} (Not tracked in Factory)"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    if [ "$pull" -gt 0 ]; then
        echo -e "${RED}Assets requiring PULL (GEPA Mutations):${NC}"
        for id in "${!ASSET_MAP_STATUS[@]}"; do
            if [[ "${ASSET_MAP_STATUS[$id]}" == "FACTORY_STALE" ]]; then
                local is_leg="${ASSET_MAP_LEGACY[$id]}"
                if [[ "$is_leg" == "true" ]]; then
                    echo -e "  - $id ${YELLOW}[LEGACY FLAT FILE - MIGRATION REQUIRED]${NC}"
                else
                    echo -e "  - $id"
                fi
            fi
        done
        echo ""
    fi
    
    if [ "$push" -gt 0 ]; then
        echo -e "${YELLOW}Assets requiring PUSH (Factory updates):${NC}"
        for id in "${!ASSET_MAP_STATUS[@]}"; do
            if [[ "${ASSET_MAP_STATUS[$id]}" == "RUNTIME_STALE" || "${ASSET_MAP_STATUS[$id]}" == "RUNTIME_MISSING" ]]; then
                echo -e "  - $id"
            fi
        done
        echo ""
    fi
}

copy_asset() {
    local src="$1"
    local dst="$2"
    local is_dir=false
    
    [ -d "$src" ] && is_dir=true
    
    mkdir -p "$(dirname "$dst")"
    
    if $DRY_RUN; then
        log_dry "Would copy: $src → $dst"
        return 0
    fi
    
    if $is_dir; then
        rsync -a --delete "$src/" "$dst/" 2>/dev/null
    else
        cp -f "$src" "$dst"
    fi
}

cmd_push() {
    local count=0
    for id in "${!ASSET_MAP_STATUS[@]}"; do
        local st="${ASSET_MAP_STATUS[$id]}"
        if [[ "$st" == "RUNTIME_STALE" || "$st" == "RUNTIME_MISSING" ]]; then
            local f_path="${ASSET_MAP_FACTORY[$id]}"
            local r_path="${ASSET_MAP_RUNTIME[$id]}"
            local is_leg="${ASSET_MAP_LEGACY[$id]}"
            
            # If pushing a legacy skill flat file to runtime, we must wrap it in a dir
            if [[ "$is_leg" == "true" ]]; then
                if [[ "$id" == SKL:* ]]; then
                    mkdir -p "$(dirname "$r_path")"
                elif [[ "$id" == KI:* ]]; then
                    mkdir -p "${r_path}/artifacts"
                    r_path="${r_path}/artifacts/$(basename "$f_path")"
                fi
            fi
            
            # If pushing a policy or workflow to runtime, we must wrap it in a KI
            if [[ "$id" == POL:* || "$id" == WF:* ]]; then
                mkdir -p "$(dirname "$r_path")"
                local ki_dir="$(dirname "$(dirname "$r_path")")"
                if [ ! -f "${ki_dir}/metadata.json" ]; then
                    local display_name="${id#*:}"
                    display_name="${display_name%.md}"
                    echo "{\"summary\": \"Auto-wrapped KI for ${id}\", \"references\": []}" > "${ki_dir}/metadata.json"
                fi
            fi
            
            copy_asset "$f_path" "$r_path"
            
            # For KI-based assets, we also sync to AROS_KI_DIR_AGENT
            if [[ "$id" == KI:* || "$id" == POL:* || "$id" == WF:* ]]; then
                local agent_r_path="${r_path/$AROS_KI_DIR/$AROS_KI_DIR_AGENT}"
                if [[ "$id" == POL:* || "$id" == WF:* ]]; then
                    local agent_ki_dir="$(dirname "$(dirname "$agent_r_path")")"
                    mkdir -p "$(dirname "$agent_r_path")"
                    if [ ! -f "${agent_ki_dir}/metadata.json" ]; then
                        local display_name="${id#*:}"
                        display_name="${display_name%.md}"
                        echo "{\"summary\": \"Auto-wrapped KI for ${id}\", \"references\": []}" > "${agent_ki_dir}/metadata.json"
                    fi
                fi
                copy_asset "$f_path" "$agent_r_path"
            fi
            
            log_ok "Pushed: $id"
            count=$((count + 1))
        fi
    done
    echo "Pushed $count assets."
}

cmd_pull() {
    local count=0
    for id in "${!ASSET_MAP_STATUS[@]}"; do
        local st="${ASSET_MAP_STATUS[$id]}"
        
        if [[ "$st" == "FACTORY_STALE" ]]; then
            local f_path="${ASSET_MAP_FACTORY[$id]}"
            local r_path="${ASSET_MAP_RUNTIME[$id]}"
            local is_leg="${ASSET_MAP_LEGACY[$id]}"
            
            if [[ "$is_leg" == "true" ]]; then
                log_warn "Skipping pull for $id: Legacy flat file in Factory. Please migrate to directory structure manually."
                continue
            fi
            
            copy_asset "$r_path" "$f_path"
            log_ok "Pulled GEPA Mutation: $id"
            count=$((count + 1))
            
        elif [[ "$st" == "FACTORY_MISSING" ]]; then
            if ! $IMPORT_ALL; then
                continue
            fi
            
            local r_path="${ASSET_MAP_RUNTIME[$id]}"
            # Determine staging path
            local type_part="${id%%:*}"
            local name_part="${id#*:}"
            local dest_dir=""
            
            case "$type_part" in
                SKL) dest_dir="${FACTORY_ROOT}/01.Shared_Assets/Skills/_imported/${name_part}" ;;
                KI)  dest_dir="${FACTORY_ROOT}/01.Shared_Assets/KIs/_imported/${name_part}" ;;
                POL) dest_dir="${FACTORY_ROOT}/01.Shared_Assets/Policies/_imported" ;;
                WF)  dest_dir="${FACTORY_ROOT}/01.Shared_Assets/Workflows/_imported" ;;
            esac
            
            if [[ "$type_part" == "SKL" || "$type_part" == "KI" ]]; then
                copy_asset "$r_path" "$dest_dir"
            else
                copy_asset "$r_path" "${dest_dir}/${name_part}"
            fi
            
            log_ok "Imported untracked: $id"
            count=$((count + 1))
        fi
    done
    echo "Pulled $count assets."
}

cmd_diff() {
    if [[ -z "${DIFF_TYPE:-}" || -z "${DIFF_NAME:-}" ]]; then
        log_error "Usage: sync_with_aros.sh diff <SKL|KI|POL|WF> <name>"
        exit 1
    fi
    local id="${DIFF_TYPE}:${DIFF_NAME}"
    if [[ -z "${ASSET_MAP_STATUS[$id]:-}" ]]; then
        log_error "Asset $id not found or in sync."
        exit 1
    fi
    local f_path="${ASSET_MAP_FACTORY[$id]}"
    local r_path="${ASSET_MAP_RUNTIME[$id]}"
    
    if [ -d "$f_path" ] && [ -d "$r_path" ]; then
        diff --color=auto -ur "$f_path" "$r_path" || true
    else
        diff --color=auto -u "$f_path" "$r_path" || true
    fi
}

# ── Main ─────────────────────────────────────────────────────────────────────

populate_asset_maps

case "$COMMAND" in
    status) cmd_status ;;
    push)   cmd_push ;;
    pull)   cmd_pull ;;
    diff)   cmd_diff ;;
    *)
        log_error "Unknown command: $COMMAND"
        exit 1
        ;;
esac
