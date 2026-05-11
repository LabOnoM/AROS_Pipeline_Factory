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

## ✅ MANDATORY AUTHORING PROTOCOL (ALL AGENTS)
For every manuscript task, regardless of final output format, proceed as follows:

### Phase 0: Source File Recovery (MANDATORY before any edit)
> **NEVER rely on conversational memory for document content.**
> If any Checkpoint has occurred in the session, or if the document exceeds 500 words,
> you MUST physically read the source file from disk using `view_file` or a shell `cat` command
> before making any edits. Failure to do this is the leading cause of content loss.

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
/tmp/tectonic manuscript.tex -o output/

# Step 5: Markdown → DOCX (for collaborator editing)
pandoc <name>.md -o output/manuscript.docx \
  --resource-path=.:figures

# Step 6: Verify — file size confirms figures are embedded (>>100KB means images present)
ls -lh output/manuscript.pdf output/manuscript.docx
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
- **Dependencies**: Use `numpy<1.25.0`, `scipy>1.10`, `matplotlib<3.8` to prevent binary compatibility issues.
- **Source of Truth**: The `.md` file is ALWAYS the source of truth. The `.tex` file is a derived artifact.

### ⚠️ RETIRED ANTI-PATTERN: `fix_latex.py` Figure Injection (April 2026)
The `fix_latex.py` approach of injecting `\includegraphics` blocks via Python regex into a compiled `.tex` file **MUST NOT be used**. It fails silently because Pandoc maps Markdown `###` level-3 headers to `\subsubsection{}` — not `\section{}`. The regex never matches, no figures are injected, and the PDF compiles cleanly with zero figures. The only diagnostic is PDF file size (~80KB = no figures; >>100KB = figures present).

**The correct approach is always:**
```markdown
![Figure caption goes here.](figures/figN.png){width=100%}
```
Embed this in `manuscript.md` at the prose location where the figure belongs. Pandoc handles the rest.

## AGENT A -- Generator Agent
Agent A is a scientific reasoning agent. Its job is to understand the full experimental picture, make intelligent decisions about data relevance, and produce a manuscript draft with figures.

### Phase A1: Wiki-First File Discovery
1. **Check Project Knowledge**: Read `<PROJECT_ROOT>/.wiki/overview.md`, `.wiki/entities/*.md`, and `00.RawData/INDEX.csv`.
2. **File Sweep**: Agent A runs recursive file discovery to locate raw data (`.pzfx`, `.xlsx`, `.czi`, `.fcs`, etc.) matching the wiki entities.
3. **Reasoning**: Write a brief scientific understanding in `DATA_AUDIT.md`.

### Phase A2 & A3: Data Extraction and Figure Generation
Agent A must adaptively read scientific formats using appropriate Python libraries, compute honest tests, and generate publication-grade figures as PNG to `figures/`.

### Phase A4 & A5: Manuscript Writing and Verification (MARKDOWN-FIRST)
1. Agent A writes the full manuscript in `<name>.md` — complete sections, full citations, exact numbers
2. Agent A runs the Phase 3 Pandoc Pipeline above to produce `.tex`, `.pdf`, `.docx`
3. Agent A verifies PDF page count and that all figures appear embedded correctly
4. Agent A embeds the Agentic State Header in `manuscript.tex` (post-conversion)

## AGENT B -- Reviewer Agent
Agent B acts as a simulated expert peer reviewer, scoring on 12 dimensions:
1. Data Completeness, 2. Figure Quality, 3. Statistical Rigor, 4. Quantitative Specificity,
5. Narrative Coherence, 6. Hypothesis Clarity, 7. Methods Reproducibility, 8. Citation Integrity,
9. Abstract Quality, 10. Novelty and Gap, 11. Technical Soundness, 12. Honest Limitations.

Agent B provides actionable feedback in `REVIEW_LOG.md`.

## STATE TRACKING & MANUSCRIPT RESUMPTION
Agent A MUST embed an **Agentic State Header** at the top of `manuscript.tex` (post-conversion).
See `dual_agent_workflow_details.md` in `~/.gemini/antigravity/knowledge/agentic_manuscript_publishing/artifacts/`.

## THE ITERATION LOOP
(Max Iterations: 5; Pass Threshold: 92/120; Dims 11 & 12 must be 10/10)
1. Agent A forms understanding → writes `.md` → generates figures → runs Pandoc pipeline → sets State Header
2. Agent B scores 12 dimensions → outputs Review Report in `REVIEW_LOG.md`
3. If criteria met: PASS. Else: Agent A edits the `.md` source → re-runs Pandoc pipeline → loops

## COMPLETE SKILL INTEGRATION
- **Pre-Draft**: `literature-review`, `bgpt-paper-search`, `hypothesis-generation`
- **Drafting**: `abstract-summarizer`, `method-writing`, `discussion-section-architect`, `study-limitations-drafter`, `scientific-critical-thinking`
- **Stats & Viz**: `scientific-visualization`, `statistical-analysis`, `seaborn`, `survival-analysis-km`, `volcano-plot-script`
- **Review**: `peer-review`, `reproducibility-check`, `result-figure-consistencycheck`
- **Post-Acceptance**: `lay-summary-gen`, `scientific-slides`