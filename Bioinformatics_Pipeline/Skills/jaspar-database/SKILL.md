---
name: jaspar-database
description: Query the JASPAR database for Transcription Factor (TF) binding profiles.
  Use when retrieving Position Frequency Matrices (PFMs) or Position Weight Matrices
  (PWMs) for specific TFs, resolving gene symbols to JASPAR Matrix IDs, or getting
  TF metadata. Supports multiple output formats (MEME, TRANSFAC, PFM, JASPAR, YAML).
---

---
JASPAR (https://jaspar.elixir.no/) is the gold-standard open-access database of curated, non-redundant transcription factor (TF) binding profiles stored as position frequency matrices (PFMs). JASPAR 2024 contains 1,210 non-redundant TF binding profiles for 164 eukaryotic species. Each profile is experimentally derived (ChIP-seq, SELEX, HT-SELEX, protein binding microarray, etc.) and rigorously validated.
**Key resources:**
- JASPAR portal: https://jaspar.elixir.no/
- REST API: https://jaspar.elixir.no/api/v1/
- API docs: https://jaspar.elixir.no/api/v1/docs/
- Python package: `jaspar` (via Biopython) or direct API
Use JASPAR when:
- **TF binding site prediction**: Scan a DNA sequence for potential binding sites of a TF
- **Regulatory variant interpretation**: Does a GWAS/eQTL variant disrupt a TF binding motif?
- **Promoter/enhancer analysis**: What TFs are predicted to bind to a regulatory element?
- **Gene regulatory network construction**: Link TFs to their target genes via motif scanning
- **TF family analysis**: Compare binding profiles across a TF family (e.g., all homeobox factors)
- **ChIP-seq analysis**: Find known TF motifs enriched in ChIP-seq peaks
- **ENCODE/ATAC-seq interpretation**: Match open chromatin regions to TF binding profiles
Base URL: `https://jaspar.elixir.no/api/v1/`
BASE_URL = "https://jaspar.elixir.no/api/v1"
def jaspar_get(endpoint, params=None):
response = requests.get(url, params=params, headers={"Accept": "application/json"})
):
"collection": collection,
"page": page,
"page_size": page_size,
"format": "json"
if tf_name:
if species:
if tf_class:
if tf_family:
# Examples:
def get_matrix(matrix_id):
# Example: Get CTCF matrix
# Matrix structure:
#   "matrix_id": "MA0139.1",
#   "name": "CTCF",
#   "collection": "CORE",
#   "tax_group": "vertebrates",
#   "pfm": { "A": [...], "C": [...], "G": [...], "T": [...] },
#   "consensus": "CCGCGNGGNGGCAG",
#   "length": 19,
#   "species": [{"tax_id": 9606, "name": "Homo sapiens"}],
#   "class": ["C2H2 zinc finger factors"],
#   "family": ["BEN domain factors"],
#   "type": "ChIP-seq",
#   "uniprot_ids": ["P49711"]
def get_pwm(matrix_id, pseudocount=0.8):
print(f"PWM for {name}: shape {pwm.shape}")
print(f"Maximum possible score: {max_score:.2f} bits")
NUCLEOTIDE_MAP = {'A': 0, 'C': 1, 'G': 2, 'T': 3,
'a': 0, 'c': 1, 'g': 2, 't': 3}
def scan_sequence(sequence: str, pwm: np.ndarray, threshold_pct: float = 0.8) -> List[dict]:
Args:
sequence: DNA sequence string
pwm: PWM array (4 x L) in ACGT order
threshold_pct: Fraction of max score to use as threshold (0-1)
Returns:
for i in range(len(seq) - motif_len + 1):
subseq = seq[i:i + motif_len]
if any(c not in NUCLEOTIDE_MAP for c in subseq):
if score >= threshold:
"position": i + 1,  # 1-based
"score": score,
"relative_score": relative_score,
"sequence": subseq,
"strand": "+"
# Example: Scan a promoter sequence for CTCF binding sites
for hit in hits:
print(f"  Position {hit['position']}: {hit['sequence']} (score: {hit['score']:.2f}, {hit['relative_score']:.0%})")
def reverse_complement(seq: str) -> str:
complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'N': 'N'}
def scan_both_strands(sequence: str, pwm: np.ndarray, threshold_pct: float = 0.8):
for h in fwd_hits:
for h in rev_hits:
return sorted(all_hits, key=lambda x: x["position"])
def variant_tfbs_impact(ref_seq: str, alt_seq: str, pwm: np.ndarray,
tf_name: str, threshold_pct: float = 0.7):
"tf": tf_name,
"ref_max_score": max_ref,
"alt_max_score": max_alt,
"ref_has_site": len(ref_hits) > 0,
"alt_has_site": len(alt_hits) > 0,
if max_ref and max_alt:
elif max_ref and not max_alt:
elif not max_ref and max_alt:
else:
### Workflow 1: Find All TF Binding Sites in a Promoter
"https://jaspar.elixir.no/api/v1/matrix/",
params={"species": "9606", "collection": "CORE", "page_size": 500, "page": 1}
for m in matrices[:10]:  # Limit for demo
pwm_data = requests.get(f"https://jaspar.elixir.no/api/v1/matrix/{m['matrix_id']}/").json()
for h in hits:
for h in sorted(all_hits, key=lambda x: -x["score"])[:5]:
print(f"  {h['tf_name']} ({h['matrix_id']}): pos {h['position']}, score {h['score']:.2f}")
### Workflow 2: SNP Impact on TF Binding (Regulatory Variant Analysis)
### Workflow 3: Motif Enrichment Analysis
name: jaspar-database
description: Query JASPAR for transcription factor binding site (TFBS) profiles (PWMs/PFMs). Search by TF name, species, or class; scan DNA sequences for TF binding sites; compare matrices; essential for regulatory genomics, motif analysis, and GWAS regulatory variant interpretation.
license: CC0-1.0
metadata:
skill-author: Kuan-lin Huang
------------|-------------|----------|
| `CORE` | Non-redundant, high-quality profiles | ~1,210 |
| `UNVALIDATED` | Experimentally derived but not validated | ~500 |
| `PHYLOFACTS` | Phylogenetically conserved sites | ~50 |
| `CNE` | Conserved non-coding elements | ~30 |
| `POLII` | RNA Pol II binding profiles | ~20 |
| `FAM` | TF family representative profiles | ~170 |
| `SPLICE` | Splice factor profiles | ~20 |

