---
name: esm
description: Toolkit for protein language models (ESM3 for multimodal generative protein design; ESM C for efficient embeddings). Use for sequence/structure/function generation or prediction, inverse folding, protein embeddings, or scalable inference via local weights or the Forge API.
license: MIT
metadata:
    skill-author: K-Dense Inc. and AIPOCH
---
```

# ESM: Evolutionary Scale Modeling

## Overview

ESM provides state-of-the-art protein language models for understanding, generating, and designing proteins. This skill enables working with two model families: ESM3 for generative protein design across sequence, structure, and function, and ESM C for efficient protein representation learning and embeddings.

## When to Use

- **Designing novel proteins** with desired properties by generating sequences (optionally conditioned on structure/function) using **ESM3**.
- **Completing or editing sequences** (e.g., filling masked residues, generating variants) for protein engineering workflows.
- **Predicting 3D structure from sequence** or performing **inverse folding** (designing sequences for a target structure) with ESM3’s structure/sequence tracks.
- **Generating protein embeddings** for downstream ML tasks (classification, clustering, similarity search, function prediction) using **ESM C**.
- **Scaling inference** to many sequences using the **Forge API** (async/batch execution, hosted large models).

## Key Features

- **ESM3 multimodal generation** across *sequence*, *structure*, and *function* tracks.
- **Local inference** (e.g., `esm3-sm-open-v1`) and **cloud inference** via **Forge** (e.g., `esm3-medium-2024-08`, `esm3-large-2024-03`).
- **Structure prediction** (sequence → coordinates/PDB) and **inverse folding** (structure → designed sequence).
- **Functional conditioning** via function annotations to bias generation toward desired functional regions.
- **ESM C embeddings** for efficient, high-quality protein representations.
- **Async batch processing** with Forge for high-throughput workloads.
- **Chain-of-thought generation** for iterative refinement of protein designs.

## Dependencies

- `esm` (Python package; install via pip/uv)
- `flash-attn` (optional; recommended for faster attention on supported GPUs)

> Version notes: exact versions depend on your environment and CUDA/PyTorch stack. Install commands below reflect the upstream package usage.

## Example Usage

The following script demonstrates:
1) local ESM3 sequence completion,  
2) Forge-based async batch generation, and  
3) local ESM C embeddings.

```python
"""
End-to-end example for ESM:
- Local ESM3: sequence completion
- Forge ESM3: async batch generation (requires token)
- Local ESM C: embeddings
"""

import os
import asyncio

# ---------- 1) Local ESM3: sequence completion ----------
from esm.models.esm3 import ESM3
from esm.sdk.api import ESMProtein, GenerationConfig

def local_esm3_sequence_completion():
    # Load a local ESM3 model (open weights)
    model = ESM3.from_pretrained("esm3-sm-open-v1").to("cuda")

    # '_' indicates masked/unknown residues to be generated
    protein = ESMProtein(sequence="MPRT___KEND")

    completed = model.generate(
        protein,
        GenerationConfig(track="sequence", num_steps=8)
    )
    print("Local ESM3 completed sequence:", completed.sequence)


# ---------- 2) Forge ESM3: async batch generation ----------
from esm.sdk.forge import ESM3ForgeInferenceClient

async def forge_batch_generation():
    token = os.environ.get("FORGE_TOKEN", "<token>")
    client = ESM3ForgeInferenceClient(
        model="esm3-medium-2024-08",
        url="https://forge.evolutionaryscale.ai",
        token=token,
    )

    proteins = [ESMProtein(sequence="MPRT" + "_" * 50 + "KEND") for _ in range(5)]
    tasks = [
        client.async_generate(p, GenerationConfig(track="sequence", num_steps=50))
        for p in proteins
    ]
    results = await asyncio.gather(*tasks)
    print("Forge batch results (first):", results[0].sequence)


# ---------- 3) Local ESM C: embeddings ----------
from esm.models.esmc import ESMC

def local_esmc_embeddings():
    model = ESMC.from_pretrained("esmc-300m").to("cuda")

    protein = ESMProtein(sequence="MPRTKEINDAGLIVHSP")
    encoded = model.encode(protein)
    embeddings = model.forward(encoded)

    # embeddings is a tensor-like output; exact shape depends on model/config
    print("ESM C embeddings computed.")


if __name__ == "__main__":
    local_esm3_sequence_completion()

    # Run Forge example only if you have a valid token
    # export FORGE_TOKEN="..."
    asyncio.run(forge_batch_generation())

    local_esmc_embeddings()
```

### Installation Commands

```bash
# Base
uv pip install esm

