# Agentic Scientific Manuscript Writing: Best Practices

This document summarizes the core experiences, pitfalls, and best practices derived from drafting, revising, and finalizing the `ISS Microgravity CARE/CellPose 3D` scientific manuscript intended for high-impact journals (e.g., *Cell*). 

## 1. Navigating Peer Review with AI Evaluators (e.g., Stanford Agentic Reviewer)
Responding to AI-agent reviewers (such as those from `paperreview.ai`) demands a radically honest, precise, and highly structured approach.
- **Do not invent data:** When reviewers point out missing functional validations (e.g., lack of Seahorse respiratory assays or protein-level LC3/Parkin expression to definitively prove mitophagy), explicitly acknowledge this in a new `Limitations of the Study` subsection. Frame these as critical next steps rather than attempting to over-interpret existing morphological data to prove functional states.
- **Defend Analytical Heuristics Clearly:** If criticized for AI artifacts (e.g., "CellPose 2D-to-3D stitching may artificially connect discrete mitochondria"), explicitly report the structural mitigations used (e.g., `stitch_threshold=0.5` IoU cutoff, `min_size` filtering logic) and explain the biological rationale (e.g., "temporary membrane fissions vs. genuine organelle separation").
- **Statistical Rigor is Paramount:** AI reviewers will brutally flag vague statistical reporting. Always provide exact model specifications. For LMMs (Linear Mixed-Effects Models), document the formula (e.g., `Value ~ Gravity * Time + (1|Sample ID)`), state the optimization method (REML), define interaction terms, and formally report multiple-comparison corrections (like the Bonferroni adjusted alpha).

## 2. Terminology and Experimental Fidelity
- **Simulation vs. True Environments:** It is incredibly easy to accidentally draft text implying "simulated" gravity mapping if relying on ungrounded LLM inference. In orbital research, explicitly define the hardware. Differentiate between `true microgravity (Stationary inside Kubik)` and the `1G on-board centrifuge control` to rule out launch/radiation/fluidic confounds.
- **Tool-Specific Ontology:** Use the exact parameter names from the utilized software plugins. Instead of generic terms like "length" or "shape", adhere exactly to the defined output terminology of the analytical pipelines used (e.g., "Branches", "Junctions", "Mean Branch Diameter", and "Aspect Ratio" as rigidly defined by the *Mitochondria-Analyzer* Fiji plugin).

## 3. Methodological Transparency & AI Pipeline Validation
High-impact manuscripts utilizing deep learning models must thoroughly validate their architectures in the supplementary or main methods:
- **Cite the Algorithms Properly:** Beyond just naming tools, provide accurate citations for the underlying fundamental architectures (e.g., Weigert et al. for CARE, Stringer et al. for CellPose, Chaudhry et al. for Mitochondria-Analyzer).
- **Compile Standalone Performance Reports:** Journals appreciate interactive, static documentation validating AI pipelines. For instance, creating standalone HTML dashboards that compute global `PSNR/SSIM/MAE` (for restoration) and `IoU/Precision/Recall` (for segmentation), coupled with interactive Z-plane base64 sliders, provides robust, undeniable proof of network efficacy that highly exceeds standard static PDF supplemental figures. 
- **Explain Discrepancies:** If a model doesn't use deconvolution but predicts morphological widths, note that optical broadening remains a factor. Acknowledge this limitation honestly.

## 4. LaTeX and Compilation Resiliency
- **Continuous Compilation Testing:** Never commit large chunks of TeX without checking for compilation. Errors like `overfull \hbox`, missing packages (e.g., required `\usepackage{amsmath}` for equations), or unescaped characters (like underscores `_` in gene names or filenames) will instantly halt the workflow.
- **Reference Integrity:** Ensure the `.bib` file accurately matches citation keys. Always check that newly added methodological papers are properly compiled into the LaTeX bibliography.
- **Formatting Structure:** Avoid placing the Graphical Abstract as Figure 1. It belongs in its own dedicated preamble/graphical abstract summary section. Ensure authors, affiliations, and headers strictly follow the journal's `.cls` requirements (e.g., `cell-template.cls`).

## 5. ⚠️ MARKDOWN-FIRST AUTHORING — HARD RULE (Added April 2026)

### Root Cause Documentation
A critical quality failure was identified and documented in April 2026 during the Spatial Transcriptomics Probe Portability manuscript project. When an AI agent was instructed to rewrite a 964-line, 5,800-word, 40-citation literature review directly in LaTeX, it produced a 93-line hollow structural outline — losing over 93% of the scientific content. Root cause: the model's attention mechanism shifted from semantic content to syntactic LaTeX closure, causing catastrophic content compression.

