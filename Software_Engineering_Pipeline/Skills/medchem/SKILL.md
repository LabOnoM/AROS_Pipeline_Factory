---
name: medchem
description: Medicinal chemistry screening filters for compound prioritization. Apply drug-likeness rules, PAINS/structural alerts, and complexity metrics to triage and optimize compound libraries.
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---
---

## Overview

Medchem is a Python library for molecular filtering and prioritization in drug discovery. It applies established and novel molecular filters, structural alerts, and medicinal chemistry rules to efficiently triage and prioritize compound libraries. Use rules and filters as guidelines combined with domain expertise.

## When to Use This Skill

- Screening large compound libraries to quickly triage drug-like candidates (e.g., Lipinski/Veber + alerts).
- Flagging problematic chemotypes (e.g., PAINS, reactive/toxicophores, curated structural alerts) before follow-up assays.
- Prioritizing lead-optimization candidates with stricter criteria (lead-like rules, demerit systems, complexity caps).
- Enforcing property constraints (MW/logP/TPSA/rotatable bonds) for target-specific design windows (e.g., CNS).
- Identifying molecules containing specific functional groups/scaffolds (e.g., Michael acceptors, hinge binders) for SAR or risk assessment.
- Assessing compound quality and medicinal chemistry properties.
- Detecting reactive or problematic functional groups.
- Calculating molecular complexity metrics.

## Key Features

- **Drug-likeness and medchem rule sets**: Lipinski (Ro5), Veber, Oprea, CNS, lead-like (soft/strict), Rule of Three, REOS, Golden Triangle, etc.
- **PAINS and structural alert filtering**: Curated alert catalogs and pattern-based screening.
- **Curated industrial filter sets**: NIBR filters; Lilly demerit scoring with pass/fail thresholds.
- **Functional-group detection** via SMARTS-based group matchers (hinge binders, phosphate binders, Michael acceptors, reactive groups, custom patterns).
- **Named catalogs** of curated structures (functional groups, protecting groups, reagents, fragments) for matching and annotation.
- **Molecular complexity metrics** (e.g., Bertz/Whitlock/Barone-style) and threshold-based complexity filters.
- **Constraint-based filtering** for property windows (MW/logP/TPSA/RB, etc.).
- **Query language** to combine heterogeneous criteria (rules + alerts + numeric thresholds) into a single expression.

## Dependencies

- `medchem` (latest)
- `datamol` (latest)
- `pandas` (latest, for tabular workflows)

## Installation

```bash
uv pip install medchem
```

## Core Capabilities

### 1. Medicinal Chemistry Rules

Apply established drug-likeness rules to molecules using the `medchem.rules` module.

**Available Rules:**

- Rule of Five (Lipinski)
- Rule of Oprea
- Rule of CNS
- Rule of leadlike (soft and strict)
- Rule of three
- Rule of Reos
- Rule of drug
- Rule of Veber
- Golden triangle
- PAINS filters

**Single Rule Application:**

```python
import medchem as mc

# Apply Rule of Five to a SMILES string
smiles = "CC(=O)OC1=CC=CC=C1C(=O)O"  # Aspirin
passes = mc.rules.basic_rules.rule_of_five(smiles)
# Returns: True

# Check specific rules
passes_oprea = mc.rules.basic_rules.rule_of_oprea(smiles)
passes_cns = mc.rules.basic_rules.rule_of_cns(smiles)
```

**Multiple Rules with RuleFilters:**

```python
import datamol as dm
import medchem as mc

# Load molecules
smiles_list = ["CC(=O)OC1=CC=CC=C1C(=O)O", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "c1ccccc1"]
mols = [dm.to_mol(smiles) for smiles in smiles_list]

# Create filter with multiple rules
rfilter = mc.rules.RuleFilters(
    rule_list=[
        "rule_of_five",
        "rule_of_oprea",
        "rule_of_cns",
        "rule_of_leadlike_soft"
    ]
)

# Apply filters with parallelization
results = rfilter(
    mols=mols,
    n_jobs=-1,  # Use all CPU cores
    progress=False
)
```

**Result Format:** Results are returned as dictionaries with pass/fail status and detailed information for each rule.

### 2. Structural Alert Filters

Detect potentially problematic structural patterns using the `medchem.structural` module. Alert systems are primarily SMARTS/pattern-based matchers curated from literature/industrial practice.

**Available Filters:**

