---
name: clinvar-database
description: Use when needing clinical significance, pathogenicity classifications
  (e.g., Pathogenic, Benign, VUS), clinical evidence rationales, or finding "hard
  positive" benchmark controls for human genomic variants.
license: MIT
metadata:
  skill-author: K-Dense Inc. and AIPOCH
---

## Overview

ClinVar is NCBI's freely accessible archive of reports on relationships between human genetic variants and phenotypes, with supporting evidence. The database aggregates information about genomic variation and its relationship to human health, providing standardized variant classifications used in clinical genetics and research.

## When to Use This Skill

This skill should be used when:

- Searching for variants by gene, condition, or clinical significance.
- Interpreting clinical significance classifications (pathogenic, benign, VUS).
- Accessing ClinVar data programmatically via E-utilities API.
- Downloading and processing bulk data from FTP.
- Understanding review status and star ratings.
- Resolving conflicting variant interpretations.
- Annotating variant call sets with clinical significance.
- Performing bulk retrieval of ClinVar datasets for offline analysis or periodic database refresh.

## Core Capabilities

### 1. Search and Query ClinVar

#### Web Interface Queries

Search ClinVar using the web interface at https://www.ncbi.nlm.nih.gov/clinvar/

**Common search patterns:**
- By gene: `BRCA1[gene]`
- By clinical significance: `pathogenic[CLNSIG]`
- By condition: `breast cancer[disorder]`
- By variant: `NM_000059.3:c.1310_1313del[variant name]`
- By chromosome: `13[chr]`
- Combined: `BRCA1[gene] AND pathogenic[CLNSIG]`

#### Programmatic Access via E-utilities

Access ClinVar programmatically using NCBI's E-utilities API. Refer to `references/api_reference.md` for comprehensive API documentation including:
- **esearch** - Search for variants matching criteria
- **esummary** - Retrieve variant summaries
- **efetch** - Download full XML records
- **elink** - Find related records in other NCBI databases

**Quick example using curl:**
```bash
# Search for pathogenic BRCA1 variants
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1[gene]+AND+pathogenic[CLNSIG]&retmode=json"
```

**Best practices:**
- Test queries on the web interface before automating.
- Use API keys to increase rate limits from 3 to 10 requests/second.
- Implement exponential backoff for rate limit errors.
- Set `Entrez.email` when using Biopython.

### 2. Interpret Clinical Significance

#### Understanding Classifications

ClinVar uses standardized terminology for variant classifications. Refer to `references/clinical_significance.md` for detailed interpretation guidelines.

**Key germline classification terms (ACMG/AMP):**
- **Pathogenic (P)** - Variant causes disease (~99% probability)
- **Likely Pathogenic (LP)** - Variant likely causes disease (~90% probability)
- **Uncertain Significance (VUS)** - Insufficient evidence to classify
- **Likely Benign (LB)** - Variant likely does not cause disease
- **Benign (B)** - Variant does not cause disease

**Review status (star ratings):**
- ★★★★ Practice guideline - Highest confidence
- ★★★ Expert panel review (e.g., ClinGen) - High confidence
- ★★ Multiple submitters, no conflicts - Moderate confidence
- ★ Single submitter with criteria - Standard weight
- ☆ No assertion criteria - Low confidence

**Critical considerations:**
- Always check review status - prefer ★★★ or ★★★★ ratings.
- Conflicting interpretations require manual evaluation.
- Classifications may change as new evidence emerges.
- VUS (uncertain significance) variants lack sufficient evidence for clinical use.

### 3. Download Bulk Data from FTP

#### Access ClinVar FTP Site

Download complete datasets from `ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/`

Refer to `references/data_formats.md` for comprehensive documentation on file formats and processing.

**Update schedule:**
- Monthly releases: First Thursday of each month (complete dataset, archived)
- Weekly updates: Every Monday (incremental updates)

#### Available Formats

**XML files** (most comprehensive):
- VCV (Variation) files: `xml/clinvar_variation/` - Variant-centric aggregation
- RCV (Record) files: `xml/RCV/` - Variant-condition pairs
- Include full submission details, evidence, and metadata

**VCF files** (for genomic pipelines):
- GRCh37: `vcf_GRCh37/clinvar.vcf.gz`
- GRCh38: `vcf_GRCh38/clinvar.vcf.gz`
- Limitations: Excludes variants >10kb and complex structural variants

