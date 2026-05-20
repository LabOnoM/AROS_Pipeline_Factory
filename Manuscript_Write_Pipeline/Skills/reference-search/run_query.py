# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

#!/usr/bin/env python3
"""Run a literature search query"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

import pubmed_search

pubmed_search.CONFIG["INPUT_JSON"] = Path(__file__).parent / "inputs" / "query.json"
pubmed_search.CONFIG["EMAIL"] = "researcher@example.com"

if __name__ == "__main__":
    pubmed_search.main()
