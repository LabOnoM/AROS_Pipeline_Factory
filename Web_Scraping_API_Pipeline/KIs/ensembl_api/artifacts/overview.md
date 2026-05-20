# Ensembl API System — Comprehensive Reference

## ⚠️ USER PREFERENCE (MANDATORY)

> **For ALL mapping and alignment steps, always use the newest reference genome
> from Ensembl.** Do not default to pre-built 10x Genomics references (e.g.,
> `refdata-gex-GRCh38-2020-A`) unless they are the latest available. Always
> check the current Ensembl release first and build custom references from
> the most recent Ensembl FASTA + GTF files when a newer release exists.

---

## 1. Ensembl Overview

Ensembl is a genome browser and annotation database maintained by EMBL-EBI and the
Wellcome Sanger Institute. It provides genome assemblies, gene annotations, regulatory
features, comparative genomics, and variant data for vertebrates and model organisms.

### Key Mirrors

| Mirror | URL | Region |
|--------|-----|--------|
| Main | `https://www.ensembl.org` | UK (Hinxton) |
| US East | `https://useast.ensembl.org` | US East |
| US West | `https://uswest.ensembl.org` | US West |
| Asia | `https://asia.ensembl.org` | Singapore |

### Current Release

The Ensembl REST API version as of April 2026 is **15.10**. The Ensembl data release
updates approximately every 2–3 months.

To check the current release:

```python
import requests

r = requests.get("https://rest.ensembl.org/info/data?",
                 headers={"Content-Type": "application/json"})
data = r.json()
print(f"Current Ensembl releases: {data['releases']}")
```

---

## 2. Reference Genome Downloads (FTP)

### FTP Site Structure

```
https://ftp.ensembl.org/pub/
├── current/                          # Symlink to latest release
├── release-115/                      # Specific release
│   ├── fasta/
│   │   ├── homo_sapiens/
│   │   │   ├── dna/                  # Genome FASTA (primary assembly, toplevel, etc.)
│   │   │   │   ├── Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
│   │   │   │   └── README
│   │   │   ├── cdna/                 # cDNA transcripts
│   │   │   ├── cds/                  # Coding sequences
│   │   │   ├── ncrna/                # Non-coding RNA
│   │   │   └── pep/                  # Protein sequences
│   │   └── mus_musculus/
│   │       └── dna/
│   │           └── Mus_musculus.GRCm39.dna.primary_assembly.fa.gz
│   ├── gtf/
│   │   ├── homo_sapiens/
│   │   │   └── Homo_sapiens.GRCh38.115.gtf.gz
│   │   └── mus_musculus/
│   │       └── Mus_musculus.GRCm39.115.gtf.gz
│   └── gff3/
│       ├── homo_sapiens/
│       └── mus_musculus/
└── release-114/
```

### Current Reference Assemblies

| Species | Assembly | Ensembl Name | NCBI Accession |
|---------|----------|-------------|----------------|
| Human | GRCh38.p14 | `homo_sapiens` | GCA_000001405.29 |
| Mouse | GRCm39 | `mus_musculus` | GCA_000001635.9 |
| Rat | mRatBN7.2 | `rattus_norvegicus` | GCA_015227675.2 |
| Zebrafish | GRCz11 | `danio_rerio` | GCA_000002035.4 |

### Download Commands

```bash
# ── Human Reference ──────────────────────────────────────────────
# Genome FASTA (primary assembly — excludes haplotypes/patches)
wget https://ftp.ensembl.org/pub/current/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz

# Gene annotations (GTF)
wget https://ftp.ensembl.org/pub/current/gtf/homo_sapiens/Homo_sapiens.GRCh38.*.gtf.gz

# ── Mouse Reference ──────────────────────────────────────────────
wget https://ftp.ensembl.org/pub/current/fasta/mus_musculus/dna/Mus_musculus.GRCm39.dna.primary_assembly.fa.gz
wget https://ftp.ensembl.org/pub/current/gtf/mus_musculus/Mus_musculus.GRCm39.*.gtf.gz

# ── Bulk download via rsync (faster, resumable) ─────────────────
rsync -av rsync://ftp.ensembl.org/ensembl/pub/current/fasta/homo_sapiens/dna/ ./human_dna/
rsync -av rsync://ftp.ensembl.org/ensembl/pub/current/gtf/homo_sapiens/ ./human_gtf/
```

### Building Custom Reference for Space Ranger or Cell Ranger

When the Ensembl release is newer than the pre-built 10x reference:

