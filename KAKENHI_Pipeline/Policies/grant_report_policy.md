# Policy: KAKENHI Grant Report Compliance (科研費報告書ポリシー)

> **Enforcement Level**: MANDATORY for all KAKENHI grant report submissions
> **Scope**: Universal — applicable to any JSPS KAKENHI PI

---

## Policy 1: Publication-Grant Attribution

### P1.1 — Exclusive Attribution Rule
Each publication MUST be attributed to the grant(s) that genuinely funded it. A paper may appear in multiple grant reports **only if**:
- Both grants contributed financial resources to the work
- The paper's acknowledgment section cites both grant numbers
- The research content is genuinely relevant to both grants' objectives

### P1.2 — Period Boundary Rule
Publications are attributed to a grant based on **publication date** (accepted/published), not submission date:
- Fiscal Year runs **April 1 → March 31**
- A paper published in March 2025 belongs to FY2024
- A paper published in April 2025 belongs to FY2025

### P1.3 — Preprint Handling
- Preprints (bioRxiv, medRxiv) may be listed under 雑誌論文 with `査読: 無` (not peer-reviewed)
- Once the peer-reviewed version is published, **update** the entry in the next report
- Do NOT list both the preprint and the published version simultaneously

---

## Policy 2: Acknowledgment Compliance (謝辞記載義務)

### P2.1 — Mandatory Acknowledgment
Every publication produced with KAKENHI funding MUST include the grant number in the acknowledgment section:

**Template (English):**
```
This work was supported by JSPS KAKENHI Grant Number [{GRANT_ID}].
```

**Template (Japanese):**
```
本研究はJSPS科研費 [{GRANT_ID}] の助成を受けたものです。
```

### P2.2 — Acknowledgment Tracking
When filling F-7-1/F-7-2, each publication entry requires:
- `科研費の謝辞`: 有 (Yes) or 無 (No)
- Papers WITHOUT acknowledgment should be flagged for correction in future reprints/erratas

---

## Policy 3: Bilingual Consistency (日英一致性)

### P3.1 — Database Synchronization
All publications listed in KAKENHI reports MUST be consistent with entries in:
- researchmap (`{PI_RESEARCHMAP_URL}`)
- ORCID (`{PI_ORCID}`)
- Google Scholar

### P3.2 — Name Consistency
The PI name MUST appear consistently across all documents:
- Japanese reports: `{PI_NAME_JP}` or `{PI_NAME_EN}`
- English reports: `{PI_NAME_EN}`
- In author lists: underline the PI name (研究代表者に下線)

---

## Policy 4: Deadline Compliance (提出期限遵守)

### P4.1 — JSPS Deadline
| Report Type | Deadline |
|---|---|
| 実施状況報告書 (F-6-1, F-7-1) | **May 31** of the following fiscal year |
| 実績報告書 (F-6-2, F-7-2) | **May 31** after the final fiscal year |
| 交付申請書 (D-2-1) | Within designated period after 内定 |
| 支払請求書 (D-4-1, F-2-1) | After 交付決定 or at start of each FY |

### P4.2 — Internal Deadline (学内締切)
The host institution's internal deadline is typically **2-4 weeks before** the JSPS deadline. Always confirm with 研究支援課 (Research Support Office).

---

## Policy 5: Budget Reporting Rules (経費報告ルール)

### P5.1 — Category Compliance
Direct costs must be reported under the same categories as the 交付申請書:
- 物品費 (Goods): Reagents, consumables, equipment < ¥500K
- 旅費 (Travel): Domestic/international conference attendance
- 人件費・謝金 (Personnel): Research assistants, collaborator honoraria
- その他 (Other): Publication fees, software licenses, etc.

### P5.2 — Threshold Rules
- Equipment ≥ ¥500,000 → Must appear in 設備備品 section
- Category changes >50% → Requires F-2-2 (変更交付申請書)
- Unspent funds (次年度使用額) → Must explain reason and usage plan

### P5.3 — Indirect Costs
- Always 30% of direct costs
- Managed by the institution, not the researcher
- Do NOT include in direct cost calculations

