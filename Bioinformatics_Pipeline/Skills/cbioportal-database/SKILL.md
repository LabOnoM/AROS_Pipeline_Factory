---
name: cbioportal-database
description: Query cBioPortal for cancer genomics data including somatic mutations, copy number alterations, gene expression, and survival data across hundreds of cancer studies. Essential for cancer target validation, oncogene/tumor suppressor analysis, and patient-level genomic profiling.
license: LGPL-3.0
metadata:
    skill-author: Kuan-lin Huang
---

# cBioPortal Database

## Overview

cBioPortal for Cancer Genomics (https://www.cbioportal.org/) is an open-access resource for exploring, visualizing, and analyzing multidimensional cancer genomics data. It hosts data from The Cancer Genome Atlas (TCGA), AACR Project GENIE, MSK-IMPACT, and hundreds of other cancer studies — covering mutations, copy number alterations (CNA), structural variants, mRNA/protein expression, methylation, and clinical data for thousands of cancer samples.

**Key resources:**
- cBioPortal website: https://www.cbioportal.org/
- REST API: https://www.cbioportal.org/api/
- API docs (Swagger): https://www.cbioportal.org/api/swagger-ui/index.html
- Python client: `bravado` or `requests`
- GitHub: https://github.com/cBioPortal/cbioportal

## When to Use This Skill

Use cBioPortal when:

- **Mutation landscape**: What fraction of a cancer type has mutations in a specific gene?
- **Oncogene/TSG validation**: Is a gene frequently mutated, amplified, or deleted in cancer?
- **Co-mutation patterns**: Are mutations in gene A and gene B mutually exclusive or co-occurring?
- **Survival analysis**: Do mutations in a gene associate with better or worse patient outcomes?
- **Alteration profiles**: What types of alterations (missense, truncating, amplification, deletion) affect a gene?
- **Pan-cancer analysis**: Compare alteration frequencies across cancer types
- **Clinical associations**: Link genomic alterations to clinical variables (stage, grade, treatment response)
- **TCGA/GENIE exploration**: Systematic access to TCGA and clinical sequencing datasets

## Core Capabilities

### 1. cBioPortal REST API

Base URL: `https://www.cbioportal.org/api`

The API is RESTful, returns JSON, and requires no API key for public data.

```python
import requests
import pandas as pd # Added for mutation data processing example

BASE_URL = "https://www.cbioportal.org/api"
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}

def cbioportal_get(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def cbioportal_post(endpoint, body):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, json=body, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_all_studies():
    """List all available cancer studies."""
    studies = cbioportal_get("studies", {"pageSize": 500})
    print(f"Total studies: {len(studies)}")
    return studies

# Each study has:
# studyId: unique identifier (e.g., "brca_tcga")
# name: human-readable name
# description: dataset description
# cancerTypeId: cancer type abbreviation
# referenceGenome: GRCh37 or GRCh38
# pmid: associated publication

# Example usage:
# studies = get_all_studies()
# tcga_studies = [s for s in studies if "tcga" in s["studyId"]]
# print(f"Common TCGA study IDs: {[s['studyId'] for s in tcga_studies[:10]]}")

# Each study has multiple molecular profiles (mutation, CNA, expression, etc.):
def get_molecular_profiles(study_id):
    """Get molecular profiles for a given study."""
    profiles = cbioportal_get(f"studies/{study_id}/molecular-profiles")
    print(f"\nMolecular profiles for {study_id}:")
    for p in profiles:
        print(f"  {p['molecularProfileId']}: {p['name']} ({p['molecularAlterationType']})")
    return profiles

# Alteration types: SOMATIC_MUTATION, COPY_NUMBER_ALTERATION, MRNA_EXPRESSION, PROTEIN_EXPRESSION, METHYLATION, FUSION, STRUCTURAL_VARIANT

def get_mutations(molecular_profile_id, entrez_gene_ids, sample_list_id=None):
    """Get mutation data for specified genes and molecular profile."""
    body = {
        "molecularProfileId": molecular_profile_id,
        "entrezGeneIds": entrez_gene_ids,
        "sampleListId": sample_list_id or molecular_profile_id.replace("_mutations", "_all")
    }
    mutations = cbioportal_post("mutations/fetch", body)
    # Example processing with pandas:
    # if mutations:
    #     df = pd.DataFrame(mutations)
    #     print(f"\nMutation types:\n{df['mutationType'].value_counts()}")
    return mutations

# Each mutation record contains:
# mutationType, proteinChange, genomicLocation, consequence, variantType, etc.

def get_cna(molecular_profile_id, entrez_gene_ids):
    """Get discrete CNA data (GISTIC: -2, -1, 0, 1, 2)."""
    body = {
        "molecularProfileId": molecular_profile_id,
        "entrezGeneIds": entrez_gene_ids,
        "sampleListId": molecular_profile_id.replace("_gistic", "_all").replace("_cna", "_all")
    }
    cna_data = cbioportal_post("copy-number-alterations/fetch", body)
    return cna_data

# GISTIC values:
# -2: Homozygous Deletion
# -1: Heterozygous Deletion
# 0: Diploid
# 1: Low-level Gain
# 2: High-level Amplification
```