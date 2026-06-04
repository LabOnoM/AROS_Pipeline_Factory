# /proteomics-enrichment Workflow

## Purpose
End-to-end reproducible proteomics pipeline for Emilio_Proteomics project.
Converts raw Bruker ESI-IT-MS data to enrichment reports.
Compatible with: KUSA-1a/b, KUSA-2, KUSA-3, KUSA-4 (Pre-incubation), KUSA-5 (PMNF-3D).

---

## Prerequisites

**Conda-Gated Dependency Preflight** (per `self_healing_environment_policy` v2.0, SPEC §4.4):

```bash
# --- L0: Ensure Conda ---
if ! command -v conda &> /dev/null; then
    if [ -f "$HOME/miniconda3/bin/conda" ]; then
        eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    elif [ -f "$HOME/anaconda3/bin/conda" ]; then
        eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
    else
        echo "  [WARN] Conda not found. Bootstrapping Miniconda3..."
        curl -fsSL --max-time 120 "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-$(uname -m).sh" \
            -o /tmp/miniconda.sh && bash /tmp/miniconda.sh -b -u -p "$HOME/miniconda3" && \
            eval "$($HOME/miniconda3/bin/conda shell.bash hook)" && rm -f /tmp/miniconda.sh
    fi
fi

# --- L1: Activate aros-base ---
if command -v conda &> /dev/null; then
    eval "$(conda shell.bash hook)"
    if ! conda activate aros-base 2>/dev/null; then
        CMD=$(command -v mamba &>/dev/null && echo "mamba" || echo "conda")
        AROS_YML="$HOME/.gemini/environments/aros-base.yml"
        [ ! -f "$AROS_YML" ] && AROS_YML="01.Shared_Assets/Environments/aros-base.yml"
        [ ! -f "$AROS_YML" ] && AROS_YML="$(find ~ -maxdepth 4 -name 'aros-base.yml' -print -quit 2>/dev/null)"
        if [ -n "$AROS_YML" ]; then
            $CMD env create -f "$AROS_YML" -y && conda activate aros-base
        else
            $CMD create -n aros-base python=3.11 git pandoc -c conda-forge -y && conda activate aros-base
        fi
    fi
fi

# --- Proteomics-specific packages (CRITICAL — required for all stages) ---
REQUIRED_PKGS="pyteomics pyopenms pandas numpy openpyxl beautifulsoup4 gseapy"
MISSING=""
for pkg in $REQUIRED_PKGS; do
    python3 -c "import $pkg" 2>/dev/null || MISSING="$MISSING $pkg"
done
if [ -n "$MISSING" ]; then
    echo "  Installing missing Python packages:$MISSING"
    CMD=$(command -v mamba &>/dev/null && echo "mamba" || echo "conda")
    $CMD install -n aros-base $MISSING -c conda-forge -y 2>/dev/null || \
        pip install $MISSING || {
            echo "  ❌ [HALT] CRITICAL: Package install failed for:$MISSING"
            exit 1
        }
else
    echo "  ✅ All Python packages present."
fi

# --- Self-Healing: Docker Check (IMPORTANT — only needed for .yep → .mzML conversion) ---
if command -v docker &> /dev/null; then
    docker image inspect chambm/pwiz-skyline-i-agree-to-the-vendor-licenses &> /dev/null || {
        echo "  Pulling ProteoWizard Docker image..."
        docker pull chambm/pwiz-skyline-i-agree-to-the-vendor-licenses || \
            echo "  [WARN] Docker pull failed. Stage 0 (.yep→.mzML) will be unavailable."
    }
else
    echo "  [WARN] Docker not found. Stage 0 (.yep→.mzML conversion) will be unavailable."
    echo "  If .mzML files already exist, subsequent stages will work without Docker."
fi

# FASTA database (Mus musculus, SwissProt reviewed)
# Download from: https://www.uniprot.org/uniprot/?query=organism:10090+reviewed:yes&format=fasta
# Save to: /mnt/Disk1/Emilio_Proteomics/References/uniprot_mouse_swissprot.fasta
```

---

## Stage 0: Raw Conversion (`.yep` → `.mzML`)

**When to run**: Only once per sample. Skip if `.mzML` files already exist.

```bash
# Convert a single sample
python3 scripts/ESI-IT-MS/convert_yep_to_mzml.py --sample KUSA-4

# Convert all 6 samples
python3 scripts/ESI-IT-MS/convert_yep_to_mzml.py --all

# Validate existing conversions (no Docker needed)
python3 scripts/ESI-IT-MS/convert_yep_to_mzml.py --validate-only
```

**Output**: `00.RawData/ESI-IT-MS/mzML_converted/<SAMPLE>.mzML`

**Parameters** (from instrument config `1DCHIP-LONG6_2.m`):
- Peak picking: `peakPicking true 1-` (mandatory for centroiding)
- Zero removal: `zeroSamples removeExtra`

> **CRITICAL**: Without `peakPicking`, data will be in profile mode and fragment matching will fail.

---

## Stage 1: Spectral Search

**When to run**: After Stage 0. Run KUSA-4 first for validation.

