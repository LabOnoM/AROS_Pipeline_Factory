---
name: clinical-data-cleaner
description: Cleans and standardizes clinical trial data for regulatory compliance with audit trails. Supports cleaning data, preparing for FDA/EMA submission, standardizing SDTM datasets, handling missing values, detecting outliers, or converting raw CRF data to CDISC format.
license: MIT
skill-author: AIPOCH
---
# Clinical Data Cleaner

Clean, validate, and standardize clinical trial data to meet CDISC SDTM standards for regulatory submissions to FDA or EMA.

## When to Use

- When cleaning clinical trial data.
- When preparing data for FDA/EMA submission.
- When standardizing SDTM datasets.
- When handling missing values in clinical studies.
- When detecting outliers in lab results.
- When converting raw CRF data to CDISC format.
- For data analysis tasks requiring explicit assumptions, a bounded scope, and reproducible output.
- When a documented fallback path is needed for missing inputs or execution errors.

## Key Features

- Scope-focused workflow aligned to CDISC SDTM standards.
- Packaged executable path: `scripts/main.py`.
- Reference material in `references/` for task-specific guidance.
- Structured execution path for consistent and reviewable outputs.

## Dependencies

- `Python`: `3.10+`
- `numpy`: Declared in `requirements.txt`.
- `pandas`: Declared in `requirements.txt`.
- `scipy`: Declared in `requirements.txt`.

## Example Usage

```bash
cd "20260318/scientific-skills/Data Analytics/clinical-data-cleaner"
python -m py_compile scripts/main.py
python scripts/main.py --help
```

Example run plan:
1. Confirm the user input, output path, and any required config values.
2. Edit the in-file `CONFIG` block or documented parameters if the script uses fixed settings.
3. Run `python scripts/main.py` with the validated inputs.
4. Review the generated output and return the final artifact, noting any assumptions.

## Implementation Details

- Execution model: Validate the request, choose the packaged workflow, and produce a bounded deliverable.
- Input controls: Confirm source files, scope limits, output format, and acceptance criteria.
- Primary implementation surface: `scripts/main.py`.
- Reference guidance: `references/` contains supporting rules, prompts, or checklists.
- Parameters to clarify first: input path, output path, scope filters, thresholds, and domain-specific constraints.
- Output discipline: Keep results reproducible, identify assumptions explicitly, and avoid undocumented side effects.

## Quick Check

Verify the packaged script entry point can be parsed before deeper execution.

```bash
python -m py_compile scripts/main.py
```

## Audit-Ready Commands

Use these commands for validation.

```bash
python -m py_compile scripts/main.py
python scripts/main.py --help
python scripts/main.py --input "Audit validation sample with explicit symptoms, history, assessment, and next-step plan."
```

## Workflow

1. Confirm the user objective, required inputs, and constraints.
2. Validate the request matches the documented scope. Stop if the task requires unsupported assumptions.
3. Use the packaged script path with available inputs.
4. Return a structured result that separates assumptions, deliverables, risks, and unresolved items.
5. If execution fails or inputs are incomplete, switch to the fallback path and state what blocked full completion.

## Quick Start

```python
from scripts.main import ClinicalDataCleaner

# Initialize for Demographics domain
cleaner = ClinicalDataCleaner(domain='DM')

# Clean data with default settings
cleaned = cleaner.clean(raw_data)

# Save with audit trail
cleaner.save_report('output.csv')
```

## Core Capabilities

### 1. SDTM Domain Validation

```python
cleaner = ClinicalDataCleaner(domain='DM')  # or 'LB', 'VS'
is_valid, missing = cleaner.validate_domain(data)
```

**Required Fields:**
- **DM**: STUDYID, USUBJID, SUBJID, RFSTDTC, RFENDTC, SITEID, AGE, SEX, RACE
- **LB**: STUDYID, USUBJID, LBTESTCD, LBCAT, LBORRES, LBORRESU, LBSTRESC, LBDTC
- **VS**: STUDYID, USUBJID, VSTESTCD, VSORRES, VSORRESU, VSSTRESC, VSDTC

