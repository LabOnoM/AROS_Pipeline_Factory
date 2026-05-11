---
description: Triggers and autonomous dual-agent pipeline for scientific manuscript writing, quantitative data extraction, and rigorous peer-review evaluation
---

# Global Workflow: /manuscript-write
## Dual-Agent Autonomous Manuscript Pipeline

## ⚠️ CARDINAL RULE: MARKDOWN-FIRST AUTHORING (HARD PROHIBITION)
**AI agents MUST write all scientific manuscript content in Markdown (`.md`) format FIRST.**
**Direct LaTeX (`.tex`) authoring by any AI agent is STRICTLY PROHIBITED.**

### Why this rule exists (root-cause documentation — April 2026)
When an AI agent writes long-form scientific text natively in LaTeX, its neural attention
mechanism shifts heavily toward syntactic closure (managing `\begin`/`\end` pairs, escaping
special characters, structuring preambles). This "syntax-cognitive-load" effect causes the
model to aggressively summarize scientific content to guarantee a compilable document —
destroying text depth, citation density, and analytical rigor. In a documented failure case,
a 964-line, 40-citation manuscript was replaced with 93 hollow lines using this approach.

Markdown has negligible syntax overhead, allowing 100% of generation capacity to focus on
scientific content. Conversion to LaTeX, DOCX, and PDF is delegated to Pandoc (deterministic,
lossless) — not to the AI agent.

## Required AROS Context
Before execution, load KIs via `find_helpful_ki`: `agentic_manuscript_publishing`, `markdown_first_manuscript_policy`, `agentic_diagramming_standard`.
Policies: `output-truncation-management`, `gepa_protocol`, `self_healing_environment_policy`.
Full skill integration list: see **COMPLETE SKILL INTEGRATION** section at the end of this workflow.

## ✅ MANDATORY AUTHORING PROTOCOL (ALL AGENTS)
For every manuscript task, regardless of final output format, proceed as follows:

### Phase 0: Source File Recovery (MANDATORY before any edit)
> **NEVER rely on conversational memory for document content.**
> If any Checkpoint has occurred in the session, or if the document exceeds 500 words,
> you MUST physically read the source file from disk using `view_file` or a shell `cat` command
> before making any edits. Failure to do this is the leading cause of content loss.

### Phase 0.5: Reference Inventory & Retrieval (MANDATORY — runs before any drafting)
> **Drafting MUST NOT begin until all cited references are verified or retrieved.**

1. **Inventory**: Scan `<PROJECT_ROOT>/.wiki/` and `00.RawData/Literature/03_Parsed_Markdown/` to identify all currently ingested papers.
2. **Gap Detection**: Cross-reference the project's bibliography (`.wiki/entities/`, `References/` folder, or user-provided DOI list) against ingested papers. Identify any DOIs/PMIDs NOT yet downloaded.
3. **Auto-Retrieval**: If gaps are found, trigger `/literature-ingest` with the missing identifiers. Wait for completion before proceeding.
4. **Retraction Scan**: Run `retraction-watcher` on the full reference list. Any retracted citation triggers a **mandatory HALT** — inform the PI and require a replacement before continuing.
5. **Verification Gate**: Confirm that ALL key cited papers exist in `03_Parsed_Markdown/` (Markdown for LLM context) and `04_Parsed_JSON/` (JSON for structural validation). Flag any that remain missing.

### Phase 1: Write / Edit in Markdown
- All manuscript content is authored or revised in `<manuscript_root>/<name>.md`
- Use standard academic Markdown: headers (`#`, `##`, `###`), bold, italics, numbered lists for references
- Figures are referenced as `![Caption](figures/figN.png)` — do NOT use LaTeX figure environments in the `.md`
- Citations use numbered inline format: `[1]`, `[2]`, etc. with a `## References` section at the end
- **Section structure** follows IMRAD or Review Article conventions as appropriate to journal

### Phase 2: Generate Figures (Python/Matplotlib)
- All figures generated as high-resolution PNG (≥300 DPI) saved to `<manuscript_root>/figures/`
- Figure generation scripts saved to `<manuscript_root>/figures/generate_figures.py`
- Use the publication-grade Matplotlib defaults defined in `dual_agent_workflow_details.md`

### Phase 3: Multi-Format Conversion (Pandoc Pipeline — NEVER manual LaTeX writing)

