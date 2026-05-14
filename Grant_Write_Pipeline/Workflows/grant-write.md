---
description: Universal scientific grant writing pipeline — orchestrates funder profiling, literature retrieval, bilingual drafting, adversarial peer review, and template injection for any funding agency.
---

# `/grant-write` Workflow (Universal Scientific Grant Writing)

This workflow triggers the **Universal Scientific Grant Writing Pipeline**, transitioning the agent into a funder-agnostic proposal generator.

## Trigger Condition
When the user explicitly calls `/grant-write` or implicitly asks to draft, write, **regenerate, or edit** a grant, proposal, or funder documentation.

## Required AROS Context
Before execution, ensure the following context is loaded via `find_helpful_ki` and `find_helpful_skills`:
- **KIs**: `grant_funder_profiles`, `agentic_manuscript_publishing`, `markdown_first_manuscript_policy`, `agentic_diagramming_standard`
- **Policies**: `output-truncation-management`, `gepa_protocol`
- **Skills**: `grant-funding-scout`, `scientific-brainstorming`, `knowledge-consolidation`, `grant-budget-justification`, `academic-cv-generator`, `visualize-data`, `grant-mock-reviewer`, `content-proofreading`, `semantic-consistency-auditor`, `response-relevance`, `abstract-trimmer`, `content-expander`, `medical-translation`, `q-and-a-prep-partner`, `secure-html-delivery`, `pdf-extract-experimental-materials`, `research-proposal-generator`, `word-read-write`, `comprehensive-task-completion`, `literature-close-read`, `literature-ingestion`, `retraction-watcher`, `md-html-docx-generator`.

---

## Phase 0: Scoping, Validation & Plan Generation (MANDATORY)
> **Actor Persona:** `project_manager`
> **Goal:** Decompose the user request into a concrete execution plan. **DO NOT proceed to drafting until this plan is confirmed by the user.**

1.  **Intent Analysis**: Determine the core intent:
    -   **`CREATE_NEW`**: A new grant from scratch.
    -   **`REGENERATE`**: Overwriting/updating existing draft files.
    -   **`EDIT`**: Modifying specific sections of existing drafts.
2.  **Constraint Identification**: Parse the user's prompt for all explicit constraints (e.g., target filenames, section length requirements like "occupy 85% of character limits", number of review rounds, specific funder guidelines).
3.  **Initial State Check**: If the intent is `REGENERATE` or `EDIT`, verify that the specified target files exist within the project. If not, ask the user for the correct path or confirm a switch to `CREATE_NEW` mode.
4.  **Plan Generation**: Create a step-by-step execution plan in Markdown. The plan must list each phase, the actions to be taken, the target files, and the identified constraints.
5.  **Confirmation Gate**: Present the plan to the user. Halt execution until the user explicitly approves the plan (e.g., with "Approved", "Proceed", "Yes").

## Phase 0.5: Reference Inventory & Retrieval (MANDATORY)
> **Actor Persona:** `research_assistant`
> **This phase is non-negotiable. Drafting MUST NOT begin until all cited references are available locally.**

1.  **Inventory**: Scan `./.wiki/` and `00.RawData/Literature/03_Parsed_Markdown/` to identify all currently ingested papers.
2.  **Gap Detection**: Cross-reference the project's bibliography against ingested papers. Identify any DOIs/PMIDs that are referenced but NOT yet downloaded.
3.  **Auto-Retrieval**: If gaps are found, trigger `/literature-ingest` with the missing identifiers and wait for completion.
4.  **Retraction Scan**: Run `retraction-watcher` on the full reference list. Any retracted citation triggers a **mandatory HALT** — inform the PI and require a replacement citation before continuing.
5.  **Verification Gate**: Confirm that ALL key cited papers exist in both `03_Parsed_Markdown/` and `04_Parsed_JSON/`. If any remain missing, notify the PI and proceed only with available evidence, flagging missing citations explicitly.

## Phase 1: Intake & Funder Configuration
1.  **Scouting (Optional):** If the funder is unknown, use `grant-funding-scout` and `scientific-brainstorming` to identify a target agency.
2.  **Profile Lookup:** Search `grant_funder_profiles` KI for an existing profile: `read_ki_document(ki_name="grant_funder_profiles", document_path="artifacts/<funder_id>.json")`.
3.  **Profile Generation (Fallback):** If no profile exists, use `pdf-extract-experimental-materials` on a user-provided PDF/URL to generate a new `funder_profile.json` and save it.
   - *Logic Gap Prevention:* If PDF extraction fails, do NOT halt. Fallback to interactive chat: ask the PI for section names, limits, and budget rules manually.