### 2. Missing Value Handling

```python
cleaner = ClinicalDataCleaner(
    domain='DM',
    missing_strategy='median'  # mean, median, mode, forward, drop
)
cleaned = cleaner.handle_missing_values(data)
```

### 3. Outlier Detection

```python
cleaner = ClinicalDataCleaner(
    domain='LB',
    outlier_method='domain',  # iqr, zscore, domain
    outlier_action='flag'     # flag, remove, cap
)
flagged = cleaner.detect_outliers(data)
```

**Clinical Thresholds:**
| Parameter | Range | Unit |
|-----------|-------|------|
| Glucose | 50-500 | mg/dL |
| Hemoglobin | 5-20 | g/dL |
| Systolic BP | 70-220 | mmHg |

### 4. Date Standardization

```python
standardized = cleaner.standardize_dates(data)

# Converts to ISO 8601: 2023-01-15T09:30:00
```

### 5. Complete Pipeline

```python
cleaner = ClinicalDataCleaner(
    domain='DM',
    missing_strategy='median',
    outlier_method='iqr',
    outlier_action='flag'
)
cleaned_data = cleaner.clean(data)
cleaner.save_report('output.csv')
```

**Output Files:**
- `output.csv` - Cleaned SDTM data
- `output.report.json` - Audit trail for regulatory submission

## CLI Usage

```text
# Clean demographics
python scripts/main.py \
  --input dm_raw.csv \
  --domain DM \
  --output dm_clean.csv \
  --missing-strategy median \
  --outlier-method iqr \
  --outlier-action flag

# Clean lab data with clinical thresholds
python scripts/main.py \
  --input lb_raw.csv \
  --domain LB \
  --output lb_clean.csv \
  --outlier-method domain
```

## Common Patterns

See [references/common-patterns.md](references/common-patterns.md) for detailed examples:
- Regulatory Submission Preparation
- Interim Analysis Data Preparation
- Database Migration Cleanup
- External Lab Data Integration

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for solutions to:
- Validation failures
- Date parsing errors
- Memory errors with large datasets
- Outlier detection issues

## Quality Checklist

**Pre-Cleaning:**
- [ ] IACUC approval obtained (animal studies)
- [ ] Sample size adequately powered
- [ ] Randomization method documented

**Post-Cleaning:**
- [ ] Validate against CDISC SDTM IG
- [ ] Review all cleaning actions in audit trail
- [ ] Test import to analysis software

## References

- `references/sdtm_ig_guide.md` - CDISC SDTM Implementation Guide
- `references/domain_specs.json` - Domain-specific field requirements
- `references/outlier_thresholds.json` - Clinical outlier thresholds
- `references/common-patterns.md` - Detailed usage patterns
- `references/troubleshooting.md` - Problem-solving guide

---

**Skill ID**: 189 | **Version**: 2.0 | **License**: MIT

## Output Requirements

Every final response should make these items explicit when relevant:

- Objective or requested deliverable
- Inputs used and assumptions introduced
- Workflow or decision path
- Core result, recommendation, or artifact
- Constraints, risks, caveats, or validation needs
- Unresolved items and next-step checks

## Error Handling

- If required inputs are missing, state which fields are missing and request the minimum information needed.
- If the task is outside the documented scope, stop and explain the limitation.
- If `scripts/main.py` fails, report the failure point, summarize what can be completed, and provide a manual fallback if available.
- Do not fabricate files, citations, data, search results, or execution outcomes.

## Input Validation

This skill accepts requests that match its documented purpose and include sufficient context for safe completion.

Do not continue if the request is out of scope, missing a critical input, or requires unsupported assumptions. Respond:

> `clinical-data-cleaner` only handles its documented workflow. Please provide the missing required inputs or switch to a more suitable skill.

## Response Template

Use the following structure for non-trivial requests:

1. Objective
2. Inputs Received
3. Assumptions
4. Workflow
5. Deliverable
6. Risks and Limits
7. Next Checks

For simple requests, the structure can be compressed, but assumptions and limits should be explicit when they affect correctness.