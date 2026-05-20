---
name: gwas-database
description: Query the NHGRI-EBI GWAS Catalog to retrieve SNP–trait associations, study metadata, and (when available) summary statistics when you need evidence for a variant, trait/disease, gene, or genomic region.
license: MIT
skill-author: AIPOCH
metadata:
    skill-author: K-Dense Inc.
---
---

## Overview

The GWAS Catalog is a comprehensive repository of published genome-wide association studies maintained by the National Human Genome Research Institute (NHGRI) and the European Bioinformatics Institute (EBI). The catalog contains curated SNP-trait associations from thousands of GWAS publications, including genetic variants, associated traits and diseases, p-values, effect sizes, and study metadata.

## When to Use

Use this skill when you need to:

1. **Look up a specific variant (rsID)** to see all reported trait/disease associations and their p-values/effect sizes.
2. **Find variants associated with a trait/disease** (via free text or an EFO trait ID) for downstream interpretation or reporting.
3. **Perform gene-centric exploration** to identify GWAS hits within/near a gene of interest.
4. **Retrieve study-level metadata** (GCST accession, PMID, cohorts, ancestry, sample size) to assess evidence quality and applicability.
5. **Access or filter summary statistics** (when available) for genome-wide analyses (e.g., fine-mapping, colocalization, PRS development).

This skill is suitable for queries involving:

- Genetic variant associations (finding SNPs associated with diseases or traits)
- SNP lookups (retrieving information about specific genetic variants)
- Trait/disease searches (discovering genetic associations for phenotypes)
- Gene associations (finding variants in or near specific genes)
- GWAS summary statistics (accessing complete genome-wide association data)
- Study metadata (retrieving publication and cohort information)
- Population genetics (exploring ancestry-specific associations)
- Polygenic risk scores (identifying variants for risk prediction models)
- Functional genomics (understanding variant effects and genomic context)
- Systematic reviews (comprehensive literature synthesis of genetic associations)

## Key Features

- Multiple query entry points: rsID, EFO trait ID, gene symbol, chromosomal region, GCST accession, PMID.
- Structured entities: studies, associations, variants (SNPs), and traits (EFO-mapped).
- Programmatic access via:
  - GWAS Catalog REST API: `https://www.ebi.ac.uk/gwas/rest/api`
  - Summary Statistics API: `https://www.ebi.ac.uk/gwas/summary-statistics/api`
- Association-level fields commonly used in analysis: p-value, strongest allele, odds ratio/beta, mapped trait labels.
- Pagination support for bulk extraction (`page`, `size`, and `_links` navigation).

## Dependencies

- Python **3.9+**
- `requests` **>= 2.31.0**
- `pandas` **>= 2.0.0** (optional; for tabular outputs)

## Core Capabilities

### Understanding GWAS Catalog Data Structure

The GWAS Catalog is organized around four core entities:

- **Studies**: GWAS publications with metadata (PMID, author, cohort details, GCST ID).
- **Associations**: SNP-trait associations with statistical evidence (p ≤ 5×10⁻⁸).
- **Variants**: Genetic markers (SNPs) with genomic coordinates and alleles (rs IDs).
- **Traits**: Phenotypes and diseases (mapped to EFO ontology terms).

**Key Identifiers:**
- Study accessions: `GCST` IDs (e.g., GCST001234)
- Variant IDs: `rs` numbers (e.g., rs7903146)
- Trait IDs: EFO terms (e.g., EFO_0001360 for type 2 diabetes)
- Gene symbols: HGNC approved names (e.g., TCF7L2)

### REST API Access

The GWAS Catalog provides two REST APIs for programmatic access:

**Base URLs:**
- GWAS Catalog API: `https://www.ebi.ac.uk/gwas/rest/api`
- Summary Statistics API: `https://www.ebi.ac.uk/gwas/summary-statistics/api`

**API Documentation:**
- Main API docs: https://www.ebi.ac.uk/gwas/rest/docs/api
- Summary stats docs: https://www.ebi.ac.uk/gwas/summary-statistics/docs/

**Core Endpoints:**

1. **Studies endpoint** - `/studies/{accessionID}`
2. **Associations endpoint** - `/associations`
3. **Variants endpoint** - `/singleNucleotidePolymorphisms/{rsID}`
4. **Traits endpoint** - `/efoTraits/{efoID}`
5. **findByGene endpoint** - `/singleNucleotidePolymorphisms/search/findByGene`
6. **findByChromBpLocationRange endpoint** - `/singleNucleotidePolymorphisms/search/findByChromBpLocationRange`

### Pagination Strategy

- Most list endpoints are paginated.
- Use query parameters:
  - `size`: number of records per page (commonly 20–100)
  - `page`: zero-based page index
