# AI-Scientist-v2: Experiment Stage Progression

## Overview

The AI-Scientist-v2 BFTS (Best-First Tree Search) runs experiments in 4 progressive stages, each with clear goals. Stages build on each other, with increasing complexity and creativity.

## Stage Definitions

### Stage 1: Preliminary Implementation
**Name:** `1_initial_implementation_1_preliminary`

**Goals:**
- Focus on getting a basic working implementation
- Use a simple dataset
- Aim for basic functional correctness
- If given starter code, use it directly as a starting point

**Success Criteria:** Code runs without errors, produces basic results on one dataset.

---

### Stage 2: Baseline Tuning
**Name:** `2_baseline_tuning`

**Goals:**
- Change hyperparameters (learning rate, epochs, batch size) to improve performance
- DO NOT change the model architecture from stage 1
- Introduce TWO more new datasets from HuggingFace to test the model
- Think carefully about which HuggingFace datasets are appropriate

**Success Criteria:** Improved performance over stage 1, results on 3 datasets total.

---

### Stage 3: Creative Research
**Name:** `3_creative_research`

**Goals:**
- Explore novel improvements
- Come up with experiments to reveal new insights
- Be creative and think outside the box
- Use THREE HuggingFace datasets in total
- Follow the experiment plan from the research idea

**Success Criteria:** Novel approach explored, insights documented, 3-dataset results.

---

### Stage 4: Ablation Studies
**Name:** `4_ablation_studies`

**Goals:**
- Conduct systematic component analysis
- Reveal the contribution of each part
- Use the same datasets from stage 3

**Success Criteria:** Clear understanding of which components drive performance.

## Tree Search Configuration

```yaml
agent:
  num_workers: 3        # Parallel exploration paths
  steps: 21             # Max nodes to explore
  num_seeds: 3          # Initial seeds (match num_workers if < 3)

search:
  max_debug_depth: 3    # Max debug attempts per failing node
  debug_prob: 0.5       # Probability of debugging vs. fresh start
  num_drafts: 3         # Number of independent starting trees
```

## Agent Manager Flow

```
┌─────────────┐
│  Load Idea  │ (Title, Abstract, Hypothesis, Experiments)
└──────┬──────┘
       ▼
┌──────────────────┐
│ Stage 1: Prelim  │──→ Journal tracks each experiment
└──────┬───────────┘    Log summarization for LLM context
       ▼
┌──────────────────┐
│ Stage 2: Tuning  │──→ Best results from Stage 1 carry forward
└──────┬───────────┘
       ▼
┌──────────────────────┐
│ Stage 3: Creative    │──→ Experiment plan from idea guides exploration
└──────┬───────────────┘
       ▼
┌──────────────────────┐
│ Stage 4: Ablation    │──→ Systematic component removal/analysis
└──────┬───────────────┘
       ▼
┌─────────────────┐
│ Summaries JSON  │ (baseline_summary, research_summary, ablation_summary)
└─────────────────┘
```
