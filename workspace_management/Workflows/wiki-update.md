---
description: Maintain, lint, and synthesize the LLM-Wiki to ensure consistency and prevent knowledge rot.
---

# Wiki Update & Lint Workflow

// Note: All commands must execute from the active project root.

Run this workflow periodically (e.g., once a week, or after a massive batch of `/wiki-ingest` operations) to ensure the `.wiki/` knowledge base remains structurally sound and conceptually coherent.

## Step 0.5: PDF Drift Detection (MANDATORY)

> **LAW 3 Enforcement**: Catch any PDFs added to the workspace outside of formal AROS workflows.

1. Scan the workspace for `.pdf` files not yet indexed in `00.RawData/Literature/02_Raw_PDFs/`.
2. For each unindexed PDF, copy it to `02_Raw_PDFs/`.
3. Run the canonical ingestion parser (which auto-installs missing dependencies):
   ```bash
   # // turbo
   python3 01.Shared_Assets/Skills/literature-ingestion/scripts/pdf_converter.py
   ```
4. For all newly parsed PDFs in `03_Parsed_Markdown/`, trigger the `/wiki-ingest` Step 1.5 logic to ensure they are added to the Wiki.

## Step 1: Structural Audit (Linting)

Run the following command in the bash terminal to check for basic structural issues in the `.wiki/` directory.

```bash
# // turbo

echo "=== Orphan Pages (No inbound links) ==="
# Find all markdown files (excluding index, log, SCHEMA) and check if they are referenced anywhere else
for file in $(find .wiki -name "*.md" -not -name "index.md" -not -name "log.md" -not -name "SCHEMA.md"); do
    basename=$(basename "$file" .md)
    # Search for the wikilink [[basename]] in other files
    if ! grep -q "\[\[$basename\]\]" -R .wiki/; then
        echo "Orphan detected: $file"
    fi
done
```

## Step 1.5: Agent Version Control (re_gent) Audit

Before making changes, verify that this workspace is protected by the AI audit layer.
This step implements the **Conda-Gated Self-Healing Pattern** (L0→L1→L2) per SPEC §4.4.

```bash
# // turbo

# --- L0: Ensure Conda ---
if ! command -v conda &> /dev/null; then
    if [ -f "$HOME/miniconda3/bin/conda" ]; then
        eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    elif [ -f "$HOME/anaconda3/bin/conda" ]; then
        eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
    else
        echo "  [WARN] Conda not found. Bootstrapping Miniconda3..."
        curl -fsSL --max-time 120 "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-$(uname -m).sh" \
            -o /tmp/miniconda.sh && bash /tmp/miniconda.sh -b -u -p "$HOME/miniconda3" && \
            eval "$($HOME/miniconda3/bin/conda shell.bash hook)" && rm -f /tmp/miniconda.sh
    fi
fi

# --- L1: Activate aros-base ---
if command -v conda &> /dev/null; then
    eval "$(conda shell.bash hook)"
    if ! conda activate aros-base 2>/dev/null; then
        CMD=$(command -v mamba &>/dev/null && echo "mamba" || echo "conda")
        AROS_YML="01.Shared_Assets/Environments/aros-base.yml"
        [ ! -f "$AROS_YML" ] && AROS_YML="$(find ~ -maxdepth 4 -name 'aros-base.yml' -print -quit 2>/dev/null)"
        if [ -n "$AROS_YML" ]; then
            $CMD env create -f "$AROS_YML" -y && conda activate aros-base
        else
            $CMD create -n aros-base python=3.11 git pandoc go -c conda-forge -y && conda activate aros-base
        fi
    fi
fi

# --- L2: re_gent deployment ---
if [ -d ".regent" ]; then
    echo "✅ re_gent audit layer is active."
else
    echo "re_gent audit layer missing. Attempting deployment..."
    RGT_BIN=""
    command -v rgt &> /dev/null && RGT_BIN="$(command -v rgt)"
    [ -z "$RGT_BIN" ] && [ -x "$HOME/go/bin/rgt" ] && RGT_BIN="$HOME/go/bin/rgt"

    if [ -z "$RGT_BIN" ] && command -v go &> /dev/null; then
        GOBIN="${CONDA_PREFIX:-$HOME/.local}/bin" go install github.com/regent-vcs/regent/cmd/rgt@latest 2>/dev/null && \
            RGT_BIN="${CONDA_PREFIX:-$HOME/.local}/bin/rgt" || \
            echo "  [WARN] rgt compilation failed. Continuing without re_gent."
    fi

    if [ -n "$RGT_BIN" ]; then
        "$RGT_BIN" init --skip-hook 2>/dev/null && {
            grep -qxF ".regent/" .gitignore 2>/dev/null || echo ".regent/" >> .gitignore
            echo "✅ Agent version control deployed."
        } || echo "  [WARN] rgt init failed. Continuing without re_gent."
    else
        echo "  [SKIP] re_gent deployment deferred — Go not available."
    fi
fi
```

