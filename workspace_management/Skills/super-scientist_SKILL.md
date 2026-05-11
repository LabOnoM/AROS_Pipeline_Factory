---
name: super-scientist
description: >
  Unified autonomous research system merging Kosmos (literature mining,
  multi-agent hypothesis generation, knowledge graphs, ScholarEval validation)
  with AI-Scientist-v2 (Best-First Tree Search experiment optimization, LaTeX
  paper writing, VLM peer review). No Docker required — runs natively on the
  isolated Antigravity machine. All 530+ Antigravity skills are auto-injected
  into Kosmos agents via SkillLoader. Use when the user mentions "autonomous
  research", "full pipeline", "hypothesis to paper", "SuperScientist",
  "super scientist", "deep research on [topic]", "Kosmos + AI Scientist",
  or "run an experiment loop".
---

# SuperScientist: Kosmos + AI-Scientist-v2

> Sources: [Kosmos](https://github.com/jimmc414/Kosmos) · [AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)
> No Docker needed — Antigravity machine IS the sandbox.

> [!TIP]
> **New to SuperScientist?** Use `/research-discovery` first.
> That workflow runs a multi-turn brainstorm conversation to clarify your goals, challenge assumptions, and generate a detailed research plan — then hands it off to `super_scientist` automatically.
> Use the CLI or Python API below only when you already have a precise, well-scoped hypothesis.

## Pipeline Overview

| Phase | Engine | What happens | Output |
|-------|--------|--------------|--------|
| 1 | **Kosmos** | Literature mining → multi-agent hypothesis generation | Ranked hypotheses |
| 2 | **AIS-v2 BFTS** | 4-stage tree search experiment optimization | Optimized experiments |
| 3 | **Kosmos** | ScholarEval 8-dimension quality validation | Quality score |
| 4 | **AIS-v2** | LaTeX paper + VLM figure review + peer review | PDF paper |
| 5 | **Kosmos** | Knowledge graph update (Neo4j/ChromaDB) | Persistent KG |
| 6 | **Antigravity** | `/wiki-ingest` → LLM-Wiki | Updated wiki |

## Quick Run (CLI)

```bash
# Load environment
source /home/owner03/.gemini/.env

cd /home/owner03/.gemini/antigravity/mcp_servers/Kosmos

# Full pipeline
python -m kosmos.workflow.super_scientist \
  "What transcriptional programs drive bone repair at 5, 10, 14 days?" \
  --domain biology \
  --kosmos-cycles 3 \
  --bfts-steps 21 \
  --output-dir ./artifacts/bone_repair

# Faster (no paper writing)
python -m kosmos.workflow.super_scientist \
  "Your research question here" \
  --domain biology \
  --kosmos-cycles 2 \
  --bfts-steps 9 \
  --no-paper \
  --output-dir ./artifacts/quick_run
```

## Python API

```python
import asyncio, sys, dotenv

# Load keys
dotenv.load_dotenv("/home/owner03/.gemini/antigravity/mcp_servers/Kosmos/.env")
dotenv.load_dotenv("/home/owner03/.gemini/.env", override=False)

sys.path.insert(0, "/home/owner03/.gemini/antigravity/mcp_servers/Kosmos")

from kosmos.workflow.super_scientist import SuperScientistWorkflow

async def run():
    ss = SuperScientistWorkflow(
        research_objective="What immune cells drive bone repair failure in aged mice?",
        domain="biology",
        artifacts_dir="./artifacts/bone_repair",
    )
    result = await ss.run(
        kosmos_cycles=3,
        bfts_steps=21,
        write_paper=True,
    )
    print(f"Paper → {result['paper_path']}")
    print(f"Score → {result['validation']}")
    return result

result = asyncio.run(run())
```

## Swarm Mode (parallel sub-questions)

```python
import asyncio, sys, dotenv
dotenv.load_dotenv("/home/owner03/.gemini/antigravity/mcp_servers/Kosmos/.env")
dotenv.load_dotenv("/home/owner03/.gemini/.env", override=False)
sys.path.insert(0, "/home/owner03/.gemini/antigravity/mcp_servers/Kosmos")

from kosmos.workflow.super_scientist import SuperScientistWorkflow

sub_questions = [
    "What immune cell changes occur in aged bone repair?",
    "What angiogenic deficits occur in aged fracture healing?",
    "What osteoprogenitor senescence markers predict repair failure?",
]

async def run_worker(q, i):
    ss = SuperScientistWorkflow(q, domain="biology",
                                artifacts_dir=f"./artifacts/worker_{i}")
    return await ss.run(kosmos_cycles=2, bfts_steps=9, write_paper=False)

async def swarm():
    results = await asyncio.gather(*[run_worker(q, i)
                                     for i, q in enumerate(sub_questions)])
    return results

results = asyncio.run(swarm())
```

## Accessing All 530+ Antigravity Skills

The `AntigravitySkillLoader` is auto-used in Phase 1. You can also query it
directly to see what skills are available for a domain:

```python
from kosmos.agents.skill_loader import SkillLoader as AntigravitySkillLoader

loader = AntigravitySkillLoader()
print(loader.describe())

# Get skills for spatial transcriptomics
prompt_snippet = loader.load_skills_for_task(domain="spatial")
print(prompt_snippet[:500])
```

## ENV Configuration

Key variables in `.env`:

```bash
ENABLE_SANDBOXING=false              # No Docker — use NativeExecutor
KOSMOS_SKILLS_DIR=/home/owner03/.gemini/skills  # All 530+ skills
LITELLM_MODEL=gemini/gemini-3.1-pro-preview     # Latest Gemini
LLM_RATE_LIMIT_PER_MINUTE=30
MAX_CONCURRENT_LLM_CALLS=3
```

## Verification

```bash
cd /home/owner03/.gemini/antigravity/mcp_servers/Kosmos

# Test NativeExecutor
python -c "
from kosmos.execution.native_executor import NativeExecutor
e = NativeExecutor()
r = e.execute('print(\"RESULT:\"+str({\"ok\":True}).__repr__())')
print('NativeExecutor:', 'OK' if r.success else 'FAIL', r.stdout[:80])
"

# Test Antigravity skill loading
python -c "
import os; os.environ['KOSMOS_SKILLS_DIR']='/home/owner03/.gemini/skills'
from kosmos.agents.skill_loader import SkillLoader as AntigravitySkillLoader
l = AntigravitySkillLoader()
print(l.describe())
"

# Quick smoke test (no paper)
python -m kosmos.workflow.super_scientist \
  "test hypothesis on bone repair" \
  --domain biology --kosmos-cycles 1 --bfts-steps 3 --no-paper \
  --output-dir /tmp/ss_test
```
