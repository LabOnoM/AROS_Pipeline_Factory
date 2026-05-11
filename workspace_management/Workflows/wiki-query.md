---
description: Query the LLM-Wiki to synthesize answers, generate comparison tables, or find specific facts based strictly on the ingested knowledge base.
---

# Wiki Query Workflow

Use this workflow to query the established LLM-Wiki. The agent must rely *only* on the contents of the `.wiki/` directory to answer, avoiding hallucinated external knowledge.

## Step 1: Define the Query

Define your question or the required output format (e.g., "Compare the isoforms of RUNX2 and SP7 in a table", or "What is the evidence for SP7-uORF promoting thrombolysis?").

## Step 2: Agent Retrieval

Prompt the agent with:
> "Please search the `.wiki/` directory for information related to [Topic]. Read the relevant entity, concept, and source pages using your tools."

## Step 3: Synthesis & Output

The agent must synthesize the answer using *only* facts present in the read pages.
- Provide citations using `[[wikilinks]]` to the specific `.wiki/` files.
- If requested, generate specific artifacts like markdown tables (e.g., `Marp` format), graphs, or Mermaid diagrams based on the wiki data.
- **Rule**: If the answer is not in the wiki, the agent must state: "This information has not yet been ingested into the wiki."
