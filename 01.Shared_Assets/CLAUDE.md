# Shared Assets Context (01.Shared_Assets)

## 🧭 Domain Context
This directory contains the canonical shared layer of the factory governed by the **Shared Asset Management System (SAMS)**. Assets here (KIs, Policies, Skills, Scripts) are consumed by multiple domain pipelines.

## ⚖️ Component Rules & Governance
1. **CPCP Enforcement (LAW 0)**: You MUST consult `00.RawData/SHARED_ASSET_REGISTRY.md` before altering anything here. You must evaluate the impact on ALL consuming pipelines.
2. **Frontmatter Standard**: All `SKILL.md` and Workflow files must contain CPCP-compliant YAML frontmatter (description ≤ 250 chars).
3. **No Local Variations**: If an asset requires pipeline-specific changes that break other pipelines, you must fork it to the consumer's pipeline directory.

## 🚀 Local Commands
- Run SAMS Audit: `python3 Scripts/audit_shared_assets.py`
- Deploy to AROS: `bash Scripts/sync_with_aros.sh push`
