---
name: scikit-bio
description: A Python bioinformatics toolkit for sequence, phylogeny, and microbiome/community-ecology analysis. Compute diversity, ordination, and statistics from biological data in standard formats (FASTA/FASTQ/Newick/BIOM).
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---

# scikit-bio

## Overview

scikit-bio is a comprehensive Python library for bioinformatics analyses. Use it for sequence manipulation, alignment, phylogenetics, microbial ecology, and multivariate statistics.

## When to Use This Skill

This skill should be used when you:

- Work with biological sequences (DNA, RNA, protein).
- Need to read/write biological file formats (FASTA, FASTQ, GenBank, Newick, BIOM).
- Perform sequence alignments or search for motifs.
- Construct or analyze phylogenetic trees.
- Calculate diversity metrics (alpha/beta diversity, UniFrac distances).
- Perform ordination analysis (PCoA, CCA, RDA).
- Run statistical tests on biological/ecological data (PERMANOVA, ANOSIM, Mantel).
- Analyze microbiome or community ecology data.
- Work with protein embeddings from language models.
- Need to manipulate biological data tables.

## Core Capabilities

### 1. Sequence Manipulation

Work with biological sequences using specialized classes for DNA, RNA, and protein data.

**Key operations:**

- Read/write sequences from FASTA, FASTQ, GenBank, EMBL formats.
- Sequence slicing, concatenation, and searching.
- Reverse complement, transcription (DNA→RNA), and translation (RNA→protein).
- Find motifs and patterns using regex.
- Calculate distances (Hamming, k-mer based).
- Handle sequence quality scores and metadata.

**Common patterns:**

```python
import skbio

# Read sequences from file
seq = skbio.DNA.read('input.fasta')

# Sequence operations
rc = seq.reverse_complement()
rna = seq.transcribe()
protein = rna.translate()

# Find motifs
motif_positions = seq.find_with_regex('ATG[ACGT]{3}')

# Check for properties
has_degens = seq.has_degenerates()
seq_no_gaps = seq.degap()
```

**Important notes:**

- Use `DNA`, `RNA`, `Protein` classes for grammared sequences with validation.
- Use `Sequence` class for generic sequences without alphabet restrictions.
- Quality scores automatically loaded from FASTQ files into positional metadata.
- Metadata types: sequence-level (ID, description), positional (per-base), interval (regions/features).

### 2. Sequence Alignment

Perform pairwise and multiple sequence alignments using dynamic programming algorithms.

**Key capabilities:**

- Global alignment (Needleman-Wunsch with semi-global variant).
- Local alignment (Smith-Waterman).
- Configurable scoring schemes (match/mismatch, gap penalties, substitution matrices).
- CIGAR string conversion.
- Multiple sequence alignment storage and manipulation with `TabularMSA`.

**Common patterns:**

```python
from skbio.alignment import local_pairwise_align_ssw, TabularMSA

# Pairwise alignment
alignment = local_pairwise_align_ssw(seq1, seq2)

# Access aligned sequences
msa = alignment.aligned_sequences

# Read multiple alignment from file
msa = TabularMSA.read('alignment.fasta', constructor=skbio.DNA)

# Calculate consensus
consensus = msa.consensus()
```

**Important notes:**

- Use `local_pairwise_align_ssw` for local alignments (faster, SSW-based).
- Use `StripedSmithWaterman` for protein alignments.
- Affine gap penalties recommended for biological sequences.
- Can convert between scikit-bio, BioPython, and Biotite alignment formats.

### 3. Phylogenetic Trees

Construct, manipulate, and analyze phylogenetic trees representing evolutionary relationships.

**Key capabilities:**

- Tree construction from distance matrices (UPGMA, WPGMA, Neighbor Joining, GME, BME).
- Tree manipulation (pruning, rerooting, traversal).
- Distance calculations (patristic, cophenetic, Robinson-Foulds).
- ASCII visualization.
- Newick format I/O.

**Common patterns:**

```python
from skbio import TreeNode
from skbio.tree import nj

# Read tree from file
tree = TreeNode.read('tree.nwk')

# Construct tree from distance matrix
tree = nj(distance_matrix)

# Tree operations
subtree = tree.shear(['taxon1', 'taxon2', 'taxon3'])
tips = [node for node in tree.tips()]
lca = tree.lowest_common_ancestor(['taxon1', 'taxon2'])

# Calculate distances
patristic_dist = tree.find('taxon1').distance(tree.find('taxon2'))
cophenetic_matrix = tree.cophenetic_matrix()

# Compare trees
rf_distance = tree.robinson_foulds(other_tree)
```

**Important notes:**

