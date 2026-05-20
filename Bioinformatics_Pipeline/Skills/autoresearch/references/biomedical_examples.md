# Autoresearch: Biomedical Examples

> Concrete examples of applying the autoresearch loop to biomedical research tasks.

## Example 1: Drug Response Prediction

**Goal**: Optimize a model that predicts cancer cell line drug response (IC50).

### File Structure

```
drug_response/
├── model.py          ← MUTABLE: neural network architecture, features, hyperparameters
├── evaluate.py       ← IMMUTABLE: Pearson correlation of predicted vs. actual IC50
├── data.py           ← IMMUTABLE: GDSC/CCLE data loading, train/val/test splits
├── gate.sh           ← IMMUTABLE: immutability check + sanity constraints
├── program.md        ← Human-edited agent instructions
└── results.tsv
```

### `program.md` Configuration

```
MUTABLE_FILES: model.py
IMMUTABLE_FILES: evaluate.py, data.py, gate.sh
METRIC_NAME: pearson_r
BEST_DIRECTION: highest
TIME_BUDGET: 10 minutes
RUN_COMMAND: python model.py
SANITY_CHECKS:
  - All predicted IC50 values in [0, 100] μM range
  - Pearson r > 0 (model is at least weakly correlated)
  - Predictions have std > 0.5 (model discriminates between drugs)
```

### What the Agent Can Try

- Switch between MLP, random forest, gradient boosting
- Feature engineering: add/remove gene expression features, mutation features, drug fingerprints
- Hyperparameter tuning: learning rate, regularization, architecture depth
- Normalization strategies: z-score, quantile, log-transform
- Ensemble methods: combine multiple models

---

## Example 2: Cell Segmentation Pipeline

**Goal**: Optimize a U-Net for cell instance segmentation.

### File Structure

```
cell_segmentation/
├── model_config.py   ← MUTABLE: architecture config, augmentation, LR schedule
├── train.py          ← MUTABLE: training loop, loss function, optimizer
├── evaluate.py       ← IMMUTABLE: Dice score, IoU, cell count accuracy
├── data.py           ← IMMUTABLE: image loading, fixed test split
├── gate.sh
├── program.md
└── results.tsv
```

### Metric

```python
# In evaluate.py (IMMUTABLE)
composite_score = 0.5 * dice_score + 0.3 * iou_score + 0.2 * cell_count_accuracy
```

### What the Agent Can Try

- Architecture: U-Net depth, encoder backbone, attention blocks
- Loss function: Dice loss, focal loss, boundary loss, combinations
- Augmentation: rotation, elastic deform, color jitter, mixup
- Post-processing: watershed, connected components, NMS threshold
- Training: learning rate schedule, optimizer (Adam vs. AdamW vs. SGD)

---

## Example 3: Survival Analysis

**Goal**: Optimize a Cox proportional hazards model for patient survival prediction.

### File Structure

```
survival/
├── features.py       ← MUTABLE: feature engineering, selection, transformations
├── model.py          ← MUTABLE: Cox model variant, regularization
├── evaluate.py       ← IMMUTABLE: C-index, Brier score, calibration
├── data.py           ← IMMUTABLE: clinical data loading, temporal split
├── gate.sh
├── program.md
└── results.tsv
```

### Multi-Metric Objective

```python
# In evaluate.py (IMMUTABLE)
composite = (
    0.4 * c_index +                    # Discrimination
    0.3 * (1 - integrated_brier) +     # Calibration
    0.2 * time_dependent_auc +         # Time-varying discrimination
    0.1 * subgroup_min_c_index         # Worst-case subgroup performance
)
```

### Sanity Checks

```python
# Survival-specific sanity
assert all(0 <= s <= 1 for s in survival_probs), "Invalid survival probabilities"
assert survival_curve_is_monotone_decreasing(survival_probs), "Non-monotone survival curve"
assert c_index > 0.5, "Model performs worse than random"
```

---

## Example 4: Differential Expression Pipeline

**Goal**: Optimize preprocessing and normalization for DESeq2 analysis.

### File Structure

```
deseq2_pipeline/
├── preprocess.py     ← MUTABLE: filtering, normalization, batch correction
├── evaluate.py       ← IMMUTABLE: run DESeq2, count DEGs at FDR<0.05, compare to known markers
├── data.py           ← IMMUTABLE: count matrix loading, metadata
├── gate.sh
├── program.md
└── results.tsv
```

### Metric

```python
# In evaluate.py (IMMUTABLE)
# Known positive markers that SHOULD be significant
known_markers = ["TP53", "BRCA1", "EGFR", ...]
true_positives = sum(1 for g in known_markers if g in significant_genes)
sensitivity = true_positives / len(known_markers)

# Total DEGs (too many = likely batch effects; too few = under-powered)
n_degs = len(significant_genes)
deg_penalty = 1.0 if 100 <= n_degs <= 5000 else 0.5

composite = sensitivity * deg_penalty
```

### What the Agent Can Try

- Filtering thresholds: minimum counts, minimum samples
- Normalization: TMM, RLE, upper-quartile, TPM
- Batch correction: ComBat, SVA, RUVseq
- Covariate adjustment: different model formulas
- Outlier detection: Cook's distance threshold

---

## Example 5: Protein Structure Scoring

**Goal**: Optimize a scoring function for protein-ligand binding affinity prediction.

### File Structure

```
binding_affinity/
├── scoring.py        ← MUTABLE: features, model, weights
├── evaluate.py       ← IMMUTABLE: Pearson r, Spearman ρ, RMSE against PDBbind test set
├── data.py           ← IMMUTABLE: PDBbind data loading
├── gate.sh
├── program.md
└── results.tsv
```

---

## General Biomedical Principles

1. **Use composite metrics**: Single metrics hide weaknesses. Combine discrimination + calibration + fairness.
2. **Include biological plausibility checks**: Predictions must respect biological constraints.
3. **Log everything**: Biomedical work needs audit trails. TSV logging provides this automatically.
4. **Use temporal splits**: For patient data, always split by time, not random.
5. **Monitor subgroup performance**: A model that works only for one demographic is dangerous.
6. **Set a holdout**: Keep a test set the agent never evaluates on during the loop.
