---
name: beesgo-spawn
description: How to deploy ("spawn") a BeesGo-Agent instance onto a fresh Linux machine from scratch. Covers Go installation, building from source, Docker setup, all dependency services (Firecrawl, Skyvern, Hindsight, RAG-Anything), full configuration with model tiers and rate limits, systemd auto-start, and verification. Use this skill whenever the user wants to install BeesGo on a new machine, set up BeesGo dependencies, troubleshoot a BeesGo deployment, reproduce the full BeesGo environment on Linux, or configure model tiers and rate limits. Also trigger for questions about BeesGo build errors, Docker service setup, missing dependencies, or Hindsight pgvector issues.
---

# BeesGo Spawn — Linux Deployment Skill

Deploy a fully-functional BeesGo-Agent instance on a fresh Linux machine. This skill is distilled from real deployment sessions and captures every gotcha encountered along the way.

> [!TIP]
> Run `scripts/preflight_check.sh` (bundled with this skill) first to verify the machine meets all requirements.
> Or run the full automated spawn: `bash scripts/spawn.sh` (interactive, handles everything).

---

## Prerequisites

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| **OS** | Ubuntu 22.04+ / Debian 12+ | Ubuntu 24.04 LTS |
| **RAM** | 8 GB | 32+ GB (for all services) |
| **CPU** | 4 cores | 8+ cores |
| **Disk** | 30 GB free | 100+ GB (Docker images grow) |
| **Arch** | x86_64, ARM64, RISC-V | x86_64 |

### System Packages (installed automatically by `make install-deps`)

**Debian/Ubuntu:**
```bash
sudo apt update && sudo apt install -y \
  git make curl wget ca-certificates gnupg \
  xdotool xclip scrot ffmpeg tesseract-ocr \
  python3 python3-pip python3-venv
```

---

## Phase 1 — Install Go

Go 1.21+ is required to build BeesGo.

```bash
# Download (check https://go.dev/dl/ for latest)
wget https://go.dev/dl/go1.24.1.linux-amd64.tar.gz

# Install
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.24.1.linux-amd64.tar.gz

# Add to PATH — IMPORTANT: persist this!
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Verify
go version
```

> [!CAUTION]
> **Lesson learned:** Simply running `export PATH=...` in the terminal does NOT persist across new shells or `make` subprocesses. You MUST add it to `~/.bashrc` (or `~/.profile`) and `source` it. If `make build` fails with "go: command not found", this is the cause.

For ARM64 boards, replace `amd64` with `arm64` in the download URL.
For RISC-V boards, use `riscv64`.

---

## Phase 2 — Clone & Build

```bash
# Clone
git clone https://github.com/LabOnoM/BeesGo-Agent.git
cd BeesGo-Agent

# Download Go dependencies
make deps

# Build for current platform (output in build/)
make build

# Full install: deps + build + Python venvs → ~/.local/bin/
make install
```

After `make install`, ensure `~/.local/bin` is in your PATH:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### What `make install` does

1. **`install-deps`** — installs system packages (xdotool, xclip, scrot, ffmpeg, tesseract, python3) + pip packages from `requirements.txt` (Pillow, requests, pyautogui, pyaudio, google-genai, opencv-python, numpy)
2. **`build`** — runs `go generate ./...` then compiles the `beesgo` binary for your platform
3. **`setup-venv`** — creates `pkg/tools/venv/` with AV/GUI Python packages
4. **`rag-setup`** — creates `deps/raganything/venv/` with RAG-Anything + LightRAG
5. **Installs Python adapter scripts** — `gui_agent_adapter.py`, `capture_photo.py`, `record_audio.py`, `live_chat.py`, `rag_anything_adapter.py` → `~/.local/bin/`

### Cross-compilation

```bash
# Build for all platforms at once
make build-all
# Produces: build/beesgo-linux-{amd64,arm64,riscv64}, darwin-arm64, windows-amd64.exe
```

---

## Phase 3 — Initialize & Configure

```bash
# Create workspace structure at ~/.beesgo/
beesgo onboard
```

