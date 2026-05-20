---
name: glycoengineering
description: Analyze and engineer protein glycosylation. Scan sequences for N-glycosylation sequons (N-X-S/T), predict O-glycosylation hotspots, and access curated glycoengineering tools (NetOGlyc, GlycoShield, GlycoWorkbench). For glycoprotein engineering, therapeutic antibody optimization, and vaccine design.
license: Unknown
metadata:
    skill-author: Kuan-lin Huang
---

# Glycoengineering

## Overview

Glycosylation is the most common and complex post-translational modification (PTM) of proteins, affecting over 50% of all human proteins. Glycans regulate protein folding, stability, immune recognition, receptor interactions, and pharmacokinetics of therapeutic proteins. Glycoengineering involves rational modification of glycosylation patterns for improved therapeutic efficacy, stability, or immune evasion.

**Two major glycosylation types:**
- **N-glycosylation**: Attached to asparagine (N) in the sequon N-X-[S/T] where X ≠ Proline; occurs in the ER/Golgi
- **O-glycosylation**: Attached to serine (S) or threonine (T); no strict consensus motif; primarily GalNAc initiation

## When to Use This Skill

Use this skill when:

- **Antibody engineering**: Optimize Fc glycosylation for enhanced ADCC, CDC, or reduced immunogenicity
- **Therapeutic protein design**: Identify glycosylation sites that affect half-life, stability, or immunogenicity
- **Vaccine antigen design**: Engineer glycan shields to focus immune responses on conserved epitopes
- **Biosimilar characterization**: Compare glycan patterns between reference and biosimilar
- **Drug target analysis**: Does glycosylation affect target engagement for a receptor?
- **Protein stability**: N-glycans often stabilize proteins; identify sites for stabilizing mutations

## Glycoengineering Tools

This skill provides functions for analyzing and modifying glycosylation sites. It can also be used in conjunction with external curated glycoengineering tools like NetOGlyc, GlycoShield, and GlycoWorkbench for more advanced predictions and analyses.

## N-Glycosylation Sequon Analysis

### Scanning for N-Glycosylation Sites

N-glycosylation occurs at the sequon **N-X-[S/T]** where X ≠ Proline.

```python
import re
from typing import List, Dict, Tuple

def find_n_glycosylation_sequons(sequence: str) -> List[Dict]:
    """
    Scan a protein sequence for canonical N-linked glycosylation sequons.
    Motif: N-X-[S/T], where X ≠ Proline.

    Args:
        sequence: Single-letter amino acid sequence

    Returns:
        List of dicts with position (1-based), motif, context, and sequon_type
    """
    seq = sequence.upper()
    results = []
    i = 0
    while i <= len(seq) - 3:
        triplet = seq[i:i+3]
        if triplet[0] == 'N' and triplet[1] != 'P' and triplet[2] in {'S', 'T'}:
            context = seq[max(0, i-3):i+6]  # ±3 residue context
            results.append({
                'position': i + 1,   # 1-based
                'motif': triplet,
                'context': context,
                'sequon_type': 'NXS' if triplet[2] == 'S' else 'NXT'
            })
        i += 1 # Increment i to avoid infinite loop
    return results
```

### Summarizing N-Glycosylation Sites

```python
def summarize_glycosylation_sites(sequence: str, protein_name: str = "") -> str:
    """
    Generates a summary report of N-glycosylation sequons found in a protein sequence.

    Args:
        sequence: Single-letter amino acid sequence.
        protein_name: Optional name of the protein for the report header.

    Returns:
        A formatted string summarizing the N-glycosylation sites.
    """
    sequons = find_n_glycosylation_sequons(sequence)
    lines = [f"# N-Glycosylation Sequon Analysis: {protein_name or 'Protein'}"]
    lines.append(f"Sequence length: {len(sequence)}")
    lines.append(f"Total N-glycosylation sequons: {len(sequons)}")
    if sequons:
        lines.append(f"\nN-X-S sites: {sum(1 for s in sequons if s['sequon_type'] == 'NXS')}")
        lines.append(f"N-X-T sites: {sum(1 for s in sequons if s['sequon_type'] == 'NXT')}")
        lines.append(f"\nSite details:")
        for s in sequons:
            lines.append(f"  Position {s['position']}: {s['motif']} (context: ...{s['context']}...)")
    else:
        lines.append("\nNo N-glycosylation sequons found.")
    return "\n".join(lines)
```

## Glycosylation Site Engineering

### Eliminating N-Glycosylation Sites

