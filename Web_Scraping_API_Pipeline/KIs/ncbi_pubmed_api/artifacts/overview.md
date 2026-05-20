# NCBI PubMed & E-utilities REST API — Comprehensive Reference

## ⚠️ CRITICAL: NCBI Traffic Control Rules

> **The NCBI API is notorious for traffic problems.** Every interaction
> with the E-utilities MUST implement:
> 1. **Rate limiting** — max 3 req/s (default) or 10 req/s (with API key)
> 2. **Exponential backoff** — on 429, 502, 503, and connection resets
> 3. **Batch splitting** — never fetch >500 records in a single call
> 4. **History Server** — always use `usehistory=y` for searches >20 results
> 5. **Off-peak scheduling** — run large jobs on weekends or 9PM–5AM ET
> 6. **HTTP POST** — use POST (not GET) when sending >200 UIDs
>
> Failure to comply **will result in IP blocking** by NCBI.

---

## 1. Overview

### What Are the E-utilities?

The Entrez Programming Utilities (E-utilities) are nine server-side programs
providing a stable REST interface to NCBI's 38+ Entrez databases. They use
a fixed URL syntax and return XML or JSON.

### Base URL

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
```

### The Nine E-utilities

| Utility | URL Suffix | Purpose |
|---------|-----------|---------|
| **EInfo** | `einfo.fcgi` | Database statistics, field lists, available links |
| **ESearch** | `esearch.fcgi` | Text query → list of matching UIDs |
| **EPost** | `epost.fcgi` | Upload UID list to History Server |
| **ESummary** | `esummary.fcgi` | Document summaries for UID list |
| **EFetch** | `efetch.fcgi` | Full data records (abstracts, sequences, XML) |
| **ELink** | `elink.fcgi` | Find linked UIDs across databases |
| **EGQuery** | `egquery.fcgi` | Global query (count hits across all DBs) |
| **ESpell** | `espell.fcgi` | Spelling suggestions |
| **ECitMatch** | `ecitmatch.cgi` | Batch citation → PMID matching |

### Key Databases

| Database | `db=` value | UID Type |
|----------|------------|----------|
| PubMed | `pubmed` | PMID |
| PubMed Central | `pmc` | PMCID |
| Gene | `gene` | Gene ID |
| Nucleotide | `nuccore` | GI / Accession.version |
| Protein | `protein` | GI / Accession.version |
| Structure | `structure` | MMDB-ID |
| Taxonomy | `taxonomy` | TaxID |
| ClinVar | `clinvar` | ClinVar ID |
| GEO Datasets | `gds` | GDS ID |
| GEO Profiles | `geoprofiles` | GEO ID |
| SRA | `sra` | SRA ID |
| BioProject | `bioproject` | BioProject ID |
| BioSample | `biosample` | BioSample ID |

---

## 2. Rate Limits & Traffic Control (⚠️ MOST IMPORTANT SECTION)

### Hard Rate Limits

| Condition | Max Requests/Second | Max Requests/Hour |
|-----------|---------------------|-------------------|
| No API key | **3** | ~10,800 |
| With API key | **10** | ~36,000 |
| Enhanced (by request) | Custom | Custom |

### Mandatory Request Parameters

**Every** E-utility request MUST include:

```
&tool=your_app_name    # No spaces; identifies your software
&email=you@example.com # Valid email; NCBI uses this to contact you
&api_key=XXXXX         # Optional but strongly recommended
```

### How to Get an API Key

1. Create an NCBI account at https://www.ncbi.nlm.nih.gov/account/
2. Go to Settings → API Key Management
3. Generate a key
4. Include `&api_key=YOUR_KEY` in every request

### Rate Limit Error Response

```json
{"error": "API rate limit exceeded", "count": "11"}
```

HTTP Status: `429 Too Many Requests`

### Exponential Backoff Strategy (MANDATORY)

```python
import time
import requests

