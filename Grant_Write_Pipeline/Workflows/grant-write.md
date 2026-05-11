---
description: Universal scientific grant writing pipeline — orchestrates funder profiling, bilingual drafting, adversarial peer review, and template injection for any funding agency.
---

# `/grant-write` Workflow (Universal Scientific Grant Writing)

This workflow triggers the **Universal Scientific Grant Writing Pipeline**, transitioning the agent into a funder-agnostic proposal generator.

## Trigger Condition
When the user explicitly calls `/grant-write` or implicitly asks to draft a grant, write a proposal, or generate funder documentation.

## Required AROS Context
Before execution, ensure the following context is loaded via `find_helpful_ki` and `find_helpful_skills`:
- **KIs**: `grant_funder_profiles`, `agentic_manuscript_publishing`, `markdown_first_manuscript_policy`
- **Policies**: `output-truncation-management`, `gepa_protocol`
- **Skills**: `grant-funding-scout`, `scientific-brainstorming`, `knowledge-consolidation`, `grant-budget-justification`, `academic-cv-generator`, `visualize-data`, `grant-mock-reviewer`, `content-proofreading`, `semantic-consistency-auditor`, `response-relevance`, `abstract-trimmer`, `medical-translation`, `q-and-a-prep-partner`, `secure-html-delivery`, `pdf-extract-experimental-materials`, `research-proposal-generator`, `word-read-write`, `comprehensive-task-completion`.

---

## Phase 1: Intake & Funder Configuration
1. **Scouting (Optional):** If the funder is unknown, use `grant-funding-scout` and `scientific-brainstorming` to identify a target agency.
2. **Profile Lookup:** Search the `grant_funder_profiles` KI for an existing profile: `read_ki_document(ki_name="grant_funder_profiles", document_path="artifacts/<funder_id>.json")`.
3. **Profile Generation (Fallback):** If no profile exists and the user provides a PDF/URL of the call, use the `pdf-extract-experimental-materials` skill to extract constraints and generate a new `funder_profile.json` → save it to the KI artifacts directory.
   - *Logic Gap Prevention:* If PDF extraction fails, do NOT halt. Fallback to interactive chat: ask the PI for section names, limits, and budget rules manually.
4. **Knowledge Consolidation:** Run `knowledge-consolidation` to synthesize researcher ORCID/researchmap data and wiki context.
5. **Confirmation:** Stop and request user confirmation of the Funder Profile and core project data.

## Phase 2: Visual Scheme & Timeline Generation
1. Use `visualize-data` to generate a high-resolution SVG technical workflow diagram based on the research plan, utilizing `fireworks-tech-graph` templates.
2. If the funder profile requires milestones, use `visualize-data` (specifically the Gantt chart or grant lifecycle templates) to create a timeline visualization.

## Phase 3: Structural Decomposition & Drafting Engine
1. **Scaffold:** Parse the sections defined in `funder_profile.json.sections`. Use `research-proposal-generator` to scaffold initial evidence limits in `00.Projects/<ProjectName>/GrantDraftElements/`.
2. **Drafting (Anti-Truncation):** Iteratively draft each section as a **separate LLM call**. *Strictly adhere to the `output-truncation-management` policy.*
3. **Translation:** If `funder_profile.languages` includes multiple languages (e.g., `["en", "ja"]`), write ALL English files first, then invoke `medical-translation` to generate localized equivalents.
4. **Compression:** If a section has a `limit_type` (chars/words/pages), invoke `abstract-trimmer`.
   - *Dead-End Prevention:* Generate 2-3 compression variants. If the agent cannot compress it to fit, halt and ask the PI to choose a variant or manually edit.

## Phase 4: CV, Publications & Budget Generation
1. **Biosketch/CV:** If `funder_profile` requires a CV, generate it using `academic-cv-generator`.
2. **Budget:** Run `grant-budget-justification` against `funder_profile.budget` constraints (caps, indirect rates, personnel limits).

## Phase 5: Simulated Peer Review & Quality Gates
1. **Mock Review:** Run `grant-mock-reviewer` (Actor-Critic pattern from `agentic_manuscript_publishing` KI) to assess the draft against `funder_profile.evaluation_criteria`.
   - *Loop Prevention:* Limit to exactly **3 refinement loops** (per `gepa_protocol`). If it still fails compliance, escalate to the PI.
2. **Quality Gates:** Run `content-proofreading`, `semantic-consistency-auditor`, and `response-relevance` to verify grammar, cross-section coherence, and mandate compliance.

## Phase 6: Assembly, Finalization & Delivery
1. **Assembly:** Compile sections per the `submission_format` constraint (e.g., inject into `.xlsx`, use Pandoc for PDF/LaTeX, or `word-read-write` for `.docx`). *Enforce `markdown_first_manuscript_policy`.*
2. **Oral Defense:** If `has_oral_defense` is true, invoke `q-and-a-prep-partner` to generate an elevator pitch and defense material.
3. **Secure Delivery:** If requested by the PI, invoke `secure-html-delivery` to encrypt the deliverables for external sharing via AES-256-GCM.
4. **Commit:** Execute `/lab-commit` to transactionally save the state to version control.
