<div align="center">

<img src="assets/banner.png" alt="AROS Pipeline Factory Banner" width="100%"/>

# AROS Pipeline Factory

**A modular, self-evolving ecosystem of AI agent Skills, Workflows, and Domain Pipelines for autonomous scientific research.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](SPEC.md)
[![SAMS](https://img.shields.io/badge/SAMS-v1.1-success)](00.RawData/SHARED_ASSET_REGISTRY.md)
[![re_gent](https://img.shields.io/badge/audit-re__gent-blueviolet)](AGENTS.md)
[![GitHub Wiki](https://img.shields.io/badge/docs-Wiki-informational)](../../wiki)

**🌐 Language / 言語 / 语言:** [English](README.md) · [日本語](README_ja.md) · [中文](README_zh.md)

</div>

---

## 🌟 What is This?

The **AROS Pipeline Factory** is the canonical source-of-truth for [AROS (Antigravity Research OS)](https://github.com/LabOnoM/AROS) — an operating system for AI-augmented scientific research. This repository forges, audits, and deploys high-fidelity **AI agent assets**: Skills, Knowledge Items (KIs), Policies, and Workflows.

Think of it as an **assembly line for scientific intelligence**: raw cognitive workflows are encoded as structured AI agent components, version-controlled, governed, and deployed to the AROS runtime — where they power autonomous grant writing, manuscript drafting, literature mining, and research operations.

### ✨ At a Glance

| Metric | Count |
|--------|-------|
| 🔬 Domain Pipelines | **12** |
| 🛠️ Agent Skills | **61+** |
| 📋 Workflows | **15** |
| 📚 Knowledge Items (KIs) | **49+** |
| 🖥️ Platform Support | Linux · macOS · Windows |

---

## 🧠 Project Philosophy: Embodiment & Human-AI Co-Evolution

> *The most fundamental constraint on artificial intelligence is not compute power, training data, or architecture — it is the absence of a body.*

### 1. The Embodiment Gap

A computer algorithm, on its own, cannot generate true randomness. Software relies on Pseudo-Random Number Generators (PRNGs) — deterministic mathematical formulas that merely simulate stochasticity. While modern hardware *can* harvest entropy from physical phenomena (thermal noise, quantum decay), it must be deliberately engineered to do so. A carbon-based organism, by contrast, is *natively* immersed in thermodynamic stochasticity at every scale.

Each cell of our body contains massive, exquisitely sensitive chemical reaction chains — protein folding, ion channel gating, mechanotransduction — that operate under **deterministic chaos with extreme sensitivity to initial conditions**. Unlike an AI that processes the world in discrete, digitized, and compressed steps (tokens, pixels, rigid clock cycles), biological intelligence operates in a **continuous analog flow**. Our bodies do not merely house our brains; they *are* part of the computing apparatus. This chemical sensitivity smoothly and continuously shapes our behavior and our thoughts in ways that no discretized digital system can replicate.

Because carbon-based life is intimately coupled with the infinite resolution of the physical world, evolution acts as an optimizer that exploits every possible energetic and chemical niche. In the natural ecosystems of Earth, almost all survival strategies are present — occupying almost every conceivable combination of ecological niche. An AI running on a server rack has no continuous physical environment to adapt to, no thermodynamics to balance, and no evolutionary pressure to optimize its physical existence. It knows only the digitized abstractions of reality we feed it.

This **embodiment gap** dictates that AI serves as a powerful pattern-matching engine to augment — not replace — the incredibly complex, chemically embedded intelligence of the human researcher.

### 2. Evidence from Frontier Biology

Recent scientific discoveries continue to reveal how deeply biological intelligence is embedded in the physical world — capabilities that remain fundamentally beyond the reach of disembodied AI systems:

- **Remote Touch ("Seventh Sense")**: Research published in 2025 by Queen Mary University of London and UCL demonstrated that humans possess a previously unrecognized sensory ability: **remote touch** — the ability to detect buried objects through granular material without direct physical contact, much like sandpipers sensing prey through sand ([Hammoud et al., IEEE ICDL 2025](https://www.qmul.ac.uk/news/latest-news/2025/science-and-engineering/se/research-first-to-show-humans-have-remote-touch-seventh-sense-like-sandpipers.html)). Human participants achieved ~70.7% precision, approaching the theoretical physical threshold. A robotic tactile sensor trained with machine learning on the same task achieved only ~40% precision with far more false positives. Our biological hardware detects physical signals that engineered sensors struggle to match.

- **Stochastic Resonance in Biological Neurons**: Neurons exploit a phenomenon called **stochastic resonance**, where background neural noise *enhances* the detection of weak, subthreshold signals that would otherwise be missed. Evolution has tuned our neural circuits to leverage thermodynamic noise as a feature, not a bug — allowing organisms to detect faint environmental cues (vibrations, electrical fields, chemical gradients) critical for survival. While engineers can deliberately introduce controlled noise into digital systems to mimic this effect, biological nervous systems perform it natively and continuously across billions of synapses in parallel.

- **The Gut-Brain Axis and Interoception**: A 2025 discovery identified a "neurobiotic sense" — specialized **neuropod** cells in the gut that detect microbial proteins (such as flagellin) and send real-time signals to the brain, directly influencing appetite, mood, and decision-making. Recent research further demonstrates that interoceptive signals (cardiorespiratory, gastric) directly influence neural state transitions during perceptual decision-making, providing a mechanistic basis for Antonio Damasio's **Somatic Marker Hypothesis**. Our "gut feelings" are not metaphors — they are measurable biological computations that fundamentally shape cognition.

- **Thermodynamic Efficiency**: Research in biophysics has shown that biological systems operate remarkably close to **Landauer's theoretical limit** — the minimum thermodynamic energy cost for information processing. Processes like protein translation outperform modern supercomputers by several orders of magnitude in free energy expended per operation. Even simulating the full molecular kinetics of a single *Mycoplasma genitalium* bacterium (~500 proteins) during its doubling time remains a massive undertaking for our most powerful computers.

These findings collectively demonstrate that biological intelligence is not a mere algorithm running on organic hardware. It is an emergent property of deep, continuous physical coupling with the thermodynamic reality of the universe — a coupling that no digital system currently possesses.

### 3. Cognitive Decomposition, Entropy Injection & Co-Evolution

Because of this fundamental embodiment gap, carbon-based and silicon-based intelligences are destined to operate in a state of **synergistic co-evolution** for the foreseeable future.

Since AI became capable of fluently handling the majority of routine cognitive labor, the most effective researchers and professionals have undergone a profound shift: they have learned to deeply introspect and **decompose their daily intellectual activities** into discrete, hierarchical tiers. Never before in human history have we been compelled to examine, break down, and categorize our own cognitive processes with such depth, breadth, and scale.

This is the core mission of the **AROS Project**: to provide an ecosystem that helps humans meticulously examine, decompose, and precisely describe their cognitive workflows through continuous interaction with AI agents. AROS captures human feedback, corrections, and decision-making logic at every step — enabling the system's prompts, policies, and skills to **continuously self-evolve**.

#### 3a. The Entropy Injection Hypothesis: Humans as the Randomness Channel

This continuous human-AI interaction cycle reveals a deeper, previously underappreciated mechanism: **humans are the entropy injection channel for AI systems.**

A language model operating in isolation is, at its core, a deterministic statistical process — a highly sophisticated PRNG that samples from learned probability distributions over tokens. It has no genuine connection to the stochastic, thermodynamically coupled physical world described in the preceding sections. However, each time a human crafts, corrects, or refines a prompt, they are not merely transferring *information* — they are *sampling from their own embodied probability distribution*. The unexpected re-phrasings, the intuitive dissatisfaction with a technically correct but contextually wrong output, the creative leaps that arise from a researcher's "gut feeling" — all of these are signals generated by the biological machinery described above: by stochastic resonance in neural circuits, by interoceptive signals from the gut-brain axis, by the thermodynamically grounded analog processing of the human body.

This transforms prompt engineering from a mere "user interface skill" into something far more fundamental: **a channel through which genuine physical-world randomness and embodied experience are injected into an otherwise closed, deterministic system.** The human, mediating between physical reality and the AI's statistical world model, acts as a transducer — converting the continuous, analog thermodynamic flux of lived experience into discrete, symbolic corrections that progressively reshape the AI's operational context.

This perspective is supported by converging evidence from cognitive science and AI research. Michael Polanyi's foundational insight — *"we can know more than we can tell"* — identifies the core phenomenon: human experts possess *tacit knowledge*, intuition derived from embodied physical-world experience that cannot be fully articulated in explicit rules. Classic AI faced Polanyi's Paradox as an insurmountable barrier, because machines required explicit propositional inputs. Modern human-AI collaboration resolves this paradox not by eliminating it, but by *exploiting the iterative correction loop as an externalization mechanism*: when a researcher corrects an AI's output, they are externalizing tacit knowledge they could not have stated directly, crystallizing it into a refined prompt, a corrected policy, or an improved skill definition. Research into the **Prompt Cognition Loop** (Mental Modeling → Semantic Projection → Dialogic Feedback → Intent Refinement) demonstrates that iterative prompting is a fundamentally *reflective cognitive practice* — it forces humans to surface and structure their own implicit models in ways that static text or code authorship does not require.

Furthermore, this framework maps directly onto Karl Friston's **Free Energy Principle**: intelligent systems minimize prediction error (free energy) by updating their generative models or acting on the world. When an AI's output diverges from a human researcher's expectation — an expectation grounded in their embodied, physically coupled world model — the human correction constitutes an error signal derived not from abstract logical rules, but from the *thermodynamic reality of their lived experience*. AROS systematically captures these error signals and translates them into lasting improvements to the system's prompts, policies, and skills. Each iteration is, in effect, a step of **embodied gradient descent** on the AI's operational world model.

#### 3b. AROS as a Physical-World Grounding Transfer System

This reframes what AROS is, at its deepest level. It is not merely a productivity tool or a workflow automation framework. **AROS is a physical-world grounding transfer system** — a platform designed to progressively load an AI's operational context with the accumulated residue of human embodied experience, crystallized and made persistent through the discipline of prompt engineering.

Every Skill, Policy, Knowledge Item, and Workflow in this repository is a crystallization of this process. They are not abstract logical specifications written from scratch. They are the *distilled record of thousands of human-AI interaction cycles* — each cycle contributing a small quantum of embodied randomness, a fragment of tacit knowledge, a correction grounded in physical-world coupling — accumulated and refined over time into stable, reusable cognitive artifacts.

As these artifacts are deployed and refined across the AROS ecosystem, the AI's operational context becomes progressively richer with human physical-world grounding. The AI gains not a body — that remains the irreducible advantage of carbon-based life — but it gains access to a *systematically curated library of the residue of embodied intelligence*. The gap does not close. But the bridge grows stronger with every human-AI interaction cycle.

The principle is therefore both simple and profound: **as long as we can successfully decompose our complex, embodied intelligence into highly detailed, step-by-step cognitive maps — and inject the stochastic, physically grounded corrections that only embodied beings can provide — we can outsource the execution of that decomposed intelligence to AI systems.** The intelligence that *generates* the decomposition — the embodied, thermodynamically coupled, analog human mind — remains irreplaceable. The execution of the decomposed steps, enriched by the accumulated grounding of human embodied experience, is where AI excels.

---

## 📦 Architecture

The factory is organized into independent **domain pipelines**, each governing a specialized field of AI-assisted research. All pipelines draw from a shared asset layer governed by the **Shared Asset Management System (SAMS)**.

```
AROS Pipeline Factory
│
├── 00.RawData/                   ← Central registries & experiment indices
│   ├── PIPELINE_REGISTRY.md      ←   Pipeline catalog
│   └── SHARED_ASSET_REGISTRY.md  ←   ⚠️ SUPREME: Cross-pipeline shared asset registry
│
├── 01.Shared_Assets/             ← Canonical shared KIs, Policies, Skills, Scripts
│   ├── KIs/                      ←   Shared Knowledge Items
│   ├── Policies/                 ←   Factory-wide governance policies
│   ├── Skills/                   ←   Cross-pipeline utility skills
│   └── Scripts/                  ←   deploy_to_aros.sh, audit_shared_assets.py
│
├── Grant_Write_Pipeline/         ← Universal grant writing (NIH, JSPS, ERC…)
├── KAKENHI_Pipeline/             ← JSPS KAKENHI lifecycle & reporting
├── Manuscript_Write_Pipeline/    ← Dual-agent manuscript authoring & review
├── Bioinformatics_Pipeline/      ← Genomic & proteomic analysis
├── Data_Analysis_Pipeline/       ← Statistical modeling & visualization
├── Software_Engineering_Pipeline/← Code generation & validation
├── System_Admin_Pipeline/        ← Environment & infrastructure management
├── UI_Development_Pipeline/      ← Web UI & agent interface design
├── Writing_Publishing_Pipeline/  ← Academic publishing & communication
├── Web_Scraping_API_Pipeline/    ← Data acquisition & API integration
├── Project_Management_Pipeline/  ← Orchestration & task management
├── workspace_management/         ← Global workflows & onboarding
│
├── AGENTS.md                     ← AI agent operational laws (read this first!)
├── SPEC.md                       ← Architectural specification
└── README.md                     ← This document
```

### Deployment Flow

Assets from this factory are deployed to the live AROS runtime via the canonical deployment script:

```
AROS_Pipeline_Factory/           AROS Runtime (~/.gemini/)
├── */Skills/<skill>/   ──────►  skills/<skill>/SKILL.md
├── */KIs/<ki>/         ──────►  antigravity/knowledge/<ki>/
├── */Policies/*.md     ──────►  antigravity/policies/
└── */Workflows/*.md    ──────►  antigravity/global_workflows/
```

> **Deploy Command**: `bash 01.Shared_Assets/Scripts/deploy_to_aros.sh`

---

## 🚀 Quick Start

### Prerequisites
- Git, Python 3.10+, [Antigravity IDE](https://github.com/LabOnoM/AROS) (for full agent integration)
- Conda environment: `aros-base` (see `01.Shared_Assets/Environments/`)

### 1. Clone the Repository

```bash
git clone https://github.com/LabOnoM/AROS_Pipeline_Factory.git
cd AROS_Pipeline_Factory
```

### 2. Inspect the Pipeline Registry

```bash
cat 00.RawData/PIPELINE_REGISTRY.md
```

### 3. Deploy Assets to AROS Runtime

```bash
# Dry run first (preview without modifying)
bash 01.Shared_Assets/Scripts/deploy_to_aros.sh --dry-run

# Full deployment
bash 01.Shared_Assets/Scripts/deploy_to_aros.sh
```

### 4. Verify Deployment (inside Antigravity IDE)

After deployment, the assets are automatically indexed by the `antigravity-brain` MCP server. You can verify with:
```
find_helpful_skills("grant writing")
find_helpful_ki("KAKENHI")
```

---

## 🔧 Domain Pipelines

| Pipeline | Domain | Key Skills | Active Workflows |
|----------|--------|-----------|-----------------|
| **Grant_Write_Pipeline** | Scientific grants | `grant-mock-reviewer`, `medical-translation`, `abstract-trimmer`, `grant-budget-justification` | `/grant-write` |
| **KAKENHI_Pipeline** | JSPS KAKENHI reporting | `kakenhi-form-completion`, `kakenhi-pre-award-forms` | `/kakenhi-annual-report` |
| **Manuscript_Write_Pipeline** | Academic manuscripts | `peer-review`, `statistical-analysis`, `literature-review`, `method-writing` | `/manuscript-write` |
| **Bioinformatics_Pipeline** | Genomics & proteomics | `string-database`, `ppt-master` | — |
| **Data_Analysis_Pipeline** | Statistical modeling | `agentic-data-scientist`, `flowcypy` | `/visualize-data` |
| **Software_Engineering_Pipeline** | Code generation & QA | `gtb-validator`, `pipeline-orchestrator` | — |
| **System_Admin_Pipeline** | Environment management | `agent-environment-capabilities`, `conditional-logic-execution` | — |
| **UI_Development_Pipeline** | Web interface design | `agent-design-principles` | — |
| **Writing_Publishing_Pipeline** | Academic publishing | `research-lookup`, `semantic-scholar-database` | — |
| **Web_Scraping_API_Pipeline** | Data acquisition | `api_availability_precheck`, `crapome` | — |
| **Project_Management_Pipeline** | Task orchestration | `modular-task-breakdown`, `critical-task-output-guarantee` | — |
| **workspace_management** | Global infrastructure | `regent-governance`, `md-html-docx-generator` | `/lab-commit`, `/wiki-*`, `/science-project-onboarding` |

---

## 🛡️ Governance & Shared Asset Management

This repository uses a two-layer governance system to ensure all pipelines remain compatible as assets evolve.

### SAMS: Shared Asset Management System (v1.1)

The **Shared Asset Registry** at [`00.RawData/SHARED_ASSET_REGISTRY.md`](00.RawData/SHARED_ASSET_REGISTRY.md) is the single source of truth for all cross-pipeline assets. Before modifying any shared Skill, KI, Policy, or Workflow, consult this registry.

> **Cross-Platform Note**: SAMS v1.1 uses direct path referencing — no POSIX symlinks. This repository is fully operable on Linux, macOS, and Windows.

### Audit Tool

```bash
python3 01.Shared_Assets/Scripts/audit_shared_assets.py
```

This script verifies structural integrity, detects orphaned assets, and flags cross-pipeline compatibility violations.

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR.

Key points for contributors:
- All asset modifications must follow the **CPCP** (Cross-Pipeline Compatibility Protocol)
- New skills must use the `skill-name/SKILL.md` directory structure
- Workflows must include YAML frontmatter with a `description` field ≤ 250 chars
- Symlinks are **strictly banned** — use direct path references

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

This project is part of the **AROS Ecosystem**, developed by [LabOnoM](https://github.com/LabOnoM). The foundational philosophy of Cognitive Decomposition draws on research in embodied cognition, stochastic resonance neuroscience, and the gut-brain axis. See the Philosophy section above for detailed references.

---

---

## 🤖 AI Agent Operational Context

> **[FOR AI AGENTS]** This section is specifically authored for AI agents operating within this workspace. All rules below are binding and carry the force of LAW within AROS governance.

### ⚠️ Asset Forging Warning

This repository is a **Factory for forging AROS assets**. Before modifying any Skill, Policy, KI, or Workflow, you MUST read `AGENTS.md` and `SPEC.md` to understand:
- The CPCP constraints (LAW 0)
- The SAMS audit rules (LAW 1)
- Known failure modes (e.g., the LaTeX truncation bug, the SAMS Basename Trap)
- Directory-structure requirements (skill-name/SKILL.md pattern)

### 🔒 Governance Summary (Active Laws)

| Law | Name | Rule |
|-----|------|------|
| LAW -2 | Agent Version Control Awareness | Never modify `.regent/` directly. Use `rgt` binary only. |
| LAW -1 | Asset Forging Constraints | Skills use `dir/SKILL.md`. No symlinks. KI-Companion pattern for large workflows. |
| LAW 0 | CPCP — **SUPREME RULE** | Evaluate → Impact → Test → Resolve/Fork → Update Registry before any shared asset modification. |
| LAW 1 | Asset Deployment Protocol | Always use `deploy_to_aros.sh`. No manual `cp` to `~/.gemini/`. |

### 📋 Chronological Timeline (Verified)

| Timestamp | Event |
|-----------|-------|
| 2026-05-11 01:24 | KAKENHI pipeline KIs (e_application_system PDFs, forms) initialized |
| 2026-05-11 18:15 | Grant_Write_Pipeline skills requirements and assets initialized |
| 2026-05-11 18:29 | Manuscript_Write_Pipeline assets and scripts established |
| 2026-05-11 18:44 | Shared Asset Registry and CPCP governance established |
| 2026-05-11 19:00 | Centralized SAMS implemented with direct referencing and programmatic audit tools |
| 2026-05-11 21:00 | Dual-VCS architecture (Git + re_gent) deployed for AI agent auditability |
| 2026-05-11 22:00 | Replaced legacy `INDEX.csv` with `PIPELINE_REGISTRY.md`; generalized workflow templates |
| 2026-05-12 00:00 | 12-domain pipeline restructuring completed; SPEC v2.0 published |
| 2026-05-13 00:00 | Repository made public; MIT license added; multi-language READMEs created |

### 🔬 Hypothesis Evolution Table

| Phase | Hypothesis |
|-------|------------|
| H1 | Developing modular pipelines and agents for different writing tasks (grants, manuscripts, KAKENHI) significantly streamlines the academic drafting and submission process. |
| H2 | Shared assets across pipelines (KIs, policies, workflows) must be governed by a central registry and compatibility protocol to prevent cross-pipeline regressions. |
| H3 | Making the AROS Pipeline Factory public requires a dual-audience README architecture: human-readable introduction at the top, AI-agent operational context at the bottom. |

### 📂 Canonical Runtime Deployment Map

| Asset Type | Factory Source | AROS Runtime Target |
|------------|---------------|---------------------|
| **Skills** | `*/Skills/<skill-name>/` | `~/.gemini/skills/<skill-name>/SKILL.md` |
| **Knowledge Items** | `*/KIs/<ki-name>/` | `~/.gemini/antigravity/knowledge/<ki-name>/` |
| **Policies** | `*/Policies/*.md` | `~/.gemini/antigravity/policies/` |
| **Workflows** | `*/Workflows/*.md` | `~/.gemini/antigravity/global_workflows/` |

### 🔧 Active Workflow Triggers

| Slash Command | Pipeline | Purpose |
|--------------|---------|---------|
| `/grant-write` | Grant_Write_Pipeline | Universal grant writing |
| `/kakenhi-annual-report` | KAKENHI_Pipeline | JSPS KAKENHI lifecycle |
| `/manuscript-write` | Manuscript_Write_Pipeline | Dual-agent manuscript drafting |
| `/lab-commit` | workspace_management | Canonical commit gateway |
| `/lab-reorganize` | workspace_management | Git-safe file reorganization |
| `/wiki-ingest` | workspace_management | Ingest papers/data into LLM-Wiki |
| `/wiki-query` | workspace_management | Grounded Q&A from LLM-Wiki |
| `/wiki-research` | workspace_management | Literature research into wiki |
| `/wiki-update` | workspace_management | Wiki linting & synthesis |
| `/wiki-build` | workspace_management | Compile wiki into output docs |
| `/audit-shared-assets` | workspace_management | SAMS structural integrity audit |
| `/science-project-onboarding` | workspace_management | First-time project setup |
| `/visualize-data` | Data_Analysis_Pipeline | Autonomous diagram generation |
| `/research-discovery` | workspace_management | Research planning & brainstorm |
| `/qa-system-audit` | workspace_management | AROS QA health checks |
