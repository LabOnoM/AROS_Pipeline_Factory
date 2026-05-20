# 10x Genomics Space Ranger — Comprehensive Pipeline Reference

## 1. What is Space Ranger?

Space Ranger is the official 10x Genomics analysis pipeline for **Visium** spatial gene expression data. It processes FASTQ reads, aligns them to a reference transcriptome, maps expression back to spatial positions on a tissue slide, and produces feature-barcode matrices at multiple resolutions.

### Supported Tissue Types
- **FFPE** (Formalin-Fixed Paraffin-Embedded)
- **Fixed Frozen (FxF)**
- **Fresh Frozen (FF)**

### Imaging Compatibility
- **Brightfield** (typically H&E stained)
- **Fluorescence** (dark background, or composite colorized)

---

## 2. Pipelines

| Pipeline | Command | Purpose | Visium HD Support |
|----------|---------|---------|-------------------|
| **Count** | `spaceranger count` | Main pipeline: FASTQ → feature-barcode matrices, clustering, DE | ✅ (v3.0+, cell segmentation v4.0+) |
| **Segment** | `spaceranger segment` | Standalone nucleus segmentation from H&E image | ✅ (v4.0+) |
| **Annotate** | `spaceranger annotate` | Cell type annotation from segmented gene expression | ✅ (human/mouse only) |
| **Aggr** | `spaceranger aggr` | Multi-sample aggregation | ❌ Not supported for Visium HD |
| **mkref** | `spaceranger mkref` | **Critical**: Build a custom reference transcriptome | ✅ |

---

## 3. The Reference Transcriptome: A Critical Prerequisite

A valid reference transcriptome is the most critical input for `spaceranger count`. The most common, fatal, and preventable error is providing an incorrectly formatted source FASTA file to the `spaceranger mkref` command.

### 3.1. Policy: Use the Hardened `safe_mkref` Wrapper

To prevent catastrophic `mkref` failures, **do not call `spaceranger mkref` directly.** Instead, use the following hardened shell function, `safe_mkref`. This wrapper function automatically performs the mandatory FASTA validation before executing the command, acting as a critical guardrail.

**Wisdom:** This function fuses the validation policy and the execution action into a single, atomic command. This is the only approved method for creating a reference.

#### **`safe_mkref` Hardened Wrapper Function**
Define this function in your shell environment before proceeding. It will parse the `--fasta` argument, validate the specified file, and only run `spaceranger mkref` if the check passes.

```bash
# safe_mkref: A hardened wrapper for 'spaceranger mkref' that prevents
# failures from empty/invalid FASTA headers.
safe_mkref() {
  echo "--- Running safe_mkref wrapper ---"
  local fasta_file=""

  # Parse arguments to find the --fasta file path
  for arg in "$@"; do
    # Handle --fasta=/path/to/file format
    if [[ "$arg" == --fasta=* ]]; then
      fasta_file="${arg#*=}"
    # Handle --fasta /path/to/file format (will be the next argument)
    elif [[ "$prev_arg" == "--fasta" ]]; then
      fasta_file="$arg"
    fi
    prev_arg="$arg"
  done

  if [ -z "$fasta_file" ]; then
    echo "FATAL: '--fasta' argument not found in command." >&2
    echo "Usage: safe_mkref --genome=MyGenome --fasta=/path/to/genome.fa --genes=/path/to/genes.gtf" >&2
    return 1
  fi
  
  if [ ! -f "$fasta_file" ]; then
    echo "FATAL: FASTA file not found at '$fasta_file'" >&2
    return 1
  fi

  echo "Step 1: Validating FASTA file for empty headers: $fasta_file"
  # Use awk to find any line that starts with '>' and is followed only by optional whitespace.
  # 'getline' ensures we don't flag a trailing '>' at the very end of the file.
  local invalid_header_line
  invalid_header_line=$(awk '/^>[[:space:]]*$/ { line=NR; next_line=getline; if(next_line > 0) {print line} else if (length($0) > 1) {print line} }' "$fasta_file")

  if [ -n "$invalid_header_line" ]; then
    echo "----------------------------------------------------------------" >&2
    echo "FATAL: Validation FAILED. Empty or whitespace-only FASTA header found at line(s): $invalid_header_line" >&2
    echo "This is a fatal error for 'spaceranger mkref'. Aborting operation." >&2
    echo "----------------------------------------------------------------" >&2
    return 1
  else
    echo "SUCCESS: FASTA file passed empty-header validation."
  fi

  echo "Step 2: Validation passed. Executing 'spaceranger mkref'..."
  # Execute the actual command with all original arguments
  spaceranger mkref "$@"
}
```

