---
description: Universal scientific grant writing pipeline — orchestrates funder profiling, literature retrieval, bilingual drafting, adversarial peer review, and template injection for any funding agency.
---

# `/grant-write` Workflow (Universal Scientific Grant Writing)

This workflow triggers the **Universal Scientific Grant Writing Pipeline**, transitioning the agent into a funder-agnostic proposal generator.

## Trigger Condition
When the user explicitly calls `/grant-write` or implicitly asks to draft a grant, write a proposal, or generate funder documentation.

## Required AROS Context
Before execution, ensure the following context is loaded via `find_helpful_ki` and `find_helpful_skills`:
- **KIs**: `grant_funder_profiles`, `agentic_manuscript_publishing`, `markdown_first_manuscript_policy`, `agentic_diagramming_standard`
- **Policies**: `output-truncation-management`, `gepa_protocol`
- **Skills**: `grant-funding-scout`, `scientific-brainstorming`, `knowledge-consolidation`, `grant-budget-justification`, `academic-cv-generator`, `visualize-data`, `grant-mock-reviewer`, `content-proofreading`, `semantic-consistency-auditor`, `response-relevance`, `abstract-trimmer`, `medical-translation`, `q-and-a-prep-partner`, `secure-html-delivery`, `pdf-extract-experimental-materials`, `research-proposal-generator`, `word-read-write`, `comprehensive-task-completion`, `literature-close-read`, `literature-ingestion`, `retraction-watcher`, `md-html-docx-generator`.

---

## Phase 0.5: Reference Inventory & Retrieval (MANDATORY — runs before any drafting)
> **This phase is non-negotiable. Drafting MUST NOT begin until all cited references are available locally.**

1. **Inventory**: Scan `<PROJECT_ROOT>/.wiki/` and `00.RawData/Literature/03_Parsed_Markdown/` to identify all currently ingested papers.
2. **Gap Detection**: Cross-reference the project's bibliography (e.g., `References/` folder, `.wiki/entities/`, or a user-provided DOI list) against ingested papers. Identify any DOIs/PMIDs that are referenced but NOT yet downloaded.
3. **Auto-Retrieval**: If gaps are found, trigger `/literature-ingest` with the missing identifiers and wait for completion before proceeding. (Ensure you pass `--base-dir <PROJECT_ROOT>` to route artifacts locally per the Universal PDF Processing Mandate).
4. **Retraction Scan**: Run `retraction-watcher` on the full reference list. Any retracted citation triggers a **mandatory HALT** — inform the PI and require a replacement citation before continuing.
5. **Verification Gate**: Confirm that ALL key cited papers exist in both `03_Parsed_Markdown/` (for LLM context) and `04_Parsed_JSON/` (for structural validation). If any remain missing after retrieval, notify the PI and proceed only with available evidence, flagging missing citations explicitly.

## Phase 1: Intake & Funder Configuration
1. **Scouting (Optional):** If the funder is unknown, use `grant-funding-scout` and `scientific-brainstorming` to identify a target agency.
2. **Profile Lookup:** Search the `grant_funder_profiles` KI for an existing profile: `read_ki_document(ki_name="grant_funder_profiles", document_path="artifacts/<funder_id>.json")`.
3. **Profile Generation (Fallback):** If no profile exists and the user provides a PDF/URL of the call, use the `pdf-extract-experimental-materials` skill to extract constraints and generate a new `funder_profile.json` → save it to the KI artifacts directory.
   - *Logic Gap Prevention:* If PDF extraction fails, do NOT halt. Fallback to interactive chat: ask the PI for section names, limits, and budget rules manually.
4. **Knowledge Consolidation:** Run `knowledge-consolidation` to synthesize researcher ORCID/researchmap data and wiki context.
5. **Confirmation:** Stop and request user confirmation of the Funder Profile and core project data.

## Phase 2: Visual Scheme & Timeline Generation
1. **Workflow Diagram**: Use `visualize-data` to generate a high-resolution SVG/PNG technical workflow diagram based on the research plan, utilizing `fireworks-tech-graph` templates (per `agentic_diagramming_standard` KI). Choose the appropriate visual style from the 7 available options (e.g., `style-4-notion-clean` for grant proposals, `style-1-flat-icon` for journal figures).
2. **Gantt / Milestone Timeline**: If the funder profile requires milestones, use `visualize-data` with the Gantt chart or grant lifecycle domain templates to create a timeline visualization.