def ncbi_request(url, max_retries=5):
    """Make an NCBI request with mandatory exponential backoff."""
    for attempt in range(max_retries):
        r = requests.get(url)
        
        if r.status_code == 200:
            return r
        
        if r.status_code == 429:
            # Rate limited — use Retry-After header if available
            wait = float(r.headers.get("Retry-After", 2 ** attempt))
            print(f"  ⚠️ Rate limited — waiting {wait}s (attempt {attempt+1})")
            time.sleep(wait)
            continue
        
        if r.status_code in (500, 502, 503):
            # Server overload — exponential backoff
            wait = min(2 ** attempt, 60)  # Cap at 60s
            print(f"  ⚠️ Server error {r.status_code} — waiting {wait}s")
            time.sleep(wait)
            continue
        
        r.raise_for_status()
    
    raise Exception(f"NCBI request failed after {max_retries} retries: {url}")
```

### Off-Peak Scheduling

For large-scale jobs (>1000 records), schedule during:
- **Weekdays**: 9:00 PM – 5:00 AM Eastern Time
- **Weekends**: Any time

---

## 3. Batch Retrieval Strategies

### ⚠️ The #1 Mistake: Fetching One Record at a Time

**WRONG** (will get you blocked):
```python
for pmid in pmid_list:  # 10,000 PMIDs
    r = requests.get(f"{BASE}/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml")
```

**RIGHT** (use History Server + batching):
```python
# Step 1: Search → post to History Server
r = requests.get(f"{BASE}/esearch.fcgi?db=pubmed&term=YOUR_QUERY"
                 "&usehistory=y&retmax=0")
# Extract WebEnv, query_key, count

# Step 2: Fetch in batches of 500
for start in range(0, total_count, 500):
    r = requests.get(f"{BASE}/efetch.fcgi?db=pubmed"
                     f"&WebEnv={webenv}&query_key={query_key}"
                     f"&retstart={start}&retmax=500&retmode=xml")
    time.sleep(0.34)  # Respect 3 req/s limit
```

### The History Server Pattern

The History Server is NCBI's mechanism for storing UID sets server-side,
avoiding the need to pass thousands of IDs in each URL.

```
┌─────────┐   WebEnv + query_key   ┌──────────┐
│ ESearch  │ ────────────────────► │  History  │
│ or EPost │                       │  Server   │
└─────────┘                        └──────────┘
                                        │
                                        ▼
                               ┌──────────────┐
                               │ EFetch /      │
                               │ ESummary      │
                               │ (with retstart│
                               │  + retmax)    │
                               └──────────────┘
```

### Recommended Batch Sizes

| Operation | Recommended `retmax` | Hard Maximum |
|-----------|---------------------|--------------|
| ESearch (get UIDs) | 10,000 | 10,000 (PubMed/PMC) |
| EFetch (get records) | **200–500** | 10,000 |
| ESummary (get summaries) | **200–500** | 10,000 |
| EPost (upload UIDs) | **500** (for accession IDs) | 10,000 (PMIDs) |

> **Why 500, not 10,000?** While the API _allows_ up to 10,000 per request,
> large batches frequently trigger 502 errors and connection timeouts,
> especially during peak hours. We recommend **200–500** as the sweet spot.

### Batch Size Decision Matrix

| Total Records | Strategy | Batch Size | Sleep Between |
|--------------|----------|-----------|---------------|
| ≤20 | Direct ID list | All at once | N/A |
| 21–200 | Direct ID list (POST) | All at once | N/A |
| 201–10,000 | History Server | 500 | 0.34s |
| 10,001–100,000 | History Server + date segmentation | 500 | 0.5s |
| >100,000 | Download local copy from FTP | N/A | N/A |

### PubMed 10,000 Result Cap

ESearch for PubMed and PMC can only return the first **10,000** UIDs.
To retrieve more:

1. **Date segmentation**: Break query into year/month ranges
2. **EDirect** (NCBI's command-line tool): Has built-in logic for this
3. **FTP bulk download**: For truly massive datasets, use
   https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/ (annual XML files)

```python
def search_pubmed_large(term, total_needed=50000):
    """Handle PubMed's 10K result cap by segmenting by year."""
    all_pmids = []
    current_year = 2026
    
    for year in range(current_year, current_year - 20, -1):
        query = f"{term} AND {year}[pdat]"
        # ESearch with retmax=10000
        r = requests.get(f"{BASE}/esearch.fcgi?db=pubmed&term={query}"
                         "&retmax=10000&retmode=json")
        data = r.json()
        pmids = data["esearchresult"]["idlist"]
        all_pmids.extend(pmids)
        time.sleep(0.34)
        
        if len(all_pmids) >= total_needed:
            break
    
    return all_pmids[:total_needed]
