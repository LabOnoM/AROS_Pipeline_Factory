# SPEC: KAKENHI Grant Lifecycle Management System (KAKENHI_Pipeline)

> **Version**: 2.0.0
> **Status**: Canonical
> **Scope**: Universal — applicable to any JSPS KAKENHI researcher, any research field, any grant category

---

## 1. Introduction

`KAKENHI_Pipeline` is a reusable, researcher-agnostic framework for managing the entire lifecycle of JSPS KAKENHI grants — from pre-award application through final post-grant reporting (F-19-1). It is designed to be **instantiated per researcher** while keeping all operational logic, skills, and policies generic and project-independent.

### 1.1 Design Philosophy

| Principle | Implementation |
|-----------|---------------|
| **Generic** | Zero hardcoded researcher names, grant IDs, or institution data |
| **Parameterized** | All researcher/grant data injected at runtime via `{PLACEHOLDER}` variables |
| **Auditable** | Every generated document has a traceable provenance chain |
| **Visual-first** | F-19-1 cf-19 forms MUST contain at least one figure |
| **Bilingual** | All output forms produced in both Japanese and English |

### 1.2 Objectives
- Ensure absolute compliance with JSPS regulations and funding constraints for any grant
- Automate factual data collection while preventing hallucinations
- Guarantee visual and factual integrity of all generated reporting documents
- Provide systematic dual-agent review processes
- Serve as a AROS-publishable skill/workflow/policy set

---

## 2. Runtime Variables

Before executing any workflow, the caller MUST populate these variables from the target researcher's `ResearcherMetaInfo/{PI_FILE}.md` and the grant's `Announcement_Rules/`:

| Variable | Source | Example |
|----------|--------|---------|
| `{PI_NAME_EN}` | ResearcherMetaInfo | `Weng Yao` |
| `{PI_NAME_JP}` | ResearcherMetaInfo | `翁 瑶` |
| `{PI_RESEARCHER_NO}` | ResearcherMetaInfo | `1000001000108` |
| `{PI_INSTITUTION_JP}` | ResearcherMetaInfo | `岡山大学` |
| `{PI_INSTITUTION_CODE}` | ResearcherMetaInfo | `15301` |
| `{PI_RESEARCHMAP_URL}` | ResearcherMetaInfo | `https://researchmap.jp/wyao` |
| `{PI_ORCID}` | ResearcherMetaInfo | `0000-0003-2455-9346` |
| `{GRANT_ID}` | Announcement_Rules | `24K23552` |
| `{GRANT_TYPE}` | Announcement_Rules | `研究活動スタート支援` |
| `{GRANT_TITLE_JP}` | Announcement_Rules | `骨芽細胞分化における...` |
| `{GRANT_START_DATE}` | Announcement_Rules | `2024/07` |
| `{GRANT_END_DATE}` | Announcement_Rules | `2026/03` |
| `{DIRECT_COST_TOTAL}` | Announcement_Rules | `¥2,200,000` |
| `{INDIRECT_COST_TOTAL}` | Announcement_Rules | `¥660,000` |
| `{REPORT_FISCAL_YEAR}` | Context | `2025` |
| `{GRANT_FOLDER}` | Context | `2024startup` |

---

## 3. System Architecture

```
KAKENHI_Pipeline/
├── SPEC.md                              ← This document (normative)
├── README.md                            ← Human-readable overview & grant folder spec
├── Workflows/
│   └── KAKENHI_annual_report_pipeline.md ← Full lifecycle workflow (trigger: /kakenhi-annual-report)
├── Skills/
│   ├── kakenhi-form-completion/         ← F-6/F-7/F-19 text generation
│   ├── researcher-data-collection/      ← 3-tier profile refresh
│   └── kakenhi-pre-award-forms/         ← D-series, F-2 forms
├── Policies/
│   ├── grant_report_policy.md           ← P1–P12 compliance rules
│   └── fact_check_policy.md             ← Metadata verification rules
├── KIs/
│   ├── kakenhi_e_application_system/    ← e-Rad system guidance + PDF manuals
│   ├── kakenhi_report_forms/            ← Form codes, cf-19.docx template
│   └── publication_grant_map/           ← Generic attribution map structure
├── Templates/                           ← Empty scaffold files for new projects
│   ├── ResearcherMetaInfo_TEMPLATE.md   ← Researcher profile shell
│   ├── Publication_Grant_Map_TEMPLATE.md ← Cross-grant attribution matrix
│   ├── XXKXXXXX_Achievements_List.md    ← Per-grant achievement isolation list
│   ├── Metadata_Verification_TEMPLATE.md ← Crossref DOI audit trail
│   └── Review_Rounds_Log_TEMPLATE.md    ← Dual-agent review log
└── Tools/
    └── process_figures.py               ← Generic PDF figure extraction & auto-crop
```

---

## 4. Grant Folder Canonical Structure

Each active grant managed under this pipeline MUST follow this directory structure exactly.