1. **Common Alerts** - General structural alerts derived from ChEMBL curation and literature
2. **NIBR Filters** - Novartis Institutes for BioMedical Research filter set
3. **Lilly Demerits** - Eli Lilly's demerit-based system (275 rules, molecules rejected at >100 demerits)

**Common Alerts:**

```python
import datamol as dm
import medchem as mc

# Create filter
alert_filter = mc.structural.CommonAlertsFilters()

# Check single molecule
mol = dm.to_mol("c1ccccc1")
has_alerts, details = alert_filter.check_mol(mol)

# Batch filtering with parallelization
mol_list = [dm.to_mol("c1ccccc1"), dm.to_mol("CC(=O)OC1=CC=CC=C1C(=O)O")]
results = alert_filter(
    mols=mol_list,
    n_jobs=-1,
    progress=False
)
```

**NIBR Filters:**

```python
import datamol as dm
import medchem as mc

# Apply NIBR filters
mol_list = [dm.to_mol("c1ccccc1"), dm.to_mol("CC(=O)OC1=CC=CC=C1C(=O)O")]
nibr_filter = mc.structural.NIBRFilters()
results = nibr_filter(mols=mol_list, n_jobs=-1, progress=False)
```

**Lilly Demerits:**

```python
import datamol as dm
import medchem as mc

# Calculate Lilly demerits
mol_list = [dm.to_mol("c1ccccc1"), dm.to_mol("CC(=O)OC1=CC=CC=C1C(=O)O")]
lilly = mc.structural.LillyDemeritsFilters()
results = lilly(mols=mol_list, n_jobs=-1, progress=False)

# Each result includes demerit score and whether it passes (≤100 demerits)
```

### 3. Functional API for High-Level Operations

The `medchem.functional` module provides convenient functions for common workflows.

**Quick Filtering:**

```python
import datamol as dm
import medchem as mc

mol_list = [dm.to_mol("c1ccccc1"), dm.to_mol("CC(=O)OC1=CC=CC=C1C(=O)O")]

# Apply NIBR filters to a list
filter_ok = mc.functional.nibr_filter(
    mols=mol_list,
    n_jobs=-1
)

# Apply common alerts
alert_results = mc.functional.common_alerts_filter(
    mols=mol_list,
    n_jobs=-1
)
```

### 4. Chemical Groups Detection

Identify specific chemical groups and functional groups using `medchem.groups`.

**Available Groups:**

- Hinge binders
- Phosphate binders
- Michael acceptors
- Reactive groups
- Custom SMARTS patterns

**Usage:**

```python
import datamol as dm
import medchem as mc

# Create group detector
group = mc.groups.ChemicalGroup(groups=["hinge_binders"])

mol = dm.to_mol("c1ccccc1")
mol_list = [mol, dm.to_mol("CC(=O)OC1=CC=CC=C1C(=O)O")]
# Check for matches
has_matches = group.has_match(mol_list)

# Get detailed match information
matches = group.get_matches(mol)
```

### 5. Named Catalogs

Access curated collections of chemical structures through `medchem.catalogs`.

**Available Catalogs:**

- Functional groups
- Protecting groups
- Common reagents
- Standard fragments

**Usage:**

```python
import datamol as dm
import medchem as mc

# Access named catalogs
catalogs = mc.catalogs.NamedCatalogs

# Use catalog for matching
catalog = catalogs.get("functional_groups")
mol = dm.to_mol("c1ccccc1")
matches = catalog.get_matches(mol)
```

### 6. Molecular Complexity

Calculate complexity metrics that approximate synthetic accessibility using `medchem.complexity`.

**Common Metrics:**

- Bertz complexity
- Whitlock complexity
- Barone complexity

**Usage:**

```python
import datamol as dm
import medchem as mc

mol = dm.to_mol("c1ccccc1")
# Calculate complexity
complexity_score = mc.complexity.calculate_complexity(mol)

# Filter by complexity threshold
complex_filter = mc.complexity.ComplexityFilter(max_complexity=500)
mol_list = [mol, dm.to_mol("CC(=O)OC1=CC=CC=C1C(=O)O")]
results = complex_filter(mols=mol_list)
```

### 7. Constraints Filtering

Apply custom property-based constraints using `medchem.constraints`.

**Example Constraints:**

- Molecular weight ranges
- LogP bounds
- TPSA limits
- Rotatable bond counts

**Usage:**

