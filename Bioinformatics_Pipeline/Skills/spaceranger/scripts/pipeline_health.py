"""
pipeline_health.py — Automated Space Ranger Pipeline Health Scoring

Parses metrics_summary.csv from a spaceranger run and produces a structured
health report with an overall grade (A/B/C/F) and detailed warnings.

Usage:
    from pipeline_health import PipelineHealthScorer
    scorer = PipelineHealthScorer("path/to/run_id")
    report = scorer.generate_report()
    print(scorer.format_report(report))
"""

import csv
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class MetricThreshold:
    """Definition of a QC metric threshold."""
    name: str
    parser: str  # "int" or "pct"
    good_min: float
    warn_min: float = 0.0
    description: str = ""


# ── Standard QC Metric Thresholds ────────────────────────────────────────────
METRIC_THRESHOLDS = [
    MetricThreshold(
        name="Estimated Number of Cells",
        parser="int",
        good_min=100,
        warn_min=50,
        description="Total tissue-covered spot/cell count",
    ),
    MetricThreshold(
        name="Mean Reads per Cell",
        parser="int",
        good_min=20000,
        warn_min=10000,
        description="Sequencing depth per cell/spot",
    ),
    MetricThreshold(
        name="Median Genes per Cell",
        parser="int",
        good_min=500,
        warn_min=200,
        description="Transcriptomic complexity",
    ),
    MetricThreshold(
        name="Fraction Reads in Spots Under Tissue",
        parser="pct",
        good_min=50.0,
        warn_min=30.0,
        description="Signal specificity (reads on tissue vs off)",
    ),
    MetricThreshold(
        name="Valid Barcodes",
        parser="pct",
        good_min=75.0,
        warn_min=50.0,
        description="Barcode quality",
    ),
    MetricThreshold(
        name="Reads Mapped Confidently to Genome",
        parser="pct",
        good_min=90.0,
        warn_min=70.0,
        description="Alignment rate to reference genome",
    ),
    MetricThreshold(
        name="Q30 Bases in Barcode",
        parser="pct",
        good_min=90.0,
        warn_min=80.0,
        description="Sequencing quality in barcode reads",
    ),
]


