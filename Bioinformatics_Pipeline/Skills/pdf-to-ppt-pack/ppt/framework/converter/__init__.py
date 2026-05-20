# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

# -*- coding: utf-8 -*-
"""
PPTX Converter Module
Converts HTML presentation to PowerPoint format with animations
"""

from .parsers import ConfigParser, DataParser
from .animation import AnimationResolver, AnimationBuilder
from .layout import LayoutCalculator
from .styles import StyleMapper
from .components import ComponentRenderers
from .renderer import SlideRenderer

__all__ = [
    'ConfigParser',
    'DataParser', 
    'AnimationResolver',
    'AnimationBuilder',
    'LayoutCalculator',
    'StyleMapper',
    'ComponentRenderers',
    'SlideRenderer',
]
