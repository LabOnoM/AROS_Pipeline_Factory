# Skill: KAKENHI Pre-Award Forms & Financial Templates

> **Purpose**: Reference guide for all KAKENHI forms NOT covered by the post-award reporting workflow (D-series + F-2 series + F-6-2 financial settlement).
> **Scope**: 基金 (Fund-type) grants — 研究活動スタート支援, 若手研究, 基盤研究(C/B/A)

---

## 1. D-2-1 交付申請書 (Grant Delivery Application)

### Timing
- After 交付内定 (grant notification), typically April
- Internal deadline: ~2 weeks after notification

### Required Fields
| Field | Source | Notes |
|-------|--------|-------|
| 研究課題名 (JP) | Pre-filled from application | Do NOT change |
| 研究課題名 (EN) | May need entry | Use exact title from application |
| 研究経費 (Budget) | 交付決定通知書 | Use EXACT figures from Decision Notice |
| 経費区分 | D-2-1 application | 物品費 / 旅費 / 人件費・謝金 / その他 |
| 研究実施計画 | Original application | Brief summary of planned research |

> [EXAMPLE - NOT NORMATIVE]
> Previous D-2-1 PDFs in the grant folder (`{GRANT_ID}_{YYYY}_D-2-1.pdf`) serve as format references.

---

## 2. D-4-1 支払請求書 (Payment Request — Initial)

### Timing
- After 交付決定 (grant decision confirmed)

### Required Fields
| Field | Source | Notes |
|-------|--------|-------|
| 請求金額 | 交付決定通知書 | Exact amount from Decision Notice |
| 振込先口座 | Institutional account | University handles this |

### Note
> This is primarily an institutional process. The researcher confirms the amounts; the university submits.

---

## 3. F-2-1 支払請求書 (Payment Request — Continuing)

### Timing
- Start of each fiscal year for multi-year 基金 grants

### Required Fields
| Field | Source | Notes |
|-------|--------|-------|
| 請求年度 | Current FY | e.g., 令和7年度 for FY2025 |
| 請求金額 | Original budget plan | May differ if F-2-2 was filed |
| 前年度繰越額 | Previous year settlement | If unspent funds carried over |

---

## 4. F-2-2 変更交付申請書兼支払請求書 (Budget Change + Payment Request)

### When Required
- Any budget category change >50% compared to original 交付申請書

### Required Fields
| Field | Source | Notes |
|-------|--------|-------|
| 変更理由 | Researcher | Clear justification for reallocation |
| 変更前経費区分 | Original D-2-1 | Original budget breakdown |
| 変更後経費区分 | New plan | Revised budget breakdown |
| 合計金額 | Must match | Total must remain unchanged |

### Justification Template
```
変更理由: 当初の研究計画において[物品費/旅費/...]に予定していた経費について、
研究の進展に伴い[具体的な理由]のため、[変更先カテゴリー]への配分変更が必要となった。
本変更により、研究目的の達成に支障はない。
```

---

## 5. F-6-2 収支決算報告書 (Final Financial Settlement)

### Timing
- After the final fiscal year of the grant period
- Due: May 31 of the following year

### Template (Agent fills structure; researcher fills numbers)

```markdown
# F-6-2 収支決算報告書

## 基本情報
- 課題番号: {GRANT_ID}
- 研究課題名: {GRANT_TITLE_JP}
- 研究代表者: {PI_NAME_JP} ({PI_NAME_EN})
- 助成期間: {GRANT_START_DATE} ～ {GRANT_END_DATE}

## 経費内訳 (直接経費)

| 費目 | 交付決定額 (千円) | 実支出額 (千円) | 差額 (千円) | 備考 |
|------|-------------------|-----------------|-------------|------|
| 物品費 | [_____] | [_____] | [_____] | 試薬・消耗品等 |
| 旅費 | [_____] | [_____] | [_____] | 学会参加・共同研究 |
| 人件費・謝金 | [_____] | [_____] | [_____] | 研究補助員等 |
| その他 | [_____] | [_____] | [_____] | 論文投稿料・ソフトウェア等 |
| **合計** | **[_____]** | **[_____]** | **[_____]** | |

## 間接経費
- 間接経費率: 30%
- 間接経費額: [直接経費合計 × 0.3] 千円
- ※間接経費は研究機関が管理

## 残額がある場合
- 残額: [_____] 千円
- 残額発生理由: [_____]
- ※基金の場合、残額は返還不要だが理由の記載は必要

## チェックリスト
- [ ] 交付決定通知書の金額と照合済み
- [ ] カテゴリー別支出が50%以上変動していないか確認
  - 変動あり → F-2-2 を提出済みか確認
- [ ] 大学経理課の数値と一致することを確認
- [ ] 間接経費は30%で正確か確認
```

---

## 6. Complete Timing Matrix

| Form | When Required | Internal Deadline | JSPS Deadline | e-App Menu |
|------|---------------|-------------------|---------------|------------|
| D-2-1 | After 内定 notification | ~2 weeks after notification | Designated period | 交付申請 |
| D-4-1 | After 交付決定 | Institution-specific | Institution-specific | 支払請求 |
| F-2-1 | Start of each FY (continuing) | March | April | 支払請求 |
| F-2-2 | When budget reallocation needed | As needed | Before expenditure | 変更交付申請 |
| F-6-1 | Non-final year end | ~2 weeks before JSPS | May 31 | 実施状況報告書 |
| F-7-1 | Non-final year end | ~2 weeks before JSPS | May 31 | 実施状況報告書 |
| F-6-2 | Final year end | ~2 weeks before JSPS | May 31 | 実績報告書 |
| F-7-2 | Final year end | ~2 weeks before JSPS | May 31 | 実績報告書 |
| F-19-1 | After grant period ends | ~2 weeks before JSPS | June (typically) | 補助事業期間終了後 |

---

*Last updated: 2026-05-11 | KAKENHI_Pipeline v2.0.0*