## Best Practices

- **Use CORE collection** for most analyses — best validated and non-redundant
- **Threshold selection**: 80% of max score is common for de novo prediction; 90% for high-confidence
- **Always scan both strands** — TFs can bind in either orientation
- **Provide flanking context** for variant analysis: at least (motif_length - 1) bp on each side
- **Consider background**: PWM scores relative to uniform (0.25) background; adjust for actual GC content
- **Cross-validate with ChIP-seq data** when available — motif scanning has many false positives
- **Use Biopython's motifs module** for full-featured scanning: `from Bio import motifs`

## Additional Resources

- **JASPAR portal**: https://jaspar.elixir.no/
- **API documentation**: https://jaspar.elixir.no/api/v1/docs/
- **JASPAR 2024 paper**: Castro-Mondragon et al. (2022) Nucleic Acids Research. PMID: 34875674
- **Biopython motifs**: https://biopython.org/docs/latest/Tutorial/chapter_motifs.html
- **FIMO tool** (for large-scale scanning): https://meme-suite.org/meme/tools/fimo
- **HOMER** (motif enrichment): http://homer.ucsd.edu/homer/
- **GitHub**: https://github.com/wassermanlab/JASPAR-UCSC-tracks

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


JASPAR is the definitive open-access database for Transcription Factor (TF)
binding profiles, stored as Position Frequency Matrices (PFMs).

