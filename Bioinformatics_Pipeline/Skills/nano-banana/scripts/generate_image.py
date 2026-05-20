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
    uv run generate_image.py --prompt "your image description" \\
        --filename "output.png" [--resolution 512|1K|2K|4K] [--api-key KEY]

    uv run generate_image.py --prompt "editing instruction" \\
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

    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    input_image = None
    output_resolution = args.resolution
    if args.input_image:
        try:
            input_image = PILImage.open(args.input_image)
            print(f"Loaded input image: {args.input_image}")

            width, height = input_image.size
            output_resolution = choose_resolution(width, height, args.resolution)
            if output_resolution != args.resolution:
                print(
                    f"Auto-detected resolution: {output_resolution} "
                    f"(from input {width}x{height})"
                )
        except Exception as exc:
            print(f"Error loading input image: {exc}", file=sys.stderr)
            return 1

    if input_image is not None:
        contents = [args.prompt, input_image]
        print(f"Editing image at {output_resolution}...")
    else:
        contents = args.prompt
        print(f"Generating image at {output_resolution}...")

    try:
        response = client.models.generate_content(
            model=args.model,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(image_size=output_resolution),
            ),
        )
    except Exception as exc:
        print(f"Error generating image: {exc}", file=sys.stderr)
        return 2

    image_saved = False
    for part in get_response_parts(response):
        if getattr(part, "text", None):
            print(f"Model response: {part.text}")
            continue

        inline = getattr(part, "inline_data", None)
        if inline is None:
            continue

        from io import BytesIO

        image_data = inline.data
        if isinstance(image_data, str):
            import base64

            image_data = base64.b64decode(image_data)

        image = PILImage.open(BytesIO(image_data))

        if image.mode == "RGBA":
            rgb = PILImage.new("RGB", image.size, (255, 255, 255))
            rgb.paste(image, mask=image.split()[3])
            rgb.save(str(output_path), "PNG")
        elif image.mode == "RGB":
            image.save(str(output_path), "PNG")
        else:
            image.convert("RGB").save(str(output_path), "PNG")

        image_saved = True

    if not image_saved:
        print("Error: No image was generated in the response.", file=sys.stderr)
        return 3

    print(f"\nImage saved: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
