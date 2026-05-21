#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# BeesGo Spawn — Automated Deployment Script
#
# Deploys a full BeesGo-Agent instance on a fresh Linux machine.
# Interactive prompts for API keys and optional services.
#
# Usage:  bash spawn.sh [--skip-docker] [--skip-services] [--no-build]
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SKIP_DOCKER=false
SKIP_SERVICES=false
NO_BUILD=false
BEESGO_REPO="https://github.com/LabOnoM/BeesGo-Agent.git"
INSTALL_DIR="${BEESGO_DIR:-$HOME/Documents/GitHub/BeesGo-Agent}"

for arg in "$@"; do
    case "$arg" in
        --skip-docker)   SKIP_DOCKER=true ;;
        --skip-services) SKIP_SERVICES=true ;;
        --no-build)      NO_BUILD=true ;;
        --help|-h)
            echo "Usage: bash spawn.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --skip-docker     Skip Docker Engine installation"
            echo "  --skip-services   Skip dependency services (Firecrawl, Skyvern, Hindsight)"
            echo "  --no-build        Skip building from source (use existing binary)"
            echo "  --help            Show this help"
            exit 0
            ;;
    esac
done

log()  { echo -e "${BOLD}[SPAWN]${NC} $1"; }
ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
warn() { echo -e "  ${YELLOW}⚠${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; exit 1; }
ask()  { echo -en "  ${CYAN}?${NC} $1: "; read -r REPLY; }

echo -e "${BOLD}"
echo "  ╔══════════════════════════════════════════╗"
echo "  ║       🐝 BeesGo Spawn — Let's Go!       ║"
echo "  ╚══════════════════════════════════════════╝"
echo -e "${NC}"

# ─── Phase 1: System Packages ────────────────────
log "Phase 1: System Packages"

if command -v apt-get &>/dev/null; then
    sudo apt-get update -qq
    sudo apt-get install -y -qq \
        git make curl wget ca-certificates gnupg \
        xdotool xclip scrot ffmpeg tesseract-ocr \
        python3 python3-pip python3-venv 2>/dev/null
    ok "System packages installed"
else
    warn "Not a Debian/Ubuntu system — install packages manually"
fi

# ─── Phase 2: Install Go ─────────────────────────
log "Phase 2: Go Compiler"

if command -v go &>/dev/null; then
    GO_VER=$(go version | awk '{print $3}')
    ok "Go already installed: $GO_VER"
else
    log "Installing Go 1.24.1..."
    ARCH=$(uname -m)
    case "$ARCH" in
        x86_64)  GO_ARCH="amd64" ;;
        aarch64) GO_ARCH="arm64" ;;
        riscv64) GO_ARCH="riscv64" ;;
        *)       fail "Unsupported architecture: $ARCH" ;;
    esac

    GO_TAR="go1.24.1.linux-${GO_ARCH}.tar.gz"
    if [ ! -f "/tmp/$GO_TAR" ]; then
        wget -q "https://go.dev/dl/$GO_TAR" -O "/tmp/$GO_TAR"
    fi
    sudo rm -rf /usr/local/go
    sudo tar -C /usr/local -xzf "/tmp/$GO_TAR"

    # Persist PATH
    if ! grep -q '/usr/local/go/bin' ~/.bashrc 2>/dev/null; then
        echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    fi
    export PATH=$PATH:/usr/local/go/bin
    ok "Go installed: $(go version | awk '{print $3}')"
fi

# ─── Phase 3: Clone & Build ──────────────────────
log "Phase 3: Clone & Build"

if [ ! -d "$INSTALL_DIR/.git" ]; then
    log "Cloning BeesGo-Agent..."
    mkdir -p "$(dirname "$INSTALL_DIR")"
    git clone "$BEESGO_REPO" "$INSTALL_DIR"
    ok "Cloned to $INSTALL_DIR"
else
    ok "Repository exists at $INSTALL_DIR"
fi

if [ "$NO_BUILD" = false ]; then
    log "Building BeesGo-Agent..."
    cd "$INSTALL_DIR"
    make deps 2>/dev/null || true
    make build
    ok "Build complete: build/beesgo"

    log "Running make install..."
    make install 2>&1 | tail -5
    ok "Installed to ~/.local/bin/"

    # Persist PATH
    if ! grep -q '\.local/bin' ~/.bashrc 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    fi
    export PATH="$HOME/.local/bin:$PATH"
else
    ok "Skipping build (--no-build)"
fi

# ─── Phase 4: Initialize ─────────────────────────
log "Phase 4: Initialize BeesGo"

if [ ! -f "$HOME/.beesgo/config.json" ]; then
    if command -v beesgo &>/dev/null; then
        beesgo onboard 2>/dev/null || true
        ok "Workspace initialized at ~/.beesgo/"
    else
        warn "beesgo not in PATH — run 'beesgo onboard' manually"
    fi
else
    ok "Workspace already exists at ~/.beesgo/"
fi

