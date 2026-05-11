# Skill: KAKENHI Form Completion (科研費報告書作成スキル)

> **Scope**: Completing all post-award JSPS KAKENHI forms for 基金 (Fund) grants
> **Applicable Grants**: 若手研究, 研究活動スタート支援, 基盤研究(B/C), 挑戦的研究(萌芽/開拓)

---

## 1. Form Code Reference

### Administrative Forms (交付関連)

| Form Code | Name (JP) | Name (EN) | When to Submit | Content |
|---|---|---|---|---|
| **D-2-1** | 交付申請書 | Grant Delivery Application | After 内定 (informal decision) | Budget breakdown, research plan summary, researcher info |
| **D-4-1** | 支払請求書 | Request for Payment | After 交付決定 (formal decision) | Payment destination, amount confirmation |
| **F-2-1** | 支払請求書 | Request for Payment (continuing) | Annually, each fiscal year | Year-by-year payment request for multi-year grants |
| **F-2-2** | 変更交付申請書兼支払請求書 | Change Request + Payment | When budget changes needed | Budget reallocation between categories |

### Report Forms (報告書関連)

| Form Code | Name (JP) | Name (EN) | When to Submit | Content |
|---|---|---|---|---|
| **F-6-1** | 収支状況報告書 | Financial Status Report | May 31 (non-final years) | Revenue/expenditure by category |
| **F-7-1** | 研究実施状況報告書 | Research Implementation Report | May 31 (non-final years) | Research progress narrative + publication list |
| **F-6-2** | 収支決算報告書 | Final Financial Report | May 31 (final year) | Final revenue/expenditure settlement |
| **F-7-2** | 研究実績報告書 | Research Results Report | May 31 (final year) | Full project results + complete publication list |

### Key Distinction

```
非最終年度 (Non-final year) → 実施状況報告書 (F-6-1 + F-7-1)
最終年度   (Final year)     → 実績報告書     (F-6-2 + F-7-2)
```

---

## 2. Skill: Filling D-2-1 (交付申請書)

### Required Fields
1. **研究課題名** — Project title (must match exactly with 内定通知)
2. **研究代表者情報** — Name, institution, researcher number, department
3. **研究経費** — Budget breakdown by fiscal year:
   - 物品費 (Goods/Equipment)
   - 旅費 (Travel)
   - 人件費・謝金 (Personnel/Honoraria)
   - その他 (Other)
4. **間接経費** — Indirect costs (30% of direct costs, auto-calculated)
5. **研究目的・計画** — Brief research purpose and multi-year plan

### Budget Pattern
```
直接経費:
  FY{N}:   ¥{DIRECT_COST_FYN} (物品: ¥{AMOUNT} / 旅費: ¥{AMOUNT} / ...)
  FY{N+1}: ¥{DIRECT_COST_FYN1} (物品: ¥{AMOUNT} / 旅費: ¥{AMOUNT} / ...)
間接経費:
  FY{N}:   ¥{INDIRECT_FYN}    (= Direct × 0.30)
  FY{N+1}: ¥{INDIRECT_FYN1}
```

### Tips
- Budget categories must be consistent with the original application (研究計画調書)
- Changes >50% in any category require F-2-2 (変更交付申請書)
- Indirect costs are always exactly 30% of direct costs

---

## 3. Skill: Filling F-7-1 (研究実施状況報告書)

### e-Rad Byte-Counting for F-7 Forms

> **CRITICAL**: F-7 研究実績の概要 uses **byte-based counting**: 全角=2バイト, 半角=1バイト, 改行=2バイト.
> Maximum: **800文字 (1600バイト)**, max 5 line feeds.
> **Warning**: e-Rad displays a warning if ≤1200バイト. Target: 600–800 文字 (≥1200バイト).

### Required Sections

#### Section A: 研究実績の概要 (Summary of Research Achievements)
- **研究目的**: Brief restatement of the project objective
- **研究方法**: Methods used during the reporting year
- **研究成果**: Results obtained
- **今後の研究方針**: Future research direction (next year plans)
- **自己評価**: Self-assessment of progress (おおむね順調 / やや遅れている / 遅れている)

