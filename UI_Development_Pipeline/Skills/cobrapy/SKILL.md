---
name: cobrapy
description: Constraint-based reconstruction and analysis (COBRA) for metabolic models; use when you need to simulate growth/production, analyze flux ranges, or run knockout and medium studies from SBML/JSON/YAML models.
license: MIT
skill-author: AIPOCH
---

# COBRApy (COBRA: Constraint-Based Reconstruction and Analysis)

## Overview

COBRApy is a Python library for constraint-based reconstruction and analysis (COBRA) of metabolic models, essential for systems biology research. Work with genome-scale metabolic models, perform computational simulations of cellular metabolism, conduct metabolic engineering analyses, and predict phenotypic behaviors.

## When to Use

Use this skill when you need to perform constraint-based analysis on metabolic networks, especially for:

1. **Predicting growth or production** under specific media and objectives using Flux Balance Analysis (FBA).
2. **Quantifying flux uncertainty** and alternative optima using Flux Variability Analysis (FVA) and flux sampling.
3. **Identifying essential genes/reactions** via single/double knockout (deletion) studies.
4. **Designing or optimizing media** (e.g., minimal medium) to support a target growth rate.
5. **Repairing infeasible models** by gapfilling against a universal reaction database/model.

## Key Features

- **Model I/O and management**: load/save models in SBML (preferred), JSON, and YAML; access reactions/metabolites/genes.
- **FBA variants**: standard FBA, parsimonious FBA (pFBA), geometric FBA.
- **FVA**: compute min/max feasible fluxes; supports fraction-of-optimum and loopless FVA.
- **Knockout analysis**: single/double gene and reaction deletions; temporary edits via context managers.
- **Medium handling**: inspect and modify `model.medium`; compute minimal media (optionally MILP-based).
- **Flux sampling**: sample feasible flux space (OptGP/ACHR) and validate samples.
- **Production envelopes**: phenotypic phase planes / production envelopes for trade-off exploration.
- **Gapfilling**: propose reaction additions to restore feasibility.
- **Model construction**: build models from scratch (metabolites, reactions, GPR rules, boundaries, objectives).

## Dependencies

- `cobra` (COBRApy) — version varies by environment (commonly `>=0.20`)
- A supported LP/MILP solver (one of):
  - `glpk` / `swiglpk` (often default)
  - `cplex` (optional)
  - `gurobi` (optional)
- Optional (for plotting/analysis in examples):
  - `pandas`
  - `matplotlib`

## Core Capabilities

### 1. Model Management

Load existing models from repositories or files:
```python
from cobra.io import load_model

# Load bundled test models
model = load_model("textbook")  # E. coli core model

# Load from files
from cobra.io import read_sbml_model, load_json_model, load_yaml_model
model = read_sbml_model("path/to/model.xml")
model = load_json_model("path/to/model.json")
model = load_yaml_model("path/to/model.yml")
```

Save models in various formats:
```python
from cobra.io import write_sbml_model, save_json_model, save_yaml_model
write_sbml_model(model, "output.xml")  # Preferred format
save_json_model(model, "output.json")  # For Escher compatibility
save_yaml_model(model, "output.yml")   # Human-readable
```

### 2. Model Structure and Components

Access and inspect model components:
```python
# Access components
model.reactions      # DictList of all reactions
model.metabolites    # DictList of all metabolites
model.genes          # DictList of all genes

# Get specific items by ID or index
reaction = model.reactions.get_by_id("PFK")
metabolite = model.metabolites[0]

# Inspect properties
print(reaction.reaction)        # Stoichiometric equation
print(reaction.bounds)          # Flux constraints
print(reaction.gene_reaction_rule)  # GPR logic
print(metabolite.formula)       # Chemical formula
print(metabolite.compartment)   # Cellular location
```

### 3. Flux Balance Analysis (FBA)

Perform standard FBA simulation:
```python
# Basic optimization
solution = model.optimize()
print(f"Objective value: {solution.objective_value}")
print(f"Status: {solution.status}")

# Access fluxes
print(solution.fluxes["PFK"])
print(solution.fluxes.head())

# Fast optimization (objective value only)
objective_value = model.slim_optimize()

# Change objective
model.objective = "ATPM"
solution = model.optimize()
```