**Self-Healing Preflight** (per `self_healing_environment_policy.md` — SPEC §4.4):
Before running conversion, the agent MUST verify `pandoc` (CRITICAL) and `tectonic` (IMPORTANT) are available.
If missing, auto-install per the Detect→Repair→Degrade pattern in the policy. If `pandoc` cannot be installed, HALT.
If `tectonic` cannot be installed, skip PDF compilation and proceed with DOCX output only.

Run the following commands **in sequence** from `<manuscript_root>/`:
```bash
# Step 1: Ensure all figures are embedded natively in manuscript.md:
# ![Caption text](figures/figN.png){width=100%}
# NEVER use a post-conversion injection script. See Institutional Memory below.

# Step 2: Generate figure PNG files (≥300 DPI)
python3 figures/generate_figures.py

# Step 3: Markdown → LaTeX (preserves all content, handles syntax automatically)
pandoc <name>.md -o manuscript.tex \
  --standalone \
  --resource-path=.:figures

# Step 4: Compile LaTeX → PDF using Tectonic (self-contained, no TeX Live required)
# Skip if tectonic was not available after self-healing attempt
if command -v tectonic &> /dev/null || [ -x /tmp/tectonic ]; then
    ${TECTONIC_BIN:-tectonic} manuscript.tex -o output/
else
    echo "  [WARN] Skipping PDF compilation — tectonic unavailable."
fi

# Step 5: Markdown → DOCX (for collaborator editing)
pandoc <name>.md -o output/manuscript.docx \
  --resource-path=.:figures

# Step 6: Verify — file size confirms figures are embedded (>>100KB means images present)
ls -lh output/manuscript.pdf output/manuscript.docx 2>/dev/null

# Step 7 (Optional): Markdown → Interactive Standalone HTML Report
# Use when PI requests an interactive deliverable or shareable web version.
python3 01.Shared_Assets/Skills/md-html-docx-generator/scripts/build_report.py \
    <name>.md -o output/manuscript_report.html [--docx]
```

### Phase 4: Surgical LaTeX Improvements (post-conversion only)
After Pandoc conversion, limited LaTeX edits are permitted via `multi_replace_file_content` ONLY for:
- Adjusting figure placement (`[H]`, `[htbp]`)
- Adding journal-specific `\usepackage{}` declarations
- Fixing Unicode character warnings (e.g., `µ` → `$\mu$`)
- Adding the Agentic State Header block
**Never rewrite large blocks of text in LaTeX. Make edits in the `.md` source and re-run the Pandoc pipeline.**

## Cross-Project Institutional Memory
- **No Placeholders**: Do NOT leave `% \includegraphics` commented placeholders. Generate & embed real figures before conversion.
- **Strict Grounding**: Only extract claims natively supported by the `.wiki/` or `00.RawData/`. Never hallucinate external references.
- **Citation-Before-Claim Protocol (MANDATORY)**: Before writing any evidence-based claim, the agent MUST use a scratchpad to ground it:
  ```
  GROUNDING CHECK:
    Claim: "[The proposed claim text]"
    Source: "[Exact quote from .wiki/ page or 03_Parsed_Markdown/ file]"
    File: [path/to/source.md or [[wiki-page]]]
    Verdict: GROUNDED / NOT_FOUND
  ```
  If `NOT_FOUND`, trigger `/wiki-research` or flag the claim as `[UNGROUNDED]` and halt.
- **Dependencies**: Use `numpy<1.25.0`, `scipy>1.10`, `matplotlib<3.8` to prevent binary compatibility issues.
- **Source of Truth**: The `.md` file is ALWAYS the source of truth. The `.tex` file is a derived artifact.

### ⚠️ RETIRED: `fix_latex.py` Figure Injection (April 2026)
**BANNED.** Use native Markdown figure embedding: `![Caption](figures/figN.png){width=100%}`. See `agentic_manuscript_publishing` KI for details.

## AGENT A -- Generator Agent
Agent A is a scientific reasoning agent. Its job is to understand the full experimental picture, make intelligent decisions about data relevance, and produce a manuscript draft with figures.

### Phase A1: Wiki-First File Discovery & Deep Reading
1. **Check Project Knowledge**: Read `<PROJECT_ROOT>/.wiki/overview.md`, `.wiki/entities/*.md`, and the Project Registry (e.g., `00.RawData/INDEX.csv` or `00.RawData/PIPELINE_REGISTRY.md`).
2. **Deep Reading**: For each critical literature paper in `03_Parsed_Markdown/`, run the `literature-close-read` skill to build a structured evidence report before drafting any section that cites it.
3. **File Sweep**: Agent A runs recursive file discovery to locate raw data (`.pzfx`, `.xlsx`, `.czi`, `.fcs`, etc.) matching the wiki entities.
4. **Reasoning**: Write a brief scientific understanding in `DATA_AUDIT.md`.

