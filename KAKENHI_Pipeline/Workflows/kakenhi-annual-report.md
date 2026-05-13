---
description: KAKENHI grant lifecycle pipeline — report generation, figure integration, dual-agent review.
---

# `/kakenhi-annual-report` — KAKENHI Grant Lifecycle Workflow

> **Trigger**: `/kakenhi-annual-report`
> **Policies**: `grant_report_policy.md` (P1–P12), `fact_check_policy.md` (§1–§7)

## Required AROS Context

Before execution, load the companion reference guide:
- **KI**: `read_ki_document(ki_name="kakenhi_management_pipeline", document_path="artifacts/KAKENHI_Report_Reference.md")`
- **KIs**: `kakenhi_report_forms`, `kakenhi_e_application_system`, `publication_grant_map`
- **Skills**: `kakenhi-form-completion`, `researcher-data-collection`, `kakenhi-pre-award-forms`

## Pre-Conditions Checklist

Before executing any step, the agent MUST verify:

1. **Rule Verification**: Read all PDFs in `{GRANT_FOLDER}/Announcement_Rules/` — these are the absolute source of truth for all budget figures (Policy P7).
2. **Researcher Profile Freshness**: `ResearcherMetaInfo/{PI_FILE}.md` updated within 30 days (Policy P9). If stale → run **Step 0** first.
3. **Grant Folder Structure**: `{GRANT_FOLDER}/References/figures/` directory exists. If missing → create it.

## Step 0: Researcher Profile Refresh (Policy P9)

1. Check `{PI_FILE}.md` last-updated timestamp
2. If >30 days old → trigger **researcher-data-collection** skill
3. Run Crossref DOI verification for any new entries
4. Update `{PI_FILE}.md` + `{GRANT_ID}_Achievements_List.md` + `Publication_Grant_Map.md`
5. Cross-reference against KAKEN database: `https://kaken.nii.ac.jp/ja/grant/KAKENHI-PROJECT-{GRANT_ID}/`

## Step 1: Determine Report Type

```
Current FY = {REPORT_FISCAL_YEAR}
Is this the FINAL year of the grant?
  YES → Generate F-6-2 + F-7-2 → Also F-19-1 (if grant period ended)
  NO  → Generate F-6-1 + F-7-1
```

## Step 1.5: Index Announcement Rule PDFs

> **LAW 3 Enforcement**: Before extracting budget rules, all `Announcement_Rules/` PDFs must be processed.

1. Scan `{GRANT_FOLDER}/Announcement_Rules/` for any unindexed `.pdf` files.
2. Copy them to `00.RawData/Literature/02_Raw_PDFs/`.
3. Route them through the canonical parser:
   ```bash
   # // turbo
   python3 01.Shared_Assets/Skills/literature-ingestion/scripts/pdf_converter.py
   ```
4. Proceed to Step 2, reading from the parsed files in `03_Parsed_Markdown/`.

## Step 2: Extract Budget & Rules

From the resulting Markdown files in `00.RawData/Literature/03_Parsed_Markdown/` (originating from `{GRANT_FOLDER}/Announcement_Rules/`): extract budget by category (物品費, 旅費, 人件費・謝金, その他), indirect cost rate (30%), and special conditions. See **KI Reference §1** for detailed table format.

## Step 3: Collect Publications

1. Read `ResearcherMetaInfo/{PI_FILE}.md`, filter by fiscal year (Policy P1.2)
2. Classify by type: 雑誌論文, 学会発表, 図書, 産業財産権, ホームページ/ソフトウェア
3. Check grant attribution via `{GRANT_ID}_Achievements_List.md` (Policy P1.1)
4. Verify acknowledgments → assign 科研費謝辞: 有/無 (Policy P2)
5. Underline `{PI_NAME_EN}` in all author lists. See **KI Reference §6** for verification sequence.

## Step 4: Figure Extraction (Policy P10 — MANDATORY for F-19-1)

