# AROS Dashboard Debugging & Code Review Strategy

*This Mental Model / Knowledge Item documents the heuristic patterns learned from deeply debugging the Antigravity Research OS (AROS) backend telemetry rendering systems.*

When building agents or resolving bugs within the AROS Control Center or the Swarm orchestrator, future system instances must adhere strictly to these diagnostic frameworks.

## 1. The Cache-Busting Imperative
**Symptom:** UI elements (like Swarm traces or Memory graphs) appear unresponsive, missing, or stalled despite successful backend logs. 
**Diagnosis:** The dashboard utilizes JavaScript logic (e.g., `app.js`) to parse `GET /api/` payloads. If the logic is updated but the frontend HTML (`index.html`) still points to `app.js` without a version bump, browsers will silently mount cached code. If the cached JSON parser encounters completely new DOM elements or newly exposed API endpoints, silent DOM exceptions occur and parsing stalls immediately.
**Heuristic Solution:**
- Always increment the cache-buster on script tags in `index.html` (e.g., `<script src="/static/js/app.js?v=2.x"></script>`) whenever updating `app.js` metrics consumption.
- If UI is broken, immediately use `curl` to separate backend functionality from frontend caching.

## 2. API Telemetry Mismatch (Silent Fails)
**Symptom:** Specific metrics on the AROS Control Center report `0`, despite database queries displaying correct values via CLI.
**Diagnosis:** AROS FastAPI endpoints (`main.py`) aggressively swallow SQLite exceptions during metric pooling to prevent complete dashboard crashes (e.g., `sqlite3.OperationalError` catch blocks).
**Heuristic Solution:**
- Never assume a table exists explicitly as named without checking. Use `PRAGMA table_info(name)` or `SELECT name FROM sqlite_master WHERE type='table'`.
- Ensure column mapping aligns strictly with schema. For instance, Swarm telemetry sits in `system_telemetry` governed by `metric_key` and `metric_value` combinations, whereas Memory elements like `agent_taxonomy` and `mental_models` exist as distinct tables and must be `COUNT(*)` tracked.

## 3. Swarm Orchestrator State Injection
**Symptom:** The AROS dashboard UI displays static Agent or Task metrics while terminal logs show agents actively spawning and completing tasks.
**Diagnosis:** Logging locally to `stdout` does not inject telemetry into the `brain.db` `system_telemetry` table. The Control Center strictly maps UI layout off `brain.db`.
**Heuristic Solution:**
- Explicit physical insertion hooks must be included within orchestrator DAG loops.
- E.g., Use SQL `INSERT INTO system_telemetry (metric_key, metric_value) VALUES (?, ?) ON CONFLICT ...` dynamically inside `orchestrator.py:execute_task()` to track the `active_nodes` and `completed_tasks`.

## Summary Application 
When reviewing future AROS architectures or diagnosing dashboard failure, ensure that **Backend States -> SQLite Persistency -> Zero-Cache Frontend Fetch** sequence is tightly bound. Any break in this chain manifests as a ghosted/stalled UI, not necessarily a failed background computational process.

## 4. Cumulative SUM() Pattern for Background Task Stats (v2.7)
**Symptom:** Dashboard stat cards reset to 0 after page refresh, despite successful runs.
**Root Cause:** The original API read stats from the **last run row only**. When the most recent run finds 0 new items (all already processed), the dashboard overwrites good values with zeros.
**Pattern:**
- **Backend:** Use `COALESCE(SUM(column), 0)` across ALL rows in `distiller_runs` / `hygiene_runs`, then return `cumulative_*` fields.
- **Frontend:** Read `data.cumulative_clusters` (not `data.last_run.clusters_found`).
- **Status pill:** Remains driven by `last_run.status` for live feedback (COMPLETED / RUNNING / IDLE).
- **Applies to:** Knowledge Distiller, Dream Hygiene Engine, and any future background-task panels.

## 5. System Daemon Log Noise Filter (v2.7)
**Symptom:** The System Daemon Trace Output panel scrolls constantly with `GET /api/... 200 OK` lines, drowning out real events.
**Root Cause:** Dashboard polls ~10 endpoints every 2–5 seconds. Uvicorn logs every request to the systemd journal. The trace panel reads the same journal.
**Fix:** Server-side filter in `GET /api/logs` strips routine polling `GET 200 OK` lines for known endpoints. The `_POLLING_ENDPOINTS` set must be updated when new pollers are added.

## 6. Orphaned Background Run Recovery (v2.8)
**Symptom:** Dashboard panels (Hygiene Engine, Knowledge Distiller) show `RUNNING` status with all counters at 0, even though the underlying subprocess completed hours ago.
**Root Cause:** Finalization callbacks (`_finalize_hygiene_run`, `_finalize_distiller_run`) execute in daemon watcher threads. When the `antigravity-os.service` restarts (e.g., `systemctl restart`), these threads are killed instantly without executing the callback, leaving permanently orphaned `status = 'running'` rows in `hygiene_runs` / `distiller_runs`.
**Fix:** A **Startup Reaper** in the `lifespan()` boot sequence:
1. Queries for rows stuck in `'running'` state.
2. For hygiene runs: attempts to recover the report by re-parsing the log file via `_finalize_hygiene_run()`.
3. For any remaining stuck rows: marks them as `'interrupted'`.
4. PID-checks all active `swarm_jobs` and reaps dead processes.
**Diagnostic:** When encountering this pattern, first check `swarm_jobs` table (`status = 'completed'`) — if the job ID matches the orphaned run, the work DID complete. The display issue is purely a tracking table desync.
