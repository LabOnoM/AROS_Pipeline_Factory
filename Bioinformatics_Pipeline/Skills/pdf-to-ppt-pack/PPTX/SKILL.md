---
name: PPTX Skill
description: Create, edit, and extract content from PowerPoint (.pptx) files; use when you need to generate slides programmatically, update existing decks, or export slide previews.
license: MIT
skill-author: AIPOCH
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
    img.save(buf, format="PNG")
    buf.seek(0)

    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    slide.shapes.title.text = "Neural Networks (Illustration)"
    slide.shapes.add_picture(buf, Inches(1), Inches(1.6), width=Inches(8))

    # Slide 4: Edit text on an existing slide (example: update slide 2 title)
    prs.slides[1].shapes.title.text = "Machine Learning: Definition & Types"

    # Slide 5: Summary
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Summary"
    tf = slide.shapes.placeholders[1].text_frame
    tf.clear()
    tf.text = "Key takeaways"
    for bullet in [
        "ML learns from data to make predictions or decisions",
        "Model choice depends on task and constraints",
        "Evaluation and iteration are essential",
    ]:
        p = tf.add_paragraph()
        p.text = bullet

    prs.save(output_path)

def list_slide_titles(pptx_path: str) -> list[str]:
    prs = Presentation(pptx_path)
    titles = []
    for slide in prs.slides:
        title_shape = slide.shapes.title if hasattr(slide.shapes, "title") else None
        if title_shape is not None and getattr(title_shape, "text", "").strip():
            titles.append(title_shape.text.strip())
        else:
            titles.append("(no title)")
    return titles

if __name__ == "__main__":
    out = "machine_learning.pptx"
    create_presentation(out)
    print("Created:", out)
    print("Slide titles:", list_slide_titles(out))
```

## Implementation Details

- **Core library**: Uses `python-pptx` to read/write the Open XML `.pptx` format.
- **Slide layouts**: Slides are created from built-in layouts (e.g., `prs.slide_layouts[0]` for title slide, `prs.slide_layouts[1]` for title+content). Layout availability can vary by template.
- **Text editing model**: Text is edited via `TextFrame` and `Paragraph` objects. Clearing and rebuilding a text frame is a common approach to ensure consistent bullet structure.
- **Image insertion**:
  - Remote images can be downloaded with `requests`.
  - Images are normalized with `Pillow` (e.g., converting to PNG) before embedding to improve compatibility.
  - Placement uses absolute positioning (e.g., `Inches(x)`) and optional sizing parameters.
- **Extraction**: Slide titles are typically accessed via `slide.shapes.title` when present; some slides may not have a title placeholder.
- **Export limitations**:
  - `python-pptx` does not natively render slides to images or PDF. Thumbnail/PDF export generally requires external rendering (commonly LibreOffice in headless mode).
- **Known constraints**:
  - Complex animations and some advanced PowerPoint features may not be editable.
  - Large decks and high-resolution images increase processing time and memory usage.