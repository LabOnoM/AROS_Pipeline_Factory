---
name: hypothesis-generation
description: Structured scientific hypothesis formulation from observations; use when you have experimental observations or preliminary data and need testable hypotheses with predictions, mechanisms, and validation experiments. Mandatory AI-generated schematics.
license: MIT
skill-author: AIPOCH
---
# Hypothesis Generation (Scientific)

## Overview

This skill facilitates structured scientific hypothesis formulation from observations or preliminary data. It helps you develop testable hypotheses with clear predictions, underlying mechanisms, and validation experiments. The output is a publication-ready LaTeX report. Every report must include AI-generated schematics.

## When to Use

- When you need to turn observations into **testable, mechanistic hypotheses** and a **validation plan**.
- When you have experimental observations (e.g., an unexpected phenotype, trend, or anomaly) and need 3-5 competing explanations with clear mechanisms.
- When you have preliminary data and must propose **testable predictions** and **decisive experiments** to discriminate between hypotheses.
- When you are preparing a mechanistic study plan (molecular/cellular/system/population) and need a structured framework for causal reasoning.
- When you are doing literature-grounded hypothesis development and want to identify gaps, contradictions, and plausible mechanisms.
- When you need a publication-ready hypothesis report (LaTeX) with a concise main text and a detailed appendix.

## Key Features

- **Scientific workflow**: observation framing → literature search → evidence synthesis → competing hypotheses → quality evaluation → experiments → predictions → structured report.
- **Competing hypotheses (3-5)**: distinct, mechanistic explanations at appropriate biological/physical scales.
- **Quality criteria**: testability, falsifiability, parsimony, explanatory power, scope, consistency, novelty (see `references/hypothesis_quality_criteria.md`).
- **Experiment design patterns**: lab, observational, clinical, computational; controls, confounders, and measurement plans (see `references/experimental_design_patterns.md`).
- **Prediction-first outputs**: quantitative/conditional predictions that differentiate hypotheses and specify falsifiers.
- **Report packaging**: LaTeX template with colored boxes and a strict main-body length budget (see `assets/hypothesis_report_template.tex`, `assets/hypothesis_generation.sty`, `assets/FORMATTING_GUIDE.md`).
- **Mandatory visuals**: every hypothesis report must include **at least 1-2 AI-generated schematics** created via the `scientific-schematics` skill.
- Scope-focused workflow aligned to: Structured scientific hypothesis formulation from observations; use when you have experimental observations or preliminary data and need testable hypotheses with predictions, mechanisms, and validation experiments.
- Documentation-first workflow with no packaged script requirement.
- Reusable packaged asset(s), including `assets/FORMATTING_GUIDE.md`.
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

- **LaTeX engine**: XeLaTeX or LuaLaTeX
- **BibTeX**: for reference compilation
- **Required LaTeX packages** (used by `assets/hypothesis_generation.sty`):
  - `tcolorbox`, `xcolor`, `fontspec`, `fancyhdr`, `titlesec`, `enumitem`, `booktabs`, `natbib`
- **Python (optional, for schematic generation script)**: Python 3.10+ recommended
- **Related skill dependency (mandatory for reports)**: `scientific-schematics` (for 1-2+ diagrams per report)
- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `Third-party packages`: `not explicitly version-pinned in this skill package`. Add pinned versions if this skill needs stricter environment control.

## Example Usage

```text
Skill directory: 20260316/scientific-skills/Protocol Design/hypothesis-generation
No packaged executable script was detected.
Use the documented workflow in SKILL.md together with the references/assets in this folder.
```

Example run plan:
1. Read the skill instructions and collect the required inputs.
2. Follow the documented workflow exactly.
3. Use packaged references/assets from this folder when the task needs templates or rules.
4. Return a structured result tied to the requested deliverable.

### A) Generate required schematics (at least 1-2)

```bash
python scripts/generate_schematic.py "Diagram showing 3 competing mechanistic hypotheses linking Observation X to Outcome Y, with key intermediates and predicted readouts." -o figures/hypothesis_framework.png

python scripts/generate_schematic.py "Experimental design flowchart comparing interventions A/B and controls, with primary/secondary endpoints and decision points." -o figures/experimental_design.png
```

### B) Create a LaTeX report using the provided template

1) Copy the template assets into a working directory:

