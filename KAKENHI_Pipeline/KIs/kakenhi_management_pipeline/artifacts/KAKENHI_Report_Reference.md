# KAKENHI Report Reference Guide

> This document is the companion reference for the `/kakenhi-annual-report` workflow.
> The workflow reads this document via `read_ki_document(ki_name="kakenhi_management_pipeline", document_path="artifacts/KAKENHI_Report_Reference.md")`.

---

## 1. F-6 Financial Report Details

### F-6-1 (Non-final year: 収支状況報告書)

Fill via e-Rad web form:
- Column 1: 前年度から繰越した助成金 (carry-over from previous year, if any)
- Column 2: 当該年度に交付された助成金 (grant amount for this FY from 交付決定通知書)
- Column 3: 支出した助成金合計 (actual expenditure — researcher provides receipts)
- Column 4: 翌年度に繰り越す助成金 = Column 1 + Column 2 - Column 3

### F-6-2 (Final year: 収支決算報告書)

Full-period settlement table:

| 費目 | FY{N} 予算額 | FY{N} 使用額 | FY{N+1} 予算額 | FY{N+1} 使用額 | 合計使用額 |
|------|------------|------------|---------------|--------------|---------|
| 物品費 | ¥{AMOUNT} | ¥{ACTUAL} | ¥{AMOUNT} | ¥[PENDING] | ¥{TOTAL} |
| 旅費  | ¥{AMOUNT} | ¥{ACTUAL} | ¥{AMOUNT} | ¥[PENDING] | ¥{TOTAL} |
| 人件費・謝金 | ¥0 | ¥0 | ¥0 | ¥0 | ¥0 |
| その他 | ¥{AMOUNT} | ¥{ACTUAL} | ¥{AMOUNT} | ¥[PENDING] | ¥{TOTAL} |

間接経費 = Direct Cost × 0.30 (managed by institution).

---

## 2. F-7 Research Report Details

### e-Rad Byte-Counting Rule for F-7 Forms (Calibrated 2026-05-11)

> **CRITICAL**: Unlike F-19-1 fields (which count visible characters), the F-7 研究実績の概要 field
> uses **byte-based counting**: 全角=2バイト, 半角=1バイト, 改行=2バイト.
> Maximum: **800文字 (1600バイト)**. Maximum line feeds: **5回**.
> **Warning threshold**: The e-Rad system displays a warning if the field is **≤1200バイト**.
> Target: 600–800 文字 (1200–1600 バイト) to avoid the warning.
> Use `Tools/erad_char_count.py --byte-mode` for F-7 validation.

### F-7-1 (Non-final: 研究実施状況報告書)

- **研究実績の概要** (≤800文字 / 1600バイト, byte-counted): Progress summary, methods, results, future plans, self-assessment
- **研究発表**: Publication list for this fiscal year only
- **ホームページ等 (Websites/Software)**: See §2.1 below for e-Rad form structure
- **次年度使用額が生じた理由と使用計画**: See §2.2 below (required when carryover > 0)
- Self-assessment: おおむね順調 / やや遅れている / 遅れている

### F-7-2 (Final: 研究実績報告書)

- **【研究実績の概要】 (Summary of Research Achievements)**: ≤800文字 (1600バイト, byte-counted), max 5 line feeds. A cohesive narrative summarizing the results of the final year and the entire research period, addressing the "Purpose of the research" and "Research plan". Include future outlook if necessary. **Target ≥1200バイト to avoid e-Rad warning.**
- **【キーワード】 (Keywords)**: 1 to 8 keywords representing the research. Avoid chemical formulas or math expressions.
- **研究発表**: Complete publication list for entire grant period.
- **ホームページ等 (Websites/Software)**: See §2.1 below for e-Rad form structure
- **次年度使用額が生じた理由と使用計画**: See §2.2 below (required when carryover > 0)
- *Note*: Ensure that the draft is consolidated so it easily pastes into the single web form text box.

### §2.1 ホームページ等 (Websites/Software) — e-Rad Form Structure

The e-Rad system provides **5 entry slots** for websites/software. Each slot has:

| Field | Limit | Notes |
|-------|-------|-------|
| **タイトル (Title)** | **≤50文字** | Short descriptive title — NOT the URL or long description |
| **URL** | Free text | Full URL to the resource |

Additionally, a shared **備考 (Remarks)** field is provided:

| Field | Limit | Max Line Feeds | Notes |
|-------|-------|----------------|-------|
| **備考** | **≤200文字 (400バイト)** | 2 | Supplementary notes for all entries |

**Template format for drafts:**
```markdown
### ホームページ等 (Websites/Software)

**(1)**
- **タイトル**: [短いタイトル ≤50文字]
- **URL**: [https://...]

**(2)**
- **タイトル**: [短いタイトル ≤50文字]
- **URL**: [https://...]

**備考 (Remarks)**:
(1) [supplementary note]. (2) [supplementary note].
```

> **⚠️ ERROR PREVENTION**: Do NOT paste URLs or long descriptions into the タイトル field.
> The e-Rad system will reject titles exceeding 50 characters with: `Error:webページ（タイトル）1行目は50文字以内で入力してください。`

