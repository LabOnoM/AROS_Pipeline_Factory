---
cpcp_asset: true
name: pptx
description: Create, edit, and extract content from PowerPoint (.pptx) files; use when you need to generate slides programmatically, update existing decks, or export slide previews.
license: MIT
skill-author: AIPOCH
original-source: benchflow-ai/skillsbench
---

## When to Use

- You need to generate a new `.pptx` deck from a short prompt or structured outline (e.g., “5 slides about machine learning”).
- You want to update an existing presentation by adding slides or editing text without manually opening PowerPoint.
- You need to extract structured information from a deck (e.g., slide titles) for indexing, review, or QA.
- You want to export slides to images (thumbnails) or PDF for previews, sharing, or downstream processing.
- You need to insert images into slides (local files or downloaded assets) as part of automated reporting.

## Key Features

- **Presentation creation**: Create new `.pptx` files and populate them with slides.
- **Slide authoring**: Add slides with titles, body text, and images.
- **Text editing**: Modify text content on existing slides.
- **Image support**: Insert and handle images (including basic manipulation via Pillow).
- **Template support**: Start from existing `.pptx` templates and extend them.
- **Export options**: Export slides as images (thumbnails) and optionally export to PDF (via external tooling).
- **Information extraction**: Read slide metadata such as slide titles.

## Dependencies

- **Python**: `>=3.7`
- **python-pptx**: `>=0.6.21`
- **Pillow**: `>=9.0.0` (image handling)
- **requests**: `>=2.28.0` (downloading remote images)
- **Optional (advanced export)**: LibreOffice `>=7.0` (e.g., PPTX → PDF conversion)

## Example Usage

```python
# pip install python-pptx Pillow requests

from pptx import Presentation
from pptx.util import Inches
from PIL import Image
import requests
from io import BytesIO

def create_presentation(output_path: str) -> None:
    prs = Presentation()

    # Slide 1: Title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Machine Learning"
    slide.placeholders[1].text = "A 5-slide overview generated programmatically"

    # Slide 2: Bullets
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "What is Machine Learning?"
    tf = slide.shapes.placeholders[1].text_frame
    tf.clear()
    tf.text = "A field of AI focused on learning patterns from data"
    for bullet in [
        "Supervised learning",
        "Unsupervised learning",
        "Reinforcement learning",
    ]:
        p = tf.add_paragraph()
        p.text = bullet

    # Slide 3: Add an image (downloaded)
    img_url = "https://upload.wikimedia.org/wikipedia/commons/4/44/Neural_network.svg"
    resp = requests.get(img_url, timeout=30)
    resp.raise_for_status()

    # Ensure the image is in a format python-pptx can embed reliably
    img = Image.open(BytesIO(resp.content)).convert("RGBA")
    buf = BytesIO()
    img.save(buf, forma