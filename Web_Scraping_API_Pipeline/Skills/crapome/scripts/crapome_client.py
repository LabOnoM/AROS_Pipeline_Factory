"""
CRAPome REST API client for flagging non-specific contaminants in AP-MS datasets.
Mouse proteins are automatically uppercased and queried against human orthologs.

Usage:
    from scripts.crapome_client import CRAPomeClient
    client = CRAPomeClient()
    result = client.flag_contaminants(["Actb", "Gapdh", "Cd44", "Itga5"])
"""

import requests
import urllib3
import pandas as pd
import time

# CRAPome SSL cert is expired — disable verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://reprint-apms.org/?q=ws"

# Known high-frequency contaminants (fast pre-filter before API query)
KNOWN_CONTAMINANTS = {
    "HSPA8", "HSP90AA1", "HSP90AB1", "HSPA5", "HSPA1A", "HSPA1B",
    "GAPDH", "ACTB", "ACTG1", "TUBB", "TUBA1A", "TUBA1B",
    "VCP", "ACTN1", "ACTN4", "FLNA", "FLNB",
    "LDHA", "LDHB", "PGK1", "ENO1", "PKM",
    "EEF1A1", "EEF2", "EIF4A1",
    # Ribosomal proteins — high-freq membrane co-pellet contaminants
    "RPL4", "RPL5", "RPL6", "RPL7", "RPL8", "RPL10", "RPL11",
    "RPL12", "RPL13", "RPL14", "RPL15", "RPL18", "RPL19", "RPL23",
    "RPL24", "RPL26", "RPL27", "RPL28", "RPL29", "RPL30",
    "RPS3", "RPS4X", "RPS6", "RPS8", "RPS9", "RPS10", "RPS11",
    "RPS12", "RPS14", "RPS15", "RPS16", "RPS18", "RPS19", "RPS20",
    # Keratins (lab contamination from skin)
    "KRT1", "KRT2", "KRT5", "KRT6A", "KRT9", "KRT10", "KRT14",
    "KRT16", "KRT6B",
}