Parsimonious FBA (minimize total flux):
```python
from cobra.flux_analysis import pfba
solution = pfba(model)
```

Geometric FBA (find central solution):
```python
from cobra.flux_analysis import geometric_fba
solution = geometric_fba(model)
```

### 4. Flux Variability Analysis (FVA)

Determine flux ranges for all reactions:
```python
from cobra.flux_analysis import flux_variability_analysis

# Standard FVA
fva_result = flux_variability_analysis(model)

# FVA at 90% optimality
fva_result = flux_variability_analysis(model, fraction_of_optimum=0.9)

# Loopless FVA (eliminates thermodynamically infeasible loops)
fva_result = flux_variability_analysis(model, loopless=True)

# FVA for specific reactions
fva_result = flux_variability_analysis(
    model,
    reaction_list=["PFK", "FBA", "PGI"]
)
```

### 5. Gene and Reaction Deletion Studies

Perform knockout analyses:
```python
from cobra.flux_analysis import (
    single_gene_deletion,
    single_reaction_deletion,
    double_gene_deletion,
    double_reaction_deletion
)

# Single deletions
gene_results = single_gene_deletion(model)
reaction_results = single_reaction_deletion(model)

# Double deletions (uses multiprocessing)
double_gene_results = double_gene_deletion(
    model,
    processes=4  # Number of CPU cores
)

# Manual knockout using context manager
with model:
    model.genes.get_by_id("b0008").knock_out()
    solution = model.optimize()
    print(f"Growth after knockout: {solution.objective_value}")
# Model automatically reverts after context exit
```

### 6. Growth Media and Minimal Media

Manage growth medium:
```python
# View current medium
print(model.medium)

# Modify medium (must reassign entire dict)
medium = model.medium
medium["EX_glc__D_e"] = 10.0  # Set glucose uptake
medium["EX_o2_e"] = 0.0       # Anaerobic conditions
model.medium = medium

# Calculate minimal media
from cobra.medium import minimal_medium

# Minimize total import flux
min_medium = minimal_medium(model, minimize_components=False)

# Minimize number of components (uses MILP, slower)
min_medium = minimal_medium(
    model,
    minimize_components=True,
    open_exchanges=True
)
```

### 7. Flux Sampling

Sample the feasible flux space:
```python
from cobra.sampling import sample

# Sample using OptGP (default, supports parallel processing)
samples = sample(model, n=1000, method="optgp", processes=4)

# Sample using ACHR
samples = sample(model, n=1000, method="achr")

# Validate samples
from cobra.sampling import OptGPSampler
sampler = OptGPSampler(model, processes=4)
sampler.sample(1000)
validation = sampler.validate(sampler.samples)
print(validation.value_counts())  # Should be all 'v' for valid
```

### 8. Production Envelopes

Calculate phenotype phase planes:
```python
from cobra.flux_analysis import production_envelope

# Standard production envelope
envelope = production_envelope(
    model,
    reactions=["EX_glc__D_e", "EX_o2_e"],
    objective="EX_ac_e"  # Acetate production
)

# With carbon yield
envelope = production_envelope(
    model,
    reactions=["EX_glc__D_e", "EX_o2_e"],
    carbon_sources="EX_glc__D_e"
)

# Visualize (use matplotlib or pandas plotting)
import matplotlib.pyplot as plt
envelope.plot(x="EX_glc__D_e", y="EX_o2_e", kind="scatter")
plt.show()
```

### 9. Gapfilling

Add reactions to make models feasible:
```python
from cobra.flux_analysis import gapfill

# Prepare universal model with candidate reactions
universal = load_model("universal")

# Perform gapfilling
with model:
    # Remove reactions to create gaps for demonstration
    model.remove_reactions([model.reactions.PGI])

    # Find reactions needed
    solution = gapfill(model, universal)
    print(f"Reactions to add: {solution}")
```

### 10. Model Building

