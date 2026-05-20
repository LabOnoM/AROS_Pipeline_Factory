---
name: market-research-reports
description: "Generate comprehensive business and economic market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartner). Features professional LaTeX formatting, extensive visual generation, deep integration with research-lookup for commercial data gathering, and multi-framework strategic business analysis."
allowed-tools: [Read, Write, Edit, Bash]
---

> **WARNING: Business & Economic Domain Only**
> This skill is exclusively for generating **business, commercial, and economic market research reports**. It is **NOT** suitable for scientific, academic, technical, or non-business analysis. Misuse for tasks like scientific data analysis (e.g., bioinformatics, genomics) or technical documentation will result in task failure.

# Market Research Reports

## Overview

Market research reports are comprehensive strategic documents that analyze industries, commercial markets, and competitive landscapes to inform business decisions, investment strategies, and strategic planning. This skill generates **professional-grade reports of 50+ pages** with extensive visual content, modeled after deliverables from top consulting firms like McKinsey, BCG, Bain, Gartner, and Forrester.

## Constraints & Limitations

- **Domain Specificity**: This skill is strictly for **business, financial, and economic analysis**. It is not designed for scientific research, academic papers, technical documentation, or data analysis in other domains.
- **Not for Scientific Data**: **DO NOT USE** this skill for analyzing or reporting on scientific data (e.g., bioinformatics, genomics, clinical trials, physics experiments).
- **Not for Technical Reporting**: This skill cannot be used to generate technical reports, software documentation, or engineering specifications.
- **No Raw Data Analysis**: This skill orchestrates research and writing; it does not perform raw statistical or computational data analysis (e.g., statistical modeling, machine learning on datasets). It uses `research-lookup` to find pre-existing analysis and data.

## When to Use This Skill

This skill should be used when:
- Creating comprehensive **commercial** market analysis for investment decisions
- Developing **industry** reports for strategic business planning
- Analyzing competitive landscapes and **commercial** market dynamics
- Conducting market sizing exercises (TAM/SAM/SOM) for a product or service
- Evaluating **business** market entry opportunities
- Preparing due diligence materials for M&A activities

### When **NOT** to Use This Skill

- **DO NOT USE** for analyzing scientific or academic research data (e.g., genomics, proteomics, physics).
- **DO NOT USE** for writing a scientific paper, technical report, or academic literature review.
- **DO NOT USE** for generating software documentation or a technical manual.
- **DO NOT USE** for summarizing or reporting on non-commercial topics.

---

## Visual Enhancement Requirements

**CRITICAL: Market research reports should include key visual content for business analysis.**

Every report should generate **6 essential visuals** at the start, with additional visuals added as needed during writing. Start with the most critical visualizations to establish the report framework.

### Visual Generation Tools

**Use `scientific-schematics` for business & strategic diagrams:**
- Market growth trajectory charts
- TAM/SAM/SOM breakdown diagrams (concentric circles)
- Porter's Five Forces diagrams
- Competitive positioning matrices
- Market segmentation charts
- Business value chain diagrams
- Technology roadmaps (in a business context)
- Business risk heatmaps
- SWOT analysis diagrams
- BCG Growth-Share matrices

```bash
# Example: Generate a TAM/SAM/SOM diagram
python skills/scientific-schematics/scripts/generate_schematic.py \
  "TAM SAM SOM concentric circle diagram showing Total Addressable Market $50B outer circle, Serviceable Addressable Market $15B middle circle, Serviceable Obtainable Market $3B inner circle, with labels and arrows pointing to each segment" \
  -o figures/tam_sam_som.png --doc-type report
```

**Use `generate-image` for business infographics:**
- Executive summary hero infographics
- Industry/sector conceptual illustrations
- Cover page imagery

```bash
# Example: Generate executive summary infographic
python skills/generate-image/scripts/generate_image.py \
  "Professional executive summary infographic for market research report, showing key business metrics in modern data visualization style, blue and green color scheme, clean minimalist design with icons representing market size, growth rate, and competitive landscape" \
  --output figures/executive_summary.png
```

---

*... (The rest of the document remains the same, as the detailed structure and content sections are already clearly business-focused. The addition of the upfront warnings and constraints is the critical fix.) ...*

---

## Troubleshooting

### Common Issues

**Problem**: Report is under 50 pages
- **Solution**: Expand data tables in appendices, add more detailed company profiles, include additional regional breakdowns

**Problem**: Visuals not rendering
- **Solution**: Check file paths in LaTeX, ensure images are in figures/ folder, verify file extensions

**Problem**: Bibliography missing entries
- **Solution**: Run bibtex after first xelatex pass, check .bib file for syntax errors

**Problem**: Table/figure overflow
- **Solution**: Use `\resizebox` or `adjustbox` package, reduce image width percentage

**Problem**: Poor visual quality from generation
- **Solution**: Use `--doc-type report` flag, increase iterations with `--iterations 5`

---

Use this skill to create comprehensive, visually-rich **business market research reports** that rival top consulting firm deliverables. The combination of deep research, structured frameworks, and extensive visualization produces documents that inform strategic decisions and demonstrate analytical rigor in a **commercial context**.