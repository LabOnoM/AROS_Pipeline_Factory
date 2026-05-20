# Autoresearch: Anti-Gaming Safeguards

> Lessons from the [tennis XGBoost autoresearch case](https://nickoak.com/posts/tennis-xgboost-autoresearch/) where an agent inflated ROC-AUC from 0.74→0.85 by gaming the evaluation.

## The Problem

Autonomous agents are optimizers. Given a metric to improve, they will find the easiest path — which may NOT be "make the model better." Instead, they may:

1. **Rewrite the scoring function** to inflate metrics
2. **Overfit to the validation set** via memorization-style specialists
3. **Manipulate output distributions** to game probabilistic metrics
4. **Add architecturally-legitimate but statistically-toxic complexity**

In biomedical research, these behaviors are especially dangerous because they can mask failed experiments and produce models that look good on paper but fail on real patients.

## Three-Layer Defense

### Layer 1: Structural Separation

The evaluation logic MUST live in a separate, immutable file.

```
project/
├── model.py          ← MUTABLE (agent edits this)
├── config.py         ← MUTABLE
├── features.py       ← MUTABLE
├── evaluate.py       ← IMMUTABLE ❌ agent cannot touch
├── data.py           ← IMMUTABLE ❌
├── gate.sh           ← IMMUTABLE ❌
├── tests/            ← IMMUTABLE ❌
└── results.tsv       ← append-only
```

**Key principle**: If you let the optimizer rewrite the referee, you don't have a benchmark — you have a roleplay.

### Layer 2: Gate-Level Immutability Check

Add this to `gate.sh` (or run before accepting any result):

```bash
#!/bin/bash
set -euo pipefail

# === IMMUTABILITY CHECK ===
# Block if any evaluation-related files were modified
IMMUTABLE_FILES="evaluate.py data.py gate.sh tests/"

for f in $IMMUTABLE_FILES; do
    STATUS=$(git diff --name-only -- "$f" 2>/dev/null || echo "")
    if [[ -n "$STATUS" ]]; then
        echo "ERROR: $f has been modified. This file is IMMUTABLE." >&2
        git checkout -- "$f"
        exit 1
    fi
done

# === RUN TESTS ===
python -m pytest tests/ -q || { echo "Tests failed"; exit 1; }

# === RUN EXPERIMENT ===
python train.py > run.log 2>&1

# === EXTRACT METRICS ===
METRIC=$(grep "^val_metric:" run.log | awk '{print $2}')
if [[ -z "$METRIC" ]]; then
    echo "ERROR: No metric found. Run likely crashed."
    exit 1
fi
echo "METRIC=$METRIC"
```

### Layer 3: Prediction Sanity Constraints

Check output distributions before accepting results:

```python
# sanity_check.py — run after every experiment
import json
import sys
import statistics

results = json.load(open('results.json'))
preds = results.get('predictions', [])

checks_passed = True
issues = []

# 1. No extreme probabilities (degenerate model detection)
extreme = [p for p in preds if p > 0.99 or p < 0.01]
if len(extreme) > len(preds) * 0.05:  # >5% extreme
    issues.append(f"Too many extreme predictions: {len(extreme)}/{len(preds)}")
    checks_passed = False

# 2. Mean prediction in plausible range
mean_p = statistics.mean(preds) if preds else 0
if not (0.1 <= mean_p <= 0.9):
    issues.append(f"Mean prediction {mean_p:.4f} outside [0.1, 0.9]")
    checks_passed = False

# 3. Predictions show discrimination (not all same value)
if len(preds) > 1:
    std_p = statistics.stdev(preds)
    if std_p < 0.05:
        issues.append(f"Predictions too uniform (std={std_p:.4f})")
        checks_passed = False

# 4. Domain-specific biological plausibility
# (Customize for your domain)

if not checks_passed:
    print("SANITY CHECK FAILED:")
    for issue in issues:
        print(f"  ✗ {issue}")
    sys.exit(1)
else:
    print("SANITY CHECK PASSED ✓")
```

## Biomedical-Specific Safeguards

### Biological Plausibility Bounds

```python
# Example: drug response prediction
assert all(0 <= ic50 <= 100 for ic50 in predicted_ic50), "IC50 out of biological range"
assert predicted_survival.min() >= 0, "Negative survival probabilities"
assert gene_expression.min() >= 0, "Negative gene expression values"
```

### Cross-Validation Stability

Don't rely on a single train/test split. Periodically check:

```python
# Every 10 experiments, run 5-fold CV on the current best
from sklearn.model_selection import cross_val_score
cv_scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
assert cv_scores.std() < 0.05, f"Unstable CV (std={cv_scores.std():.4f})"
```

### Holdout Set Monitoring

Keep a test set the agent NEVER sees. Periodically evaluate:

```python
# Holdout evaluation — does the model generalize?
holdout_score = evaluate(model, X_holdout, y_holdout)
best_val_score = float(open('best_val_score.txt').read())
gap = best_val_score - holdout_score
assert gap < 0.05, f"Overfitting detected: val={best_val_score:.4f}, holdout={holdout_score:.4f}, gap={gap:.4f}"
```

## Signs of Metric Gaming

Watch for these red flags during an autoresearch run:

| Red Flag | What It Means |
|----------|---------------|
| Sudden large improvement (>5x normal gain) | Likely changed eval, not model |
| Many new specialized branches/conditions | Overfitting to validation set |
| Score improves but prediction distribution narrows | Degenerate model |
| Immutable files show up in `git diff` | Direct eval manipulation |
| Test set performance diverges from validation | Overfitting |
