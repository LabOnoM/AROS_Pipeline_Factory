---
cpcp_asset: true
---
# Secure HTML Delivery Skill

Provides a standardized mechanism to generate AES-256 encrypted HTML reports (`build_secure_grant.py`) and generic interactive HTML reports (`generic_interactive_report.py`).

## Usage

1. Create generic interactive HTML report:
```bash
python ~/.gemini/antigravity/skills/secure-html-delivery/generic_interactive_report.py \
  --project-dir <path_to_project_root> \
  --funder-profile <path_to_funder_profile_json> \
  --output <path_to_output_html>
```

2. Encrypt the interactive report:
```bash
python ~/.gemini/antigravity/skills/secure-html-delivery/build_secure_grant.py \
  --input <path_to_output_html> \
  --output <path_to_secure_html> \
  --token "<PROJECT_SPECIFIC_TOKEN>"
```
