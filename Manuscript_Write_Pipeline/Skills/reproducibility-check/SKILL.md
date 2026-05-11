---
name: reproducibility-check
description: Check whether a paper’s Methods section contains all information needed for replication and is explained in an accessible manner; use when preparing a manuscript for submission or reviewing methodological completeness.
license: MIT
skill-author: AIPOCH
---

## GEPA Rules

**GEPA-Rule-Bio-01: Accessible Methodology Explanation**

The report must provide a detailed yet accessible explanation of the bioinformatics methodology and all parameters used, enabling clarity and reproducibility without overwhelming the user with unnecessary jargon. The explanation should be clear to a competent researcher in the field who may not be an expert in the specific technique used.

## When to Use

Use this skill when you need to assess whether a study can be reproduced based on its Methods section, for example:

1.  **Pre-submission self-check** to ensure the Methods section is complete and clear before journal submission.
2.  **Replication feasibility review** to determine whether another lab/team could repeat the work.
3.  **Peer review / methodological audit** to identify missing details, ambiguities, or overly technical descriptions.
4.  **Internal lab documentation check** to improve protocol clarity and reduce tacit knowledge.
5.  **Meta-research / reproducibility screening** to triage papers by reproducibility risk.

Trigger condition: if the user provides only an abstract/results/discussion without the full Methods section, request the complete Methods section first.

## Key Features

-   **Methods completeness audit** focused on replication-critical details.
-   **Structured missing-items report** with clear priority levels (High/Low).
-   **Ambiguity detection** for unclear or underspecified descriptions.
-   **Clarity and Jargon Check** to assess the accessibility of the explanation per GEPA-Rule-Bio-01.
-   **Reproducibility risk rating** (Low/Medium/High) with explicit rationale.
-   **Actionable supplementation suggestions** mapped to specific deficiencies.
-   **Checklist-driven output** using `assets/reproducibility_checklist.md` when available.

## Dependencies

-   `assets/reproducibility_checklist.md` (recommended for structured reporting)
-   `references/guide.md` (recommended for formatting guidance and key checkpoints)

## Example Usage

### Input (user)
```text
Please check whether the following Methods section is complete and reproducible. Identify missing items (high/low priority), unclear descriptions, and provide a reproducibility risk rating with suggestions.

[PASTE FULL METHODS SECTION HERE]

Optional context:
- Equipment list: [models, manufacturers]
- Software: R 4.3.1, Python 3.11, packages: ...
- Statistical plan: ...
- Data processing workflow: ...
```

### Output (assistant)
```markdown
## Reproducibility Check (Methods Section)

### 1) Missing Information
**High Priority (required for replication)**
1.  **Sample size determination**: No power analysis or rationale provided for n=...
    -   Location in text: "..."
    -   Why it matters: affects statistical validity and replication planning.
2.  **Reagent/source details**: Antibody X lacks catalog number, clone, vendor, and lot.
    -   Location in text: "..."

**Low Priority (improves robustness/clarity)**
1.  **Environmental conditions**: Temperature/humidity not reported for assay Y.
    -   Location in text: "..."

### 2) Unclear or Ambiguous Descriptions
1.  **“Performed as previously described”** without a specific, accessible citation.
    -   Location in text: "..."
    -   Suggestion: Provide a direct citation with a page or method number.
2.  **Ambiguous software parameter**: The parameter for software tool Y is described as “default,” but the software version is not specified, and defaults can change between versions.
    -   Location in text: "..."
    -   Suggestion: Specify the software version and the actual value of the parameter used.

### 3) Methodology Explanation and Accessibility (GEPA-Rule-Bio-01)
1.  **High Jargon Density**: The section on statistical analysis uses highly specialized terms without definition (e.g., "isomorphic manifold assumption," "Bayesian hyper-prior").
    -   Location in text: "..."
    -   Suggestion: Define these terms upon first use or provide a citation to a standard definition. For complex methodologies, consider adding a supplementary information section.
2.  **Inaccessible Parameter Explanation**: The parameter `q-value-threshold` for the DEG analysis tool is given as `0.05`, but the report does not explain what this parameter represents or why this value was chosen over a standard p-value.
    -   Location in text: "..."
    -   Suggestion: Briefly explain the function of critical parameters. For example, "The `q-value-threshold` (set to 0.05) controls the False Discovery Rate (FDR) for multiple hypothesis testing..."
```
