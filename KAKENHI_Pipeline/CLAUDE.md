# KAKENHI Pipeline Context

## 🧭 Domain Context
This pipeline handles the specific JSPS KAKENHI lifecycle, including F-7 annual reports, compliance forms, and JSPS-specific grant management.

## ⚖️ Component Rules
- **Fact-Checking**: Heavily references the `fact_check_policy.md` and relies on `/wiki-build` to pull accurate publication lists.
- **Funder Alignment**: Follows the JSPS e-Rad system structures and JSPS guidelines explicitly.

## 🚀 Execution
- **Trigger**: The `/kakenhi-annual-report` workflow governs generation here.
