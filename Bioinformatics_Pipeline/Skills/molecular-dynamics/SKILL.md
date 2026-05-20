---
name: molecular-dynamics
description: Run and analyze molecular dynamics simulations with OpenMM and MDAnalysis. Set up protein/small molecule systems, define force fields, run energy minimization and production MD, analyze trajectories (RMSD, RMSF, contact maps, free energy surfaces). For structural biology, drug binding, and biophysics.
license: MIT
metadata:
    skill-author: Kuan-lin Huang
---

# Molecular Dynamics

## Overview

Molecular dynamics (MD) simulation computationally models the time evolution of molecular systems by integrating Newton's equations of motion. This skill covers two complementary tools:

- **OpenMM** (https://openmm.org/): High-performance MD simulation engine with GPU support, Python API, and flexible force field support
- **MDAnalysis** (https://mdanalysis.org/): Python library for reading, writing, and analyzing MD trajectories from all major simulation packages

**Installation:**
```bash
conda install -c conda-forge openmm mdanalysis nglview
# or
pip install openmm mdanalysis
```

## When to Use This Skill

Use molecular dynamics when:

- **Protein stability analysis**: How does a mutation affect protein dynamics?
- **Drug binding simulations**: Characterize binding mode and residence time of a ligand
- **Conformational sampling**: Explore protein flexibility and conformational changes
- **Protein-protein interaction**: Model interface dynamics and binding energetics
- **RMSD/RMSF analysis**: Quantify structural fluctuations from a reference structure
- **Free energy estimation**: Compute binding free energy or conformational free energy
- **Membrane simulations**: Model proteins in lipid bilayers
- **Intrinsically disordered proteins**: Study IDR conformational ensembles

## Core Workflow: OpenMM Simulation

```python
from openmm.app import *
from openmm import *
from openmm.unit import *
import sys
import MDAnalysis as mda

def prepare_system_from_pdb(pdb_file, forcefield_name="amber14-all.xml",
                              water_model="amber14/tip3pfb.xml"):
    """
    Prepare an OpenMM system from a PDB file.

    Args:
        pdb_file: Path to cleaned PDB file (use PDBFixer for raw PDB files)
        forcefield_name: Force field XML file
        water_model: Water model XML file

    Returns:
        pdb, forcefield, system, topology, positions (for further steps)
    """
    # Load PDB
    pdb = PDBFile(pdb_file)

    # Load force field
    forcefield = ForceField(forcefield_name, water_model)

    # Add hydrogens and solvate
    modeller = Modeller(pdb.topology, pdb.positions)
    modeller.addHydrogens(forcefield)

    # Add solvent box (10 Å padding, 150 mM NaCl)
    modeller.addSolvent(
        forcefield,
        model='tip3p',
        padding=10*angstroms,
        ionicStrength=0.15*molar
    )

    print(f"System: {modeller.topology.getNumAtoms()} atoms, "
          f"{modeller.topology.getNumResidues()} residues")

    # Create OpenMM System
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=PME,
                                     nonbondedCutoff=1.0*nanometers, constraints=HBonds)
    return pdb, forcefield, system, modeller.topology, modeller.positions

def minimize_energy(modeller_topology, initial_positions, system, output_pdb="minimized.pdb",
                    max_iterations=1000, tolerance=10.0):
    """
    Perform energy minimization on the system.

    Args:
        modeller_topology: OpenMM Topology object
        initial_positions: Initial positions from Modeller
        system: OpenMM System
        output_pdb: Path to save minimized structure
        max_iterations: Maximum minimization steps
        tolerance: Convergence criterion in kJ/mol/nm

    Returns:
        simulation: OpenMM Simulation object after minimization
    """
    integrator = VerletIntegrator(1.0*femtoseconds) # A simple integrator for setup, minimization uses a different algorithm
    simulation = Simulation(modeller_topology, system, integrator)
    simulation.context.setPositions(initial_positions)

    # Attempt to set platform properties (from remote's fragments)
    try:
        properties = {'DeviceIndex': '0', 'Precision': 'mixed'}
        simulation.platform = Platform.getPlatformByName('CUDA')
        simulation.context.setPlatformProperties(properties)
    except Exception:
        try:
            simulation.platform = Platform.getPlatformByName('OpenCL')
            simulation.context.setPlatformProperties(properties)
        except Exception:
            print("CUDA or OpenCL not available, using CPU.")
            simulation.platform = Platform.getPlatformByName('CPU')

    print(f"Initial energy: {simulation.context.getState(getEnergy=True).getPotentialEnergy()}")
    simulation.minimizeEnergy(maxIterations=max_iterations, tolerance=tolerance)
    print(f"Minimized energy: {simulation.context.getState(getEnergy=True).getPotentialEnergy()}")

    positions = simulation.context.getState(getPositions=True).getPositions()
    PDBFile.writeFile(simulation.topology, positions, open(output_pdb, 'w'))
    return simulation

def run_nvt_equilibration(simulation, n_steps=50000, temperature=300*kelvin,
                          report_interval=1000, output_prefix="nvt"):
    """
    NVT equilibration: constant N, V, T.

    Args:
        simulation: OpenMM Simulation (after minimization)
        n_steps: Number of MD steps (50000 × 2fs = 100 ps)
        temperature: Temperature in Kelvin
        report_interval: Steps between data reports
        output_prefix: File prefix for trajectory and log

    Returns:
        simulation: OpenMM Simulation object after NVT
    """
    # (Optional: restraint heavy atoms)
    simulation.reporters.append(DCDReporter(f'{output_prefix}.dcd', report_interval))
    simulation.reporters.append(StateDataReporter(f'{output_prefix}.log', report_interval, step=True,
                                                potentialEnergy=True, kineticEnergy=True, totalEnergy=True,
                                                temperature=True, volume=True, density=True))
    print(f"Running NVT equilibration: {n_steps} steps ({n_steps*2/1000:.1f} ps)")
    simulation.step(n_steps)
    return simulation

def run_npt_production(simulation, n_steps=500000, temperature=300*kelvin,
                       pressure=1*bar, report_interval=5000, output_prefix="npt"):
    """
    NPT production run: constant N, P, T.

    Args:
        simulation: OpenMM Simulation (after NVT equilibration)
        n_steps: Production steps (500000 × 2fs = 1 ns)
        temperature: Temperature in Kelvin
        pressure: Pressure in bar
        report_interval: Steps between reports
        output_prefix: File prefix for trajectory and log

    Returns:
        simulation: OpenMM Simulation object after NPT
    """
    # Add a barostat for NPT
    system = simulation.context.getSystem()
    if not any(isinstance(force, MonteCarloBarostat) for force in system.getForces()):
        system.addForce(MonteCarloBarostat(pressure, temperature))
        simulation.context.reinitialize(preserveState=True) # Reinitialize context after adding force

    simulation.reporters.append(DCDReporter(f'{output_prefix}.dcd', report_interval))
    simulation.reporters.append(StateDataReporter(f'{output_prefix}.log', report_interval, step=True,
                                                potentialEnergy=True, kineticEnergy=True, totalEnergy=True,
                                                temperature=True, volume=True, density=True, pressure=True))
    print(f"Running NPT production: {n_steps} steps ({n_steps*2/1000000:.2f} ns)")
    simulation.step(n_steps)
    return simulation

def load_trajectory(topology_file, trajectory_file):
    """
    Load an MD trajectory using MDAnalysis.

    Args:
        topology_file: PDB, PSF, or other topology file
        trajectory_file: DCD, XTC, TRR, or other trajectory

    Returns:
        u: MDAnalysis Universe object
    """
    u = mda.Universe(topology_file, trajectory_file)
    print(f"Universe: {u.atoms.n_atoms} atoms, {u.trajectory.n_frames} frames")
    print(f"Time range: 0 to {u.trajectory.totaltime:.0f} ps")
    return u
```