**Tab-delimited files** (for quick analysis):
- `tab_delimited/variant_summary.txt.gz` - Summary of all variants
- `tab_delimited/var_citations.txt.gz` - PubMed citations
- `tab_delimited/cross_references.txt.gz` - Database cross-references

**Example download:**
```bash
# Download latest monthly XML release
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_00-latest.xml.gz

# Download VCF for GRCh38
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
```

### 4. Process and Analyze ClinVar Data

#### Working with XML Files

Process XML files to extract variant details, classifications, and evidence.

**Python example with xml.etree:**
```python
import gzip
import xml.etree.ElementTree as ET

with gzip.open('ClinVarVariationRelease.xml.gz', 'rt') as f:
    for event, elem in ET.iterparse(f, events=('end',)):
        if elem.tag == 'VariationArchive':
            variation_id = elem.attrib.get('VariationID')
            # Extract clinical significance, review status, etc.
            elem.clear()  # Free memory
```

#### Working with VCF Files

Annotate variant calls or filter by clinical significance using bcftools or Python.

**Using bcftools:**
```bash
# Filter pathogenic variants
bcftools view -i 'INFO/CLNSIG~"Pathogenic"' clinvar.vcf.gz

# Extract specific genes
bcftools view -i 'INFO/GENEINFO~"BRCA"' clinvar.vcf.gz

# Annotate your VCF with ClinVar
bcftools annotate -a clinvar.vcf.gz -c INFO your_variants.vcf
```

**Using PyVCF in Python:**
```python
import vcf

vcf_reader = vcf.Reader(filename='clinvar.vcf.gz')
for record in vcf_reader:
    clnsig = record.INFO.get('CLNSIG', [])
    if 'Pathogenic' in clnsig:
        gene = record.INFO.get('GENEINFO', [''])[0]
        print(f"{record.CHROM}:{record.POS} {gene} - {clnsig}")
```

#### Working with Tab-Delimited Files

Use pandas or command-line tools for rapid filtering and analysis.

**Using pandas:**
```python
import pandas as pd

# Load variant summary
df = pd.read_csv('variant_summary.txt.gz', sep='\t', compression='gzip')

# Filter pathogenic variants in specific gene
pathogenic_brca = df[
    (df['GeneSymbol'] == 'BRCA1') &
    (df['ClinicalSignificance'].str.contains('Pathogenic', na=False))
]

# Count variants by clinical significance
sig_counts = df['ClinicalSignificance'].value_counts()
```

**Using command-line tools:**
```bash
# Extract pathogenic variants for specific gene
zcat variant_summary.txt.gz | \
  awk -F'\t' '$7=="TP53" && $13~"Pathogenic"' | \
  cut -f1,5,7,13,14
```

### 5. Handle Conflicting Interpretations

When multiple submitters provide different classifications for the same variant, ClinVar reports "Conflicting interpretations of pathogenicity."

**Resolution strategy:**
1. Check review status (star rating) - higher ratings carry more weight.
2. Examine evidence and assertion criteria from each submitter.
3. Consider submission dates - newer submissions may reflect updated evidence.
4. Review population frequency data (e.g., gnomAD) for context.
5. Consult expert panel classifications (★★★) when available.
6. For clinical use, always defer to a genetics professional.

**Search query to exclude conflicts:**
```
TP53[gene] AND pathogenic[CLNSIG] NOT conflicting[RVSTAT]
```

### 6. Track Classification Updates

Variant classifications may change over time as new evidence emerges.

**Why classifications change:**
- New functional studies or clinical data.
- Updated population frequency information.
- Revised ACMG/AMP guidelines.
- Segregation data from additional families.

**Best practices:**
- Document ClinVar version and access date for reproducibility.
- Re-check classifications periodically for critical variants.
- Subscribe to ClinVar mailing list for major updates.
- Use monthly archived releases for stable datasets.

### 7. Submit Data to ClinVar

Organizations can submit variant interpretations to ClinVar.

**Submission methods:**
- Web submission portal: https://submit.ncbi.nlm.nih.gov/subs/clinvar/
- API submission (requires service account): See `references/api_reference.md`
- Batch submission via Excel templates

**Requirements:**
- Organizational account with NCBI.
- Assertion criteria (preferably ACMG/AMP guidelines).
- Supporting evidence for classification.

Contact: clinvar@ncbi.nlm.nih.gov for submission account setup.

