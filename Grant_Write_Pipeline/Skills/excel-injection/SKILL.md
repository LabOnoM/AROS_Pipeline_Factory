# Excel Injection Skill

Provides a Python script `generic_inject_excel.py` to inject generated markdown files (from `GrantDraftElements/`) into a formal Excel application form. This standardizes the final deliverable without needing to rewrite python scripts from scratch for each project.

## Usage
When the workflow reaches the Phase 6 Delivery phase and the funder profile indicates `submission_format: "xlsx"`, run:

```bash
python ~/.gemini/antigravity/skills/excel-injection/generic_inject_excel.py \
  --project-dir <path_to_project_root> \
  --funder-profile <path_to_funder_profile_json> \
  --template <path_to_empty_template_xlsx>
```
