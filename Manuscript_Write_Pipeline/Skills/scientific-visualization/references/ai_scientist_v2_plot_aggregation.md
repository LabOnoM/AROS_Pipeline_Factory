# AI-Scientist-v2: LLM-Driven Plot Aggregation Pattern

> Adapted from [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2)

## Auto-Aggregator Pattern

When you have multiple experiment results (JSON summaries, `.npy` files), use an LLM to automatically generate a comprehensive plotting script.

### Workflow

1. **Collect experiment summaries** as structured JSON (baseline, research, ablation)
2. **Prompt an LLM** to write a self-contained Python plotting script
3. **Run the script** to generate figures in a `figures/` directory
4. **Review outputs** and iterate if needed (up to 5 rounds)

### Aggregator Script Rules

```python
# The aggregator script MUST:
# 1. Be fully self-contained (all imports, data loading)
# 2. Load data only from .npy files or JSON summaries — NO hallucinated data
# 3. Place all final plots in 'figures/' directory
# 4. Produce comprehensive, unique (non-duplicate) figures
# 5. Use larger-than-default font sizes for paper readability
# 6. Combine related plots as subfigures (max 3 per figure)
# 7. Use fig, axes = plt.subplots(1, N) for multi-panel figures

import matplotlib.pyplot as plt
import json
import numpy as np

plt.rcParams.update({'font.size': 14, 'axes.titlesize': 16, 'axes.labelsize': 14})

# Load experiment summaries
with open('logs/0-run/baseline_summary.json') as f:
    baseline = json.load(f)
with open('logs/0-run/research_summary.json') as f:
    research = json.load(f)

# Create comprehensive figures
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
# ... plot data from summaries ...
plt.tight_layout()
plt.savefig('figures/main_results.png', dpi=300, bbox_inches='tight')
```

### When to Use This Pattern

- After running systematic experiments with structured outputs
- When you have multiple result files that need unified visualization
- For preparing publication-quality figures from experiment logs
- When you want to ensure no data is hallucinated in plots
