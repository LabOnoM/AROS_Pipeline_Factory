#!/usr/bin/env python3
# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""
AROS Skill — Markdown Report Generator (build_report.py)

Converts markdown documents into polished HTML and DOCX formats.
Integrates with the AROS Cloud Federation proxy for cost-optimal and monitored LLM routing.

Key Functions/Classes:
- resolve_api_key: Resolves credentials from AROS_CLOUD_KEY or fallbacks.
- encode_images_in_markdown: Replaces local image paths with base64 data URIs for embedding.
- main: Initializes the google.generativeai SDK with proxy client_options.

Integration Points:
- Swarm Agents: Generates final deliverables in multiple formats.
- AROS Proxy: Intercepts requests via AROS_CLOUD_URL when configured.

Part of: md-html-docx-generator (Skill)
"""
import os
import re
import sys
import base64
import argparse
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

try:
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig
except ImportError:
    print("Error: google-generativeai is not installed. Please install it with 'pip install google-generativeai'.")
    sys.exit(1)


@dataclass
class Section:
    index: int
    title: str
    markdown_body: str
    html_content: str = ""
    anchor: str = ""

def resolve_api_key(args_key: Optional[str] = None) -> str:
    """Portable 4-tier API key resolution chain."""
    if args_key:
        return args_key
    
    key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    try:
        from dotenv import load_dotenv
    except ImportError:
        def load_dotenv(*args, **kwargs): pass
        
    for start_dir in [Path.cwd(), Path(__file__).resolve().parent]:
        d = start_dir
        for _ in range(6):
            env_path = d / ".env"
            if env_path.exists():
                load_dotenv(dotenv_path=env_path, override=False)
                key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GEMINI_API_KEY")
                if key:
                    return key
            if d.parent == d:
                break
            d = d.parent
            
    aros_env = Path.home() / ".gemini" / ".env"
    if aros_env.exists():
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=aros_env, override=False)
        key = os.environ.get("GOOGLE_AI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if key:
            return key
            
    raise EnvironmentError(
        "No API key found. Set GOOGLE_AI_API_KEY via:\n"
        "  1. CLI: --api-key YOUR_KEY\n"
        "  2. Environment: export GOOGLE_AI_API_KEY=YOUR_KEY\n"
        "  3. File: Add to ~/.gemini/.env"
    )

def encode_images_in_markdown(md_content: str, base_dir: Path) -> str:
    """Replaces local image paths in markdown with base64 data URIs."""
    img_pattern = re.compile(r'!\\[([^\\]*)\\]\\(([^)]+)\\)')
    
    def replace_image(match):
        alt_text = match.group(1)
        img_path_str = match.group(2).strip()
        
        if img_path_str.startswith(("http://", "https://", "data:")):
            return match.group(0)
            
        img_path = base_dir / img_path_str
        if not img_path.is_absolute():
            img_path = (base_dir / img_path_str).resolve()
            
        if img_path.exists() and img_path.is_file():
            ext = img_path.suffix.lower().lstrip(".")
            mime_type = "image/png"
            if ext in ["jpg", "jpeg"]: mime_type = "image/jpeg"
            elif ext == "svg": mime_type = "image/svg+xml"
            elif ext == "gif": mime_type = "image/gif"
            
            try:
                with open(img_pa