### The Mandatory Rule
**ALL scientific manuscript text MUST be written in Markdown (`.md`) first. AI agents are PROHIBITED from writing substantive manuscript sections directly in `.tex`.**

Rationale:
- Markdown syntax overhead is negligible → 100% of model capacity → scientific content
- LaTeX syntax overhead is very high → model compresses science to guarantee compilation
- Pandoc converts Markdown → LaTeX deterministically with zero content loss

### Mandatory Pandoc Conversion Pipeline
```bash
# Step 1: Embed figures natively in manuscript.md using standard Markdown:
# ![Figure caption](figures/figN.png){width=100%}
# Do NOT use fix_latex.py — see Section 6 below.

# Step 2: Generate figure PNG files
python3 figures/generate_figures.py

# Step 3: Convert & compile (no post-processing needed)
pandoc manuscript.md -o manuscript.tex --standalone --resource-path=.:figures
/tmp/tectonic manuscript.tex -o output/   # Compile PDF (tectonic = no TeX Live needed)
pandoc manuscript.md -o output/manuscript.docx --resource-path=.:figures

# Step 4: Verify — a PDF with embedded figures will be >>100KB
ls -lh output/
```

### Source of Truth Hierarchy
1. **`manuscript.md`** — THE source of truth. Always edit this.
2. **`manuscript.tex`** — Derived artifact from Pandoc. Limited surgical edits only (figure float settings, usepackage, Unicode fixes).
3. **`output/manuscript.pdf`** and **`output/manuscript.docx`** — Final compiled outputs.

### Source File Recovery Protocol (MANDATORY)
Before ANY edit to a manuscript, if a conversational Checkpoint has occurred or the session is long:
> STOP. Read the `.md` source file from disk using `view_file` or `cat` before editing.
> NEVER assume the content is in your active context memory. Checkpoints compress document bodies.

## 6. ⚠️ FIGURE EMBEDDING — HARD RULE (Added April 2026)

### Root Cause Documentation
A second critical failure was identified in the same April 2026 session. A `fix_latex.py` script attempted to inject `\includegraphics` blocks into the Pandoc-generated `.tex` by searching for exact section header strings like `'section{1. Introduction}'`. This approach **fails silently**: Pandoc maps Markdown `###` (level 3) headers to `\subsubsection{}` — not `\section{}` — so the regex never matched. The PDF compiled without errors but contained zero embedded figures. The only diagnostic clue was PDF file size (~83KB with no images vs ~514KB with two PNGs).

### The Mandatory Rule
**NEVER use post-conversion regex injection (`fix_latex.py` or equivalent) to embed figures. All figures MUST be embedded natively in `manuscript.md` using standard Markdown image syntax.**

```markdown
![Caption describing this figure in full.](figures/figN.png){width=100%}
```

Place this image tag in the `.md` file at the exact prose location where the figure should appear. Pandoc converts this deterministically to a LaTeX `\figure` environment regardless of surrounding section hierarchy.

### Mandatory Figure Embedding Checklist
- [ ] Every figure is referenced by `![caption](figures/filename.png)` in `manuscript.md`
- [ ] All PNG files exist in the `figures/` directory before running Pandoc
- [ ] After compilation, `ls -lh output/manuscript.pdf` shows size >>100KB (confirms images embedded)
- [ ] Open and visually verify the PDF shows figures at correct positions

## Summary Workflow Rule for Future Agents
When tasked with revising a manuscript based on reviewer feedback:
1. **Recover Source**: Read `manuscript.md` from disk — NEVER rely on conversational memory.
2. **Digest** all criticisms and group them by Biological, Computational, Statistical, Formatting.
3. **Review Source Data:** Check exact statistical scripts or metadata to report correct equations.
4. **Embed figures natively** in the `.md` source using `![caption](figures/figN.png){width=100%}`.
5. **Revise the `.md` file** (NOT the `.tex` file) — edit `manuscript.md` directly.
6. **Re-run the Pandoc Pipeline**: `pandoc manuscript.md -o manuscript.tex ... && /tmp/tectonic manuscript.tex -o output/ && pandoc manuscript.md -o output/manuscript.docx`
7. **Validate**: Check `ls -lh output/manuscript.pdf` for file size, open PDF to visually verify figures appear.
