# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

#!/usr/bin/env python3
"""
NCBI E-utilities Client — Production-grade Python client with traffic control.

⚠️ CRITICAL: This client enforces NCBI's rate limits automatically.
Never bypass the built-in rate limiting — NCBI WILL block your IP.

Usage:
    from ncbi_client import NCBIClient
    
    client = NCBIClient(
        tool="my_research_app",
        email="researcher@university.edu",
        api_key="OPTIONAL_API_KEY"     # 10 req/s vs 3 req/s
    )
    
    # Search PubMed
    results = client.search_pubmed("spatial transcriptomics Visium HD")
    
    # Fetch abstracts
    records = client.fetch_pubmed_records(results["pmids"])
    
    # Batch search with date segmentation (for >10K results)
    all_pmids = client.search_pubmed_large("cancer", max_results=50000)
    
    # Cross-database links
    gene_ids = client.link("pubmed", "gene", pmid_list)
    
    # PMC ID conversion
    mapping = client.convert_ids(["PMC3531190", "23193287"])

Author: Auto-generated for the NCBI PubMed API KI
"""

import time
import requests
import xml.etree.ElementTree as ET
from typing import Optional, Union
from datetime import datetime


class NCBIClient:
    """
    Production-grade NCBI E-utilities client with mandatory traffic control.
    
    Features:
    - Automatic rate limiting (3 req/s default, 10 req/s with API key)
    - Exponential backoff on 429/502/503 errors
    - History Server integration for large retrievals
    - Batch splitting for EPost/EFetch/ESummary
    - Date segmentation for breaking the 10K PubMed cap
    """
    
    BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    PMC_ID_CONVERTER = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
    
    def __init__(self, tool: str, email: str, api_key: Optional[str] = None,
                 max_retries: int = 5):
        """
        Initialize the NCBI client.
        
        Parameters
        ----------
        tool : str
            Your application name (no spaces). REQUIRED by NCBI.
        email : str
            Your valid email address. REQUIRED by NCBI.
        api_key : str, optional
            NCBI API key for 10 req/s (vs 3 req/s without).
        max_retries : int
            Maximum retry attempts on server errors.
        """
        if not tool or not email:
            raise ValueError("NCBI requires both 'tool' and 'email' parameters.")
        
        self.tool = tool
        self.email = email
        self.api_key = api_key
        self.max_retries = max_retries
        self.session = requests.Session()
        
        # Rate limiting
        self._min_interval = 0.11 if api_key else 0.34  # seconds between requests
        self._last_request_time = 0.0
    
    def _build_params(self, extra_params: dict = None) -> dict:
        """Build base parameters with required tool/email/api_key."""
        params = {"tool": self.tool, "email": self.email}
        if self.api_key:
            params["api_key"] = self.api_key
        if extra_params:
            params.update(extra_params)
        return params
    
    def _throttle(self):
        """Enforce minimum interval between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request_time = time.time()
    
    def _get(self, endpoint: str, params: dict = None) -> requests.Response:
        """GET with rate limiting and exponential backoff."""
        url = f"{self.BASE}/{endpoint}"
        params = self._build_params(params)
        
        for attempt in range(self.max_retries):
            self._throttle()
            try:
                r = self.session.get(url, params=params, timeout=30)
            except requests.exceptions.ConnectionError:
                wait = min(2 ** attempt, 60)
                print(f"  ⚠️ Connection error — waiting {wait}s (attempt {attempt+1})")
                time.sleep(wait)
                continue
            except requests.exceptions.Timeout:
                wait = min(2 ** attempt, 60)
                print(f"  ⚠️ Timeout — waiting {wait}s (attempt {attempt+1})")
                time.sleep(wait)
                continue
            
            if r.status_code == 200:
                return r
            
            if r.status_code == 429:
                wait = float(r.headers.get("Retry-After", 2 ** attempt))
                print(f"  ⚠️ Rate limited (429) — waiting {wait}s (attempt {attempt+1})")
                time.sleep(wait)
                continue
            
            if r.status_code in (500, 502, 503):
                wait = min(2 ** attempt * 2, 60)
                print(f"  ⚠️ Server error {r.status_code} — waiting {wait}s "
                      f"(attempt {attempt+1})")
                time.sleep(wait)
                continue
            
            r.raise_for_status()
        
        raise Exception(f"NCBI request failed after {self.max_retries} retries: "
                        f"{endpoint}")
    
    def _post(self, endpoint: str, data: dict = None) -> requests.Response:
        """POST with rate limiting and exponential backoff."""
        url = f"{self.BASE}/{endpoint}"
        if data is None:
            data = {}
        data.update({"tool": self.tool, "email": self.email})
        if self.api_key:
            data["api_key"] = self.api_key
        
        for attempt in range(self.max_retries):
            self._throttle()
            try:
                r = self.session.post(url, data=data, timeout=60)
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout):
                wait = min(2 ** attempt, 60)
                time.sleep(wait)
                continue
            
            if r.status_code == 200:
                return r
            if r.status_code in (429, 500, 502, 503):
                wait = min(2 ** attempt * 2, 60)
                time.sleep(wait)
                continue
            
            r.raise_for_status()
        
        raise Exception(f"NCBI POST failed after {self.max_retries} retries")
    
    # ── EInfo ─────────────────────────────────────────────────────
    
    def database_info(self, db: str = None) -> dict:
        """
        Get database statistics or list all databases.
        
        If db is None, returns list of all Entrez database names.
        If db is specified, returns field list and link list for that DB.
        """
        params = {"retmode": "json"}
        if db:
            params["db"] = db
        r = self._get("einfo.fcgi", params)
        return r.json()
    
    # ── ESearch ───────────────────────────────────────────────────
    
    def search(self, db: str, term: str, retmax: int = 20,
               use_history: bool = True, sort: str = None,
               datetype: str = None, mindate: str = None,
               maxdate: str = None, reldate: int = None) -> dict:
        """
        Search an Entrez database.
        
        Parameters
        ----------
        db : str
            Database name (e.g., 'pubmed', 'pmc', 'gene')
        term : str
            Search query (Entrez syntax)
        retmax : int
            Max UIDs to return in response (up to 10,000)
        use_history : bool
            If True, stores results on History Server for batched retrieval
        sort : str, optional
            Sort order (e.g., 'relevance', 'pub_date' for PubMed)
        
        Returns
        -------
        dict with keys:
            count: total matching records
            idlist: list of UIDs (up to retmax)
            webenv: History Server token (if use_history=True)
            query_key: History Server key (if use_history=True)
        """
        params = {
            "db": db,
            "term": term,
            "retmax": retmax,
            "retmode": "json",
        }
        if use_history:
            params["usehistory"] = "y"
        if sort:
            params["sort"] = sort
        if datetype:
            params["datetype"] = datetype
        if mindate:
            params["mindate"] = mindate
        if maxdate:
            params["maxdate"] = maxdate
        if reldate:
            params["reldate"] = reldate
        
        r = self._get("esearch.fcgi", params)
        data = r.json()["esearchresult"]
        
        return {
            "count": int(data.get("count", 0)),
            "idlist": data.get("idlist", []),
            "webenv": data.get("webenv"),
            "query_key": data.get("querykey"),
            "translation_set": data.get("translationset", []),
        }
    
    def search_pubmed(self, query: str, max_results: int = 100,
                      sort: str = "relevance") -> dict:
        """Convenience wrapper for PubMed searches."""
        return self.search("pubmed", query, retmax=min(max_results, 10000),
                          sort=sort)
    
    def search_pubmed_large(self, query: str, max_results: int = 50000,
                            start_year: int = None) -> list:
        """
        Search PubMed for more than 10,000 results using date segmentation.
        
        Breaks the query into year-by-year searches to bypass
        PubMed's 10,000 result cap.
        
        Parameters
        ----------
        query : str
            PubMed search query
        max_results : int
            Target number of PMIDs to collect
        start_year : int, optional
            Start from this year (default: current year)
        
        Returns
        -------
        list of str
            PMIDs
        """
        all_pmids = []
        current_year = start_year or datetime.now().year
        
        for year in range(current_year, current_year - 30, -1):
            if len(all_pmids) >= max_results:
                break
            
            term = f"{query} AND {year}[pdat]"
            result = self.search("pubmed", term, retmax=10000, use_history=False)
            new_pmids = result["idlist"]
            all_pmids.extend(new_pmids)
            
            print(f"  Year {year}: +{len(new_pmids)} PMIDs "
                  f"(total: {len(all_pmids)})")
            
            # If a single year has 10,000 results, we need month-level
            if len(new_pmids) >= 9999:
                print(f"  ⚠️ Year {year} may be capped at 10K — "
                      f"consider month-level segmentation")
        
        return all_pmids[:max_results]
    
    # ── EPost ─────────────────────────────────────────────────────
    
    def post_ids(self, db: str, id_list: list,
                 webenv: str = None) -> dict:
        """
        Upload a list of UIDs to the History Server.
        
        Parameters
        ----------
        db : str
            Database name
        id_list : list
            List of UIDs (PMIDs, Gene IDs, etc.)
        webenv : str, optional
            Existing WebEnv to append to
        
        Returns
        -------
        dict with webenv and query_key
        
        ⚠️ For sequence databases with accession IDs, batch in groups of ≤500.
        """
        # Split into chunks of 5000 for PubMed (500 for accessions)
        chunk_size = 5000
        last_webenv = webenv
        last_qkey = None
        
        for i in range(0, len(id_list), chunk_size):
            chunk = id_list[i:i+chunk_size]
            data = {
                "db": db,
                "id": ",".join(str(x) for x in chunk),
            }
            if last_webenv:
                data["WebEnv"] = last_webenv
            
            r = self._post("epost.fcgi", data)
            root = ET.fromstring(r.text)
            last_webenv = root.findtext("WebEnv")
            last_qkey = root.findtext("QueryKey")
        
        return {"webenv": last_webenv, "query_key": last_qkey}
    
    # ── EFetch ────────────────────────────────────────────────────
    
    def fetch(self, db: str, ids: list = None,
              webenv: str = None, query_key: str = None,
              rettype: str = None, retmode: str = "xml",
              batch_size: int = 500) -> list:
        """
        Fetch full records with automatic batching.
        
        Can use either a direct ID list OR History Server (webenv+query_key).
        
        Parameters
        ----------
        db : str
            Database name
        ids : list, optional
            Direct list of UIDs (will be batched automatically)
        webenv : str, optional
            History Server WebEnv (from search or post_ids)
        query_key : str, optional
            History Server query key
        rettype : str, optional
            Return type (e.g., 'abstract', 'medline', 'fasta', 'gb')
        retmode : str
            Return mode ('xml', 'text', 'json')
        batch_size : int
            Records per request (recommended: 200-500)
        
        Returns
        -------
        list of str
            Raw response texts from each batch
        """
        results = []
        
        if ids and not webenv:
            # Upload IDs to History Server first
            hist = self.post_ids(db, ids)
            webenv = hist["webenv"]
            query_key = hist["query_key"]
            total = len(ids)
        elif webenv and query_key:
            # Need to know total count — do a search
            total = len(ids) if ids else None
            if total is None:
                # Estimate from a quick fetch attempt
                total = 100000  # Will stop when empty
        else:
            raise ValueError("Provide either 'ids' or 'webenv'+'query_key'")
        
        for start in range(0, total, batch_size):
            params = {
                "db": db,
                "WebEnv": webenv,
                "query_key": query_key,
                "retstart": start,
                "retmax": batch_size,
                "retmode": retmode,
            }
            if rettype:
                params["rettype"] = rettype
            
            r = self._get("efetch.fcgi", params)
            
            # Check for empty response (we've gone past the end)
            if not r.text.strip() or len(r.text) < 50:
                break
            
            results.append(r.text)
        
        return results
    
    def fetch_pubmed_xml(self, pmids: list, batch_size: int = 500) -> str:
        """
        Fetch PubMed records as XML.
        
        Returns concatenated XML text.
        """
        batches = self.fetch("pubmed", ids=[str(p) for p in pmids],
                            retmode="xml", batch_size=batch_size)
        return "\n".join(batches)
    
    def fetch_pubmed_abstracts(self, pmids: list, batch_size: int = 200) -> str:
        """Fetch PubMed abstracts as plain text."""
        batches = self.fetch("pubmed", ids=[str(p) for p in pmids],
                            rettype="abstract", retmode="text",
                            batch_size=batch_size)
        return "\n".join(batches)
    
    # ── ESummary ──────────────────────────────────────────────────
    
    def summary(self, db: str, ids: list = None,
                webenv: str = None, query_key: str = None,
                batch_size: int = 500) -> list:
        """
        Get document summaries with automatic batching.
        
        Returns list of parsed JSON summaries.
        """
        all_summaries = []
        
        if ids and not webenv:
            hist = self.post_ids(db, ids)
            webenv = hist["webenv"]
            query_key = hist["query_key"]
            total = len(ids)
        else:
            total = len(ids) if ids else 100000
        
        for start in range(0, total, batch_size):
            params = {
                "db": db,
                "WebEnv": webenv,
                "query_key": query_key,
                "retstart": start,
                "retmax": batch_size,
                "retmode": "json",
                "version": "2.0",
            }
            
            r = self._get("esummary.fcgi", params)
            data = r.json()
            
            result_key = "result"
            if result_key in data:
                uids = data[result_key].get("uids", [])
                if not uids:
                    break
                for uid in uids:
                    all_summaries.append(data[result_key][uid])
            else:
                break
        
        return all_summaries
    
    # ── ELink ─────────────────────────────────────────────────────
    
    def link(self, dbfrom: str, db: str, ids: list,
             linkname: str = None, cmd: str = "neighbor") -> dict:
        """
        Find linked UIDs across databases.
        
        Parameters
        ----------
        dbfrom : str
            Source database
        db : str
            Target database
        ids : list
            Source UIDs
        linkname : str, optional
            Specific link name (e.g., 'gene_protein_refseq')
        cmd : str
            'neighbor', 'neighbor_score', 'neighbor_history', 'acheck'
        
        Returns
        -------
        dict with linked UIDs or History Server tokens
        """
        params = {
            "dbfrom": dbfrom,
            "db": db,
            "id": ",".join(str(i) for i in ids),
            "cmd": cmd,
            "retmode": "json",
        }
        if linkname:
            params["linkname"] = linkname
        
        r = self._get("elink.fcgi", params)
        return r.json()
    
    # ── PMC ID Converter ──────────────────────────────────────────
    
    def convert_ids(self, ids: list, id_type: str = None) -> list:
        """
        Convert between PMID, PMCID, DOI using the PMC ID Converter.
        
        Parameters
        ----------
        ids : list
            Mix of PMIDs, PMCIDs (e.g., 'PMC3531190'), or DOIs
        id_type : str, optional
            Force input type: 'pmid', 'pmcid', 'doi'
        
        Returns
        -------
        list of dict
            Each dict has 'pmid', 'pmcid', 'doi' keys (where available)
        
        ⚠️ Max 200 IDs per request.
        """
        all_records = []
        
        for i in range(0, len(ids), 200):
            chunk = ids[i:i+200]
            params = {
                "ids": ",".join(str(x) for x in chunk),
                "format": "json",
                "tool": self.tool,
                "email": self.email,
            }
            if id_type:
                params["idtype"] = id_type
            
            self._throttle()
            r = self.session.get(self.PMC_ID_CONVERTER, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            all_records.extend(data.get("records", []))
        
        return all_records
    
    # ── ECitMatch ─────────────────────────────────────────────────
    
    def citation_match(self, citations: list) -> dict:
        """
        Match citations to PMIDs.
        
        Parameters
        ----------
        citations : list of dict
            Each dict should have: journal, year, volume, first_page, author
            Optional: key (your local identifier)
        
        Returns
        -------
        dict mapping key → PMID (or None if not found)
        """
        bdata_parts = []
        for i, cit in enumerate(citations):
            key = cit.get("key", f"cit{i}")
            parts = [
                cit.get("journal", "").replace(" ", "+"),
                str(cit.get("year", "")),
                str(cit.get("volume", "")),
                str(cit.get("first_page", "")),
                cit.get("author", "").replace(" ", "+"),
                key,
                ""
            ]
            bdata_parts.append("|".join(parts))
        
        bdata = "%0D".join(bdata_parts)
        
        params = {
            "db": "pubmed",
            "retmode": "xml",
            "bdata": bdata,
        }
        
        r = self._get("ecitmatch.cgi", params)
        
        # Parse results
        results = {}
        for line in r.text.strip().split("\n"):
            parts = line.strip().split("|")
            if len(parts) >= 7:
                key = parts[5]
                pmid = parts[6] if parts[6] and parts[6] != "AMBIGUOUS" else None
                results[key] = pmid
        
        return results
    
    # ── Convenience Methods ───────────────────────────────────────
    
    def parse_pubmed_xml(self, xml_text: str) -> list:
        """
        Parse PubMed XML into a list of article dicts.
        
        Returns
        -------
        list of dict
            Each dict has: pmid, title, abstract, authors, journal,
            pub_date, doi, mesh_terms
        """
        articles = []
        
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError:
            # Try wrapping in a root element
            try:
                root = ET.fromstring(f"<root>{xml_text}</root>")
            except ET.ParseError:
                return articles
        
        for article_el in root.iter("PubmedArticle"):
            art = {}
            
            # PMID
            art["pmid"] = article_el.findtext(".//PMID", "")
            
            # Title
            art["title"] = article_el.findtext(".//ArticleTitle", "")
            
            # Abstract
            abstract_parts = []
            for abs_text in article_el.findall(".//AbstractText"):
                label = abs_text.get("Label", "")
                text = abs_text.text or ""
                # Handle mixed content
                full_text = "".join(abs_text.itertext())
                if label:
                    abstract_parts.append(f"{label}: {full_text}")
                else:
                    abstract_parts.append(full_text)
            art["abstract"] = " ".join(abstract_parts)
            
            # Authors
            authors = []
            for author_el in article_el.findall(".//Author"):
                last = author_el.findtext("LastName", "")
                fore = author_el.findtext("ForeName", "")
                if last:
                    authors.append(f"{last} {fore}".strip())
            art["authors"] = authors
            
            # Journal
            art["journal"] = article_el.findtext(".//Journal/Title", "")
            art["journal_abbrev"] = article_el.findtext(
                ".//Journal/ISOAbbreviation", "")
            
            # Publication date
            year = article_el.findtext(".//PubDate/Year", "")
            month = article_el.findtext(".//PubDate/Month", "")
            day = article_el.findtext(".//PubDate/Day", "")
            art["pub_date"] = f"{year} {month} {day}".strip()
            
            # DOI
            for id_el in article_el.findall(".//ArticleId"):
                if id_el.get("IdType") == "doi":
                    art["doi"] = id_el.text
                    break
            else:
                art["doi"] = ""
            
            # MeSH terms
            mesh_terms = []
            for mesh_el in article_el.findall(".//MeshHeading/DescriptorName"):
                mesh_terms.append(mesh_el.text or "")
            art["mesh_terms"] = mesh_terms
            
            # Keywords
            keywords = []
            for kw_el in article_el.findall(".//Keyword"):
                keywords.append(kw_el.text or "")
            art["keywords"] = keywords
            
            articles.append(art)
        
        return articles


if __name__ == "__main__":
    # Demo: Search PubMed for spatial transcriptomics papers
    client = NCBIClient(
        tool="spatial_tx_pipeline",
        email="researcher@example.com",
        # api_key="YOUR_KEY_HERE"  # Uncomment for 10 req/s
    )
    
    print("=== NCBI E-utilities Client Demo ===")
    print(f"Rate limit: {'10 req/s (API key)' if client.api_key else '3 req/s (no key)'}")
    
    # Search
    print("\n--- PubMed Search ---")
    result = client.search_pubmed("Visium HD spatial transcriptomics", max_results=5)
    print(f"Total results: {result['count']}")
    print(f"First {len(result['idlist'])} PMIDs: {result['idlist']}")
    
    if result["idlist"]:
        # Fetch
        print("\n--- Fetching Abstracts ---")
        xml_text = client.fetch_pubmed_xml(result["idlist"], batch_size=200)
        articles = client.parse_pubmed_xml(xml_text)
        for art in articles[:3]:
            print(f"\n  PMID: {art['pmid']}")
            print(f"  Title: {art['title'][:100]}")
            print(f"  Authors: {', '.join(art['authors'][:3])}")
            print(f"  Journal: {art['journal_abbrev']}")
            print(f"  Date: {art['pub_date']}")
    
    # Database info
    print("\n--- Available Databases ---")
    info = client.database_info()
    db_list = info.get("einforesult", {}).get("dblist", [])
    print(f"Total databases: {len(db_list)}")
    print(f"First 10: {db_list[:10]}")