```python
def eliminate_glycosite(sequence: str, position: int, replacement: str = "Q") -> str:
    """
    Eliminate an N-glycosylation site by mutating the Asn residue at the specified position.

    Args:
        sequence: Protein sequence.
        position: 1-based position of the Asn residue to mutate.
        replacement: Amino acid to substitute (default Q = Gln; similar size, not glycosylated).

    Returns:
        Modified protein sequence with the potential glycosylation site removed.
    """
    if not (1 <= position <= len(sequence)):
        raise ValueError("Position out of bounds.")
    
    # A more robust check would verify if it's part of an actual sequon,
    # but for simplicity, we mutate the residue at the given position.
    if sequence[position - 1].upper() != 'N':
        print(f"Warning: Residue at position {position} is not N. Proceeding with mutation to '{replacement}'.")

    seq_list = list(sequence)
    seq_list[position - 1] = replacement
    return "".join(seq_list)
```

### Introducing N-Glycosylation Sites

```python
def add_glycosite(sequence: str, position: int, flanking_context: str = "S") -> str:
    """
    Attempt to introduce an N-glycosylation site (N-X-S/T) at a given position.
    This function is illustrative and might require further context-specific adjustments
    to ensure biological viability and avoid disrupting protein function.

    Args:
        sequence: Protein sequence.
        position: 1-based position to introduce Asn (this will be the 'N' of the sequon).
                  The sequon will be N-X-[S/T] where X is at position+1 and S/T at position+2.
        flanking_context: 'S' or 'T' for the X+2 position.

    Returns:
        Modified protein sequence with an attempted N-glycosylation site.
    """
    if not (1 <= position <= len(sequence) - 2): # Need space for N-X-S/T
        raise ValueError("Position too close to end of sequence to add N-X-S/T sequon.")

    seq_list = list(sequence)
    current_n_pos_aa = seq_list[position - 1].upper()
    current_x_pos_aa = seq_list[position].upper()
    current_st_pos_aa = seq_list[position + 1].upper()
    
    target_st = flanking_context.upper()
    
    # Check if it's already a valid sequon
    if current_n_pos_aa == 'N' and current_x_pos_aa != 'P' and current_st_pos_aa in {'S', 'T'}:
        print(f"Warning: Position {position} already has a valid N-X-S/T sequon.")
        return sequence

    # Attempt to create a sequon
    if current_x_pos_aa == 'P':
        print(f"Cannot introduce N-X-S/T at position {position} because X (position {position+1}) is Proline.")
        return sequence
    
    # Modify to create N-X-S/T
    seq_list[position - 1] = 'N' # Ensure N at position
    if current_st_pos_aa not in {'S', 'T'}:
        seq_list[position + 1] = target_st # Ensure S/T at position+2
        print(f"Modified position {position} to 'N' and position {position+2} to '{target_st}' to create N-X-S/T.")
    else:
        print(f"Modified position {position} to 'N'. Position {position+2} already '{current_st_pos_aa}'.")
    
    return "".join(seq_list)
```

## O-Glycosylation Hotspot Prediction

```python
def predict_o_glycosylation_hotspots(
    sequence: str,
    window: int = 7,
    min_st_fraction: float = 0.4,
    disallow_proline_next: bool = True
) -> List[Dict]:
    """
    Predict potential O-glycosylation hotspots based on local Serine/Threonine density.
    This is a simplified heuristic, not a full prediction algorithm like NetOGlyc.

    Rules:
        - High density of S/T residues in a local window.
        - Optionally, disallow Proline immediately following S/T (can hinder O-glycosylation).

    Args:
        sequence: Protein sequence.
        window: Odd window size for local S/T density (e.g., 7 means +/- 3 residues).
        min_st_fraction: Minimum fraction of S/T in window to flag a site.
        disallow_proline_next: If True, S/T followed by P will not be considered a hotspot.

    Returns:
        List of dicts with position (1-based), residue, context, and S/T fraction for each hotspot.
    """
    if window % 2 == 0:
        raise ValueError("Window size must be odd.")

    seq = sequence.upper()
    hotspots = []
    half_window = window // 2

    for i, aa in enumerate(seq):
        if aa in ('S', 'T'): # Only consider S or T as potential O-glycosylation sites
            if disallow_proline_next and i + 1 < len(seq) and seq[i+1] == 'P':
                continue # Skip if S/T is followed by Proline and rule is active

            start = max(0, i - half_window)
            end = min(len(seq), i + half_window + 1)
            segment = seq[start:end]
            st_count = sum(1 for char in segment if char in ('S', 'T'))
            
            if len(segment) > 0: # Avoid division by zero for very short sequences/windows
                frac = st_count / len(segment)
            else:
                frac = 0.0

            if frac >= min_st_fraction:
                hotspots.append({
                    'position': i + 1, # 1-based
                    'residue': aa,
                    'context': segment,
                    'st_fraction': round(frac, 2)
                })
    return hotspots
```