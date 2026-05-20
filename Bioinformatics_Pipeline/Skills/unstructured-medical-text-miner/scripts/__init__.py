# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""Unstructured Medical Text Miner (Skill ID: 213)

Python package for mining MIMIC-IV medical text data"""

from .main import MedicalTextMiner

__version__ = "0.1.0"
__all__ = ["MedicalTextMiner"]
