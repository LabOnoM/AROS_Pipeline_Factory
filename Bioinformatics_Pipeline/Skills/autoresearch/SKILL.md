---
name: autoresearch
description: Autonomous experiment loop for iterative optimization — the agent modifies one file, runs a fixed-budget experiment, evaluates, keeps or discards via git, and loops forever. Adapted from Karpathy's autoresearch with anti-gaming safeguards and biomedical domain support. Use when the user wants autonomous iterative experiments, autoresearch-style optimization loops, overnight ML training, autonomous hyperparameter search, automated pipeline optimization, or mentions "autoresearch", "experiment loop", "autonomous research", "overnight experiments", or wants to optimize a metric by iterating on code autonomously.
---

# Autoresearch: Autonomous Experiment Loop

> Inspired by [karpathy/autoresearch](https://github.com/karpathy/autoresearch) and informed by [awesome-autoresearch](https://github.com/WecoAI/awesome-autoresearch) real-world cases.

## Overview

Autoresearch is a pattern where an AI agent autonomously iterates on code to optimize a metric. The agent:

1. **Modifies** one or more mutable files
2. **Runs** a fixed-budget experiment
3. **Evaluates** against an immutable metric
4. **Keeps** (git commit) or **discards** (git reset) the change
5. **Logs** results to a TSV file
6. **Repeats** forever until interrupted

This pattern works for any domain with measurable outputs — not just LLM training. Real-world applications include GPU kernel optimization, XGBoost tabular models, earth system models, RL agents, and biomedical pipelines.

## The Universal Loop

```
LOOP FOREVER:
  1. Read current state (git branch, previous results)
  2. Propose ONE bounded change to the mutable file(s)
  3. git commit -m "description of change"
  4. Run experiment: {RUN_COMMAND} > run.log 2>&1
  5. Extract results: grep key metrics from run.log
  6. Handle Failures and Crashes: If the experiment command returns a non-zero exit code or fails to produce the expected output file (`run.log`), initiate the failure recovery protocol:
      a. Read the traceback: Analyze `run.log` and `stderr` for keywords like "Error", "Exception", "Traceback", "failed".
      b. Classify the failure: Is it a transient issue (e.g., network timeout, resource unavailable) or a code issue (e.g., `SyntaxError`, `ModuleNotFoundError`, `CUDA out of memory`)?
      c. Attempt a fix:
          - For code issues, propose a targeted change to the mutable file(s) to fix the error. For example, add a missing import, correct syntax, or wrap a call in a `try...except` block.
          - For resource issues like OOM, try reducing a relevant parameter (e.g., `batch_size`) in the configuration.
      d. If a fix is attempted, re-run the experiment. If it succeeds, continue the main loop.
      e. If the fix fails or no fix is possible: Log the status as "crash" along with the truncated traceback in `results.tsv`, discard the change (`git reset --hard HEAD~1`), and proceed to the next iteration. This prevents the agent from getting stuck on an un-fixable error.
  7. Log to results.tsv (commit, metric, memory, status, description)
  8. If metric improved → KEEP (advance branch)
  9. If metric equal/worse → DISCARD (git reset --hard HEAD~1)
  10. NEVER STOP — keep going until manually interrupted
```

## Setup Protocol

Before entering the loop:

1. **Agree on a run tag** (e.g., `mar30-biomedical`) — branch must not exist
2. **Create branch**: `git checkout -b autoresearch/{tag}`
3. **Read all in-scope files** for full context
4. **Verify data exists** (datasets, tokenizers, preprocessed data)
5. **Initialize results.tsv** with header row only
6. **Run baseline** — first experiment is always the unmodified code
7. **Confirm** setup looks good, then enter the loop

## File Architecture

Every autoresearch project has this structure:

| File | Role | Mutable? |
|------|------|----------|
| `program.md` | Agent instructions ("the skill") | Human-edited |
| Mutable file(s) | What the agent modifies (model, config, pipeline) | ✅ Agent-edited |
| Evaluation file(s) | Metric computation, data loading | ❌ **IMMUTABLE** |
| `gate.sh` | Pre-acceptance validation script | ❌ **IMMUTABLE |
