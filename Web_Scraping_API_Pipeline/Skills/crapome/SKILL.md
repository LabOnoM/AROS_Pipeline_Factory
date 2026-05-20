---
name: crapome
description: Query the CRAPome (Contaminant Repository for Affinity Purification) via its REST API to flag non-specific background proteins in AP-MS / membrane-enrichment proteomic datasets. Supports single-protein and batch frequency lookups, organism-specific filtering, and SAINT-score-based de-prioritization of contaminants.
license: MIT
metadata:
    skill-author: Scraped from reprint-apms.org + Antigravity AROS
    source_url: http://reprint-apms.org/?q=api
    last_scraped: 2026-04-20
---

# CRAPome — Contaminant Filter for AP-MS Proteomics

## What is CRAPome?

CRAPome (Contaminant Repository for Affinity Purification) is a curated database containing **negative control AP-MS experiments** from hundreds of laboratories. It allows researchers to determine how frequently a protein appears as a non-specific background contaminant (a "frequent flier") across thousands of AP-MS experiments — before claiming it is a genuine interactor.

- **Website**: http://www.crapome.org (mirrors: http://reprint-apms.org)
- **Organisms supported**: `human`, `yeast`, `ecoli`
- **Experiment types**: `singleStep`, `tandem`, `bioId`
- **Versions**: `1.0`, `1.1`, `2.0` (default = latest)

> [!IMPORTANT]
> CRAPome's SSL certificate has expired (as of April 2026). Use `verify=False` in `requests.get()` calls and suppress `InsecureRequestWarning` with `urllib3.disable_warnings()`.

---

## API Endpoints (REST — GET/POST)

All endpoints return **JSON** by default.

### 1. Protein Detail — How often does one gene appear as a contaminant?

```
GET http://reprint-apms.org/?q=ws/proteindetail/{gene_symbol}/{organism}/{experiment_type}/{version}
```

**Parameters:**
| Param | Values | Note |
|:---|:---|:---|
| `gene_symbol` | e.g. `TP53`, `EGFR`, `ACTN4` | Use gene symbols, NOT UniProt accessions |
| `organism` | `human`, `yeast`, `ecoli` | No mouse — use ortholog mapping |
| `experiment_type` | `singleStep`, `tandem`, `bioId` | `singleStep` is most common |
| `version` | `1.0`, `1.1`, `2.0` | Omit for current |

**Example:**
```
http://reprint-apms.org/?q=ws/proteindetail/EGFR/human/singleStep
```

**Output fields (JSON):**
- `gene`: gene symbol queried
- `freq`: frequency = number of experiments the protein was observed in
- `total_exp`: total negative control experiments in this dataset version
- `freq_pct`: `freq / total_exp × 100` — the key metric (higher = more likely to be a contaminant)

---

### 2. Protein + Experiment Detail — Cross-reference a protein with a specific experiment

```
GET http://reprint-apms.org/?q=ws/proteinexpdetail/{gene_symbol}/{experiment_name}/{organism}/{experiment_type}
```

Less useful for batch analysis — primarily for manual validation.

---

### 3. Experiment Detail — Metadata about a specific negative control experiment

```
GET http://reprint-apms.org/?q=ws/expdetail/{experiment_name}/{organism}/{experiment_type}
```

---

## Mouse Proteomics Workaround

> [!WARNING]
> **CRAPome does NOT directly support mouse proteins.** The database is limited to `human`, `yeast`, and `ecoli`.
>
> **Solution**: Convert mouse gene symbols (Title-case, e.g. `Actb`) to their human orthologs (Upper-case, e.g. `ACTB`) using the name directly — most mouse proteins are direct orthologs with identical gene symbols.
>
> **Practical rule**: Upper-case your mouse gene symbols and query them against the `human` organism endpoint. This works for ~85% of conserved housekeeping/structural proteins that are the typical "frequent fliers".

---

## Python Client

