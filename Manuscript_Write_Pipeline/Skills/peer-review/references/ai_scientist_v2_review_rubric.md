# AI-Scientist-v2: NeurIPS Review Rubric & Ensemble Meta-Review

> Adapted from [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)

## NeurIPS Review Form (Full Rubric)

### Scoring Dimensions

| # | Dimension | Scale | Key Question |
|---|-----------|-------|--------------|
| 1 | Summary | text | Can the authors agree with this factual summary? |
| 2 | Strengths & Weaknesses | text | Originality, Quality, Clarity, Significance |
| 3 | Questions | text | What could change the reviewer's opinion? |
| 4 | Limitations | text | Are limitations adequately addressed? |
| 5 | Ethics | flag | Does this need an ethics review? |
| 6 | Soundness | 1-4 | Are technical claims and methods well-supported? |
| 7 | Presentation | 1-4 | Is the writing clear, organized, contextualized? |
| 8 | Contribution | 1-4 | Does this advance the field meaningfully? |
| 9 | Overall | 1-10 | Holistic assessment (10=Award, 1=Very Strong Reject) |
| 10 | Confidence | 1-5 | How well does the reviewer know this area? |

### Overall Score Guide

| Score | Label | Description |
|-------|-------|-------------|
| 10 | Award quality | Flawless, groundbreaking impact |
| 8 | Strong Accept | Novel ideas, excellent impact |
| 6 | Weak Accept | Solid, moderate-to-high impact |
| 5 | Borderline Accept | Solid but limited evaluation |
| 4 | Borderline Reject | Reasons to reject outweigh accept |
| 3 | Reject | Technical flaws, weak evaluation |
| 1 | Very Strong Reject | Trivial results |

## Ensemble Meta-Review Pattern

Generate multiple independent reviews and synthesize:

1. **Generate N reviews** (recommended: 3) at temperature 0.75
2. **Parse each** into structured JSON with all scoring dimensions
3. **Aggregate scores**: for each numeric dimension, collect all scores, compute mean, clip to valid range
4. **Synthesize text**: combine strengths, weaknesses, questions from all reviewers
5. **Produce meta-review**: unified assessment with aggregated scores

```python
# Score aggregation pattern
for dimension, (min_val, max_val) in scoring_dimensions.items():
    scores = [review[dimension] for review in parsed_reviews if dimension in review]
    if scores:
        aggregated = int(round(np.mean(scores)))
        aggregated = max(min_val, min(max_val, aggregated))
        meta_review[dimension] = aggregated
```

## VLM Figure Review

Use vision models to review paper figures with structured output:

```json
{
  "Img_description": "What the figure shows",
  "Img_review": "Quality analysis + improvement suggestions",
  "Caption_review": "Caption-figure alignment",
  "Figrefs_review": "Main text integration quality",
  "Overall_comments": "Keep in main text or move to appendix?",
  "Containing_sub_figures": "Sub-figure density and alignment",
  "Informative_review": "Does it effectively communicate patterns?"
}
```
