# Scientific Data Interpretation Pattern

This pattern focuses on how to present complex scientific dataset context and AI-driven insights within an A2UI interface.

## 1. Guided Dataset Introduction (Welcome Screen)

When an agent is bound to a specific dataset (like GSE261849 RNA-seq), it should provide an immediate orienting context.

### Intro Card Components:
- **Abstract/Background**: A 2-3 sentence summary of the study (e.g., "iPSC-derived NCC differentiation").
- **Dataset Scale**: Metadata about samples, replicates, and gene counts (e.g., "15 samples, 14,312 genes").
- **Developmental Stages**: A clear textual timeline or list of conditions (📋 Stages: Day 5 -> Day 9 ...).

### Key Findings Card:
Instead of just describing tools, the agent summarizes the data's "Ground Truth" findings:
- PCA variance explanations (e.g., "PC1 separates early NCC aggregates...").
- DE gene counts for primary comparisons.
- Pathway enrichment highlights (WNT, EMT, etc.).
- Notable marker gene patterns.

## 2. Dynamic AI Suggestions (Plot Context)

In interactive plot configuration panels, the agent should not just provide "Settings" (sliders/dropdowns) but also "Expert Advice" (Text pills with 💡 tips).

### Types of Suggestions:
- **Visual/Publication Tips**: "Try 'pastel' palette for a publication-ready look."
- **Analysis Tips**: "Show PC1 vs PC3 to reveal additional variance structure."
- **Discovery Tips**: "Adjust LFC threshold to 2.0 to focus on strongest effects."
- **Biological Tips**: "Enable labels to identify specific replicates in the mdEM cluster."

## 3. Tool Metadata & Skill Grounding

The agent links its native tools with the broader Skills Library:
- Mentions available bioinformatics skills (scanpy, pydeseq2).
- Encourages users to ask about methodology (e.g., "Ask me how DESeq2 normalization works").
- Connects dataset findings to scientific databases (gene-database, pubmed-database).

## Implementation Tips

- **Server-Side Generation**: Generate these interpretation components server-side (`ui_builder.py`) to ensure they are always present and formatted correctly, rather than relying on the LLM to remember the findings every turn.
- **Action Buttons**: Pair interpretations with Action Buttons that immediately generate the relevant plots (e.g., "📊 See PCA Plot").
- **Context-Aware Suggestions**: For Volcano plots, suggest LFC/p-value changes; for PCA plots, suggest Axis/Palette changes.
