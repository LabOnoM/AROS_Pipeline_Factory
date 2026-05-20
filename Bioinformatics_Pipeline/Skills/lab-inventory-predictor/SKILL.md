---
name: lab-inventory-predictor
description: Predict depletion time of critical lab reagents based on historical usage frequency, and automatically generate purchase alerts when stock falls below safety thresholds.
license: MIT
skill-author: AIPOCH
status: beta
version: 2.0
GEPA-Compliant: true
---
# Lab Inventory Predictor

Predicts reagent depletion time by analyzing historical usage frequency, and automatically generates reminders when purchases are needed. This skill complies with the GEPA rule for explicit dependency and input validation.

## Inputs

This skill requires structured data about lab reagent inventory.

- **`--action`** (string, required): The operation to perform. One of `status`, `predict`, `report`.
- **`--data`** (filepath, required): Path to the inventory data file (CSV or JSON). The file must contain `reagent_id`, `current_stock_ml`, `last_updated`, and `usage_history` columns.
- **`--reagent-id`** (string, optional): The specific reagent to analyze. If not provided, the skill will analyze all reagents in the data file.
- **`--safety-threshold`** (float, optional, default: 0.2): The stock level (as a percentage) at which to trigger a purchase alert.

## Dependencies

- **Python Version:** 3.8+ (due to use of the `dataclasses` module).
- **Python Libraries:** None. This script uses only the standard library (`csv`, `json`, `datetime`, `sys`, `argparse`).
- **System Packages:** None.
- **Environment Variables:** None.

## Validation Logic

The script (`scripts/main.py`) performs the following checks at runtime before execution:

1.  **Python Version Check:** The script immediately exits with an error if the Python version is less than 3.8.
    ```python
    if sys.version_info < (3, 8):
        sys.exit("Error: Python 3.8+ is strictly required for this script.")
    ```
2.  **Input Parameter Validation:**
    - Uses the `argparse` library to ensure that the required `--action` and `--data` parameters are provided. If they are missing, `argparse` automatically shows a help message and exits.
    - The `--action` parameter is validated to be one of the allowed choices.
3.  **File Existence:** The script checks if the file provided via the `--data` parameter actually exists. If not, it exits with a clear error message: `Error: Data file not found at <path>`.

If any of these checks fail, the script will not proceed with the main workflow, preventing unexpected errors. Instead, it provides a clear, actionable error message as mandated by the `agent-communication` policy.

## Quick Check

```bash
# Check for syntax errors
python -m py_compile scripts/main.py

# View help and all required inputs
python scripts/main.py --help

# Run a status check (will fail if data file is missing, demonstrating validation)
python scripts/main.py --action status --data /path/to/your/data.csv
```

## Workflow

1.  **Validate Inputs and Dependencies:** Confirm that all requirements are met using the built-in validation logic.
2.  **Process Data:** Read and parse the inventory data file.
3.  **Perform Action:** Execute the requested action (`status`, `predict`, or `report`).
4.  **Return Structured Result:** Output the results in the specified format (text, JSON, or CSV).
