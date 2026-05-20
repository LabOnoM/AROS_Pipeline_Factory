---
name: etetoolkit
description: ETE (Environment for Tree Exploration) toolkit for phylogenetic and hierarchical tree analysis; use it when you need to parse/manipulate Newick/NHX trees, detect duplication/speciation events, integrate NCBI taxonomy, and render publication-quality figures.
license: MIT
metadata:
    skill-author: AIPOCH & K-Dense Inc.
---
---

## Overview

ETE (Environment for Tree Exploration) is a toolkit for phylogenetic and hierarchical tree analysis. Manipulate trees, analyze evolutionary events, visualize results, and integrate with biological databases for phylogenomic research and clustering analysis.

## When to Use

- **Preprocess phylogenetic trees**: convert formats (Newick/NHX/PhyloXML), reroot (midpoint/outgroup), prune taxa, and resolve polytomies before downstream analyses.
- **Detect evolutionary events in gene trees**: infer **duplication vs. speciation** events and derive **ortholog/paralog** relationships for phylogenomics.
- **Annotate trees with taxonomy**: map species names to **NCBI TaxIDs**, retrieve lineages/ranks, and build minimal taxonomy topologies connecting a set of taxa.
- **Generate publication-quality visualizations**: render trees to **PDF/SVG/PNG** with custom styles, support-based coloring, and node "faces" (labels, shapes, heatmaps).
- **Compare alternative topologies**: quantify differences between trees using **Robinson–Foulds (RF)** distance and partition/bipartition analysis.
- **Analyze hierarchical clustering results**: Connect tree leaves to numerical profiles, validate cluster quality, and create heatmap visualizations.

## Key Features

- **Tree I/O and manipulation**
    - Read/write: Newick, NHX, PhyloXML, NeXML
    - Traversals: preorder, postorder, levelorder
    - Operations: prune, reroot, collapse, resolve polytomies
    - Metrics: branch/topological distances, Robinson-Foulds distance
- **Phylogenetic (gene tree) analysis**
    - Alignment association (FASTA/Phylip)
    - Species name extraction from gene IDs
    - Duplication/speciation detection (e.g., species overlap / reconciliation-style workflows)
    - Orthology/paralogy extraction and gene-family splitting
- **NCBI taxonomy integration**
    - Auto-download + local cache of taxonomy DB
    - TaxID ↔ scientific name translation
    - Lineage/rank retrieval and taxonomy-based topology building
    - Tree annotation with taxonomic metadata
- **Visualization**
    - Rectangular/circular layouts, GUI exploration
    - NodeStyle/TreeStyle customization
    - Faces (text, shapes, charts/heatmaps) and layout functions
    - Export to PDF/SVG/PNG
- **Clustering support**
    - ClusterTree for dendrograms linked to numeric matrices
    - Cluster quality metrics (e.g., silhouette, Dunn index)
    - Heatmap + tree combined views

## Dependencies

- `ete3` (recommended: `>=3.1.0`)
- Optional GUI/rendering dependencies (platform-specific):
    - `PyQt5` (e.g., `>=5.15`)
    - Qt SVG support (often packaged as `python3-pyqt5.qtsvg` on Debian/Ubuntu)

## Installation and Setup

Install ETE toolkit:

```bash
uv pip install ete3

# With external dependencies for rendering (optional but recommended)
# On macOS:
brew install qt@5

# On Ubuntu/Debian:
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg

# For full features including GUI
uv pip install ete3[gui]
```

First-time NCBI Taxonomy setup:

The first time NCBITaxa is instantiated, it automatically downloads the NCBI taxonomy database (~300MB) to `~/.etetoolkit/taxa.sqlite`. This happens only once:

```python
from ete3 import NCBITaxa
ncbi = NCBITaxa()  # Downloads database on first run
```

Update taxonomy database:

```python
ncbi.update_taxonomy_database()  # Download latest NCBI data
```

## Example Usage

The following example is designed to be runnable end-to-end (it uses an in-memory Newick string and does not require external files).

```python
# pip install ete3

from ete3 import Tree, TreeStyle, NodeStyle

# 1) Load a tree (Newick)
nw = "((A:0.1,B:0.2)90:0.3,(C:0.2,D:0.4)70:0.1);"
t = Tree(nw, format=1)

# 2) Basic stats
print("Leaves:", len(t))
print("Total nodes:", sum(1 for _ in t.traverse()))

# 3) Midpoint rooting
mid = t.get_midpoint_outgroup()
t.set_outgroup(mid)

# 4) Prune to taxa of interest (preserve branch lengths)
t.prune(["A", "C", "D"], preserve_branch_length=True)

# 5) Style nodes (color internal nodes by support)
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_support = True

for n in t.traverse():
    st = NodeStyle()
    if n.is_leaf():
        st["fgcolor"] = "blue"
        st["size"] = 8
    else:
        # ETE stores internal support in n.support when present
        st["fgcolor"] = "darkgreen" if getattr(n, "support", 0) >= 80 else "red"
        st["size"] = 5
    n.set_style(st)

# 6) Render (PDF/SVG/PNG supported depending on your environment)
t.render("example_tree.pdf", tree_style=ts)
print("Wrote: example_tree.pdf")
```