#### Section B: 研究発表 (Research Publications)
Categorized list:

| Category | Fields Required |
|---|---|
| **雑誌論文** (Journal Articles) | Authors, Title, Journal name, Vol(Issue):Pages, Year, DOI, Peer-review status (有/無), OA status (有/無), Acknowledgment of 科研費 (有/無) |
| **学会発表** (Conference Presentations) | Presenter(s), Title, Conference name, Date, Invited/Oral/Poster |
| **図書** (Books/Chapters) | Authors, Chapter title, Book title, Publisher, Pages, Year |
| **産業財産権** (Patents) | Type, Title, Applicant, Application number, Date |
| **ホームページ/作品** (Web/Software) | タイトル (≤50文字), URL, 備考 (≤200文字) |

#### Section C: ホームページ等 (Websites/Software) — e-Rad Form Structure

The e-Rad system provides **5 entry slots**. Each slot requires:
- **タイトル (Title)**: ≤50文字 — short descriptive name, NOT a URL or description
- **URL**: Full URL to the resource
- **備考 (Remarks)**: Shared field, ≤200文字 (400バイト), max 2 line feeds

> **⚠️ KNOWN ERROR**: Pasting URLs or descriptions into the タイトル field causes:
> `Error:webページ（タイトル）1行目は50文字以内で入力してください。`

#### Section D: 次年度使用額が生じた理由と使用計画 (Carryover Justification)

**Required when**: 「次年度使用額（B-A）」column is greater than zero.

| Field | Limit | Max Line Feeds |
|-------|-------|----------------|
| 次年度使用額が生じた理由と使用計画 | ≤600文字 (1200バイト) | 3 |

Content must include:
1. **理由**: Why funds were not fully expended (procurement delays, timeline shifts, etc.)
2. **使用計画**: Specific items to be funded, combined with next year's allocation

> **NOTE**: If carryover is ¥0, this field is not required.

### Tips
- 研究代表者の名前に下線を引く (underline the PI name in author lists)
- Only include publications from the reporting fiscal year (April 1 – March 31)
- Must include DOI for all peer-reviewed publications
- OA (Open Access) status is now mandatory
- 科研費謝辞 (Acknowledgment): Papers funded by this grant MUST include the grant number

---

## 4. Skill: Filling F-7-2 (研究実績報告書 — Final Report)

### Differences from F-7-1
- Covers the **entire project period** (not just one fiscal year)
- Requires consolidating the research results, comparison with the plan, and future outlook into a single, strict-length text box.
- Publication list should include ALL publications from the project period.

### Required Sections for Web Form
- **【研究実績の概要】 (Summary of Research Achievements)**: Max **800文字 (1600バイト, byte-counted: 全角=2, 半角=1, 改行=2)**, max 5 line feeds. Must synthesize the objectives, methods, key findings, and future outlook. **Target ≥1200バイト to avoid e-Rad warning.**
- **【キーワード】 (Keywords)**: 1 to 8 keywords. No chemical/mathematical formulas.
- **研究発表 (Publications)**: Complete list of papers, presentations, etc.
- **ホームページ等 (Websites/Software)**: タイトル (≤50文字) + URL per entry, max 5 entries. 備考 (≤200文字). See Section 3, Section C above.
- **次年度使用額が生じた理由と使用計画**: ≤600文字 (1200バイト), max 3 line feeds. Required when carryover > 0. See Section 3, Section D above.

## 5. Skill: Filling F-19-1 (研究成果報告書 — Web Entry)

### e-Rad Character Counting Rule (Calibrated 2026-05-11)

> **1 visible character = 1 文字** regardless of byte width (全角=1, 半角=1).
> Line feeds are **NOT counted** toward the total but are limited separately (max 2).
> Use `Tools/erad_char_count.py --file <path> --section <header> --limit <N>` to verify.

### e-Rad JIS X0208 Encoding Constraint

