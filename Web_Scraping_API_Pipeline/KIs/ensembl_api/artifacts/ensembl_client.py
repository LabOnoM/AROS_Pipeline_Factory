# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

#!/usr/bin/env python3
"""
Ensembl API Client — Reusable utility for querying the Ensembl REST API.

Usage:
    from ensembl_client import EnsemblClient
    client = EnsemblClient()
    
    # Check latest release
    print(client.current_release())
    
    # Get assembly info
    info = client.assembly_info("mus_musculus")
    
    # Lookup a gene
    gene = client.lookup("ENSG00000157764")
    
    # Map symbol → Ensembl ID
    hits = client.symbol_lookup("mus_musculus", "Bglap")
    
    # Get cross-references
    xrefs = client.get_xrefs("ENSG00000157764", external_db="Uniprot/SWISSPROT")
    
    # Retrieve sequence
    seq = client.get_sequence("ENST00000288602", seq_type="cdna")
    
    # Batch lookup
    results = client.batch_lookup(["ENSG00000157764", "ENSG00000141510"])
    
    # Check if reference needs updating
    client.check_reference_currency("refdata-gex-GRCh38-2020-A")

Author: Auto-generated for the Ensembl API KI
"""

import time
import re
import requests
from typing import Optional, Union


class EnsemblClient:
    """Client for the Ensembl REST API with rate-limit handling."""

    # Mirrors, in priority order
    MIRRORS = [
        "https://rest.ensembl.org",
        "https://rest.ensembl.org",  # Retry same
    ]

    def __init__(self, server: str = "https://rest.ensembl.org", max_retries: int = 3):
        self.server = server
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _get(self, endpoint: str, content_type: str = "application/json") -> requests.Response:
        """GET with exponential backoff on 429/503."""
        url = f"{self.server}{endpoint}"
        for attempt in range(self.max_retries):
            r = self.session.get(url, headers={"Content-Type": content_type})
            if r.status_code == 429:
                retry_after = float(r.headers.get("Retry-After", 2 ** attempt))
                print(f"  Rate limited — sleeping {retry_after}s (attempt {attempt+1})")
                time.sleep(retry_after)
                continue
            if r.status_code == 503:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            return r
        r.raise_for_status()
        return r

    def _post(self, endpoint: str, json_data: dict) -> requests.Response:
        """POST with exponential backoff."""
        url = f"{self.server}{endpoint}"
        for attempt in range(self.max_retries):
            r = self.session.post(
                url,
                json=json_data,
                headers={"Content-Type": "application/json", "Accept": "application/json"}
            )
            if r.status_code in (429, 503):
                retry_after = float(r.headers.get("Retry-After", 2 ** attempt))
                time.sleep(retry_after)
                continue
            r.raise_for_status()
            return r
        r.raise_for_status()
        return r

    # ── Information ───────────────────────────────────────────────

    def current_release(self) -> list:
        """Get the current Ensembl release number(s)."""
        r = self._get("/info/data?")
        return r.json()["releases"]

    def api_version(self) -> str:
        """Get the REST API software version."""
        r = self._get("/info/rest?")
        return r.json()["release"]

    def list_species(self, division: str = "EnsemblVertebrates") -> list:
        """List all species available in Ensembl."""
        r = self._get(f"/info/species?division={division}")
        return r.json()["species"]

    def assembly_info(self, species: str = "homo_sapiens") -> dict:
        """
        Get assembly information for a species.
        
        Returns: dict with assembly_name, assembly_accession, karyotype, etc.
        """
        r = self._get(f"/info/assembly/{species}?")
        info = r.json()
        return {
            "assembly_name": info["assembly_name"],
            "assembly_accession": info.get("assembly_accession"),
            "coord_system_version": info.get("default_coord_system_version"),
            "top_level_regions": len(info.get("top_level_region", [])),
            "karyotype": info.get("karyotype", []),
        }

    # ── Lookup ────────────────────────────────────────────────────

    def lookup(self, ensembl_id: str, expand: bool = False) -> dict:
        """
        Look up gene/transcript/protein by Ensembl stable ID.
        
        Parameters
        ----------
        ensembl_id : str
            e.g., 'ENSG00000157764', 'ENSMUSG00000030787'
        expand : bool
            If True, include child objects (transcripts for genes, etc.)
        """
        ext = f"/lookup/id/{ensembl_id}?"
        if expand:
            ext += "expand=1"
        r = self._get(ext)
        return r.json()

    def batch_lookup(self, ensembl_ids: list) -> dict:
        """
        Look up multiple Ensembl IDs in one request (max 1000).
        
        Returns: dict mapping ID → metadata
        """
        # Chunk into batches of 1000
        results = {}
        for i in range(0, len(ensembl_ids), 1000):
            chunk = ensembl_ids[i:i+1000]
            r = self._post("/lookup/id", {"ids": chunk})
            results.update(r.json())
        return results

    def symbol_lookup(self, species: str, symbol: str,
                      external_db: Optional[str] = None) -> list:
        """
        Look up Ensembl objects linked to a gene symbol.
        
        Parameters
        ----------
        species : str
            e.g., 'homo_sapiens', 'mus_musculus'
        symbol : str
            Gene symbol, e.g., 'BRCA2', 'Bglap'
        external_db : str, optional
            Filter by DB, e.g., 'HGNC', 'MGI'
        """
        ext = f"/xrefs/symbol/{species}/{symbol}?"
        if external_db:
            ext += f"external_db={external_db}"
        r = self._get(ext)
        return r.json()

    # ── Cross-References ──────────────────────────────────────────

    def get_xrefs(self, ensembl_id: str,
                  external_db: Optional[str] = None) -> list:
        """
        Get external database cross-references for an Ensembl ID.
        
        Parameters
        ----------
        ensembl_id : str
            Ensembl stable ID
        external_db : str, optional
            Filter, e.g., 'Uniprot/SWISSPROT', 'HGNC', 'EntrezGene', 'MGI'
        """
        ext = f"/xrefs/id/{ensembl_id}?"
        if external_db:
            ext += f"external_db={external_db}"
        r = self._get(ext)
        return r.json()

    # ── Sequence Retrieval ────────────────────────────────────────

    def get_sequence(self, ensembl_id: str, seq_type: str = "genomic",
                     fmt: str = "fasta") -> Union[str, dict]:
        """
        Retrieve sequence by Ensembl stable ID.
        
        Parameters
        ----------
        ensembl_id : str
            ENSG, ENST, ENSP, or ENSE ID
        seq_type : str
            'genomic', 'cdna', 'cds', 'protein'
        fmt : str
            'fasta' or 'json'
        """
        content_type = "text/x-fasta" if fmt == "fasta" else "application/json"
        ext = f"/sequence/id/{ensembl_id}?type={seq_type}"
        r = self._get(ext, content_type=content_type)
        return r.text if fmt == "fasta" else r.json()

    def get_region_sequence(self, species: str, region: str,
                            fmt: str = "fasta") -> Union[str, dict]:
        """
        Retrieve sequence for a genomic region.
        
        Parameters
        ----------
        species : str
            e.g., 'homo_sapiens'
        region : str
            e.g., '7:140424943-140624564'
        """
        content_type = "text/x-fasta" if fmt == "fasta" else "application/json"
        ext = f"/sequence/region/{species}/{region}?"
        r = self._get(ext, content_type=content_type)
        return r.text if fmt == "fasta" else r.json()

    # ── Mapping ───────────────────────────────────────────────────

    def assembly_map(self, species: str, asm_from: str, region: str,
                     asm_to: str) -> dict:
        """
        Map coordinates between genome assemblies (liftover).
        
        Parameters
        ----------
        species : str
            e.g., 'human'
        asm_from : str
            Source assembly, e.g., 'GRCh37'
        region : str
            e.g., '17:7565097-7590856'
        asm_to : str
            Target assembly, e.g., 'GRCh38'
        """
        ext = f"/map/{species}/{asm_from}/{region}/{asm_to}?"
        r = self._get(ext)
        return r.json()

    # ── Comparative Genomics ──────────────────────────────────────

    def get_homologs(self, species: str, ensembl_id: str,
                     target_species: Optional[str] = None) -> dict:
        """
        Get orthologs/paralogs for a gene.
        
        Parameters
        ----------
        target_species : str, optional
            e.g., 'mus_musculus' to get only mouse orthologs
        """
        ext = f"/homology/id/{species}/{ensembl_id}?"
        if target_species:
            ext += f"target_species={target_species}"
        r = self._get(ext)
        return r.json()

    # ── Overlap ───────────────────────────────────────────────────

    def get_features_in_region(self, species: str, region: str,
                                feature: str = "gene") -> list:
        """
        Get features overlapping a genomic region.
        
        Parameters
        ----------
        feature : str
            'gene', 'transcript', 'variation', 'regulatory', etc.
        """
        ext = f"/overlap/region/{species}/{region}?feature={feature}"
        r = self._get(ext)
        return r.json()

    # ── Variation ─────────────────────────────────────────────────

    def vep_hgvs(self, species: str, hgvs: str) -> list:
        """
        Variant Effect Predictor for an HGVS notation variant.
        """
        ext = f"/vep/{species}/hgvs/{hgvs}?"
        r = self._get(ext)
        return r.json()

    # ── Reference Currency Check ──────────────────────────────────

    def check_reference_currency(self, ref_name: str) -> dict:
        """
        Check if a 10x Genomics pre-built reference is still current
        relative to the latest Ensembl release.
        
        Parameters
        ----------
        ref_name : str
            e.g., 'refdata-gex-GRCh38-2020-A' or 'refdata-gex-GRCm39-2024-A'
        
        Returns
        -------
        dict
            {'needs_update': bool, 'ref_year': int, 'current_release': int,
             'recommendation': str}
        """
        import datetime
        
        match = re.search(r'(\d{4})-([A-Z])', ref_name)
        ref_year = int(match.group(1)) if match else 2000
        
        releases = self.current_release()
        current_release = releases[0] if releases else None
        current_year = datetime.datetime.now().year
        
        needs_update = (current_year - ref_year) >= 2
        
        result = {
            "needs_update": needs_update,
            "ref_year": ref_year,
            "current_year": current_year,
            "current_ensembl_release": current_release,
            "recommendation": ""
        }
        
        if needs_update:
            result["recommendation"] = (
                f"Reference '{ref_name}' is from {ref_year} "
                f"({current_year - ref_year} years old). "
                f"Build a new reference from Ensembl release {current_release} "
                f"using cellranger mkref with the latest FASTA + GTF files."
            )
        else:
            result["recommendation"] = (
                f"Reference '{ref_name}' from {ref_year} is reasonably current "
                f"(Ensembl release {current_release})."
            )
        
        return result

    def get_ftp_urls(self, species: str = "mus_musculus",
                     release: str = "current") -> dict:
        """
        Generate FTP download URLs for a species' reference files.
        
        Returns
        -------
        dict
            Keys: 'fasta', 'gtf', 'gff3', 'cdna', 'ncrna'
        """
        base = f"https://ftp.ensembl.org/pub/{release}"
        species_lower = species.lower()
        
        return {
            "genome_fasta": f"{base}/fasta/{species_lower}/dna/",
            "cdna_fasta": f"{base}/fasta/{species_lower}/cdna/",
            "ncrna_fasta": f"{base}/fasta/{species_lower}/ncrna/",
            "protein_fasta": f"{base}/fasta/{species_lower}/pep/",
            "gtf": f"{base}/gtf/{species_lower}/",
            "gff3": f"{base}/gff3/{species_lower}/",
        }


if __name__ == "__main__":
    client = EnsemblClient()
    
    print("=== Ensembl API Client ===")
    print(f"API version: {client.api_version()}")
    print(f"Current release: {client.current_release()}")
    
    print("\n--- Mouse Assembly ---")
    info = client.assembly_info("mus_musculus")
    for k, v in info.items():
        if k != "karyotype":
            print(f"  {k}: {v}")
    
    print("\n--- Reference Currency ---")
    check = client.check_reference_currency("refdata-gex-GRCh38-2020-A")
    print(f"  Needs update: {check['needs_update']}")
    print(f"  {check['recommendation']}")
    
    print("\n--- FTP URLs (mouse) ---")
    urls = client.get_ftp_urls("mus_musculus")
    for k, v in urls.items():
        print(f"  {k}: {v}")
