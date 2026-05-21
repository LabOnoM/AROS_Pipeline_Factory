#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# BeesGo Spawn — Preflight Check
# Run this BEFORE starting the spawn process to verify the
# machine meets all requirements.
#
# Usage:  bash preflight_check.sh
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

PASS=0
FAIL=0
WARN=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

pass() { PASS=$((PASS+1)); echo -e "  ${GREEN}✓${NC} $1"; }
fail() { FAIL=$((FAIL+1)); echo -e "  ${RED}✗${NC} $1"; }
warn() { WARN=$((WARN+1)); echo -e "  ${YELLOW}⚠${NC} $1"; }
info() { echo -e "  ${CYAN}ℹ${NC} $1"; }

echo -e "${BOLD}━━━ BeesGo Spawn — Preflight Check ━━━${NC}"
echo ""

# ─── OS & Architecture ───────────────────────────
echo -e "${BOLD}[1/7] OS & Architecture${NC}"

if [ -f /etc/os-release ]; then
    . /etc/os-release
    pass "OS: $PRETTY_NAME"
else
    warn "Cannot detect OS (no /etc/os-release)"
fi

ARCH=$(uname -m)
case "$ARCH" in
    x86_64)  pass "Architecture: x86_64 (amd64)" ;;
    aarch64) pass "Architecture: ARM64" ;;
    riscv64) pass "Architecture: RISC-V 64" ;;
    *)       warn "Architecture: $ARCH (may not have pre-built Go binary)" ;;
esac

echo ""

# ─── Hardware Resources ──────────────────────────
echo -e "${BOLD}[2/7] Hardware Resources${NC}"

# RAM
TOTAL_RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
TOTAL_RAM_GB=$((TOTAL_RAM_KB / 1024 / 1024))
if [ "$TOTAL_RAM_GB" -ge 16 ]; then
    pass "RAM: ${TOTAL_RAM_GB} GB (recommended: 16+ GB)"
elif [ "$TOTAL_RAM_GB" -ge 8 ]; then
    warn "RAM: ${TOTAL_RAM_GB} GB (minimum met, but 16+ GB recommended for all services)"
else
    fail "RAM: ${TOTAL_RAM_GB} GB (minimum 8 GB required)"
fi

# CPU
CPU_CORES=$(nproc)
if [ "$CPU_CORES" -ge 8 ]; then
    pass "CPU: $CPU_CORES cores"
elif [ "$CPU_CORES" -ge 4 ]; then
    warn "CPU: $CPU_CORES cores (4 minimum, 8+ recommended)"
else
    fail "CPU: $CPU_CORES cores (minimum 4 required)"
fi

# Disk
DISK_FREE_KB=$(df / | tail -1 | awk '{print $4}')
DISK_FREE_GB=$((DISK_FREE_KB / 1024 / 1024))
if [ "$DISK_FREE_GB" -ge 50 ]; then
    pass "Disk: ${DISK_FREE_GB} GB free"
elif [ "$DISK_FREE_GB" -ge 30 ]; then
    warn "Disk: ${DISK_FREE_GB} GB free (30 GB minimum, 50+ recommended)"
else
    fail "Disk: ${DISK_FREE_GB} GB free (need at least 30 GB)"
fi

echo ""

# ─── Required Tools ──────────────────────────────
echo -e "${BOLD}[3/7] Required Tools${NC}"

# Git
if command -v git &>/dev/null; then
    pass "git: $(git --version | awk '{print $3}')"
else
    fail "git: not installed (sudo apt install git)"
fi

# Make
if command -v make &>/dev/null; then
    pass "make: available"
else
    fail "make: not installed (sudo apt install make)"
fi

# curl
if command -v curl &>/dev/null; then
    pass "curl: available"
else
    fail "curl: not installed (sudo apt install curl)"
fi

# wget
if command -v wget &>/dev/null; then
    pass "wget: available"
else
    warn "wget: not installed (needed for Go download; sudo apt install wget)"
fi

echo ""

# ─── Go ──────────────────────────────────────────
echo -e "${BOLD}[4/7] Go Compiler${NC}"

