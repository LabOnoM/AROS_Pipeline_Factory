---
name: hypothesis-generation
description: Structured scientific hypothesis formulation from observations; use when you have experimental observations or preliminary data and need testable hypotheses with predictions, mechanisms, and validation experiments. Mandatory AI-generated schematics.
license: MIT
skill-author: AIPOCH
---
# Hypothesis Generation (Scientific)

## Overview

This skill facilitates structured scientific hypothesis formulation from observations or preliminary data. It helps you develop testable hypotheses with clear predictions, underlying mechanisms, and validation experiments. The output is a publication-ready LaTeX report. Every report must include AI-generated schematics.

## When to Use

- When you need to turn observations into **testable, mechanistic hypotheses** and a **validation plan**.
- When you have experimental observations (e.g., an unexpected phenotype, trend, or anomaly) and need 3-5 competing explanations with clear mechanisms.
- When you have preliminary data and must propose **testable predictions** and **decisive experiments** to discriminate between hypotheses.
- When you are preparing a mechanistic study plan (molecular/cellular/system/population) and need a structured framework for causal reasoning.
- When you are doing literature-grounded hypothesis development and want to identify gaps, contradictions, and plausible mechanisms.
- When you need a publication-ready hypothesis report (LaTeX) with a concise main text and a detailed appendix.

## Key Features

- **Scientific workflow**: observation framing → literature search → evidence synthesis → competing hypotheses → quality evaluation → experiments → predictions → structured report.
- **Competing hypotheses (3-5)**: distinct, mechanistic explanations at appropriate biological/physical scales.
- **Quality criteria**: testability, falsifiability, parsimony, explanatory power, scope, consistency, novelty (see `references/hypothesis_quality_criteria.md`).
- **Experiment design patterns**: lab, observational, clinical, computational; controls, confounders, and measurement plans (see `references/experimental_design_patterns.md`).
- **Prediction-first outputs**: quantitative/conditional predictions that differentiate hypotheses and specify falsifiers.
- **Report packaging**: LaTeX template with colored boxes and a strict main-body length budget (see `assets/hypothesis_report_template.tex`, `assets/hypothesis_generation.sty`, `assets/FORMATTING_GUIDE.md`).
- **Mandatory visuals**: every hypothesis report must include **at least 1-2 AI-generated schematics** created via the `scientific-schematics` skill.
- Scope-focused workflow aligned to: Structured scientific hypothesis formulation from observations; use when you have experimental observations or preliminary data and need testable hypotheses with predictions, mechanisms, and validation experiments.
- Documentation-first workflow with no packaged script requirement.