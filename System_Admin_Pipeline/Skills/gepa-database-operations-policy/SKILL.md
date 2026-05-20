---
name: gepa-database-operations-policy
---
# GEPA-Rule-DB-001: DB operations must be atomic, secure, and resilient.
Manage connections via `with` blocks. Use parameterized placeholders. Catch specific DB exceptions. Use exponential backoff.
## 20 edge cases:
1. Pool Exhaustion: limit explicitly.
2. Network Drops: retry with backoff.
3. Lock Contention: WAL mode.
4. Orphaned Tx: `with` context.
5. Stale Connections: validate liveness.
6. Deadlocks: deterministic locks.
7. OOM: `fetchmany()`.
8. Truncation: validate bounds.
9. Timezones: use UTC.
10. Schema Drift: migrate on startup.
11. Unindexed: index columns.
12. Encoding: UTF-8.
13. Leaks: context managers.
14. Corrupt DB: verify/backup.
15. Hangs: query timeouts.
16. Disk Space: monitor/archive.
17. Binding: cast types.
18. Threads: local connections.
19. Throttling: 429 backoff.
20. Zombies: keepalive/limits.