```bash
# 1. Download FASTA + GTF from the latest Ensembl release
wget https://ftp.ensembl.org/pub/current/fasta/mus_musculus/dna/Mus_musculus.GRCm39.dna.primary_assembly.fa.gz
wget https://ftp.ensembl.org/pub/current/gtf/mus_musculus/Mus_musculus.GRCm39.*.gtf.gz
gunzip *.gz

# 2. Filter GTF (Cell Ranger/Space Ranger mkgtf step)
cellranger mkgtf Mus_musculus.GRCm39.115.gtf Mus_musculus.GRCm39.115.filtered.gtf \
  --attribute=gene_biotype:protein_coding \
  --attribute=gene_biotype:lncRNA \
  --attribute=gene_biotype:IG_C_gene \
  --attribute=gene_biotype:IG_D_gene \
  --attribute=gene_biotype:IG_J_gene \
  --attribute=gene_biotype:IG_LV_gene \
  --attribute=gene_biotype:IG_V_gene \
  --attribute=gene_biotype:TR_C_gene \
  --attribute=gene_biotype:TR_D_gene \
  --attribute=gene_biotype:TR_J_gene \
  --attribute=gene_biotype:TR_V_gene

# 3. Build reference
cellranger mkref \
  --genome=Mus_musculus_GRCm39_ensembl115 \
  --fasta=Mus_musculus.GRCm39.dna.primary_assembly.fa \
  --genes=Mus_musculus.GRCm39.115.filtered.gtf

# 4. Use with spaceranger
spaceranger count \
  --transcriptome=Mus_musculus_GRCm39_ensembl115 \
  ...
```

> **Note**: `cellranger mkref` and `cellranger mkgtf` are bundled with Cell Ranger.
> Space Ranger uses the same reference format. If only Space Ranger is installed,
> download Cell Ranger to use `mkref`/`mkgtf`.

---

## 3. REST API Reference

### Base URL

```
https://rest.ensembl.org
```

### Rate Limits

- **15 requests/second** (without API key)
- **55,000 requests/hour** (without API key)
- Use `Content-Type: application/json` for all requests
- Include a user agent header for polite access

### Authentication

No API key required for public endpoints. For higher rate limits, contact Ensembl
helpdesk.

### Endpoint Categories

| Category | Endpoints | Primary Use |
|----------|----------|-------------|
| **Lookup** | `lookup/id/:id`, `lookup/symbol/:species/:symbol` | Find species/db for a gene/transcript/protein ID |
| **Cross References** | `xrefs/id/:id`, `xrefs/symbol/:species/:symbol`, `xrefs/name/:species/:name` | Map between Ensembl ↔ external DBs (UniProt, HGNC, EntrezGene) |
| **Sequence** | `sequence/id/:id`, `sequence/region/:species/:region` | Retrieve DNA/mRNA/protein sequences |
| **Assembly Info** | `info/assembly/:species`, `info/assembly/:species/:region_name` | Current assembly details, chromosomes, karyotype |
| **Mapping** | `map/:species/:asm_one/:region/:asm_two`, `map/cdna/:id/:region` | Coordinate conversion between assemblies or transcript/genomic |
| **Overlap** | `overlap/id/:id`, `overlap/region/:species/:region` | Find features overlapping a genomic region |
| **Information** | `info/species`, `info/data`, `info/rest`, `info/software` | List species, releases, API version |
| **Comparative** | `homology/id/:species/:id`, `genetree/id/:id` | Orthologs, paralogs, gene trees |
| **Variation** | `variation/:species/:id`, `vep/:species/hgvs/:hgvs` | Variant effect prediction |
| **Ontology** | `ontology/id/:id`, `taxonomy/id/:id` | GO terms, taxonomy classification |
| **Regulation** | `species/:species/binding_matrix/:id` | Regulatory features |
| **Phenotype** | `phenotype/gene/:species/:gene` | Disease associations |
| **Archive** | `archive/id/:id` | Historical ID→current ID mapping |
| **Linkage Disequilibrium** | `ld/:species/:id/:population_name` | LD data for population genetics |

---

## 4. Key Python Recipes

### 4.1 Check Current Ensembl Release & Assembly Info

```python
import requests

SERVER = "https://rest.ensembl.org"

def get_current_release():
    """Get the current Ensembl release number."""
    r = requests.get(f"{SERVER}/info/data?",
                     headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()["releases"]

def get_assembly_info(species="mus_musculus"):
    """Get assembly information for a species."""
    r = requests.get(f"{SERVER}/info/assembly/{species}?",
                     headers={"Content-Type": "application/json"})
    r.raise_for_status()
    info = r.json()
    return {
        "assembly_name": info["assembly_name"],
        "assembly_accession": info.get("assembly_accession"),
        "coord_system_version": info.get("default_coord_system_version"),
        "top_level_region_count": len(info.get("top_level_region", [])),
        "karyotype": info.get("karyotype", []),
    }

print(f"Current releases: {get_current_release()}")
print(f"Mouse assembly: {get_assembly_info('mus_musculus')}")
print(f"Human assembly: {get_assembly_info('homo_sapiens')}")
```