if command -v go &>/dev/null; then
    GO_VER=$(go version | awk '{print $3}' | sed 's/go//')
    GO_MAJOR=$(echo "$GO_VER" | cut -d. -f1)
    GO_MINOR=$(echo "$GO_VER" | cut -d. -f2)
    if [ "$GO_MAJOR" -ge 1 ] && [ "$GO_MINOR" -ge 21 ]; then
        pass "Go: $GO_VER (≥ 1.21 required)"
    else
        fail "Go: $GO_VER (need 1.21+, download from https://go.dev/dl/)"
    fi
else
    fail "Go: not installed (see Phase 1 in SKILL.md)"
    info "Download from https://go.dev/dl/"
    info "After installing, add to ~/.bashrc: export PATH=\$PATH:/usr/local/go/bin"
fi

echo ""

# ─── Docker ──────────────────────────────────────
echo -e "${BOLD}[5/7] Docker${NC}"

if command -v docker &>/dev/null; then
    DOCKER_VER=$(docker --version | grep -oP '[\d.]+' | head -1)
    pass "Docker Engine: $DOCKER_VER"

    # Check if user can run docker without sudo
    if docker ps &>/dev/null 2>&1; then
        pass "Docker permissions: OK (no sudo needed)"
    else
        warn "Docker permissions: need sudo — run 'sudo usermod -aG docker \$USER && newgrp docker'"
    fi
else
    warn "Docker: not installed (needed for Firecrawl, Skyvern, Hindsight)"
    info "See Phase 4 in SKILL.md for installation"
fi

if command -v docker &>/dev/null && docker compose version &>/dev/null 2>&1; then
    COMPOSE_VER=$(docker compose version | grep -oP '[\d.]+' | head -1)
    pass "Docker Compose: v$COMPOSE_VER"
else
    warn "Docker Compose: not available (install docker-compose-plugin)"
fi

echo ""

# ─── Python ──────────────────────────────────────
echo -e "${BOLD}[6/7] Python${NC}"

if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version | awk '{print $2}')
    PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
    PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 11 ]; then
        pass "Python: $PY_VER (≥ 3.11 recommended)"
    elif [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 8 ]; then
        warn "Python: $PY_VER (works, but 3.11+ recommended)"
    else
        fail "Python: $PY_VER (need 3.8+, recommend 3.11+)"
    fi
else
    fail "Python3: not installed (sudo apt install python3 python3-pip python3-venv)"
fi

if command -v pip3 &>/dev/null; then
    pass "pip3: available"
else
    warn "pip3: not installed (sudo apt install python3-pip)"
fi

echo ""

# ─── Ports ───────────────────────────────────────
echo -e "${BOLD}[7/7] Port Availability${NC}"

PORTS=(3002 8000 8080 8888 9999 18790)
LABELS=("Firecrawl API" "Skyvern API" "Skyvern UI" "Hindsight API" "Hindsight Panel" "BeesGo Gateway")

for i in "${!PORTS[@]}"; do
    PORT=${PORTS[$i]}
    LABEL=${LABELS[$i]}
    if ss -tlnp 2>/dev/null | grep -q ":${PORT} " ; then
        PROC=$(ss -tlnp 2>/dev/null | grep ":${PORT} " | grep -oP 'users:\(\("\K[^"]+' || echo "unknown")
        warn "Port $PORT ($LABEL): IN USE by $PROC"
    else
        pass "Port $PORT ($LABEL): available"
    fi
done

echo ""

# ─── Summary ─────────────────────────────────────
TOTAL=$((PASS + FAIL + WARN))
echo -e "${BOLD}━━━ Preflight Summary ━━━${NC}"
echo -e "  ${GREEN}Passed${NC}:   $PASS"
echo -e "  ${RED}Failed${NC}:   $FAIL"
echo -e "  ${YELLOW}Warnings${NC}: $WARN"
echo -e "  Total:    $TOTAL"
echo ""

if [ "$FAIL" -gt 0 ]; then
    echo -e "${RED}${BOLD}PREFLIGHT FAILED: Fix $FAIL issue(s) before spawning BeesGo.${NC}"
    exit 1
elif [ "$WARN" -gt 0 ]; then
    echo -e "${YELLOW}${BOLD}PREFLIGHT PASSED with $WARN warning(s). Safe to proceed.${NC}"
    exit 0
else
    echo -e "${GREEN}${BOLD}PREFLIGHT PASSED: Machine is ready for BeesGo spawn!${NC}"
    exit 0
fi