```python
# scripts/crapome_client.py
import requests
import urllib3
import pandas as pd
import time

# CRAPome SSL cert is expired — disable verification
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://reprint-apms.org/?q=ws"

class CRAPomeClient:
    """
    Client for the CRAPome REST API.
    Determines how frequently each protein appears as a non-specific 
    contaminant in AP-MS negative control experiments.
    
    Mouse usage: pass organism='human' after uppercasing gene symbols.
    """

    def __init__(self, organism: str = "human", 
                 exp_type: str = "singleStep",
                 version: str = "2.0",
                 rate_limit: float = 0.5):
        self.organism = organism
        self.exp_type = exp_type
        self.version = version
        self.rate_limit = rate_limit  # seconds between calls

    def get_protein_frequency(self, gene_symbol: str) -> dict:
        """Query frequency of a single gene symbol in CRAPome negatives."""
        gene = gene_symbol.upper()
        url = f"{BASE_URL}/proteindetail/{gene}/{self.organism}/{self.exp_type}/{self.version}"
        try:
            r = requests.get(url, verify=False, timeout=10)
            r.raise_for_status()
            data = r.json()
            # Normalize output
            freq = int(data.get("freq", 0))
            total = int(data.get("total_exp", 1))
            return {
                "gene": gene,
                "freq": freq,
                "total_exp": total,
                "freq_pct": round(freq / total * 100, 2),
                "is_contaminant": (freq / total) > 0.05  # >5% = likely contaminant
            }
        except Exception as e:
            return {"gene": gene, "freq": None, "total_exp": None,
                    "freq_pct": None, "is_contaminant": None, "error": str(e)}

    def batch_query(self, gene_list: list, verbose: bool = True) -> pd.DataFrame:
        """
        Query CRAPome frequency for a list of gene symbols.
        Returns a DataFrame sorted by freq_pct (highest contaminants first).
        
        For mouse proteins: automatically uppercases all gene symbols before query.
        """
        results = []
        for i, gene in enumerate(gene_list):
            result = self.get_protein_frequency(gene)
            results.append(result)
            if verbose and (i + 1) % 25 == 0:
                print(f"  Queried {i+1}/{len(gene_list)} proteins...")
            time.sleep(self.rate_limit)
        
        df = pd.DataFrame(results)
        df = df.sort_values("freq_pct", ascending=False, na_position="last")
        return df.reset_index(drop=True)

    def flag_contaminants(self, gene_list: list, 
                          threshold_pct: float = 5.0) -> dict:
        """
        Run batch query and split proteins into:
          - contaminants: freq_pct >= threshold_pct
          - clean: freq_pct < threshold_pct
          - unknown: API returned no data
          
        Returns dict with keys: 'contaminants', 'clean', 'unknown', 'summary_df'
        """
        df = self.batch_query(gene_list)
        contaminants = df[df["freq_pct"] >= threshold_pct]["gene"].tolist()
        clean = df[(df["freq_pct"] < threshold_pct) & (df["freq_pct"].notna())]["gene"].tolist()
        unknown = df[df["freq_pct"].isna()]["gene"].tolist()
        
        print(f"\n=== CRAPome Filter Results (threshold: {threshold_pct}% frequency) ===")
        print(f"  Total queried  : {len(gene_list)}")
        print(f"  Contaminants   : {len(contaminants)} ({len(contaminants)/len(gene_list)*100:.1f}%)")
        print(f"  Clean          : {len(clean)} ({len(clean)/len(gene_list)*100:.1f}%)")
        print(f"  Unknown/No data: {len(unknown)}")
        
        return {
            "contaminants": contaminants,
            "clean": clean,
            "unknown": unknown,
            "summary_df": df
        }
```

---

## Typical Contaminants in Membrane Proteomics

These proteins always appear as high-frequency CRAPome hits and should be treated with caution unless validated by orthogonal methods:

| Gene | Common Name | Why it appears |
|:---|:---|:---|
| `ACTN4` | Alpha-actinin-4 | Sticky cytoskeletal protein |
| `HSP90AA1` | Hsp90-alpha | Abundant chaperone, binds anything |
| `HSPA8` | Hsc70 | Constitutive chaperone |
| `VCP` | p97/VCP | AAA-ATPase, abundant |
| `TUBB` | Beta-tubulin | Cytoskeletal |
| `GAPDH` | GAPDH | Extremely abundant glycolytic enzyme |
| `RPL* / RPS*` | Ribosomal proteins | Co-pellet with membranes |
| `KRTX` | Keratins | Lab contaminants (skin, dust) |
| `ACTB` | Beta-actin | Abundant, sticky |
| `LDHA/B` | Lactate dehydrogenase | Abundant metabolic enzyme |

---

## Recommended Workflow for This Project

```python
from scripts.crapome_client import CRAPomeClient
import pandas as pd

# Load your protein lists
lysate = pd.read_csv("01.Results/ESI-IT-MS/Lysate_Combined/02.Data_Tables/gene_abundances.csv")
pellet = pd.read_csv("01.Results/ESI-IT-MS/Pellet_Combined/02.Data_Tables/gene_abundances.csv")

# Initialize client (mouse → use human orthologs by uppercasing)
client = CRAPomeClient(organism="human", exp_type="singleStep")

# Step 1: Flag contaminants in Lysate
lysate_genes = lysate["Gene_Symbol"].tolist()
lysate_result = client.flag_contaminants(lysate_genes, threshold_pct=5.0)
lysate_result["summary_df"].to_csv("lysate_crapome_flags.csv", index=False)

# Step 2: Keep only clean proteins for downstream PPI analysis
clean_lysate = [g for g in lysate_genes if g.upper() in lysate_result["clean"]]
```

---

## Threshold Guidance

| Frequency % | Interpretation | Action |
|:---|:---|:---|
| > 50% | High-confidence common contaminant | Remove from PPI analysis |
| 10–50% | Frequent background | Flag; require orthogonal evidence |
| 5–10% | Occasional background | Include with caution |
| < 5% | Likely genuine | Include in PPI analysis |

---

## Citation

> Mellacheruvu D, et al. **The CRAPome: a contaminant repository for affinity purification–mass spectrometry data.** *Nat Methods* 10, 730–736 (2013). doi: 10.1038/nmeth.2557
