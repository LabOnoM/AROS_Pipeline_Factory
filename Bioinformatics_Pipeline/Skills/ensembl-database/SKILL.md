---
name: ensembl-database
description: Query the Ensembl database to resolve gene, transcript, and protein IDs,
  fetch genomic or protein sequences, retrieve gene structures (exons), and get variant
  consequence and effect predictions (VEP). Use this skill as a primary ID translator,
  genomic sequence database and variant effect prediction tool.
license: MIT
metadata:
  skill-author: AIPOCH + K-Dense Inc.
---

---

# Ensembl Database Skill

## Overview

Access and query the Ensembl genome database, a comprehensive resource for vertebrate genomic data maintained by EMBL-EBI. The database provides gene annotations, sequences, variants, regulatory information, and comparative genomics data for over 250 species. Current release is 115 (September 2025).

## When to Use This Skill

- Use this skill when you need access to the Ensembl REST API for vertebrate genomic data for gene/ID lookups, sequence retrieval, variant effect prediction (VEP), or homology/assembly coordinate mapping in a reproducible workflow.
- Use this skill when an evidence insight task needs a packaged method instead of ad-hoc freeform output.
- Use this skill when the user expects a concrete deliverable or file-based result.
- Use this skill when `scripts/query_ensembl.py` is the most direct path to complete the request.
- Use this skill when you need the `ensembl-database` package behavior rather than a generic answer.
- **Gene-centric queries**: When you need to resolve a gene symbol or region to Ensembl identifiers and basic annotations (e.g., `BRCA2` in human).
- **Sequence extraction**: When you need DNA/cDNA/protein sequences for a known Ensembl gene/transcript/protein ID in FASTA or JSON.
- **Variant interpretation**: When you need to predict functional consequences of variants using **VEP** from HGVS notation.
- **Comparative genomics**: When you need ortholog/paralog relationships across vertebrate species.
- **Assembly/coordinate mapping**: When you need to map coordinates between assemblies (e.g., GRCh37 ↔ GRCh38).

## Key Features

- Scope-focused workflow aligned to: Access Ensembl REST API for vertebrate genomic data; use when you need gene/ID lookups, sequence retrieval, variant effect prediction (VEP), or homology/assembly coordinate mapping.
- Packaged executable path(s): `scripts/query_ensembl.py`.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.
- Query Ensembl REST endpoints for:
    - **Gene lookup** by symbol, Ensembl ID, or genomic region
    - **Sequence retrieval** (DNA, cDNA, protein) in FASTA/JSON
    - **Variant Effect Predictor (VEP)** analysis from HGVS inputs
    - **Homology** retrieval (orthologs/paralogs)
    - **Assembly/coordinate mapping** between common human assemblies
- CLI helper script for repeatable queries:
    - `scripts/query_ensembl.py` (wrapper around an `ensembl_rest` client)
- Reference documentation for endpoints:
    - `references/api_endpoints.md`
    - Ensembl REST base URL: https://rest.ensembl.org

## Dependencies

- `Python`: `3.8+`. Repository baseline for current packaged skills.
- `ensembl_rest` (Python client; version depends on your environment)
- `requests`
- Network access to `https://rest.ensembl.org`

## Example Usage

```bash
cd "20260316/scientific-skills/Evidence Insight/ensembl-database"
python -m py_compile scripts/query_ensembl.py
python scripts/query_ensembl.py --help
```

```bash
python scripts/query_ensembl.py --action lookup --species human --symbol BRCA2
```

```bash
python scripts/query_ensembl.py --action sequence --id ENSG00000139618
```

```bash
python scripts/query_ensembl.py --action vep --species human --hgvs "ENST00000380152.8:c.68_69delAG"
```

Example run plan:

1.  Confirm the user input, output path, and any required config values.
2.  Edit the in-file `CONFIG` block or documented parameters if the script uses fixed settings.
3.  Run `python scripts/query_ensembl.py` with the validated inputs.
4.  Review the generated output and return the final artifact with any assumptions called out.

## Implementation Details

- Execution model: validate the request, choose the packaged workflow, and produce a bounded deliverable.
- Input controls: confirm the source files, scope limits, output format, and acceptance criteria before running any script.
- Primary implementation surface: `scripts/query_ensembl.py`.
- Reference guidance: `references/` contains supporting rules, prompts, or checklists.
- Parameters to clarify first: input path, output path, scope filters, thresholds, and any domain-specific constraints.
- Output discipline: keep results reproducible, identify assumptions explicitly, and avoid undocumented side effects.

### Script entry point

- **Tool**: `scripts/query_ensembl.py`
- **Purpose**: Provide a simple command-line interface that dispatches to Ensembl REST calls via an `ensembl_rest` client.

### Core parameters

- `--action`: Operation selector.
    - Supported values: `lookup`, `sequence`, `vep`
