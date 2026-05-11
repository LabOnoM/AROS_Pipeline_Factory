# Citation-Before-Claim Protocol

> **Type**: Institutional Policy / Drafting Standard
> **Applies To**: `/manuscript-write`, `/grant-write`, `/wiki-build`
> **Status**: MANDATORY
> **Last Updated**: 2026-05-12 (v1.1 — Added Phase 0.5 and Retraction Scan)

## 1. Core Principle
The **Citation-Before-Claim Protocol** (Strict Grounding) enforces that an AI agent cannot generate any evidence-based scientific claim without first providing an explicit, verifiable grounding source. This acts as a circuit breaker against AI hallucinations and "hallucinated citations" (e.g., citing a non-existent paper, or misattributing a finding to a real paper).

## 2. Phase 0.5: Reference Inventory & Retrieval (Pre-Draft Gate)
Before ANY drafting begins in a manuscript or grant workflow, the agent MUST complete the following gate:

1. **Inventory**: Scan `<PROJECT_ROOT>/.wiki/` and `00.RawData/Literature/03_Parsed_Markdown/` to identify all currently ingested papers.
2. **Gap Detection**: Cross-reference the bibliography against ingested papers. Identify any DOIs/PMIDs NOT yet downloaded.
3. **Auto-Retrieval**: Trigger `/literature-ingest` for any missing identifiers. Wait for completion.
4. **Retraction Scan**: Run `retraction-watcher` on the full reference list. Any retracted citation triggers a **mandatory HALT** — inform the PI and require a replacement citation before continuing.
5. **Verification Gate**: Confirm ALL key cited papers exist in both `03_Parsed_Markdown/` (Markdown for LLM context) and `04_Parsed_JSON/` (JSON for structural validation).

> **Why this gate exists**: Without it, agents draft against references they assume exist but haven't retrieved, creating `[UNGROUNDED]` claims that pass local checks but fail peer review.

## 3. The Scratchpad Pattern
When an agent is tasked with writing a section of a manuscript or a grant proposal, it must generate a structured "Grounding Check" scratchpad for every factual claim *before* writing the final paragraph.

### Format
```markdown
GROUNDING CHECK:
  Claim: "[The proposed claim text to be written]"
  Source: "[Exact quote from the .wiki/ page or the 03_Parsed_Markdown/ file]"
  File: [path/to/source.md or [[wiki-page]]]
  Verdict: GROUNDED / NOT_FOUND
```

### Rule
If the agent cannot locate a supporting quote in the local knowledge base, the Verdict is `NOT_FOUND`.
The agent **MUST NOT** write the claim.
Instead, the agent must either:
1. Run `/wiki-research` to autonomously find the literature to support the claim.
2. Flag the draft text with `[UNGROUNDED: REQUIRES CITATION]` and notify the PI.

## 4. Supported Tooling
To successfully execute this protocol, agents must rely on these primary skills:
- **`retraction-watcher`**: MANDATORY pre-draft scan of all references against Retraction Watch DB.
- **`literature-close-read`**: Used for deep, structured evidence extraction from newly ingested PDFs (`03_Parsed_Markdown/`).
- **`/wiki-query`**: Used for rapid fact retrieval from established LLM-Wiki concepts.
- **`literature-ingestion`**: Retrieves missing PDFs via 6-tier cascade and converts to Dual-Format (Markdown + JSON).

## 5. Review Enforcement
The dual-agent review loop enforces this protocol with a **minimum of 3 review rounds**:
- **Agent B (Reviewer)** scores Citation Integrity (Dimension 8) and MUST flag any `[UNGROUNDED]` claim.
- Even if the manuscript/grant passes the score threshold before Round 3, Agent B continues with hardening reviews.
- All review rounds are logged as `## Round N` sections in `REVIEW_LOG.md`.

## 6. Rationale
In earlier pipeline iterations (e.g., the April 2026 spatial transcriptomics case), agents would generate highly plausible but entirely fabricated mechanisms if they were asked to connect two concepts without explicit context. By enforcing a "Show Your Work" scratchpad, the LLM is forced to do the retrieval *before* the generation, utilizing its in-context attention to prevent hallucination.
