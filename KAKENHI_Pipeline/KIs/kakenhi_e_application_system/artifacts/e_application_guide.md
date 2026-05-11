# KAKENHI e-Application System — Researcher Operations Guide

> **Source**: Official JSPS Manuals (v6.9 基金 / v4.4 国際共同研究加速基金)
> **Full PDFs**: [kofumanual-shinseisha_K.pdf](./kofumanual-shinseisha_K.pdf) / [kofumanual-shinseisha_KK.pdf](./kofumanual-shinseisha_KK.pdf)
> **System URL**: https://www-shinsei.jsps.go.jp/kaken/index.html

---

## 1. System Overview

The 科研費電子申請システム (KAKENHI e-Application System) is the mandatory portal for all post-award grant procedures. Researchers log in using their **e-Rad ID and password**.

### Key Menu: 「交付内定・決定後の手続」
After login, click **「課題状況の確認」** on the target grant to access all reporting functions.

---

## 2. Post-Award Report Types & Procedures

### 2.1 Annual Reports (Non-Final Year)
| Form | Name | Menu Location |
|---|---|---|
| F-6-1 | 収支状況報告書 (Financial Status) | 「実施状況報告書」欄 → [入力] |
| F-7-1 | 研究実施状況報告書 (Research Implementation) | 同上 |

### 2.2 Final Year Reports
| Form | Name | Menu Location |
|---|---|---|
| F-6-2 | 収支決算報告書 (Final Financial Settlement) | 「実績報告書」欄 → [入力] |
| F-7-2 | 研究実績報告書 (Research Results) | 同上 |

### 2.3 Post-Grant Period Report (F-19-1) ← CRITICAL
| Form | Name | Menu Location |
|---|---|---|
| F-19-1 | 研究成果報告書 (Research Achievements) | **「補助事業期間終了後」欄 → [入力] or [再開]** |

---

## 3. F-19-1 研究成果報告書 — Step-by-Step Procedure

This is the most critical and complex reporting procedure. It consists of **two parts**:
1. **Web input items** (entered directly in the system)
2. **研究成果報告内容ファイル** (Word/PDF file uploaded to the system)

### Step 1: Download the Word Template
> **Source**: Official manual Section 2.17.1 (p.259)

```
① 科学研究費助成事業のWebページ等から研究成果報告内容ファイル様式をダウンロードします。
② ダウンロードした研究成果報告内容ファイル様式に報告内容を記入し、保存します。
```

**Where to download**: The template can be obtained from the JSPS website under:
- https://www.jsps.go.jp/j-grantsinaid/index.html → 「使用ルール・様式集」→「交付決定後の様式(E･F様式)」
- Or search for: `科研費 様式 F-19` on the JSPS website

**CRITICAL constraints**:
- Do NOT modify the template structure/layout
- Do NOT change margin settings (will cause upload errors)
- File size limit: **10MB maximum**
- Supported formats: **MS-Word (.doc, .docx) or PDF**
- External/special fonts may not render correctly

### Step 2: Enter Web Input Items
> **Source**: Official manual Section 2.17.2 (p.260-266)

Navigate to: 「課題管理」→「補助事業期間終了後」欄 → **[入力]** button

#### Required Web Input Fields (必須項目 ＊印)

| Field | JP Name | Limit | Notes |
|---|---|---|---|
| 研究課題名（英文） | Title (English) | — | Pre-filled if already registered |
| 研究代表者氏名（英語） | PI Name (EN) | — | Family: ALL CAPS, Given: capitalize first letter |
| 部局 | Department | — | Use full-width space if no department |
| 職 | Position | — | Required |
| 研究成果の概要（和文） | Outline JP | **Max 300 chars, ≤2 line breaks** | Target ~200 chars. Public-facing — avoid jargon |
| 研究成果の概要（英文） | Outline EN | **Max 1000 chars, ≤2 line breaks** | Public-facing |
| 研究成果の学術的意義や社会的意義 | Significance | **Max 300 chars, ≤2 line breaks** | Public-facing — avoid jargon |
| 研究分野 | Research Area | — | PI's area of specialization |
| キーワード（1～8） | Keywords | 1-8 items | Avoid chemical/math formulas |

#### Optional Fields
| Field | Notes |
|---|---|
| 後日再提出する | Check if you need to resubmit later |
| 再提出予定日 | Expected resubmission date |
| 再提出理由 | Reason for resubmission |

### Step 3: Upload the Word File
> **Source**: Official manual Section 2.17.2 ④ (p.266)

After completing Web input, click **[ファイルの選択]** in the 「研究成果報告内容ファイル選択」section at the bottom of the page, and select your prepared Word/PDF file.

### Step 4: Enter Publication Data
> **Source**: Official manual Section 2.17.2 ⑥ (p.267+)

The system **auto-populates** publication data from previously submitted F-6/F-7 reports. You only need to **[追加]** (Add) any new entries not yet in the system.

Categories:
- 雑誌論文 (Journal Articles)
- 学会発表 (Conference Presentations)  
- 図書 (Books)

### Step 5: Confirm and Send
> **Source**: Official manual Section 2.17.2 ⑧⑨ (p.272+)

1. System converts your report to PDF
2. Click **[研究成果報告書の確認]** to review the generated PDF
3. Click **[確認完了・送信]** to submit

⚠️ **WARNING**: The PDF generated at this stage contains a watermark 「未送信」. This is removed only after final submission.

---

## 4. Session & Character Encoding Warnings

- **Session timeout**: 60+ minutes of inactivity will cause data loss. Click **[一時保存]** frequently!
- **Character encoding**: JIS Level 1 & 2 only. The following are PROHIBITED:
  - Half-width katakana (半角カナ)
  - Circled numbers (①②③)
  - Roman numerals (Ⅰ～Ⅴ)
  - Era abbreviations (㍾㍽㍼)
  - Unit characters (㍉㌔㎜㎝)
  - External characters (外字)
  - Non-JIS kanji (old forms, rare characters)

---

## 5. Processing Status & Resume
> **Source**: Official manual Section 2.18 (p.283+)

| Button | Meaning |
|---|---|
| [入力] | Start new report entry |
| [再開] | Resume a previously saved draft |
| [確認] | Review a submitted report |
| [PDF ダウンロード] | Download the submitted PDF |

---

## 6. Quick Reference: Manual Sections by Task

| Task | Manual _K Section | Page |
|---|---|---|
| 交付申請書 (D-2-1) | 2.1 | ~p.10 |
| 支払請求書 (F-2-1) | 2.7 | ~p.100 |
| 収支状況報告 (F-6-1) | 2.12 | ~p.170 |
| 実施状況報告 (F-7-1) | 2.13 | ~p.190 |
| 収支決算報告 (F-6-2) | 2.14 | ~p.210 |
| 実績報告 (F-7-2) | 2.15 | ~p.230 |
| **研究成果報告 (F-19-1)** | **2.17** | **~p.259** |
| 処理状況確認・再開 | 2.18 | ~p.283 |

---

*Last updated: 2026-05-10*
