#!/usr/bin/env python3
"""
fetch_and_convert.py — Literature Ingestion Orchestrator

Part of the ``literature-ingestion`` Shared Skill
(01.Shared_Assets/Skills/literature-ingestion/).

Reads a newline-delimited file of DOIs, attempts to download each paper
using the 6-tier retrieval cascade (see ``retrieval_tiers.py``), validates
the resulting PDF, and writes per-paper metadata JSON.

Key design properties:
  - **Idempotent**: re-running the script skips DOIs whose PDFs already
    exist in ``02_Raw_PDFs/``.
  - **Bounded retries**: the rate-limit handler from the legacy prototype
    used unguarded recursion — this version relies on the bounded cascade
    in ``retrieval_tiers.download_pdf_tiered()``.
  - **Failure logging**: DOIs that fail all tiers are appended to
    ``failed_downloads.json`` for human follow-up.

Usage:
    python3 fetch_and_convert.py \\
        --input 00.RawData/Literature/01_Target_DOIs.txt \\
        [--config 01.Shared_Assets/Skills/literature-ingestion/config.json]

Cross-Platform: Pure Python, no OS-specific calls.
"""

import json
import argparse
from pathlib import Path

from retrieval_tiers import download_pdf_tiered


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_config(config_path: str) -> dict:
    """Load and return the JSON configuration file."""
    with open(config_path, "r") as f:
        return json.load(f)


def sanitize_filename(doi: str) -> str:
    """Convert a DOI into a safe filesystem-friendly filename."""
    return doi.replace("/", "_").replace("\\", "_")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch literature PDFs using a tiered cascade."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input TXT file with one DOI per line.",
    )
    # Calculate the default config path relative to this script
    script_dir = Path(__file__).resolve().parent
    default_config = script_dir.parent / "config.json"
    
    parser.add_argument(
        "--config",
        default=str(default_config),
        help="Path to config file.",
    )
    parser.add_argument(
        "--base-dir",
        default=None,
        help="Override the output_base directory (e.g. for project-specific locations).",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    output_base = Path(args.base_dir) if args.base_dir else Path(config["output_base"])
    pdf_dir = output_base / "02_Raw_PDFs"
    meta_dir = output_base / "05_Metadata"
    failed_log = output_base / "failed_downloads.json"

    pdf_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)

    # Read input DOIs
    with open(args.input, "r") as f:
        dois = [line.strip() for line in f if line.strip()]

    # Load existing failure manifest (append-only)
    failed_dois: list[dict] = []
    if failed_log.exists():
        with open(failed_log, "r") as f:
            try:
                failed_dois = json.load(f)
            except json.JSONDecodeError:
                failed_dois = []

    # Process each DOI
    for doi in dois:
        pdf_path = pdf_dir / f"{sanitize_filename(doi)}.pdf"
        meta_path = meta_dir / f"{sanitize_filename(doi)}.json"

        # Idempotency guard — skip already-downloaded PDFs
        if pdf_path.exists():
            print(f"Skipping {doi}: PDF already exists.")
            continue

        print(f"Fetching {doi}...")
        success, content, source = download_pdf_tiered(doi, config)

        if success and content:
            with open(pdf_path, "wb") as f:
                f.write(content)

            # Persist per-paper metadata
            meta = {"doi": doi, "source_tier": source, "status": "success"}
            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=2)
            print(f"  -> Success ({source})")
        else:
            print(f"  -> Failed all tiers.")
            failed_entry = {"doi": doi, "reason": "All tiers failed"}
            if failed_entry not in failed_dois:
                failed_dois.append(failed_entry)

    # Write updated failure manifest
    with open(failed_log, "w") as f:
        json.dump(failed_dois, f, indent=2)

    print("Fetch process completed.")


if __name__ == "__main__":
    main()