### 3.2. Example `mkref` Workflow (Hardened)

First, ensure the `safe_mkref` function from Section 3.1 is defined in your current shell session.

```bash
# STEP 1: DEFINE THE HARDENED WRAPPER (copy from Section 3.1)
safe_mkref() { ...pasting function code here... }

# STEP 2: BUILD THE REFERENCE USING THE WRAPPER
# The wrapper will handle validation automatically.
# If the FASTA is invalid, it will exit with an error before spaceranger runs.
safe_mkref \
  --genome=MyGenome \
  --fasta=/path/to/source/genome.fa \
  --genes=/path/to/source/genes.gtf
```

### 3.3. Input File Constraints (Domain Wisdom)

The source FASTA and GTF files must adhere to these rules. The `safe_mkref` wrapper automatically checks for the most common fatal error (Rule #1).

#### FASTA File Rules:
1.  **FATAL (Empty/Null Headers)**: A header line (starting with `>`) **must not** be empty or contain only whitespace (e.g., `>` or `> `). **The `safe_mkref` function enforces this.**
2.  **Unique Headers**: All sequence identifiers after the `>` must be unique.
3.  **Simple Headers Recommended**: `>chr1` is better than `>1 dna:chromosome...`.
4.  **Matching Chromosome Names**: Names must match between the FASTA and GTF files (e.g., `chr1` in FASTA and `chr1` in GTF).

#### GTF File Rules:
- **Required Attributes**: The 9th column **must** contain `gene_id "value";` and `gene_name "value";`.
- **Exon Features**: The 3rd column must contain `exon` features for genes to be included.

---

## 4. `spaceranger count` — Detailed Reference

### 4.1. Required Inputs

| Input | Flag | Format | Notes |
|-------|------|--------|-------|
| Reference transcriptome | `--transcriptome` | Directory | **Must be a directory created by `spaceranger mkref` via the `safe_mkref` wrapper**. See Section 3. |
| CytAssist image | `--cytaimage` | TIFF | **Required** for all CytAssist-processed slides |
| Microscope image | `--image` / `--darkimage` / `--colorizedimage` | TIFF, QPTIFF, BTF, JPEG | **Optional** but critical for segmentation; `--image` for brightfield H&E |
| FASTQ files | `--fastqs` | Directory | Output from `bcl2fastq` / `mkfastq` |
| Probe set | `--probe-set` | CSV | Required for Visium HD (FFPE/probe-based); **NOT** for Visium HD 3' |
| Slide parameters | `--slide` + `--area` | String | Use `--unknown-slide` if slide info is unavailable. |

---

## 8. Pre-Run Checks & Troubleshooting

| Check | Command / Action | Purpose |
|---|---|---|
| **Build Reference Safely** | Use the `safe_mkref` function from Section 3.1. | **Critical**: This is the only approved method. It automatically validates the source FASTA to prevent the most common fatal error. |
| **Validate Reference Output**| `ls -R /path/to/transcriptome` | Ensure the built reference directory contains `fasta/`, `genes/`, and `star/` subdirectories. If not, the build failed. |
| **Check GTF Attributes**| `grep -v "^#" /path/to/source.gtf | cut -f9 | head` | Verify the 9th column contains `gene_id` and `gene_name`. |
| Disk space | `df -h .` | Ensure at least 300GB, preferably 1TB, of free space. |

### Common Issues

| Issue | Solution |
|-------|----------|
| **Immediate failure of `mkref`** | You likely called `spaceranger mkref` directly instead of using the **`safe_mkref` wrapper function from Section 3.1**. The most probable cause is an empty FASTA header. Always use the hardened wrapper to build references. |
| **Immediate failure of `count`**| The **reference transcriptome** is invalid. Verify it was built successfully using `safe_mkref` and that the source files met all constraints in Section 3. |
| Fiducial alignment failure | Use `--loupe-alignment` with manual Loupe Browser alignment. |