```python
import datamol as dm
import medchem as mc

mol_list = [dm.to_mol("c1ccccc1"), dm.to_mol("CC(=O)OC1=CC=CC=C1C(=O)O")]
# Define constraints
constraints = mc.constraints.Constraints(
    mw_range=(200, 500),
    logp_range=(-2, 5),
    tpsa_max=140,
    rotatable_bonds_max=10
)

# Apply constraints
results = constraints(mols=mol_list, n_jobs=-1)
```

### 8. Medchem Query Language

Use a specialized query language for complex filtering criteria.

**Query Examples:**

```
# Molecules passing Ro5 AND not having common alerts
"rule_of_five AND NOT common_alerts"

# CNS-like molecules with low complexity
"rule_of_cns AND complexity < 400"

# Leadlike molecules without Lilly demerits
"rule_of_leadlike AND lilly_demerits == 0"
```

**Usage:**

```python
import datamol as dm
import medchem as mc

mol_list = [dm.to_mol("c1ccccc1"), dm.to_mol("CC(=O)OC1=CC=CC=C1C(=O)O")]
# Parse and apply query
query = mc.query.parse("rule_of_five AND NOT common_alerts")
results = query.apply(mols=mol_list, n_jobs=-1)
```

## Example Usage

```python
# End-to-end, runnable example:
# 1) load SMILES
# 2) apply Ro5 + Veber
# 3) apply common structural alerts
# 4) compute complexity and filter
# 5) export a CSV with decisions

import pandas as pd
import datamol as dm
import medchem as mc

smiles_list = [
    "CC(=O)OC1=CC=CC=C1C(=O)O",  # aspirin
    "CN1C=NC2=C1C(=O)N(C(=O)N2C)C",  # caffeine
    "c1ccccc1",  # benzene
]

df = pd.DataFrame({"smiles": smiles_list})
mols = [dm.to_mol(smi) for smi in df["smiles"]]

# 1) Drug-likeness rules
rule_filter = mc.rules.RuleFilters(rule_list=["rule_of_five", "rule_of_veber"])
rule_res = rule_filter(mols=mols, n_jobs=-1, progress=False)
df["passes_rules"] = rule_res["pass"]

# 2) Structural alerts
alerts = mc.structural.CommonAlertsFilters()
alert_res = alerts(mols=mols, n_jobs=-1, progress=False)
df["has_alerts"] = alert_res["has_alerts"]

# 3) Complexity (example threshold)
complex_filter = mc.complexity.ComplexityFilter(max_complexity=500)
complex_res = complex_filter(mols=mols, n_jobs=-1, progress=False)
df["passes_complexity"] = complex_res["pass"]

# 4) Final decision
df["keep"] = df["passes_rules"] & (~df["has_alerts"]) & df["passes_complexity"]

# 5) Save results
df.to_csv("medchem_screening_results.csv", index=False)
print(df)
```

## Workflow Patterns

### Pattern 1: Initial Triage of Compound Library

Filter a large compound collection to identify drug-like candidates.

```python
import datamol as dm
import medchem as mc
import pandas as pd

# Load compound library
df = pd.read_csv("compounds.csv")
mols = [dm.to_mol(smi) for smi in df["smiles"]]

# Apply primary filters
rule_filter = mc.rules.RuleFilters(rule_list=["rule_of_five", "rule_of_veber"])
rule_results = rule_filter(mols=mols, n_jobs=-1, progress=False)

# Apply structural alerts
alert_filter = mc.structural.CommonAlertsFilters()
alert_results = alert_filter(mols=mols, n_jobs=-1, progress=False)

# Combine results
df["passes_rules"] = rule_results["pass"]
df["has_alerts"] = alert_results["has_alerts"]
df["drug_like"] = df["passes_rules"] & ~df["has_alerts"]

# Save filtered compounds
filtered_df = df[df["drug_like"]]
filtered_df.to_csv("filtered_compounds.csv", index=False)
```

### Pattern 2: Lead Optimization Filtering

Apply stricter criteria during lead optimization.

```python
import datamol as dm
import medchem as mc

# Sample molecules
smiles_list = ["CC(=O)OC1=CC=CC=C1C(=O)O", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "c1ccccc1"]
candidate_mols = [dm.to_mol(smi) for smi in smiles_list]

# Create comprehensive filter
filters = {
    "rules": mc.rules.RuleFilters(rule_list=["rule_of_leadlike_strict"]),
    "alerts": mc.structural.NIBRFilters(),
    "lilly": mc.structural.LillyDemeritsFilters(),
    "complexity": mc.complexity.ComplexityFilter(max_complexity=400)
}

# Apply all filters
results = {}
for name, filt in filters.items():
    results[name] = filt(mols=candidate_mols, n_jobs=-1, progress=False)

# Identify compounds passing all filters
passes_all = all(r["pass"] for r in results.values())
```