```bash
mkdir -p hypothesis_report figures
cp assets/hypothesis_report_template.tex hypothesis_report/hypothesis_report.tex
cp assets/hypothesis_generation.sty hypothesis_report/
```

2) Edit `hypothesis_report/hypothesis_report.tex` to include:
- Executive summary
- 3-5 hypothesis boxes (each on a fresh page)
- Predictions and critical comparisons
- Appendix A-D with detailed literature, protocols, and evaluations
- References (BibTeX)

3) Compile:

```bash
cd hypothesis_report
xelatex hypothesis_report.tex
bibtex hypothesis_report
xelatex hypothesis_report.tex
xelatex hypothesis_report.tex
```

### C) Minimal LaTeX snippet demonstrating the required structure

```latex
\documentclass{article}
\usepackage{hypothesis_generation}
\usepackage{natbib}

\begin{document}

\begin{summarybox}
\textbf{Executive Summary.} Observation X shows pattern Y under condition Z. We propose 3 competing mechanisms and outline decisive experiments and predictions.
\end{summarybox}

\newpage
\begin{hypothesisbox1}[Hypothesis 1: Mechanism A]
\textbf{Mechanistic explanation.} Brief causal chain describing how A produces Y under Z.

\textbf{Key supporting evidence.}
\begin{itemize}
  \item Evidence point 1 \citep{author2023}.
  \item Evidence point 2 \citep{author2021}.
\end{itemize}

\textbf{Core assumptions.}
\begin{itemize}
  \item Assumption 1.
\end{itemize}
\end{hypothesisbox1}

\newpage
\begin{hypothesisbox2}[Hypothesis 2: Mechanism B]
% Keep concise; move details to Appendix.
\end{hypothesisbox2}

\begin{predictionbox}
\textbf{Testable predictions.}
\begin{itemize}
  \item If Hypothesis 1 is correct, intervention I increases readout R by ~20-40\% under Z.
  \item If Hypothesis 2 is correct, R does not change, but marker M shifts directionally.
\end{itemize}
\end{predictionbox}

\begin{comparisonbox}
\textbf{Critical comparisons.} Prioritize experiments that maximally separate predictions across hypotheses.
\end{comparisonbox}

\end{document}
```

## Workflow

Follow this systematic process to generate robust scientific hypotheses:

### 1. Understand the Phenomenon

Start by clarifying the observation, question, or phenomenon that requires explanation:

- Identify the core observation or pattern that needs explanation
- Define the scope and boundaries of the phenomenon
- Note any constraints or specific contexts
- Clarify what is already known vs. what is uncertain
- Identify the relevant scientific domain(s)

### 2. Conduct Comprehensive Literature Search

Search existing scientific literature to ground hypotheses in current evidence. Use domain-appropriate sources (e.g., PubMed for biomedical topics; general scholarly search otherwise).

**For biomedical topics:**
- Use WebFetch with PubMed URLs to access relevant literature
- Search for recent reviews, meta-analyses, and primary research
- Look for similar phenomena, related mechanisms, or analogous systems

**For all scientific domains:**
- Use WebSearch to find recent papers, preprints, and reviews
- Search for established theories, mechanisms, or frameworks
- Identify gaps in current understanding

**Search strategy:**
- Begin with broad searches to understand the landscape
- Narrow to specific mechanisms, pathways, or theories
- Look for contradictory findings or unresolved debates
- Consult `references/literature_search_strategies.md` for detailed search techniques

### 3. Synthesize Existing Evidence

Analyze and integrate findings from literature search:

- Summarize current understanding of the phenomenon
- Identify established mechanisms or theories that may apply
- Note conflicting evidence or alternative viewpoints
- Recognize gaps, limitations, or unanswered questions
- Identify analogies from related systems or domains

### 4. Generate Competing Hypotheses

Develop 3-5 distinct hypotheses that could explain the phenomenon. Each hypothesis should:

- Provide a mechanistic explanation (not just description)
- Be distinguishable from other hypotheses
- Draw on evidence from the literature synthesis
- Consider different levels of explanation (molecular, cellular, systemic, population, etc.)

**Strategies for generating hypotheses:**
- Apply known mechanisms from analogous systems
- Consider multiple causative pathways
- Explore different scales of explanation
- Question assumptions in existing explanations
- Combine mechanisms in novel ways

### 5. Evaluate Hypothesis Quality