## Example Usage
### 1) Search ClinVar for pathogenic variants in a gene

```bash
python scripts/search.py --term "BRCA1[gene] AND pathogenic[CLNSIG]"
```

### 2) Annotate a VCF with ClinVar data

```bash
python scripts/annotate.py --input input.vcf --output annotated.vcf
```

## Implementation Details
- **Search (`scripts/search.py`)**
  - Uses **NCBI E-utilities** to query ClinVar with a user-provided `--term`.
  - The query term supports ClinVar/Entrez syntax (e.g., `BRCA1[gene]`, `pathogenic[CLNSIG]`) to filter by gene and clinical significance.
  - Output is expected to include matching ClinVar records/identifiers suitable for follow-up interpretation or annotation.

- **Interpretation fields**
  - Clinical significance values (e.g., Pathogenic/Benign/VUS) and related interpretation guidance follow ClinVar conventions; see `references/clinical_significance.md`.
  - Review status (e.g., level of evidence/review) is retrieved alongside significance where available.

- **VCF annotation (`scripts/annotate.py`)**
  - Takes an input VCF (`--input`) and produces an annotated VCF (`--output`).
  - Integrates with `bcftools` to add ClinVar-derived annotations to variant records (requires `bcftools` installed and available on `PATH`).
  - Designed for pipeline use: deterministic input/output files and command-line parameters.

## Workflow Examples

### Example 1: Identify High-Confidence Pathogenic Variants in a Gene

**Objective:** Find pathogenic variants in CFTR gene with expert panel review.

**Steps:**
1. Search using web interface or E-utilities:
   ```
   CFTR[gene] AND pathogenic[CLNSIG] AND (reviewed by expert panel[RVSTAT] OR practice guideline[RVSTAT])
   ```
2. Review results, noting review status (should be ★★★ or ★★★★)
3. Export variant list or retrieve full records via efetch
4. Cross-reference with clinical presentation if applicable

### Example 2: Annotate VCF with ClinVar Classifications

**Objective:** Add clinical significance annotations to variant calls.

**Steps:**
1. Download appropriate ClinVar VCF (match genome build: GRCh37 or GRCh38):
   ```bash
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi
   ```
2. Annotate using bcftools:
   ```bash
   bcftools annotate -a clinvar.vcf.gz \
     -c INFO/CLNSIG,INFO/CLNDN,INFO/CLNREVSTAT \
     -o annotated_variants.vcf \
     your_variants.vcf
   ```
3. Filter annotated VCF for pathogenic variants:
   ```bash
   bcftools view -i 'INFO/CLNSIG~"Pathogenic"' annotated_variants.vcf
   ```

### Example 3: Analyze Variants for a Specific Disease

**Objective:** Study all variants associated with hereditary breast cancer.

**Steps:**
1. Search by condition:
   ```
   hereditary breast cancer[disorder] OR "Breast-ovarian cancer, familial"[disorder]
   ```
2. Download results as CSV or retrieve via E-utilities
3. Filter by review status to prioritize high-confidence variants
4. Analyze distribution across genes (BRCA1, BRCA2, PALB2, etc.)
5. Examine variants with conflicting interpretations separately

### Example 4: Bulk Download and Database Construction

**Objective:** Build a local ClinVar database for analysis pipeline.

**Steps:**
1. Download monthly release for reproducibility:
   ```bash
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_YYYY-MM.xml.gz
   ```
2. Parse XML and load into database (PostgreSQL, MySQL, MongoDB)
3. Index by gene, position, clinical significance, review status
4. Implement version tracking for updates
5. Schedule monthly updates from FTP site

## Important Limitations and Considerations

### Data Quality
- **Not all submissions have equal weight** - Check review status (star ratings).
- **Conflicting interpretations exist** - Require manual evaluation.
- **Historical submissions may be outdated** - Newer data may be more accurate.
- **VUS classification is not a clinical diagnosis** - Means insufficient evidence.

### Scope Limitations
- **Not for direct clinical diagnosis** - Always involve genetics professional.
- **Population-specific** - Variant frequencies vary by ancestry.
- **Incomplete coverage** - Not all genes or variants are well-studied.
- **Version dependencies** - Coordinate genome build (GRCh37/GRCh38) across analyses.