```

---

## 4. ESearch — Text Search

### Basic Syntax

```
esearch.fcgi?db=pubmed&term=QUERY&retmax=N&retmode=json
```

### Common PubMed Search Fields

| Field Tag | Description | Example |
|-----------|-------------|---------|
| `[ti]` | Title | `asthma[ti]` |
| `[tiab]` | Title/Abstract | `CRISPR[tiab]` |
| `[au]` | Author | `Smith J[au]` |
| `[ta]` | Journal abbreviation | `Nature[ta]` |
| `[dp]` | Publication date | `2024[dp]` |
| `[pdat]` | Publication date (for ranges) | `2023/01:2024/06[pdat]` |
| `[mh]` | MeSH term | `neoplasms[mh]` |
| `[pt]` | Publication type | `review[pt]` |
| `[la]` | Language | `english[la]` |
| `[filter]` | Special filters | `free full text[filter]` |

### Boolean Operators (MUST be uppercase)

```
asthma[ti] AND treatment[tiab]
cancer OR tumor OR neoplasm
BRCA2[gene] NOT review[pt]
```

### Proximity Search (PubMed only)

```
"asthma treatment"[Title:~3]    # Terms within 3 words of each other
```

### Date-Limited Search

```
esearch.fcgi?db=pubmed&term=cancer&datetype=pdat&mindate=2024/01/01&maxdate=2024/12/31
esearch.fcgi?db=pubmed&term=stem+cells&reldate=90&datetype=edat   # Last 90 days
```

---

## 5. EFetch — Retrieve Full Records

### PubMed Retrieval Formats

| `rettype` | `retmode` | Output |
|-----------|-----------|--------|
| `abstract` | `text` | Plain text abstract |
| `medline` | `text` | MEDLINE format |
| (default) | `xml` | PubMed XML (full article metadata) |
| (default) | `json` | NOT supported for EFetch |

### PMC Retrieval

```
efetch.fcgi?db=pmc&id=212403              # Full XML article
```

### Gene / Nucleotide / Protein

```
efetch.fcgi?db=gene&id=2&retmode=xml      # Gene record
efetch.fcgi?db=nuccore&id=21614549&rettype=fasta&retmode=text
efetch.fcgi?db=protein&id=8&rettype=gp&retmode=xml
```

---

## 6. EPost — Uploading UID Lists to History Server

### When to Use

- You have a pre-existing list of PMIDs/UIDs (not from an ESearch)
- You need to combine multiple UID sets with Boolean operations
- You're about to perform a batch EFetch/ESummary

### Syntax

```
# POST method (recommended for >200 UIDs)
POST https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi
Content-Type: application/x-www-form-urlencoded

db=pubmed&id=11237011,12466850,15718680,...(up to 10000 PMIDs)
```

### Response

```xml
<ePostResult>
  <QueryKey>1</QueryKey>
  <WebEnv>MCID_12345...</WebEnv>