Assess each hypothesis against established quality criteria from `references/hypothesis_quality_criteria.md`:

**Testability:** Can the hypothesis be empirically tested?
**Falsifiability:** What observations would disprove it?
**Parsimony:** Is it the simplest explanation that fits the evidence?
**Explanatory Power:** How much of the phenomenon does it explain?
**Scope:** What range of observations does it cover?
**Consistency:** Does it align with established principles?
**Novelty:** Does it offer new insights beyond existing explanations?

Explicitly note the strengths and weaknesses of each hypothesis.

### 6. Design Experimental Tests

For each viable hypothesis, propose specific experiments or studies to test it. Consult `references/experimental_design_patterns.md` for common approaches:

**Experimental design elements:**
- What would be measured or observed?
- What comparisons or controls are needed?
- What methods or techniques would be used?
- What sample sizes or statistical approaches are appropriate?
- What are potential confounds and how to address them?

**Consider multiple approaches:**
- Laboratory experiments (in vitro, in vivo, computational)
- Observational studies (cross-sectional, longitudinal, case-control)
- Clinical trials (if applicable)
- Natural experiments or quasi-experimental designs

### 7. Formulate Testable Predictions

For each hypothesis, generate specific, quantitative predictions:

- State what should be observed if the hypothesis is correct
- Specify expected direction and magnitude of effects when possible
- Identify conditions under which predictions should hold
- Distinguish predictions between competing hypotheses
- Note predictions that would falsify the hypothesis

### 8. Present Structured Output

Generate a professional LaTeX document using the template in `assets/hypothesis_report_template.tex`. The report should be well-formatted with colored boxes for visual organization and divided into a concise main text with comprehensive appendices.

**Document Structure:**

**Main Text (Maximum 4 pages):**
1. **Executive Summary** - Brief overview in summary box (0.5-1 page)
2. **Competing Hypotheses** - Each hypothesis in its own colored box with brief mechanistic explanation and key evidence (2-2.5 pages for 3-5 hypotheses)
   - **IMPORTANT:** Use `\newpage` before each hypothesis box to prevent content overflow
   - Each box should be ≤0.6 pages maximum
3. **Testable Predictions** - Key predictions in amber boxes (0.5-1 page)
4. **Critical Comparisons** - Priority comparison boxes (0.5-1 page)

Keep main text highly concise - only the most essential information. All details go to appendices.

**Page Break Strategy:**
- Always use `\newpage` before hypothesis boxes to ensure they start on fresh pages
- This prevents content from overflowing off page boundaries
- LaTeX boxes (tcolorbox) do not automatically break across pages

**Appendices (Comprehensive, Detailed):**
- **Appendix A:** Comprehensive literature review with extensive citations
- **Appendix B:** Detailed experimental designs with full protocols
- **Appendix C:** Quality assessment tables and detailed evaluations
- **Appendix D:** Supplementary evidence and analogous systems

**Colored Box Usage:**

Use the custom box environments from `hypothesis_generation.sty`:

- `hypothesisbox1` through `hypothesisbox5` - For each competing hypothesis (blue, green, purple, teal, orange)
- `predictionbox` - For testable predictions (amber)
- `comparisonbox` - For critical comparisons (steel gray)
- `evidencebox` - For supporting evidence highlights (light blue)
- `summarybox` - For executive summary (blue)

**Each hypothesis box should contain (keep concise for 4-page limit):**
- **Mechanistic Explanation:** 1-2 brief paragraphs (6-10 sentences max) explaining HOW and WHY
- **Key Supporting Evidence:** 2-3 bullet points with citations (most important evidence only)
- **Core Assumptions:** 1-2 critical assumptions

All detailed explanations, additional evidence, and comprehensive discussions belong in the appendices.

**Critical Overflow Prevention:**
- Insert `\newpage` before each hypothesis box to start it on a fresh page
- Keep each complete hypothesis box to ≤0.6 pages (approximately 15-20 lines of content)
- If content exceeds this, move additional details to Appendix A
- Never let boxes overflow off page boundaries - this creates unreadable PDFs

**Citation Requirements:**

Aim for extensive citation to support all claims:
- **Main text:** 10-15 key citations for most important evidence only (keep concise for 4-page limit)
- **Appendix A:** 40-70+ comprehensive citations covering all relevant literature
- **Total target:** 50+ references in bibliography