## Implementation Details

### Tree parsing formats (Newick "format" codes)

ETE uses a `format` integer to control how node attributes are interpreted when reading/writing Newick. Common patterns:

- `format=0`: flexible default (often includes branch lengths)
- `format=1`: includes internal node names
- `format=2`: includes support/bootstrap values
- `format=5`: internal node names + branch lengths
- `format=8`: name + distance + support (maximal common usage)
- `format=9`: leaf names only
- `format=100`: topology only

Example:

```python
from ete3 import Tree

t = Tree("tree.nw", format=1)
t.write(outfile="out.nw", format=5)
```

### NHX feature preservation

NHX is used to store custom per-node features. When writing, specify which features to serialize:

```python
t.write(outfile="tree.nhx", features=["taxid", "habitat", "lineage"])
```

### Rerooting and pruning behavior

- **Midpoint rooting** uses `get_midpoint_outgroup()` to select an outgroup that balances path lengths.
- **Pruning** should typically use `preserve_branch_length=True` to avoid distorting distances in phylogenetic contexts.

### Evolutionary event detection (gene trees)

For gene trees, `PhyloTree` supports event labeling on internal nodes (commonly:
- `evoltype == "D"` for duplication
- `evoltype == "S"` for speciation)

A typical workflow is:
1. Load a gene tree (optionally with an alignment).
2. Provide a **species naming function** to map gene IDs → species.
3. Run descendant event detection.
4. Extract ortholog groups (speciation subtrees) or query ortholog/paralog sets from events.

### Tree comparison (Robinson–Foulds)

`Tree.robinson_foulds(other_tree)` returns:

- `rf`: RF distance (number of differing bipartitions)
- `max_rf`: maximum possible RF given shared leaves
- plus shared leaves and partition sets for deeper inspection

Normalized RF is typically computed as `rf / max_rf` (when `max_rf > 0`).

## Common Use Cases

### Use Case 1: Phylogenomic Pipeline

Complete workflow from gene tree to ortholog identification:

```python
from ete3 import PhyloTree, NCBITaxa

# 1. Load gene tree with alignment
tree = PhyloTree("gene_tree.nw", alignment="alignment.fasta")

# 2. Configure species naming
tree.set_species_naming_function(lambda x: x.split("_")[0])

# 3. Detect evolutionary events
tree.get_descendant_evol_events()

# 4. Annotate with taxonomy
ncbi = NCBITaxa()
for leaf in tree:
    #Assumes species_to_taxid is defined elsewhere in the workflow
    if leaf.species in species_to_taxid:
        taxid = species_to_taxid[leaf.species]
        lineage = ncbi.get_lineage(taxid)
        leaf.add_feature("lineage", lineage)

# 5. Extract ortholog groups
ortho_groups = tree.get_speciation_trees()

# 6. Save and visualize
for i, ortho in enumerate(ortho_groups):
    ortho.write(outfile=f"ortho_{i}.nw")
```

### Use Case 2: Tree Preprocessing and Formatting

Batch process trees for analysis (demonstrates command-line usage):

```bash
# Convert format
python scripts/tree_operations.py convert input.nw output.nw --in-format 0 --out-format 1

# Root at midpoint
python scripts/tree_operations.py reroot input.nw rooted.nw --midpoint

# Prune to focal taxa
python scripts/tree_operations.py prune rooted.nw pruned.nw --keep-taxa taxa_list.txt

# Get statistics
python scripts/tree_operations.py stats pruned.nw
```

### Use Case 3: Publication-Quality Figures

Create styled visualizations:

```python
from ete3 import Tree, TreeStyle, NodeStyle, TextFace

tree = Tree("tree.nw")

# Define clade colors
clade_colors = {
    "Mammals": "red",
    "Birds": "blue",
    "Fish": "green"
}

def layout(node):
    # Highlight clades
    if node.is_leaf():
        for clade, color in clade_colors.items():
            if clade in node.name:
                nstyle = NodeStyle()
                nstyle["fgcolor"] = color
                nstyle["size"] = 8
                node.set_style(nstyle)
    else:
        # Add support values
        if node.support > 0.95:
            support = TextFace(f"{node.support:.2f}", fsize=8)
            node.add_face(support, column=0, position="branch-top")

ts = TreeStyle()
ts.layout_fn = layout
ts.show_scale = True

# Render for publication
tree.render("figure.pdf", w=200, units="mm", tree_style=ts)
tree.render("figure.svg", tree_style=ts)  # Editable vector
```

