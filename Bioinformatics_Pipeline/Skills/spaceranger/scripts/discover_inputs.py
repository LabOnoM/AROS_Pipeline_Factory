# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""
discover_inputs.py — Auto-discover Space Ranger inputs in a project directory.

Scans for FASTQ files, CytAssist images, microscope images, probe sets, and slide
serial numbers. Produces a structured inventory for QC Gate 1 user confirmation.

Usage:
    from discover_inputs import InputDiscovery
    discovery = InputDiscovery("/path/to/project")
    inputs = discovery.scan()
    print(discovery.format_inventory(inputs))
"""

import glob
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class DiscoveredInputs:
    """Container for all discovered pipeline inputs."""
    fastq_dirs: List[str] = field(default_factory=list)
    fastq_files: List[str] = field(default_factory=list)
    cytassist_images: List[str] = field(default_factory=list)
    microscope_images: List[str] = field(default_factory=list)
    probe_sets: List[str] = field(default_factory=list)
    slide_serials: List[str] = field(default_factory=list)
    reference_dirs: List[str] = field(default_factory=list)
    alignment_jsons: List[str] = field(default_factory=list)
    segmentation_files: List[str] = field(default_factory=list)


class InputDiscovery:
    """Auto-discover Space Ranger inputs in a project directory."""

    # Patterns for slide serial numbers (e.g., H1-YD7CDZK)
    SLIDE_PATTERN = re.compile(r'(H\d-[A-Z0-9]{7})')

    # CytAssist image identifiers
    CYTASSIST_KEYWORDS = ["CAVG", "CYTASSIST", "cytassist"]

    # Minimum size for microscope images (100 MB)
    MICROSCOPE_MIN_SIZE = 100_000_000

    def __init__(self, project_dir: str, search_depth: int = 5):
        self.project_dir = os.path.abspath(project_dir)
        self.search_depth = search_depth

    def scan(self) -> DiscoveredInputs:
        """Perform a full scan of the project directory."""
        inputs = DiscoveredInputs()

        # ── FASTQ Files ──────────────────────────────────────
        for ext in ["*.fastq.gz", "*.fq.gz"]:
            found = glob.glob(
                os.path.join(self.project_dir, "**", ext),
                recursive=True,
            )
            inputs.fastq_files.extend(found)

        # Deduce FASTQ directories
        fq_dirs = set(os.path.dirname(f) for f in inputs.fastq_files)
        inputs.fastq_dirs = sorted(fq_dirs)

        # ── Image Files ──────────────────────────────────────
        all_images = []
        for ext in ["*.tif", "*.tiff", "*.btf", "*.qptiff", "*.jpg", "*.jpeg"]:
            all_images.extend(
                glob.glob(os.path.join(self.project_dir, "**", ext), recursive=True)
            )

        for img in all_images:
            basename = os.path.basename(img).upper()

            # CytAssist detection
            if any(kw.upper() in basename for kw in self.CYTASSIST_KEYWORDS):
                inputs.cytassist_images.append(img)
            # Large TIFFs / BTFs as microscope images
            elif img.lower().endswith((".btf", ".qptiff")):
                inputs.microscope_images.append(img)
            elif img.lower().endswith((".tif", ".tiff")):
                try:
                    size = os.path.getsize(img)
                    if size > self.MICROSCOPE_MIN_SIZE:
                        inputs.microscope_images.append(img)
                except OSError:
                    pass

        # ── Probe Sets ───────────────────────────────────────
        inputs.probe_sets = glob.glob(
            os.path.join(self.project_dir, "**", "*Probe_Set*.csv"),
            recursive=True,
        )
        # Also check inside spaceranger installation
        sr_probe_dir = os.path.expanduser("~/spaceranger*/probe_sets")
        inputs.probe_sets.extend(glob.glob(os.path.join(sr_probe_dir, "*.csv")))

        # ── Slide Serials ────────────────────────────────────
        slide_candidates = set()
        for f in inputs.fastq_files + inputs.cytassist_images + inputs.microscope_images:
            matches = self.SLIDE_PATTERN.findall(os.path.basename(f))
            slide_candidates.update(matches)
        inputs.slide_serials = sorted(slide_candidates)

        # ── Reference Transcriptomes ─────────────────────────
        ref_patterns = [
            os.path.join(self.project_dir, "**", "refdata-gex-*"),
            os.path.join("/opt", "refdata-gex-*"),
            os.path.expanduser("~/refdata-gex-*"),
        ]
        for pattern in ref_patterns:
            for d in glob.glob(pattern, recursive=True):
                if os.path.isdir(d) and os.path.exists(os.path.join(d, "fasta")):
                    inputs.reference_dirs.append(d)

        # ── Alignment JSONs ──────────────────────────────────
        inputs.alignment_jsons = glob.glob(
            os.path.join(self.project_dir, "**", "*.json"),
            recursive=True,
        )
        # Filter to likely alignment files
        inputs.alignment_jsons = [
            f for f in inputs.alignment_jsons
            if any(kw in os.path.basename(f).lower() for kw in ["align", "loupe", "fiducial"])
        ]

        # ── Custom Segmentation Files ────────────────────────
        inputs.segmentation_files = glob.glob(
            os.path.join(self.project_dir, "**", "*.geojson"),
            recursive=True,
        )
        inputs.segmentation_files.extend(
            glob.glob(os.path.join(self.project_dir, "**", "*segmentation*.tif*"), recursive=True)
        )

        return inputs

    @staticmethod
    def format_inventory(inputs: DiscoveredInputs) -> str:
        """Format discovered inputs as a readable table."""
        lines = [
            "┌─────────────────────────────────────────────────────────────┐",
            "│           SPACE RANGER INPUT DISCOVERY REPORT               │",
            "├─────────────────────────────────────────────────────────────┤",
        ]

        def _add_section(title, items, max_show=5):
            lines.append(f"│ {title}:")
            if not items:
                lines.append("│   (none found)")
            else:
                for item in items[:max_show]:
                    lines.append(f"│   • {os.path.basename(item)}")
                    lines.append(f"│     {item}")
                if len(items) > max_show:
                    lines.append(f"│   ... and {len(items) - max_show} more")
            lines.append("│")

        _add_section("📁 FASTQ Directories", inputs.fastq_dirs)
        _add_section(f"🧬 FASTQ Files ({len(inputs.fastq_files)} total)",
                     inputs.fastq_files, max_show=3)
        _add_section("📷 CytAssist Images", inputs.cytassist_images)
        _add_section("🔬 Microscope Images", inputs.microscope_images)
        _add_section("🎯 Probe Sets", inputs.probe_sets)
        _add_section("📋 Slide Serials", [f"Slide: {s}" for s in inputs.slide_serials])
        _add_section("📚 Reference Transcriptomes", inputs.reference_dirs)
        _add_section("🔧 Alignment JSONs", inputs.alignment_jsons)
        _add_section("🔬 Custom Segmentation Files", inputs.segmentation_files)

        lines.append("└─────────────────────────────────────────────────────────────┘")
        return "\n".join(lines)


# ── CLI Entrypoint ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python discover_inputs.py <project_directory>")
        sys.exit(1)

    discovery = InputDiscovery(sys.argv[1])
    inputs = discovery.scan()
    print(discovery.format_inventory(inputs))