Main text citations should be selective - cite only the most critical papers. All comprehensive citation and detailed literature discussion belongs in the appendices. Use `\citep{author2023}` for parenthetical citations.

**LaTeX Compilation:**

The template requires XeLaTeX or LuaLaTeX for proper rendering:

```bash
xelatex hypothesis_report.tex
bibtex hypothesis_report
xelatex hypothesis_report.tex
xelatex hypothesis_report.tex
```

**Required packages:** The `hypothesis_generation.sty` style package must be in the same directory or LaTeX path. It requires: tcolorbox, xcolor, fontspec, fancyhdr, titlesec, enumitem, booktabs, natbib.

**Page Overflow Prevention:**

To prevent content from overflowing on pages, follow these critical guidelines:

1. **Monitor Box Content Length:** Each hypothesis box should fit comfortably on a single page. If content exceeds ~0.7 pages, it will likely overflow.

2. **Use Strategic Page Breaks:** Insert `\newpage` before boxes that contain substantial content:
   ```latex
   \newpage
   \begin{hypothesisbox1}[Hypothesis 1: Title]
   % Long content here
   \end{hypothesisbox1}
   ```

3. **Keep Main Text Boxes Concise:** For the 4-page main text limit:
   - Each hypothesis box: Maximum 0.5-0.6 pages
   - Mechanistic explanation: 1-2 brief paragraphs only (6-10 sentences max)
   - Key evidence: 2-3 bullet points only
   - Core assumptions: 1-2 items only
   - If content is longer, move details to appendices

4. **Break Long Content:** If a hypothesis requires extensive explanation, split across main text and appendix:
   - Main text box: Brief mechanistic overview + 2-3 key evidence points
   - Appendix A: Detailed mechanism explanation, comprehensive evidence, extended discussion

5. **Test Page Boundaries:** Before each new box, consider if remaining page space is sufficient. If less than 0.6 pages remain, use `\newpage` to start the box on a fresh page.

6. **Appendix Page Management:** In appendices, use `\newpage` between major sections to avoid overflow in detailed content areas.

**Quick Reference:** See `assets/FORMATTING_GUIDE.md` for detailed examples of all box types, color schemes, and common formatting patterns.

## Implementation Details

### 5.1 End-to-end workflow (recommended)

1. **Define the phenomenon**
   - State the observation/pattern to explain, scope, constraints, and what is known vs unknown.
2. **Literature search**
   - Use domain-appropriate sources (e.g., PubMed for biomedical topics; general scholarly search otherwise).
   - Apply strategies in `references/literature_search_strategies.md`.
3. **Evidence synthesis**
   - Summarize consensus mechanisms, contradictions, and gaps; extract candidate causal links.
4. **Generate 3-5 competing hypotheses**
   - Each must be mechanistic (how/why), distinct, and grounded in evidence or plausible analogies.
5. **Evaluate hypothesis quality**
   - Use criteria in `references/hypothesis_quality_criteria.md`:
     - Testability, falsifiability, parsimony, explanatory power, scope, consistency, novelty.
   - Record strengths/weaknesses explicitly.
6. **Design experimental tests**
   - Use patterns in `references/experimental_design_patterns.md`.
   - Specify: measurements, controls, comparisons, confounders, sample size/statistics (as appropriate).
7. **Formulate testable predictions**
   - Provide discriminative predictions (direction, magnitude when possible), boundary conditions, and falsifiers.
8. **Produce structured report**
   - Use `assets/hypothesis_report_template.tex` and `assets/hypothesis_generation.sty`.
   - Include **1-2+ schematics** generated via `scientific-schematics`.

### 5.2 Mandatory schematic requirement

- Every hypothesis generation report must include **at least 1-2 diagrams** (framework, mechanism, experimental flowchart, decision tree, causal graph).
- Reports without visuals are considered incomplete.
- Recommended placement: one schematic in the main body (overview), additional schematics in the appendix (mechanisms/experimental details).

### 5.3 LaTeX formatting constraints (overflow prevention)

- The main body should be **≤ 4 pages** (template-guided).
- Insert `\newpage` **before each hypothesis box**; `tcolorbox` environments do not reliably break across pages.
- Keep each hypothesis box to roughly **0.5-0.6 page**:
  - Mechanism: 1-2 short paragraphs (≈ 6-10 sentences)
  - Evidence: 2-3 bullets with key citations
  - Assumptions: 1-2 bullets