### Use Case 4: Automated Tree Analysis

Process multiple trees systematically:

```python
from ete3 import Tree
import os

input_dir = "trees"
output_dir = "processed"

for filename in os.listdir(input_dir):
    if filename.endswith(".nw"):
        tree = Tree(os.path.join(input_dir, filename))

        # Standardize: midpoint root, resolve polytomies
        midpoint = tree.get_midpoint_outgroup()
        tree.set_outgroup(midpoint)
        tree.resolve_polytomy(recursive=True)

        # Filter low support branches
        for node in tree.traverse():
            if hasattr(node, 'support') and node.support < 0.5:
                if not node.is_leaf() and not node.is_root():
                    node.delete()

        # Save processed tree
        output_file = os.path.join(output_dir, f"processed_{filename}")
        tree.write(outfile=output_file)
```

### Use Case 5: Clustering Analysis

Analyze hierarchical clustering results and visualize with a heatmap:

```python
from ete3 import ClusterTree

# Load tree with data matrix
matrix = """#Names\tSample1\tSample2\tSample3
Gene1\t1.5\t2.3\t0.8
Gene2\t0.9\t1.1\t1.8
Gene3\t2.1\t2.5\t0.5"""

tree = ClusterTree("((Gene1,Gene2),Gene3);", text_array=matrix)

# Evaluate cluster quality
for node in tree.traverse():
    if not node.is_leaf():
        silhouette = node.get_silhouette()
        dunn = node.get_dunn()

        print(f"Cluster: {node.name}")
        print(f"  Silhouette: {silhouette:.3f}")
        print(f"  Dunn index: {dunn:.3f}")

# Visualize with heatmap
tree.show("heatmap")
```

### Use Case 6: Tree Comparison

Compare two trees and calculate the Robinson-Foulds distance:

```python
from ete3 import Tree

tree1 = Tree("tree1.nw")
tree2 = Tree("tree2.nw")

# Calculate RF distance
rf, max_rf, common_leaves, parts_t1, parts_t2 = tree1.robinson_foulds(tree2)

print(f"RF distance: {rf}/{max_rf}")
print(f"Normalized RF: {rf/max_rf:.3f}")
print(f"Common leaves: {len(common_leaves)}")

# Find unique partitions
unique_t1 = parts_t1 - parts_t2
unique_t2 = parts_t2 - parts_t1

print(f"Unique to tree1: {len(unique_t1)}")
print(f"Unique to tree2: {len(unique_t2)}")
```

## Troubleshooting

**Import errors:**

```bash
# If "ModuleNotFoundError: No module named 'ete3'"
uv pip install ete3

# For GUI and rendering issues
uv pip install ete3[gui]
```

**Rendering issues:**

If `tree.render()` or `tree.show()` fails with Qt-related errors, install system dependencies:

```bash
# macOS
brew install qt@5

# Ubuntu/Debian
sudo apt-get install python3-pyqt5 python3-pyqt5.qtsvg
```

**NCBI Taxonomy database:**

If database download fails or becomes corrupted:

```python
from ete3 import NCBITaxa
ncbi = NCBITaxa()
ncbi.update_taxonomy_database()  # Redownload database
```

**Memory issues with large trees:**

For very large trees (>10,000 leaves), use iterators instead of list comprehensions:

```python
# Memory-efficient iteration
for leaf in tree.iter_leaves():
    process(leaf)

# Instead of
for leaf in tree.get_leaves():  # Loads all into memory
    process(leaf)
```

## Best Practices

1. **Preserve branch lengths**: Use `preserve_branch_length=True` when pruning for phylogenetic analysis.
2. **Cache content**: Use `get_cached_content()` for repeated access to node contents on large trees.
3. **Use iterators**: Employ `iter_*` methods for memory-efficient processing of large trees.
4. **Choose appropriate traversal**: Postorder for bottom-up analysis, preorder for top-down.
5. **Validate monophyly**: Always check returned clade type (monophyletic/paraphyletic/polyphyletic).
6. **Vector formats for publication**: Use PDF or SVG for publication figures (scalable, editable).
7. **Interactive testing**: Use `tree.show()` to test visualizations before rendering to file.
8. **PhyloTree for phylogenetics**: Use PhyloTree class for gene trees and evolutionary analysis.
9. **Copy method selection**: "newick" for speed, "cpickle" for full fidelity, "deepcopy" for complex objects.
10. **NCBI query caching**: Store NCBI taxonomy query results to avoid repeated database access.