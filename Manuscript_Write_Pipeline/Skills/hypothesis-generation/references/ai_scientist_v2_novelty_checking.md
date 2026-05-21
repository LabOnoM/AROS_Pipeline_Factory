# AI-Scientist-v2: Novelty-Validated Ideation Pattern

> Adapted from [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)

## Semantic Scholar Novelty Checking

Before finalizing any research hypothesis, validate novelty by searching academic literature:

1. **Formulate search queries** based on your hypothesis keywords
2. **Search Semantic Scholar** for similar work (API: `https://api.semanticscholar.org/graph/v1/paper/search`)
3. **Analyze results** — check if the core idea has been explored
4. **Differentiate** — clearly articulate how your hypothesis differs from existing work
5. **Iterate** — refine the hypothesis based on what you find

## Structured Hypothesis JSON Output

For machine-readable hypothesis output, use this schema:

```json
{
  "Name": "short_descriptor",
  "Title": "Informative title",
  "Short Hypothesis": "Concise testable statement",
  "Related Work": "Key differences from existing literature",
  "Abstract": "~250 word summary",
  "Experiments": "Specific tests with metrics",
  "Risk Factors and Limitations": "Known risks"
}
```

## Multi-Round Reflection

Use iterative refinement (3-5 rounds):
1. Generate initial hypothesis
2. Search literature for novelty
3. Reflect: evaluate quality, novelty, feasibility
4. Refine: incorporate search results
5. Finalize only when confident in novelty

**Key Principle:** Every hypothesis must survive at least one round of literature-based novelty checking before being considered valid.
