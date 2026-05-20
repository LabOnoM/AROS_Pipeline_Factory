# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

#!/usr/bin/env python3
"""
retrieval_tiers.py — Tiered PDF Retrieval Cascade

Part of the ``literature-ingestion`` Shared Skill
(01.Shared_Assets/Skills/literature-ingestion/).

Implements a 6-tier fallback cascade for downloading academic PDFs:
  T1  Semantic Scholar  — Open Access API (fastest, cleanest)
  T2  Unpaywall         — Broadest OA coverage
  T3  PubMed Central    — Biomedical focus (BioC/PMC)
  T4  Publisher Proxy   — DOI redirect + optional institutional proxy
  T5  LibGen / Anna's   — Shadow library DOM scraping (fragile)
  T6  Sci-Hub           — Last resort, highest risk of bot-blocks

Each tier function returns a tuple:
    (success: bool, content: bytes | None, source_label: str)

Design Notes:
  - Every tier is independently try/except-wrapped — a crash in one
    tier never prevents the next tier from executing.
  - PDF validation uses magic bytes (``%PDF``) and a minimum 5 KB
    size check to reject HTML error pages masquerading as PDFs.
  - Rate limiting uses the ``rate_limit_delay`` config key (seconds).
  - No infinite recursion: the old prototype used unguarded recursion
    on 429 status — this version uses bounded retries only.

Cross-Platform: Pure Python, no OS-specific calls.
"""

import time
import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def validate_pdf(content: bytes) -> bool:
    """Validate that byte content is a genuine PDF.

    Checks the ``%PDF`` magic number at the start of the file and
    rejects anything smaller than 5 KB (likely an HTML error page).
    """
    if len(content) < 5000:
        return False
    return content.startswith(b"%PDF-")


# ---------------------------------------------------------------------------
# Tier 1: Semantic Scholar Open Access API
# ---------------------------------------------------------------------------
def fetch_semantic_scholar(
    doi: str, config: dict
) -> tuple[bool, bytes | None, str]:
    """Attempt to download the OA PDF via Semantic Scholar."""
    url = (
        f"https://api.semanticscholar.org/graph/v1/paper/"
        f"DOI:{doi}?fields=openAccessPdf"
    )
    headers = {}
    if config.get("semantic_scholar_api_key"):
        headers["x-api-key"] = config["semantic_scholar_api_key"]

    try:
        resp = requests.get(url, headers=headers, timeout=config["timeout_seconds"])
        resp.raise_for_status()
        data = resp.json()
        oa_info = data.get("openAccessPdf")
        if oa_info and oa_info.get("url"):
            pdf_resp = requests.get(
                oa_info["url"], timeout=config["timeout_seconds"]
            )
            if pdf_resp.status_code == 200 and validate_pdf(pdf_resp.content):
                return True, pdf_resp.content, "Semantic Scholar"
    except Exception:
        pass
    return False, None, ""


# ---------------------------------------------------------------------------
# Tier 2: Unpaywall
# ---------------------------------------------------------------------------
def fetch_unpaywall(doi: str, config: dict) -> tuple[bool, bytes | None, str]:
    """Attempt to download the OA PDF via Unpaywall."""
    email = config.get("unpaywall_email", "researcher@example.com")
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    try:
        resp = requests.get(url, timeout=config["timeout_seconds"])
        resp.raise_for_status()
        data = resp.json()
        best_oa = data.get("best_oa_location")
        if best_oa and best_oa.get("url_for_pdf"):
            pdf_resp = requests.get(
                best_oa["url_for_pdf"], timeout=config["timeout_seconds"]
            )
            if pdf_resp.status_code == 200 and validate_pdf(pdf_resp.content):
                return True, pdf_resp.content, "Unpaywall"
    except Exception:
        pass
    return False, None, ""


# ---------------------------------------------------------------------------
# Tier 3: PubMed Central
# ---------------------------------------------------------------------------
def fetch_pmc(doi: str, config: dict) -> tuple[bool, bytes | None, str]:
    """Attempt to retrieve via PubMed Central (DOI → PMCID conversion).

    For a full implementation this would use the NCBI ID Converter API
    to map DOI → PMCID, then fetch the PDF from PMC.  Currently a
    placeholder that gracefully returns False.
    """
    return False, None, ""


