# Dual-Agent Autonomous Manuscript Pipeline

## ⚠️ CARDINAL RULE: MARKDOWN-FIRST AUTHORING (HARD PROHIBITION)
**AI agents MUST write all scientific manuscript content in Markdown (`.md`) format FIRST.**
**Direct LaTeX (`.tex`) authoring by any AI agent is STRICTLY PROHIBITED.**

## Required AROS Context
Load KIs: `agentic_manuscript_publishing`, `markdown_first_manuscript_policy`, `agentic_diagramming_standard`.
Policies: `output-truncation-management`, `gepa_protocol`, `self_healing_environment_policy`.

## ✅ MANDATORY AUTHORING PROTOCOL (ALL AGENTS)

### Phase 0: Source File Recovery (MANDATORY before any edit)
> **NEVER rely on conversational memory for document content.**
> If any Checkpoint has occurred or document exceeds 500 words, you MUST `view_file` or `cat` the source before making edits.

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
Activate `aros-base` env. Verify `pandoc` (CRITICAL), `tectonic` (IMPORTANT).
Convert `.md` to `.tex`, `.pdf`, and `.docx` using pandoc and tectonic.

### Phase 4: Surgical LaTeX Improvements (post-conversion only)
Limited edits via `multi_replace_file_content` ONLY for: figure placement, `\usepackage{}`, Unicode fixes, State Header. **Never rewrite text in LaTeX.**

## AGENT A — Generator Agent
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