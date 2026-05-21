import argparse
import re
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as exc:  # pragma: no cover - environment specific
    raise SystemExit(f"PyMuPDF (fitz) is required: {exc}")

try:
    from PIL import Image
except Exception as exc:  # pragma: no cover - environment specific
    raise SystemExit(f"Pillow is required: {exc}")


FIGURE_RE = re.compile(r"\b(?:Fig(?:ure)?\.?)\s*(\d+)\b", re.IGNORECASE)
GA_RE = re.compile(r"\bGraphical\s+Abstract\b", re.IGNORECASE)


def extract_page_text(doc):
    pages_text = []
    for page in doc:
        pages_text.append(page.get_text("text"))
    return pages_text


def find_captions(page):
    captions = []
    blocks = page.get_text("blocks")  # (x0, y0, x1, y1, text, block_no, block_type)
    for x0, y0, x1, y1, text, *_ in blocks:
        if not text or not isinstance(text, str):
            continue
        text_str = " ".join(text.split())
        if not text_str:
            continue
        ga_match = GA_RE.search(text_str)
        if ga_match:
            captions.append(
                {
                    "kind": "graphical_abstract",
                    "label": "Graphical abstract",
                    "y0": y0,
                    "y1": y1,
                    "x0": x0,
                    "text": text_str,
                }
            )
            continue
        fig_match = FIGURE_RE.search(text_str)
        if fig_match:
            fig_no = fig_match.group(1)
            captions.append(
                {
                    "kind": "figure",
                    "label": f"Figure_{fig_no}",
                    "y0": y0,
                    "y1": y1,
                    "x0": x0,
                    "text": text_str,
                }
            )
    return captions


def collect_image_rects(page):
    rects = []
    for img in page.get_images(full=True):
        xref = img[0]
        for rect in page.get_image_rects(xref):
            rects.append(rect)
    return rects


def _scale_rect(rect, sx, sy):
    return (
        int(rect.x0 * sx),
        int(rect.y0 * sy),
        int(rect.x1 * sx),
        int(rect.y1 * sy),
    )


def render_masked_gray(page, dpi=150):
    pix = page.get_pixmap(dpi=dpi)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    gray = img.convert("L")
    pixels = gray.load()

    sx = pix.width / page.rect.width
    sy = pix.height / page.rect.height
    blocks = page.get_text("blocks")
    for x0, y0, x1, y1, _text, _bn, btype in blocks:
        if btype != 0:
            continue
        ix0, iy0, ix1, iy1 = _scale_rect(fitz.Rect(x0, y0, x1, y1), sx, sy)
        for y in range(max(0, iy0), min(pix.height, iy1)):
            for x in range(max(0, ix0), min(pix.width, ix1)):
                pixels[x, y] = 255

    return gray, sx, sy


def raster_components_without_text(page, gray, sx, sy):
    pixels = gray.load()
    w, h = gray.size
    visited = [[False] * w for _ in range(h)]
    components = []
    min_area = (w * h) * 0.002

    def flood_fill(x, y):
        stack = [(x, y)]
        minx = maxx = x
        miny = maxy = y
        area = 0
        while stack:
            cx, cy = stack.pop()
            if cx < 0 or cy < 0 or cx >= w or cy >= h:
                continue
            if visited[cy][cx]:
                continue
            visited[cy][cx] = True
            if pixels[cx, cy] > 245:
                continue
            area += 1
            if cx < minx:
                minx = cx
            if cx > maxx:
                maxx = cx
            if cy < miny:
                miny = cy
            if cy > maxy:
                maxy = cy
            stack.extend(
                [
                    (cx + 1, cy),
                    (cx - 1, cy),
                    (cx, cy + 1),
                    (cx, cy - 1),
                ]
            )
        return minx, miny, maxx, maxy, area

    for y in range(h):
        for x in range(w):
            if visited[y][x]:
                continue
            if pixels[x, y] > 245:
                continue
            minx, miny, maxx, maxy, area = flood_fill(x, y)
            if area >= min_area:
                components.append((minx, miny, maxx, maxy))

    # Convert components back to PDF coordinate rects
    rects = []
    for minx, miny, maxx, maxy in components:
        rx0 = minx / sx
        ry0 = miny / sy
        rx1 = maxx / sx
        ry1 = maxy / sy
        rects.append(fitz.Rect(rx0, ry0, rx1, ry1))
    return rects


def band_density(gray, sx, sy, band_top, band_bottom, step=3):
    w, h = gray.size
    y0 = max(0, int(band_top * sy))
    y1 = min(h, int(band_bottom * sy))
    if y1 <= y0:
        return 0.0
    pixels = gray.load()
    count = 0
    total = 0
    for y in range(y0, y1, step):
        for x in range(0, w, step):
            total += 1
            if pixels[x, y] <= 245:
                count += 1
    return count / max(1, total)


def pick_image_for_caption(rects, caption_y0):
    if not rects:
        return None
    candidates = []
    for rect in rects:
        if rect.y1 <= caption_y0:
            distance = caption_y0 - rect.y1
            area = rect.get_area()
            candidates.append((distance, -area, rect))
    if candidates:
        candidates.sort(key=lambda t: (t[0], t[1]))
        return candidates[0][2]
    # Fallback: pick largest image on page
    rects_sorted = sorted(rects, key=lambda r: r.get_area(), reverse=True)
    return rects_sorted[0] if rects_sorted else None


def rects_in_band(rects, band_top, band_bottom):
    hits = []
    for rect in rects:
        # Any overlap with the band counts.
        if rect.y1 >= band_top and rect.y0 <= band_bottom:
            hits.append(rect)
    return hits


