---
description: Dual-agent pipeline for scientific manuscript writing, data extraction, and peer-review evaluation.
---

# Global Workflow: /manuscript-write
## Dual-Agent Autonomous Manuscript Pipeline

## ⚠️ CARDINAL RULE: MARKDOWN-FIRST AUTHORING (HARD PROHIBITION)
**AI agents MUST write all scientific manuscript content in Markdown (`.md`) format FIRST.**
**Direct LaTeX (`.tex`) authoring by any AI agent is STRICTLY PROHIBITED.**
See `markdown_first_manuscript_policy` KI for root-cause documentation.

## Required AROS Context
Load KIs: `agentic_manuscript_publishing`, `markdown_first_manuscript_policy`, `agentic_diagramming_standard`.
Policies: `output-truncation-management`, `gepa_protocol`, `self_healing_environment_policy`.
Skill list: see **COMPLETE SKILL INTEGRATION** at end of this workflow.

## ✅ MANDATORY AUTHORING PROTOCOL (ALL AGENTS)

### Phase 0: Source File Recovery (MANDATORY before any edit)
> **NEVER rely on conversational memory for document content.**
> If any Checkpoint has occurred or document exceeds 500 words,
> you MUST `view_file` or `cat` the source before making edits.

### Phase 0.5: Reference Inventory & Retrieval (MANDATORY before drafting)
> **Drafting MUST NOT begin until all cited references are verified or retrieved.**

1. **Inventory**: Scan `.wiki/` and `00.RawData/Literature/03_Parsed_Markdown/`.
2. **Gap Detection**: Cross-reference bibliography against ingested papers.
3. **Auto-Retrieval**: Trigger `/literature-ingest` for missing DOIs/PMIDs.
4. **Retraction Scan**: Run `retraction-watcher`. Retracted citation → **HALT**.
5. **Verification Gate**: Confirm papers in `03_Parsed_Markdown/` + `04_Parsed_JSON/`.

### Phase 1: Write in Markdown
- Author in `<manuscript_root>/<name>.md` using IMRAD structure
- Figures: `![Caption](figures/figN.png)` — no LaTeX figure environments
- Citations: `[1]`, `[2]` with `## References` section at end

### Phase 2: Generate Figures (Python/Matplotlib)
- ≥300 DPI PNG to `<manuscript_root>/figures/`
- Use publication-grade defaults from `dual_agent_workflow_details.md`

### Phase 3: Multi-Format Conversion (Pandoc — NEVER manual LaTeX)

**Conda-Gated Preflight** (SPEC §4.4): Activate `aros-base` env (L0→L1). Verify `pandoc` (CRITICAL), `tectonic` (IMPORTANT) via `conda list -n aros-base`.

```bash
python3 figures/generate_figures.py
pandoc <name>.md -o manuscript.tex --standalone --resource-path=.:figures
tectonic manuscript.tex -o output/           # skip if unavailable
pandoc <name>.md -o output/manuscript.docx --resource-path=.:figures
ls -lh output/manuscript.pdf output/manuscript.docx 2>/dev/null
```

Optional HTML: `python3 01.Shared_Assets/Skills/md-html-docx-generator/scripts/build_report.py <name>.md -o output/manuscript_report.html`

### Phase 4: Surgical LaTeX Improvements (post-conversion only)
Limited edits via `multi_replace_file_content` ONLY for: figure placement, `\usepackage{}`, Unicode fixes, State Header. **Never rewrite text in LaTeX.**

## AGENT A — Generator Agent
Details in `agentic_manuscript_publishing` KI (`dual_agent_workflow_details.md`).

### Phase A1: Wiki-First Discovery & Deep Reading
1. Read `.wiki/overview.md`, `.wiki/entities/*.md`, Project Registry
2. Run `literature-close-read` on each critical paper in `03_Parsed_Markdown/`
3. File sweep for raw data; write `DATA_AUDIT.md`

### Phase A1.5: Graphical Abstract (Optional)
Use `visualize-data` with `fireworks-tech-graph` engine. Save to `figures/graphical_abstract.svg`.

### Phase A2–A5: Data → Figures → Draft → Verify
Extract data, generate figures, write full `.md`, run Pandoc pipeline, verify PDF, set State Header.

## AGENT B — Reviewer Agent
12-dimension scoring (max 120). Dimension 8 = **Citation Integrity** (verify ALL citations grounded + retraction-watcher).

Output each round as `## Round N` in `<manuscript_root>/REVIEW_LOG.md` with scores, `[UNGROUNDED]` flags, revision instructions.

## Citation-Before-Claim Protocol (MANDATORY)
Before writing any evidence-based claim, ground it:
```
GROUNDING CHECK:
  Claim: "[text]"  Source: "[exact quote]"  File: [path]  Verdict: GROUNDED/NOT_FOUND
```
If `NOT_FOUND` → `/wiki-research` or flag `[UNGROUNDED]` and halt.

## THE ITERATION LOOP
> **Minimum 3 review rounds MANDATORY regardless of initial score.**

(Min: 3; Max: 5; Pass: 92/120; Dims 11 & 12 must be 10/10)
1. Agent A: Phase 0.5 → write `.md` → figures → Pandoc → State Header
2. Agent B: score 12 dims → `## Round N` in `REVIEW_LOG.md`
3. If pass before Round 3: Agent B runs hardening review (Dims 7, 8, 12)
4. If criteria met after ≥3 rounds: PASS. Else: loop.

## COMPLETE SKILL INTEGRATION
- **Pre-Draft**: `literature-ingestion`, `literature-close-read`, `retraction-watcher`, `literature-review`, `reference-search`, `bgpt-paper-search`, `hypothesis-generation`
- **Drafting**: `abstract-summarizer`, `method-writing`, `discussion-section-architect`, `study-limitations-drafter`, `scientific-critical-thinking`
- **Stats & Viz**: `scientific-visualization`, `statistical-analysis`, `seaborn`, `survival-analysis-km`, `volcano-plot-script`, `visualize-data`
- **Review**: `peer-review`, `reproducibility-check`, `result-figure-consistencycheck`
- **Delivery**: `md-html-docx-generator`, `secure-html-delivery`, `word-read-write`
- **Post-Acceptance**: `lay-summary-gen`, `scientific-slides`