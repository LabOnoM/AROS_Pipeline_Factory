from __future__ import annotations

import argparse
import uuid
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def copy_tree(src: Path, dest: Path) -> None:
    if not src.exists():
        return
    if src.is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        for child in src.iterdir():
            copy_tree(child, dest / child.name)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(src.read_bytes())


def merge_content_types(template_ct: Path, target_ct: Path) -> None:
    t_root = ET.fromstring(template_ct.read_bytes())
    dst_root = ET.fromstring(target_ct.read_bytes())

    existing_defaults = {
        el.attrib.get("Extension"): el for el in dst_root.findall("{*}Default")
    }
    existing_overrides = {
        el.attrib.get("PartName"): el for el in dst_root.findall("{*}Override")
    }

    for el in t_root.findall("{*}Default"):
        ext = el.attrib.get("Extension")
        if ext and ext not in existing_defaults:
            dst_root.append(el)

    for el in t_root.findall("{*}Override"):
        part = el.attrib.get("PartName")
        if part and part not in existing_overrides:
            dst_root.append(el)

    target_ct.write_bytes(ET.tostring(dst_root, encoding="utf-8", xml_declaration=True))


def apply_template(template_pptx: Path, target_pptx: Path, output_pptx: Path) -> None:
    work_root = Path.cwd() / ".pptx_template_tmp" / uuid.uuid4().hex
    template_dir = work_root / "template"
    target_dir = work_root / "target"
    template_dir.mkdir(parents=True, exist_ok=True)
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(template_pptx, "r") as zf:
            zf.extractall(template_dir)
        with zipfile.ZipFile(target_pptx, "r") as zf:
            zf.extractall(target_dir)

        # Replace theme and masters/layouts with template versions.
        copy_tree(template_dir / "ppt" / "theme" / "theme1.xml", target_dir / "ppt" / "theme" / "theme1.xml")
        copy_tree(template_dir / "ppt" / "slideMasters", target_dir / "ppt" / "slideMasters")
        copy_tree(template_dir / "ppt" / "slideLayouts", target_dir / "ppt" / "slideLayouts")

        # Merge content types to support template media formats.
        merge_content_types(
            template_dir / "[Content_Types].xml",
            target_dir / "[Content_Types].xml",
        )

        # Copy template media if not already present.
        template_media = template_dir / "ppt" / "media"
        target_media = target_dir / "ppt" / "media"
        if template_media.exists():
            target_media.mkdir(parents=True, exist_ok=True)
            for media_file in template_media.iterdir():
                dest = target_media / media_file.name
                if dest.exists():
                    continue
                dest.write_bytes(media_file.read_bytes())

        # Repack
        output_pptx.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output_pptx, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in target_dir.rglob("*"):
                if path.is_file():
                    zf.write(path, path.relative_to(target_dir))
    finally:
        if work_root.exists():
            for path in sorted(work_root.rglob("*"), reverse=True):
                try:
                    if path.is_file():
                        path.unlink(missing_ok=True)
                    else:
                        path.rmdir()
                except Exception:
                    pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply PPTX template theme/masters/layouts to a target PPTX.")
    parser.add_argument("--template", required=True, help="Template PPTX path.")
    parser.add_argument("--target", required=True, help="Target PPTX path.")
    parser.add_argument("--output", required=True, help="Output PPTX path.")
    args = parser.parse_args()

    apply_template(Path(args.template), Path(args.target), Path(args.output))


if __name__ == "__main__":
    main()