def union_rect(rects):
    if not rects:
        return None
    x0 = min(r.x0 for r in rects)
    y0 = min(r.y0 for r in rects)
    x1 = max(r.x1 for r in rects)
    y1 = max(r.y1 for r in rects)
    return fitz.Rect(x0, y0, x1, y1)

def total_area(rects):
    return sum(r.get_area() for r in rects)


def largest_rect(rects, min_area):
    if not rects:
        return None
    rects_sorted = sorted(rects, key=lambda r: r.get_area(), reverse=True)
    return rects_sorted[0] if rects_sorted[0].get_area() >= min_area else None


def save_clip(page, rect, out_path):
    pix = page.get_pixmap(clip=rect, dpi=200)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path)


def caption_pages(doc):
    page_map = {}
    for i, page in enumerate(doc):
        text = page.get_text("text") or ""
        for m in FIGURE_RE.finditer(text):
            fig_no = m.group(1)
            page_map[f"Figure_{fig_no}"] = i
        if GA_RE.search(text):
            page_map["Graphical abstract"] = i
    return page_map


def render_page_image(doc, page_index, out_path, dpi=200):
    page = doc[page_index]
    pix = page.get_pixmap(dpi=dpi)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(out_path)


def get_page_rects(page):
    gray, sx, sy = render_masked_gray(page)
    rects = collect_image_rects(page)
    rects.extend(raster_components_without_text(page, gray, sx, sy))
    return rects


def extract_figures(pdf_path: Path, out_dir: Path):
    doc = fitz.open(pdf_path)
    pages_text = extract_page_text(doc)
    extracted = []

    for page_index, page in enumerate(doc):
        rects = get_page_rects(page)
        captions = find_captions(page)
        page_text = pages_text[page_index] or ""
        # Fallback: detect figure labels in page text even if no caption block is found.
        for match in FIGURE_RE.finditer(page_text):
            fig_no = match.group(1)
            label = f"Figure_{fig_no}"
            if not any(c["label"] == label for c in captions):
                captions.append(
                    {
                        "kind": "figure",
                        "label": label,
                        "y0": page.rect.y1,
                        "x0": page.rect.x0,
                        "text": f"Figure {fig_no}",
                    }
                )
        if GA_RE.search(page_text) and not any(
            c["kind"] == "graphical_abstract" for c in captions
        ):
            captions.append(
                {
                    "kind": "graphical_abstract",
                    "label": "Graphical abstract",
                    "y0": page.rect.y1,
                    "x0": page.rect.x0,
                    "text": "Graphical Abstract",
                }
            )
        # Sort captions by vertical position to create bands between them.
        captions_sorted = sorted(captions, key=lambda c: c["y0"])
        for idx, cap in enumerate(captions_sorted):
            prev_y = page.rect.y0 if idx == 0 else captions_sorted[idx - 1]["y1"]
            next_y = (
                captions_sorted[idx + 1]["y0"]
                if idx + 1 < len(captions_sorted)
                else page.rect.y1
            )
            band_top = prev_y
            band_bottom = cap["y0"]
            band2_top = cap["y1"]
            band2_bottom = next_y

            band_rects_above = rects_in_band(rects, band_top, band_bottom)
            band_rects_below = rects_in_band(rects, band2_top, band2_bottom)

            rect = None
            if band_rects_above or band_rects_below:
                area_above = total_area(band_rects_above)
                area_below = total_area(band_rects_below)
                if area_above >= area_below and band_rects_above:
                    rect = union_rect(band_rects_above)
                elif band_rects_below:
                    rect = union_rect(band_rects_below)
            if rect is None:
                rect = pick_image_for_caption(rects, cap["y0"])

            target_page = page
            min_area = page.rect.get_area() * 0.01
            if rect is None or rect.get_area() < min_area:
                prev_page = doc[page_index - 1] if page_index > 0 else None
                next_page = doc[page_index + 1] if page_index + 1 < len(doc) else None
                prev_rect = None
                next_rect = None
                if prev_page is not None:
                    prev_rects = get_page_rects(prev_page)
                    prev_rect = largest_rect(prev_rects, prev_page.rect.get_area() * 0.01)
                if next_page is not None:
                    next_rects = get_page_rects(next_page)
                    next_rect = largest_rect(next_rects, next_page.rect.get_area() * 0.01)
                if prev_rect is not None:
                    rect = prev_rect
                    target_page = prev_page
                elif next_rect is not None:
                    rect = next_rect
                    target_page = next_page

            if rect is None:
                rect = page.rect
            label = cap["label"]
            if cap["kind"] == "graphical_abstract":
                filename = "Graphical abstract.jpg"
            else:
                filename = f"{label}.jpg"
            out_path = out_dir / filename
            try:
                save_clip(target_page, rect, out_path)
                extracted.append((label, str(out_path)))
            except Exception:
                continue

    # Save full extracted text for offline summarization
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "extracted_text.txt").write_text("\n\n".join(pages_text), encoding="utf-8")

    # Save a simple figure legend list for quick reference
    legend_lines = []
    full_text = "\n".join(pages_text)
    for match in FIGURE_RE.finditer(full_text):
        legend_lines.append(match.group(0))
    (out_dir / "figure_legend_hits.txt").write_text(
        "\n".join(sorted(set(legend_lines))), encoding="utf-8"
    )

    doc.close()
    return extracted


def main():
    parser = argparse.ArgumentParser(description="Extract figure images from a PDF (no API).")
    parser.add_argument("--pdf", required=True, help="Path to the PDF file.")
    parser.add_argument("--outdir", required=True, help="Output directory.")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    out_dir = Path(args.outdir)

    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    extracted = extract_figures(pdf_path, out_dir)
    print(f"Extracted {len(extracted)} figure images.")


if __name__ == "__main__":
    main()
