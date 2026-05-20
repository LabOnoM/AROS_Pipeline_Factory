# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

# Western Blot Quantifier Package
from .main import WesternBlotQuantifier, AnalysisResult, BandRegion

__version__ = "1.0.0"
__all__ = ["WesternBlotQuantifier", "AnalysisResult", "BandRegion"]
