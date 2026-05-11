# 課題成果報告における出版物のFact Checkポリシー (Fact-Check Policy for Grant Reporting)

**Version**: 2.0 (KAKENHI_Pipeline v2.0.0)
**Scope**: All KAKENHI and MEXT/JSPS grant reporting workflows.

## 1. 目的 (Purpose)
科研費・公的資金の成果報告において、研究成果（論文等）が実際に当該助成金（課題番号）からの支援をAcknowledgement等で受けているか、あるいは「直接的な成果」ではなく「関連成果」であるかを厳密に区別・検証し、虚偽や誤認に基づく報告を完全に防止する。

## 2. 適用基準 (Verification Standards)
成果として報告するすべての論文・プレプリント等について、**必ずPDF本文レベルの監査（Fact Check）** を実施しなければならない。抄録や外部メタデータ（PubMed, CrossRef等）のみの確認は不可とする。

### A. 直接的成果 (Direct Output - ✅)
以下の条件を**すべて**満たす場合のみ「直接的成果」として報告可能である。
1. **謝辞の記載**: 当該論文のAcknowledgement等のセクションに、当該科研費課題番号（例: JSPS KAKENHI Grant Number `{GRANT_ID}`）が明記されていること。
2. **期間の合致**: 助成期間内に行われた研究成果であること。

### B. 関連成果・波及的成果 (Thematically Related Output - 🔷)
以下の条件に該当する場合は「関連成果」として厳密に区別して報告する。
1. **謝辞の記載なし**: 本課題に関連する研究であるが、当該科研費の直接的な支援を明記していない。
2. **別課題の成果**: 関連する別プロジェクト（共同研究等）から生み出され、本課題と学術的・テーマ的に密接な繋がりがあるもの。

## 3. 自動化ワークフローでの強制適用 (Enforcement in Automated Workflows)
AIエージェントおよびワークフロー（例: `/kakenhi-annual-report`, `/wiki-build`）が成果リストを生成・更新する際は、必ず以下の手順を経る。
1. `{GRANT_FOLDER}/References/` 内の対象論文PDFを走査する。
2. "Acknowledgement", "Funding", "Grant" のキーワード周辺で課題番号の有無を検索する。
3. `{GRANT_ID}_Achievements_List.md` および `Publication_Grant_Map.md` のマッピング情報と照合し、不一致があれば警告を発する。
4. ドラフト生成時、関連成果を誤って「本課題の助成による成果」と記述しないよう、表現（例：「本研究課題に関連して」）を強制的に修正する。

## 4. 違反時の対応 (Handling Violations)
本ポリシーに違反した報告書案（PDFエビデンスのない謝辞の主張等）が検出された場合、エージェントは即座にその出力をリジェクトし（Score: 0/10）、ユーザーに修正を要求しなければならない。

---

## 5. 図版の視覚的検証 (Visual Asset Verification)

**Established**: May 2026 (Root Cause: 100% figure mismatch during F-19-1 cf-19 audit)

### Rule
F-19-1 研究成果報告内容ファイル (cf-19) に含まれるすべての図版は、ソース論文と照合してLLMの視覚機能で検証しなければならない。

### Background
2026年5月の監査において、PDFから自動抽出された全4枚の図版がキャプションと不一致であることが判明した（エラー率100%）。これは `pdfimages` や `pdftoppm` 等の自動抽出ツールがページ番号・図版境界を誤認識したことが原因である。

### Procedure
1. ソースPDFから候補図版を抽出する（ページ番号を明示的に指定）
2. `view_file` (バイナリイメージ対応) で抽出画像を確認する
3. 図版の内容がキャプションと一致するか、LLMの視覚能力で検証する
4. 不一致の場合: 正しいページ/パネルを特定し再抽出する
5. 検証済み図版は `{GRANT_FOLDER}/References/figures/audit/` にステージングし、`audit_log.md` に記録する

### Enforcement
- 自動抽出のみで視覚検証を経ていない図版を含む報告書は **即時リジェクト** する
- 図版の選択は、複数の論文から適切なパネルを組み合わせて構成してよい

---

## 6. 複数ソース相互検証 (Multi-Source Cross-Verification)

### Rule
報告書に記載するすべての出版物メタデータは、最低2つの独立したソースで検証しなければならない。

### Verification Matrix
| データ項目 | Source A | Source B | Source C (optional) |
|-----------|---------|---------|---------------------|
| DOI | Crossref API | Publisher website | — |
| 著者名・著者順序 | Crossref API | researchmap | ORCID |
| 論文タイトル | Crossref API | researchmap | Google Scholar |
| 雑誌名・巻号 | Crossref API | J-GLOBAL | KAKEN |

### Crossref API Verification Command
```bash
curl -s "https://api.crossref.org/works?query.title=TITLE_HERE&select=DOI,title,author" | jq '.message.items[0]'
```

### Discrepancy Handling
- 著者順序の不一致 → ソースPDFの著者リストを最終的な正とする
- 雑誌名の表記揺れ → ISOの正式略称を採用する
- タイトルの差異 → DOIリンク先のPublisher版を正とする

---

## 7. 助成期間の境界チェック (Grant Period Boundary Enforcement)

### Rule
報告書に記載する出版物の発表日（accepted/published date）が、助成期間内に収まるか自動チェックを行う。

### Grant Period Boundary Calculation
For each active grant, determine the fiscal year boundaries:
```
FY{N}: {N}/04/01 – {N+1}/03/31
```
The grant start/end dates are found in `{GRANT_FOLDER}/Announcement_Rules/*_ketteitsuuchi.pdf`.

### Edge Cases
| Scenario | Allowed? | Handling |
|----------|----------|---------|
| Paper accepted before grant start, published during grant period | ✅ Yes | Note publication date in report |
| Paper submitted during grant period, published after grant end | ✅ Yes (F-19-1) | List as "in press" with expected publication info |
| Paper funded by a different grant, thematically related | 🔷 Related only | Clearly mark as 関連成果, not 直接的成果 |
| Preprint posted during grant period, published version after | ✅ Yes | List published version; if still preprint at F-19-1, list preprint |

---

*Version: 2.0 | Updated: 2026-05-11 | KAKENHI_Pipeline v2.0.0*