</ePostResult>
```

### ⚠️ EPost Gotcha for Sequence Databases

When using accession.version identifiers (not GI numbers) with sequence databases:
- There's an internal conversion step that can timeout for large batches
- **Limit to ~500 accession IDs per EPost call** for sequence databases

---

## 7. ESummary — Document Summaries

Returns brief metadata (title, authors, date, source, etc.) without full abstracts.

```
esummary.fcgi?db=pubmed&id=11850928,11482001&retmode=json&version=2.0
```

Use `version=2.0` for richer, database-specific XML.

---

## 8. ELink — Cross-Database Links

| Use Case | URL Pattern |
|----------|-------------|
| PubMed → Gene | `elink.fcgi?dbfrom=pubmed&db=gene&id=PMID` |
| Gene → Protein (RefSeq) | `elink.fcgi?id=GENEID&linkname=gene_protein_refseq` |
| Related articles | `elink.fcgi?dbfrom=pubmed&db=pubmed&id=PMID&cmd=neighbor_score` |
| PubMed → PMC full text | `elink.fcgi?dbfrom=pubmed&db=pmc&id=PMID` |
| Cited by | `elink.fcgi?dbfrom=pubmed&db=pubmed&id=PMID&linkname=pubmed_pubmed_citedin` |

---

## 9. PMC-Specific APIs

### PMC ID Converter API

Converts between PMID, PMCID, DOI, and Manuscript IDs.

```
https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/
  ?ids=PMC3531190,23193287
  &format=json
  &tool=my_tool
  &email=my_email@example.com
```

Response:
```json
{
  "records": [
    {"pmcid": "PMC3531190", "pmid": "23193287", "doi": "10.1093/nar/gks1195"}
  ]
}
```

**Batch limit**: Up to **200 IDs** per request.

### PMC Open Access Web Service

For programmatic retrieval of full-text articles from the Open Access Subset:

```
https://www.ncbi.nlm.nih.gov/pmc/utils/oa/oa.fcgi?id=PMC3531190
```

### PMC BioC API

Machine-readable full text in BioC format (for NLP/text mining):

```
https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC3531190/unicode
```

### Allowed Automated Retrieval Services

Only these services may be used for systematic/bulk retrieval of PMC content:
1. PMC Cloud Service (AWS)
2. PMC OAI-PMH Service
3. PMC FTP Service
4. E-Utilities
5. BioC API

**Any other automated scraping is prohibited.**

---

## 10. Common E-utility Pipelines

### Pipeline 1: Search PubMed → Fetch Abstracts (Basic)

```python
import requests, time, xml.etree.ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PARAMS = "&tool=my_app&email=me@example.com&api_key=MY_KEY"

# Step 1: Search
r = requests.get(f"{BASE}/esearch.fcgi?db=pubmed"
                 f"&term=spatial+transcriptomics[tiab]"
                 f"&usehistory=y&retmax=0&retmode=json{PARAMS}")
data = r.json()["esearchresult"]
total = int(data["count"])
webenv = data["webenv"]
qkey = data["querykey"]
print(f"Found {total} results")

# Step 2: Fetch in batches of 500
batch_size = 500
for start in range(0, total, batch_size):
    r = requests.get(f"{BASE}/efetch.fcgi?db=pubmed"
                     f"&WebEnv={webenv}&query_key={qkey}"
                     f"&retstart={start}&retmax={batch_size}"
                     f"&retmode=xml{PARAMS}")
    # Parse XML...
    root = ET.fromstring(r.text)
    articles = root.findall(".//PubmedArticle")
    for art in articles:
        title = art.findtext(".//ArticleTitle", "")
        pmid = art.findtext(".//PMID", "")
        print(f"  PMID:{pmid} — {title[:80]}")
    
    time.sleep(0.34)  # 3 req/s limit (0.1s with API key)
