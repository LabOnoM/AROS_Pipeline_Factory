# Skill: Researcher Data Collection & Profile Refresh

> **Purpose**: Systematically collect, verify, and update researcher academic profile data from authoritative sources for KAKENHI grant reporting.
> **Target Profile**: `ResearcherMetaInfo/{PI_FILE}.md`
> **Refresh Trigger**: Mandatory within 30 days of any report submission deadline

---

## 1. 3-Tier Collection Strategy

### Tier 1: URL Scraping (Default)
**Tool**: `read_url_content`
**Suitable for**: Static HTML pages, publicly accessible profiles

```bash
# researchmap
read_url_content("{PI_RESEARCHMAP_URL}")

# ORCID  
read_url_content("https://orcid.org/{PI_ORCID}")

# J-GLOBAL
read_url_content("{PI_JGLOBAL_URL}")

# KAKEN
read_url_content("https://kaken.nii.ac.jp/ja/grant/KAKENHI-PROJECT-{GRANT_ID}/")

# Institutional database (e.g., SORAN, researcherDB)
read_url_content("{PI_INSTITUTIONAL_URL}")
```

### Tier 2: Browser Automation (Fallback)
**Tool**: `browser_subagent`
**Use when**: Tier 1 fails due to JS rendering, AJAX pagination, CAPTCHAs, or login requirements

```
Typical Tier 2 scenarios:
- Google Scholar: pagination of publication list (AJAX)
- researchmap: MISC/presentations tab (dynamic loading)
- Web of Science: requires session authentication
```

**Browser Subagent Task Template**:
```
Navigate to [URL]. Wait for the page to fully load (including AJAX content).
Extract all [publications/presentations/awards] visible on the page.
If there is pagination, click through all pages and collect all entries.
Return the data as structured JSON with fields: title, authors, journal, year, DOI.
```

### Tier 3: API (Future Enhancement)
**Tool**: HTTP API calls
**Prerequisites**: JST application for researchmap v2 API access (利用申請書 required)
**Endpoint pattern**: `https://api.researchmap.jp/{permalink}/{achievement_type}`
**Status**: Not yet applied — document for future use

---

## 2. Data Categories to Collect

| Category | KAKENHI Classification | Sources | Notes |
|----------|----------------------|---------|-------|
| Journal Articles | 雑誌論文 | researchmap, ORCID, Google Scholar | Must include DOI |
| Preprints | 雑誌論文 (査読: 無) | bioRxiv, ORCID | Dedup when published version exists |
| Conference Abstracts | MISC | researchmap, J-GLOBAL | NOT 雑誌論文 even if published in journal supplement |
| Oral Presentations | 学会発表 | researchmap | Include: invited/oral/poster distinction |
| Books/Chapters | 図書 | researchmap, ORCID | Rarely applicable |
| Awards | 受賞 | researchmap | Include: date, organization, title |
| Software/Works | 作品等 | researchmap, GitHub | Include: ShinyApp, R packages |
| Grants (PI) | 研究代表者 | KAKEN | Include: ID, period, type, title |
| Grants (Co-I) | 研究分担者 | KAKEN | Include: PI name, role |
| Peer Review | 査読活動 | researchmap | Include: journal, period |
| Teaching | 担当授業 | Institutional DB | Verify current semester |
| Society Memberships | 所属学協会 | researchmap | Include: active/expired |

---

## 3. Cross-Reference & Deduplication

### DOI Verification (Mandatory for every new paper)
```bash
curl -s "https://api.crossref.org/works?query.title=TITLE_HERE&select=DOI,title,author" | jq '.message.items[0]'
```

### Deduplication Priority
1. **DOI match** — identical DOI = same paper
2. **Title fuzzy match** — >90% string similarity + same year = likely duplicate
3. **Author list match** — identical first author + year + journal = likely duplicate

### Preprint → Published Paper Deduplication
- When a preprint (bioRxiv) gets a peer-reviewed version published:
  - **Remove** the preprint entry
  - **Replace** with the published version
  - **Do NOT** list both simultaneously (Policy P1.3)

### MISC vs. Journal Article Classification
> **CRITICAL**: Conference abstracts published in journal supplements (e.g., ASBMR abstracts in JBMR) are classified as **MISC** (その他), NOT 雑誌論文, per KAKENHI reporting standards.

---

## 4. KAKEN Database Cross-Reference

After refreshing the local profile, compare against the KAKEN database:

1. **Navigate**: `https://kaken.nii.ac.jp/ja/grant/KAKENHI-PROJECT-{GRANT_ID}/`
2. **Count**: Number of 雑誌論文, 学会発表, 図書, 備考 registered
3. **Compare**: Against `{GRANT_ID}_Achievements_List.md` entries
4. **Flag**: Any KAKEN-registered outputs missing from local records
5. **Reconcile**: Add missing entries to `{PI_FILE}.md` + `{GRANT_ID}_Achievements_List.md`

---

## 5. Output Checklist

After completing a profile refresh:

- [ ] `{PI_FILE}.md` updated with all new entries
- [ ] `{GRANT_ID}_Achievements_List.md` updated for relevant grant(s)
- [ ] `Publication_Grant_Map.md` updated with grant attribution for new papers
- [ ] Crossref DOI verification completed for all new entries
- [ ] KAKEN cross-reference completed (no unaccounted outputs)
- [ ] Deduplication check passed (no preprint + published duplicates)
- [ ] MISC vs. journal article classification verified
- [ ] Last-updated timestamp changed in `{PI_FILE}.md`

---

*Last updated: 2026-05-11 | KAKENHI_Pipeline v2.0.0*