### Pattern 3: Identify Specific Chemical Groups

Find molecules containing specific functional groups or scaffolds.

```python
import datamol as dm
import medchem as mc

# Sample molecules
smiles_list = ["CC(=O)OC1=CC=CC=C1C(=O)O", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "c1ccccc1"]
mol_list = [dm.to_mol(smi) for smi in smiles_list]

# Create group detector for multiple groups
group_detector = mc.groups.ChemicalGroup(
    groups=["hinge_binders", "phosphate_binders"]
)

# Screen library
matches = group_detector.get_all_matches(mol_list)

# Filter molecules with desired groups
mol_with_groups = [mol for mol, match in zip(mol_list, matches) if match]
```

## Implementation Details

- **Rule evaluation (`medchem.rules`)**
  - Rules are implemented as callable checks over SMILES or RDKit-like molecule objects (commonly via `datamol`).
  - `RuleFilters(rule_list=[...])` applies multiple rules and returns a structured result (typically including an overall `pass` plus per-rule details).
  - Typical use: start broad (Ro5/Veber), then tighten (CNS/lead-like) as project constraints become clearer.

- **Structural alerts (`medchem.structural`)**
  - Alert systems are primarily SMARTS/pattern-based matchers curated from literature/industrial practice.
  - `CommonAlertsFilters`, `NIBRFilters`, and `LillyDemeritsFilters` provide different philosophies:
    - **Common alerts**: general-purpose red flags.
    - **NIBR**: curated industrial filter set.
    - **Lilly demerits**: assigns penalties per matched rule; a common convention is reject if total demerits > 100.

- **Complexity (`medchem.complexity`)**
  - Complexity scores approximate synthetic difficulty / structural intricacy using established heuristics (e.g., Bertz/Whitlock/Barone-style metrics).
  - `ComplexityFilter(max_complexity=...)` converts a numeric score into a pass/fail gate for library triage.

- **Constraints (`medchem.constraints`)**
  - Property windows (MW/logP/TPSA/rotatable bonds, etc.) are applied as hard filters.
  - Use constraints to encode target-specific design hypotheses (e.g., CNS-like space) rather than universal “good/bad” judgments.

- **Groups and catalogs (`medchem.groups`, `medchem.catalogs`)**
  - Group detection is SMARTS-driven and returns boolean matches and/or match details (substructure hits).
  - Named catalogs provide curated sets for consistent annotation and matching across projects.

- **Parallelization**
  - Most batch APIs accept `n_jobs`; set `n_jobs=-1` to use all available CPU cores for large libraries.

## Best Practices

1. **Context Matters**: Don't blindly apply filters. Understand the biological target and chemical space.
2. **Combine Multiple Filters**: Use rules, structural alerts, and domain knowledge together for better decisions.
3. **Use Parallelization**: For large datasets (>1000 molecules), always use `n_jobs=-1` for parallel processing.
4. **Iterative Refinement**: Start with broad filters (Ro5), then apply more specific criteria (CNS, leadlike) as needed.
5. **Document Filtering Decisions**: Track which molecules were filtered out and why for reproducibility.
6. **Validate Results**: Remember that marketed drugs often fail standard filters—use these as guidelines, not absolute rules.
7. **Consider Prodrugs**: Molecules designed as prodrugs may intentionally violate standard medicinal chemistry rules.

## Resources

### references/api_guide.md
Comprehensive API reference covering all medchem modules with detailed function signatures, parameters, and return types.

### references/rules_catalog.md
Complete catalog of available rules, filters, and alerts with descriptions, thresholds, and literature references.

### scripts/filter_molecules.py
Production-ready script for batch filtering workflows. Supports multiple input formats (CSV, SDF, SMILES), configurable filter combinations, and detailed reporting.

**Usage:**
```bash
python scripts/filter_molecules.py input.csv --rules rule_of_five,rule_of_cns --alerts nibr --output filtered.csv
```

## Documentation

Official documentation: https://medchem-docs.datamol.io/
GitHub repository: https://github.com/datamol-io/medchem