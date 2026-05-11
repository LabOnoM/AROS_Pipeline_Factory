---
description: Automated literature research to expand the LLM-Wiki while adhering to Strict Grounding.
---

# Wiki Research Workflow

Run this workflow whenever the AI detects a biological knowledge gap that it cannot answer using the local files, OR when the user explicitly asks the AI to research an external scientific mechanism. This workflow bridges the "Strict Grounding" barrier by physically downloading external facts into the local workspace so they become verifiable ground truth.

## Step 1: Online Search & API Queries

Use your `search_web` tool to find open access literature (PubMed PMC is preferred) covering the requested mechanism or topic.

If searching for PubMed articles, use the PMC APIs to directly pull the raw `BioC_json` or text formats, avoiding bot-blocking associated with PDFs.  
Example API Endpoint: `https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/[PMCID]/unicode`

## Step 2: Download Source File (Strict Grounding)

Use `run_command` and `curl -L` or `wget` to save the raw JSON/Text/PDF file directly into the `Articles/01.Review&Mechanism/` directory.

**Rule**: You cannot simply read the abstract online and pretend it's in the wiki. You MUST download the raw representation into the local filesystem.

## Step 3: Digest into LLM-Wiki

Immediately trigger the `/wiki-ingest` logic:
1. Create a new `.wiki/sources/[Author]-[Year]-[Topic].md` file documenting the mechanism and explicitly linking to the downloaded raw file.
2. Create or update the necessary `.wiki/concepts/` or `.wiki/entities/` pages to connect this new knowledge to the project's existing variables (e.g. SP7, MSCs).

## Step 4: Commit

Use the standard automated `/lab-commit` trigger to save the newly expanded knowledge graph into the git tree with a `[P#] MECHANISM ...` styled commit message.
