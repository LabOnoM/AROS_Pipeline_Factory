# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

 Brain Federation Sync Engine — Cross-PC brain.db Merge with LLM Review
=======================================================================
Provides export_brain() and import_and_merge() for the AROS Brain Federation
protocol. Allows two AROS instances on different PCs to share and merge their
accumulated knowledge, skills, and world models.

Architecture:
  Export: Selective extraction of mergeable layers → JSON envelope
  Import: Cosine dedup (≥0.92) → LLM review of conflicts → Merge commit

Merge Depth Matrix (v2.2 — Full-Directory Sync):
  ✅ Deep merge: world_facts (cosine dedup), mental_models, agent_taxonomy
  ✅ LLM review: Skill directories (all text files), KI artifacts (all files),
                 Workflows, AROS_POLICY.md — per-file granularity
  ✅ Binary:     Skill binary files (images, .pyc) — install-if-missing only
  ✅ Metadata:   KI metadata.json — timestamp-aware union merge
  ❌ Excluded:   experiences, system_telemetry, processed_files, swarm_jobs
                 (machine-local records must NOT be federated)

Adaptive Timeout Architecture (AROS v2.6):
  - _llm_review_merge() resolves the Gemini API key via 3-step chain:
      1. GEMINI_API_KEY env var
      2. GOOGLE_AI_API_KEY env var (aliased to GEMINI_API_KEY)
      3. ~/.gemini/.env file fallback
  - Per-Gemini-call timeout: adaptive via estimate_llm_call_timeout(),
    scaled by prompt length. On timeout, returns keep_local (fail-safe).
  - Full merge timeout: adaptive via estimate_merge_timeout() in main.py,
    with a threading.Event cancellation token for clean thread shutdown.
  - EMA self-calibration: actual throughput is recorded via record_throughput()
    and used to refine future timeout estimates automatically.
  - All exceptions return keep_local — never corrupt local brain data.

Called from: antigravity_dashboard/main.py → merge_brain() endpoint.
The caller attaches a FileHandler to this module's 'brain-sync' logger
for per-job log visibility in the dashboard Swarm panel.
"""


import os
import json
import struct
import base64
import math
import shutil
import sqlite3
import logging
import threading
import time
from datetime import datetime, timezone
from typing import Optional
from .adaptive_timeout import estimate_llm_call_timeout, record_throughput

logger = logging.getLogger("brain-sync")

DB_PATH = os.environ.get(
    "BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db")
)

SKILLS_DIR  = os.path.expanduser("~/.gemini/skills")
KI_DIR      = os.path.expanduser("~/.gemini/antigravity/knowledge")
WORKFLOW_DIR = os.path.expanduser("~/.gemini/antigravity/global_workflows")
AROS_POLICY_PATH  = os.path.expanduser("~/.gemini/antigravity/AROS_POLICY.md")

COSINE_DEDUP_THRESHOLD = 0.92


# ── Embedding Helpers ────────────────────────────────────────

def _pack_embedding(emb: list[float]) -> bytes:
    return struct.pack(f"{len(emb)}f", *emb)


def _unpack_embedding(blob: bytes) -> list[float]:
    n = len(blob) // 4
    return list(struct.unpack(f"{n}f", blob))


def _b64_encode_embedding(emb: list[float]) -> str:
    return base64.b64encode(_pack_embedding(emb)).decode("ascii")


def _b64_decode_embedding(b64: str) -> list[float]:
    return _unpack_embedding(base64.b64decode(b64))


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _get_db():
    import sqlite_vec
    db = sqlite3.connect(DB_PATH)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    db.row_factory = sqlite3.Row
    return db


# ── EXPORT ───────────────────────────────────────────────────

def export_brain(instance_id: str = "default") -> dict:
    """
    Export a selective brain snapshot to a portable JSON envelope.
    
    Includes:
      - world_facts WHERE source_url IS NULL (conversation-extracted wisdom)
      - mental_models (all)
      - agent_taxonomy (all)
      - Mutated SKILL.md files (from disk)
      - KI directories (from disk)
      - Workflow files (from disk)
      - AROS_POLICY.md policy (from disk)
    
    Excludes:
      - experiences (raw, already distilled)
      - system_telemetry (machine-local counters)
      - processed_files (machine-local paths)
      - indexed world_facts (reproducible from skill files)
    """
    db = _get_db()
    c = db.cursor()

    envelope = {
        "aros_version": "2.1",
        "instance_id": instance_id,
        "exported_at": datetime.now(timezone.utc).isof