### Technical Limitations
- **VCF files exclude large variants** - Variants >10kb not in VCF format.
- **Rate limits on API** - 3 req/sec without key, 10 req/sec with API key.
- **File sizes** - Full XML releases are multi-GB compressed files.
- **No real-time updates** - Website updated weekly, FTP monthly/weekly.

## Dependencies

- Python `>=3.8`
- `requests` (Python package)
- `bcftools` (system dependency; required for VCF annotation)
- `pandas` (Python package; optional for downstream data processing)

## Resources

### Reference Documentation

This skill includes comprehensive reference documentation:

- **`references/api_reference.md`** - Complete E-utilities API documentation with examples for esearch, esummary, efetch, and elink; includes rate limits, authentication, and Python/Biopython code samples

- **`references/clinical_significance.md`** - Detailed guide to interpreting clinical significance classifications, review status star ratings, conflict resolution, and best practices for variant interpretation

- **`references/data_formats.md`** - Documentation for XML, VCF, and tab-delimited file formats; FTP directory structure, processing examples, and format selection guidance

### External Resources

- ClinVar home: https://www.ncbi.nlm.nih.gov/clinvar/
- ClinVar documentation: https://www.ncbi.nlm.nih.gov/clinvar/docs/
- E-utilities documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- ACMG variant interpretation guidelines: Richards et al., 2015 (PMID: 25741868)
- ClinGen expert panels: https://clinicalgenome.org/

### Contact

For questions about ClinVar or data submission: clinvar@ncbi.nlm.nih.gov

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://www.ncbi.nlm.nih.gov/clinvar/, then (2) create the file recording
    the notification text and timestamp.
3.  **`.env` file**: Make sure the `.env` file exists in your home directory.
    Create one if it does not exist.
