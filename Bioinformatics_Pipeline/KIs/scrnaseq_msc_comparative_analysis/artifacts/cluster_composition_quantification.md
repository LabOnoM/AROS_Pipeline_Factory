# Cell Type Composition & Niche Collapse Quantification (Case Study: BM-cDNA vs. Cell-day3)

## Quantification of the Composition Shift

A key biological insight from the comparative analysis of fresh versus cultured cells is the **near-total replacement of functional niches** with generalized fibroblastic phenotypes. 

Below are the percentage distributions derived from the 16-cluster mapping (Analytic Pearson Residuals + Harmony):

| Annotated Lineage | BM-cDNA (%) | Cultured (Cell-day3) (%) |
|-------------------|-------------|-------------------------|
| **BM CAR/MSC**     | 25.7%       | 0.05%                   |
| **Endothelial**    | 21.5%       | 5.2%                    |
| **Osteoprog.**     | 16.0%       | 5.3%                    |
| **Mature Osteoblast**| 14.1%      | 0.2%                    |
| **Fibroblasts**    | 2.0%        | 67.9%*                  |
| **Myofibroblasts** | 0.07%       | 15.9%                   |
| **Erythroid**      | 7.4%        | 0.03%                   |
| **BM Stromal**     | 5.6%        | 0.0%                    |
| **Myeloid/Mac**    | 1.1%        | 5.1%                    |
| **Smooth Muscle**  | 3.1%        | 0.15%                   |
| **Other (Glial, etc.)**| <2%      | <1%                     |

*\* Sum of generic and stress-associated fibroblasts.*

## Biological Interpretations

1. **Niche Identity Loss (Niche Collapse)**:
   - Functional BM stromal populations like *Cxcl12+* **CAR** cells and *Pecam1+/Emcn+* **Endothelial** cells represent ~47% of the fresh BM sample but essentially vanish (effectively <0.1% for CAR) after 72 hours of 2D culturing. 
   - **Mature Osteoblasts** (*Bglap+*) also do not persist, dropping from 14% to 0.2%.

2. **Homogenization & Activation**:
   - The expanded culture is overwhelmingly dominated by a single **activated fibroblastic phenotype** (~68%). 
   - A significant fraction (15.9%) trans-differentiates into **Acta2+ Myofibroblasts**.

3. **Transcriptomic Convergence**:
   - While the BM is highly heterogeneous (diverse clusters for individual lineages), the cultured population is transcriptomically restricted, with most clusters representing slightly varied stress or proliferative states of the same base fibroblast identity.

## Analytical Pattern for Composition Visualization

Use a stacked bar graph to quantify exactly how much of each lineage survives expansion. In this specialized comparison, where conditions are so distinct, normalized percentages (as shown above) are more informative than raw cell counts.

```python
# Proportions calculation pattern
df = adata.obs.groupby(['condition', 'cell_type'], observed=True).size().reset_index(name='count')
df['percentage'] = df.groupby('condition')['count'].transform(lambda x: x / x.sum() * 100)
df_pivoted = df.pivot(index='condition', columns='cell_type', values='percentage').fillna(0)

# Plotting
df_pivoted.plot(kind='bar', stacked=True, ...)
```