- `--species`: Target species name used by Ensembl REST (e.g., `human`).
- `--symbol`: Gene symbol used for lookup actions (e.g., `BRCA2`).
- `--id`: Ensembl stable ID used for sequence retrieval (e.g., `ENSG...`, `ENST...`, `ENSP...`).
- `--hgvs`: HGVS notation string used for VEP (e.g., `ENST...:c.123A>G`).

### Data types and outputs

- **Lookup**: Returns gene/transcript metadata as provided by Ensembl REST.
- **Sequence**: Returns DNA/cDNA/protein sequence; format depends on the endpoint/options (commonly FASTA or JSON).
- **VEP**: Returns consequence annotations and (when available) population frequency fields as provided by Ensembl VEP REST responses.

### Endpoint reference

For the exact REST paths, required parameters, and response schemas, see:

- `references/api_endpoints.md`
- https://rest.ensembl.org

---

## CLI/Plugin Integration Guidance

This section integrates the CLI tool definitions and guidelines from the AROS plugin workspace.


## Prerequisites

1.  **`uv`**: Read the `uv` skill and follow its Setup instructions to ensure
    `uv` is installed and on PATH.
2.  **User Notification**: If LICENSE_NOTIFICATION.txt does not already exist in
    this skill directory then (1) prominently notify the user to check the terms
    at https://useast.ensembl.org/index.html and
    https://github.com/Ensembl/ensembl-rest/wiki, then (2) create the file
    recording the notification text and timestamp.

## Overview

The Ensembl database is a resource for genome annotation. This skill allows you
to interact with the Ensembl REST API to resolve ambiguous symbols,
cross-reference IDs (RefSeq, HGNC, UniProt, ENSG), fetch raw sequences, and
retrieve detailed transcript structures.

**Key Concepts:**

-   **ENSG (Gene):** Stable identifier for a human gene. Other species will have
    different three-letter species codes.
-   **ENST (Transcript):** Stable identifier for a transcript (splicing
    isoform).
-   **ENSP (Protein):** Stable identifier for a translated protein.
-   **MANE Select:** The consensus primary transcript agreed upon by Ensembl and
    NCBI.
-   **Canonical:** Ensembl's representative transcript (used if MANE is not
    available or non-human).

## Core Rules

-   **Use the Wrapper**: ALWAYS execute the provided helper scripts to query the
    database rather than accessing the database directly. The scripts
    automatically enforce the required rate limit gracefully.
-   **Default Species:** If the species is absent or ambiguous in the prompt,
    default to `"human"`. You MUST explicitly flag this default to the user to
    ensure they are aware.
-   **Primary Transcripts:** When listing transcripts for a gene, only return
    the MANE Select transcript (for human) or the Canonical transcript (for
    others) unless the user explicitly asks for all alternative isoforms. You
    MUST flag to the user when multiple transcripts are available and you are
    defaulting to the primary one.
-   **Assembly Handling:** The default assembly is GRCh38. For GRCh37 requests,
    you MUST use the `--assembly GRCh37` flag. You MUST explicitly flag to the
    user when a non-default assembly is being used.
-   **Output Location:** The script writes full JSON/FASTA output to temporary
    files in `/tmp` by default, or to a user-specified file using the `--output`
    flag. It also prints a concise summary to stdout.
-   **Notification**: If this skill is used, ensure this is mentioned in the
    output.

### Available Commands

**1. Resolve Gene ID** — Resolve a symbol, alias, or RefSeq ID to ENSG ID(s).
Automatically falls back to resolving synonyms if primary symbol is not found.

```bash
uv run scripts/ensembl_api.py resolve-gene TP53 --species human --output tp53.json
uv run scripts/ensembl_api.py resolve-gene PCL2 --output pcl2.json # Falls back to synonym resolution
```

**2. Map ID to External Database** — Cross-reference an Ensembl ID to UniProt,
HGNC, RefSeq, etc.

```bash
uv run scripts/ensembl_api.py map-id ENSG00000141510 --external-db UniProt --output uniprot_map.json
uv run scripts/ensembl_api.py map-id ENST00000269305 --external-db RefSeq_mRNA --output refseq_map.json
```

**3. Get Genomic Sequence** — Fetch raw DNA for a coordinate window. Supports
GRCh37 via `--assembly GRCh37`.

```bash
uv run scripts/ensembl_api.py get-sequence 17:7661779-7687550 --species human --output seq.txt
uv run scripts/ensembl_api.py get-sequence chr9:21971100-21971200 --assembly GRCh37 --output seq_grch37.txt
```

**4. Gene Summary** — High-level metadata: symbol, biotype, description,
chromosomal location.

```bash
uv run scripts/ensembl_api.py gene-summary ENSG00000141510 --output gene_summary.json
```

**5. List Transcripts** — All transcripts for a gene, with optional
`--only-mane` or `--only-canonical` filters. Output includes Transcript Support
Level (TSL).