```
{GRANT_FOLDER}/                          ← Named by researcher (e.g., "2024startup")
├── Announcement_Rules/                  ← 使用ルール PDF + 交付決定通知書 PDF
├── Application/                         ← Original 申請書 and supporting docs
├── Management/                          ← Internal tracking, cf-19.docx local copy
├── References/
│   ├── paper/                           ← Published paper PDFs (cited in reports)
│   ├── 学会/                             ← Conference materials (by event folder)
│   │   └── {YYYY}_{ConferenceName}/     ← e.g., 2024第66回歯科基礎医学会学術大会
│   ├── figures/                         ← ← MANDATORY for F-19-1 cf-19
│   │   ├── {FigureN}_{Label}.png        ← Named, cropped key figures
│   │   └── audit/                       ← ← All PDF pages as PNGs (audit trail)
│   │       └── audit_log.md             ← Source PDF, page, method, verification
│   ├── {GRANT_ID}_Achievements_List.md  ← ← Copied from Templates/XXKXXXXX_Achievements_List.md
│   └── Metadata_Verification.md         ← ← Copied from Templates/
└── Reports/
    ├── cf-19.docx                       ← Official JSPS blank template (do not edit)
    ├── {GRANT_ID}_{YYYY}_D-2-1.pdf      ← Submitted PDFs
    ├── {GRANT_ID}_{YYYY}_D-4-1.pdf
    ├── {GRANT_ID}_{YYYY}_F-6-1.pdf
    ├── {GRANT_ID}_{YYYY}_F-7-1.pdf
    ├── {GRANT_ID}_{YYYY}_F-2-1.pdf
    ├── {GRANT_ID}_{YYYY}_F-6-2_draft.md ← Working draft (Japanese)
    ├── {GRANT_ID}_{YYYY}_F-7-2_draft.md
    ├── {GRANT_ID}_{YYYY}_F-19-1-cf-19_draft.md     ← JP cf-19 (source of truth)
    ├── {GRANT_ID}_{YYYY}_F-19-1-cf-19_draft_en.md  ← EN cf-19 (internal ref)
    ├── {GRANT_ID}_{YYYY}_F-19-1-cf-19_draft.docx   ← JP Word with figures (JSPS upload)
    ├── {GRANT_ID}_{YYYY}_F-19-1-cf-19_draft_en.docx ← EN Word
    └── {GRANT_ID}_{YYYY}_Review_Rounds_Log.md       ← Dual-agent audit trail
```

> [!IMPORTANT]
> The `figures/` subdirectory under `References/` is **not optional**. Every F-19-1 report MUST have at least one figure visually verified and embedded in the cf-19 .docx. Missing figures will cause automatic review failure.

---

## 5. Component Contracts

### 5.1 Workflows
- **KAKENHI_annual_report_pipeline.md**: The canonical orchestrator. Trigger with `/kakenhi-annual-report`. It calls Skills and enforces Policies sequentially. It MUST NOT contain hardcoded researcher data.

### 5.2 Skills
Each skill MUST:
- Accept `{VARIABLE}` placeholders as input parameters
- Read researcher data from `ResearcherMetaInfo/{PI_FILE}.md` (provided at call time)
- Reference `{GRANT_FOLDER}/Announcement_Rules/` for grant-specific constraints
- Never write hardcoded names, IDs, or URLs for specific individuals

### 5.3 Policies
- All policies use `{GRANT_ID}`, `{PI_NAME_EN}`, etc. in examples
- Specific grant IDs or researcher names appear only in non-normative examples wrapped in `>` blockquotes with the label `[EXAMPLE - NOT NORMATIVE]`

### 5.4 Templates
- All template files contain ONLY structural scaffolding
- All data fields use `{PLACEHOLDER}` syntax
- Templates are copied (not symlinked) into the `{GRANT_FOLDER}/References/` on project onboarding

---

## 6. Cross-Platform Compatibility

### 6.1 File Paths
- Absolute paths MUST NOT be hardcoded in executable scripts
- Use `os.path.join()` or `pathlib.Path` for dynamic resolution in Python
- Markdown documents should use relative paths from the project root

### 6.2 Encodings
- All text files: strictly `UTF-8`
- Python scripts: `encoding="utf-8"` explicitly declared in all open() calls

### 6.3 Line Endings
- All markdown and config files: Unix-style `\n` line endings

---

## 7. Review & Governance

All outputs generated through this pipeline are subject to the **Mandatory Dual-Agent Review Gate** (Policy P12):
- Minimum score: **7/10** across six dimensions
- Maximum revision rounds: **5**
- Review log: mandatory `{GRANT_ID}_{YYYY}_Review_Rounds_Log.md`

---

## 8. AROS Integration

This pipeline is synced to the AROS ecosystem at:
```
Skills/     → ~/.gemini/skills/
Workflows/  → ~/.gemini/antigravity/global_workflows/
Policies/   → ~/.gemini/antigravity/policies/
KIs/        → ~/.gemini/antigravity/knowledge/
```

The sync script is run via `/lab-commit` after any pipeline update.

---

## 9. Security & Workspace Governance

- **Decoupled Metadata**: All researcher-specific data (`ResearcherMetaInfo/` and `{GRANT_ID}_Achievements_List.md`) lives at the **project root** or in the `{GRANT_FOLDER}/References/`, never inside `KAKENHI_Pipeline/`
- **Ephemeral Scripting**: All scratch/debug scripts → `~/.gemini/antigravity/brain/.../scratch/`
- **Immutable Templates**: Files in `Templates/` must not be edited in-place; copy first, then customize

---

*Last Updated: 2026-05-11 | KAKENHI_Pipeline v2.0.0*
