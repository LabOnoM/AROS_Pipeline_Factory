# AROS Curation Policy

**Version:** 1.0.0
**Last Evolved:** 2026-05-13

This document defines the rules, thresholds, and logic by which the AROS Skill Curator decides the lifecycle of ecosystem assets (Skills, KIs, Workflows). 
It is evolved by `policy_evolver.py` through LLM-as-a-judge review of historical performance.

## 1. Global Thresholds

These hard thresholds govern the immediate promotion, updating, or deletion of skills based on their Composite Reward (`comp_avg`) which is calculated as `(r_corr * 0.7) + (r_cnt * 0.3)`.

* **`delete_threshold`**: `0.50`
  * Action: `DELETE`
  * Rationale: If a skill's composite reward falls below 0.50, it is actively causing regressions, hallucinating, or failing to execute. It must be soft-deleted.
  
* **`update_threshold`**: `0.80`
  * Action: `UPDATE`
  * Rationale: If a skill's composite reward is between `delete_threshold` and `update_threshold`, it is useful but unstable. Trigger an update refinement cycle to improve abstraction or prompt clarity.

* **`preserve_threshold`**: `>= 0.80`
  * Action: `PRESERVE`
  * Rationale: The skill is highly reliable and performs as expected. Leave it untouched.

## 2. Policy Evolution Thresholds

Rules governing the promotion of a candidate version of this very document (`CURATION_POLICY.md`).

* **`composite_reward_improvement_threshold`**: `0.02` (2%)
  * Action: If shadow-mode testing of a proposed policy candidate yields a projected mean composite reward that is `> 0.02` better than the active policy across historical tasks, the candidate policy is automatically promoted to active.

## 3. Heuristic Rules (Pre-Evolution Baseline)

* **Rule 1 (Zero-Shot Failure):** Any skill that scores an `r_corr = 0.0` (task failure requiring a retry) on its very first usage receives an immediate penalty weight of 1.5x to its `r_cnt` deduction.
* **Rule 2 (Duplicate Pruning):** Any two skills with a semantic embedding cosine similarity `> 0.92` must be subjected to a forced A/B test or immediate manual merge via `batch_evolver.py`.

---
*Note: This file is dynamically parsed by `curator_service.py`. Minimal diffs altering thresholds must retain the `* **var_name**:` structure for safe regex extraction.*