Build models from scratch:
```python
from cobra import Model, Reaction, Metabolite

# Create model
model = Model("my_model")

# Create metabolites
atp_c = Metabolite("atp_c", formula="C10H12N5O13P3",
                   name="ATP", compartment="c")
adp_c = Metabolite("adp_c", formula="C10H12N5O10P2",
                   name="ADP", compartment="c")
pi_c = Metabolite("pi_c", formula="HO4P",
                  name="Phosphate", compartment="c")

# Create reaction
reaction = Reaction("ATPASE")
reaction.name = "ATP hydrolysis"
reaction.subsystem = "Energy"
reaction.lower_bound = 0.0
reaction.upper_bound = 1000.0

# Add metabolites with stoichiometry
reaction.add_metabolites({
    atp_c: -1.0,
    adp_c: 1.0,
    pi_c: 1.0
})

# Add gene-reaction rule
reaction.gene_reaction_rule = "(gene1 and gene2) or gene3"

# Add to model
model.add_reactions([reaction])

# Add boundary reactions
model.add_boundary(atp_c, type="exchange")
model.add_boundary(adp_c, type="demand")

# Set objective
model.objective = "ATPASE"
```

## Example Usage

The following script is a complete, runnable example that loads a built-in model, runs FBA, performs FVA, runs a gene knockout, adjusts medium, and samples fluxes.

```python
# cobrapy_example.py
from cobra.io import load_model
from cobra.flux_analysis import flux_variability_analysis, single_gene_deletion, pfba
from cobra.sampling import sample

def main():
    # 1) Load a model (built-in test model)
    model = load_model("textbook")  # E. coli core model

    # 2) Run standard FBA
    sol = model.optimize()
    print("=== FBA ===")
    print("Status:", sol.status)
    print("Objective (growth):", sol.objective_value)

    # 3) Run pFBA (minimize total flux at optimal growth)
    pfba_sol = pfba(model)
    print("\n=== pFBA ===")
    print("Objective (growth):", pfba_sol.objective_value)

    # 4) Flux Variability Analysis at 90% of optimum
    print("\n=== FVA (90% optimum) ===")
    fva = flux_variability_analysis(model, fraction_of_optimum=0.9)
    print(fva.head())

    # 5) Single gene deletion screen (may take time on large models)
    print("\n=== Single Gene Deletion (first 5 rows) ===")
    del_res = single_gene_deletion(model)
    print(del_res.head())

    # 6) Medium modification (must re-assign the full dict)
    print("\n=== Medium ===")
    medium = model.medium
    # Example: limit glucose uptake (exchange IDs depend on the model)
    if "EX_glc__D_e" in medium:
        medium["EX_glc__D_e"] = 5.0
        model.medium = medium
        sol2 = model.optimize()
        print("Growth after limiting glucose:", sol2.objective_value)
    else:
        print("Model has no EX_glc__D_e in medium; skipping medium edit.")

    # 7) Flux sampling (small n for quick demo)
    print("\n=== Flux Sampling ===")
    samples = sample(model, n=200, method="optgp")
    print(samples.head())

if __name__ == "__main__":
    main()
```

Run:

```bash
python cobrapy_example.py
```

## Common Workflows

### Workflow 1: Load Model and Predict Growth

```python
from cobra.io import load_model

# Load model
model = load_model("ecoli")

# Run FBA
solution = model.optimize()
print(f"Growth rate: {solution.objective_value:.3f} /h")

# Show active pathways
print(solution.fluxes[solution.fluxes.abs() > 1e-6])
```

### Workflow 2: Gene Knockout Screen

```python
from cobra.io import load_model
from cobra.flux_analysis import single_gene_deletion

# Load model
model = load_model("ecoli")

# Perform single gene deletions
results = single_gene_deletion(model)

# Find essential genes (growth < threshold)
essential_genes = results[results["growth"] < 0.01]
print(f"Found {len(essential_genes)} essential genes")

# Find genes with minimal impact
neutral_genes = results[results["growth"] > 0.9 * solution.objective_value]
```

### Workflow 3: Media Optimization

```python
from cobra.io import load_model
from cobra.medium import minimal_medium

# Load model
model = load_model("ecoli")

# Calculate minimal medium for 50% of max growth
target_growth = model.slim_optimize() * 0.5
min_medium = minimal_medium(
    model,
    target_growth,
    minimize_components=True
)

print(f"Minimal medium components: {len(min_medium)}")
print(min_medium)
```

### Workflow 4: Flux Uncertainty Analysis