This creates:
```
~/.beesgo/
├── config.json          # Main configuration
├── workspace/
│   ├── sessions/        # Conversation history
│   ├── memory/          # Long-term memory (MEMORY.md)
│   ├── state/           # Persistent state
│   ├── cron/            # Scheduled jobs
│   ├── skills/          # Custom skills (149 scientific + operational)
│   ├── banks/           # Knowledge bank descriptors
│   ├── AGENTS.md        # Agent behavior guide
│   ├── HEARTBEAT.md     # Periodic task prompts (checked every 30 min)
│   ├── IDENTITY.md      # Agent identity
│   ├── SOUL.md          # Agent soul
│   ├── TOOLS.md         # Tool descriptions
│   └── USER.md          # User preferences
└── logs/
    └── system.log
```

### Configure `~/.beesgo/config.json`

Start from the example template:
```bash
cp config/config.example.json ~/.beesgo/config.json
```

#### Minimal Config (just get it running)

```json
{
  "agents": {
    "defaults": {
      "provider": "gemini",
      "model": "models/gemini-2.5-flash",
      "max_tokens": 125000,
      "temperature": 0.7,
      "max_tool_iterations": 100
    }
  },
  "providers": {
    "gemini": {
      "api_key": "YOUR_GEMINI_API_KEY"
    }
  }
}
```

#### Model Tiers (Director/Worker/Runner)

BeesGo uses a multi-tier model architecture for complex tasks (`deep_task`):

| Tier | Role | Recommended Model |
|------|------|-------------------|
| **Director** | Orchestrates D/W/R pipeline, strategic decisions | Top-tier (Gemini Pro, Claude Opus) |
| **Worker** | Executes subtasks, code generation | Mid-tier (Gemini Flash, Qwen 35B) |
| **Runner** | Quick evaluations, routing | Lightweight (Gemini Flash Lite, Ministral) |
| **Router** | Auto-routes tasks to appropriate tier | Tiny model (Qwen 2B) |

```json
{
  "agents": {
    "defaults": {
      "model_tiers": {
        "director": {
          "provider": "gemini",
          "model": "models/gemini-3-flash-preview",
          "api_key": "",
          "api_base": "https://generativelanguage.googleapis.com/v1beta/openai"
        },
        "worker": {
          "provider": "openai",
          "model": "Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf",
          "api_key": "",
          "api_base": "https://your-local-inference-server/v1"
        },
        "runner": {
          "provider": "openai",
          "model": "Ministral-3-14B-Instruct-2512-Q4_K_M.gguf",
          "api_key": "",
          "api_base": "https://your-local-inference-server/v1"
        },
        "router": {
          "enabled": true,
          "provider": "openai",
          "model": "Qwen3-VL-2B-Instruct-UD-Q4_K_XL.gguf",
          "api_key": "",
          "api_base": "https://your-local-inference-server/v1",
          "timeout_ms": 10000,
          "max_turns": 2
        }
      }
    }
  }
}
```

> [!TIP]
> Model tier API keys and endpoints can be overridden via environment variables:
> `PICOCLAW_TIER_DIRECTOR_PROVIDER`, `PICOCLAW_TIER_DIRECTOR_MODEL`, `PICOCLAW_TIER_DIRECTOR_API_KEY`, etc.

#### Rate Limits

Production deployments should configure rate limits to prevent API abuse:

```json
{
  "rate_limits": {
    "main": {
      "max_parallel": 1,
      "cooldown_sec": 72,
      "tpm_limit": 400000,
      "rpm_limit": 15,
      "priority": 10
    },
    "heartbeat": {
      "max_parallel": 1,
      "cooldown_sec": 72,
      "tpm_limit": 100000,
      "rpm_limit": 15,
      "priority": 1
    },
    "director": {
      "max_parallel": 1,
      "cooldown_sec": 72,
      "tpm_limit": 400000,
      "rpm_limit": 15,
      "priority": 5
    },
    "worker": {
      "max_parallel": 2,
      "cooldown_sec": 0,
      "tpm_limit": 0,
      "rpm_limit": 15,
      "priority": 5
    },
    "runner": {
      "max_parallel": 2,
      "cooldown_sec": 0,
      "tpm_limit": 0,
      "rpm_limit": 15,
      "priority": 3
    }
  }
}
```

#### API Key Sources

