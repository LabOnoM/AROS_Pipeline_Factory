---
cpcp_asset: true
canonical_location: "01.Shared_Assets/KIs/markdown_first_manuscript_policy"
consumers:
  - Grant_Write_Pipeline
  - Manuscript_Write_Pipeline
last_cpcp_review: "2026-05-11"
---
# Markdown-First Manuscript Policy

**Status:** ACTIVE HARD RULE  
**Scope:** All AI agents in all sessions  
**Origin:** Documented failure case, April 2026

---

## The Rule (One Sentence)

> **AI agents MUST write all scientific manuscript text in Markdown (`.md`) first and use Pandoc to convert to `.tex`, `.docx`, and `.pdf`. Direct LaTeX authoring of substantive text is PROHIBITED.**

---

## Documented Root Cause (April 2026)

During the *Spatial Transcriptomics Probe Portability* manuscript project (conversation `e52ba847`), the following catastrophic failure occurred:

| Metric | Original `.md` draft | Agent's direct `.tex` rewrite |
|--------|---------------------|-------------------------------|
| Lines | 964 | 93 |
| Word count | ~5,800 | ~600 |
| Citations | 40 | 0 |
| Sections | 9 full sections | 6 skeletal stubs |
| Quality | Publication-ready | First-year student draft |
| **Loss** | — | **93% content destroyed** |

### Why this happens (the "Syntax-Cognitive-Load" mechanism)

When an LLM generates text in Markdown, syntactic overhead is near-zero. The model allocates ~100% of its attention budget to **semantic content generation**: pulling precise scientific facts, constructing nuanced arguments, synthesizing citations.

When an LLM generates text in LaTeX, syntactic overhead is very high. Every sentence requires the model to simultaneously:
- Track open/close of `\begin{}`/`\end{}` environments
- Escape special characters (`_`, `%`, `&`, `~`, `^`, `$`)
- Manage figure float environments, cross-references, `\label`/`\ref` pairs
- Ensure preamble package completeness

To guarantee a **compilable document**, the model aggressively summarizes scientific content — trading depth for structural correctness. This is an emergent LLM behavior, not a configuration error.

---

## The Pandoc-First Execution Protocol

---

### ⚠️ SECOND DOCUMENTED FAILURE MODE: Figure Injection via `fix_latex.py` (April 2026)

A second critical failure was identified in April 2026 in the same Spatial Transcriptomics project. The `fix_latex.py` script attempted to inject `\includegraphics` blocks into the Pandoc-generated `manuscript.tex` using Python `str.replace()` targeting exact LaTeX section header strings:

```python
# fix_latex.py — BROKEN APPROACH (DO NOT USE)
if 'section{1. Introduction}' in text:
    target = '\\section{1. Introduction}'
```

**This silent failure mechanism:** Pandoc maps Markdown `###` headers (level 3) to `\subsubsection{}` — NOT `\section{}`. The regex never matched the target strings, so no figures were injected. The PDF compiled cleanly (no error) but contained **zero figures**. The agent and user would only discover this by carefully reading the PDF, not from any compilation error.

**File size is a reliable diagnostic:** A PDF with 0 embedded images is ~80–90KB. A PDF with 2 embedded PNGs is ~500KB+. Always check `ls -lh output/manuscript.pdf`.

---

### ✅ CORRECT FIGURE EMBEDDING: Native Markdown Image Syntax

**NEVER use `fix_latex.py` or any post-conversion regex injection for figures.**

Embed all figures **natively in `manuscript.md`** using standard Markdown image syntax at the exact position in the text where the figure should appear:

```markdown
![Figure caption text here describing what the figure shows.](figures/figN.png){width=100%}
```

Pandoc converts this deterministically and correctly into LaTeX `\includegraphics` + `\figure` environments, regardless of section header level mapping. The `{width=100%}` attribute is passed through to LaTeX as `\textwidth`.

**The updated, correct compilation pipeline (no `fix_latex.py`):**

```bash
# Step 1: Embed figures natively in manuscript.md (see above)

# Step 2: Generate figure PNG files
python3 figures/generate_figures.py   # → figures/fig1_xxx.png, figures/graphical_abstract.png

# Step 3: Convert & Compile (no fix_latex.py step)
pandoc manuscript.md -o manuscript.tex --standalone --resource-path=.:figures
/tmp/tectonic manuscript.tex -o output/
pandoc manuscript.md -o output/manuscript.docx --resource-path=.:figures

# Step 4: Verify file sizes (figures embedded = file size >> 100KB for PDF)
ls -lh output/
```

### Step 4: Permitted Post-Conversion LaTeX Edits (ONLY via multi_replace_file_content)
After Pandoc generates `manuscript.tex`, **only** the following surgical edits are permitted directly in the `.tex` file:
- Figure float specifier (e.g., `[H]` → `[htbp]`)  
- Adding `\usepackage{}` declarations not auto-included  
- Fixing Unicode character rendering (e.g., `μ` → `$\mu$`) — **fix in `.md` first when possible**  
- Adding the Agentic State Header block  
- Journal-specific `.cls` class changes  

**ANY change to body text MUST be made in `manuscript.md` and the Pandoc pipeline re-run.**

### Unicode Character Handling

Unicode characters (e.g., `µ` U+00B5 or `μ` U+03BC for micro) are NOT supported by the default `lmroman` font in Tectonic. Two fix strategies:

1. **(Preferred — fix in source)**: Replace in `manuscript.md` using `sed`:
   ```bash
   sed -i 's/µ/$\\mu$/g; s/μ/$\\mu$/g' manuscript.md
   ```
   Then re-run the full Pandoc pipeline.

2. **(Permitted fallback — fix in `.tex`)**: Use `multi_replace_file_content` to surgically replace only the affected line(s) in `manuscript.tex`.

---

## Source of Truth Hierarchy

```
manuscript.md          ← THE source of truth — always edit here
    │
    ▼ pandoc + fix_latex.py
manuscript.tex         ← Derived artifact — surgical edits only
    │
    ▼ tectonic / pandoc
output/
  ├── manuscript.pdf   ← Final compiled output
  └── manuscript.docx  ← Final compiled output
```

---

## Source File Recovery Before Any Edit

> **BEFORE editing any manuscript, if any conversational Checkpoint has occurred:**
> 1. Run `cat manuscript.md | wc -l` to verify the source file is intact on disk
> 2. Run `view_file` on `manuscript.md` to load its content into active context
> 3. ONLY THEN proceed with edits
> 
> Checkpoints aggressively summarize document bodies in conversational memory. The file on disk is ALWAYS more complete than what you "remember."

---

## Checklist (Pre-Manuscript-Write)

- [ ] I have read the current `manuscript.md` from disk (not from memory)
- [ ] I will write all new content in `manuscript.md` only
- [ ] I have generated all figures as PNG files to `figures/`
- [ ] I will run the Pandoc pipeline for all format conversions
- [ ] I will NOT use `write_to_file` with `Overwrite=True` on `manuscript.tex`
- [ ] Any LaTeX changes I make will be surgical `multi_replace_file_content` edits only

---

*This KI was created to permanently record the root-cause of the April 2026 manuscript quality failure and prevent its recurrence in all future agents and sessions.*
