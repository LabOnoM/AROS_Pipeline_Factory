# KI: KAKENHI Report Forms Reference

> **Purpose**: Quick-reference for all JSPS KAKENHI post-award form codes
> **Source**: JSPS official site, existing grant folder analysis

---

## Form Code Dictionary

### D-Series (交付関連 / Grant Delivery)

| Code | JP Name | EN Name | Timing |
|---|---|---|---|
| D-2-1 | 交付申請書 | Grant Delivery Application | After 内定 notification |
| D-4-1 | 支払請求書 | Payment Request | After 交付決定 |

### F-Series (報告・請求 / Reports & Requests)

| Code | JP Name | EN Name | Timing |
|---|---|---|---|
| F-2-1 | 支払請求書 | Payment Request (annual) | Start of each FY |
| F-2-2 | 変更交付申請書兼支払請求書 | Budget Change + Payment | When budget reallocation needed |
| F-6-1 | 収支状況報告書 | Financial Status Report | May 31, non-final years |
| F-6-2 | 収支決算報告書 | Final Financial Report | May 31, final year |
| F-7-1 | 研究実施状況報告書 | Research Implementation Report | May 31, non-final years |
| F-7-2 | 研究実績報告書 | Research Results Report | May 31, final year |
| F-19 | 研究成果報告書 | Research Outcomes Report | After grant period ends |

### A-Series / C-Series (特別研究員 / JSPS Fellows)

| Code | JP Name | EN Name | Context |
|---|---|---|---|
| A-2-1 | 採用時研究計画 | Research Plan at Adoption | DC2/PD adoption |
| A-4-1 | 採用時評定 | Evaluation at Adoption | DC2/PD adoption |
| C-6 | 研究経費実績報告 | Budget Report | DC2/PD annual |
| C-7-1 | 研究実績報告書 | Research Results Report | DC2/PD annual |
| Form 14 | 研究経過及び研究計画 | Progress + Plan | PD specific |
| Form 15 | 最終研究報告書 | Final Research Report | PD specific |

---

## Submission Decision Tree

```
Grant type = 基金 (Fund)?
├── Yes → Is this the final year?
│   ├── Yes → Submit F-6-2 + F-7-2 (実績報告書)
│   └── No  → Submit F-6-1 + F-7-1 (実施状況報告書)
└── No (補助金/Subsidy) → Different form series (E-series)
```

---

## Official URLs

| Resource | URL |
|---|---|
| 電子申請システム | https://www-shinsei.jsps.go.jp/ |
| 使用ルール・様式 | https://www.jsps.go.jp/j-grantsinaid/16_rule/index.html |
| 科研費ハンドブック | https://www.jsps.go.jp/j-grantsinaid/15_hand/index.html |
| e-Rad | https://www.e-rad.go.jp/ |

---

*Last updated: 2026-05-11*

---

## F-19-1 研究成果報告内容ファイル Template (cf-19.docx)

> **Template file**: `artifacts/cf-19.docx` (様式 C-19 / F-19-1 共通)

### Section Structure (Verified from template)
| # | JP Section Title | EN Translation |
|---|---|---|
| 1 | 研究開始当初の背景 | Background at the start of research |
| 2 | 研究の目的 | Purpose of research |
| 3 | 研究の方法 | Research methods |
| 4 | 研究成果 | Research achievements |

### Template Constraints
- **Do NOT** modify margin settings or page layout
- **Do NOT** change font styles set by the template
- File size limit: **10MB maximum**
- Supported formats: MS-Word (.doc, .docx) or PDF
- External/special fonts may not render correctly in the e-Rad system
