# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""
STRING Physical Network Analysis for AP-MS Co-Purification Hypothesis Testing.

This script is a specialized workflow on top of the base StringClient.
It tests whether non-membrane proteins identified in a membrane enrichment
proteomics experiment can be explained by documented physical PPIs 
with the membrane protein fraction.

Key design decisions:
  - Species: 10090 (Mus musculus) — used natively, no ortholog conversion needed
  - Network type: physical (escore + dscore only, excludes text-mining/coexpression)
  - Confidence threshold: 700 (high confidence, experimental evidence preferred)
  - Batching: STRING API limits to ~2000 proteins; we chunk if necessary

Usage:
    python3 string_ppi_analysis.py \
        --lysate_csv 01.Results/ESI-IT-MS/Lysate_Combined/02.Data_Tables/gene_abundances.csv \
        --pellet_csv 01.Results/ESI-IT-MS/Pellet_Combined/02.Data_Tables/gene_abundances.csv \
        --localization_csv 01.Results/ESI-IT-MS/Lysate_Combined/02.Data_Tables/abundance_weighted_cc_ratios.csv \
        --out_dir 01.Results/ESI-IT-MS/PPI_Analysis
"""

import sys, os, time, io, json
import pandas as pd
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

STRING_API = "https://version-12-0.string-db.org/api"
SPECIES = 10090        # Mus musculus
SCORE_THRESHOLD = 700  # High confidence physical interactions
CALLER = "kusa_ppi_analysis"

MEMBRANE_KEYWORDS = [
    "membrane", "transmembrane", "plasma membrane", "cell membrane",
    "lipid bilayer", "integral membrane", "membrane protein",
]


def map_ids(gene_list: list) -> dict:
    """Map gene symbols to STRING IDs for mouse."""
    params = {
        "identifiers": "\r".join(gene_list),
        "species": SPECIES,
        "echo_query": 1,
        "caller_identity": CALLER,
    }
    r = requests.post(f"{STRING_API}/tsv-no-header/get_string_ids", data=params, timeout=30)
    r.raise_for_status()
    mapping = {}
    for line in r.text.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            query_gene = parts[0].strip()
            string_id = parts[2].strip()
            mapping[query_gene] = string_id
    return mapping


def get_physical_network(string_ids: list) -> pd.DataFrame:
    """
    Retrieve physical interaction network for a set of STRING IDs.
    Uses 'network_type=physical' to restrict to experimental + database evidence.
    """
    params = {
        "identifiers": "\r".join(string_ids),
        "species": SPECIES,
        "required_score": SCORE_THRESHOLD,
        "network_type": "physical",
        "caller_identity": CALLER,
    }
    r = requests.post(f"{STRING_API}/tsv/network", data=params, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text), sep="\t")
    return df


def get_network_image(string_ids: list, out_path: str):
    """Download a physical network PNG image."""
    params = {
        "identifiers": "\r".join(string_ids[:50]),  # limit to 50 for readability
        "species": SPECIES,
        "required_score": SCORE_THRESHOLD,
        "network_type": "physical",
        "network_flavor": "confidence",
        "caller_identity": CALLER,
    }
    r = requests.post(f"{STRING_API}/image/network", data=params, timeout=60)
    r.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(r.content)
    print(f"  Network image saved to: {out_path}")


def classify_by_localization(gene_list: list, mapping_df: pd.DataFrame) -> dict:
    """
    Split gene list into membrane vs. non-membrane based on
    UniProt subcellular location annotations already in the mapping table.
    
    mapping_df must have columns: Gene_Symbol, Subcellular_Location (or similar)
    Falls back to keyword matching if no annotation available.
    """
    membrane, non_membrane = [], []
    loc_col = None
    for col in ["Subcellular_Location", "Subcellular", "location", "cc"]:
        if col in mapping_df.columns:
            loc_col = col
            break

    for gene in gene_list:
        if loc_col:
            rows = mapping_df[mapping_df["Gene_Symbol"] == gene]
            if not rows.empty:
                loc = str(rows.iloc[0][loc_col]).lower()
                if any(kw in loc for kw in MEMBRANE_KEYWORDS):
                    membrane.append(gene)
                else:
                    non_membrane.append(gene)
            else:
                non_membrane.append(gene)
        else:
            # No annotation — place in non-membrane (conservative)
            non_membrane.append(gene)

    return {"membrane": membrane, "non_membrane": non_membrane}


def run_ppi_analysis(
    membrane_genes: list,
    candidate_genes: list,
    out_dir: str,
    fraction_name: str = "Fraction",
):
    """
    Core analysis: test how many candidate (non-membrane) proteins
    have documented physical interactions with membrane proteins.

    Steps:
        1. Map all genes to STRING IDs
        2. Get physical interaction network for membrane proteins
        3. Count how many candidate genes appear as interaction partners
        4. Report and export

    Returns:
        dict with ppi_hit_genes, ppi_miss_genes, network_df, coverage_pct
    """
    os.makedirs(out_dir, exist_ok=True)

    all_genes = list(set(membrane_genes + candidate_genes))
    print(f"\n[{fraction_name}] Mapping {len(all_genes)} genes to STRING IDs...")

    # Chunk if needed (STRING max ~2000)
    id_map = {}
    chunk_size = 500
    for i in range(0, len(all_genes), chunk_size):
        chunk = all_genes[i:i + chunk_size]
        chunk_map = map_ids(chunk)
        id_map.update(chunk_map)
        time.sleep(1)

    membrane_ids = [id_map[g] for g in membrane_genes if g in id_map]
    candidate_ids = [id_map[g] for g in candidate_genes if g in id_map]

    print(f"  Mapped {len(membrane_ids)}/{len(membrane_genes)} membrane proteins")
    print(f"  Mapped {len(candidate_ids)}/{len(candidate_genes)} candidate proteins")
    print(f"  Querying STRING physical network (score ≥ {SCORE_THRESHOLD})...")

    # Get physical network for membrane proteins (their interaction partners)
    if not membrane_ids:
        print("  ERROR: No membrane proteins could be mapped to STRING IDs.")
        return None

    net_df = get_physical_network(membrane_ids)
    time.sleep(1)

    # Collect all STRING IDs that interact with any membrane protein
    interacting_ids = set()
    if not net_df.empty:
        for col in ["stringId_A", "stringId_B"]:
            if col in net_df.columns:
                interacting_ids.update(net_df[col].tolist())

    # Remove membrane proteins themselves from interacting set
    membrane_id_set = set(membrane_ids)
    interacting_nonmembrane = interacting_ids - membrane_id_set

    # Map back to gene names
    reverse_map = {v: k for k, v in id_map.items()}
    hit_genes = [reverse_map[sid] for sid in interacting_nonmembrane
                 if sid in reverse_map and reverse_map[sid] in candidate_genes]
    miss_genes = [g for g in candidate_genes if g not in hit_genes]

    coverage = len(hit_genes) / max(len(candidate_genes), 1) * 100

    print(f"\n{'='*60}")
    print(f"PPI Coverage Analysis — {fraction_name}")
    print(f"{'='*60}")
    print(f"  Membrane proteins queried      : {len(membrane_genes)}")
    print(f"  Non-membrane proteins tested   : {len(candidate_genes)}")
    print(f"  PPI-explained (hit)            : {len(hit_genes)} ({coverage:.1f}%)")
    print(f"  Unexplained (miss)             : {len(miss_genes)} ({100-coverage:.1f}%)")

    # Save network image (top 50 membrane proteins + their hits)
    top_ids = membrane_ids[:40] + [id_map[g] for g in hit_genes[:10] if g in id_map]
    if top_ids:
        get_network_image(top_ids, os.path.join(out_dir, f"{fraction_name}_ppi_network.png"))

    # Export results
    results_df = pd.DataFrame({
        "Gene_Symbol": hit_genes + miss_genes,
        "PPI_Explained": ["Yes"] * len(hit_genes) + ["No"] * len(miss_genes),
    })
    out_csv = os.path.join(out_dir, f"{fraction_name}_ppi_results.csv")
    results_df.to_csv(out_csv, index=False)
    print(f"  Results saved to: {out_csv}")

    return {
        "ppi_hit_genes": hit_genes,
        "ppi_miss_genes": miss_genes,
        "network_df": net_df,
        "coverage_pct": coverage,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="STRING physical PPI analysis for membrane co-purification hypothesis"
    )
    parser.add_argument("--genes_csv", required=True,
                        help="gene_abundances.csv (Gene_Symbol column required)")
    parser.add_argument("--membrane_list", default=None,
                        help="Optional: newline-separated file of membrane gene symbols")
    parser.add_argument("--clean_genes", default=None,
                        help="Optional: newline-separated file of CRAPome-cleaned genes")
    parser.add_argument("--out_dir", required=True, help="Output directory")
    parser.add_argument("--fraction", default="Fraction", help="Label for this fraction")
    args = parser.parse_args()

    all_genes_df = pd.read_csv(args.genes_csv)
    all_genes = all_genes_df["Gene_Symbol"].tolist()

    if args.membrane_list:
        with open(args.membrane_list) as f:
            membrane_genes = [g.strip() for g in f if g.strip()]
    else:
        print("WARNING: No membrane gene list provided — all proteins used as candidates.")
        membrane_genes = all_genes[:50]  # placeholder

    if args.clean_genes:
        with open(args.clean_genes) as f:
            candidate_genes = [g.strip() for g in f if g.strip()]
    else:
        candidate_genes = [g for g in all_genes if g not in membrane_genes]

    run_ppi_analysis(membrane_genes, candidate_genes, args.out_dir, args.fraction)