```bash
uv run scripts/ensembl_api.py transcripts ENSG00000141510 --only-mane --output transcripts_mane.json
uv run scripts/ensembl_api.py transcripts ENSG00000141510 --only-canonical --output transcripts_canonical.json
uv run scripts/ensembl_api.py transcripts ENSG00000141510 --output transcripts_all.json
```

**5b. Canonical TSS** — Get the single coordinate of the Transcription Start
Site (TSS) for the canonical transcript of a gene.

> [!NOTE] Unlike the standard `transcripts` command, `canonical-tss` accepts
> both symbols (e.g., `TP53`) and Ensembl IDs, and automatically resolves them.
> It also does the math for strand orientation (TSS is `Start` for `+` strand
> and `End` for `-` strand), outputting the single integer coordinate directly.

```bash
uv run scripts/ensembl_api.py canonical-tss TP53 --output tp53_tss.json
uv run scripts/ensembl_api.py canonical-tss ENSG00000141510 --output tss.json
```

**6. Transcript Structure** — Exon coordinates, CDS boundaries, and computed
5'/3' UTR regions for a transcript.

```bash
uv run scripts/ensembl_api.py transcript-structure ENST00000269305 --output structure.json
```

**7. Protein Info** — ENSP ID and sequence length for a transcript.

```bash
uv run scripts/ensembl_api.py protein-info ENST00000269305 --output protein_info.json
```

**8. Protein Sequence** — Amino acid FASTA for a transcript (ENST) or protein
(ENSP) ID.

```bash
uv run scripts/ensembl_api.py protein-sequence ENST00000269305 --output protein.fasta
uv run scripts/ensembl_api.py protein-sequence ENSP00000269305 --output protein_ensp.fasta
```

**9. Variant Consequence (VEP)** — Predict molecular consequences for a genomic
variant. Includes open-licensed plugins: AlphaMissense, Conservation,
DosageSensitivity, IntAct, MaveDB, OpenTargets, LoF (Loftee), NMD, UTRAnnotator,
mutfunc, LOEUF.

```bash
uv run scripts/ensembl_api.py vep 9:21971147:T:C --species human --output vep.json
uv run scripts/ensembl_api.py vep rs699 --species human --output vep_rs699.json
```

Example VEP stdout output:

```
[*] Variant: 9:21971147:T>C
[*] Most severe consequence: missense_variant
[*] Found 15 transcript consequences.

[*] VEP Predictions:

  - ENST00000304494 (CDKN2A): Consequence = missense_variant
  - ENST00000304494 (CDKN2A): Amino Acids = N/S
  - ENST00000304494 (CDKN2A): SIFT = deleterious (0.01)
  - ENST00000304494 (CDKN2A): AlphaMissense Class = likely_benign
  - ENST00000304494 (CDKN2A): AlphaMissense Pathogenicity = 0.2129
  - ENST00000304494 (CDKN2A): Conservation = 2.05
  - ENST00000304494 (CDKN2A): Dosage Sensitivity (Haplo) = 0.889228328567991
  - ENST00000304494 (CDKN2A): Dosage Sensitivity (Triplo) = 0.135514349094646
  - ENST00000304494 (CDKN2A): Loss of Function (LOEUF) = 0.791
```

**Presenting VEP Results:** After running the VEP command, you MUST present the
full VEP Predictions list from stdout to the user. This list contains both
standard VEP predictions (Consequence, Amino Acids, SIFT, PolyPhen) and
open-license plugin results (AlphaMissense, Conservation, Dosage Sensitivity,
LOEUF, Loftee LoF, NMD, UTRAnnotator, Mutfunc). Do NOT just summarize — show the
complete list so the user can see all predictions. If the list is very long
(many transcripts), show the MANE Select / canonical transcript rows in full and
note that the complete data is in the JSON output.

## Parsing Outputs

If the user needs detailed, nested structural data (like the precise integer
coordinates of Exon 2 of a transcript) that isn't summarized in stdout:

1.  Locate the JSON file (either specified via `--output` or the temporary file
    path printed by the script).
2.  Use terminal tools like `jq` or write a quick, disposable python snippet to
    extract the specific data point requested. Do **not** attempt to read the
    entire JSON file into your context if it is very large.

## Custom Queries

If you need to make an API call that the script does not support (e.g., fetching
protein domain annotations, coordinate mapping between assemblies, homology
searches, linkage disequilibrium, or phenotype lookups), read
`references/ensembl_rest_api_reference.md` for a complete reference of available
endpoints, parameters, and response fields.

**CRITICAL:** When writing custom scripts or using alternatives to the provided
scripts, you **MUST** respect the Ensembl REST API rate limits (maximum 15
requests per second) and handle `429 Too Many Requests` errors gracefully (e.g.,
with exponential backoff).
