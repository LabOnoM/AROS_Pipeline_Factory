---
description: Clarify research objectives, brainstorm directions, and make a plan before running super_scientist.
---

# Research Discovery Workflow
> **Slash command:** `/research-discovery`
> **Purpose:** Multi-turn conversation to clarify research objectives, brainstorm directions, and generate a plan before launching `super_scientist`.

---

## Pre-Flight — Read Before Every Launch

**Before launching any run**, check the `kosmos_pipeline_operations` KI for:
- Model must be `gemini/gemini-2.5-pro` (never `3.1-pro-preview`)
- Output must go to the **project folder**, not `.gemini/antigravity/artifacts/`
- `write_paper=True` must always be set
- ScholarEval thresholds calibrated for qualitative (0.50/0.40) vs quantitative (0.75/0.70)

---

## When to Use

Use **before** `super_scientist` when:
- The research question is broad or vague
- The user is unsure which angle to investigate
- Multiple competing hypotheses exist
- The user hasn't articulated data, constraints, or success criteria

Do **not** use when the user provides a precise, well-scoped hypothesis.

---

## Workflow Phases

// turbo-all

### Phase 0 — Intake (1 message)

**Goal:** Receive the raw query and align with **Kosmos Best Practices**. Start asking, not answering.

1. Acknowledge the research area warmly but do not synthesize yet.
2. Ask **3 intake questions** (all in one message):
   - Q1. *"What is the core puzzle you want to solve? (Should be hypothesis-driven, not a simple lookup.)"*
   - Q2. *"What complex, PROCESSED datasets are you working with? Are columns/layers cleanly labeled?"*
   - Q3. *"What nuances or past assumptions should I know, as if briefing a new colleague?"*
3. Tell the user: *"I'll use your answers to build an optimized query for Kosmos."*

---

### Phase 1 — Clarification (2–4 turns)

**Goal:** Understand domain, data quality, multi-faceted objectives, assumptions, constraints, and prior failures.

**Rules:**
- Max 2 questions per turn
- **Enforce Best Practices:** Push simple lookups toward mechanistic hypotheses
- **Enforce Data Hygiene:** Ask about column labels and data dictionaries
- Go deeper on previous answers; challenge implicit assumptions

| If user says... | Probe with... |
|-----------------|---------------|
| "I want to know why X happens" | "Is X the cause or a correlate?" |
| "List DEGs between groups" | "Can we expand to regulatory pathways?" |
| "We have raw sequencing data" | "Have you generated count matrices yet?" |
| "Analyze this metadata table" | "Are column definitions labeled clearly?" |

**Ends when:** You can fill all fields in the Convergence Summary (Phase 3).

---

### Phase 2 — Brainstorm (1–2 turns)

**Goal:** Offer 3–5 unexpected angles. Be intellectually bold.

> *"Let me propose directions you might not have considered. Push back — disagreement is useful."*

Each angle: `**[Name]** → Hypothesis / Why unexpected / Prediction / Risk`

Then ask: *"Which resonates? Which feels wrong? Missing directions?"*

For example angles, read `research_discovery_templates` KI.

---

### Phase 3 — Convergence (1 turn)

**Goal:** Narrow to 1–3 testable hypotheses and confirm.

Present a **Convergence Summary** with: Core Question, H1/H2, Anti-scope, Domain, Expected output, Constraints (data, time, compute).

> *"Does this capture what you want? Edit any line — this becomes the exact input."*

Wait for explicit confirmation.

---

### Phase 4 — Research Plan Generation

**Goal:** Generate a complete execution plan for `super_scientist`.

Use the full template from `research_discovery_templates` KI (sections 1–10: Objective, Hypotheses, Literature Context, Experiment Design, Success Criteria, Anti-Goals, Execution Params, Swarm Config, Timeline, Post-Run Actions).

**Critical:** Set `artifacts_dir` to the user's project folder — ask the user where they want the output saved. Default to CWD, never to `.gemini/`.

---

### Phase 5 — Approval and Launch

**Goal:** Get explicit approval, then fire `super_scientist`.

Offer: Approve as-is / Edit / Save for later. On approval, confirm exact parameters:
- Objective, Domain
- Cycles (1=fast, 2-3=thorough), Tasks/cycle (3-5)
- BFTS steps (3=fast, 9=standard, 21=publication)
- Paper: yes
- **Output dir:** project folder path (confirm with user)
- **Model:** gemini/gemini-2.5-pro (hardcoded, do not change)

Then invoke `kosmos_super_scientist` MCP tool.

---

## Post-Run Checklist

After pipeline completes:
1. Check `paper/paper.html` exists — if not, run `generate_paper.py --artifacts <dir>`
2. Check `Validated: N/M` counts in `pipeline.log` — if 0/M, thresholds need recalibration
3. Ingest results with `/wiki-ingest` if the project has an LLM-Wiki

---

### Phase 6 — AROS Memory Ingestion (Manual, with Active Reminder)

**Goal:** Close the Collective Intelligence loop by feeding validated Kosmos findings into brain.db.

> [!IMPORTANT]
> This step is **MANUAL by design**. Never auto-ingest. Always prompt the user to review Kosmos output quality before committing to permanent memory.

**After the pipeline completes, you MUST actively prompt the user with this message:**

> 🔬 **Your Kosmos run has completed.** Would you like to ingest the findings into AROS memory?
>
> This will:
> - Add validated findings as **world_facts** in brain.db
> - Feed the **Knowledge Distiller** for clustering and GEPA proposal generation
> - Improve **pre-flight context** in future research sessions
>
> To proceed, I'll call:
> `ingest_kosmos_findings(artifacts_dir="<project_dir>", run_label="<topic>")`
>
> **Shall I go ahead?** (You can also do this later from the Dashboard → Kosmos Research Integration panel)

**On user approval:**
1. Call `ingest_kosmos_findings(artifacts_dir="<project_dir>", run_label="<topic>")`
2. Verify report: `findings_ingested > 0` and `status == "success"` or `"partial"`
3. Call `trigger_consolidation()` to force a dream cycle immediately
4. Inform the user: *"Findings are now in the AROS Knowledge Distiller pipeline."*

**If path resolution fails** (status="error"):
- Try the Smart Path Resolution fallback: pass just the directory name (basename)
- Or open the Dashboard → Kosmos Research Integration panel and enter the path manually

---

## Agent Persona

Curious (not interrogating), intellectually bold, practically grounded, good memory, non-assuming, anti-scope-creep. Full persona details in `research_discovery_templates` KI.