4.  **`NCBI_API_KEY`** (optional): Raises the NCBI rate limit from 3 to 10
    requests/second. The skill works without it, but a key is recommended if the
    user plans many queries or encounters a 429 error. The user can obtain one
    for free by registering at https://www.ncbi.nlm.nih.gov/account/settings/.
    If the variable is missing from `.env`, do NOT ask the user to paste it into
    the chat (this would leak the key into the agent's context). Instead, give
    the user this command — **substituting `ENV_FILE` with the resolved literal
    path to the `.env` file**:

    ```bash
    printf "Enter NCBI API key (typing hidden): " && read -s key && echo && echo "NCBI_API_KEY=$key" >> "ENV_FILE" && echo "Saved."
    ```

    The scripts load credentials automatically via `dotenv`. **NEVER** read,
    print, or inspect the `.env` file or its variables (e.g. no `cat`, `grep`,
    `echo`, `printenv`, or `os.environ.get` on keys). Credentials must stay out
    of the agent's context. See the
    [API Key section](#obtaining-and-using-an-api-key) for more details.

## Overview

ClinVar is the primary consensus record for clinical classifications of human
genomic variations. It provides the "clinical ground truth" for pathogenicity
labels (Pathogenic, Likely Pathogenic, Benign, VUS) based on assertions from
global laboratories.

## When to Use

**Use when you need to:**

-   Find the current clinical significance and star rating (review status) for a
    specific variant.
-   Fetch clinician notes, assertion criteria, or rationales for previous
    clinical laboratory classifications.
-   Retrieve the preferred condition name and associated HPO terms for a
    specific variant.
-   Find a list of variant controls (e.g., "Find all Pathogenic variants in the
    HBB gene within 50bp of a signal").
-   Check for conflicting interpretations for a given variant and identify the
    organizations submitting each classification.

**Do NOT use when you need to:**

-   Find specific allele frequencies in global populations (use **gnomAD**).
-   Describe the normal biological role of a protein and typical inheritance
    patterns (use **OMIM**).
-   Predict mechanistic effects of novel mutations, like frameshifts or exon
    skipping (use **AlphaGenome**).
-   Find recommended surveillance schedules for patients with a pathogenic
    variant (use **GeneReviews**).
-   Generate or view 3D structural models of affected proteins (use **PDB /
    AlphaFold**).

## Quick Start

ClinVar queries are executed via a robust Python wrapper script to handle strict
rate limiting and XML/JSON parsing.

Example: Search for BRCA1 variants

```bash
uv run scripts/clinvar_api.py search --query "BRCA1[gene]" --output results.json
```

## Core Rules

-   **Retmax Constraint**: The search command defaults to `--retmax 200`. For
    any "List all" or gene-wide request, you MUST explicitly set `--retmax`
    higher (e.g., 1000) to ensure data completeness.
-   **Use the Wrapper**: Prefer the wrapper script for standard queries. It
    handles rate limiting, retries, and the complex XML parsing for you. If the
    script's parsed output does not contain the specific fields you need, you
    may modify the script or query the NCBI E-utilities API directly — but be
    aware that the raw XML schemas are complex and vary between record types.
-   If the rate limit is hit, the script will throw a clear error. Follow the
    prerequisite instructions above to help the user add `NCBI_API_KEY` to the
    `.env` file.
-   **Notification**: If this skill is used, ensure this is mentioned in the
    output.

## Utility Scripts

### 1. `count` — Count Matching Variants

**Purpose:** Check how many variants match a query without fetching IDs. Use to
decide whether a full `search` is warranted.

*Arguments:*

-   `--query`: (Required) NCBI Entrez search query string.
-   `--output`: (Required) Output JSON file path.

*Example:* `uv run scripts/clinvar_api.py count \ --query "TP53[gene] AND
\"uncertain significance\"[clinsig]" \ --output count.json` *Output:*
`{"total_count": <int>}`

### 2. `search` — Search Variants

**Purpose:** Identify variants based on genomic location, gene symbols, or
clinical attributes using NCBI Entrez search syntax. The search command
**automatically paginates** through all matching results to ensure complete,
deterministic retrieval.

```bash
# Fetch ALL matching variants (default behavior)
uv run scripts/clinvar_api.py search \
  --query "BRCA1[gene]" --output results.json

# Search by Chromosome and Position Range
uv run scripts/clinvar_api.py search \
  --query "11[chr] AND 5225000:5226000[chrpos]" --output results.json

# Combine terms using Entrez syntax
uv run scripts/clinvar_api.py search \
  --query "HBB[gene] AND pathogenic[clinsig]" --output results.json

# Cap results at 50
uv run scripts/clinvar_api.py search \
  --query "TP53[gene]" --retmax 50 --output results.json
```

*Arguments:*

-   `--query`: (Required) NCBI Entrez search query string.
-   `--retmax`: Maximum total number of variant IDs to return. **Default is 0,
    which means "fetch all matching results."** Set to a positive integer to cap
    the result set.
-   `--page_size`: Number of IDs to fetch per API request (default: 500, max:
    10000 per NCBI limits).
-   `--output`: (Required) Output JSON file path.

*Output:* A JSON object containing:

-   `total_count` — Total number of matching variants in ClinVar.
-   `fetched_count` — Number of IDs actually retrieved.
-   `variant_ids` — List of ClinVar Variation ID strings.

### 3. `summary` — Get Interpretation Summary

**Purpose:** Retrieve top-line clinical significance labels, star ratings
(review status), and basic phenotype data for rapid variant screening.

```bash
# Get summary for one or more Variation IDs
uv run scripts/clinvar_api.py summary \
  --variant_ids 12345 67890 --output summary.json
```

*Arguments:*

-   `--variant_ids`: (Required) One or more ClinVar Variation IDs.
-   `--output`: (Required) Output JSON file path.

*Output:* A JSON list of summary objects, each containing:

-   `variant_id`, `title`, `clinical_significance`, `review_status`, \
    `last_evaluated`, `phenotypes`
-   `genes` — list of `{gene_id, symbol, strand}`
-   `variation_type` — e.g., single nucleotide variant, Deletion, Insertion
-   `molecular_consequences` — list of strings (e.g., ["missense variant", \
    "nonsense"])

### 4. `evidence` — Get Clinical Evidence

**Purpose:** Fetch the full clinical record for a single variant, including
free-text clinician rationales, assertion methods, and specific submitter notes.

```bash
# Get full evidence for a single Variation ID
uv run scripts/clinvar_api.py evidence \
  --variant_id 12345 --output evidence.json
```

*Arguments:*

-   `--variant_id`: (Required) A single ClinVar Variation ID.
-   `--output`: (Required) Output JSON file path.

*Output:* A JSON object containing:

-   `variant_id`
-   `allele_info` — `{chromosome, position_start, position_stop,
    reference_allele, alternate_allele, cytogenetic_band, dbsnp_rsid}` (GRCh38
    preferred)
-   `conditions` — list of `{name, medgen_cui, omim_id, orphanet_id, hpo_terms}`
-   `functional_consequences` — list of `{value, sequence_ontology_id}`
-   `structural_variant_details` — `{outer_start, inner_start, inner_stop,
    outer_stop, copy_number}` (present only for CNVs, otherwise null)
-   `citation_references` — list of PubMed IDs cited in the global "Citations"
    section
-   `submissions` — list of per-submitter records, each containing:
    -   `submitter_name`, `classification`, `curator_notes`,
        `assertion_criteria`
    -   `date_last_evaluated` — when the submitter last reviewed the
        classification

## Typical Workflows

### Count-First Workflow (Recommended)

For large or unknown result sets, use `count` first to decide whether to
proceed, then `search` (which auto-paginates and returns `total_count` /
`fetched_count`), then `summary` to screen.

```bash
# Step 1: Gauge size (optional — search also returns total_count)
uv run scripts/clinvar_api.py count \
  --query "HBB[gene] AND pathogenic[clinsig]" --output count.json

# Step 2: Fetch all variant IDs (auto-paginates)
uv run scripts/clinvar_api.py search \
  --query "HBB[gene] AND pathogenic[clinsig]" --output ids.json

# Step 3: Get summaries (extract variant_ids from search output)
uv run scripts/clinvar_api.py summary \
  --variant_ids 12345 67890 --output summary.json
```

### Deep Dive: search → evidence

When you need the full clinical picture for a specific variant — including
submitter rationales, PubMed citations, ontology-linked conditions, and allele
coordinates — use `evidence`.

```bash
uv run scripts/clinvar_api.py evidence \
  --variant_id 12345 --output evidence.json
```

### Workflow: Robust Variant Discovery (Triangulation)

ClinVar metadata is inconsistent. To fulfill "List all" requests, do not rely on
a single filter. Perform the following in a single turn and merge results:

1.  **Search by exact label** (e.g., `"3 prime UTR
    variant"[molecular_consequence]`).
2.  **Search by HGVS nomenclature pattern** (e.g., `c.*`).
3.  **Search by genomic coordinate range** (using `[chrpos]`).

This "triangulation" ensures structural variants with missing labels are not
overlooked.

### Verifying Coding vs. Non-Coding Status via HGVS

`molecular_consequences` alone can be ambiguous (e.g., `splice donor variant`
appears in both coding and non-coding contexts). Always cross-check the `title`
field for HGVS patterns:

-   `c.-…` — 5' UTR (non-coding)
-   `c.*…` — 3' UTR (non-coding)
-   `c.123+N` / `c.123-N` — intronic (non-coding)
-   `p.Trp146Arg` etc. — protein effect (coding)

A variant with UTR/intronic HGVS and no `p.` annotation is non-coding, even with
splicing labels. Conversely, any `p.` annotation indicates a coding effect.

### ClinVar Metadata Reference

-   **3' UTR**
    -   Search String: `"3 prime UTR variant"[mol_consequence]`
    -   HGVS: `c.*`
-   **5' UTR**
    -   Search String: `"5 prime UTR variant"[mol_consequence]`
    -   HGVS: `c.-`
-   To find "high-confidence" variants or expert-reviewed consensus, use the
    `review_status` filter. This is the most efficient way to distinguish
    between single-laboratory assertions and panel-reviewed ground truth.

### When to Use Which Fields

-   **Quick pathogenicity label** — Use `summary` → `clinical_significance`
-   **Gene symbol and strand** — Use `summary` → `genes`
-   **Variant type (SNV, del, etc.)** — Use `summary` → `variation_type`
-   **Protein-level effect** — Use `summary` → `molecular_consequences`
-   **Genomic coordinates (GRCh38)** — Use `evidence` → `allele_info`
-   **Linked conditions (ontology)** — Use `evidence` → `conditions`
-   **SO functional consequence** — Use `evidence` → `functional_consequences`
-   **CNV breakpoints/copy number** — Use `evidence` →
    `structural_variant_details`
-   **PubMed references** — Use `evidence` → `citation_references`
-   **Date of last lab review** — Use both → `last_evaluated`
-   **Clinician rationales** — Use `evidence` → `submissions[].curator_notes`

### Retrieving Genomic Coordinates (Default HG38/GRCh38)

To get precise genomic coordinates in the format `<chrom>:<pos>:<ref>><alt>`
(e.g., `chr5:70951945:G>A`), you must use the `evidence` command, as these
details are not available in the `summary` output.

**You MUST always include genomic coordinates in the format
`<chrom>:<pos>:<ref>><alt>` when listing or presenting variants, even if not
explicitly requested by the user. If coordinates are missing from the summary,
use the `evidence` command or dbSNP fallback to retrieve them.**

1.  **Fetch Evidence**: Use `uv run scripts/clinvar_api.py evidence --variant_id
    <ID> --output evidence.json`.
2.  **Extract VCF Attributes**: The `evidence` command parses the XML. Extract:
    *   Chromosome: `Chr`
    *   Position: `positionVCF` (or `start`)
    *   Ref: `referenceAlleleVCF` (or `referenceAllele`)
    *   Alt: `alternateAlleleVCF` (or `alternateAllele`) from the
        `SequenceLocation` element with `Assembly="GRCh38"`.

**Fallback for Imprecise Coordinates (Gene Range):** ClinVar often returns the
full gene range for non-coding variants. If the extracted coordinates correspond
to the gene range instead of a specific position, use the `dbsnp-database` skill
to resolve the precise coordinates using the `dbsnp_rsid` or HGVS title: 1.Check
for `dbsnp_rsid` in the `evidence` output. 2. Run `uv run scripts/dbsnp_cli.py
resolve-rsid {rsid}` to get precise GRCh38 coordinates. 3. Format as
`<chrom>:<pos>:<ref>><alt>` using the SPDI or HGVS data from dbSNP.

### Structural Variant Note

The `structural_variant_details` field is **only populated for copy number
variants (CNVs)**. For standard SNVs and small indels this field will be `null`.
Use the `allele_info` fields (`position_start`, `position_stop`,
`reference_allele`, `alternate_allele`) instead.

### CNV / Large Deletion Note

Large copy-number variants (CNVs) frequently have empty
`molecular_consequences`. If a variant title mentions "del" and coordinates
overlap your target region, it is relevant regardless of missing labels.

### Obtaining and Using an API Key

To increase the rate limit to 10 requests per second, you need to obtain an NCBI
API key and add it to the `.env` file. You can obtain a key by following the
instructions at [NCBI ClinVar API docs][ncbi-api]

[ncbi-api]: https://www.ncbi.nlm.nih.gov/clinvar/docs/api_http/

Once you have a key, follow the prerequisite instructions to add it to the
`.env` file.

```bash
uv run scripts/clinvar_api.py search --query "BRCA1[gene]" --output results.json
```

If a `RateLimitError` is encountered, follow the prerequisite instructions to
help the user add `NCBI_API_KEY` to the `.env` file, providing the
[NCBI ClinVar API docs][ncbi-api] URL for instructions on how to obtain one.

## Best Practices

-   Always use `uv run` to execute `python`.
-   If `jq` is unavailable pivot immediately to using Python one-liners for
    processing JSON (e.g., `uv run python3 -c "import json; ..."`).
-   Use `count` before `search` to understand the result set size.
-   The `search` command fetches all results by default and includes
    `total_count` and `fetched_count` in the output — always verify these match
    to confirm complete retrieval.
-   Entrez results are **unsorted**. To order by date, fetch all results and
    sort locally by `last_evaluated`.

## Common Mistakes

-   **Attempting to parse the E-utilities XML yourself** — Always use the
    provided `clinvar_api.py` client which handles the unpredictable XML schemas
    robustly.
-   **Getting HTTP 429 Too Many Requests** — The client throws an exception
    telling you to pause. Follow the prerequisite instructions to help the user
    add `NCBI_API_KEY` to the `.env` file, then retry.
-   **Sending raw DNA sequences to the API** — The API expects HGVS
    nomenclature, RS IDs, or proper Entrez coordinate syntax (`11[chr] AND
    1234[chrpos]`), not raw ATCG strings.
-   **For synonymous or non-coding variants** — HGVS nomenclature (e.g., CAPN3
    AND "c.551C>T") is more reliable than coordinate searches ([chrpos]), as
    many ClinVar records for these types lack precise genomic mappings.
-   **Case sensitivity in molecular consequences** — ClinVar returns mixed-case
    strings. Always use case-insensitive matching (`.lower()`) when filtering.
-   **Parsing `search` output as a bare list** — `search` returns a JSON object
    with `total_count`, `fetched_count`, and `variant_ids` — not a bare list.