### 4.2 Gene Lookup by Ensembl ID

```python
def lookup_gene(ensembl_id, expand=False):
    """
    Look up gene/transcript/protein by Ensembl stable ID.
    
    Parameters
    ----------
    ensembl_id : str
        e.g., 'ENSG00000157764' (BRAF) or 'ENSMUSG00000030787'
    expand : bool
        If True, include transcript details.
    
    Returns
    -------
    dict
        Gene metadata (species, biotype, strand, coordinates, etc.)
    """
    ext = f"/lookup/id/{ensembl_id}?"
    if expand:
        ext += "expand=1"
    r = requests.get(f"{SERVER}{ext}",
                     headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()

# Example
gene = lookup_gene("ENSG00000157764", expand=True)
print(f"Gene: {gene['display_name']} ({gene['species']})")
print(f"Biotype: {gene['biotype']}")
print(f"Location: {gene['seq_region_name']}:{gene['start']}-{gene['end']}")
```

### 4.3 Gene Symbol → Ensembl ID Mapping

```python
def symbol_to_ensembl(species, symbol, external_db=None):
    """
    Look up Ensembl objects linked to a gene symbol.
    
    Parameters
    ----------
    species : str
        e.g., 'homo_sapiens', 'mus_musculus'
    symbol : str
        Gene symbol, e.g., 'BRCA2', 'Bglap'
    external_db : str, optional
        Filter to specific DB, e.g., 'HGNC', 'MGI'
    
    Returns
    -------
    list of dict
        Ensembl objects (genes, transcripts, translations).
    """
    ext = f"/xrefs/symbol/{species}/{symbol}?"
    if external_db:
        ext += f"external_db={external_db}"
    r = requests.get(f"{SERVER}{ext}",
                     headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()

# Example: Mouse gene symbol → Ensembl ID
results = symbol_to_ensembl("mus_musculus", "Bglap")
for hit in results:
    print(f"  {hit['type']}: {hit['id']}")
```

### 4.4 Ensembl ID → External DB Cross-References (UniProt, HGNC, EntrezGene)

```python
def get_xrefs(ensembl_id, external_db=None):
    """
    Get cross-references for an Ensembl stable ID.
    
    Parameters
    ----------
    ensembl_id : str
        Ensembl gene/transcript/protein ID.
    external_db : str, optional
        Filter to specific DB, e.g., 'UniProt/SWISSPROT', 'HGNC', 'EntrezGene'
    
    Returns
    -------
    list of dict
        External database references.
    """
    ext = f"/xrefs/id/{ensembl_id}?"
    if external_db:
        ext += f"external_db={external_db}"
    r = requests.get(f"{SERVER}{ext}",
                     headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()

# Example: Get UniProt IDs for a human gene
xrefs = get_xrefs("ENSG00000157764", external_db="Uniprot/SWISSPROT")
for xref in xrefs:
    print(f"  {xref['dbname']}: {xref['primary_id']} ({xref.get('display_id', '')})")
```

### 4.5 Batch Lookup (POST endpoints for multi-ID queries)

```python
def batch_lookup(ensembl_ids):
    """
    Look up multiple Ensembl IDs in a single request (max 1000 IDs).
    """
    r = requests.post(
        f"{SERVER}/lookup/id",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json={"ids": ensembl_ids}
    )
    r.raise_for_status()
    return r.json()

# Example
results = batch_lookup(["ENSG00000157764", "ENSG00000141510", "ENSG00000171862"])
for eid, data in results.items():
    print(f"  {eid}: {data.get('display_name', 'N/A')} ({data.get('biotype', 'N/A')})")
```

### 4.6 Retrieve Sequence by ID

```python
def get_sequence(ensembl_id, seq_type="genomic", format="fasta"):
    """
    Retrieve sequence for an Ensembl stable ID.
    
    Parameters
    ----------
    ensembl_id : str
        ENSG, ENST, ENSP, or ENSE ID.
    seq_type : str
        'genomic', 'cdna', 'cds', 'protein'
    format : str
        'fasta' or 'json'
    
    Returns
    -------
    str or dict
        Sequence data.
    """
    content_type = "text/x-fasta" if format == "fasta" else "application/json"
    ext = f"/sequence/id/{ensembl_id}?type={seq_type}"
    r = requests.get(f"{SERVER}{ext}",
                     headers={"Content-Type": content_type})
    r.raise_for_status()
    return r.text if format == "fasta" else r.json()

# Example: Get mRNA sequence for a transcript
seq = get_sequence("ENST00000288602", seq_type="cdna", format="fasta")
print(seq[:200])
```