- Move extended rationale, extra citations, and protocol details to the appendix.

### 5.4 Citation targets

- Main body: ~10-15 carefully selected citations (only the most decisive evidence).
- Appendix A: ~40-70+ citations for comprehensive coverage.
- Total references goal: **50+** entries when the topic warrants it.
- Use `\citep{author2023}` for parenthetical citations (per template conventions).

### 5.5 Included repository resources

- `references/hypothesis_quality_criteria.md`: evaluation rubric for hypothesis strength.
- `references/experimental_design_patterns.md`: reusable experimental design templates.
- `references/literature_search_strategies.md`: search tactics for PubMed and general scientific sources.
- `assets/hypothesis_generation.sty`: colored box environments and report styling.
- `assets/hypothesis_report_template.tex`: full report template (main body + appendix).
- `assets/FORMATTING_GUIDE.md`: examples and troubleshooting for box usage and layout.

## Quality Standards

Ensure all generated hypotheses meet these standards:

- **Evidence-based:** Grounded in existing literature with citations
- **Testable:** Include specific, measurable predictions
- **Mechanistic:** Explain how/why, not just what
- **Comprehensive:** Consider alternative explanations
- **Rigorous:** Include experimental designs to test predictions

## When Not to Use

- Do not use this skill when the required source data, identifiers, files, or credentials are missing.
- Do not use this skill when the user asks for fabricated results, unsupported claims, or out-of-scope conclusions.
- Do not use this skill when a simpler direct answer is more appropriate than the documented workflow.

## Required Inputs

- A clearly specified task goal aligned with the documented scope.
- All required files, identifiers, parameters, or environment variables before execution.
- Any domain constraints, formatting requirements, and expected output destination if applicable.

## Recommended Workflow

1. Validate the request against the skill boundary and confirm all required inputs are present.
2. Select the documented execution path and prefer the simplest supported command or procedure.
3. Produce the expected output using the documented file format, schema, or narrative structure.
4. Run a final validation pass for completeness, consistency, and safety before returning the result.

## Output Contract

- Return a structured deliverable that is directly usable without reformatting.
- If a file is produced, prefer a deterministic output name such as `hypothesis_generation_result.md` unless the skill documentation defines a better convention.
- Include a short validation summary describing what was checked, what assumptions were made, and any remaining limitations.

## Validation and Safety Rules

- Validate required inputs before execution and stop early when mandatory fields or files are missing.
- Do not fabricate measurements, references, findings, or conclusions that are not supported by the provided source material.
- Emit a clear warning when credentials, privacy constraints, safety boundaries, or unsupported requests affect the result.
- Keep the output safe, reproducible, and within the documented scope at all times.

## Failure Handling

- If validation fails, explain the exact missing field, file, or parameter and show the minimum fix required.
- If an external dependency or script fails, surface the command path, likely cause, and the next recovery step.
- If partial output is returned, label it clearly and identify which checks could not be completed.

## Quick Validation

Run this minimal verification path before full execution when possible:

```text
No local script validation step is required for this skill.
```

Expected output format:

```text
Result file: hypothesis_generation_result.md
Validation summary: PASS/FAIL with brief notes
Assumptions: explicit list if any
```

## Resources

### references/

- `hypothesis_quality_criteria.md` - Framework for evaluating hypothesis quality (testability, falsifiability, parsimony, explanatory power, scope, consistency)
- `experimental_design_patterns.md` - Common experimental approaches across domains (RCTs, observational studies, lab experiments, computational models)
- `literature_search_strategies.md` - Effective search techniques for PubMed and general scientific sources

### assets/

- `hypothesis_generation.sty` - LaTeX style package providing colored boxes, professional formatting, and custom environments for hypothesis reports
- `hypothesis_report_template.tex` - Complete LaTeX template with main text structure and comprehensive appendix sections
- `FORMATTING_GUIDE.md` - Quick reference guide with examples of all box types, color schemes, citation practices, and troubleshooting tips

### Related Skills

When preparing hypothesis-driven research for publication, consult the **venue-templates** skill for writing style guidance:
- `venue_writing_styles.md` - Master guide comparing styles across venues
- Venue-specific guides for Nature/Science, Cell Press, medical journals, and ML/CS conferences
- `reviewer_expectations.md` - What reviewers look for when evaluating research hypotheses