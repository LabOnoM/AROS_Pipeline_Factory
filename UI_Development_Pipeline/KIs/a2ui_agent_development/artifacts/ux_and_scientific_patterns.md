# UX and Scientific Interpretation Patterns

This document covers high-level patterns for orienting users and presenting complex scientific insights within A2UI-powered agents.

## 1. The Guided Welcome Screen Pattern

The **Guided Welcome Screen** is a proactive UX pattern that provides immediate value upon the user's first interaction, reducing the "blank page" problem.

### Key Features
*   **Automatic Arrival**: Triggered on page load via an `__init__` handshake message from the client.
*   **Server-Side Reliability**: Generated as a static A2UI surface by the server (not the LLM) for speed and technical correctness.
*   **Discovery**: Displays "Action Buttons" (e.g., "📊 See PCA Plot") that translate UI clicks into LLM queries.

### Implementation Checklist
- [ ] **Title & Abstract**: Clearly identify the dataset (e.g., GSE261849) and provide a 2-sentence summary.
- [ ] **Scale & Conditions**: List sample counts, genes, and experimental stages.
- [ ] **Quick Start Actions**: Row of buttons for the most frequent workflows.
- [ ] **Agent Expertise**: Mention the available scientific skills (e.g., scanpy, pydeseq2).

## 2. Scientific Data Grounding

For scientific datasets, the interface should not just offer "tools" but also "ground truth" context.

### The "Key Findings" Card
A card that summarizes the core variance and results of the dataset, providing the user with immediate knowledge:
*   "PC1 (31.9% variance) separates aggregates from mdEM."
*   "3,247 genes are DE between Stage 1 and Stage 5."
*   "Enrichment found in neural crest and WNT pathways."

### AI Suggestions (Expert Tips)
In configuration panels or results cards, provide "AI Suggestions" (marked with 💡) to guide the user's next steps:
*   **Visual Tips**: "Try 'vivid' palette for clearer sample separation."
*   **Analysis Tips**: "Show PC2 vs PC3 to explore lineage divergence."
*   **Discovery Tips**: "Decrease LFC threshold to 0.5 to see broader trends."

## 3. Skill Integration and Discovery

Use the interface to bridge the gap between the dataset analysis and the broader skills library:
*   **Methodology Inquiries**: Prompt the user to ask "How does GO enrichment calculation work?" to trigger a `read_skill` call.
*   **Expert Recommendations**: Based on the data, suggest using specific skills like `cellxgene-census` for broad tissue comparison.

## 4. Interaction Flow: UI Action to LLM Intent

When a user clicks a button on the welcome screen or a results card:
1.  **Client**: Sends a `userAction` (e.g., `explore_action`) with a `query` context (e.g., "Show me the PCA plot").
2.  **Executor**: Intercepts the action, extracts the `query`, and sends it to the LLM.
3.  **LLM**: Processes the intent as if the user typed it, keeping the conversation natural while providing the efficiency of a GUI.