## Phase 3: Structural Decomposition & Drafting Engine
1. **Scaffold:** Parse the sections defined in `funder_profile.json.sections`. Use `research-proposal-generator` to scaffold initial evidence limits in `00.Projects/<ProjectName>/GrantDraftElements/`.
2. **Drafting (Anti-Truncation):** Iteratively draft each section as a **separate LLM call**. *Strictly adhere to the `output-truncation-management` policy.*
3. **Citation-Before-Claim Protocol (MANDATORY):** Before writing any evidence-based claim, run `/wiki-query` or `literature-close-read` on the relevant ingested paper. Use the scratchpad pattern:
   ```
   GROUNDING CHECK:
     Claim: "[The proposed claim text]"
     Source: "[Exact quote from .wiki/ or 03_Parsed_Markdown/]"
     File: [path/to/source.md or [[wiki-page]]]
     Verdict: GROUNDED / NOT_FOUND
   ```
   If `NOT_FOUND`, run `/wiki-research` or flag as `[UNGROUNDED]`. **Do NOT write the claim until it is GROUNDED.**
4. **Translation:** If `funder_profile.languages` includes multiple languages (e.g., `["en", "ja"]`), write ALL English files first, then invoke `medical-translation` to generate localized equivalents.
5. **Compression:** If a section has a `limit_type` (chars/words/pages), invoke `abstract-trimmer`.
   - *Dead-End Prevention:* Generate 2-3 compression variants. If the agent cannot compress it to fit, halt and ask the PI to choose a variant or manually edit.

## Phase 4: CV, Publications & Budget Generation
1. **Biosketch/CV:** If `funder_profile` requires a CV, generate it using `academic-cv-generator`.
2. **Budget:** Run `grant-budget-justification` against `funder_profile.budget` constraints (caps, indirect rates, personnel limits).

## Phase 5: Simulated Peer Review & Quality Gates
> **Minimum 3 review rounds are MANDATORY regardless of initial score.**

1. **Mock Review (≥3 Rounds):** Run `grant-mock-reviewer` (Actor-Critic pattern from `agentic_manuscript_publishing` KI) to assess the draft against `funder_profile.evaluation_criteria`.
   - Output each review round as a new `## Round N` section in `<ProjectRoot>/GrantDraftElements/REVIEW_LOG.md`.
   - **Grounding Audit:** The reviewer MUST flag any claim that cannot be traced to a `.wiki/` or `03_Parsed_Markdown/` source as `[UNGROUNDED — CITE REQUIRED]`.
   - **Retraction Audit:** Verify the final reference list with `retraction-watcher` after every revision round.
   - *Loop Enforcement:* Run a minimum of **3 refinement rounds**. Even if the draft passes evaluation criteria before Round 3, continue with a "hardening review" targeting citation completeness, budget accuracy, and language compliance. Maximum 5 rounds total (per `gepa_protocol`). If it still fails after Round 5, escalate to the PI.
2. **Quality Gates:** Run `content-proofreading`, `semantic-consistency-auditor`, and `response-relevance` to verify grammar, cross-section coherence, and mandate compliance.

## Phase 6: Assembly, Finalization & Delivery
1. **Assembly:** Compile sections per the `submission_format` constraint (e.g., inject into `.xlsx`, use Pandoc for PDF/LaTeX, or `word-read-write` for `.docx`). *Enforce `markdown_first_manuscript_policy`.*
2. **Interactive HTML Report (Optional):** If the PI requests an interactive deliverable or a shareable progress report, run the `md-html-docx-generator` skill on the assembled Markdown:
   ```bash
   python3 01.Shared_Assets/Skills/md-html-docx-generator/scripts/build_report.py \
       <assembled_markdown.md> -o <ProjectRoot>/output/grant_report.html [--docx]
   ```
3. **Oral Defense:** If `has_oral_defense` is true, invoke `q-and-a-prep-partner` to generate an elevator pitch and defense material.
4. **Secure Delivery:** If requested by the PI, invoke `secure-html-delivery` to encrypt the HTML deliverables for external sharing via AES-256-GCM.
5. **Commit:** Execute `/lab-commit` to transactionally save the state to version control.
