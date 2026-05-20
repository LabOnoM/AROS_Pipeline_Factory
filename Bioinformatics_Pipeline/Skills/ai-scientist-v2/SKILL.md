---
name: ai-scientist-v2
description: End-to-end automated scientific discovery using agentic tree search (AI-Scientist-v2 by SakanaAI). Use when the user wants to automate the full research lifecycle — idea generation with novelty checking, staged ML experiments via Best-First Tree Search (BFTS), LLM-driven plot aggregation, LaTeX paper writeup with citation rounds, automated peer review (LLM and VLM-based figure review), or when they mention "AI Scientist", "automated scientific discovery", "tree search experiments", "agentic research", "VLM figure review", or want to structure ML experiments in stages (preliminary → tuning → creative → ablation).
---

# AI-Scientist-v2: Automated Scientific Discovery

> Source: [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)
> Paper: [arXiv:2504.08066](https://arxiv.org/abs/2504.08066)

## Overview

AI-Scientist-v2 is a fully autonomous scientific research system that generates hypotheses, runs experiments via agentic tree search, analyzes data, writes LaTeX manuscripts, and performs automated peer review. This skill captures its **methodology and prompting patterns** so the agent can apply them in any research context.

## Core Capabilities

### 1. Research Ideation with Novelty Validation

Generate structured research ideas with automatic novelty checking via Semantic Scholar.

**Idea JSON Schema:**
```json
{
  "Name": "short_descriptor_no_spaces",
  "Title": "Catchy and informative title",
  "Short Hypothesis": "Concise statement of the main hypothesis",
  "Related Work": "Discussion of relevant work and how this differs",
  "Abstract": "~250 word conference-style abstract",
  "Experiments": "List of specific experiments with evaluation metrics",
  "Risk Factors and Limitations": "Potential risks and limitations"
}
```

**Ideation Loop:**
1. Generate initial idea based on a topic description
2. Search Semantic Scholar to check novelty and find related work
3. Reflect and refine (up to N rounds), incorporating search results
4. Finalize with structured JSON output

**System Prompt Pattern:**
```
You are an experienced AI researcher who aims to propose high-impact research 
ideas resembling exciting grant proposals. Be very creative and think out of 
the box. Each proposal should stem from a simple and elegant question, 
observation, or hypothesis. Ensure proposals don't require resources beyond 
what an academic lab could afford.
```

**Key Principle:** Always perform at least one literature search before finalizing an idea to ensure it is well-informed by existing research.

---

### 2. Best-First Tree Search (BFTS) Experimentation

Run ML experiments through a 4-stage progressive pipeline with parallel exploration.

**Stage Progression:**

| Stage | Name | Goals |
|-------|------|-------|
| 1 | `preliminary` | Get basic working implementation; use a simple dataset; aim for functional correctness |
| 2 | `baseline_tuning` | Tune hyperparameters (LR, epochs, batch size); DO NOT change architecture; introduce 2 more datasets |
| 3 | `creative_research` | Explore novel improvements; reveal new insights; be creative; use 3 total datasets |
| 4 | `ablation_studies` | Systematic component analysis; reveal contribution of each part; same datasets as stage 3 |

**Tree Search Parameters:**
- `num_workers`: Number of parallel exploration paths (e.g., 3)
- `steps`: Maximum nodes to explore (e.g., 21)
- `num_drafts`: Number of independent root nodes (initial trees)
- `max_debug_depth`: Max debug attempts before abandoning a failing node
- `debug_prob`: Probability of attempting to debug vs. starting fresh

**Agent Manager Pattern:**
- Each stage has a journal tracking experiment history
- Log summarization compresses experiment history for LLM context
- Stage transitions happen when the current stage's goals are met
- Each node in the tree represents an experiment variant

**When to use this pattern:**
- Running systematic ML experiments that need parallel exploration
- When you want to try multiple approaches and keep the best
- For research that benefits from staged complexity (start simple, then get creative)

---

### 3. LLM-Driven Plot Aggregation

Automatically synthesize publication-quality figures from experiment result summaries.

**Aggregation Pattern:**
1. Load all experiment summaries (baseline, research, ablation) as JSON
2. Prompt LLM to design a comprehensive plot aggregator script
3. The script must be self-contained, loading data from `.npy` files or JSON summaries
4. Output goes to `figures/` directory only
5. Up to 3 subplots per figure using `plt.subplots(1, 3)`
6. Use larger-than-default font sizes for paper readability
7. Each figure must be unique (no duplicates)
8. Iteratively debug the aggregator script if it fails

**Key rules:**
- Do NOT hallucinate data — only use data from actual experiment outputs
- Combine related plots into subfigures
- Ensure every plot reflects major findings from the experiment data

---

### 4. LaTeX Paper Writeup with Citation Rounds

Write full conference papers with multi-round citation enhancement.

**Section-by-Section Tips:**
- **Title**: Catchy, informative, under 2 lines
- **Abstract**: TL;DR of the paper; one continuous paragraph; what and why
- **Introduction**: Longer abstract; context and relevance; summarize contributions
- **Related Work**: Academic siblings; compare and contrast approaches
- **Background**: Foundational concepts needed to understand the method
- **Method**: What you propose and why; how it tests hypotheses
- **Experimental Setup**: Data, environment, baselines (omit hardware unless mentioned)
- **Experiments**: Results truthfully per data; include all relevant plots/tables
- **Conclusion**: Summary; strengths; future directions; be honest about negatives
- **Appendix**: Supplementary material

**Citation Round Pattern:**
1. Use a smaller model (e.g., GPT-4o) for citation search (cost-efficient)
2. Search Semantic Scholar for relevant papers
3. Add BibTeX entries to `references.bib`
4. Run up to 20 citation rounds to build comprehensive references
5. Use a larger model (e.g., o1) for the final writeup

**LaTeX Best Practices:**
- Keep `\graphicspath` directive intact
- Escape special characters: `& % $ # _ { } ~ ^ \`
- Avoid duplicate figure labels
- Ensure proper table/figure closure
- Do not hallucinate citations or experimental results

---

### 5. Automated Peer Review

#### LLM-Based Review (NeurIPS Format)

Perform structured peer review using a conference review form.

**9-Dimension Scoring:**

| Dimension | Scale | Description |
|-----------|-------|-------------|
| Summary | text | Factual summary of contributions |
| Strengths & Weaknesses | text | Originality, Quality, Clarity, Significance |
| Questions | text | Items where author response could change opinion |
| Limitations | text | Adequacy of limitations discussion |
| Ethics | flag | Flag for ethics review if needed |
| Soundness | 1-4 | Technical claims and methodology |
| Presentation | 1-4 | Writing quality and contextualization |
| Contribution | 1-4 | Overall research contribution quality |
| Overall | 1-10 | Holistic paper score (10=Award, 1=Very Strong Reject) |
| Confidence | 1-5 | Reviewer's self-assessed expertise |

**Ensemble Meta-Review Pattern:**
1. Generate N independent reviews (e.g., 3) at temperature 0.75
2. Parse each into structured JSON
3. Aggregate scores (clip to valid ranges)
4. Generate a meta-review synthesizing all perspectives

#### VLM-Based Figure Review

Use vision-language models to review paper figures.

**Figure Review JSON Schema:**
```json
{
  "Img_description": "Detailed scientific description of figure contents",
  "Img_review": "Analysis with suggestions for improvement",
  "Caption_review": "Assessment of caption-figure alignment",
  "Figrefs_review": "Whether main text adequately references the figure",
  "Overall_comments": "Whether figure adds value or should move to appendix",
  "Containing_sub_figures": "Sub-figure analysis: density, alignment, combination suggestions",
  "Informative_review": "Does the figure effectively communicate differences/patterns?"
}
```

**VLM Review Checks:**
- Are axis labels clear and readable?
- Does the figure match what the caption claims?
- Are bars/lines distinguishable (not too similar heights)?
- Should related plots be combined?
- Is the figure informative enough for the main text?

---

### 6. Semantic Scholar Integration

Use Semantic Scholar for both ideation and citation phases.

**During Ideation:**
- Search for related work to validate novelty
- Check if similar ideas have been published
- Find relevant baselines and methods

**During Writeup:**
- Gather citations for related work section
- Find papers that support claims
- Build comprehensive reference list

**API Configuration:**
- Optional API key via `S2_API_KEY` environment variable
- Works without key but may hit rate limits
- Can skip citation phase if API is unavailable

## Reference Files

- `references/experiment_stages.md` — Detailed stage progression and goals
- `references/review_forms.md` — Complete NeurIPS review form and VLM review schema
- `references/ideation_schema.md` — Research idea JSON format and ideation loop details

## Related Skills

- `hypothesis-generation` — For manual hypothesis formulation (complementary)
- `scientific-writing` — For manuscript-level writing guidance
- `peer-review` — For structured review writing
- `scientific-visualization` — For figure creation guidance
- `agentic-data-scientist` — For multi-agent data science workflows
- `denario` — For automated research pipelines