### 4.7 Assembly Coordinate Mapping

```python
def map_coordinates(species, asm_from, region, asm_to):
    """
    Map genomic coordinates between assemblies.
    
    Example: GRCh37 → GRCh38 coordinate liftover
    """
    ext = f"/map/{species}/{asm_from}/{region}/{asm_to}?"
    r = requests.get(f"{SERVER}{ext}",
                     headers={"Content-Type": "application/json"})
    r.raise_for_status()
    return r.json()

# Example: Lift GRCh37 coordinates to GRCh38
# mapped = map_coordinates("human", "GRCh37", "17:7565097-7590856", "GRCh38")
```

---

## 5. BioMart — Bulk ID Mapping

### 5.1 Using `pybiomart` (Python)

```python
# pip install pybiomart
from pybiomart import Server

server = Server(host="http://www.ensembl.org")
dataset = (server.marts['ENSEMBL_MART_ENSEMBL']
                 .datasets['mmusculus_gene_ensembl'])

# Map Ensembl gene IDs → gene symbols + descriptions
result = dataset.query(
    attributes=['ensembl_gene_id', 'external_gene_name', 'description',
                'chromosome_name', 'start_position', 'end_position'],
    filters={'ensembl_gene_id': ['ENSMUSG00000030787', 'ENSMUSG00000015437']}
)
print(result)
```

### 5.2 Using `biomart` (Python)

```python
# pip install biomart
from biomart import BiomartServer

server = BiomartServer("http://www.ensembl.org/biomart")
ensembl = server.datasets['hsapiens_gene_ensembl']

response = ensembl.search({
    'filters': {'hgnc_symbol': ['BRCA2', 'TP53', 'BGLAP']},
    'attributes': ['ensembl_gene_id', 'hgnc_symbol', 'gene_biotype',
                   'chromosome_name', 'start_position', 'end_position']
})

for line in response.iter_lines():
    line = line.decode('utf-8')
    print(line)
```

### 5.3 BioMart via Direct HTTP (no library needed)

```python
import requests

def biomart_query(dataset, attributes, filters=None):
    """
    Query Ensembl BioMart using the XML-based REST interface.
    No external libraries needed — just requests.
    """
    filter_xml = ""
    if filters:
        for name, values in filters.items():
            vals = ",".join(values) if isinstance(values, list) else values
            filter_xml += f'<Filter name="{name}" value="{vals}"/>'
    
    attr_xml = "".join(f'<Attribute name="{a}"/>' for a in attributes)
    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE Query>
    <Query virtualSchemaName="default" formatter="TSV" header="0"
           uniqueRows="0" count="" datasetConfigVersion="0.6">
        <Dataset name="{dataset}" interface="default">
            {filter_xml}
            {attr_xml}
        </Dataset>
    </Query>"""
    
    r = requests.get("http://www.ensembl.org/biomart/martservice",
                     params={"query": xml})
    r.raise_for_status()
    return r.text

# Example: Get gene info for a list of Ensembl IDs
result = biomart_query(
    dataset="mmusculus_gene_ensembl",
    attributes=["ensembl_gene_id", "external_gene_name", "gene_biotype"],
    filters={"ensembl_gene_id": ["ENSMUSG00000030787"]}
)
print(result)
```

### Common BioMart Datasets

| Dataset | Species |
|---------|---------|
| `hsapiens_gene_ensembl` | Human |
| `mmusculus_gene_ensembl` | Mouse |
| `rnorvegicus_gene_ensembl` | Rat |
| `drerio_gene_ensembl` | Zebrafish |

### Common BioMart Attributes

| Attribute | Description |
|-----------|-------------|
| `ensembl_gene_id` | Ensembl gene stable ID |
| `ensembl_transcript_id` | Ensembl transcript stable ID |
| `external_gene_name` | Gene symbol (HGNC/MGI) |
| `description` | Gene description |
| `gene_biotype` | Protein coding, lncRNA, etc. |
| `chromosome_name` | Chromosome |
| `start_position` | Gene start |
| `end_position` | Gene end |
| `strand` | Strand (+1/-1) |
| `uniprotswissprot` | UniProt/SwissProt accession |
| `entrezgene_id` | NCBI Entrez Gene ID |
| `hgnc_symbol` | HGNC symbol (human) |
| `mgi_symbol` | MGI symbol (mouse) |
| `go_id` | Gene Ontology ID |

