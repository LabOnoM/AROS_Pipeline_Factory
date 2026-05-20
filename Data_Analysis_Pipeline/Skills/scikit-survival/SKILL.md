---
name: scikit-survival
description: Comprehensive toolkit for survival analysis and time-to-event modeling in Python. Use it to model censored time-to-event outcomes, fit Cox/RSF/GB models or Survival SVMs, evaluate with C-index/Brier score, and/or handle competing risks.
license: MIT
skill-author: AIPOCH
---
---

## Overview

scikit-survival is a Python library for survival analysis built on top of scikit-learn. It provides specialized tools for time-to-event analysis, handling the unique challenge of censored data.

Survival analysis aims to establish connections between covariates and the time of an event, accounting for censored records (particularly right-censored data from studies where participants don't experience events during observation periods).

## When to Use This Skill

Use this skill when you need to:

1.  Model **time-to-event outcomes with censoring** (right/left/interval censored observations).
2.  Fit and interpret **Cox Proportional Hazards** models (including **penalized** Cox for high-dimensional data).
3.  Train **non-linear survival models** such as **Random Survival Forests** or **Gradient Boosting** survival models.
4.  Use **Survival SVMs** for margin-based survival prediction (linear or kernel).
5.  Evaluate survival predictions with **censoring-aware metrics** (Uno/Harrell C-index, time-dependent AUC, Brier/Integrated Brier Score) and/or perform **competing risks** analysis.
6.  Perform non-parametric survival estimation (Kaplan-Meier, Nelson-Aalen).

## Core Capabilities

### 1. Model Types and Selection

scikit-survival provides multiple model families, each suited for different scenarios:

#### Cox Proportional Hazards Models
**Use for**: Standard survival analysis with interpretable coefficients
- `CoxPHSurvivalAnalysis`: Basic Cox model
- `CoxnetSurvivalAnalysis`: Penalized Cox with elastic net for high-dimensional data
- `IPCRidge`: Ridge regression for accelerated failure time models

#### Ensemble Methods
**Use for**: High predictive performance with complex non-linear relationships
- `RandomSurvivalForest`: Robust, non-parametric ensemble method
- `GradientBoostingSurvivalAnalysis`: Tree-based boosting for maximum performance
- `ComponentwiseGradientBoostingSurvivalAnalysis`: Linear boosting with feature selection
- `ExtraSurvivalTrees`: Extremely randomized trees for additional regularization

#### Survival Support Vector Machines
**Use for**: Medium-sized datasets with margin-based learning
- `FastSurvivalSVM`: Linear SVM optimized for speed
- `FastKernelSurvivalSVM`: Kernel SVM for non-linear relationships
- `HingeLossSurvivalSVM`: SVM with hinge loss
- `ClinicalKernelTransform`: Specialized kernel for clinical + molecular data

#### Model Selection Heuristics
- **High-dimensional (p > n)**: prefer `CoxnetSurvivalAnalysis` (Elastic Net) for stability and feature selection.
- **Interpretability required**: prefer `CoxPHSurvivalAnalysis` (coefficients as log hazard ratios).
- **Strong non-linearities / interactions**: prefer `RandomSurvivalForest` or `GradientBoostingSurvivalAnalysis`.
- **Kernelized decision boundaries**: consider `FastKernelSurvivalSVM` (ensure scaling).

### 2. Data Preparation and Preprocessing

Before modeling, properly prepare survival data:

#### Creating Survival Outcomes
```python
from sksurv.util import Surv

# From separate arrays
y = Surv.from_arrays(event=event_array, time=time_array)

# From DataFrame
y = Surv.from_dataframe('event', 'time', df)
```

#### Essential Preprocessing Steps
1. **Handle missing values**: Imputation strategies for features.
2. **Encode categorical variables**: One-hot encoding or label encoding.
3. **Standardize features**: Critical for SVMs and regularized Cox models.
4. **Validate data quality**: Check for non-negative times, and sufficient events per feature.
5. **Train-test split**: Maintain similar censoring rates across splits.

### 3. Model Evaluation

Proper evaluation is critical for survival models. Use appropriate metrics that account for censoring:

#### Concordance Index (C-index)
Primary metric for ranking/discrimination:
- **Harrell's C-index**: Use for low censoring (<40%)
- **Uno's C-index**: Use for moderate to high censoring (>40%) - more robust

```python
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw

# Harrell's C-index
c_harrell = concordance_index_censored(y_test['event'], y_test['time'], risk_scores)[0]

# Uno's C-index (recommended)
c_uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
```

#### Time-Dependent AUC
Evaluate discrimination at specific time points:

```python
from sksurv.metrics import cumulative_dynamic_auc

times = [365, 730, 1095]  # 1, 2, 3 years
auc, mean_auc = cumulative_dynamic_auc(y_train, y_test, risk_scores, times)
```

#### Brier Score
Assess both discrimination and calibration:

```python
from sksurv.metrics import integrated_brier_score

ibs = integrated_brier_score(y_train, y_test, survival_functions, times)
```

### 4. Competing Risks Analysis

Handle situations with multiple mutually exclusive event types:

```python
from sksurv.nonparametric import cumulative_incidence_competing_risks

# Estimate cumulative incidence for each event type
time_points, cif_event1, cif_event2 = cumulative_incidence_competing_risks(y)
```

**Use competing risks when**:
- Multiple mutually exclusive event types exist (e.g., death from different causes)
- Occurrence of one event prevents others
- Need probability estimates for specific event types

### 5. Non-parametric Estimation

Estimate survival functions without parametric assumptions:

#### Kaplan-Meier Estimator
```python
from sksurv.nonparametric import kaplan_meier_estimator

time, survival_prob = kaplan_meier_estimator(y['event'], y['time'])
```

#### Nelson-Aalen Estimator
```python
from sksurv.nonparametric import nelson_aalen_estimator

time, cumulative_hazard = nelson_aalen_estimator(y['event'], y['time'])
```

## Example Usage

A complete, runnable example using a scikit-survival built-in dataset, a scikit-learn pipeline, and Uno’s C-index (IPCW):

```python
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sksurv.datasets import load_breast_cancer
from sksurv.linear_model import CoxPHSurvivalAnalysis
from sksurv.metrics import concordance_index_ipcw, as_concordance_index_ipcw_scorer

# 1) Load data (X: features, y: structured array with fields like ('event', 'time'))
X, y = load_breast_cancer()

# 2) Split (keep y_train for IPCW-based metrics)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3) Build a pipeline (scaling is important for many survival models)
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("model", CoxPHSurvivalAnalysis()),
])

# 4) Optional: hyperparameter tuning (CoxPH has few knobs; shown for workflow completeness)
# If your version exposes regularization parameters, tune them here.
param_grid = {
    # Example placeholder; remove if unsupported in your installed version:
    # "model__alpha": [0.0, 1e-4, 1e-3]
}

if param_grid:
    search = GridSearchCV(
        pipe,
        param_grid=param_grid,
        scoring=as_concordance_index_ipcw_scorer(),
        cv=5,
        n_jobs=-1,
    )
    search.fit(X_train, y_train)
    best = search.best_estimator_
else:
    best = pipe.fit(X_train, y_train)

# 5) Predict risk scores (higher typically means higher risk / shorter survival)
risk_scores = best.predict(X_test)

# 6) Evaluate with Uno's C-index (IPCW)
c_uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
print(f"Uno's C-index (IPCW): {c_uno:.3f}")
```

## Implementation Details

### 1) Survival Target Representation (`Surv`)
scikit-survival expects outcomes as a **structured array** with at least:
- an **event indicator** (boolean)
- a **time** value (float/int)

Common construction patterns:

```python
from sksurv.util import Surv

y = Surv.from_arrays(event=event_array, time=time_array)
# or
y = Surv.from_dataframe("event", "time", df)
```

### 2) Evaluation Under Censoring
- **Harrell’s C-index** (`concordance_index_censored`): common, but can be less robust with heavy censoring.
- **Uno’s C-index** (`concordance_index_ipcw`): uses **inverse probability of censoring weights** and requires `y_train` to estimate censoring distribution.

```python
from sksurv.metrics import concordance_index_censored, concordance_index_ipcw

c_harrell = concordance_index_censored(y_test["event"], y_test["time"], risk_scores)[0]
c_uno = concordance_index_ipcw(y_train, y_test, risk_scores)[0]
```

### 3) Time-dependent Metrics (AUC, Brier/IBS)
- **Time-dependent AUC** evaluates discrimination at specific time horizons.
- **Brier score / Integrated Brier Score (IBS)** evaluates calibration + discrimination over time and requires survival probabilities/functions.

```python
from sksurv.metrics import cumulative_dynamic_auc

times = np.array([365, 730, 1095])  # example horizons
auc, mean_auc = cumulative_dynamic_auc(y_train, y_test, risk_scores, times)
```

### 4) Competing Risks (Cumulative Incidence)
Use competing risks methods when multiple mutually exclusive event types exist and one event prevents the others.

```python
from sksurv.nonparametric import cumulative_incidence_competing_risks

# y must encode event types appropriately for competing risks workflows
time_points, cif1, cif2 = cumulative_incidence_competing_risks(y)
```

## Dependencies

- `scikit-survival` (recommended: `>=0.22`)
- `scikit-learn` (recommended: `>=1.2`)
- `numpy` (recommended: `>=1.23`)
- `pandas` (recommended: `>=1.5`)

## Additional Resources

- **Official Documentation**: https://scikit-survival.readthedocs.io/
- **GitHub Repository**: https://github.com/sebp/scikit-survival
- **Built-in Datasets**: Use `sksurv.datasets` for practice datasets (GBSG2, WHAS500, veterans lung cancer, etc.)
- **API Reference**: Complete list of classes and functions at https://scikit-survival.readthedocs.io/en/stable/api/index.html

## Quick Reference: Key Imports

```python
# Models
from sksurv.linear_model import CoxPHSurvivalAnalysis, CoxnetSurvivalAnalysis, IPCRidge
from sksurv.ensemble import RandomSurvivalForest, GradientBoostingSurvivalAnalysis
from sksurv.svm import FastSurvivalSVM, FastKernelSurvivalSVM
from sksurv.tree import SurvivalTree

# Evaluation metrics
from sksurv.metrics import (
    concordance_index_censored,
    concordance_index_ipcw,
    cumulative_dynamic_auc,
    brier_score,
    integrated_brier_score,
    as_concordance_index_ipcw_scorer,
    as_integrated_brier_score_scorer
)

# Non-parametric estimation
from sksurv.nonparametric import (
    kaplan_meier_estimator,
    nelson_aalen_estimator,
    cumulative_incidence_competing_risks
)

# Data handling
from sksurv.util import Surv
from sksurv.preprocessing import OneHotEncoder, encode_categorical
from sksurv.datasets import load_gbsg2, load_breast_cancer, load_veterans_lung_cancer

# Kernels
from sksurv.kernels import ClinicalKernelTransform