- Stop conditions:
  - `_embedded.associations` is empty, or
  - you reach a predefined `max_pages` safety limit.

## Example Usage

The following script is a complete, runnable example that:
1) fetches associations for an EFO trait,
2) filters by genome-wide significance,
3) returns a tidy table.

```python
import time
import requests
import pandas as pd

GWAS_REST_BASE = "https://www.ebi.ac.uk/gwas/rest/api"

def fetch_trait_associations(efo_id: str, page_size: int = 100, max_pages: int = 50):
    """
    Fetch associations for a given EFO trait ID from the GWAS Catalog REST API.
    Returns a list of association JSON objects.
    """
    url = f"{GWAS_REST_BASE}/efoTraits/{efo_id}/associations"
    headers = {"Accept": "application/json"}

    all_assocs = []
    for page in range(max_pages):
        params = {"page": page, "size": page_size}
        r = requests.get(url, params=params, headers=headers, timeout=60)
        r.raise_for_status()
        data = r.json()

        assocs = data.get("_embedded", {}).get("associations", [])
        if not assocs:
            break

        all_assocs.extend(assocs)
        time.sleep(0.1)  # be polite to the public API

    return all_assocs

def to_table(assocs, p_threshold: float = 5e-8) -> pd.DataFrame:
    rows = []
    for a in assocs:
        p = a.get("pvalue")
        try:
            p_float = float(p) if p is not None else None
        except (TypeError, ValueError):
            p_float = None

        if p_float is None or p_float > p_threshold:
            continue

        rows.append({
            "rsId": a.get("rsId"),
            "trait": a.get("efoTrait") or a.get("mappedLabel"),
            "pvalue": p_float,
            "strongestAllele": a.get("strongestAllele"),
            "orPerCopyNum": a.get("orPerCopyNum"),
            "betaNum": a.get("betaNum"),
            "pubmedId": a.get("pubmedId"),
            "studyAccession": a.get("studyAccession"),
        })

    df = pd.DataFrame(rows).drop_duplicates()
    if not df.empty:
        df = df.sort_values("pvalue", ascending=True).reset_index(drop=True)
    return df

if __name__ == "__main__":
    # Example: Type 2 diabetes (EFO_0001360)
    efo_id = "EFO_0001360"

    assocs = fetch_trait_associations(efo_id)
    df = to_table(assocs, p_threshold=5e-8)

    print(df.head(20).to_string(index=False))
    print(f"\nSignificant associations: {len(df)}")
    if not df.empty:
        print(f"Unique variants: {df['rsId'].nunique()}")
```

## Query Workflows

### Workflow 1: Exploring Genetic Associations for a Disease

1. **Identify the trait** using EFO terms or free text.
2. **Query associations via API:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/efoTraits/{efo_id}/associations"
   ```
3. **Filter by significance and population:** Check p-values (genome-wide significant: p ≤ 5×10⁻⁸) and review ancestry information in study metadata.
4. **Extract variant details:** rs IDs, effect alleles and directions, effect sizes (odds ratios, beta coefficients), and population allele frequencies.
5. **Cross-reference with other databases:** Look up variant consequences in Ensembl and check population frequencies in gnomAD.

### Workflow 2: Investigating a Specific Genetic Variant

1. **Query the variant:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}"
   ```