# Optional acceleration (GPU environments where supported)
uv pip install flash-attn --no-build-isolation
```

## Implementation Details

### ESM3 Tracks and Generation

- **Tracks** determine what the model generates:
  - `track="sequence"`: generates amino-acid tokens (use `_` for masked positions).
  - `track="structure"`: predicts 3D coordinates; can be exported as PDB (see `references/esm3-api.md`).
  - `track="function"`: predicts or conditions on functional annotations.

- **Core generation parameters** (via `GenerationConfig`):
  - `num_steps`: number of iterative generation steps; commonly aligned with the number of masked residues for sequence completion, or set to a design budget for de novo generation.
  - `temperature`: controls sampling diversity (lower = more deterministic; higher = more diverse).
  - Additional advanced controls and multimodal prompting patterns are documented in `references/esm3-api.md`.

### Structure Prediction and Inverse Folding

- **Structure prediction**: provide a sequence and generate on the `structure` track to obtain coordinates and/or a PDB representation.
- **Inverse folding**: start from a target structure (e.g., `ESMProtein.from_pdb(...)`), remove/omit the sequence, then generate on the `sequence` track to design a sequence compatible with the structure.

### ESM C Embeddings

- ESM C models are optimized for **representation learning**:
  - Use `model.encode(ESMProtein(...))` to tokenize/prepare inputs.
  - Use `model.forward(...)` to obtain embeddings/logits suitable for downstream tasks (classification, clustering, similarity).
- For batching and performance strategies (padding, caching, normalization), see `references/esm-c-api.md`.

### Forge API (Hosted Inference)

- Forge provides access to larger hosted models and scalable execution:
  - Use `ESM3ForgeInferenceClient(...)` with a token.
  - Prefer `async_generate` + `asyncio.gather(...)` for throughput.
- Authentication, rate limits, and batching modes are detailed in `references/forge-api.md`.

## Model Selection Guide

**ESM3 Models (Generative):**
- `esm3-sm-open-v1` (1.4B) - Open weights, local usage, good for experimentation
- `esm3-medium-2024-08` (7B) - Best balance of quality and speed (Forge only)
- `esm3-large-2024-03` (98B) - Highest quality, slower (Forge only)

**ESM C Models (Embeddings):**
- `esmc-300m` (30 layers) - Lightweight, fast inference
- `esmc-600m` (36 layers) - Balanced performance
- `esmc-6b` (80 layers) - Maximum representation quality

**Selection criteria:**
- **Local development/testing:** Use `esm3-sm-open-v1` or `esmc-300m`
- **Production quality:** Use `esm3-medium-2024-08` via Forge
- **Maximum accuracy:** Use `esm3-large-2024-03` or `esmc-6b`
- **High throughput:** Use Forge API with batch executor
- **Cost optimization:** Use smaller models, implement caching strategies

## Common Workflows

For detailed examples and complete workflows, see `references/workflows.md` which includes:
- Novel GFP design with chain-of-thought
- Protein variant generation and screening
- Structure-based sequence optimization
- Function prediction pipelines
- Embedding-based clustering and analysis

## Best Practices

**For generation tasks:**
- Start with smaller models for prototyping (`esm3-sm-open-v1`)
- Use temperature parameter to control diversity (0.0 = deterministic, 1.0 = diverse)
- Implement iterative refinement with chain-of-thought for complex designs
- Validate generated sequences with structure prediction or wet-lab experiments

**For embedding tasks:**
- Batch process sequences when possible for efficiency
- Cache embeddings for repeated analyses
- Normalize embeddings when computing similarities
- Use appropriate model size based on downstream task requirements

**For production deployment:**
- Use Forge API for scalability and latest models
- Implement error handling and retry logic for API calls
- Monitor token usage and implement rate limiting
- Consider AWS SageMaker deployment for dedicated infrastructure

## References

This skill includes comprehensive reference documentation:

- `references/esm3-api.md` - ESM3 model architecture, API reference, generation parameters, and multimodal prompting
- `references/esm-c-api.md` - ESM C model details, embedding strategies, and performance optimization
- `references/forge-api.md` - Forge platform documentation, authentication, batch processing, and deployment
- `references/workflows.md` - Complete examples and common workflow patterns

These references contain detailed API specifications, parameter descriptions, and advanced usage patterns. Load them as needed for specific tasks.

## Resources and Documentation

- **GitHub Repository:** https://github.com/evolutionaryscale/esm
- **Forge Platform:** https://forge.evolutionaryscale.ai
- **Scientific Paper:** Hayes et al., Science (2025) - https://www.science.org/doi/10.1126/science.ads0018
- **Blog Posts:**
  - ESM3 Release: https://www.evolutionaryscale.ai/blog/esm3-release
  - ESM C Launch: https://www.evolutionaryscale.ai/blog/esm-cambrian
- **Community:** Slack community at https://bit.ly/3FKwcWd
- **Model Weights:** HuggingFace EvolutionaryScale organization

## Responsible Use

ESM is designed for beneficial applications in protein engineering, drug discovery, and scientific research. Follow the Responsible Biodesign Framework (https://responsiblebiodesign.ai/) when designing novel proteins. Consider biosafety and ethical implications of protein designs before experimental validation.