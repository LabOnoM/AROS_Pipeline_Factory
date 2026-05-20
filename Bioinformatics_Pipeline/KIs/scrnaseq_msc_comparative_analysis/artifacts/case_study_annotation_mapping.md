# Case Study: BM vs. Cultured MSC Cell Type Annotation (MGI DNBelab C4)

This case study demonstrates a successful labeling of 16 clusters generated from marrow-derived vs. day-3 cultured MSCs (SCTransform + Harmony integration). 

## Cluster Annotation Mapping

| Cluster | Metadata Condition | Assigned Cell Type | Key Marker Genes |
|---------|--------------------|-------------------|-----------------|
| **0**   | BM                 | **Erythroid**      | *Ahsp*, *Car2*, *Hba-a1*, *Blvrb*, *Hbb-bs* |
| **1, 2**| Cultured           | **Fibroblasts**    | *S100a4*, *Ccnd1*, *Lgals3*, *Fabp5*, *S100a10* |
| **3**   | BM                 | **BM CAR/MSC**     | *Cxcl12*, *Serping1*, *Adipoq*, *Igfbp5*, *Apoe* |
| **4**   | BM                 | **Endothelial**    | *Pecam1*, *Emcn*, *Plvap*, *Egfl7*, *Cdh5* |
| **5**   | BM/Cultured        | **Osteoprog.**     | *Csmd1*, *Malat1*, *Gpc6*, *Rbms3*, *Rora* |
| **6**   | BM                 | **BM Stromal**     | *Igfbp6*, *Dcn*, *Gsn*, *Fos*, *Col3a1* |
| **7**   | BM                 | **Smooth Muscle**  | *Notch3*, *Rgs5*, *Ndufa4l2*, *Myh11*, *Crip1* |
| **8**   | Cultured           | **Fibroblasts (Stress)** | *Camk1d*, *Cmss1*, *Camk1* |
| **9**   | BM                 | **Mature Osteoblast** | *Bglap2*, *Bglap*, *Col1a1*, *Cfh*, *Lum* |
| **10, 15**| Cultured/Mixed   | **Myeloid/Mac**    | *S100a9*, *S100a8*, *Lyz2*, *Pglyrp1*, *Ctss* |
| **11, 12**| Cultured         | **Fibroblasts**    | *Spp1*, *S100a6*, *Npc2*, *Cxcl14*, *Serpine1* |
| **13**  | BM/Cultured        | **Schwann Cells**  | *Cadm4*, *Kcna1*, *Plekhb1*, *Plp1*, *Fxyd1* |
| **14**  | Cultured           | **Myofibroblasts** | *Tagln*, *Acta2*, *Myl9*, *Tpm2*, *Pfn1* |

## Biological Interpretation of Annotation Results
1. **Erasure of Niche Identity**: Fresh bone marrow contains a highly diverse population set (*Cxcl12+* CAR cells, *Pecam1+* endothelial, *Hba-a1+* erythroid). 
2. **Homogenization**: Upon three days of culture, the majority of niche diversity is lost. Most clusters (1, 2, 8, 11, 12, 14) represent slightly varied states of a common **activated fibroblastic phenotype**.
3. **Myofibroblast Transformation**: Cluster 14 specifically highlights the ubiquity of **Acta2+** cells in the expanded culture, which are absent or restricted to pericyte-only clusters in marrow settings.
4. **Minority Survival**: Rare populations like schwann cells (Cluster 13) may persist through expansion, though their relative frequency changes.