- Use `nj()` for neighbor joining (classic phylogenetic method).
- Use `upgma()` for UPGMA (assumes molecular clock).
- GME and BME are highly scalable for large trees.
- Trees can be rooted or unrooted; some metrics require specific rooting.

### 4. Diversity Analysis

Calculate alpha and beta diversity metrics for microbial ecology and community analysis.

**Key capabilities:**

- Alpha diversity: richness, Shannon entropy, Simpson index, Faith's PD, Pielou's evenness.
- Beta diversity: Bray-Curtis, Jaccard, weighted/unweighted UniFrac, Euclidean distances.
- Phylogenetic diversity metrics (require tree input).
- Rarefaction and subsampling.
- Integration with ordination and statistical tests.

**Common patterns:**

```python
from skbio.diversity import alpha_diversity, beta_diversity
import skbio

# Alpha diversity
alpha = alpha_diversity('shannon', counts_matrix, ids=sample_ids)
faith_pd = alpha_diversity('faith_pd', counts_matrix, ids=sample_ids,
                          tree=tree, otu_ids=feature_ids)

# Beta diversity
bc_dm = beta_diversity('braycurtis', counts_matrix, ids=sample_ids)
unifrac_dm = beta_diversity('unweighted_unifrac', counts_matrix,
                           ids=sample_ids, tree=tree, otu_ids=feature_ids)

# Get available metrics
from skbio.diversity import get_alpha_diversity_metrics
print(get_alpha_diversity_metrics())
```

**Important notes:**

