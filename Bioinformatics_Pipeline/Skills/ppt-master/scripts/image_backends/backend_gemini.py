# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

#!/usr/bin/env python3
"""
AROS Skill — PPT Master Gemini Backend (backend_gemini.py)

Generates images via the Google GenAI API (Gemini) for presentation decks.
Integrates with the AROS Cloud Federation proxy for cost-optimal and monitored LLM routing.

Configuration keys:
  GEMINI_API_KEY   (required)
  GEMINI_BASE_URL  (optional) Custom API endpoint for proxy services (AROS_CLOUD_URL can also be used)
  GEMINI_MODEL     (optional) Override default model

Dependencies:
  pip install google-genai Pillow

Key Functions/Classes:
- init_client: Constructs a google.genai.Client respecting AROS_CLOUD_URL proxy.
- generate_image: Generates and saves an image from a prompt.

Integration Points:
- ppt-master: Used by image_gen.py as a modular image backend.
- AROS Proxy: Intercepts requests via AROS_CLOUD_URL when configured.

Part of: ppt-master (Skill)
"""

import os
import time
import threading
from google import genai
from google.genai import types
from image_backends.backend_common import (
    MAX_RETRIES,
    is_rate_limit_error,
    normalize_image_size,
    resolve_output_path,
    retry_delay,
    save_image_bytes,
)


# ╔═══════════════════════════════╦═══════════════════════════════════╗
# ║  Constants                                                      ║
# ╚═══════════════════════════════╩═══════════════════════════════════╝

VALID_ASPECT_RATIOS = [
    "1:1", "1:4", "1:8",
    "2:3", "3:2", "3:4", "4:1", "4:3",
    "4:5", "5:4", "8:1", "9:16", "16:9", "21:9"
]

VALID_IMAGE_SIZES = ["512px", "1K", "2K", "4K"]

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"


# ╔═══════════════════════════════════════════════════════════════════╗
# ║  Image Generation                                               ║
# ╚═══════════════════════════════════════════════════════════════════╝

def _generate_image(api_key: str, prompt: str, negative_prompt: str = None,
                    aspect_ratio: str = "1:1", image_size: str = "1K",
                    output_dir: str = None, filename: str = None,
                    model: str = DEFAULT_MODEL, base_url: str = None) -> str:
    """
    Image generation via Gemini API (streaming).

    Returns:
        Path of the saved image file

    Raises:
        RuntimeError: When generation fails
    """
    if base_url:
        client = genai.Client(api_key=api_key, http_options={'base_url': base_url})
    else:
        client = genai.Client(api_key=api_key)

    final_prompt = prompt
    if negative_prompt:
        final_prompt += f"\n\nNegative prompt: {negative_prompt}"

    config_kwargs = {
        "response_modalities": ["IMAGE"],
        "image_config": types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=image_size,
        ),
    }
    if "flash" in model.lower():
        config_kwargs["thinking_config"] =