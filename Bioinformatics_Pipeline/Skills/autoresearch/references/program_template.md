# Autoresearch: Generalized `program.md` Template

> Adapt this template for any domain. Replace `{PLACEHOLDERS}` with your experiment-specific values.

---

# autoresearch

This is an autonomous experiment loop for optimizing {DOMAIN_DESCRIPTION}.

## Setup

To set up a new experiment, work with the user to:

1. **Agree on a run tag**: propose a tag based on today's date (e.g., `mar30`). The branch `autoresearch/{tag}` must not already exist.
2. **Create the branch**: `git checkout -b autoresearch/{tag}` from current main.
3. **Read the in-scope files**:
   - `README.md` — repository context
   - `{IMMUTABLE_FILES}` — fixed evaluation, data loading. **Do not modify.**
   - `{MUTABLE_FILES}` — the file(s) you modify. Everything is fair game.
4. **Verify data exists**: Check that `{DATA_PATH}` contains the required datasets.
5. **Initialize results.tsv**: Create with header row only.
6. **Run baseline**: First run is always the unmodified code.
7. **Confirm and go**.

## Experimentation

Each experiment runs with a **fixed budget of {TIME_BUDGET}** (wall clock).

**What you CAN do:**
- Modify `{MUTABLE_FILES}` — everything is fair game: {WHAT_CAN_CHANGE}

**What you CANNOT do:**
- Modify `{IMMUTABLE_FILES}`. They are read-only.
- Install new packages or add dependencies.
- Modify the evaluation harness.

**The goal: get the {BEST_DIRECTION} {METRIC_NAME}.**

**Simplicity criterion**: All else being equal, simpler is better. A small improvement that adds ugly complexity is not worth it. Removing something and getting equal or better results is a great outcome.

## Output format

Once the script finishes it prints a summary like this:

```
---
{METRIC_NAME}:    {EXAMPLE_VALUE}
wall_time_sec:    {EXAMPLE_TIME}
{ADDITIONAL_METRICS}
```

Extract the key metric:
```bash
grep "^{METRIC_NAME}:" run.log
```

## Logging results

Log each experiment to `results.tsv` (tab-separated):

```
commit	{METRIC_NAME}	{SECONDARY_METRIC}	status	description
```

- git commit hash (short, 7 chars)
- {METRIC_NAME} achieved — use 0.000000 for crashes
- {SECONDARY_METRIC} — use 0.0 for crashes
- status: `keep`, `discard`, or `crash`
- short text description

## Sanity checks

Before accepting a result, verify:

{SANITY_CHECKS}

## The experiment loop

LOOP FOREVER:

1. Look at the git state: current branch/commit
2. Edit `{MUTABLE_FILES}` with an experimental idea
3. git commit
4. Run: `{RUN_COMMAND} > run.log 2>&1`
5. Read results: `grep "^{METRIC_NAME}:" run.log`
6. If grep is empty → run crashed. `tail -n 50 run.log` to debug.
7. Record in results.tsv
8. If {METRIC_NAME} improved ({BEST_DIRECTION}), keep the commit
9. If {METRIC_NAME} equal or worse, `git reset --hard HEAD~1`

**Timeout**: If a run exceeds {TIMEOUT}, kill it and treat as failure.

**Crashes**: Fix simple bugs (typo, import). If fundamentally broken, log "crash" and move on.

**NEVER STOP**: Do NOT pause to ask the human. The human might be asleep. Continue working indefinitely until manually stopped. If you run out of ideas, think harder — re-read code, try combining near-misses, try radical changes.

---

## Quick Reference: Placeholder Values

| Placeholder | Description | Example |
|---|---|---|
| `{DOMAIN_DESCRIPTION}` | What you're optimizing | "drug response prediction model" |
| `{MUTABLE_FILES}` | Files the agent edits | "model.py, config.py" |
| `{IMMUTABLE_FILES}` | Read-only files | "evaluate.py, data.py, gate.sh" |
| `{METRIC_NAME}` | Primary optimization target | "val_auc", "dice_score", "c_index" |
| `{BEST_DIRECTION}` | "lowest" or "highest" | "highest" |
| `{TIME_BUDGET}` | Per-experiment time limit | "5 minutes", "10 minutes" |
| `{TIMEOUT}` | Kill threshold | "2x time budget" |
| `{RUN_COMMAND}` | How to run one experiment | "python train.py", "uv run train.py" |
| `{DATA_PATH}` | Where datasets live | "data/", "~/.cache/autoresearch/" |
| `{WHAT_CAN_CHANGE}` | Scope of modifications | "model architecture, hyperparameters, features" |
| `{SANITY_CHECKS}` | Domain-specific output validation | See anti_gaming.md |
| `{SECONDARY_METRIC}` | Extra tracked metric | "peak_vram_mb", "train_time_sec" |
| `{ADDITIONAL_METRICS}` | Extra output fields | "calibration: 0.95\nfairness: 0.88" |