```python
from cobra.io import load_model
from cobra.flux_analysis import flux_variability_analysis
from cobra.sampling import sample

# Load model
model = load_model("ecoli")

# First check flux ranges at optimality
fva = flux_variability_analysis(model, fraction_of_optimum=1.0)

# For reactions with large ranges, sample to understand distribution
samples = sample(model, n=1000)

# Analyze specific reaction
reaction_id = "PFK"
import matplotlib.pyplot as plt
samples[reaction_id].hist(bins=50)
plt.xlabel(f"Flux through {reaction_id}")
plt.ylabel("Frequency")
plt.show()
```

### Workflow 5: Context Manager for Temporary Changes

Use context managers to make temporary modifications:
```python
# Model remains unchanged outside context
with model:
    # Temporarily change objective
    model.objective = "ATPM"

    # Temporarily modify bounds
    model.reactions.EX_glc__D_e.lower_bound = -5.0

    # Temporarily knock out genes
    model.genes.b0008.knock_out()

    # Optimize with changes
    solution = model.optimize()
    print(f"Modified growth: {solution.objective_value}")

# All changes automatically reverted
solution = model.optimize()
print(f"Original growth: {solution.objective_value}")
```

## Key Concepts

### DictList Objects
Models use `DictList` objects for reactions, metabolites, and genes - behaving like both lists and dictionaries:
```python
# Access by index
first_reaction = model.reactions[0]

# Access by ID
pfk = model.reactions.get_by_id("PFK")

# Query methods
atp_reactions = model.reactions.query("atp")
```

### Flux Constraints
Reaction bounds define feasible flux ranges:
- **Irreversible**: `lower_bound = 0, upper_bound > 0`
- **Reversible**: `lower_bound < 0, upper_bound > 0`
- Set both bounds simultaneously with `.bounds` to avoid inconsistencies

### Gene-Reaction Rules (GPR)
Boolean logic linking genes to reactions:
```python
# AND logic (both required)
reaction.gene_reaction_rule = "gene1 and gene2"

# OR logic (either sufficient)
reaction.gene_reaction_rule = "gene1 or gene2"

# Complex logic
reaction.gene_reaction_rule = "(gene1 and gene2) or (gene3 and gene4)"
```

### Exchange Reactions
Special reactions representing metabolite import/export:
- Named with prefix `EX_` by convention
- Positive flux = secretion, negative flux = uptake
- Managed through `model.medium` dictionary

## Implementation Details

### 5.1 Core optimization model (FBA)
- COBRApy formulates a **linear program (LP)**:
  - **Mass balance** (steady state): \( S \cdot v = 0 \)
  - **Bounds**: \( l \le v \le u \)
  - **Objective**: maximize (or minimize) a linear function \( c^\top v \) (e.g., biomass reaction flux)
- `model.optimize()` solves the LP and returns a `Solution` with:
  - `solution.status` (e.g., `optimal`)
  - `solution.objective_value`
  - `solution.fluxes` (pandas Series of reaction fluxes)

### 5.2 Reaction directionality and bounds
- Irreversible reactions typically use `lower_bound = 0`.
- Reversible reactions allow negative flux: `lower_bound < 0`.
- Use `reaction.bounds = (lb, ub)` to set both consistently.

### 5.3 Gene-Protein-Reaction (GPR) rules
- `reaction.gene_reaction_rule` encodes Boolean logic:
  - `"gene1 and gene2"` means both genes required.
  - `"gene1 or gene2"` means either gene sufficient.
- Knockouts propagate through GPR logic to constrain affected reactions.

### 5.4 FVA parameters
- `flux_variability_analysis(model, fraction_of_optimum=x)` constrains the objective to be at least `x * optimum` before computing per-reaction min/max.
- `loopless=True` attempts to remove thermodynamically infeasible loops (typically more expensive).

### 5.5 Context manager for temporary edits
- `with model:` creates a reversible sandbox:
  - changes to objectives, bounds, knockouts, and reaction sets revert automatically on exit.
- This prevents accidental state carryover across analyses.

### 5.6 Flux sampling
- Sampling explores the feasible polytope defined by constraints.
- `sample(..., method="optgp")` uses OptGP (often parallelizable); `method="achr"` uses ACHR.
- For numerical stability, validate samples when needed (e.g., via `OptGPSampler.validate`).