### §2.2 次年度使用額が生じた理由と使用計画 (Carryover Justification)

This section is **required** when the 「次年度使用額（B-A）」column is greater than zero.

| Field | Limit | Max Line Feeds | Notes |
|-------|-------|----------------|-------|
| **次年度使用額が生じた理由と使用計画** | **≤600文字 (1200バイト)** | 3 | Byte-counted (全角=2, 半角=1, 改行=2) |

The text should cover:
1. **理由 (Reason)**: Why the funds were not fully expended (e.g., equipment procurement delays, experimental timeline shifts)
2. **使用計画 (Usage Plan)**: Specific items the carryover will fund in the next fiscal year, combined with the next year's allocation

> **⚠️ NOTE**: If carryover is ¥0, this field does not need to be filled. The agent must check with the researcher for actual carryover amounts before drafting.

---

## 3. F-19-1 cf-19 (研究成果報告内容ファイル) — Full Specification

> **Trigger**: Only when the grant period has fully ended
> **Register**: Public-facing (「社会・国民にわかりやすく」— Policy P8.3)

### Required Output Files (ALL FOUR are mandatory)

| File | Format | Language | Purpose |
|------|--------|----------|---------|
| `{GRANT_ID}_{YYYY}_F-19-1-cf-19_draft.md` | Markdown | Japanese | **Source of truth** |
| `{GRANT_ID}_{YYYY}_F-19-1-cf-19_draft_en.md` | Markdown | English | Internal reference |
| `{GRANT_ID}_{YYYY}_F-19-1-cf-19_draft.docx` | Word | Japanese | **JSPS upload file** |
| `{GRANT_ID}_{YYYY}_F-19-1-cf-19_draft_en.docx` | Word | English | Internal reference |

### Web Entry Fields (e-Rad system)

In addition to uploading the cf-19 Word document, the following text fields must be prepared for direct entry into the e-Rad web system.

> **Counting Rule (calibrated 2026-05-11):** The e-Rad "入力文字数" counts each **visible character as 1** regardless of byte width (全角=1, 半角=1). Line feeds are NOT counted toward the total but are limited separately. Use `Tools/erad_char_count.py` to verify.

| Field | Limit | Max Line Feeds | Notes |
|-------|-------|----------------|-------|
| 研究成果の概要（和文） | **300 chars** | 2 | Plain language for the general public |
| 研究成果の概要（英文） | **1000 chars** | 2 | Plain language for the general public |
| 研究成果の学術的意義や社会的意義 | **300 chars** | 2 | Academic + societal impact |
| 研究分野 | — | — | e.g., 骨代謝学, 細胞生物学 |
| キーワード | 1–8 items | — | No chemical/mathematical formulas |

> **⚠️ JIS X0208 Encoding Constraint:** The e-Rad system only accepts characters within the JIS X0208 standard. Non-JIS characters (em-dash `—`, smart quotes `""''`, etc.) are silently converted to `&#xxxx;` HTML entities, causing a red warning. **For English text, use only ASCII printable characters.** Run `Tools/erad_char_count.py --check-jis` to validate.

### cf-19 Section Structure

**1. 研究開始当初の背景** (Background at the Start of Research)
- Prior art and knowledge gap
- Applicant's own preliminary findings
- Numbered literature citations (①②③...)

**2. 研究の目的** (Purpose of Research)
- Numbered objectives (typically 2–4 items)
- Plain language accessible to non-specialists

**3. 研究の方法** (Research Methods)
- Each method as a separate paragraph
- Include specific: cell lines, reagents, equipment, databases used
- Style: `Compact` paragraph style in Word

**4. 研究成果** (Research Achievements)
- Numbered findings, each linked to a publication
- **≥1 figure REQUIRED** (Policy P10): You MUST read the audit log (`References/figures/audit/audit_log.md`) and explicitly add an inline citation (e.g. `（図1参照）` or `(See Figure 1)`) within the narrative text of the corresponding finding.
- Positioning/international impact statement
- Future outlook
- Reference list at bottom with DOIs

### Figure Embedding Rules

- **Markdown**: `![Figure 1. Caption text](../References/figures/Figure1_Label.png)`
- **Word (.docx)**: Use `python-docx`'s `add_picture()` with 14cm width max
- **Caption**: Must match the figure content (verified in Step 3.6)
- **Position**: After the finding it illustrates, before the next finding

### Word Document Formatting

```python
# Font settings (JP version)
JP_FONT = "ＭＳ 明朝"
FONT_SIZE = Pt(10.5)
STYLES = {
    "section_header": "First Paragraph",  # e.g., "１．研究開始当初の背景"
    "body_text": "Body Text",              # narrative paragraphs
    "method_item": "Compact",             # method/finding items
    "narrative_block": "Normal"           # positioning/future outlook
}

# Font settings (EN version)
EN_FONT = "Times New Roman"
FONT_SIZE = Pt(10.5)

# Figure insertion
from docx.shared import Cm
doc.add_picture(figure_path, width=Cm(14))

# DO NOT modify: margins, page layout, or template styles
```