```

### Pipeline 2: Known PMID List → Full Metadata (EPost → EFetch)

```python
def fetch_by_pmids(pmid_list, batch_size=200):
    """Fetch PubMed records for a known list of PMIDs."""
    results = []
    
    # Step 1: Upload all PMIDs to History Server
    for i in range(0, len(pmid_list), 5000):
        chunk = pmid_list[i:i+5000]
        id_str = ",".join(str(p) for p in chunk)
        
        r = requests.post(f"{BASE}/epost.fcgi",
                          data={"db": "pubmed", "id": id_str})
        root = ET.fromstring(r.text)
        webenv = root.findtext("WebEnv")
        qkey = root.findtext("QueryKey")
        time.sleep(0.34)
        
        # Step 2: Fetch in batches
        for start in range(0, len(chunk), batch_size):
            r = requests.get(f"{BASE}/efetch.fcgi?db=pubmed"
                             f"&WebEnv={webenv}&query_key={qkey}"
                             f"&retstart={start}&retmax={batch_size}"
                             f"&retmode=xml{PARAMS}")
            # Parse and accumulate results
            root = ET.fromstring(r.text)
            articles = root.findall(".//PubmedArticle")
            results.extend(articles)
            time.sleep(0.34)
    
    return results
```

### Pipeline 3: Cross-Database Discovery (PubMed → Gene → Protein)

```python
# Find genes mentioned in a set of papers, then get their proteins
# Step 1: Search PubMed
esearch_url = (f"{BASE}/esearch.fcgi?db=pubmed"
               f"&term=Bglap+AND+osteoblast&usehistory=y"
               f"&retmax=0{PARAMS}")
r = requests.get(esearch_url)
# ... extract webenv, qkey

# Step 2: Link PubMed → Gene
elink_url = (f"{BASE}/elink.fcgi?dbfrom=pubmed&db=gene"
             f"&WebEnv={webenv}&query_key={qkey}"
             f"&cmd=neighbor_history{PARAMS}")
r = requests.get(elink_url)
# ... extract new webenv2, qkey2

# Step 3: Fetch Gene records
efetch_url = (f"{BASE}/efetch.fcgi?db=gene"
              f"&WebEnv={webenv2}&query_key={qkey2}"
              f"&retmode=xml{PARAMS}")
r = requests.get(efetch_url)
```

---

## 11. Biopython Integration

Biopython's `Bio.Entrez` module wraps the E-utilities with built-in
rate limiting and credential management.

```python
from Bio import Entrez, Medline

# MANDATORY: Set credentials
Entrez.email = "your.email@example.com"
Entrez.api_key = "YOUR_API_KEY"  # Increases limit to 10 req/s
Entrez.tool = "spatial_transcriptomics_pipeline"

# Search
handle = Entrez.esearch(db="pubmed", term="Visium HD spatial transcriptomics",
                        retmax=100, usehistory="y")
result = Entrez.read(handle)
count = int(result["Count"])
webenv = result["WebEnv"]
qkey = result["QueryKey"]

# Batch fetch using History Server
batch_size = 200
records = []
for start in range(0, count, batch_size):
    handle = Entrez.efetch(db="pubmed", rettype="medline", retmode="text",
                           retstart=start, retmax=batch_size,
                           webenv=webenv, query_key=qkey)
    batch = Medline.parse(handle)
    records.extend(list(batch))
    handle.close()

print(f"Retrieved {len(records)} records")
for rec in records[:5]:
    print(f"  {rec.get('PMID','?')}: {rec.get('TI','No title')[:80]}")
```

### Biopython Automatic Rate Limiting

`Bio.Entrez` automatically enforces a **0.34s** delay between requests
(3 req/s). With an API key set, it reduces to **0.11s** (10 req/s).

---

## 12. ECitMatch — Citation → PMID Matching

Match partial citations (journal, year, volume, page, author) to PMIDs:

```python
bdata = ("proc+natl+acad+sci+u+s+a|1991|88|3248|mann+bj|Art1|"
         "%0D"
         "science|1987|235|182|palmenberg+ac|Art2|")

r = requests.get(f"{BASE}/ecitmatch.cgi?db=pubmed&retmode=xml"
                 f"&bdata={bdata}{PARAMS}")
