---
name: venue-templates
description: Venue-specific LaTeX templates, formatting requirements, and submission guidelines for journals, conferences, posters, and grants—use when a target venue imposes strict layout, page limits, anonymization, or agency compliance rules.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
skill-author: AIPOCH
---

## Overview

Access comprehensive LaTeX templates, formatting requirements, and submission guidelines for major scientific publication venues, academic conferences, research posters, and grant proposals. This skill provides ready-to-use templates and detailed specifications for successful academic submissions across disciplines. It also includes writing style guides and examples to ensure your content matches the venue's expectations.

Use this skill when preparing manuscripts for journal submission, conference papers, research posters, or grant proposals and need venue-specific formatting requirements and templates.

## When to Use This Skill

This skill should be used when:

- You are submitting a manuscript to a specific journal (e.g., Nature, Science, PLOS, Cell Press, IEEE, ACM) and must follow its official LaTeX class/style and author instructions.
- You are preparing a conference paper (e.g., NeurIPS, ICML, ICLR, CVPR, CHI, ACL/EMNLP) with strict page limits, anonymization rules, and required formatting.
- You need to produce a conference poster in a standard size (A0/A1/36×48/etc.) using common LaTeX poster packages.
- You are drafting a grant proposal (e.g., NSF, NIH, DOE, DARPA) where compliance constraints (page limits, margins, font rules, required sections) are enforced.
- You want to validate that a compiled PDF complies with venue requirements (page count, margins, fonts, reference style, figure constraints).

## Core Capabilities

### 1. Template Library

Access LaTeX templates and formatting guidelines for:

- **Journal articles**: Nature portfolio, Science family, PLOS, Cell Press, IEEE, ACM, Springer/Elsevier/Wiley/BMC/Frontiers, etc.
- **Conference papers**: NeurIPS/ICML/ICLR/CVPR/AAAI/CHI/SIGKDD/EMNLP/SIGIR/USENIX, etc.
- **Research posters**: A0/A1/US sizes; `beamerposter`, `tikzposter`, `baposter` packages.
- **Grant proposals**: NSF/NIH/DOE/DARPA + selected foundations.

### 2. Venue Requirements References

Access information on:

- Page limits
- Fonts
- Margins
- Spacing
- Anonymization rules
- File formats
- Supplementary material limits

### 3. Helper Scripts

Utilize scripts to:

- Query templates/requirements by venue (`scripts/query_template.py`)
- Customize templates with metadata (`scripts/customize_template.py`)
- Validate compiled outputs (`scripts/validate_format.py`)

### 4. Writing Style Guides and Examples

Consult guides and examples (stored under `references/` and `assets/examples/`) to understand how the "voice" differs across venues.

## Workflow: Finding, Using, and Validating Templates

### Step 1: Identify Target Venue

Determine the specific publication venue, conference, or funding agency.

```
Example queries:
- "I need to submit to Nature"
- "What are the requirements for NeurIPS 2025?"
- "Show me NSF proposal formatting"
- "I'm creating a poster for ISMB"
```

### Step 2: Query Template and Requirements

Access venue-specific templates and formatting guidelines using the helper scripts.

```bash
# Discover templates and requirements for a venue
python scripts/query_template.py --venue "NeurIPS" --type "article"
python scripts/query_template.py --venue "NeurIPS" --requirements
```

### Step 3: Review Formatting Requirements

Check critical specifications before customizing.

### Step 4: Customize Template

Use the helper script or manual customization. Recommended practice: do not override class options, margins, font settings, or bibliography style unless the venue explicitly allows it.

```bash
# Customize a template (example: Nature article)
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --title "Your Paper Title" \
  --authors "First Author, Second Author" \
  --affiliations "University Name" \
  --output my_nature_paper.tex
```

### Step 5: Compile the Document

```bash
# Compile (choose one)
latexmk -pdf my_nature_paper.tex
# or:
pdflatex my_nature_paper.tex
bibtex my_nature_paper
pdflatex my_nature_paper.tex
pdflatex my_nature_paper.tex
```

