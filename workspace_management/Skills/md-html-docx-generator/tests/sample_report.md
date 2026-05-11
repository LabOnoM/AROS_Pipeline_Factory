---
TITLE: "Sample Scientific Report"
AUTHOR: "Antigravity AI"
DATE: "2026-05-11"
---

## Introduction

This is a sample markdown document designed to test the chunking capabilities of the `md-html-docx-generator` skill. It contains standard elements like paragraphs, lists, and code.

We expect this section to be chunked into its own HTML block.

## Methodology

### Data Collection
Data was collected using a standard randomized block design.

> This is an important note regarding the data collection that should be styled as an alert block.

### Code Implementation

Here is a snippet of the data processing script:

```python
import pandas as pd

def process_data(df):
    return df.dropna().reset_index(drop=True)
```

## Results

The following table summarizes the primary outcomes:

| Metric | Baseline | Treatment | p-value |
|--------|----------|-----------|---------|
| Score A | 45.2 | 58.7 | <0.01 |
| Score B | 12.1 | 14.5 | 0.05 |
| Score C | 99.0 | 99.1 | 0.82 |

As seen in the table, the treatment effect is significant for Score A.

## Discussion

The results indicate that the chunking pipeline works effectively. Each section should now appear cleanly formatted in the final HTML document with the proper Huashu design classes applied.
