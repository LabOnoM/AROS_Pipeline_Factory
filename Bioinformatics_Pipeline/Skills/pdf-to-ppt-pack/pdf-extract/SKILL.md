---
name: pdf-extract
description: Extract PDF selectable text and full-page or segmented page images (including tables) into Markdown with per-page headings and image links; use when you need both readable text and page visuals for PPT creation, review, or analysis.
license: MIT
skill-author: AIPOCH
---

## When to Use

- Converting a PDF report/paper into Markdown while preserving page structure (`## Page XX`) for easy navigation.
- Preparing PPT or design materials where you need both extracted text and page screenshots/blocks (tables, figures, diagrams).
- Reviewing scanned or mixed PDFs and filtering out “text-only” screenshots to keep only meaningful visuals.
- Building a dataset for downstream analysis where each page’s text and images must be linked and traceable.
- Creating a lightweight “PDF-to-Markdown” archive with per-page headings and image references.

## Key Features

- Extracts selectable PDF text and normalizes paragraphs (collapses line breaks into readable paragraphs).
- Writes Markdown with a document title and per-page sections (`# <filename>`, `## Page XX`).
- Supports multiple image extraction modes:
  - **segment** (default): renders segmented page blocks (useful for tables/figures).
  - **embedded**: extracts embedded images from the PDF.
  - **page**: renders full pages as images.
- Optional post-filters to reduce noisy images:
  - Filter text-heavy images via OCR (`--filter-text`).
  - Drop images that match extracted page text (likely screenshots of text) (`--filter-match`).
  - Drop images overlapping PDF text blocks without OCR (`--filter-pdf-text`).
- Produces stable, per-page image links in Markdown for easy referencing.

## Dependencies

- `pdfplumber` (version not specified)
- `pymupdf` (version not specified)
- `pytesseract` (version not specified; required only when `--filter-text on` or `--filter-match on`)

## Example Usage

```bash
python scripts/extract_pdf.py \
  --input input.pdf \
  --output output.md \
  --image-dir images \
  --image-mode segment \
  --filter-text on \
  --text-threshold 0.25 \
  --text-lang eng \
  --filter-match on \
  --match-lang eng \
  --match-min-len 30 \
  --filter-pdf-text on \
  --pdf-text-threshold 0.1
```

Expected Markdown structure:

- Document title: `# <filename>`
- Per-page section: `## Page XX`
- Text paragraphs (normalized)
- Image links, depending on mode:
  - Segmented blocks: `![page-XX](images/page-XX-block-YY.png)` with `--image-mode segment`
  - Embedded images: `![page-XX](images/page-XX-img-YY.png)` with `--image-mode embedded`
  - Full page render: `![page-XX](images/page-XX.png)` with `--image-mode page`

## Implementation Details

- **Text extraction and normalization**
  - Extracts selectable text from the PDF and collapses line breaks to form coherent paragraphs.
  - Headings are inferred using font-size heuristics (larger font sizes are treated as heading markers).

- **Image extraction modes**
  - `segment` (default): renders page segments/blocks to capture localized content (tables/figures) rather than entire pages.
  - `embedded`: extracts images embedded in the PDF content stream.
  - `page`: renders each full page as a single image (not recommended if you need cropped screenshots/blocks).

- **Filtering options**
  - `--filter-text on`: runs OCR on extracted images and removes images whose OCR text density exceeds `--text-threshold` (e.g., `0.25`).
  - `--filter-match on`: removes images whose OCR text substantially matches the page’s extracted text; controlled by `--match-min-len` and language via `--match-lang`.
  - `--filter-pdf-text on`: removes images that overlap PDF text blocks using PDF layout information (no OCR); controlled by `--pdf-text-threshold` (e.g., `0.1`).

- **Output writing**
  - Writes a single Markdown file with `## Page XX` sections and image links pointing to files saved under `--image-dir`.