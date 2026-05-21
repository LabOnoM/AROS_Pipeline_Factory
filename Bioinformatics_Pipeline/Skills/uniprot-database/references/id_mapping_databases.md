# UniProt ID Mapping Databases Reference

This document lists the exact database identifiers to use with the `map` command
of `uniprot_tools.py` (i.e. the `--from_db` and `--to_db` arguments).
It provides a complete list of databases supported by the UniProt ID Mapping service. Use these database names when calling the ID mapping API.

## Usage Examples

### Retrieving Database List Programmatically

```python
import requests
response = requests.get("https://rest.uniprot.org/configure/idmapping/fields")
databases = response.json()
```

### Using uniprot_tools.py

```bash
uv run uniprot_tools.py map "P12345,Q67890" --from_db UniProtKB_AC-ID --to_db PDB
```

**Source:** `https://rest.uniprot.org/configure/idmapping/fields`

---

## UniProt Databases

*   **CRC64**: `CRC64`
*   **Proteome ID**: `Proteome_ID` (`--from_db` only)
*   **UniParc**: `UniParc` - UniProt Archive
*   **UniProtKB**: `UniProtKB` - UniProt Knowledgebase (`--to_db` only)
*   **UniProtKB AC/ID**: `UniProtKB_AC-ID` - UniProt accession and ID (`--from_db` only)
*   **UniProtKB/Swiss-Prot**: `UniProtKB-Swiss-Prot` - Reviewed (Swiss-Prot) (`--to_db` only)
*   **UniProtKB-TrEMBL**: `UniProtKB-TrEMBL` - Unreviewed (TrEMBL)
*   **UniRef100**: `UniRef100` - UniRef 100% identity clusters
*   **UniRef50**: `UniRef50` - UniRef 50% identity clusters
*   **UniRef90**: `UniRef90` - UniRef 90% identity clusters

## Sequence Databases

### Nucleotide Sequence
*   **CCDS**: `CCDS` - Consensus CDS
*   **EMBL/GenBank/DDBJ**: `EMBL-GenBank-DDBJ`
*   **EMBL/GenBank/DDBJ CDS**: `EMBL-GenBank-DDBJ_CDS`
*   **GI number**: `GI_number`
*   **RefSeq Nucleotide**: `RefSeq_Nucleotide` - RefSeq nucleotide sequences

### Protein Sequence
*   **PIR**: `PIR` - Protein Information Resource
*   **RefSeq Protein**: `RefSeq_Protein` - RefSeq protein sequences

## Gene Databases

*   **GeneID**: `GeneID` - Entrez Gene
*   **Gene Name**: `Gene_Name`
*   **Gene ORF Name**: `Gene_ORFName`
*   **Gene Ordered Locus Name**: `Gene_OrderedLocusName`
*   **Gene Synonym**: `Gene_Synonym`

## Genome Databases

### General
*   **Ensembl**: `Ensembl`
*   **Ensembl Genomes**: `Ensembl_Genomes`
*   **Ensembl Genomes Protein**: `Ensembl_Genomes_Protein`
*   **Ensembl Genomes Transcript**: `Ensembl_Genomes_Transcript`
*   **Ensembl Protein**: `Ensembl_Protein`
*   **Ensembl Transcript**: `Ensembl_Transcript`

### Organism-Specific
*   **KEGG**: `KEGG` - KEGG Genes
*   **PATRIC**: `PATRIC`
*   **UCSC**: `UCSC` - UCSC Genome Browser
*   **VectorBase**: `VectorBase`
*   **WBParaSite**: `WBParaSite` - WormBase ParaSite
*   **WBParaSite Transcript/Protein**: `WBParaSite_Transcript-Protein`

## Structure Databases

*   **AlphaFoldDB**: `AlphaFoldDB` - AlphaFold Database
*   **BMRB**: `BMRB` - Biological Magnetic Resonance Data Bank
*   **PDB**: `PDB` - Protein Data Bank
*   **PDBsum**: `PDBsum` - PDB summary
*   **SASBDB**: `SASBDB` - Small Angle Scattering Biological Data Bank
*   **SMR**: `SMR` - SWISS-MODEL Repository

## Protein Family and Domain Databases

*   **InterPro**: `InterPro`
*   **Pfam**: `Pfam` - Pfam protein families
*   **PROSITE**: `PROSITE`
*   **SMART**: `SMART` - SMART domains
*   **CDD**: `CDD` - Conserved Domain Database
*   **HAMAP**: `HAMAP`
*   **PANTHER**: `PANTHER`
*   **PRINTS**: `PRINTS`
*   **ProDom**: `ProDom`
*   **SFLD**: `SFLD` - Structure-Function Linkage Database
*   **SUPFAM**: `SUPFAM` - SUPERFAMILY
*   **TIGRFAMs**: `TIGRFAMs`

## Organism-Specific Databases

### Model Organisms
*   **MGI**: `MGI` - Mouse Genome Informatics
*   **RGD**: `RGD` - Rat Genome Database
*   **FlyBase**: `FlyBase` - FlyBase (Drosophila)
*   **WormBase**: `WormBase` - WormBase (C. elegans)
*   **Xenbase**: `Xenbase` - Xenbase (Xenopus)
*   **ZFIN**: `ZFIN` - Zebrafish Information Network
*   **dictyBase**: `dictyBase` - dictyBase (Dictyostelium)
*   **EcoGene**: `EcoGene` - EcoGene (E. coli)
*   **SGD**: `SGD` - Saccharomyces Genome Database (yeast)
*   **PomBase**: `PomBase` - PomBase (S. pombe)
*   **TAIR**: `TAIR` - The Arabidopsis Information Resource

### Human-Specific
*   **HGNC**: `HGNC` - HUGO Gene Nomenclature Committee
*   **CCDS**: `CCDS` - Consensus Coding Sequence Database

## Pathway Databases

*   **Reactome**: `Reactome`
*   **BioCyc**: `BioCyc`
*   **PlantReactome**: `PlantReactome`
*   **SIGNOR**: `SIGNOR`
*   **SignaLink**: `SignaLink`

## Enzyme and Metabolism

*   **EC**: `EC` - Enzyme Commission