> **CRITICAL**: The e-Rad system only accepts characters within the **JIS X0208** standard.
> Non-JIS characters are silently converted to `&#xxxx;` HTML entities, triggering a red warning banner.

**Common offenders to AVOID:**
| Character | Unicode | Name | Safe Replacement |
|-----------|---------|------|------------------|
| `—` | U+2014 | EM DASH | ` - ` (spaced hyphen) |
| `–` | U+2013 | EN DASH | `-` (hyphen) |
| `'` `'` | U+2018/9 | SMART QUOTES | `'` (apostrophe) |
| `"` `"` | U+201C/D | SMART DOUBLE QUOTES | `"` (ASCII quote) |
| `…` | U+2026 | HORIZONTAL ELLIPSIS | `...` (three dots) |

**Rule**: For English text, use only **ASCII printable characters** (U+0020–U+007E).
Use `Tools/erad_char_count.py --check-jis` to validate before pasting into e-Rad.

### Web Entry Required Sections

| Field | Limit | Max LF | Register |
|-------|-------|--------|----------|
| 研究成果の概要（和文） | **300 chars** | 2 | Plain language, general public |
| 研究成果の概要（英文） | **1000 chars** | 2 | Plain language, general public |
| 研究成果の学術的意義や社会的意義 | **300 chars** | 2 | Academic + societal significance |
| 研究分野 | — | — | Research area keywords |
| キーワード | 1–8 items | — | No formulas |

### Significance Section Guidance
The significance text (max **300 chars**, max **2 line feeds**) must:
1. State **academic significance**: What new knowledge was produced? What prior understanding was expanded?
2. State **social significance**: How could the findings benefit society, patients, or industry?
3. Avoid jargon — written for the general public.
4. Use line feed markers 【学術的意義】/【社会的意義】 only if character budget allows.

---

## 6. Skill: Publication List Assembly

### Step-by-Step Process
1. **Identify grant period**: Start date → End date (from Announcement_Rules)
2. **Filter `{PI_FILE}.md` publications** by year range
3. **Classify each publication**:
   - Is the PI first/corresponding author? → Primary output
   - Is it a co-authored paper? → Include only if genuinely related
4. **Check acknowledgment**: Does the paper cite `{GRANT_ID}`?
5. **Format per JSPS requirements**: Authors, Title, Journal, Vol:Pages, Year, DOI, 査読/OA/謝辞
6. **Add conference presentations** from the same period
7. **Add software/tools** developed during the period

### Publication Attribution Matrix Pattern

> [EXAMPLE - NOT NORMATIVE]
> Build a matrix similar to the one below, customized for the PI's actual grants:

| Publication | Grant A ({ID_A}) | Grant B ({ID_B}) | Grant C ({ID_C}) |
|---|---|---|---|
| Paper 1 (Year) | ✅ Direct | — | — |
| Paper 2 (Year) | ✅ Direct | 🔶 Related | — |
| Paper 3 (Year) | — | — | ✅ Direct |

---

## 6. Key Resources & Rules

### Local Rules (Primary Source of Truth)
Before completing any form, you MUST consult the `Announcement_Rules/` folder located within the target grant's directory:
- **`*_ketteitsuuchi.pdf`** (交付決定通知書): Contains the exact approved budget figures and formal project title.
- **`*_shiyouru-ru.pdf`** (補助条件/使用ルール): Contains the strict legal rules for fund usage and reporting for that specific year. **These local files supersede general web guidelines.**

### Online Resources
| Resource | URL | Content |
|---|---|---|
| 科研費電子申請システム | https://www-shinsei.jsps.go.jp/ | Online submission portal (e-Rad login) |
| 使用ルール・様式集 | https://www.jsps.go.jp/j-grantsinaid/16_rule/index.html | Official forms, manuals, and guidelines |
| 科研費ハンドブック | https://www.jsps.go.jp/j-grantsinaid/15_hand/index.html | Comprehensive usage rules |
| 電子申請操作手引 | Available after login on the 電子申請 system | Step-by-step screenshots for each form |

---

*Last updated: 2026-05-11 | KAKENHI_Pipeline v2.1.0*
