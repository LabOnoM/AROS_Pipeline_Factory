# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

import subprocess
import os
import sys

script_path = os.path.expanduser("~/.gemini/skills/iterative-validator/scripts/main.py")

def test_smoke():
    # Calling without arguments should return error and exit 2
    result = subprocess.run(["python3", script_path], capture_output=True)
    assert result.returncode == 2
    assert b"the following arguments are required" in result.stderr