class CRAPomeClient:
    """
    Client for the CRAPome REST API.

    Determines how frequently each protein appears as a non-specific
    contaminant across thousands of AP-MS negative control experiments.

    Mouse usage: automatically uppercases gene symbols and queries
    against the 'human' organism (valid for conserved orthologs).

    Args:
        organism: 'human', 'yeast', or 'ecoli' (default: 'human')
        exp_type: 'singleStep', 'tandem', or 'bioId' (default: 'singleStep')
        version: API version '1.0', '1.1', '2.0' (default: '2.0')
        rate_limit: seconds to wait between API calls (default: 0.5)
        threshold_pct: % frequency above which a protein is a contaminant
    """

    def __init__(
        self,
        organism: str = "human",
        exp_type: str = "singleStep",
        version: str = "2.0",
        rate_limit: float = 0.1,
        threshold_pct: float = 5.0,
    ):
        self.organism = organism
        self.exp_type = exp_type
        self.version = version
        self.rate_limit = rate_limit
        self.threshold_pct = threshold_pct

    def get_protein_frequency(self, gene_symbol: str) -> dict:
        """
        Query frequency of a single gene in CRAPome negative controls.

        Returns:
            dict with keys: gene, freq, total_exp, freq_pct, is_contaminant
        """
        gene = gene_symbol.upper()

        # Fast pre-filter from known contaminant set
        if gene in KNOWN_CONTAMINANTS:
            return {
                "gene": gene,
                "freq": None,
                "total_exp": None,
                "freq_pct": 100.0,  # treated as certain contaminant
                "is_contaminant": True,
                "source": "known_contaminant_list",
            }

        url = (
            f"{BASE_URL}/proteindetail/{gene}/"
            f"{self.organism}/{self.exp_type}/{self.version}"
        )
        try:
            r = requests.get(url, verify=False, timeout=10)
            r.raise_for_status()
            data = r.json()
            freq = int(data.get("freq", 0))
            total = int(data.get("total_exp", 1))
            freq_pct = round(freq / max(total, 1) * 100, 2)
            return {
                "gene": gene,
                "freq": freq,
                "total_exp": total,
                "freq_pct": freq_pct,
                "is_contaminant": freq_pct >= self.threshold_pct,
                "source": "api",
            }
        except Exception as e:
            # API down or protein not found — do not remove from analysis
            return {
                "gene": gene,
                "freq": None,
                "total_exp": None,
                "freq_pct": None,
                "is_contaminant": False,  # conservative: don't discard if unknown
                "source": "error",
                "error": str(e),
            }

    def batch_query(self, gene_list: list, verbose: bool = True) -> pd.DataFrame:
        """
        Batch-query CRAPome for a list of gene symbols.

        Args:
            gene_list: List of gene symbols (mouse Title-case or human UPPER-case)
            verbose: Print progress every 25 proteins

        Returns:
            DataFrame sorted by freq_pct descending (worst contaminants first)
        """
        results = []
        consecutive_errors = 0
        api_dead = False
        
        for i, gene in enumerate(gene_list):
            if api_dead and gene.upper() not in KNOWN_CONTAMINANTS:
                # Fast fail if API is unresponsive
                result = {
                    "gene": gene.upper(), "freq": None, "total_exp": None,
                    "freq_pct": None, "is_contaminant": False, 
                    "source": "api_dead_fallback", "error": "API aborted"
                }
            else:
                result = self.get_protein_frequency(gene)
                if result.get('source') == 'error':
                    consecutive_errors += 1
                    if consecutive_errors >= 3:
                        print("  [WARNING] CRAPome API unresponsive. Circuit breaker triggered. Using local rules only.")
                        api_dead = True
                else:
                    consecutive_errors = 0
                    
            results.append(result)
            if verbose and (i + 1) % 25 == 0:
                print(f"  [{i+1}/{len(gene_list)}] queried CRAPome...")
            if not api_dead and result.get('source') != 'known_contaminant_list':
                time.sleep(self.rate_limit)

        df = pd.DataFrame(results)
        df = df.sort_values("freq_pct", ascending=False, na_position="last")
        return df.reset_index(drop=True)

    def flag_contaminants(
        self, gene_list: list, threshold_pct: float = None, verbose: bool = True
    ) -> dict:
        """
        Query CRAPome and classify proteins into:
          - contaminants  : freq_pct >= threshold_pct
          - clean         : freq_pct < threshold_pct
          - unknown       : API returned no data (conservatively kept)

        Args:
            gene_list: List of gene symbols
            threshold_pct: Override instance threshold (default: self.threshold_pct)
            verbose: Print summary stats

        Returns:
            dict with keys: 'contaminants', 'clean', 'unknown', 'summary_df'
        """
        thr = threshold_pct if threshold_pct is not None else self.threshold_pct
        df = self.batch_query(gene_list, verbose=verbose)

        contaminants = df[df["freq_pct"] >= thr]["gene"].tolist()
        clean = df[(df["freq_pct"] < thr) & (df["freq_pct"].notna())]["gene"].tolist()
        unknown = df[df["freq_pct"].isna()]["gene"].tolist()

        if verbose:
            print(f"\n{'='*60}")
            print(f"CRAPome Filter Summary (threshold: {thr}%)")
            print(f"{'='*60}")
            print(f"  Total proteins  : {len(gene_list)}")
            print(f"  Contaminants    : {len(contaminants)} ({len(contaminants)/len(gene_list)*100:.1f}%)")
            print(f"  Clean           : {len(clean)} ({len(clean)/len(gene_list)*100:.1f}%)")
            print(f"  Unknown/No data : {len(unknown)} (conservatively kept)")
            if contaminants:
                print(f"\nTop contaminants:")
                top = df[df["gene"].isin(contaminants)].head(10)
                for _, row in top.iterrows():
                    print(f"  {row['gene']:15s}  {row['freq_pct']:.1f}%")

        return {
            "contaminants": contaminants,
            "clean": clean + unknown,  # keep unknowns in clean list
            "unknown": unknown,
            "summary_df": df,
        }
