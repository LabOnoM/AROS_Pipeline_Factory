# AI-Scientist-v2: Research Ideation Schema

## Structured Idea JSON Format

Every research idea is represented as a JSON object with the following fields:

```json
{
  "Name": "short_descriptor_lowercase_underscores",
  "Title": "A Catchy and Informative Title for the Proposal",
  "Short Hypothesis": "A concise statement of the main hypothesis or research question. Clarify the need for this specific direction, ensure this is the best setting to investigate, and there are not obvious simpler ways to answer the question.",
  "Related Work": "A brief discussion of the most relevant related work and how the proposal clearly distinguishes from it, and is not a trivial extension.",
  "Abstract": "An abstract that summarizes the proposal in conference format (approximately 250 words).",
  "Experiments": "A list of experiments to validate the proposal. Be specific in exactly how you would test the hypothesis, with precise algorithmic changes. Include evaluation metrics.",
  "Risk Factors and Limitations": "Potential risks and limitations of the proposal."
}
```

## Ideation Loop (Temperature-Free)

### Step 1: Initial Generation
```
Given a workshop/topic description and any previously generated ideas,
generate an interestingly new high-level research proposal that differs 
from what was previously proposed.
```

### Step 2: Tool Use (Semantic Scholar Search)
Before finalizing, perform at least one literature search:
```
ACTION: SearchSemanticScholar
ARGUMENTS: {"query": "your search query here"}
```

### Step 3: Reflection (N rounds)
```
In your thoughts, carefully consider:
- Quality, novelty, and feasibility of the proposal
- Any other important evaluation factors
- Ensure clarity and conciseness
- Don't make things overly complicated
- Stick to the spirit of the original idea unless glaring issues

If you have new information from tools (e.g., literature search results),
incorporate them into your reflection and refine accordingly.
```

### Step 4: Finalize
```
ACTION: FinalizeIdea
ARGUMENTS: {"idea": { ... JSON ... }}
```

## Topic Description Template

Create a Markdown file with these sections:

```markdown
# Title
[Research area title]

# Keywords
[Comma-separated keywords]

# TL;DR
[One-sentence summary of the research direction]

# Abstract
[Detailed description of the research area, open questions, and what 
types of contributions would be valuable]
```

## Key Principles

1. **Novelty First**: Always search literature before finalizing
2. **Feasibility**: Ensure proposals don't exceed academic lab resources
3. **Simplicity**: Stem from simple, elegant questions or observations
4. **Specificity**: Detail exact algorithmic changes and evaluation metrics
5. **Differentiation**: Clearly distinguish from existing work
6. **Iterative Refinement**: Use multiple reflection rounds to improve quality