Every F-19-1 cf-19 MUST contain ≥1 visually verified figure. Run the automated pipeline:

```bash
python3 KAKENHI_Pipeline/KIs/kakenhi_management_pipeline/artifacts/Tools/process_figures.py auto \
  --grant-folder {GRANT_FOLDER} \
  --pi-names "{PI_NAME_EN_SURNAME}" \
  --grant-id {GRANT_ID} \
  --report-year {REPORT_FISCAL_YEAR}
```

This will: (1) find the PI's first-author paper PDF, (2) extract pages as PNGs to `figures/audit/`, (3) select and crop the key figure, (4) embed it in all 4 cf-19 files (.md + .docx × JP + EN), (5) write an audit log. See **KI Reference §4** for manual override sub-steps.

## Step 5: Generate F-6 (Financial Report)

Generate the appropriate financial report (F-6-1 or F-6-2). See **KI Reference §1** for field-level details and table templates. Draft file: `{GRANT_FOLDER}/Reports/{GRANT_ID}_{YYYY}_F-6-{1|2}_draft.md`

## Step 6: Generate F-7 (Research Report)

Generate the appropriate research report (F-7-1 or F-7-2). See **KI Reference §2** for character limits, byte-counting rules, and section structure. Draft file: `{GRANT_FOLDER}/Reports/{GRANT_ID}_{YYYY}_F-7-{1|2}_draft.md`

### Step 6a: Validate 研究実績の概要 Byte Count

The e-Rad F-7 field uses **byte-based counting** (全角=2, 半角=1, 改行=2). After drafting, verify:
- **Hard limit**: ≤800文字 (1600バイト), ≤5 line feeds
- **Warning threshold**: ≥1200バイト (below this triggers e-Rad warning)
- Run `Tools/erad_char_count.py --byte-mode` to validate

### Step 6b: Format ホームページ等 Entries

Each website entry in e-Rad requires a separate **タイトル (≤50文字)** and **URL** field. See **KI Reference §2.1**.
- Do NOT paste URLs or descriptions into the タイトル field
- Use the structured template format: `**(N)** → タイトル + URL`
- 備考 field: ≤200文字 (400バイト), max 2 line feeds

### Step 6c: Draft 次年度使用額 Section (if applicable)

When the grant has carryover funds (次年度使用額 > 0), draft the justification section. See **KI Reference §2.2**.
- Limit: ≤600文字 (1200バイト), max 3 line feeds
- Must include: 理由 (reason for unspent funds) + 使用計画 (specific usage plan)
- Confirm actual carryover amount with the researcher before finalizing

## Step 7: Generate F-19-1 cf-19 (if applicable)

Only when the grant period has fully ended. Must produce 4 output files (.md + .docx × JP + EN). See **KI Reference §3** for the full cf-19 specification, section structure, Word formatting code, and character limits.

## Step 8: Dual-Agent Review Gate (Policy P12 — MANDATORY)

All forms must pass 3 rounds of dual-agent review (6 dimensions, min 7/10 each). Hard cap at 5 rounds → escalate to human. Log to `{GRANT_ID}_{YYYY}_Review_Rounds_Log.md`. See **KI Reference §5** for the rubric.

## Step 9: Submit via 科研費電子申請システム

1. Login: https://www-shinsei.jsps.go.jp/
2. Navigate: 「交付内定・決定後の手続き」→ select grant → select form
3. Web entry + Word file upload (cf-19.docx, max 10MB)
4. Save confirmation PDF to `{GRANT_FOLDER}/Reports/`

## Step 10: Post-Submission KAKEN Verification (Policy P11.2)

After submission, verify publication counts match on KAKEN database. See **KI Reference §7** for the cross-check procedure.

## Step 11: Archive via /lab-commit

Delegate to the `/lab-commit` workflow to stage and commit all report drafts, figures, and references.
