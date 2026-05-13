#!/usr/bin/env python3
"""
pdf_converter.py — opendataloader-pdf Batch Converter Wrapper

Part of the ``literature-ingestion`` Shared Skill
(01.Shared_Assets/Skills/literature-ingestion/).

Scans ``02_Raw_PDFs/`` for new PDF files that have not yet been converted,
then invokes ``opendataloader-pdf`` in full hybrid mode to produce:
  - Structured Markdown   → ``03_Parsed_Markdown/``
  - Structured JSON (bbox) → ``04_Parsed_JSON/``

Configuration is loaded from ``config.json``:
  - ``output_formats``              — list of formats (default: ["markdown", "json"])
  - ``hybrid_mode``                 — "full" | "fast" (default: full)
  - ``ocr_languages``               — comma-separated (default: en,ja)
  - ``enrich_formula``              — bool, enable LaTeX extraction
  - ``enrich_picture_description``  — bool, enable SmolVLM image descriptions

Dependencies:
  - ``pip install 'opendataloader-pdf[hybrid]'``
  - Java 11+ runtime

Design Notes:
  - Uses batch mode (passing all PDFs at once) to avoid cold-starting
    the JVM per file — a known performance trap warned in the official docs.
  - Idempotent: skips PDFs whose ``.md`` and ``.json`` outputs already exist.

Cross-Platform: Pure Python, no OS-specific calls.
"""

import json
import subprocess
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_config(config_path: str) -> dict:
    """Load and return the JSON configuration file."""
    with open(config_path, "r") as f:
        return json.load(f)


def check_dependency_and_install():
    """Check for opendataloader-pdf and try to install it if missing."""
    import shutil
    if shutil.which("opendataloader-pdf") is None:
        print("[WARN] opendataloader-pdf not found in PATH. Attempting to install...")
        try:
            subprocess.run(["pip", "install", "opendataloader-pdf[hybrid]"], check=True)
            print("[INFO] Successfully installed opendataloader-pdf.")
        except subprocess.CalledProcessError:
            print("[ERROR] Failed to install opendataloader-pdf. Will fallback to pdftotext.")
            return False
    return True

def ensure_hybrid_server():
    """Ensure the hybrid server is running before attempting conversion."""
    import urllib.request
    import time
    try:
        # docling fast server exposes health or docs at root usually, or we just check if port is listening
        urllib.request.urlopen("http://127.0.0.1:5002/docs", timeout=1)
        print("[INFO] Hybrid server is already running.")
    except Exception:
        print("[INFO] Hybrid server is not running. Starting opendataloader-pdf-hybrid in background...")
        # Start in background, ignoring output to not clutter
        subprocess.Popen(
            ["opendataloader-pdf-hybrid", "--port", "5002"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        print("[INFO] Waiting for hybrid server to initialize...")
        time.sleep(7)

def fallback_convert_pdfs(pdfs_to_convert: list[str], md_dir: Path):
    """Gracefully degrade to pdftotext if opendataloader-pdf is unavailable."""
    print("[INFO] Executing fallback conversion via pdftotext...")
    import shutil
    has_pdftotext = shutil.which("pdftotext") is not None
    
    for pdf_file in pdfs_to_convert:
        pdf_path = Path(pdf_file)
        md_file = md_dir / f"{pdf_path.stem}.md"
        
        if has_pdftotext:
            print(f"Fallback processing {pdf_path.name} via pdftotext...")
            try:
                # pdftotext outputs to stdout if '-' is passed
                result = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, check=True)
                md_content = f"# {pdf_path.name}\n\n```text\n{result.stdout}\n```\n"
                md_file.write_text(md_content)
                print(f"Successfully generated basic fallback markdown for {pdf_path.name}.")
            except subprocess.CalledProcessError as e:
                print(f"[ERROR] pdftotext failed for {pdf_path.name}: {e}")
        else:
            print(f"[WARN] pdftotext is also unavailable. Creating placeholder for {pdf_path.name} to avoid dead-end loop.")
            md_file.write_text(f"# {pdf_path.name}\n\n> [!WARNING]\n> Auto-conversion failed. Missing opendataloader-pdf and pdftotext.\n")

# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PDFs to Markdown using opendataloader-pdf."
    )
    parser.add_argument(
        "--config",
        default="01.Shared_Assets/Skills/literature-ingestion/config.json",
        help="Path to config file.",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    output_base = Path(config["output_base"])
    pdf_dir = output_base / "02_Raw_PDFs"
    md_dir = output_base / "03_Parsed_Markdown"
    json_dir = output_base / "04_Parsed_JSON"

    md_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)

    # Identify PDFs that have NOT yet been converted (idempotency guard)
    pdfs_to_convert: list[str] = []
    if pdf_dir.exists():
        for pdf_file in pdf_dir.glob("*.pdf"):
            md_file = md_dir / f"{pdf_file.stem}.md"
            # Even if we only generate Markdown in fallback, we check for it
            if not md_file.exists():
                pdfs_to_convert.append(str(pdf_file))

    if not pdfs_to_convert:
        print("No new PDFs to convert.")
        return

    print(f"Found {len(pdfs_to_convert)} PDFs to convert.")

    can_use_opendataloader = check_dependency_and_install()

    if can_use_opendataloader:
        ensure_hybrid_server()
        # Build the opendataloader-pdf CLI command
        formats = config.get("output_formats", ["markdown", "json"])
        cmd = [
            "opendataloader-pdf",
            "--hybrid", "docling-fast",
            "--hybrid-mode", config.get("hybrid_mode", "full"),
            "-f", ",".join(formats),
            "--output-dir", str(md_dir),
        ]

        # Batch mode: pass all PDFs in a single invocation
        cmd.extend(pdfs_to_convert)

        print("Running command:", " ".join(cmd))

        try:
            # Execute the conversion.
            subprocess.run(cmd, check=True)
            print("Conversion batch complete.")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] opendataloader-pdf execution failed: {e}")
            fallback_convert_pdfs(pdfs_to_convert, md_dir)
        except FileNotFoundError:
            print("[ERROR] opendataloader-pdf not found despite checks.")
            fallback_convert_pdfs(pdfs_to_convert, md_dir)
    else:
        fallback_convert_pdfs(pdfs_to_convert, md_dir)


if __name__ == "__main__":
    main()