### P5.4 — Carryover Justification (次年度使用額が生じた理由と使用計画)
When unspent funds carry over to the next fiscal year (次年度使用額 > 0):
- **MANDATORY**: The agent MUST include the 「次年度使用額が生じた理由と使用計画」 section in F-7-1/F-7-2 drafts
- Content must explain: (1) 理由 — why funds were not fully expended, (2) 使用計画 — specific planned expenditures for the next year
- Limit: ≤600文字 (1200バイト), max 3 line feeds
- Agent must confirm actual carryover amount with the researcher before drafting

---

## Policy 6: Version Control & File Naming

### P6.1 — File Naming Convention
```
{GRANT_ID}_{FiscalYear}_{FormCode}.pdf
```
> [EXAMPLE - NOT NORMATIVE]
> `24K23552_2024_F-6-1.pdf`, `25K20204_2025_D-2-1.pdf`

### P6.2 — Draft Management
- Working drafts: `{GRANT_ID}_{FY}_{FormCode}_draft.md`
- Final versions: `{GRANT_ID}_{FY}_{FormCode}.pdf`
- Never delete drafts — keep for audit trail

---

## Policy 7: Local Rules Precedence (決定通知・使用ルール優先)

### P7.1 — Mandatory Verification
Before filling out any form, the agent or user MUST verify the specific requirements outlined in the `Announcement_Rules/` directory within the respective grant folder.
- The **交付決定通知書 (Decision Notice)** is the ultimate source of truth for budget figures and official titles.
- The **使用ルール (Usage Rules)** pdf contains the specific compliance rules for that fiscal year's fund.
- **If these local documents conflict with general JSPS web guidelines, the local `Announcement_Rules/` documents take absolute precedence.**

---

## Policy 8: F-19-1 Multi-Year Coverage (研究成果報告書の全期間対象)

### P8.1 — Full-Period Aggregation Rule
F-19-1 (研究成果報告書) MUST aggregate ALL achievements from the ENTIRE grant period (all fiscal years), not just the final year. This is fundamentally different from annual reports (F-7-1) which cover a single fiscal year.

### P8.2 — Cross-Reference Checklist
Before finalizing F-19-1, verify completeness using these 4 sources:
1. **KAKEN database** — `https://kaken.nii.ac.jp/ja/grant/KAKENHI-PROJECT-{GRANT_ID}/` → registered outputs
2. **Annual reports** — All F-7-1/F-7-2 filed during the grant period
3. **`{PI_FILE}.md`** — Researcher's complete profile
4. **`{GRANT_ID}_Achievements_List.md`** — Grant-specific achievement list

If KAKEN shows registered outputs not in the F-19-1 draft → mandatory reconciliation before submission.

### P8.3 — F-19-1 Writing Register
F-19-1 is a **public-facing document** published to the KAKEN database. Writing register:
- **Avoid technical jargon** (「社会・国民にわかりやすく」)
- Explain significance in terms accessible to non-specialists
- Character limits: Japanese max 300 chars (target ~200), English max 1000 chars, max 2 line feeds each

---

## Policy 9: Researcher Profile Freshness (研究者情報の鮮度)

### P9.1 — Mandatory Refresh
Before generating any KAKENHI form, `ResearcherMetaInfo/{PI_FILE}.md` must have been refreshed within **30 calendar days** of the report submission deadline.

### P9.2 — Refresh Procedure
Use the `researcher-data-collection` skill (3-tier strategy):
- **Tier 1**: `read_url_content` from researchmap, ORCID, KAKEN, J-GLOBAL, Google Scholar, Web of Science, institutional SORAN
- **Tier 2**: `browser_subagent` for JS-rendered pages or those requiring interaction
- **Tier 3**: researchmap v2 API (future — requires JST application)

### P9.3 — Staleness Warning
If the profile was last updated >30 days before the submission deadline:
- Agent MUST issue a **WARNING** and refuse to proceed until refresh is completed
- Exception: user explicitly overrides with documented justification

---

## Policy 10: Visual Asset Integrity (図版の完全性)

### P10.1 — Mandatory Figure Inclusion
All F-19-1 cf-19 (研究成果報告内容ファイル) reports MUST include **at least one figure** illustrating key research outcomes. Reports lacking visual evidence will fail the dual-agent review gate.

