# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
AROS Skill — Nano Banana Image Generation (generate_image.py)

Generates or edits images with Google's Nano Banana 2 model (`gemini-3.1-flash-image-preview`).
Integrates with the AROS Cloud Federation proxy for cost-optimal and monitored LLM routing.

Key Functions/Classes:
- get_proxy_aware_client: Constructs a google.genai.Client respecting AROS_CLOUD_URL.
- create_image: Handles prompt-to-image generation.
- edit_image: Handles image-to-image modification.

Usage:
    uv run generate_image.py --prompt "your image description" \
        --filename "output.png" [--resolution 512|1K|2K|4K] [--api-key KEY]

    uv run generate_image.py --prompt "editing instruction" \
        --filename "edited.png" --input-image "source.png"

Integration Points:
- Swarm Agents: Directly invokes this script for scientific or artistic visualization.
- AROS Proxy: Intercepts requests via AROS_CLOUD_URL when configured.

Part of: nano-banana (Skill)
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

MODEL_NAME = "gemini-3.1-flash-image-preview"
DEFAULT_RESOLUTION = "1K"
RESOLUTION_CHOICES = ("512", "1K", "2K", "4K")

def get_proxy_aware_client(provided_key: str | None = None):
    """Construct a genai.Client that respects AROS Cloud proxy env vars."""
    from google import genai

    cloud_url = os.environ.get("AROS_CLOUD_URL", "").rstrip("/")
    cloud_key = os.environ.get("AROS_CLOUD_KEY", "")

    if cloud_url and cloud_key:
        print(f"[nano-banana] Using AROS Cloud proxy: {cloud_url}")
        try:
            client = genai.Client(
                api_key=cloud_key,
                http_options={"base_url": cloud_url},
            )
            return client
        except Exception as e:
            print(f"[nano-banana] Proxy failed ({e}). Falling back to direct API.")

    # Fallback to direct API key
    api_key = (
        provided_key
        or os.environ.get("GEMINI_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
        or os.environ.get("GOOGLE_AI_API_KEY")
    )
    if not api_key:
        print("Error: No API key provided. Set GEMINI_API_KEY or pass --api-key.", file=sys.stderr)
        sys.exit(1)

    print("[nano-banana] Using direct Google AI Studio API")
    return genai.Client(api_key=api_key)

def choose_resolution(width: int, height: int, requested: str) -> str:
    """Infer a reasonable output size when editing and no explicit size was set."""
    if requested != DEFAULT_RESOLUTION:
        return requested

    max_dim = max(width, height)
    if max_dim >= 3000:
        return "4K"
    if max_dim >= 1500:
        return "2K"
    if max_dim >= 1024:
        return "1K"
    return "512"

def get_response_parts(response):
    """Handle both convenience accessors and raw candidate payloads."""
    parts = getattr(response, "parts", None)
    if parts is not None:
        return parts

    candidates = getattr(response, "candidates", None) or []
    if not candidates:
        return []

    content = getattr(candidates[0], "content", None)
    return getattr(content, "parts", None) or []

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate or edit images with Nano Banana 2",
    )
    parser.add_argument("--prompt", "-p", required=True, help="Image description / edit instruction")
    parser.add_argument("--filename", "-f", required=True, help="Output filename (PNG)")
    parser.add_argument("--input-image", "-i", help="Optional input image for edit mode")
    parser.add_argument(
        "--resolution",
        "-r",
        choices=list(RESOLUTION_CHOICES),
        default=DEFAULT_RESOLUTION,
        help="Output resolution (default: 1K)",
    )
    parser.add_argument("--api-key", "-k", help="Gemini API key (overrides env)")
    parser.add_argument("--model", "-m", default=MODEL_NAME, help=f"Model name (default: {MODEL_NAME})")

    args = parser.parse_args()

    # Lazy import so argparse errors are fast.
    from google import genai
    from google.genai import types
    from PIL import Image as PILImage

    client = get_proxy_aware_client(args.api_key)
    model = client.get_model(args.model)

    if args.input_image:
        # Edit mode
        try:
            input_image = PILImage.open(args.input_image)
        except FileNotFoundError:
            print(f"Error: Input image '{args.input_image}' not found.", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error loading input image: {e}", file=sys.stderr)
            return 1

        # Infer resolution if not explicitly set
        width, height = input_image.size
        output_resolution = choose_resolution(width, height, args.resolution)

        print(f"Editing image with prompt: '{args.prompt}' (resolution: {output_resolution})")
        response = model.generate_content(
            [args.prompt, types.Blob(mime_type="image/png", data=input_image.tobytes())],
            generation_config=types.GenerationConfig(
                response_mime_type="image/png",
                image_generation_config=types.ImageGenerationConfig(
                    response_size=output_resolution,
                ),
            ),
        )
    else:
        # Generation mode
        print(f"Generating image with prompt: '{args.prompt}' (resolution: {args.resolution})")
        response = model.generate_content(
            args.prompt,
            generation_config=types.GenerationConfig(
                response_mime_type="image/png",
                image_generation_config=types.ImageGenerationConfig(
                    response_size=args.resolution,
                ),
            ),
        )

    parts = get_response_parts(response)
    if not parts:
        print("Error: No image parts found in the response.", file=sys.stderr)
        print(response, file=sys.stderr)
        return 1

    image_data = parts[0].blob.data
    output_path = Path(args.filename)
    output_path.write_bytes(image_data)
    print(f"Image saved to {output_path}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
