---
name: experimental-data-analysis
description: Perform statistical analysis on experimental data (descriptive stats, t-tests, ANOVA, multiple comparisons) when you need to interpret experimental results, assess statistical significance, or generate reproducible reports.
license: MIT
skill-author: AIPOCH
---

## When to Use

- You have experimental results in CSV format and need a reproducible end-to-end analysis workflow.
- You need to compare two conditions (independent or paired) using a t-test (or a non-parametric alternative when assumptions fail).
- You need to compare 3+ groups or multiple factors using one-way or multi-way ANOVA, including post-hoc multiple comparisons.
- You must generate report-ready outputs (tables/figures) including p-values, effect sizes, and assumption notes.
- You need strict execution hygiene where every run writes only into a timestamped run directory.

## Key Features

- **GEPA Error Prevention Rule (Pipeline Comprehensiveness):** To prevent incomplete or superficial analyses, the agent's output MUST comprehensively demonstrate a full data analysis pipeline. The final output must be a self-contained report detailing each of the following five phases, ensuring a clear narrative from raw data to final interpretation.

    ### Phase 1: Data Reception and Initial Assessment
    The agent must explicitly load the dataset and perform an initial structural assessment.
    - **1.1. Data Loading:** Clearly show the code used to load the data (e.g., `pd.read_csv`).
    - **1.2. Initial Inspection:** Display the initial rows (`.head()`), data types (`.info()`), and basic descriptive statistics (`.describe()`) of the raw data.
    - **1.3. Objective Statement:** State the primary analytical objective or hypothesis being investigated.

    ### Phase 2: Data Cleaning and Preparation
    The agent must document and execute necessary pre-processing steps.
    - **2.1. Missing Values:** Identify and report the strategy for handling any missing values (e.g., imputation, removal).
    - **2.2. Outlier Detection:** Describe the method used to detect potential outliers and the rationale for either retaining or excluding them.
    - **2.3. Data Transformation:** If applicable, perform and explain any required transformations (e.g., normalization, scaling, log transformation) to meet statistical assumptions.

    ### Phase 3: Exploratory Data Analysis (EDA)
    The agent must generate visualizations and summary statistics to explore the data's underlying structure.
    - **3.1. Univariate Analysis:** Visualize the distribution of key variables (e.g., histograms, box plots).
    - **3.2. Bivariate/Multivariate Analysis:** Generate plots (e.g., scatter plots, correlation heatmaps) to investigate relationships between variables relevant to the objective.
    - **3.3. Summarize EDA Findings:** Provide a brief textual summary of the key insights discovered during EDA.

    ### Phase 4: Formal Statistical Analysis
    The agent must perform the core statistical tests and validate their assumptions.
    - **4.1. Model/Test Selection:** Justify the choice of statistical test (e.g., t-test, ANOVA) based on the data structure and objective.
    - **4.2. Assumption Checking:** Explicitly test and report on the assumptions of the chosen statistical method (e.g., normality, homogeneity of variances).
    - **4.3. Execution and Results:** Execute the test and present the primary results, including the test statistic, p-value, effect size, and confidence intervals.

    ### Phase 5: Synthesis and Publication-Ready Outputs
    The agent must conclude the analysis with a clear interpretation and generate final, high-quality artifacts.
    - **5.1. Publication-Quality Visualizations:** Create polished plots with clear labels, titles, and annotations that effectively communicate the main findings.
    - **5.2. Summary Table:** Generate a concise table summarizing the key statistical results.
    - **5.3. Final Interpretation:** Provide a concluding paragraph that interprets the results in the context of the initial objective, states the final conclusion, and mentions any limitations of the analysis. This interpretation MUST adhere to the `textual-interpretability-policy`.

- **GEPA Error Prevention Rule (Analytical Robustness):** The agent must employ a comprehensive analytical approach, utilizing a diverse set of appropriate bioinformatics methods relevant to the data type and task.
- **GEPA Error Prevention Rule (Targeted Analysis):** The agent must enforce targeted, refined analyses on specific subsets of the data (e.g., particular cell types, genetic groups) to uncover nuanced insights, rather than relying solely on global, high-level comparisons.
- Reproducible run-based execution: each analysis is isolated under `outputs/runs/<timestamp>/`.
- Data preparation guidance: missing values, outliers, and variable type identification (continuous/categorical, grouping factors).
- Descriptive statistics: mean, standard deviation, confidence intervals, and grouped summary tables.
- Inferential statistics: independent/paired t-tests, ANOVA (one-way/multi-way), and post-hoc tests (e.g., Tukey).
- Reporting outputs: test statistics, p-values, effect sizes, charts/tables, and explicit assumption documentation.
- Built-in references for method selection and reporting templates:
  - `references/stats-method-selection.md`
  - `references/reporting-template.md`

## Dependencies

- Python 3.10+ (recommended)
- pandas >= 2.0
- numpy >= 1.24
- scipy >= 1.10

## Example Usage

### 1) Initialize a new run directory

```bash
python scripts/init_run.py
```

This creates a new directory like:

```text
outputs/runs/<timestamp>/
  config.json
  (sample input files, if provided by the initializer)
```

### 2) Run the analysis (descriptive stats + t-test/ANOVA)

```bash
python scripts/analyze_experiment.py
```

**Execution standard (required):**
- Run `python scripts/init_run.py` before each execution to generate `outputs/runs/<timestamp>/`.
- All intermediate files (config, inputs, outputs) must be written inside that run directory; writing elsewhere is prohibited.
- Scripts default to using the latest run directory under `outputs/runs/`.

## Implementation Details

### Workflow Stages

1. **Data Preparation**
   - Handle missing values and outliers.
   - Identify variable types:
     - continuous vs. categorical variables
     - grouping factors (e.g., treatment group, timepoint, subject ID)

2. **Descriptive Statistics**
   - Compute summary metrics such as:
     - mean, standard deviation
     - confidence intervals (CI)
   - Produce g
