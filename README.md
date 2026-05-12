# AROS Pipeline Factory

## Executive Summary
This repository serves as the central hub for AROS (Antigravity Research OS) automated pipelines. It houses the `Grant_Write_Pipeline`, `KAKENHI_Pipeline`, `Manuscript_Write_Pipeline`, and `workspace_management` module, along with their associated skills, policies, and knowledge items (KIs). It is an infrastructural project designed to enable multi-agent workflows for scientific writing and grant management.

> **⚠️ Agent Warning (Asset Forging Constraints)**: This repository is a Factory for forging AROS assets. Before modifying any Skill, Policy, KI, or Workflow, you MUST read `AGENTS.md` and `SPEC.md` to understand the CPCP constraints, SAMS audit rules, known failure modes (e.g., LaTeX truncation), and directory-structure requirements.

## 🧠 Project Philosophy: Embodiment & Co-Evolution

The AROS Pipeline Factory is grounded in a fundamental distinction between artificial and biological intelligence—specifically, the concept of **embodiment and environmental coupling**—which necessitates a future of **human-AI co-evolution** rather than replacement.

### 1. The Embodiment Gap

A computer algorithm, on its own, cannot generate true randomness. Software relies on Pseudo-Random Number Generators (PRNGs)—deterministic mathematical formulas that merely simulate stochasticity. While modern hardware *can* harvest entropy from physical phenomena (thermal noise, quantum decay), it must be deliberately engineered to do so. A carbon-based organism, by contrast, is *natively* immersed in thermodynamic stochasticity at every scale.

Each cell of our body contains massive, exquisitely sensitive chemical reaction chains—protein folding, ion channel gating, mechanotransduction—that operate under **deterministic chaos with extreme sensitivity to initial conditions**. Unlike an AI that processes the world in discrete, digitized, and compressed steps (tokens, pixels, rigid clock cycles), biological intelligence operates in a **continuous analog flow**. Our bodies do not merely house our brains; they *are* part of the computing apparatus. This chemical sensitivity smoothly and continuously shapes our behavior and our thoughts in ways that no discretized digital system can replicate.

Because carbon-based life is intimately coupled with the infinite resolution of the physical world, evolution acts as an optimizer that exploits every possible energetic and chemical niche. In the natural ecosystems of Earth, almost all survival strategies are present—occupying almost every conceivable combination of ecological niche. An AI running in a vacuum on a server rack has no continuous physical environment to adapt to, no thermodynamics to balance, and no evolutionary pressure to optimize its physical existence. It knows only the digitized abstractions of reality we feed it.

This **embodiment gap** dictates that AI serves as a powerful pattern-matching engine to augment—not replace—the incredibly complex, chemically embedded intelligence of the human researcher.

### 2. Evidence from Frontier Biology

Recent scientific discoveries continue to reveal how deeply biological intelligence is embedded in the physical world—capabilities that remain fundamentally beyond the reach of disembodied AI systems:

