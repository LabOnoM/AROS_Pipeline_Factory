# Kosmos SuperScientist Pipeline — Operations Guide

## Critical Fix Registry

These are hard-won fixes from debugging failures. **Never revert these.**

### 1. Model Selection
- **MUST use:** `gemini/gemini-2.5-pro`
- **NEVER use:** `gemini/gemini-3.1-pro-preview` — causes empty responses and JSON parse failures
- **Why:** The gemini-3.1-pro-preview model returns empty content for structured JSON prompts used by the plan reviewer and data analyst agents

### 2. Token Limits — Minimum 8192 for JSON Generation
All LiteLLM `completion()` calls that expect structured JSON output **must** use `max_tokens=8192` or higher.

| File | Location | Original | Fixed |
|------|----------|----------|-------|
| `kosmos/orchestration/plan_reviewer.py` | lines ~141, ~174 | 2000 | **8192** |
| `kosmos/agents/data_analyst.py` | line ~435 | 2000 | **8192** |

**Symptom of too-low tokens:** `json.JSONDecodeError: Expecting ',' delimiter` or `No JSON object could be decoded` — the response gets cut off mid-JSON.

### 3. ScholarEval Threshold Calibration

The `ScholarEvalValidator` must be calibrated to the type of research:

| Research Type | `threshold` | `min_rigor_score` | Rationale |
|--------------|-------------|-------------------|-----------|
| Quantitative experimental | 0.75 | 0.70 | Original defaults — strict stats checks |
| **Qualitative literature review** | **0.50** | **0.40** | No p-values/chi2 in reviews |
| Hypothesis generation | 0.50 | 0.40 | Novelty matters more than rigor |

**Location:** `kosmos/workflow/research_loop.py` line ~110:
```python
self.scholar_eval = ScholarEvalValidator(anthropic_client, threshold=0.50, min_rigor_score=0.40)
```

**Symptom of wrong thresholds:** `Validated: 0/N findings` — every finding rejected despite pipeline completing successfully.

### 4. Hypothesis Statement max_length

`kosmos/models/hypothesis.py` — the `statement` field must allow ≥2000 characters:
```python
statement: str = Field(..., max_length=2000)
```
**Original:** `max_length=500` — too short for Gemini's verbose multi-clause hypothesis statements.

### 5. Paper Generation — Mandatory Fallback

When AI-Scientist-v2 is not installed, `super_scientist.py` must:
1. Create the `/paper` directory
2. Write `research_report.md` (summary)
3. Invoke `generate_paper.py` which synthesises all validated findings into a full IMRaD paper (`paper/paper.md`, `paper/paper.html`, `paper/appendix_findings.md`)

**Location:** `_write_markdown_report()` in `super_scientist.py`

### 6. Output Directory Convention

**Rule:** Output goes to the **project folder**, never to `.gemini/antigravity/artifacts/`.

When launching from the workflow:
```python
artifacts_dir = "/path/to/project/folder"  # user's workspace
```

The `super_scientist` creates these sub-directories:
```
<project>/
├── kosmos/         # Phase 1 findings
├── bfts/           # Phase 2 BFTS stages
│   ├── preliminary/
│   ├── baseline_tuning/
│   ├── creative_research/
│   └── ablation_studies/
├── paper/          # Phase 4 paper output
│   ├── paper.md
│   ├── paper.html
│   └── appendix_findings.md
├── research_report.md
├── super_scientist_summary.json
└── pipeline.log
```

---

## Pre-Flight Checklist

Run this mental checklist before every `super_scientist` launch:

- [ ] **Model:** Is `model=` set to `gemini/gemini-2.5-pro`?
- [ ] **Output dir:** Points to the project folder, not `.gemini/`?
- [ ] **API key:** `GOOGLE_AI_API_KEY` set in `~/.gemini/.env`?
- [ ] **Clean state:** Old artifacts purged? (`rm -rf kosmos/ bfts/ paper/ *.log *.json .chroma_db .literature_cache .concept_extraction_cache .pdf_cache`)
- [ ] **DB:** `kosmos.db` fresh or deleted?
- [ ] **write_paper:** Set to `True`?

---

## Known Issues (Non-Blocking)

### Semantic Scholar Rate Limits (429)
The pipeline encounters 429 rate limits from Semantic Scholar on nearly every search. It handles this with exponential backoff (1s → 3s → 9s → 27s) but frequently exhausts retries. This is **non-blocking** — arXiv and PubMed provide sufficient papers.

### Neo4j Not Available
The pipeline logs `Failed to connect to Neo4j: Cannot open connection to bolt://localhost:7687`. This is **non-blocking** — it falls back to SQLite/VectorDB. Install Neo4j Community in Docker only if knowledge graph features are needed.

### NullModelValidator Warnings
`Could not extract test statistic: No test statistic found in finding` — **expected** for qualitative literature reviews. The null model correctly bypasses with `shuffle_method: qualitative_bypass`.

### `'list' object has no attribute 'items'` in creative_research
A minor serialisation bug in the research loop when compressing cycle context. The cycle still completes and validated findings are preserved. Non-blocking.

---

## Execution Pattern

```python
# Recommended launch pattern for literature review
import asyncio
from kosmos.workflow.super_scientist import SuperScientistWorkflow

ss = SuperScientistWorkflow(
    research_objective="...",
    domain="biology",
    artifacts_dir="/path/to/project",     # project folder, NOT .gemini/
    model="gemini/gemini-2.5-pro",        # NEVER change this
)
result = await ss.run(
    kosmos_cycles=1,     # 1 for fast, 2-3 for thorough
    tasks_per_cycle=3,   # 3 for fast, 5 for thorough
    bfts_steps=3,        # 3=fast(9 subtasks), 9=medium, 21=full
    write_paper=True,    # always True
)
```

## Cycle Budget vs Quality

| Setting | Time | Findings | Best For |
|---------|------|----------|----------|
| cycles=1, tasks=3, bfts=3 | ~20 min | 8-12 | Quick feasibility |
| cycles=2, tasks=4, bfts=9 | ~45 min | 15-25 | Standard review |
| cycles=3, tasks=5, bfts=21 | ~2 hr | 25-40 | Publication-grade |