### Phase A1.5: Graphical Abstract / Workflow Diagram (Optional)
If the target journal requires a graphical abstract or the PI requests an experimental workflow diagram:
1. Use `visualize-data` with the `fireworks-tech-graph` engine (per `agentic_diagramming_standard` KI).
2. Choose the appropriate style: `style-1-flat-icon` for journal figures, `style-4-notion-clean` for clean overviews.
3. Save output to `figures/graphical_abstract.svg` and `figures/graphical_abstract.png`.

### Phase A2 & A3: Data Extraction and Figure Generation
Agent A must adaptively read scientific formats using appropriate Python libraries, compute honest tests, and generate publication-grade figures as PNG to `figures/`. Use `statistical-analysis` and `scientific-visualization` skills.

### Phase A4 & A5: Manuscript Writing and Verification (MARKDOWN-FIRST)
1. Agent A writes the full manuscript in `<name>.md` — complete sections, full citations, exact numbers
2. Agent A runs the Phase 3 Pandoc Pipeline above to produce `.tex`, `.pdf`, `.docx`
3. Agent A verifies PDF page count and that all figures appear embedded correctly
4. Agent A embeds the Agentic State Header in `manuscript.tex` (post-conversion)

## AGENT B -- Reviewer Agent
Agent B acts as a simulated expert peer reviewer, scoring on 12 dimensions:
1. Data Completeness, 2. Figure Quality, 3. Statistical Rigor, 4. Quantitative Specificity,
5. Narrative Coherence, 6. Hypothesis Clarity, 7. Methods Reproducibility, 8. **Citation Integrity** (MUST verify that ALL citations have a corresponding grounded source in `.wiki/` or `03_Parsed_Markdown/`, AND confirm no retracted papers via `retraction-watcher`),
9. Abstract Quality, 10. Novelty and Gap, 11. Technical Soundness, 12. Honest Limitations.

Agent B outputs each review round as a new `## Round N` section in `<manuscript_root>/REVIEW_LOG.md`, with:
- Numeric score per dimension (0–10) and total (max 120)
- Specific `[UNGROUNDED]` flags for any citation without a verified source
- Actionable revision instructions for Agent A

## STATE TRACKING & MANUSCRIPT RESUMPTION
Agent A MUST embed an **Agentic State Header** at the top of `manuscript.tex` (post-conversion).
See `dual_agent_workflow_details.md` in `~/.gemini/antigravity/knowledge/agentic_manuscript_publishing/artifacts/`.

## THE ITERATION LOOP
> **Minimum 3 review rounds are MANDATORY regardless of initial score.**

(Min Iterations: 3; Max Iterations: 5; Pass Threshold: 92/120; Dims 11 & 12 must be 10/10)
1. Agent A forms understanding → runs Phase 0.5 (reference retrieval) → writes `.md` → generates figures → runs Pandoc pipeline → sets State Header
2. Agent B scores 12 dimensions → outputs Review Report as `## Round N` in `REVIEW_LOG.md`
3. **Even if Pass Threshold is met before Round 3:** Agent B MUST continue with a "hardening review" focusing on Citation Integrity (Dim 8), Methods Reproducibility (Dim 7), and Honest Limitations (Dim 12). Log results as Round 2/3 in `REVIEW_LOG.md`.
4. If criteria met after ≥3 iterations: PASS. Else: Agent A edits the `.md` source → re-runs Pandoc pipeline → loops back to step 2.

## COMPLETE SKILL INTEGRATION
- **Pre-Draft**: `literature-ingestion`, `literature-close-read`, `retraction-watcher`, `literature-review`, `reference-search`, `bgpt-paper-search`, `hypothesis-generation`
- **Drafting**: `abstract-summarizer`, `method-writing`, `discussion-section-architect`, `study-limitations-drafter`, `scientific-critical-thinking`
- **Stats & Viz**: `scientific-visualization`, `statistical-analysis`, `seaborn`, `survival-analysis-km`, `volcano-plot-script`, `visualize-data`
- **Review**: `peer-review`, `reproducibility-check`, `result-figure-consistencycheck`
- **Delivery**: `md-html-docx-generator`, `secure-html-delivery`, `word-read-write`
- **Post-Acceptance**: `lay-summary-gen`, `scientific-slides`