Use this skill to map abstract sequence motifs or genomic regions to specific
biological regulators (e.g., "what TFs bind here?" or "what is the motif for
CTCF?").

## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://jaspar.elixir.no/ and https://jaspar.elixir.no/api/, then (2)
    create the file recording the notification text and timestamp.

## Core Rules

**CRITICAL**: You MUST respect the JASPAR API Terms of Use by adhering to the
following:

-   **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
    database rather than accessing the database directly. The scripts
    automatically enforce the required rate limit gracefully.
-   **Maximum API Window Size**: The genomic window for a single API query MUST
    NOT exceed 100,000 bp (100kb). The `jaspar_api.py` script automatically
    chunks larger requests for you to bypass this limitation when querying
    larger regions.
-   **Valid Matrix IDs**: `get_tf_motif`, `get_tf_metadata`, and `get_tf_pwm`
    require a stable JASPAR Matrix ID (e.g., `MA0488.2`). If a user provides a
    gene symbol (e.g., `JUN`), you must resolve it first using `resolve_tf_id`.
-   **Taxonomy Required**: Resolving IDs requires a `tax_id` to ensure targeted
    searches. Common IDs: Human=9606, Mouse=10090.
-   **Notification**: If this skill is used, ensure this is mentioned in the
    output.

## Utility Scripts

Run all commands using the bundled Python script:

### 1. Resolve TF to Matrix ID

Maps a transcription factor name to a stable Matrix ID. Required step before
fetching motifs if only a gene name is provided.

```bash
uv run scripts/jaspar_api.py resolve_tf_id --name "JUN" --tax-id 9606
```

### 2. Get TF Motif (PFM)

Retrieves the raw Position Frequency Matrix for a specific TF. Supports
`--format` flag.

```bash
uv run scripts/jaspar_api.py get_tf_motif --matrix-id "MA0488.2"
uv run scripts/jaspar_api.py get_tf_motif --matrix-id "MA0488.2" --format meme
```

### 3. Get TF Metadata

Retrieves TF class, family, and links to external databases (e.g., UniProt).
Supports `--format` flag.

```bash
uv run scripts/jaspar_api.py get_tf_metadata --matrix-id "MA0488.2"
uv run scripts/jaspar_api.py get_tf_metadata --matrix-id "MA0488.2" --format yaml
```

### 4. Compute PWM (Position Weight Matrix)

Fetches the PFM for a matrix and converts it to log-odds scores (PWM).

```bash
uv run scripts/jaspar_api.py get_tf_pwm --matrix-id "MA0488.2"
uv run scripts/jaspar_api.py get_tf_pwm --matrix-id "MA0488.2" --pseudocount 0.1
```

### 5. Infer Matrix from Protein Sequence

Infers potential JASPAR matrix profiles from a raw transcription factor protein
sequence.

```bash
uv run scripts/jaspar_api.py infer_from_sequence --sequence "QAQLLPSHHVG"
```

### 6. Get TF Flexible Model (TFFM)

Retrieves metadata for a JASPAR TF Flexible Model. (Note: The JASPAR TFFM
endpoints occasionally experience 500 Internal Server errors).

```bash
uv run scripts/jaspar_api.py get_tffm --tffm-id "TFFM0001.1"
```

### Output Formats

The `get_tf_motif` and `get_tf_metadata` commands accept an optional `--format`
flag. Supported formats: `json` (default), `jsonp`, `jaspar`, `meme`,
`transfac`, `pfm`, `yaml`.

## Anti-Patterns

*   **DON'T** pass gene symbols (e.g., `JUN`) to `get_tf_motif`. You must pass
    the `MA...` Matrix ID.
*   **DON'T** forget the `--tax-id` when resolving a TF name.
*   **DON'T** use this skill for determining tissue-specific epigenetic
    availability (JASPAR shows *potential* binding, not *actual* tissue
    expression context).
*   **DON'T** use this skill to model how a specific protein mutation affects
    binding.
