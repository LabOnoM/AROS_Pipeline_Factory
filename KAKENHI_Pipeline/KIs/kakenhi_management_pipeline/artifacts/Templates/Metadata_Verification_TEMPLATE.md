# Metadata Verification Log — {GRANT_ID}

> **Purpose**: Track Crossref DOI verification and multi-source metadata cross-checks for all publications attributed to this grant.
> **Policy Reference**: fact_check_policy.md §6 (Multi-Source Cross-Verification)
> **Last Updated**: {DATE}

---

## Verification Matrix

| # | Publication | DOI | Crossref ✓ | researchmap ✓ | ORCID ✓ | KAKEN ✓ | PDF Acknowledgment ✓ | Status |
|---|-------------|-----|-----------|--------------|---------|---------|---------------------|--------|
| 1 | | | ☐ | ☐ | ☐ | ☐ | ☐ | Pending |

---

## Verification Commands Used

```bash
# Crossref DOI verification
curl -s "https://api.crossref.org/works?query.title=TITLE&select=DOI,title,author" | jq '.message.items[0]'

# Direct DOI lookup
curl -s "https://api.crossref.org/works/{DOI}" | jq '.message | {title, author, "container-title", volume, issue, page, published}'
```

---

## Discrepancy Log

| Publication | Field | Source A Value | Source B Value | Resolution |
|-------------|-------|---------------|---------------|------------|
| | | | | |

---

*Template from KAKENHI_Pipeline v2.0.0*