# Returns: journal|year|vol|page|author|key|PMID
```

---

## 13. Troubleshooting Guide

| Problem | Cause | Solution |
|---------|-------|----------|
| HTTP 429 | Exceeded 3 req/s (or 10/s with key) | Implement exponential backoff; add `time.sleep()` |
| HTTP 502 Bad Gateway | Server overload | Reduce batch size to 200; retry with backoff; schedule off-peak |
| HTTP 503 Service Unavailable | Temporary maintenance | Wait 5–30 minutes; retry with backoff |
| Connection Reset | URL too long (GET with >200 IDs) | Switch to HTTP POST method |
| Empty results | Incorrect field tags or DB name | Use EInfo to check valid fields; verify `db=` value |
| Partial results from EPost | Accession ID conversion timeout | Batch accession IDs in groups of ≤500 |
| ESearch returns max 10,000 | PubMed/PMC hard cap | Use date segmentation or EDirect |
| XML parsing errors | Malformed response from timeout | Validate XML before parsing; retry on parse failure |
| IP blocked | Persistent policy violation | Register `tool` + `email` with NCBI at eutilities@ncbi.nlm.nih.gov |
| `{"error":"..."}` JSON response | Invalid parameters | Check parameter names (lowercase); verify db name |
| Stale WebEnv | History Server session expired | WebEnv is valid for ~20 minutes; re-search if expired |

### Emergency: IP Has Been Blocked

1. Email `eutilities@ncbi.nlm.nih.gov` with your registered `tool` and `email` values
2. Explain what happened and what you've fixed
3. NCBI will unblock after verifying compliance

---

## 14. PMC FTP Bulk Data

For massive-scale work (>100K articles), use FTP instead of the API:

| Dataset | URL | Format |
|---------|-----|--------|
| PubMed baseline | `ftp.ncbi.nlm.nih.gov/pubmed/baseline/` | Compressed XML (annual) |
| PubMed daily updates | `ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/` | Compressed XML |
| PMC Open Access | `ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/` | XML/PDF bundles |
| PMC Author Manuscripts | `ftp.ncbi.nlm.nih.gov/pub/pmc/manuscript/` | XML bundles |
| Gene data | `ftp.ncbi.nlm.nih.gov/gene/DATA/` | Tabular files |

---

## 15. Quick Reference Card

### Minimum Viable PubMed Search

```python
import requests, time

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
TOOL = "my_app"
EMAIL = "me@example.com"

def pubmed_search(query, max_results=100):
    """Search PubMed and return PMIDs with rate limiting."""
    url = (f"{BASE}/esearch.fcgi?db=pubmed"
           f"&term={query}&retmax={max_results}"
           f"&retmode=json&tool={TOOL}&email={EMAIL}")
    r = requests.get(url)
    r.raise_for_status()
    return r.json()["esearchresult"]["idlist"]

def fetch_abstracts(pmids, batch=200):
    """Fetch abstracts for a list of PMIDs with batching."""
    all_text = []
    for i in range(0, len(pmids), batch):
        chunk = pmids[i:i+batch]
        url = (f"{BASE}/efetch.fcgi?db=pubmed"
               f"&id={','.join(chunk)}&rettype=abstract"
               f"&retmode=text&tool={TOOL}&email={EMAIL}")
        r = requests.get(url)
        all_text.append(r.text)
        time.sleep(0.34)
    return "\n".join(all_text)
```

---

## 16. References

- [E-utilities Overview (NBK25497)](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
- [E-utilities In-Depth Parameters (NBK25499)](https://www.ncbi.nlm.nih.gov/books/NBK25499/)
- [E-utilities Quick Start (NBK25500)](https://www.ncbi.nlm.nih.gov/books/NBK25500/)
- [PMC Developer Portal](https://pmc.ncbi.nlm.nih.gov/tools/developers/)
- [PMC ID Converter API](https://pmc.ncbi.nlm.nih.gov/tools/id-converter-api/)
- [Biopython Entrez Module](https://biopython.org/wiki/Entrez)
- [PubMed FTP Baseline](https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/)
- [EDirect (command-line E-utilities)](https://www.ncbi.nlm.nih.gov/books/NBK179288/)