- **Remote Touch ("Seventh Sense")**: Research published in 2025 by Queen Mary University of London and UCL demonstrated that humans possess a previously unrecognized sensory ability: **remote touch**—the ability to detect buried objects through granular material without direct physical contact, much like sandpipers sensing prey through sand ([Hammoud et al., IEEE ICDL 2025](https://www.qmul.ac.uk/news/latest-news/2025/science-and-engineering/se/research-first-to-show-humans-have-remote-touch-seventh-sense-like-sandpipers.html)). Human participants achieved ~70.7% precision, approaching the theoretical physical threshold for detecting mechanical reflections. A robotic tactile sensor trained with machine learning on the same task achieved only ~40% precision with far more false positives. Our biological hardware detects physical signals that engineered sensors struggle to match.

- **Stochastic Resonance in Biological Neurons**: Neurons exploit a phenomenon called **stochastic resonance**, where background neural noise *enhances* the detection of weak, subthreshold signals that would otherwise be missed. Evolution has tuned our neural circuits to leverage thermodynamic noise as a feature, not a bug—allowing organisms to detect faint environmental cues (vibrations, electrical fields, chemical gradients) critical for survival. While engineers can deliberately introduce controlled noise into digital systems to mimic this effect, biological nervous systems perform it natively and continuously across billions of synapses in parallel.

- **The Gut-Brain Axis and Interoception**: A 2025 discovery identified a "neurobiotic sense"—specialized **neuropod** cells in the gut that detect microbial proteins (such as flagellin) and send real-time signals to the brain, directly influencing appetite, mood, and decision-making. Recent research further demonstrates that interoceptive signals (cardiorespiratory, gastric) directly influence neural state transitions during perceptual decision-making, providing a mechanistic basis for Antonio Damasio's **Somatic Marker Hypothesis**. Our "gut feelings" are not metaphors—they are measurable biological computations that fundamentally shape cognition.

- **Thermodynamic Efficiency**: Research in biophysics has shown that biological systems operate remarkably close to **Landauer's theoretical limit**—the minimum thermodynamic energy cost for information processing. Processes like protein translation outperform modern supercomputers by several orders of magnitude in free energy expended per operation. Even simulating the full molecular kinetics of a single *Mycoplasma genitalium* bacterium (~500 proteins) during its doubling time remains a massive undertaking for our most powerful computers.

These findings collectively demonstrate that biological intelligence is not a mere algorithm running on organic hardware. It is an emergent property of deep, continuous physical coupling with the thermodynamic reality of the universe—a coupling that no digital system currently possesses.

### 3. Cognitive Decomposition & Co-Evolution

Because of this fundamental embodiment gap, carbon-based and silicon-based intelligences are destined to operate in a state of **synergistic co-evolution** for the foreseeable future.

Since AI became capable of fluently handling the majority of routine cognitive labor, the most effective researchers and professionals have undergone a profound shift: they have learned to deeply introspect and **decompose their daily intellectual activities** into discrete, hierarchical tiers. Never before in human history have we been compelled to examine, break down, and categorize our own cognitive processes with such depth, breadth, and scale. By doing so, we can effectively route different levels of intellectual labor to the appropriate tier of AI compute or human oversight.

This is the core mission of the **AROS Project**: to provide an ecosystem that helps humans meticulously examine, decompose, and precisely describe their cognitive workflows through continuous interaction with AI agents. AROS captures human feedback, corrections, and decision-making logic at every step—enabling the system's prompts, policies, and skills to **continuously self-evolve**.

The principle is simple but profound: **as long as we can successfully decompose our complex, embodied intelligence into highly detailed, step-by-step cognitive maps, we can outsource the execution of that decomposed intelligence to AI systems.** The intelligence that *generates* the decomposition—the embodied, thermodynamically coupled, analog human mind—remains irreplaceable. The execution of the decomposed steps is where AI excels.

## 🔒 Shared Asset Governance (SUPREME RULE)

Multiple pipelines in this factory share KIs, Skills, Policies, and Workflows. The **Cross-Pipeline Compatibility Protocol (CPCP)** — defined in `AGENTS.md` as LAW 0 — ensures that any modification to a shared asset is evaluated, tested, and validated across ALL consuming pipelines before being committed.

📄 **Central Registry**: [`00.RawData/SHARED_ASSET_REGISTRY.md`](00.RawData/SHARED_ASSET_REGISTRY.md)

This registry must be consulted before modifying any shared asset. If a modification creates an unresolvable conflict between pipelines, a new pipeline-specific variant must be forked rather than overwriting the shared original.

## ⚠️ Architecture Constraints
**Cross-Platform Enabled (SAMS v1.1)**: This repository does not rely on POSIX symlinks. It is fully operable on Linux, macOS, and Windows. Do not re-introduce symlinks or platform-specific directory references.

## Chronological Timeline
- **[verified] 2026-05-11 01:24**: KAKENHI pipeline KIs (e.g., e_application_system PDFs, forms) initialized.
- **[verified] 2026-05-11 18:15**: Grant_Write_Pipeline skills requirements and assets initialized.
- **[verified] 2026-05-11 18:29**: Manuscript_Write_Pipeline assets and scripts established.
- **[verified] 2026-05-11 18:44**: Shared Asset Registry and CPCP governance established.
- **[verified] 2026-05-11 19:00**: Centralized Shared Asset Management System (SAMS) implemented with direct referencing and programmatic audit tools.
- **[verified] 2026-05-11 21:00**: Dual-VCS architecture (Git + re_gent) deployed for AI agent auditability.
- **[verified] 2026-05-11 22:00**: Replaced legacy `INDEX.csv` with `PIPELINE_REGISTRY.md`. Generalized all workflow templates for dynamic registry discovery.

## Hypothesis Evolution Table
| Phase | Hypothesis |
|-------|------------|
| H1 | Developing modular pipelines and agents for different writing tasks (grants, manuscripts, KAKENHI) significantly streamlines the academic drafting and submission process. |
| H2 | Shared assets across pipelines (KIs, policies, workflows) must be governed by a central registry and compatibility protocol to prevent cross-pipeline regressions. |

## Repository Structure Map
```
.
├── 00.RawData/                  # Central registry and experiment indices
│   ├── PIPELINE_REGISTRY.md    #   Pipeline catalog (replaced INDEX.csv)
│   ├── SHARED_ASSET_REGISTRY.md #   ⚠️ SUPREME: Cross-pipeline shared asset registry
│   └── Literature/              #   Standardized literature storage (PDFs, Markdown, metadata)
├── 01.Shared_Assets/            # Canonical repository for shared KIs, Policies, Skills, Scripts
│   ├── KIs/                     #   agentic_manuscript_publishing, markdown_first_manuscript_policy
│   ├── Policies/                #   gepa_protocol, output-truncation-management
│   ├── Skills/                  #   literature-ingestion (tiered PDF retrieval + conversion)
│   └── Scripts/                 #   Factory-level infrastructure tools (audit_shared_assets.py)
├── Grant_Write_Pipeline/        # Universal Scientific Grant Writing
│   ├── KIs/                     #   grant_funder_profiles
│   ├── Policies/                #   (references 01.Shared_Assets)
│   ├── Skills/                  #   18 skills (grant-mock-reviewer, medical-translation, etc.)
│   └── Workflows/               #   grant-write.md
├── KAKENHI_Pipeline/            # KAKENHI-specific reporting and management
│   ├── KIs/                     #   kakenhi_e_application_system, kakenhi_report_forms, etc.
│   ├── Policies/                #   fact_check_policy, grant_report_policy
│   ├── Skills/                  #   3 skills (kakenhi-form-completion, etc.)
│   └── Workflows/               #   kakenhi-annual-report.md
├── Manuscript_Write_Pipeline/   # Dual-agent manuscript drafting tools
│   ├── KIs/                     #   agentic_manuscript_publishing, markdown_first_manuscript_policy
│   ├── Policies/                #   (none yet)
│   ├── Skills/                  #   16 skills (peer-review, statistical-analysis, etc.)
│   └── Workflows/               #   manuscript-write.md
├── workspace_management/        # Cross-pipeline infrastructure
│   ├── KIs/                     #   AROS architecture references
│   ├── Skills/                  #   workflow-authoring, super-scientist
│   └── Workflows/               #   lab-commit, lab-reorganize, wiki-*, literature-ingest, etc.
├── .wiki/                       # LLM-Wiki knowledge base
├── AGENTS.md                    # Agent operational rules (includes CPCP as LAW 0)
├── SPEC.md                      # Architectural specification
└── README.md                    # This document
```

## Key Parameters
- **Scope**: Automation of scientific drafting and management tasks.
- **Components**: KIs, Skills, Policies, Workflows.
- **Governance**: Cross-Pipeline Compatibility Protocol (CPCP) via `SHARED_ASSET_REGISTRY.md`.

## Critical Notes and Caveats
- This repository is primarily code and templates, rather than raw biological data.
- Do not mix raw data directly into the Pipeline templates.
- **Any modification to shared assets MUST follow the CPCP** (see `AGENTS.md` LAW 0).

## Methods and Tools Inventory
- **Python / Scripts**: Included in the `scripts/` subdirectories of skills.
- **Knowledge Items**: Embedded in `KIs/` to support domain-specific intelligence.
- **Shared Asset Registry**: `00.RawData/SHARED_ASSET_REGISTRY.md` — the authoritative cross-pipeline dependency tracker.