| Provider | Get Key | Notes |
|----------|---------|-------|
| **Gemini** | [aistudio.google.com](https://aistudio.google.com/api-keys) | Free tier available |
| **OpenRouter** | [openrouter.ai/keys](https://openrouter.ai/keys) | Access to all models |
| **Zhipu** | [bigmodel.cn](https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys) | GLM models |
| **Anthropic** | [console.anthropic.com](https://console.anthropic.com) | Claude models |
| **OpenAI** | [platform.openai.com](https://platform.openai.com) | GPT models |
| **Groq** | [console.groq.com](https://console.groq.com) | LLM + Whisper voice |
| **Brave Search** | [brave.com/search/api](https://brave.com/search/api) | 2000 free queries/month |

### Environment Variables (`.env`)

Copy and edit the environment template:
```bash
cp .env.example .env
```

Key variables:
```bash
TZ=Asia/Tokyo                              # Your timezone
# OPENROUTER_API_KEY=sk-or-v1-xxx          # LLM provider
# GEMINI_API_KEY=xxx                       # LLM provider
# TELEGRAM_BOT_TOKEN=123456:ABC...         # Chat channel
# BRAVE_SEARCH_API_KEY=BSA...              # Web search (optional)
```

### Quick Smoke Test

```bash
beesgo agent -m "What is 2+2?"
```

If this works, the core agent is alive. Move on to dependency services.

---

## Phase 4 — Install Docker Engine

Docker is required for Firecrawl, Skyvern, and Hindsight services.

```bash
# Add Docker's GPG key and repo
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine + Compose plugin
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Allow current user to run docker without sudo
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version          # e.g., 29.2.1
docker compose version    # e.g., v5.0.2
```

> [!WARNING]
> **Lesson learned:** After `usermod -aG docker $USER`, you need `newgrp docker` or a fresh login for the group change to take effect. Without this, `docker compose up` will fail with "permission denied".

---

## Phase 5 — Dependency Services

### 5a. Firecrawl (Web Scraping — 5 containers)

```bash
cd deps/firecrawl
docker compose up -d
```

| Container | Image | Port | Resources |
|-----------|-------|------|-----------|
| api | `ghcr.io/firecrawl/firecrawl:latest` | **3002** | 4 CPU, 8GB RAM |
| playwright-service | `ghcr.io/firecrawl/playwright-service:latest` | 3000 (internal) | 2 CPU, 4GB RAM |
| redis | `redis:alpine` | 6379 (internal) | — |
| rabbitmq | `rabbitmq:3-management` | 5672 (internal) | — |
| nuq-postgres | `postgres:16-alpine` | 5432 (internal) | — |

**Key env vars** (set in docker-compose.yml):
- `USE_DB_AUTHENTICATION=false` (no API key needed for self-hosted)
- `NUM_WORKERS_PER_QUEUE=8`
- `FIRECRAWL_PORT` can override the host port (default: 3002)

Health check: `curl -s http://localhost:3002 | head -c 200`

### 5b. Skyvern (Browser Automation — 3 containers)

```bash
cd deps/skyvern
docker compose up -d
```

| Container | Image | Port | Resources |
|-----------|-------|------|-----------|
| skyvern | `public.ecr.aws/skyvern/skyvern:latest` | **8000** | 2 CPU, 4GB RAM |
| postgres | `postgres:16-alpine` | 5432 (internal) | — |
| skyvern-ui | `public.ecr.aws/skyvern/skyvern-ui:latest` | **8080** | — |

**Key env vars** (set in docker-compose.yml):
- `SKYVERN_API_KEY` — optional, empty by default for self-hosted
- `SKYVERN_PORT` can override the host port (default: 8000)
- `OPENAI_API_KEY=sk-dummy-key-to-bypass-startup-check` — Skyvern requires this env var to start but BeesGo routes LLM calls through its own providers

Health check: `curl -s http://localhost:8000 | head -c 200`

### 5c. Hindsight (Long-term Memory)

Hindsight is a Python API service backed by PostgreSQL+pgvector. It has two components:
1. **hindsight-api** — the memory bank API (port 8888)
2. **hindsight-control-plane** — web UI dashboard (port 9999)

> [!IMPORTANT]
> On Ubuntu 22.04 (glibc 2.35), the embedded `pg0` database's pgvector extension (`vector.so`) requires glibc 2.38 and will fail to load. You MUST use Docker PostgreSQL instead.

**Step 1: Install `uv` (Python package manager)**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc   # adds uv to PATH
uv --version
```

**Step 2: Start Docker PostgreSQL+pgvector**

```bash
cd deps/hindsight
docker compose up -d
# Starts pgvector/pgvector:pg17 on port 5433
# Data persisted to ~/.beesgo/hindsight-pgdata/
```

**Step 3: Clone Hindsight source (if `deps/hindsight/hindsight-api/` is empty)**

```bash
cd deps/hindsight
git clone --depth 1 https://github.com/vectorize-io/hindsight.git .
cd hindsight-api
uv sync  # install Python dependencies
```

**Step 4: Configure Hindsight environment**

Create `~/.beesgo/.env` (or set env vars before starting):

```bash
# Required
HINDSIGHT_API_LLM_PROVIDER=gemini
HINDSIGHT_API_LLM_API_KEY=YOUR_GEMINI_API_KEY
HINDSIGHT_API_LLM_MODEL=models/gemini-2.5-flash-lite
HINDSIGHT_API_DATABASE_URL=postgresql://hindsight:hindsight@localhost:5433/hindsight

# Recommended (CPU-only embeddings, no GPU needed)
HINDSIGHT_API_EMBEDDINGS_PROVIDER=local
HINDSIGHT_API_EMBEDDINGS_LOCAL_FORCE_CPU=true
HINDSIGHT_API_RERANKER_PROVIDER=rrf

# API server
HINDSIGHT_API_HOST=0.0.0.0
HINDSIGHT_API_PORT=8888
HINDSIGHT_API_LOG_LEVEL=info
```

**Supported LLM providers for Hindsight:** openai, groq, ollama, gemini, anthropic, lmstudio, vertexai

| Port | Purpose |
|------|---------|
| **8888** | Hindsight API |
| **9999** | Control Panel UI |
| 5433 | PostgreSQL+pgvector (Docker) |

BeesGo's watchdog auto-starts Hindsight when `service_dir` is set in `config.json` and `auto_restart: true`.

> [!CAUTION]
> **Lesson learned:** Hindsight WILL NOT start without `HINDSIGHT_API_LLM_API_KEY`. If you see the service crash-looping, check:
> 1. Is `HINDSIGHT_API_LLM_API_KEY` set and valid?
> 2. Is Docker PostgreSQL running on port 5433? (`docker ps | grep beesgo-hindsight-db`)
> 3. Is the `HINDSIGHT_API_DATABASE_URL` pointing to port **5433** (Docker) not 5432?

### 5d. RAG-Anything (Document Processing)

Handled automatically by `make rag-setup`, which:
1. Creates a venv at `deps/raganything/venv/`
2. Clones RAG-Anything source from HKUDS/RAG-Anything if missing
3. Installs lightrag-hku, openai, tiktoken, numpy, etc.

MinerU (PDF parser) is optional:
```bash
deps/raganything/venv/bin/pip install 'mineru[core]'
```

RAG config in `config.json`:
```json
{
  "tools": {
    "rag_anything": {
      "enabled": true,
      "storage_dir": "~/.beesgo/rag_storage",
      "llm_provider": "gemini",
      "llm_model": "models/gemini-2.5-flash-lite",
      "embed_model": "text-embedding-004",
      "parser": "mineru",
      "timeout": 6000
    }
  }
}
```

---

## Phase 6 — Full Config for All Services

After all services are running, here is a complete production `~/.beesgo/config.json`:

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.beesgo/workspace",
      "media_dir": "~/.beesgo/workspace/media",
      "restrict_to_workspace": false,
      "provider": "gemini",
      "model": "models/gemini-2.5-flash",
      "max_tokens": 125000,
      "temperature": 0.7,
      "max_tool_iterations": 100,
      "model_tiers": {
        "director": {
          "provider": "gemini",
          "model": "models/gemini-3-flash-preview",
          "api_key": ""
        },
        "worker": {
          "provider": "gemini",
          "model": "models/gemini-2.5-flash",
          "api_key": ""
        },
        "runner": {
          "provider": "gemini",
          "model": "models/gemini-2.5-flash-lite",
          "api_key": ""
        }
      }
    }
  },
  "providers": {
    "gemini": {
      "api_key": "YOUR_GEMINI_API_KEY",
      "api_base": ""
    }
  },
  "channels": {
    "telegram": {
      "enabled": false,
      "token": "YOUR_BOT_TOKEN",
      "allow_from": ["YOUR_USER_ID"]
    }
  },
  "gateway": {
    "host": "0.0.0.0",
    "port": 18790
  },
  "tools": {
    "web": {
      "duckduckgo": { "enabled": true, "max_results": 5 }
    },
    "firecrawl": {
      "enabled": true,
      "base_url": "http://localhost:3002",
      "compose_dir": "/ABSOLUTE/PATH/TO/BeesGo-Agent/deps/firecrawl",
      "auto_restart": true
    },
    "rag_anything": {
      "enabled": true,
      "storage_dir": "~/.beesgo/rag_storage",
      "llm_provider": "gemini",
      "llm_model": "models/gemini-2.5-flash-lite",
      "embed_model": "text-embedding-004",
      "parser": "mineru",
      "timeout": 6000
    },
    "image_gen": {
      "enabled": true,
      "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
      "api_key": "",
      "model": "models/gemini-3-pro-image-preview",
      "timeout": 6000
    }
  },
  "heartbeat": {
    "enabled": true,
    "interval": 30
  },
  "hindsight": {
    "enabled": true,
    "base_url": "http://localhost:8888",
    "api_key": "",
    "model": "models/gemini-2.5-flash-lite",
    "timeout": 6000,
    "service_dir": "/ABSOLUTE/PATH/TO/BeesGo-Agent/deps/hindsight/hindsight-api",
    "auto_restart": true,
    "control_panel": {
      "enabled": true,
      "port": 9999,
      "service_dir": "/ABSOLUTE/PATH/TO/BeesGo-Agent/deps/hindsight/hindsight-control-plane"
    },
    "banks": {
      "identity": "BeesGo-00",
      "user": "user-preferences",
      "skills": "skills-library",
      "shared_knowledge": "shared-knowledge",
      "agent_comms": "agent-comms"
    },
    "auto_recall_roles": ["user", "skills", "shared_knowledge"],
    "skills_ingestion": {
      "source_dir": "/ABSOLUTE/PATH/TO/workspace/skills",
      "refresh_on_startup": true
    }
  },
  "self_dev": {
    "enabled": true,
    "source_dir": "/ABSOLUTE/PATH/TO/BeesGo-Agent",
    "timeout": 600,
    "max_timeout": 1800,
    "max_iterations": 20
  },
  "logging": {
    "file": "~/.beesgo/logs/system.log",
    "level": "info",
    "rotation": { "max_size_mb": 10, "max_backups": 5 }
  },
  "rate_limits": {
    "main":      { "max_parallel": 1, "cooldown_sec": 72, "tpm_limit": 400000, "rpm_limit": 15, "priority": 10 },
    "heartbeat": { "max_parallel": 1, "cooldown_sec": 72, "tpm_limit": 100000, "rpm_limit": 15, "priority": 1 },
    "director":  { "max_parallel": 1, "cooldown_sec": 72, "tpm_limit": 400000, "rpm_limit": 15, "priority": 5 },
    "worker":    { "max_parallel": 2, "cooldown_sec": 0,  "tpm_limit": 0,      "rpm_limit": 15, "priority": 5 },
    "runner":    { "max_parallel": 2, "cooldown_sec": 0,  "tpm_limit": 0,      "rpm_limit": 15, "priority": 3 }
  }
}
```

> [!IMPORTANT]
> Replace all `/ABSOLUTE/PATH/TO/` with your actual paths. Use absolute paths, not `~` (tilde is only expanded for certain fields).

---

## Phase 7 — Verification

### Quick Health Checks

```bash
# Core agent
beesgo agent -m "Hello"

# Firecrawl
curl -s http://localhost:3002 | head -c 200

# Skyvern
curl -s http://localhost:8000 | head -c 200

# Hindsight
curl -s http://localhost:8888 | head -c 200

# All Docker containers
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Full Regression Test

```bash
bash scripts/test_regression.sh
# or quick mode:
bash scripts/test_regression.sh --quick
```

### Doctor Check

```bash
beesgo doctor
```

### Expected Healthy State

| Service | Port | Status |
|---------|------|--------|
| BeesGo Agent | — | `beesgo agent` responds |
| BeesGo Gateway | 18790 | `beesgo gateway` starts |
| Firecrawl | 3002 | HTTP 200 |
| Skyvern API | 8000 | Responding |
| Skyvern UI | 8080 | Accessible |
| Hindsight API | 8888 | Responding |
| Hindsight Panel | 9999 | Accessible |
| Hindsight DB | 5433 | PostgreSQL healthy |

---

## Phase 8 — Production Deployment

### Systemd Service (auto-start on boot)

Create `/etc/systemd/system/beesgo-gateway.service`:

```ini
[Unit]
Description=BeesGo-Agent Gateway
After=network.target docker.service
Wants=docker.service

[Service]
Type=simple
User=YOUR_USER
Environment=HOME=/home/YOUR_USER
WorkingDirectory=/home/YOUR_USER/Documents/GitHub/BeesGo-Agent
ExecStart=/home/YOUR_USER/.local/bin/beesgo gateway
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable beesgo-gateway
sudo systemctl start beesgo-gateway
sudo systemctl status beesgo-gateway
```

### Log Monitoring

```bash
# System log
tail -f ~/.beesgo/logs/system.log

# Systemd journal
journalctl -u beesgo-gateway -f

# Docker service logs
docker compose -f deps/firecrawl/docker-compose.yml logs -f
docker compose -f deps/skyvern/docker-compose.yml logs -f
docker logs -f hindsight 2>/dev/null || docker compose -f deps/hindsight/docker-compose.yml logs -f
```

---

## Chat Channel Setup (Optional)

Start the gateway bot after configuring a channel in `config.json`:

```bash
beesgo gateway
```

**Telegram** (easiest):
1. Talk to `@BotFather` → `/newbot` → copy token
2. Get your user ID from `@userinfobot`
3. Set in config: `channels.telegram.enabled = true`, `token`, `allow_from`

**Discord:**
1. Create app at discord.com/developers → Bot → copy token
2. Enable MESSAGE CONTENT INTENT
3. OAuth2 → URL Generator → Scopes: `bot` → Permissions: `Send Messages`, `Read Message History`
4. Open invite URL, add to server
5. Set in config: `channels.discord.enabled = true`, `token`

**Other channels:** QQ, DingTalk, LINE, Slack, Feishu, OneBot — see `config.example.json` for full schema.

---

## Docker Compose Deploy (Alternative)

Instead of building from source, deploy the whole agent via Docker:

```bash
cp config/config.example.json config/config.json
# Edit config/config.json with your API keys

docker compose --profile gateway up -d
docker compose logs -f beesgo-gateway
```

---

## Tips & Gotchas (from real deployments)

1. **Go not found in make**: Always persist Go's PATH in `~/.bashrc`, not just the current shell
2. **Docker permission denied**: Run `newgrp docker` after `usermod -aG docker $USER`, or log out and back in
3. **Hindsight crash-loop**: Set `HINDSIGHT_API_LLM_API_KEY` env var before starting; also ensure Docker PostgreSQL is running on port 5433
4. **pgvector glibc issue**: On Ubuntu 22.04 (glibc 2.35), pg0's bundled `vector.so` requires glibc 2.38. Use Docker PostgreSQL+pgvector via `deps/hindsight/docker-compose.yml` instead
5. **Port conflicts**: Check existing services: `ss -tlnp | grep -E '3002|8000|8080|8888|9999|18790|5433'`
6. **deps/ directories empty**: Some deps are git submodules — run `git submodule update --init --recursive`, or clone manually
7. **Python venv failures**: `pyaudio` needs `portaudio19-dev` (`sudo apt install portaudio19-dev`), opencv may need build tools (`sudo apt install build-essential cmake`)
8. **Disk space**: Docker images for all services total ~15-20 GB; plan accordingly
9. **`restrict_to_workspace: false`** is needed if the agent should access files outside `~/.beesgo/workspace`
10. **Hindsight env var duplication**: The watchdog deduplicates `HINDSIGHT_*` env vars. If Hindsight ignores your `.env` settings, check for conflicting system env vars
11. **Skyvern OPENAI_API_KEY**: Skyvern requires this env var to start. The docker-compose.yml sets a dummy key — BeesGo routes LLM calls through its own providers
12. **Firecrawl self-hosted**: No API key needed — `USE_DB_AUTHENTICATION=false` in docker-compose.yml
13. **`uv` not found**: Install with `curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc`
14. **make build fails at generate**: Run `make clean && rm -rf cmd/beesgo/workspace && make build`

> [!TIP]
> Read `references/troubleshooting.md` bundled with this skill for detailed solutions to each issue.
