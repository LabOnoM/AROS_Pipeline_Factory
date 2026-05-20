# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================

"""
AROS Brain — Database Layer (db.py)
====================================
Manages the central brain.db (SQLite + sqlite-vec) used by all AROS subsystems.

Responsibilities:
  - Schema creation and migration for all tables:
    world_facts, experiences, mental_models, system_telemetry, processed_files,
    swarm_jobs, task_taxonomy, task_evaluations, evaluation_rules, golden_test_battery
  - Vector table initialization (vec_world_facts, vec_experiences, vec_mental_models)
  - Connection factory (get_db) with sqlite-vec extension loading
  - verify_and_init_db() — idempotent bootstrapper called at startup

Part of: antigravity-brain (AROS Memory & Persistence Layer)
"""
import sqlite3
import sqlite_vec
import os

DB_PATH = os.environ.get("BRAIN_DB_PATH", os.path.expanduser("~/.gemini/antigravity/brain.db"))

def verify_and_init_db():
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        
    db = sqlite3.connect(DB_PATH)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    
    # Enable WAL for concurrent background dreaming and foreground MCP queries
    db.execute("PRAGMA journal_mode=WAL;")
    
    # 1. Experiences (Episodic Memory from logs)
    db.execute("""
        CREATE TABLE IF NOT EXISTS experiences (
            id INTEGER PRIMARY KEY,
            content TEXT,
            context_id TEXT,
            ttl DATETIME,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_experiences USING vec0(
            embedding float[768]
        )
    """)
    
    # 2. World Facts (Semantic Memory curated by LLM or KIs)
    db.execute("""
        CREATE TABLE IF NOT EXISTS world_facts (
            id INTEGER PRIMARY KEY,
            entity TEXT,
            fact TEXT,
            confidence_score REAL DEFAULT 1.0,
            importance INTEGER DEFAULT 1,
            source_url TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_world_facts USING vec0(
            embedding float[768]
        )
    """)

    # 3. Mental Models (Reflections, skills, pipelines)
    db.execute("""
        CREATE TABLE IF NOT EXISTS mental_models (
            id INTEGER PRIMARY KEY,
            topic TEXT,
            description TEXT,
            rule TEXT,
            success_count INTEGER DEFAULT 0,
            failure_count INTEGER DEFAULT 0,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_mental_models USING vec0(
            embedding float[768]
        )
    """)
    
    # 4. Swarm and GEPA tracking
    db.execute("""
        CREATE TABLE IF NOT EXISTS system_telemetry (
            metric_key TEXT PRIMARY KEY,
            metric_value INTEGER DEFAULT 0
        )
    """)
    db.execute("INSERT OR IGNORE INTO system_telemetry (metric_key, metric_value) VALUES ('swarm_active_nodes', 0)")
    db.execute("INSERT OR IGNORE INTO system_telemetry (metric_key, metric_value) VALUES ('swarm_completed_tasks', 0)")
    db.execute("INSERT OR IGNORE INTO system_telemetry (metric_key, metric_value) VALUES ('gepa_mutated_skills', 0)")
    db.execute("INSERT OR IGNORE INTO system_telemetry (metric_key, metric_value) VALUES ('gepa_mutated_kis', 0)")
    db.execute("INSERT OR IGNORE INTO system_telemetry (metric_key, metric_value) VALUES ('gepa_mutated_policies', 0)")
    db.execute("INSERT OR IGNORE INTO system_telemetry (metric_key, metric_value) VALUES ('gepa_mutated_workflows', 0)")
    db.execute("INSERT OR IGNORE INTO system_telemetry (metric_key, metric_value) VALUES ('gepa_failed_traces', 0)")

    # 5. Incremental processing tracker — prevents re-scanning unchanged files
    db.execute("""
        CREATE TABLE IF NOT EXISTS processed_files (
            file_path TEXT PRIMARY KEY,
            mtime REAL NOT NULL,
            processor TEXT NOT NULL DEFAULT 'dreamer',
            processed_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 6. Agent Taxonomy — dynamic, mutable agent type registry for swarm orchestrator
    db.execute("""
        CREATE TABLE IF NOT EXISTS agent_taxonomy (
            agent_type TEXT PRIMARY KEY,
            description TEXT NOT NULL,
            skills JSON NOT NULL DEFAULT '[]',
            model_tier TEXT NOT NULL DEFAULT 'utility',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 7. Wisdom Distillation (Higher-Order GEPA)
    # Task taxonomy registry
    db.execute("""
        CREATE TABLE IF NOT EXISTS task_taxonomy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_type TEXT UNIQUE NOT NULL,
            description TEXT,
            evaluation_dimensions TEXT,  -- JSON: [{name, weight, description}]
            success_threshold REAL DEFAULT 7.0,
            total_evaluations INTEGER DEFAULT 0,
            mean_quality_score REAL,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Individual task evaluations
    db.execute("""
        CREATE TABLE IF NOT EXISTS task_evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            walkthrough_path TEXT,
            task_type TEXT,
            user_request_summary TEXT,    -- What user actually wanted (higher-order intent)
            agent_output_summary TEXT,    -- What agent actually did
            alignment_gap TEXT,           -- Delta
            dimension_scores TEXT,        -- JSON: {dimension: score}
            overall_quality REAL,
            failure_root_causes TEXT,     -- JSON array
            success_patterns TEXT,        -- JSON array
            retry_recommended BOOLEAN DEFAULT FALSE,
            evaluated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_type) REFERENCES task_taxonomy(task_type)
        )
    """)

    # Extracted evaluation rules
    db.execute("""
        CREATE TABLE IF NOT EXISTS evaluation_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_type TEXT,
            rule_text TEXT NOT NULL,
            test_condition TEXT,
            component TEXT,
            target_name TEXT,
            failure_consequence TEXT,
            priority INTEGER DEFAULT 5,
            validation_count INTEGER DEFAULT 0,  -- Times this rule was validated by retry
            success_count INTEGER DEFAULT 0,
            failure_count INTEGER DEFAULT 0,
            promoted_to_gtb BOOLEAN DEFAULT FALSE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Golden Test Battery
    db.execute("""
        CREATE TABLE IF NOT EXISTS golden_test_battery (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_type TEXT NOT NULL,
            test_name TEXT NOT NULL,
            input_prompt TEXT NOT NULL,
            expected_behavior TEXT NOT NULL,
            evaluation_rubric TEXT NOT NULL,
            min_score REAL DEFAULT 7.0,
            success_count INTEGER DEFAULT 0,
            failure_count INTEGER DEFAULT 0,
            source_rule_id INTEGER,  -- Which evaluation_rule spawned this
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_rule_id) REFERENCES evaluation_rules(id)
        )
    """)

    # 8. Swarm Job tracking (Async Delegation + Self-Healing)
    db.execute("""
        CREATE TABLE IF NOT EXISTS swarm_jobs (
            id TEXT PRIMARY KEY,
            agent_role TEXT NOT NULL,
            task TEXT NOT NULL,
            working_dir TEXT,
            status TEXT NOT NULL DEFAULT 'dispatched',
            -- dispatched | running | healing | completed | failed_permanent
            pid INTEGER,
            result TEXT,
            log_path TEXT,
            retry_count INTEGER DEFAULT 0,
            last_error TEXT,
            healing_history TEXT,
            tokens_input INTEGER DEFAULT 0,
            tokens_output INTEGER DEFAULT 0,
            model_used TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            completed_at DATETIME,
            healed_at DATETIME
        )
    """)

    # Migration: add new columns to existing swarm_jobs tables
    _swarm_migration_cols = [
        ("retry_count", "INTEGER DEFAULT 0"),
        ("last_error", "TEXT"),
        ("healing_history", "TEXT"),
        ("tokens_input", "INTEGER DEFAULT 0"),
        ("tokens_output", "INTEGER DEFAULT 0"),
        ("model_used", "TEXT"),
        ("healed_at", "DATETIME"),
    ]
    for col_name, col_type in _swarm_migration_cols:
        try:
            db.execute(f"ALTER TABLE swarm_jobs ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Migration: add distilled_at column to world_facts for Knowledge Distiller tracking
    # This replaces the old pattern of overwriting source_url with 'distilled://' prefixes.
    try:
        db.execute("ALTER TABLE world_facts ADD COLUMN distilled_at DATETIME")
    except sqlite3.OperationalError:
        pass  # Column already exists

    # 9. Dream Cycle Memory Hygiene tracking tables
    # Immutable audit trail
    db.execute("""
        CREATE TABLE IF NOT EXISTS dream_audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            target_type TEXT NOT NULL,
            target_id INTEGER,
            target_path TEXT,
            reason TEXT NOT NULL,
            agent_job_id TEXT,
            llm_confidence REAL,
            anchor_evidence TEXT,
            conflict_group_id TEXT,
            winning_fact_id INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            reversed_at DATETIME
        )
    """)

    # Snapshot table for in-flight conflict resolution
    db.execute("""
        CREATE TABLE IF NOT EXISTS conflict_resolution_jobs (
            id TEXT PRIMARY KEY,
            fact_ids TEXT NOT NULL,
            fact_texts TEXT NOT NULL,
            conflict_type TEXT NOT NULL,
            entity TEXT,
            status TEXT DEFAULT 'pending',
            dispatched_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolved_at DATETIME,
            swarm_job_id TEXT
        )
    """)

    # 10. Universal Mission Queue (UMQ) — all agent work funnels through here
    db.execute("""
        CREATE TABLE IF NOT EXISTS orchestrator_missions (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            caller_job_id TEXT,
            mission_type TEXT NOT NULL,
            category_id TEXT,
            payload TEXT NOT NULL,
            priority INTEGER DEFAULT 2,
            status TEXT DEFAULT 'pending',
            cycle_id TEXT,
            session_context TEXT,
            result_summary TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            started_at DATETIME,
            completed_at DATETIME
        )
    """)

    # 11. Orchestrator Cycles — tracks full dream cycles with pause/resume/cancel
    db.execute("""
        CREATE TABLE IF NOT EXISTS orchestrator_cycles (
            id TEXT PRIMARY KEY,
            triggered_by TEXT NOT NULL,
            status TEXT DEFAULT 'running',
            current_category TEXT,
            completed_categories TEXT DEFAULT '[]',
            quota_used TEXT DEFAULT '{}',
            audit_trail TEXT DEFAULT '[]',
            session_context_snapshot TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            paused_at DATETIME,
            completed_at DATETIME
        )
    """)

    # 10. Native SQLite Graph Layer
    db.execute("""
        CREATE TABLE IF NOT EXISTS memory_edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_type TEXT NOT NULL,
            source_id INTEGER NOT NULL,
            target_type TEXT NOT NULL,
            target_id INTEGER NOT NULL,
            relation_type TEXT NOT NULL,
            weight REAL DEFAULT 1.0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(source_type, source_id, target_type, target_id, relation_type)
        )
    """)
    db.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON memory_edges(source_type, source_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON memory_edges(target_type, target_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_edges_relation ON memory_edges(relation_type)")

    # Migrations for Memory Hygiene Engine soft-deletion columns
    _hygiene_migration_cols = [
        ("world_facts", "is_archived", "BOOLEAN DEFAULT FALSE"),
        ("world_facts", "archived_at", "DATETIME"),
        ("world_facts", "conflict_group_id", "TEXT"),
        ("world_facts", "reflected_at", "DATETIME"),
        ("experiences", "is_archived", "BOOLEAN DEFAULT FALSE"),
        ("experiences", "archived_at", "DATETIME"),
        ("mental_models", "is_archived", "BOOLEAN DEFAULT FALSE"),
        ("mental_models", "archived_at", "DATETIME"),
    ]
    for table_name, col_name, col_type in _hygiene_migration_cols:
        try:
            db.execute(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_type}")
        except sqlite3.OperationalError:
            pass  # Column already exists

    db.commit()
    db.close()

def get_db():
    db = sqlite3.connect(DB_PATH)
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    db.enable_load_extension(False)
    db.row_factory = sqlite3.Row
    return db
