# Grant Write Pipeline

The Universal Scientific Grant Writing Pipeline is a funder-agnostic proposal generator designed to orchestrate the entire lifecycle of a grant application.

## Key Features
- **Phase 0 (Output Manifest)**: Mandates the generation of a `GRANT_OUTPUT_MANIFEST.md` to define expected outputs before drafting.
- **Phase Completion Gates**: Mandatory verification steps (using `find`, `wc -l`) after critical drafting and assembly phases.
- **Bilingual Drafting**: Sequential drafting (EN first, then translation to JP) to ensure narrative coherence.
- **Skill Integration**: Utilizes `secure-html-delivery` and `excel-injection` for final deliverables.

## Governance
- Adheres to [[cross_pipeline_compatibility_protocol]]
- Enforces [[citation_before_claim_protocol]]