4.  **Knowledge Consolidation:** Run `knowledge-consolidation` to synthesize researcher data and wiki context.

## Phase 2: Visual Scheme & Timeline Generation
1.  **Workflow Diagram**: Use `visualize-data` to generate a technical workflow diagram (SVG/PNG) based on the research plan, adhering to the `agentic_diagramming_standard` KI.
2.  **Gantt / Milestone Timeline**: If required, use `visualize-data` with Gantt chart templates to create a timeline visualization.

## Phase 3: Structural Decomposition & Drafting Engine
> **Actor Persona:** `manuscript_writer`

1.  **Scaffold:** Parse `funder_profile.json.sections`. Use `research-proposal-generator` to scaffold initial Markdown files in `./GrantDraftElements/`.
2.  **Drafting (Anti-Truncation):** Iteratively draft each section as a **separate LLM call**. *Strictly adhere to the `output-truncation-management` policy.*
3.  **Draft, Placeholder, and Ground Protocol (MANDATORY):**
    a. **Draft First**: Write a full paragraph or section focusing on scientific flow and argumentation.
    b. **Insert Placeholders**: After drafting, review the text and insert citation placeholders for every evidence-based claim, e.g., `[CITE: mechanism of action for drug X]`.
    c. **Grounding Pass**: In a separate, dedicated step, use `/wiki-query` or `literature-close-read` to resolve all `[CITE: ...]` placeholders with actual references. Any claim that cannot be grounded must be flagged as `[UNGROUNDED - EVIDENCE REQUIRED]`.
4.  **Content Length Adjustment**:
    - **Expansion**: If the Phase 0 plan includes a minimum length constraint (e.g., "85% fill rate"), and a drafted section is too short, invoke the `content-expander` skill to elaborate on technical details, add context, or provide more examples.
    - **Compression**: If a section exceeds a `limit_type` (chars/words), invoke `abstract-trimmer`.
    - *Dead-End Prevention:* If automated adjustments fail to meet constraints, halt and ask the PI for guidance.
5.  **Translation:** If `funder_profile.languages` requires multiple languages, write ALL English files first, then invoke `medical-translation` to generate localized equivalents.

## Phase 4: CV, Publications & Budget Generation
1.  **Biosketch/CV:** If required, generate using `academic-cv-generator`.
2.  **Budget:** Run `grant-budget-justification` against `funder_profile.budget` constraints.

## Phase 5: Simulated Peer Review & Quality Gates
> **Actor Persona:** `peer_reviewer`

1.  **Review Round Configuration**:
    - **Default:** Minimum of 3, maximum of 5 refinement rounds.
    - **User Override:** If the user specified a number of rounds in the initial prompt (and it was approved in the Phase 0 plan), that number becomes the **mandatory** target.
2.  **Mock Review Loop:** Run `grant-mock-reviewer` to assess the draft against `funder_profile.evaluation_criteria`.
   - Output each review round as a new `## Round N` section in `./GrantDraftElements/REVIEW_LOG.md`.
   - **Grounding Audit:** Reviewer MUST flag any claim not backed by a citation as `[UNGROUNDED — CITE REQUIRED]`.
   - **Retraction Audit:** Verify the final reference list with `retraction-watcher` after every revision round.
   - **Loop Enforcement:** Continue review/refinement cycles until the target number of rounds is complete. If the draft fails evaluation after the final round, escalate to the PI.
3.  **Quality Gates:** After the final review round, run `content-proofreading`, `semantic-consistency-auditor`, and `response-relevance`.

## Phase 6: Assembly, Finalization & Delivery
1.  **Assembly:** Compile sections per the `submission_format` constraint (e.g., inject into `.xlsx`, use Pandoc for PDF/LaTeX, or `word-read-write` for `.docx`). *Enforce `markdown_first_manuscript_policy`.*
2.  **Interactive HTML Report (Optional):** If requested, run `md-html-docx-generator`.
3.  **Oral Defense:** If `has_oral_defense` is true, invoke `q-and-a-prep-partner`.
4.  **Secure Delivery:** If requested, invoke `secure-html-delivery` to encrypt HTML deliverables.
5.  **Commit:** Execute `/lab-commit` to transactionally save the state to version control.