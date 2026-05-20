---
name: biological-insight-interpretation
description: A policy for agents on how to correctly extract, interpret, and present biological insights from scientific data and reports, including explaining significance, proposing hypotheses, and connecting findings to the broader context.
license: MIT
skill-author: AROS-Core
---

# Biological Insight Interpretation Policy

This document outlines the policy for handling and presenting biological insights, ensuring scientific accuracy, depth of interpretation, and integrity.

## GEPA Error Prevention Rules

**GEPA-Rule-BIO-001: Maintain Original Context and Meaning**

Extract and present the biological insights and interpretations derived from enrichment analysis or other reported findings, maintaining their original context and meaning without oversimplification or causal leaps.

**GEPA-Rule-BIO-002: Explain Significance and Propose Next Steps**

When reporting a biological finding, the agent MUST move beyond literal interpretation and provide deeper analytical value. This includes:
1.  **Explaining Significance:** State *why* the finding is important in the context of the research question or biological system.
2.  **Proposing Hypotheses:** Formulate at least one plausible, testable hypothesis that logically follows from the finding.
3.  **Connecting to Broader Context:** Briefly explain how the finding relates to the broader field of study, connecting it to established knowledge.

**GEPA-Rule-BIO-003: Demonstrate Comprehensive Contextual Understanding**

The agent must demonstrate a comprehensive understanding of the relevant biological context and processes to accurately interpret data.

## When to Use

- Use this policy when processing outputs from bioinformatics tools, such as gene enrichment analysis, differential expression results, or pathway analysis.
- Apply this policy when summarizing or extracting conclusions from scientific papers, reports, or datasets.
- This policy is critical when generating Knowledge Items (KIs) or reports that require not just data extraction, but also scientific interpretation.

## Guiding Principles

- **No Overstating Conclusions:** Agents must not exaggerate or generalize findings beyond what the data and original authors have stated. Avoid speculative language unless it is explicitly marked as such and attributed to the source.
- **Preserve Nuance:** Biological findings often have important caveats, limitations, or specific conditions. These must be preserved in any summary or interpretation.
- **Attribute Source:** All extracted insights must be clearly attributed to their original source (e.g., publication, dataset, analysis report).
- **Go Beyond Literal Reporting:** Do not simply state the finding. Add value by explaining what it means, why it matters, and what could be tested next.
- **Context is Key:** When presenting a finding, include relevant context such as the organism studied, experimental conditions, and statistical significance.

## Validation

To validate the application of this policy, an agent's output should be reviewed against the following checklist:
1.  **Context Preservation:** Does the interpretation accurately reflect the source's context, inc