# ─── Phase 5: Docker Engine ──────────────────────
if [ "$SKIP_DOCKER" = false ]; then
    log "Phase 5: Docker Engine"

    if command -v docker &>/dev/null; then
        ok "Docker already installed: $(docker --version | grep -oP '[\d.]+' | head -1)"
    else
        log "Installing Docker Engine..."
        sudo install -m 0755 -d /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
            | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg 2>/dev/null
        sudo chmod a+r /etc/apt/keyrings/docker.gpg

        echo "deb [arch=$(dpkg --print-architecture) \
            signed-by=/etc/apt/keyrings/docker.gpg] \
            https://download.docker.com/linux/ubuntu \
            $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
            | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

        sudo apt-get update -qq
        sudo apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-compose-plugin
        sudo usermod -aG docker "$USER"
        ok "Docker installed — NOTE: run 'newgrp docker' or re-login for group changes"
    fi

    if docker compose version &>/dev/null 2>&1; then
        ok "Docker Compose: $(docker compose version | grep -oP '[\d.]+' | head -1)"
    else
        warn "Docker Compose not available"
    fi
else
    log "Phase 5: Docker (skipped)"
fi

# ─── Phase 6: Dependency Services ────────────────
if [ "$SKIP_SERVICES" = false ]; then
    log "Phase 6: Dependency Services"

    cd "$INSTALL_DIR"

    # Firecrawl
    if [ -f deps/firecrawl/docker-compose.yml ]; then
        log "Starting Firecrawl..."
        docker compose -f deps/firecrawl/docker-compose.yml up -d 2>/dev/null && \
            ok "Firecrawl started (port 3002)" || \
            warn "Firecrawl failed to start"
    else
        warn "deps/firecrawl/docker-compose.yml not found"
    fi

    # Skyvern
    if [ -f deps/skyvern/docker-compose.yml ]; then
        log "Starting Skyvern..."
        docker compose -f deps/skyvern/docker-compose.yml up -d 2>/dev/null && \
            ok "Skyvern started (ports 8000, 8080)" || \
            warn "Skyvern failed to start"
    else
        warn "deps/skyvern/docker-compose.yml not found"
    fi

    # Hindsight DB
    if [ -f deps/hindsight/docker-compose.yml ]; then
        log "Starting Hindsight PostgreSQL..."
        docker compose -f deps/hindsight/docker-compose.yml up -d 2>/dev/null && \
            ok "Hindsight DB started (port 5433)" || \
            warn "Hindsight DB failed to start"
    else
        warn "deps/hindsight/docker-compose.yml not found"
    fi

    # Hindsight API (Python)
    if [ -d deps/hindsight/hindsight-api ]; then
        if ! command -v uv &>/dev/null; then
            log "Installing uv (Python package manager)..."
            curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null
            export PATH="$HOME/.local/bin:$PATH"
            ok "uv installed"
        else
            ok "uv already installed"
        fi

        log "Syncing Hindsight dependencies..."
        cd deps/hindsight/hindsight-api
        uv sync 2>/dev/null && ok "Hindsight deps installed" || warn "Hindsight deps failed"
        cd "$INSTALL_DIR"
    else
        warn "deps/hindsight/hindsight-api not found — may need: cd deps/hindsight && git clone https://github.com/vectorize-io/hindsight.git ."
    fi
else
    log "Phase 6: Services (skipped)"
fi

# ─── Phase 7: Config Guidance ────────────────────
log "Phase 7: Configuration"

echo ""
echo -e "  ${BOLD}Next steps:${NC}"
echo ""
echo "  1. Edit ~/.beesgo/config.json:"
echo "     - Set your API key in providers.gemini.api_key"
echo "     - Set absolute paths for compose_dir / service_dir"
echo ""
echo "  2. Set Hindsight env vars in ~/.beesgo/.env:"
echo "     HINDSIGHT_API_LLM_PROVIDER=gemini"
echo "     HINDSIGHT_API_LLM_API_KEY=your-key"
echo "     HINDSIGHT_API_DATABASE_URL=postgresql://hindsight:hindsight@localhost:5433/hindsight"
echo ""
echo "  3. Test the agent:"
echo "     beesgo agent -m 'Hello'"
echo ""
echo "  4. Start the gateway (after configuring a channel):"
echo "     beesgo gateway"
echo ""

# ─── Phase 8: Verification ───────────────────────
log "Phase 8: Quick Verification"

# Check binary
if command -v beesgo &>/dev/null; then
    ok "beesgo binary: $(beesgo version 2>/dev/null || echo 'found')"
else
    warn "beesgo not in PATH"
fi

# Check Docker containers
if command -v docker &>/dev/null && docker ps &>/dev/null 2>&1; then
    RUNNING=$(docker ps --format '{{.Names}}' 2>/dev/null | wc -l)
    ok "Docker containers running: $RUNNING"
fi

# Check ports
for port in 3002 8000 8080 8888 5433; do
    if ss -tlnp 2>/dev/null | grep -q ":${port} "; then
        ok "Port $port: in use"
    fi
done

echo ""
echo -e "${GREEN}${BOLD}  🐝 BeesGo Spawn Complete! 🐝${NC}"
echo ""