# ---------------------------------------------------------------------------
# Tier 4: Publisher Landing Page (with optional institutional proxy)
# ---------------------------------------------------------------------------
def fetch_publisher_proxy(
    doi: str, config: dict
) -> tuple[bool, bytes | None, str]:
    """Resolve DOI and attempt direct PDF download.

    If ``config["proxy_url"]`` is set (e.g. an EZProxy/OpenAthens URL),
    it is prepended to the publisher URL to enable institutional access.
    """
    proxy_url = config.get("proxy_url", "")
    target_url = f"https://doi.org/{doi}"
    if proxy_url:
        target_url = f"{proxy_url}{target_url}"

    try:
        resp = requests.get(target_url, timeout=config["timeout_seconds"])
        if resp.status_code == 200 and validate_pdf(resp.content):
            return True, resp.content, "Publisher Proxy"
    except Exception:
        pass
    return False, None, ""


# ---------------------------------------------------------------------------
# Tier 5: LibGen / Anna's Archive (DOM scraping)
# ---------------------------------------------------------------------------
def fetch_libgen(doi: str, config: dict) -> tuple[bool, bytes | None, str]:
    """Attempt to download the PDF from LibGen mirrors."""
    mirrors = config.get("libgen_mirrors", [])
    for mirror in mirrors:
        try:
            search_url = f"{mirror}/scimag/?q={doi}"
            resp = requests.get(search_url, timeout=config["timeout_seconds"])
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                links = soup.find_all("a")
                for link in links:
                    href = link.get("href")
                    if href and ("get.php" in href or href.endswith(".pdf")):
                        if href.startswith("/"):
                            href = f"{mirror}{href}"
                        pdf_resp = requests.get(
                            href, timeout=config["timeout_seconds"]
                        )
                        if pdf_resp.status_code == 200 and validate_pdf(
                            pdf_resp.content
                        ):
                            return True, pdf_resp.content, "LibGen"
        except Exception:
            continue
    return False, None, ""


# ---------------------------------------------------------------------------
# Tier 6: Sci-Hub (DOM scraping — last resort)
# ---------------------------------------------------------------------------
def fetch_scihub(doi: str, config: dict) -> tuple[bool, bytes | None, str]:
    """Attempt to download the PDF from Sci-Hub mirrors."""
    mirrors = config.get("sci_hub_mirrors", [])
    for mirror in mirrors:
        try:
            url = f"{mirror}/{doi}"
            resp = requests.get(url, timeout=config["timeout_seconds"])
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                pdf_iframe = soup.find("iframe", {"id": "pdf"})
                if pdf_iframe and pdf_iframe.get("src"):
                    pdf_url = pdf_iframe["src"]
                    if pdf_url.startswith("//"):
                        pdf_url = f"https:{pdf_url}"
                    elif pdf_url.startswith("/"):
                        pdf_url = f"{mirror}{pdf_url}"
                    pdf_resp = requests.get(
                        pdf_url, timeout=config["timeout_seconds"]
                    )
                    if pdf_resp.status_code == 200 and validate_pdf(
                        pdf_resp.content
                    ):
                        return True, pdf_resp.content, "Sci-Hub"
        except Exception:
            continue
    return False, None, ""


# ---------------------------------------------------------------------------
# Public API — cascade entry point
# ---------------------------------------------------------------------------
def download_pdf_tiered(
    doi: str, config: dict
) -> tuple[bool, bytes | None, str]:
    """Iterate through all 6 retrieval tiers and return the first success.

    Returns:
        (success, pdf_bytes, source_label)
    """
    tiers = [
        fetch_semantic_scholar,
        fetch_unpaywall,
        fetch_pmc,
        fetch_publisher_proxy,
        fetch_libgen,
        fetch_scihub,
    ]

    for tier_func in tiers:
        success, content, source = tier_func(doi, config)
        if success:
            return True, content, source
        time.sleep(config.get("rate_limit_delay", 2))

    return False, None, ""