### 5.7 Medium handling
- `model.medium` is a dictionary mapping exchange reaction IDs to allowed uptake rates.
- You must **re-assign** the full dictionary after edits: `model.medium = medium`.

### 5.8 Gapfilling
- `gapfill(model, universal)` searches for a minimal set of reactions from `universal` that restores feasibility (commonly formulated as MILP/optimization with penalties).
- Use `with model:` when testing removals/additions to avoid permanently mutating the model.

## Best Practices

1. **Use context managers** for temporary modifications to avoid state management issues
2. **Validate models** before analysis using `model.slim_optimize()` to ensure feasibility
3. **Check solution status** after optimization - `optimal` indicates successful solve
4. **Use loopless FVA** when thermodynamic feasibility matters
5. **Set fraction_of_optimum** appropriately in FVA to explore suboptimal space
6. **Parallelize** computationally expensive operations (sampling, double deletions)
7. **Prefer SBML format** for model exchange and long-term storage
8. **Use slim_optimize()** when only objective value needed for performance
9. **Validate flux samples** to ensure numerical stability

## When Not to Use

- Do not use this skill when the required source data, identifiers, files, or credentials are missing.
- Do not use this skill when the user asks for fabricated results, unsupported claims, or out-of-scope conclusions.
- Do not use this skill when a simpler direct answer is more appropriate than the documented workflow.

## Required Inputs

- A clearly specified task goal aligned with the documented scope.
- All required files, identifiers, parameters, or environment variables before execution.
- Any domain constraints, formatting requirements, and expected output destination if applicable.

## Recommended Workflow

1. Validate the request against the skill boundary and confirm all required inputs are present.
2. Select the documented execution path and prefer the simplest supported command or procedure.
3. Produce the expected output using the documented file format, schema, or narrative structure.
4. Run a final validation pass for completeness, consistency, and safety before returning the result.

## Deterministic Output Rules

- Use the same section order for every supported request of this skill.
- Keep output field names stable and do not rename documented keys across examples.
- If a value is unavailable, emit an explicit placeholder instead of omitting the field.

## Output Contract

- Return a structured deliverable that is directly usable without reformatting.
- If a file is produced, prefer a deterministic output name such as `cobrapy_result.md` unless the skill documentation defines a better convention.
- Include a short validation summary describing what was checked, what assumptions were made, and any remaining limitations.

## Validation and Safety Rules

- Validate required inputs before execution and stop early when mandatory fields or files are missing.
- Do not fabricate measurements, references, findings, or conclusions that are not supported by the provided source material.
- Emit a clear warning when credentials, privacy constraints, safety boundaries, or unsupported requests affect the result.
- Keep the output safe, reproducible, and within the documented scope at all times.

## Troubleshooting

**Infeasible solutions**: Check medium constraints, reaction bounds, and model consistency
**Slow optimization**: Try different solvers (GLPK, CPLEX, Gurobi) via `model.solver`
**Unbounded solutions**: Verify exchange reactions have appropriate upper bounds
**Import errors**: Ensure correct file format and valid SBML identifiers

## Failure Handling

- If validation fails, explain the exact missing field, file, or parameter and show the minimum fix required.
- If an external dependency or script fails, surface the command path, likely cause, and the next recovery step.
- If partial output is returned, label it clearly and identify which checks could not be completed.

## Completion Checklist

- Confirm all required inputs were present and valid.
- Confirm the supported execution path completed without unresolved errors.
- Confirm the final deliverable matches the documented format exactly.
- Confirm assumptions, limitations, and warnings are surfaced explicitly.

## Quick Validation

Run this minimal verification path before full execution when possible:

```text
No local script validation step is required for this skill.
```

Expected output format:

```text
Result file: cobrapy_result.md
Validation summary: PASS/FAIL with brief notes
Assumptions: explicit list if any
```

## References

For detailed workflows and API patterns, refer to:
- `references/workflows.md` - Comprehensive step-by-step workflow examples
- `references/api_quick_reference.md` - Common function signatures and patterns

Official documentation: https://cobrapy.readthedocs.io/en/latest/

## Scope Reminder

- Core purpose: Constraint-based reconstruction and analysis (COBRA) for metabolic models; use when you need to simulate growth/production, analyze flux ranges, or run knockout and medium studies from SBML/JSON/YAML models.