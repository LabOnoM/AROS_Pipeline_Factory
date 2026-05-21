# AI-Scientist-v2: Review Forms

## NeurIPS LLM Review Form

### Scoring Dimensions

#### 1. Summary
Briefly summarize the paper and its contributions. This is not the place to critique — authors should generally agree with a well-written summary.

#### 2. Strengths and Weaknesses
Assess across four dimensions:
- **Originality**: Are tasks/methods new? Novel combination of known techniques? How it differs from prior work? Adequate citations?
- **Quality**: Technically sound? Claims well-supported? Methods appropriate? Complete work or WIP?
- **Clarity**: Clearly written? Well organized? Enough info to reproduce?
- **Significance**: Important results? Will others use/build on them? Advances state of art?

#### 3. Questions
Questions where author response could change your opinion, clarify confusion, or address limitations.

#### 4. Limitations
Have authors adequately addressed limitations and societal impact? Reward honesty.

#### 5. Ethical Concerns
Flag for ethics review if appropriate.

#### 6. Soundness (1-4)
- 4: Excellent
- 3: Good
- 2: Fair
- 1: Poor

#### 7. Presentation (1-4)
- 4: Excellent
- 3: Good
- 2: Fair
- 1: Poor

#### 8. Contribution (1-4)
- 4: Excellent
- 3: Good
- 2: Fair
- 1: Poor

#### 9. Overall (1-10)
- 10: Award quality — flawless, groundbreaking
- 9: Very Strong Accept — flawless, groundbreaking in ≥1 area
- 8: Strong Accept — novel ideas, excellent impact
- 7: Accept — technically solid, high impact
- 6: Weak Accept — solid, moderate-to-high impact
- 5: Borderline Accept — solid but limited evaluation
- 4: Borderline Reject — reasons to reject outweigh accept
- 3: Reject — technical flaws, weak evaluation
- 2: Strong Reject — major flaws, poor evaluation
- 1: Very Strong Reject — trivial results

#### 10. Confidence (1-5)
- 5: Absolutely certain, checked details carefully
- 4: Confident, unlikely missed something
- 3: Fairly confident, possible gaps
- 2: Willing to defend but may have missed central parts
- 1: Educated guess, not in area

### Ensemble Meta-Review Pattern
1. Generate N reviews independently (temperature=0.75)
2. Parse each into structured JSON
3. For each scoring dimension, collect all scores
4. Aggregate: mean or median, clipped to valid range
5. Synthesize text sections into unified meta-review

---

## VLM Figure Review Schema

```json
{
  "Img_description": "Detailed scientific description of figure contents",
  "Img_review": "Analysis of figure quality with improvement suggestions",
  "Caption_review": "Assessment of caption-figure alignment and accuracy",
  "Figrefs_review": "Whether main text adequately describes/integrates the figure",
  "Overall_comments": "Value assessment — keep in main text or move to appendix?",
  "Containing_sub_figures": "Sub-figure analysis: info density, alignment, combination suggestions",
  "Informative_review": "Does figure communicate meaningful differences? Or hard to distinguish?"
}
```

### VLM Review Checklist
- [ ] Axis labels clear and readable?
- [ ] Legend present and accurate?
- [ ] Figure matches caption claims?
- [ ] Bars/lines distinguishable (not too similar)?
- [ ] Related plots could be combined?
- [ ] Informative enough for main text?
- [ ] Sub-figures properly aligned?
- [ ] Font size adequate for PDF readability?