---

## 6. Ensembl ID Format Reference

| Prefix | Object Type | Example |
|--------|------------|---------|
| `ENSG` | Gene | `ENSG00000157764` (BRAF) |
| `ENST` | Transcript | `ENST00000288602` |
| `ENSP` | Protein | `ENSP00000288602` |
| `ENSE` | Exon | `ENSE00001154485` |
| `ENSR` | Regulatory Feature | `ENSR00000000001` |
| `ENSMUSG` | Mouse Gene | `ENSMUSG00000030787` |
| `ENSMUST` | Mouse Transcript | `ENSMUST00000033012` |
| `ENSMUSP` | Mouse Protein | `ENSMUSP00000033012` |
| `ENSRNOG` | Rat Gene | `ENSRNOG00000014303` |

### Version Numbers

Ensembl IDs can include version numbers: `ENSG00000157764.14`
- The number after the dot is the **version** and changes when annotations are updated
- REST API accepts both versioned and unversioned IDs

---

## 7. Integration with Space Ranger / 10x Genomics

### Checking if a Newer Reference is Available

```python
def should_update_reference(current_ref_name):
    """
    Compare current 10x reference (e.g., 'refdata-gex-GRCh38-2020-A')
    with the latest Ensembl release to see if an update is available.
    """
    import re
    
    # Extract year from 10x reference name
    match = re.search(r'(\d{4})-([A-Z])', current_ref_name)
    if not match:
        return True  # Can't parse → assume update needed
    
    ref_year = int(match.group(1))
    
    # Get latest Ensembl release
    r = requests.get("https://rest.ensembl.org/info/data?",
                     headers={"Content-Type": "application/json"})
    current_release = r.json()["releases"][0]
    
    # Ensembl releases ~4× per year; release 115 was ~2024
    # Approximate: if ref_year is >1 year old, recommend update
    import datetime
    current_year = datetime.datetime.now().year
    
    if current_year - ref_year >= 2:
        print(f"⚠️  Reference from {ref_year} is {current_year - ref_year} years old.")
        print(f"   Current Ensembl release: {current_release}")
        print(f"   Recommend building a new reference from Ensembl release {current_release}.")
        return True
    else:
        print(f"✅ Reference from {ref_year} is recent. Ensembl release: {current_release}")
        return False

# Example
should_update_reference("refdata-gex-GRCh38-2020-A")
```

### FTP URLs for Space Ranger Custom Reference Build

| Species | FASTA URL | GTF URL |
|---------|-----------|---------|
| Human | `ftp.ensembl.org/pub/current/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz` | `ftp.ensembl.org/pub/current/gtf/homo_sapiens/Homo_sapiens.GRCh38.*.gtf.gz` |
| Mouse | `ftp.ensembl.org/pub/current/fasta/mus_musculus/dna/Mus_musculus.GRCm39.dna.primary_assembly.fa.gz` | `ftp.ensembl.org/pub/current/gtf/mus_musculus/Mus_musculus.GRCm39.*.gtf.gz` |

---

## 8. Troubleshooting

| Issue | Solution |
|-------|----------|
| REST API returns 429 (Too Many Requests) | Back off and retry; implement exponential backoff; limit to 15 req/s |
| REST API returns 400 for gene symbol | Check species name is correct (e.g., `homo_sapiens` not `human`) |
| BioMart query returns empty | Verify dataset name matches species; check filter values |
| FTP timeout | Use `rsync` instead of `wget`; try a different mirror |
| GTF version mismatch with FASTA | Always download both from the **same** Ensembl release directory |
| `cellranger mkref` fails | Ensure GTF chromosomes match FASTA headers; Ensembl uses `1`, `2`, etc. (not `chr1`, `chr2`) |
| UCSC vs Ensembl chromosome names | Ensembl uses `1`, `2`, `X`; UCSC uses `chr1`, `chr2`, `chrX`. Use `sed 's/^>/>chr/' genome.fa` to convert. |

---

## 9. References

- [Ensembl Documentation Portal](https://useast.ensembl.org/info/docs/index.html)
- [REST API Endpoints](https://rest.ensembl.org)
- [REST API User Guide](https://github.com/Ensembl/ensembl-rest/wiki)
- [FTP Downloads](https://ftp.ensembl.org/pub/)
- [BioMart](http://www.ensembl.org/biomart/martview)
- [Ensembl Blog (release announcements)](https://www.ensembl.info/category/01-release/)