### P10.2 — LLM Vision Verification
All figures included in cf-19 reports MUST be visually verified using LLM vision capabilities:
- Automated extraction alone is **NEVER sufficient** for final reports
- Every extracted figure must be viewed via `view_file` and confirmed to match its caption

### P10.3 — Staging & Audit Trail
- Verified figures must be staged in `{GRANT_FOLDER}/References/figures/audit/`
- An `audit_log.md` recording source PDF, page number, extraction method, and verification result must be maintained
- Composite figures (panels from multiple papers) are allowed and encouraged when they improve narrative clarity

---

## Policy 11: KAKEN Database Consistency (KAKENデータベースとの整合性)

### P11.1 — Pre-Drafting Cross-Check
Before drafting F-19-1, the agent MUST check the KAKEN database entry for the grant:
- URL: `https://kaken.nii.ac.jp/ja/grant/KAKENHI-PROJECT-{GRANT_ID}/`
- Compare: count of 雑誌論文, 学会発表, 図書, 備考

### P11.2 — Post-Submission Verification
After F-19-1 submission, verify the published KAKEN page matches submitted content.

### P11.3 — Benchmark Quality
Search KAKEN for 2–3 exemplary past F-19-1 reports from similar grants (same review section) to use as quality benchmarks for writing style, length, and figure usage.

---

## Policy 12: Mandatory Dual-Agent Review (全書式への査読)

### P12.1 — Scope
**ALL KAKENHI forms** undergo **3-round writer/reviewer dual-agent review** before finalization.

### P12.2 — Review Dimensions
| Dimension | Pass Threshold |
|-----------|---------------|
| 事実正確性 (Factual Accuracy) | ≥ 7/10 |
| 助成金帰属 (Grant Attribution) | ≥ 7/10 |
| 文字数・書式 (Character/Page Count) | ≥ 7/10 |
| 日英一致性 (Bilingual Consistency) | ≥ 7/10 |
| 図版-キャプション整合 (Figure-Caption Alignment) | ≥ 7/10 |
| 科研費の文体・レジスター (KAKENHI Tone/Register) | ≥ 7/10 |

### P12.3 — Review Process
1. **Round 1**: Writer agent generates draft → Reviewer agent scores all dimensions
2. **Round 2**: Writer agent revises based on feedback → Reviewer re-scores
3. **Round 3**: Final revision and approval
4. If all dimensions ≥ 7/10 after any round → approved
5. **Hard cap**: Maximum 5 revision rounds. If still failing → escalate to user

### P12.4 — Audit Trail
All review rounds must be logged to `{GRANT_ID}_{FY}_Review_Rounds_Log.md` with:
- Round number, reviewer scores, specific feedback, and resolution status

---

## Policy 13: e-Rad Form Field Validation (電子申請フォームフィールド検証)

### P13.1 — Byte-Based Counting for F-7 Forms
The F-7 研究実績の概要 field uses **byte-based counting**: 全角=2バイト, 半角=1バイト, 改行=2バイト.
- **Hard limit**: ≤800文字 (1600バイト), max 5 line feeds
- **Warning threshold**: ≤1200バイト triggers a system warning — target ≥1200バイト
- **Verification**: All F-7 drafts MUST be validated with `Tools/erad_char_count.py --byte-mode` before review gate

### P13.2 — ホームページ等 Title Constraint
Each website entry in the e-Rad form requires:
- **タイトル**: ≤50文字 (short descriptive name, NOT URLs or long descriptions)
- **URL**: Separate field for the full URL
- **備考**: Shared remarks field, ≤200文字 (400バイト), max 2 line feeds
- Violation triggers: `Error:webページ（タイトル）1行目は50文字以内で入力してください。`

### P13.3 — Mandatory Sections Checklist
Before passing to the dual-agent review gate (P12), verify ALL of the following e-Rad sections are present in the draft:
- [ ] 研究実績の概要 (byte-count validated)
- [ ] キーワード (1–8 items)
- [ ] 研究発表: 雑誌論文, 学会発表, 図書, 産業財産権
- [ ] ホームページ等 (structured: タイトル + URL, 備考)
- [ ] 受賞 (if applicable)
- [ ] 次年度使用額が生じた理由と使用計画 (if carryover > 0)

---

*Last updated: 2026-05-11 | KAKENHI_Pipeline v2.1.0*