2. **Retrieve all trait associations:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/{rs_id}/associations"
   ```
3. **Analyze pleiotropy:** Identify all traits associated with this variant and review effect directions across traits.
4. **Check genomic context:** Determine nearby genes and identify if variant is in coding/regulatory regions.

### Workflow 3: Gene-Centric Association Analysis

1. **Search by gene symbol** in web interface or:
   ```python
   url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/search/findByGene"
   params = {"geneName": gene_symbol}
   ```
2. **Retrieve variants in gene region:** Get chromosomal coordinates for gene and query variants in region.
3. **Analyze association patterns:** Identify traits associated with variants in this gene and look for consistent associations across studies.
4. **Functional interpretation:** Determine variant consequences and check expression QTL (eQTL) data.

### Workflow 4: Systematic Review of Genetic Evidence

1. **Define research question:** Specific trait or disease of interest.
2. **Comprehensive variant extraction:** Query all associations for trait and set significance threshold.
3. **Quality assessment:** Review study sample sizes and check for population diversity.
4. **Data synthesis:** Aggregate associations across studies.
5. **Export and documentation:** Download full association data.

### Workflow 5: Accessing and Analyzing Summary Statistics

1. **Identify studies with summary statistics.**
2. **Download summary statistics.**
3. **Query via API for specific variants:**
   ```python
   url = f"https://www.ebi.ac.uk/gwas/summary-statistics/api/chromosomes/{chrom}/associations"
   params = {"start": start_pos, "end": end_pos}
   ```
4. **Process and analyze.**

## Response Formats and Data Fields

**Key Fields in Association Records:**
- `rsId`: Variant identifier (rs number)
- `strongestAllele`: Risk allele for the association
- `pvalue`: Association p-value
- `pvalueText`: P-value as text (may include inequality)
- `orPerCopyNum`: Odds ratio or beta coefficient
- `betaNum`: Effect size (for quantitative traits)
- `betaUnit`: Unit of measurement for beta
- `range`: Confidence interval
- `efoTrait`: Associated trait name
- `mappedLabel`: EFO-mapped trait term
- `studyAccession`: GCST study identifier
- `pubmedId`: PubMed ID

**Study Metadata Fields:**
- `accessionId`: GCST study identifier
- `pubmedId`: PubMed ID
- `author`: First author
- `publicationDate`: Publication date
- `ancestryInitial`: Discovery population ancestry
- `ancestryReplication`: Replication population ancestry
- `sampleSize`: Total sample size

## Best Practices

### Query Strategy
- Start with web interface to identify relevant EFO terms and study accessions.
- Use API for bulk data extraction and automated analyses.
- Implement pagination handling for large result sets.
- Cache API responses to minimize redundant requests.

### Data Interpretation
- Always check p-value thresholds (genome-wide: 5×10⁻⁸).
- Review ancestry information for population applicability.
- Consider sample size when assessing evidence strength.
- Check for replication across independent studies.

### Rate Limiting and Ethics
- Respect API usage guidelines (no excessive requests).
- Use summary statistics downloads for genome-wide analyses.
- Implement appropriate delays between API calls.
- Cache results locally when performing iterative analyses.
- Cite the GWAS Catalog in publications.

### Data Quality Considerations
- GWAS Catalog curates published associations (may contain inconsistencies).
- Effect sizes reported as published (may need harmonization).
- Some studies report conditional or joint associations.
- Check for study overlap when combining results.
- Be aware of ascertainment and selection biases.

## Implementation Details

### Data Model and Identifiers
- **Study accession**: `GCST...` (e.g., `GCST001234`)
- **Variant identifier**: `rs...` (e.g., `rs7903146`)
- **Trait identifier**: **EFO** term (e.g., `EFO_0001360`)
- **Gene symbol**: HGNC-approved symbol (e.g., `APOE`, `TCF7L2`)

### Significance Thresholds and Filtering
- A common GWAS threshold is **p ≤ 5×10⁻⁸** (genome-wide significance).
- Filtering should be applied after parsing `pvalue` into a numeric type; handle missing or non-numeric values safely.

### Summary Statistics Access (when available)
- Summary Statistics API base: `https://www.ebi.ac.uk/gwas/summary-statistics/api`
- Typical filters include chromosome/position ranges and p-value bounds (endpoint availability and parameters may vary by resource version).
- For bulk downloads, the Catalog also provides an FTP directory:
  - `http://ftp.ebi.ac.uk/pub/databases/gwas/summary_statistics/`

### Practical Notes for Robust Use
- Respect public API usage (add small delays; cache results for iterative workflows).
- Always interpret associations in context: ancestry/cohort metadata, sample size, replication status, effect size harmonization needs across studies.

## Resources

- **GWAS Catalog website**: https://www.ebi.ac.uk/gwas/
- **Documentation**: https://www.ebi.ac.uk/gwas/docs
- **API documentation**: https://www.ebi.ac.uk/gwas/rest/docs/api
- **Summary Statistics API**: https://www.ebi.ac.uk/gwas/summary-statistics/docs/
- **FTP site**: http://ftp.ebi.ac.uk/pub/databases/gwas/
- **Training materials**: https://github.com/EBISPOT/GWAS_Catalog-workshop
- **PGS Catalog** (polygenic scores): https://www.pgscatalog.org/
- **Help and support**: gwas-info@ebi.ac.uk

## Important Notes

### Data Updates
- The GWAS Catalog is updated regularly with new publications.
- Re-run queries periodically for comprehensive coverage.
- Summary statistics are added as studies release data.
- EFO mappings may be updated over time.

### Citation Requirements
When using GWAS Catalog data, cite:
- Sollis E, et al. (2023) The NHGRI-EBI GWAS Catalog: knowledgebase and deposition resource. Nucleic Acids Research. PMID: 37953337
- Include access date and version when available.
- Cite original studies when discussing specific findings.

### Limitations
- Not all GWAS publications are included (curation criteria apply).
- Full summary statistics available for subset of studies.
- Effect sizes may require harmonization across studies.
- Population diversity is growing but historically limited.
- Some associations represent conditional or joint effects.

### Data Access
- Web interface: Free, no registration required.
- REST APIs: Free, no API key needed.
- FTP downloads: Open access.
- Rate limiting applies to API (be respectful).