## Step 2: Resolve Orphans & Consistency Checks (Check)

This is the semantic linting phase. Make sure the knowledge base is internally consistent:

1. **Resolve Orphans**: If Step 1 reveals orphans, prompt the LLM to read them and add `[[wikilinks]]` to them from relevant entities.
2. **Conflict Detection**: Prompt the agent to check for logical contradictions.
> "Review the recently modified `.wiki/entities/` and `.wiki/sources/`. Identify if any new findings contradict older statements in the wiki. Flag these contradictions for human review."


## Step 3: Global Synthesis

After ingesting new experimental data or papers, the global narrative may have shifted.
Prompt the LLM agent:
> "Please review the recent entries in `.wiki/log.md`. Based on the newly ingested information, do we need to update the theory outined in `.wiki/overview.md` or append an event to `.wiki/timeline.md`?"

## Step 4: Index Rebuild

Ensure `.wiki/index.md` acts as a complete table of contents.
Prompt the agent:
> "Rebuild `.wiki/index.md` so that it categorizes and links to every file within the `.wiki/` directory."

## Step 4.5: AROS Policy Evolution (Phase 4)

Trigger the RL-Informed Context Evolution loop to analyze recent curator rewards and propose updates to `CURATION_POLICY.md`.
Run the following python script via the terminal. It checks the DB lock internally to ensure it doesn't collide with the dashboard daemon.

```bash
# // turbo
python3 -c "import sys; import os; sys.path.insert(0, '/home/ubuntu4/GitHub/AROS/antigravity-evolution/src'); from antigravity_evolution.policy_evolver import propose_policy_update; from antigravity_evolution.policy_analyst import generate_performance_report; report = generate_performance_report(); propose_policy_update(report) if 'error' not in report and report.get('status') != 'insufficient_data' else print('No evolution required: ' + str(report))"
```

## Step 4.6: Daemon Health Verification

Ensure that the core AROS background daemons (including the `mutation_sweeper` and `dreamer`) are executing properly without silent failures.

```bash
# // turbo
python3 -c "import os, sqlite3, time; db_path = os.environ.get('BRAIN_DB_PATH', os.path.expanduser('~/.gemini/antigravity/brain.db')); db = sqlite3.connect(db_path); failed_jobs = db.execute(\"SELECT id, agent_role, created_at, status FROM swarm_jobs WHERE status = 'failed' AND created_at > datetime('now', '-24 hours')\").fetchall(); print(f'\\n=== Daemon Health Report ===\\nFailed Jobs (Last 24h): {len(failed_jobs)}'); [print(f'- {j[1]} (ID: {j[0]}) at {j[2]}') for j in failed_jobs]; db.close()"
```
If this health report shows recent failures for system daemons, check the SwarmDoctor logs in `~/.gemini/antigravity/logs/` to verify auto-healing was engaged.

## Step 5: Auto-Commit

Delegate to the canonical `/lab-commit` workflow. Do NOT write inline `git add` / `git commit` commands here — the lab-commit workflow handles staging, Obsidian symlink verification, project registry updates (e.g., INDEX.csv or PIPELINE_REGISTRY.md), and commit message formatting automatically.
