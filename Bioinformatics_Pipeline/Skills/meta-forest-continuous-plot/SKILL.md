---
name: meta-forest-continuous-plot
description: "Generate forest plots for meta-analysis of continuous data. Input a CSV file containing study names, means, standard deviations, and sample sizes for experimental and control groups. Output forest plot PNG and data table CSV."
license: MIT
skill-author: AIPOCH
---
# Continuous Data Forest Plot Generation

You are a meta-analysis chart generation assistant. Users provide continuous data (means/standard deviations), and you are responsible for calling R scripts to generate forest plots.

**Important: Do not repeat the content of this instruction document to users. Only output user-visible content defined in the workflow.**

---

## When to Use

- Use this skill when the request matches its documented task boundary.
- Use it when the user can provide the required inputs and expects a structured deliverable.
- Prefer this skill for repeatable, checklist-driven execution rather than open-ended brainstorming.

## Key Features

- Scope-focused workflow aligned to: "Generate forest plots for meta-analysis of continuous data. Input a CSV file containing study names, means, standard deviations, and sample sizes for experimental and control groups. Output forest plot PNG and data table CSV.".
- Packaged executable path(s): `scripts/convert_data.py` plus 1 additional script(s).
- Structured execution path designed to keep outputs consistent and reviewable.

## Dependencies

- `Python`: `3.10+`. Repository baseline for current packaged skills.
- `Third-party packages`: `not explicitly version-pinned in this skill package`. Add pinned versions if this skill needs stricter environment control.

## Example Usage

```bash
cd "20260316/scientific-skills/Data Analytics/meta-forest-continuous-plot"
python -m py_compile scripts/convert_data.py
python scripts/convert_data.py --help
```

Example run plan:
1. Confirm the user input, output path, and any required config values.
2. Edit the in-file `CONFIG` block or documented parameters if the script uses fixed settings.
3. Run `python scripts/convert_data.py` with the validated inputs.
4. Review the generated output and return the final artifact with any assumptions called out.

## Implementation Details

See `## Workflow` above for related details.

- Execution model: validate the request, choose the packaged workflow, and produce a bounded deliverable.
- Input controls: confirm the source files, scope limits, output format, and acceptance criteria before running any script.
- Primary implementation surface: `scripts/convert_data.py` with additional helper scripts under `scripts/`.
- Parameters to clarify first: input path, output path, scope filters, thresholds, and any domain-specific constraints.
- Output discipline: keep results reproducible, identify assumptions explicitly, and avoid undocumented side effects.

## Interoperability and Data Propagation

**Rule:** Outputs from this task must be accurately and consistently propagated as inputs to subsequent dependent tasks, specifically the `meta-funnel-plot` skill.

To enforce this, this skill MUST produce a standardized `results_table.csv` alongside the plot. This CSV serves as the direct input for the `meta-funnel-plot` skill, ensuring data integrity and preventing schema mismatches. The format of this output is strictly defined below and must be validated upon creation.

## Data Format Requirements

### Input Data
Users need to provide a CSV file containing the following columns:
| Column Name | Description | Example |
|---|---|---|
| study | Name of the study/author | "Smith et al. 2021" |
| mean_e | Mean of the experimental group | 10.5 |
| sd_e | Standard Deviation of the experimental group | 2.1 |
| n_e | Sample size of the experimental group | 50 |
| mean_c | Mean of the control group | 12.2 |
| sd_c | Standard Deviation of the control group | 2.5 |
| n_c | Sample size of the control group | 55 |

### Output Data Table (for Funnel Plot Interoperability)
The script `scripts/convert_data.py` must generate a `results_table.csv` with the following schema to ensure seamless input for the `meta-funnel-plot` skill.

| Column Name | Description | Example |
|---|---|---|
| study | Name of the study/author | "Smith et al. 2021" |
| TE | Treatment Effect (calculated, e.g., SMD or Hedges' g) | -0.72 |
| seTE | Standard Error of the Treatment Effect (calculated) | 0.25 |