```bash
# ESI-IT-MS samples
MZML_DIR="/mnt/Disk1/Emilio_Proteomics/00.RawData/ESI-IT-MS/mzML_converted"
FASTA="/mnt/Disk1/Emilio_Proteomics/References/uniprot_mouse_swissprot.fasta"
RESULTS="/mnt/Disk1/Emilio_Proteomics/01.Results/ESI-IT-MS"

# Run KUSA-4 first (validation target)
python3 scripts/ESI-IT-MS/esi_spectral_search.py \
    --mzml "$MZML_DIR/260414KUSA_LYSATE.mzML" \
    --fasta "$FASTA" \
    --sample-id KUSA-4 \
    --outdir "$RESULTS/KUSA-4/02.Data_Tables/"

# Then remaining samples (after validation passes):
for SAMPLE in KUSA-1a KUSA-1b KUSA-2 KUSA-3 KUSA-5; do
    # Map sample ID to mzML filename
    case $SAMPLE in
        KUSA-1a) MZML="251223_KUSA.mzML" ;;
        KUSA-1b) MZML="251223_KUSA2.mzML" ;;
        KUSA-2)  MZML="260209_1.mzML" ;;
        KUSA-3)  MZML="260209_2.mzML" ;;
        KUSA-5)  MZML="260416KUSA_LYSATE_3D.mzML" ;;
    esac

    python3 scripts/ESI-IT-MS/esi_spectral_search.py \
        --mzml "$MZML_DIR/$MZML" \
        --fasta "$FASTA" \
        --sample-id "$SAMPLE" \
        --outdir "$RESULTS/$SAMPLE/02.Data_Tables/"
done
```

**Search Parameters**:
| Parameter | Value |
|---|---|
| Precursor tolerance | ±1.5 Da |
| Fragment tolerance | ±0.5 Da |
| Fixed modification | Carbamidomethylation (C, +57.021 Da) |
| Variable modification | Oxidation (M, +15.995 Da) |
| Enzyme | Trypsin (K/R, not before P) |
| Missed cleavages | 1 |
| Charge states | 2+, 3+ |
| Database | Mouse SwissProt |
| FDR | 1% peptide-level |

**Outputs per sample**:
- `psm_results.csv` — All Peptide-Spectrum Matches
- `peptide_abundance_matrix.csv` — Peptide-level (de novo ready)
- `protein_mapping_results.xlsx` — Protein rollup for enrichment

---

## Stage 2: Validation (KUSA-4 only)

**When to run**: After Stage 1 for KUSA-4, before running all other samples.

```bash
python3 scripts/ESI-IT-MS/validate_vs_spectrum_mill.py \
    --sample-id KUSA-4 \
    --our-results 01.Results/ESI-IT-MS/KUSA-4/02.Data_Tables/protein_mapping_results.xlsx \
    --html-dir 00.RawData/ESI-IT-MS/20260414-Proteomic-LC-MS-KUSA-4/
```

**Acceptance**: ≥70% overlap in top-30 proteins.
**If fails**: See diagnostic output and adjust tolerances in `esi_spectral_search.py`.

---

## Stage 3: GSEA Enrichment Analysis

**When to run**: After Stage 1, for each sample independently.

```bash
# Generate GSEA reports
python3 scripts/ESI-IT-MS/generate_reports.py

# Generate interactive FEA
python3 scripts/ESI-IT-MS/generate_clickable_assets.py

# Inject QC metrics
python3 scripts/ESI-IT-MS/inject_qc_html.py
```

---

## Stage 4: Cross-Condition Comparison

**When to run**: After all samples complete Stage 1.

```bash
python3 scripts/Comparison/compare_preincubation_vs_pmnf3d.py \
    --results-dir 01.Results/
```

**Outputs**:
- `01.Results/Comparison/comparison_report.html` — Interactive report
- `01.Results/Comparison/differential_proteins.csv` — Log2FC table
- `01.Results/Comparison/protein_abundance_matrix.csv` — All samples matrix
- `01.Results/Comparison/venn_protein_sets.csv` — Set overlaps

---

## Stage 5: Documentation

```bash
# Rebuild Project Registry (INDEX.csv or PIPELINE_REGISTRY.md)
python3 scripts/rebuild_index.py  # If available

# Git commit
git add -A
git commit -m "feat: add raw spectral search results for <SAMPLE>"
```

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `docker: command not found` | Docker not in PATH | `export PATH=$PATH:/usr/local/bin` |
| `No PSMs found` | Profile-mode mzML | Rerun with `peakPicking true 1-` |
| `FDR filter rejects everything` | Wrong FASTA organism | Use Mus musculus SwissProt |
| `GSEA fails silently` | <15 genes | Check FDR cutoff, try 5% |
| `Validation overlap <30%` | Tolerance too tight | Increase PRECURSOR_TOL to 2.0 Da |

---

## Related Scripts
- `convert_yep_to_mzml.py` — Stage 0
- `esi_spectral_search.py` — Stage 1
- `validate_vs_spectrum_mill.py` — Stage 2
- `generate_reports.py` — Stage 3 (existing)
- `generate_clickable_assets.py` — Stage 3 (existing)
- `inject_qc_html.py` — Stage 3 (existing)
- `compare_preincubation_vs_pmnf3d.py` — Stage 4