### Step 6: Validate Format

Check compliance with venue requirements using the helper script.

```bash
# Validate the compiled PDF against venue rules
python scripts/validate_format.py \
  --file my_nature_paper.pdf \
  --venue "Nature" \
  --check-all
```

**Validation Checks (typical)**:

- Page count vs. venue limit (e.g., NeurIPS/ICML main text limits; NSF/NIH section limits).
- Margin and font constraints (common in grants; sometimes enforced in conferences).
- Reference/citation style consistency (numeric vs author-year; bracket vs superscript).
- Figure constraints (resolution guidance, allowed formats, color requirements).
- Anonymization requirements for double-blind venues (presence of author-identifying metadata).

## Integration with Other Skills

This skill works seamlessly with other scientific skills, such as scientific-writing, literature-review, and research-grants.

## Resources

### Bundled Resources

**Requirements**:

- `references/journals_formatting.md`: Journal formatting requirements
- `references/conferences_formatting.md`: Conference paper specifications
- `references/posters_guidelines.md`: Research poster design and sizing
- `references/grants_requirements.md`: Grant proposal requirements by agency

**Templates**:

- `assets/journals/`: Journal article LaTeX templates
- `assets/posters/`: Research poster templates
- `assets/grants/`: Grant proposal templates

**Writing Style Guides**:

- `references/venue_writing_styles.md`: Master style overview and comparison
- `references/nature_science_style.md`: Nature/Science writing conventions
- `references/ml_conference_style.md`: ML conference writing conventions
- `references/reviewer_expectations.md`: What reviewers look for by venue

**Writing Examples**:

- `assets/examples/`: Examples illustrating venue-typical abstracts/introductions/structured sections.

**Scripts**:

- `scripts/query_template.py`: Search and retrieve templates
- `scripts/customize_template.py`: Customize with author info
- `scripts/validate_format.py`: Check compliance with requirements

### External Resources

**Journal Author Guidelines**:

- Nature: https://www.nature.com/nature/for-authors
- Science: https://www.science.org/content/page/instructions-authors
- PLOS: https://plos.org/resources/for-authors/
- Cell Press: https://www.cell.com/author-guidelines

**Conference Formatting**:

- NeurIPS: https://neurips.cc/Conferences/2024/CallForPapers
- ICML: https://icml.cc/Conferences/2024/StyleAuthorInstructions
- CVPR: https://cvpr.thecvf.com/Conferences/2024/AuthorGuidelines

**Grant Resources**:

- NSF PAPPG: https://www.nsf.gov/publications/pub_summ.jsp?ods_key=pappg
- NIH Forms: https://grants.nih.gov/grants/how-to-apply-application-guide.html
- DOE Funding: https://science.osti.gov/grants

## Dependencies

- Python `>=3.10`
- TeX Live `>=2023` (or MiKTeX `>=23.x`)
- `latexmk >=4.80` (recommended for reproducible builds)

## Example Usage

### Example 1: NeurIPS Paper

```markdown
User: I am writing a NeurIPS paper. What are the formatting requirements?

Response:
Here are the NeurIPS formatting requirements from references/conferences_formatting.md:

- Page limit: 8 pages main text + unlimited references/appendix
- Format: Two-column, 10pt font
- Template: neurips_2024.sty (official style file)
- Anonymization: Required for initial submission
- Citations: Numbered (brackets)
- Figures: High resolution, colorblind-safe recommended

You can use scripts/query_template.py to find the appropriate template file.
```

### Example 2: Nature Submission

```markdown
User: I need to format a paper for Nature.

Response:
Here are the Nature formatting requirements from references/journals_formatting.md:

- Length: ~3000 words, ~5 pages
- Format: Single column, 12pt font
- Citations: Numbered superscript (Nature style)
- Figures: 300+ dpi, RGB color

You can find the Nature template at assets/journals/nature_article.tex. Use scripts/customize_template.py to fill in your paper's metadata.
```