class PipelineHealthScorer:
    """Parse and score Space Ranger pipeline outputs."""

    def __init__(self, run_dir: str):
        self.run_dir = run_dir
        self.outs_dir = os.path.join(run_dir, "outs")

    @staticmethod
    def _parse_pct(val: str) -> float:
        """Parse percentage string like '95.1%' → 95.1."""
        if isinstance(val, (int, float)):
            return float(val)
        return float(str(val).replace("%", "").replace(",", "").strip())

    @staticmethod
    def _parse_int(val: str) -> int:
        """Parse comma-separated integer like '12,450' → 12450."""
        if isinstance(val, int):
            return val
        return int(str(val).replace(",", "").strip())

    def _load_metrics(self) -> Optional[Dict[str, str]]:
        """Load metrics_summary.csv."""
        metrics_file = os.path.join(self.outs_dir, "metrics_summary.csv")
        if not os.path.exists(metrics_file):
            return None
        with open(metrics_file, "r") as f:
            reader = csv.DictReader(f)
            return next(reader, None)

    def _load_scale_factors(self) -> Optional[dict]:
        """Load scalefactors_json.json."""
        sf_file = os.path.join(self.outs_dir, "spatial", "scalefactors_json.json")
        if not os.path.exists(sf_file):
            return None
        with open(sf_file) as f:
            return json.load(f)

    def _check_outputs_exist(self) -> Dict[str, bool]:
        """Check which output files exist."""
        checks = {
            "web_summary": os.path.join(self.outs_dir, "web_summary.html"),
            "metrics_summary": os.path.join(self.outs_dir, "metrics_summary.csv"),
            "filtered_matrix_h5": os.path.join(self.outs_dir, "filtered_feature_bc_matrix.h5"),
            "spatial_dir": os.path.join(self.outs_dir, "spatial"),
            "aligned_fiducials": os.path.join(self.outs_dir, "spatial", "aligned_fiducials.jpg"),
            "detected_tissue": os.path.join(self.outs_dir, "spatial", "detected_tissue_image.jpg"),
            "cloupe": os.path.join(self.outs_dir, "cloupe.cloupe"),
        }

        # Visium HD specific
        for bin_size in ["square_002um", "square_008um", "square_016um"]:
            checks[f"binned_{bin_size}"] = os.path.join(
                self.outs_dir, "binned_outputs", bin_size, "filtered_feature_bc_matrix.h5"
            )

        # Segmented outputs
        checks["segmented_outputs"] = os.path.join(
            self.outs_dir, "segmented_outputs", "filtered_feature_bc_matrix.h5"
        )

        return {name: os.path.exists(path) for name, path in checks.items()}

    def generate_report(self) -> dict:
        """
        Generate a comprehensive pipeline health report.
        Returns a structured dict with grade, metrics, warnings, and output inventory.
        """
        report = {
            "run_dir": self.run_dir,
            "grade": "A",
            "metrics": {},
            "warnings": [],
            "errors": [],
            "outputs_exist": self._check_outputs_exist(),
            "scale_factors": self._load_scale_factors(),
            "is_visium_hd": False,
        }

        # Check if Visium HD
        report["is_visium_hd"] = report["outputs_exist"].get("binned_square_002um", False)

        # Load and score metrics
        raw_metrics = self._load_metrics()
        if raw_metrics is None:
            report["errors"].append("metrics_summary.csv not found — pipeline may not have completed")
            report["grade"] = "F"
            return report

        for threshold in METRIC_THRESHOLDS:
            raw_val = raw_metrics.get(threshold.name)
            if raw_val is None or raw_val == "":
                continue

            try:
                if threshold.parser == "int":
                    parsed = self._parse_int(raw_val)
                else:
                    parsed = self._parse_pct(raw_val)
            except (ValueError, TypeError):
                report["warnings"].append(f"Could not parse {threshold.name}: {raw_val}")
                continue

            report["metrics"][threshold.name] = {
                "value": parsed,
                "raw": raw_val,
                "status": "good",
            }

            if parsed < threshold.warn_min:
                report["metrics"][threshold.name]["status"] = "fail"
                report["warnings"].append(
                    f"🔴 {threshold.name} = {parsed} (below minimum {threshold.warn_min})"
                )
                report["grade"] = "F" if report["grade"] != "F" else "F"
            elif parsed < threshold.good_min:
                report["metrics"][threshold.name]["status"] = "warn"
                report["warnings"].append(
                    f"🟡 {threshold.name} = {parsed} (below recommended {threshold.good_min})"
                )
                if report["grade"] == "A":
                    report["grade"] = "B"

        # Downgrade for missing critical outputs
        if not report["outputs_exist"].get("web_summary", False):
            report["errors"].append("web_summary.html missing")
            report["grade"] = "C"
        if not report["outputs_exist"].get("spatial_dir", False):
            report["errors"].append("spatial/ directory missing")
            report["grade"] = "C"

        return report

    @staticmethod
    def format_report(report: dict) -> str:
        """Format a health report as a human-readable string."""
        lines = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║            SPACE RANGER PIPELINE HEALTH REPORT              ║",
            "╠══════════════════════════════════════════════════════════════╣",
            f"║  Run:    {report['run_dir']:<50} ║",
            f"║  Grade:  {report['grade']:<50} ║",
            f"║  Type:   {'Visium HD' if report['is_visium_hd'] else 'Standard Visium':<50} ║",
            "╠══════════════════════════════════════════════════════════════╣",
        ]

        for name, data in report["metrics"].items():
            icon = "✅" if data["status"] == "good" else ("⚠️" if data["status"] == "warn" else "❌")
            short_name = name[:35]
            lines.append(f"║  {icon} {short_name:<38} {str(data['value']):>12}  ║")

        if report["warnings"]:
            lines.append("╠══════════════════════════════════════════════════════════════╣")
            for w in report["warnings"]:
                lines.append(f"║  {w:<58} ║")

        if report["errors"]:
            lines.append("╠══════════════════════════════════════════════════════════════╣")
            for e in report["errors"]:
                lines.append(f"║  🔴 {e:<55} ║")

        lines.append("╚══════════════════════════════════════════════════════════════╝")
        return "\n".join(lines)


# ── CLI Entrypoint ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pipeline_health.py <spaceranger_run_dir>")
        sys.exit(1)

    scorer = PipelineHealthScorer(sys.argv[1])
    report = scorer.generate_report()
    print(scorer.format_report(report))

    # Exit with appropriate code
    sys.exit(0 if report["grade"] in ("A", "B") else 1)