### Character Limit Constraints
- **Japanese**: Max 300 characters for the public KAKEN summary (target ~200 chars, max 2 line feeds)
- **English**: Max 1000 characters (max 2 line feeds)
- **Full report body** (cf-19 Word document): No strict limit, but aim for 3–5 pages

---

## 4. Figure Extraction & Preparation (Policy P10)

> **MANDATORY VISUAL EVIDENCE**: Every F-19-1 cf-19 MUST contain at least one figure illustrating key research outcomes.

### Sub-steps:

1. **Identify key result papers** from `{GRANT_ID}_Achievements_List.md` (first/corresponding author publications preferred)
2. **Extract PDF pages as PNGs** → `{GRANT_FOLDER}/References/figures/audit/`:
   ```python
   # Use: python3 ~/.gemini/antigravity/knowledge/kakenhi_management_pipeline/artifacts/Tools/process_figures.py extract-pages
   # Input: --pdf {GRANT_FOLDER}/References/paper/{paper}.pdf --output {GRANT_FOLDER}/References/figures/audit/
   ```
3. **Visual verification** (Policy P10.2 — MANDATORY):
   - Open each extracted PNG via `view_file` tool (binary image mode)
   - Identify the figure that best represents the key finding
   - Confirm the image is correctly extracted (not blank, not garbled)
4. **Auto-crop & rename** → `{GRANT_FOLDER}/References/figures/`:
   ```python
   # Use: python3 ~/.gemini/antigravity/knowledge/kakenhi_management_pipeline/artifacts/Tools/process_figures.py crop-rename
   # Input: --input {GRANT_FOLDER}/References/figures/audit/ --mapping "src.png:Figure1_Label.png"
   ```
5. **Write audit log** → `{GRANT_FOLDER}/References/figures/audit/audit_log.md`

---

## 5. Dual-Agent Review Gate (Policy P12)

### Review Dimensions & Pass Threshold

| Dimension | Min Score |
|-----------|-----------|
| 事実正確性 (Factual Accuracy) | ≥ 7/10 |
| 助成金帰属 (Grant Attribution) | ≥ 7/10 |
| 文字数・書式 (Character/Format Count) | ≥ 7/10 |
| 日英一致性 (Bilingual Consistency) | ≥ 7/10 |
| 図版-キャプション整合 (Figure-Caption Alignment) | ≥ 7/10 |
| 文体・レジスター (Tone/Register) | ≥ 7/10 |

### Review Process

1. **Round 1**: Writer agent generates draft → Reviewer agent scores all 6 dimensions
2. **Round 2**: Writer revises → Reviewer re-scores
3. **Round 3**: Final revision and approval
4. If all ≥ 7/10 after any round → **APPROVED**
5. Hard cap at 5 rounds → escalate to human if still failing

### Audit Trail

Log all rounds to: `{GRANT_FOLDER}/Reports/{GRANT_ID}_{YYYY}_Review_Rounds_Log.md`
```markdown
## Round {N}: {Date}
**Reviewer Scores**: Factual: X/10 | Attribution: X/10 | Format: X/10 | Bilingual: X/10 | Figures: X/10 | Register: X/10
**Key Issues**: [feedback]
**Writer Actions**: [what was revised]
**Status**: APPROVED / REVISION REQUIRED
```

---

## 6. Publication Verification Sequence

```
For each publication:
  1. Check {GRANT_ID}_Achievements_List.md → is it listed?
  2. Check Metadata_Verification.md → is DOI verified?
  3. Check acknowledgment in paper PDF → does it cite {GRANT_ID}?
  4. Assign 謝辞: 有/無 accordingly
  5. If NOT in Achievements_List but included → flag as "関連成果" (related, not direct)
```

---

## 7. Pre-Submission KAKEN Cross-Check (Policy P11)

```
1. Read: https://kaken.nii.ac.jp/ja/grant/KAKENHI-PROJECT-{GRANT_ID}/
2. Count: 雑誌論文 / 学会発表 / 図書 / 備考
3. Compare: against {GRANT_ID}_Achievements_List.md
4. Flag: any KAKEN-registered output not in draft
5. Benchmark: search 2-3 exemplary past F-19-1 in same review section (Policy P11.3)
```

---

## 8. AROS Sync (Run after any pipeline update)

```bash
# Sync Skills
cp -r KAKENHI_Pipeline/Skills/*/  ~/.gemini/skills/

# Sync Workflow
cp KAKENHI_Pipeline/Workflows/kakenhi-annual-report.md \
   ~/.gemini/antigravity/global_workflows/

# Sync Policies
cp KAKENHI_Pipeline/Policies/*.md ~/.gemini/antigravity/policies/

# Sync KIs
for ki in KAKENHI_Pipeline/KIs/*/; do
    ki_name=$(basename "$ki")
    mkdir -p ~/.gemini/antigravity/knowledge/$ki_name/artifacts
    cp -r "$ki"/* ~/.gemini/antigravity/knowledge/$ki_name/
done
```

---

*Last Updated: 2026-05-11 | KAKENHI_Pipeline v2.1.0*
