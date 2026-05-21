# BeesGo Spawn — Troubleshooting Guide

All issues documented here were encountered during real deployment sessions.

---

## Table of Contents

1. [Go: command not found](#1-go-command-not-found)
2. [Docker: permission denied](#2-docker-permission-denied)
3. [Hindsight crash-loop / API key error](#3-hindsight-crash-loop)
4. [Hindsight pgvector glibc error](#4-hindsight-pgvector-glibc-error)
5. [Hindsight DATABASE_URL wrong port](#5-hindsight-database_url-wrong-port)
6. [Firecrawl containers fail to start](#6-firecrawl-containers-fail)
7. [Skyvern OPENAI_API_KEY required](#7-skyvern-openai-api-key)
8. [Skyvern postgres volume conflict](#8-skyvern-postgres-conflict)
9. [Python venv / pip failures](#9-python-venv-failures)
10. [uv: command not found](#10-uv-not-found)
11. [Port already in use](#11-port-already-in-use)
12. [deps/ directory is empty](#12-deps-directory-empty)
13. [make build fails with generate errors](#13-make-build-generate-errors)
14. [BeesGo Gateway won't start](#14-gateway-wont-start)
15. [Config paths with tilde (~) not expanding](#15-tilde-expansion)
16. [Model tier env var overrides ignored](#16-model-tier-env-vars)

---

## 1. Go: command not found

**Symptom:** `make build` fails with `go: command not found` even though you just installed Go.

**Cause:** Go was installed to `/usr/local/go/bin` but the PATH was only set in the current terminal session, not persisted.

**Fix:**
```bash
# Add to ~/.bashrc (NOT just the current shell)
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Verify
which go
go version
```

**Why it happens:** `make` spawns subshells that don't inherit the current shell's temporary PATH exports. The PATH must be in a file that's sourced by new shells.

---

## 2. Docker: permission denied

**Symptom:** `docker compose up -d` returns "permission denied" or "Cannot connect to the Docker daemon".

**Cause:** The current user is not in the `docker` group, or the group membership hasn't taken effect.

**Fix:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply immediately (without logout)
newgrp docker

# Verify
docker ps
```

**Alternative:** Log out and log back in for group changes to take effect system-wide.

---

## 3. Hindsight crash-loop

**Symptom:** Hindsight API starts and immediately exits. Logs show an error about missing LLM API key.

**Cause:** `HINDSIGHT_API_LLM_API_KEY` is not set or empty.

**Fix:**
```bash
# Create ~/.beesgo/.env with:
HINDSIGHT_API_LLM_PROVIDER=gemini
HINDSIGHT_API_LLM_API_KEY=your-actual-gemini-api-key
HINDSIGHT_API_LLM_MODEL=models/gemini-2.5-flash-lite
HINDSIGHT_API_DATABASE_URL=postgresql://hindsight:hindsight@localhost:5433/hindsight
```

**For manual start:**
```bash
cd deps/hindsight/hindsight-api
HINDSIGHT_API_LLM_API_KEY=your-key \
HINDSIGHT_API_LLM_PROVIDER=gemini \
HINDSIGHT_API_DATABASE_URL=postgresql://hindsight:hindsight@localhost:5433/hindsight \
uv run uvicorn app.main:app --host 0.0.0.0 --port 8888
```

---

## 4. Hindsight pgvector glibc error

**Symptom:** Hindsight fails on startup with error like:
```
/lib/x86_64-linux-gnu/libc.so.6: version 'GLIBC_2.38' not found
```

**Cause:** The embedded `pg0` database bundles a `vector.so` (pgvector) compiled against glibc 2.38. Ubuntu 22.04 ships glibc 2.35.

**Fix:** Use Docker PostgreSQL+pgvector instead of embedded pg0:
```bash
cd deps/hindsight
docker compose up -d
# Uses pgvector/pgvector:pg17 on port 5433
```

Then set in `.env`:
```bash
HINDSIGHT_API_DATABASE_URL=postgresql://hindsight:hindsight@localhost:5433/hindsight
```

---

## 5. Hindsight DATABASE_URL wrong port

**Symptom:** Hindsight starts but can't connect to PostgreSQL.

**Cause:** The Docker PostgreSQL runs on port **5433** (to avoid conflicts), but the config might point to 5432.

**Fix:** Ensure the DATABASE_URL uses port **5433**:
```bash
HINDSIGHT_API_DATABASE_URL=postgresql://hindsight:hindsight@localhost:5433/hindsight
```

---

## 6. Firecrawl containers fail

**Symptom:** `docker compose up -d` in `deps/firecrawl/` errors out or containers keep restarting.

**Common causes & fixes:**

- **Port 3002 in use:** `ss -tlnp | grep 3002` → stop the conflicting service
- **Insufficient resources:** Firecrawl API needs 4 CPU + 8GB RAM, Playwright needs 2 CPU + 4GB
- **Missing .env:** Some configs reference a `.env` file — create one with defaults if missing
- **Docker network conflict:** `docker network prune` (careful: removes unused networks)
- **Out of disk space:** `docker system df` then `docker system prune`
- **RabbitMQ health check:** RabbitMQ has a 30s start period — wait for it before panicking

---

## 7. Skyvern OPENAI_API_KEY

**Symptom:** Skyvern container fails to start with an OpenAI API key error.

**Cause:** Skyvern requires `OPENAI_API_KEY` to be set as an env var to pass its startup check, even when you're not using OpenAI.

**Fix:** The docker-compose.yml already sets a dummy key:
```yaml
OPENAI_API_KEY: "sk-dummy-key-to-bypass-startup-check"
```
BeesGo routes LLM calls through its own providers, so this dummy key is fine.

---

## 8. Skyvern postgres conflict

**Symptom:** Skyvern's postgres container conflicts with another postgres.

**Fix:** Each compose stack uses its own Docker network, so internal port 5432 doesn't conflict. If there's a host-level conflict, check if either compose file exposes 5432 to the host. Skyvern's postgres only exposes to the `backend` network, not the host.

---

## 9. Python venv failures

**Symptom:** `make setup-venv` or `make rag-setup` fails installing packages.

**Common fixes:**

```bash
# pyaudio needs PortAudio headers
sudo apt install portaudio19-dev

# opencv may need build tools
sudo apt install build-essential cmake

# If pip itself fails
python3 -m pip install --upgrade pip

# If venv creation fails
sudo apt install python3-venv

# If python3 is missing entirely
sudo apt install python3 python3-pip python3-venv
```

**For RAG-Anything specifically:**
```bash
# If deps/raganything/src is missing:
git clone --depth 1 https://github.com/HKUDS/RAG-Anything.git deps/raganything/src
```

---

## 10. uv: command not found

**Symptom:** `uv sync` fails because `uv` is not installed. Needed for Hindsight.

**Fix:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc   # or restart terminal
uv --version
```

---

## 11. Port already in use

**Symptom:** A service fails to bind because the port is taken.

**Diagnostic:**
```bash
# Check all BeesGo-related ports at once
for port in 3002 8000 8080 8888 9999 5433 18790; do
  echo -n "Port $port: "
  ss -tlnp | grep ":$port " || echo "available"
done
```

**Fix:** Stop the conflicting service or change the port:
- Firecrawl: set `FIRECRAWL_PORT=3003` before `docker compose up`
- Skyvern: set `SKYVERN_PORT=8001` before `docker compose up`
- Others: edit the relevant docker-compose.yml or config.json

---

## 12. deps/ directory empty

**Symptom:** `deps/firecrawl/`, `deps/skyvern/`, or `deps/hindsight/` are empty.

**Cause:** These may be git submodules that weren't initialized, or they need manual cloning.

**Fix:**
```bash
# Try git submodules first
git submodule update --init --recursive

# If that doesn't work, clone manually:
# (Hindsight is the most common one to be missing)
cd deps/hindsight && git clone --depth 1 https://github.com/vectorize-io/hindsight.git .
```

---

## 13. make build fails with generate errors

**Symptom:** `make build` fails at the `go generate` step.

**Cause:** The embedded workspace files may have stale artifacts.

**Fix:**
```bash
make clean
rm -rf cmd/beesgo/workspace 2>/dev/null || true
make build
```

---

## 14. Gateway won't start

**Symptom:** `beesgo gateway` exits immediately or shows "no channels enabled".

**Fix:** Ensure at least one channel is enabled in `~/.beesgo/config.json`:
```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_TOKEN",
      "allow_from": ["YOUR_USER_ID"]
    }
  }
}
```

Also verify the gateway port (18790) is available:
```bash
ss -tlnp | grep 18790
```

---

## 15. Config paths with tilde (~) not expanding

**Symptom:** BeesGo can't find service directories despite config looking correct.

**Cause:** Some config fields require absolute paths. Tilde (`~`) expansion only works for certain fields like `workspace` and `media_dir`.

**Fix:** Use full absolute paths for these fields:
- `tools.firecrawl.compose_dir`
- `hindsight.service_dir`
- `hindsight.control_panel.service_dir`
- `hindsight.skills_ingestion.source_dir`
- `self_dev.source_dir`

```json
"service_dir": "/home/owner03/Documents/GitHub/BeesGo-Agent/deps/hindsight/hindsight-api"
```

---

## 16. Model tier env var overrides ignored

**Symptom:** Setting `PICOCLAW_TIER_DIRECTOR_MODEL=...` doesn't change the model used.

**Cause:** Environment variable names use the legacy prefix `PICOCLAW_`, not `BEESGO_`.

**Fix:** Use the exact variable names:
```bash
PICOCLAW_TIER_DIRECTOR_PROVIDER=anthropic
PICOCLAW_TIER_DIRECTOR_MODEL=claude-opus-4-0520
PICOCLAW_TIER_DIRECTOR_API_KEY=sk-ant-xxx
PICOCLAW_TIER_DIRECTOR_API_BASE=https://api.anthropic.com/v1
```

These override the corresponding fields in `config.json` under `agents.defaults.model_tiers.director`.
