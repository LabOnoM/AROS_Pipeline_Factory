# Grant Write Pipeline Context

## 🧭 Domain Context
This pipeline is dedicated to Universal Grant Writing (e.g., NIH, JSPS, ERC). It orchestrates funder profiling, bilingual drafting, and peer review.

## ⚖️ Component Rules
- **Literature Grounding**: Mandatory use of the `literature-ingestion` shared skill for retrieving PDFs and citations before generating grant claims.
- **Dual-Agent Review**: Drafts must pass through a strict adversarial peer-review loop.
- **Output Format**: Final outputs are generated via `md-html-docx-generator` to bypass LLM token limits and create structured, interactive reports.

## 🚀 Execution
- **Trigger**: The `/grant-write` workflow governs operations here.
