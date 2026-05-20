# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validation helper for file-search."""

from __future__ import annotations

import argparse
import shutil


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate that ripgrep is available before using the file-search skill."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Print a short availability result for ripgrep.",
    )
    args = parser.parse_args()
    if args.check:
        print("rg: ok" if shutil.which("rg") else "rg: missing")


if __name__ == "__main__":
    main()