- Counts must be integers representing abundances, not relative frequencies.
- Phylogenetic metrics (Faith's PD, UniFrac) require tree and OTU ID mapping.
- Use `partial_beta_diversity()` for computing specific sample pairs only.
- Alpha diversity returns Series, beta diversity returns DistanceMatrix.

### 5. Ordination Methods

Reduce high-dimensional biological data to visualizable lower-dimensional spaces.

**Key capabilities:**

- PCoA (Principal Coordinate Analysis) from distance matrices.
- CA (Correspondence Analysis) for contingency tables.
- CCA (Canonical Correspondence Analysis) with environmental constraints.
- RDA (Redundancy Analysis) for linear relationships.
- Biplot projection for feature interpretation.

**Common patterns:**

```python
from skbio.stats.ordination import pcoa, cca

# PCoA from distance matrix
pcoa_results = pcoa(distance_matrix)
pc1 = pcoa_results.samples['PC1']
pc2 = pcoa_results.samples['PC2']

# CCA with environmental variables
cca_results = cca(species_matrix, environmental_matrix)

# Save/load ordination results
pcoa_results.write('ordination.txt')
results = skbio.OrdinationResults.read('ordination.txt')
```

**Important notes:**

- PCoA works with any distance/dissimilarity matrix.
- CCA reveals environmental drivers of community composition.
- Ordination results include eigenvalues, proportion explained, and sample/feature coordinates.
- Results integrate with plotting libraries (matplotlib, seaborn, plotly).

### 6. Statistical Testing

Perform hypothesis tests specific to ecological and biological data.

**Key capabilities:**

- PERMANOVA: test group differences using distance matrices.
- ANOSIM: alternative test for group differences.
- PERMDISP: test homogeneity of group dispersions.
- Mantel test: correlation between distance matrices.
- Bioenv: find environmental variables correlated with distances.

**Common patterns:**

```python
from skbio.stats.distance import permanova, anosim, mantel

# Test if groups differ significantly
permanova_results = permanova(distance_matrix, grouping, permutations=999)
print(f"p-value: {permanova_results['p-value']}")

# ANOSIM test
anosim_results = anosim(distance_matrix, grouping, permutations=999)

# Mantel test between two distance matrices
mantel_results = mantel(dm1, dm2, method='pearson', permutations=999)
print(f"Correlation: {mantel_results[0]}, p-value: {mantel_results[1]}")
```

**Important notes:**

- Permutation tests provide non-parametric significance testing.
- Use 999+ permutations for robust p-values.
- PERMANOVA sensitive to dispersion differences; pair with PERMDISP.
- Mantel tests assess matrix correlation (e.g., geographic vs genetic distance).

### 7. File I/O and Format Conversion

Read and write 19+ biological file formats with automatic format detection.

**Supported formats:**

- Sequences: FASTA, FASTQ, GenBank, EMBL, QSeq
- Alignments: Clustal, PHYLIP, Stockholm
- Trees: Newick
- Tables: BIOM (HDF5 and JSON)
- Distances: delimited square matrices
- Analysis: BLAST+6/7, GFF3, Ordination results
- Metadata: TSV/CSV with validation

**Common patterns:**

```python
import skbio

# Read with automatic format detection
seq = skbio.DNA.read('file.fasta', format='fasta')
tree = skbio.TreeNode.read('tree.nwk')

# Write to file
seq.write('output.fasta', format='fasta')

# Generator for large files (memory efficient)
for seq in skbio.io.read('large.fasta', format='fasta', constructor=skbio.DNA):
    process(seq)

# Convert formats
seqs = list(skbio.io.read('input.fastq', format='fastq', constructor=skbio.DNA))
skbio.io.write(seqs, format='fasta', into='output.fasta')
```

**Important notes:**

- Use generators for large files to avoid memory issues.
- Format can be auto-detected when `into` parameter specified.
- Some objects can be written to multiple formats.
- Support for stdin/stdout piping with `verify=False`.

### 8. Distance Matrices

Create and manipulate distance/dissimilarity matrices with statistical methods.

**Key capabilities:**

- Store symmetric (DistanceMatrix) or asymmetric (DissimilarityMatrix) data.
- ID-based indexing and slicing.
- Integration with diversity, ordination, and statistical tests.
- Read/write delimited text format.

**Common patterns:**

```python
from skbio import DistanceMatrix
import numpy as np

# Create from array
data = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]])
dm = DistanceMatrix(data, ids=['A', 'B', 'C'])

# Access distances
dist_ab = dm['A', 'B']
row_a = dm['A']

# Read from file
dm = DistanceMatrix.read('distances.txt')

# Use in downstream analyses
pcoa_results = pcoa(dm)
permanova_results = permanova(dm, grouping)
```

**Important notes:**

- DistanceMatrix enforces symmetry and zero diagonal.
- DissimilarityMatrix allows asymmetric values.
- IDs enable integration with metadata and biological knowledge.
- Compatible with pandas, numpy, and scikit-learn.

### 9. Biological Tables

Work with feature tables (OTU/ASV tables) common in microbiome research.

**Key capabilities:**

- BIOM format I/O (HDF5 and JSON).
- Integration with pandas, polars, AnnData, numpy.
- Data augmentation techniques (phylomix, mixup, compositional methods).
- Sample/feature filtering and normalization.
- Metadata integration.

**Common patterns:**

```python
from skbio import Table

# Read BIOM table
table = Table.read('table.biom')

# Access data
sample_ids = table.ids(axis='sample')
feature_ids = table.ids(axis='observation')
counts = table.matrix_data

# Filter
filtered = table.filter(sample_ids_to_keep, axis='sample')

# Convert to/from pandas
df = table.to_dataframe()
table = Table.from_dataframe(df)
```

**Important notes:**

- BIOM tables are standard in QIIME 2 workflows.
- Rows typically represent samples, columns represent features (OTUs/ASVs).
- Supports sparse and dense representations.
- Output format configurable (pandas/polars/numpy).

### 10. Protein Embeddings

Work with protein language model embeddings for downstream analysis.

**Key capabilities:**

- Store embeddings from protein language models (ESM, ProtTrans, etc.).
- Convert embeddings to distance matrices.
- Generate ordination objects for visualization.
- Export to numpy/pandas for ML workflows.

**Common patterns:**

```python
from skbio.embedding import ProteinEmbedding, ProteinVector

# Create embedding from array
embedding = ProteinEmbedding(embedding_array, sequence_ids)

# Convert to distance matrix for analysis
dm = embedding.to_distances(metric='euclidean')

# PCoA visualization of embedding space
pcoa_results = embedding.to_ordination(metric='euclidean', method='pcoa')

# Export for machine learning
array = embedding.to_array()
df = embedding.to_dataframe()
```

**Important notes:**

- Embeddings bridge protein language models with traditional bioinformatics.
- Compatible with scikit-bio's distance/ordination/statistics ecosystem.
- SequenceEmbedding and ProteinEmbedding provide specialized functionality.
- Useful for sequence clustering, classification, and visualization.

## Example Usage

```python
# pip install scikit-bio numpy pandas

import numpy as np
import pandas as pd

import skbio
from skbio import DNA, TreeNode
from skbio.diversity import alpha_diversity, beta_diversity
from skbio.stats.ordination import pcoa
from skbio.stats.distance import permanova

# ----------------------------
# 1) Sequence manipulation
# ----------------------------
seq = DNA("ACGTACGTNN--ACGT", metadata={"id": "seq1"})
seq_clean = seq.degap()
rc = seq_clean.reverse_complement()
motif_hits = seq_clean.find_with_regex("ACG[TA]")

print("Original:", str(seq))
print("Degapped:", str(seq_clean))
print("Reverse complement:", str(rc))
print("Motif hits:", list(motif_hits))

# ----------------------------
# 2) Microbiome-style counts
# ----------------------------
# rows = samples, cols = features/OTUs/ASVs
counts = np.array([
    [10,  0,  3,  1],
    [ 0,  8,  2,  0],
    [ 5,  1,  0,  4],
], dtype=int)

sample_ids = ["S1", "S2", "S3"]
feature_ids = ["F1", "F2", "F3", "F4"]

# Alpha diversity (Shannon)
shannon = alpha_diversity("shannon", counts, ids=sample_ids)
print("\nAlpha diversity (Shannon):")
print(shannon)

# Beta diversity (Bray-Curtis) -> DistanceMatrix
dm = beta_diversity("braycurtis", counts, ids=sample_ids)
print("\nBeta diversity (Bray-Curtis) distance matrix:")
print(dm)

# ----------------------------
# 3) Ordination (PCoA)
# ----------------------------
ord_res = pcoa(dm)
print("\nPCoA sample coordinates (first 2 axes):")
print(ord_res.samples[["PC1", "PC2"]])

# ----------------------------
# 4) PERMANOVA on the distance matrix
# ----------------------------
grouping = pd.Series(["A", "A", "B"], index=sample_ids)
perma = permanova(dm, grouping=grouping, permutations=99)
print("\nPERMANOVA result:")
print(perma)

# ----------------------------
# 5) Tree I/O (Newick) + basic manipulation
# ----------------------------
newick = "((F1:0.1,F2:0.2):0.3,(F3:0.2,F4:0.4):0.1);"
tree = TreeNode.read([newick])
subtree = tree.shear(["F1", "F2", "F3"])
print("\nSheared tree (tips F1,F2,F3):")
print(subtree.ascii_art())
```

## Implementation Details

- **Sequence model**
  - Use `DNA`/`RNA`/`Protein` for alphabet-aware validation and biological operations (e.g., `reverse_complement`, `transcribe`, `translate`).
  - Use `Sequence` when you need a generic container without strict alphabet constraints.
  - FASTQ quality scores (when read via scikit-bio I/O) are stored as positional metadata.

- **Diversity computations**
  - `alpha_diversity(metric, counts, ids=...)` returns a per-sample vector (typically a pandas `Series`).
  - `beta_diversity(metric, counts, ids=...)` returns a `DistanceMatrix` suitable for ordination and hypothesis tests.
  - Count inputs should be **non-negative integers** representing abundances (not relative frequencies). Phylogenetic metrics (e.g., Faith’s PD, UniFrac) additionally require a tree and feature/OTU IDs.

- **Distance matrices**
  - `DistanceMatrix` enforces symmetry and a zero diagonal; IDs are used for consistent alignment with metadata and group labels.
  - Many downstream methods (PCoA, PERMANOVA, ANOSIM, Mantel) operate directly on `DistanceMatrix`.

- **Ordination**
  - `pcoa(dm)` performs eigen-decomposition on a transformed distance matrix and returns `OrdinationResults` containing eigenvalues and sample coordinates.

- **Permutation-based statistics**
  - `permanova(dm, grouping, permutations=N)` estimates significance by permuting group labels; increase `permutations` (e.g., 999+) for more stable p-values in real analyses.

## Best Practices

### Installation

```bash
uv pip install scikit-bio
```

### Performance Considerations

- Use generators for large sequence files to minimize memory usage.
- For massive phylogenetic trees, prefer GME or BME over NJ.
- Beta diversity calculations can be parallelized with `partial_beta_diversity()`.
- BIOM format (HDF5) more efficient than JSON for large tables.

### Integration with Ecosystem

- Sequences interoperate with Biopython via standard formats.
- Tables integrate with pandas, polars, and AnnData.
- Distance matrices compatible with scikit-learn.
- Ordination results visualizable with matplotlib/seaborn/plotly.
- Works seamlessly with QIIME 2 artifacts (BIOM, trees, distance matrices).

### Common Workflows

1.  **Microbiome diversity analysis**: Read BIOM table → Calculate alpha/beta diversity → Ordination (PCoA) → Statistical testing (PERMANOVA)
2.  **Phylogenetic analysis**: Read sequences → Align → Build distance matrix → Construct tree → Calculate phylogenetic distances
3.  **Sequence processing**: Read FASTQ → Quality filter → Trim/clean → Find motifs → Translate → Write FASTA
4.  **Comparative genomics**: Read sequences → Pairwise alignment → Calculate distances → Build tree → Analyze clades

## Dependencies

- `scikit-bio>=0.6.0`
- `numpy>=1.23`
- `pandas>=1.5`

## Additional Resources

- Official documentation: https://scikit.bio/docs/latest/
- GitHub repository: https://github.com/scikit-bio/scikit-bio
- Forum support: https://forum.qiime2.org (scikit-bio is part of QIIME 2 ecosystem)