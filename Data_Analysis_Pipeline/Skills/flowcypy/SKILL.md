---
name: flowcypy
description: Use this skill to computationally model flow cytometer hardware limits, model Photomultiplier Tube (PMT) or APD voltage/gain transfer distributions, run virtual flow cytometry simulations using Python, simulate fluorescent or scattering responses of extracellular vesicles and cells, and generate 'forward modeled' synthetic FCS data or diagnostic event plots from physical inputs. Make sure to use this whenever the user asks about simulating cytometer voltage settings, determining machine performance via algorithmic modeling, or virtual flow cell experiments using FlowCyPy.
---

# FlowCyPy Simulation Skill

This skill explains how to build a virtual Flow Cytometer pipeline in Python using the `FlowCyPy` framework. This generates highly realistic signal responses by physically modeling fluidics, optical scattering (via PyMieSim), and analog-digital electronics (detectors like PMTs/APDs + Shot/Thermal noise elements).

## Standard Architecture

FlowCyPy relies on a four-stage architecture:
1.  **Fluidics**: Define `FlowCell`, `ScattererCollection`, and custom EV/cell populations (size distributions, refractive indices).
2.  **OptoElectronics**: Define the lasers (`source`), physical analog processing (`circuits`), detectors (e.g. `Detector(phi=90, NA=1.1, responsivity=...)`), and `Amplifier` containing specific current/voltage noise densities to simulate gain variables.
3.  **DigitalProcessing**: Set up discriminators (e.g., thresholding 4-sigma over background on SSC) and `PeakLocator` algorithms.
4.  **FlowCytometer**: Assemble and `.run()` to trigger data acquisition, resulting in a dataset analogous to an FCS file with physical truth metrics.

## Example Usage: Modeling Voltage / PMT Gain Performance 

If the user wants to understand how PMT gain adjustments influence cell population resolving capabilities, construct the analog section correctly by tweaking `Amplifier(gain=...)` or `responsivity`, and add `current_noise_density`/`voltage_noise_density` inputs.

```python
# A typical FlowCyPy Python simulation script wrapper:
from FlowCyPy.units import ureg
from FlowCyPy.fluidics import Fluidics, FlowCell, ScattererCollection, populations, distributions, SampleFlowRate, SheathFlowRate
from FlowCyPy.opto_electronics import OptoElectronics, Amplifier, Digitizer, Detector, source, circuits
from FlowCyPy.digital_processing import DigitalProcessing, peak_locator, discriminator
from FlowCyPy import FlowCytometer

# 1. Create Scatter populations (cells)
flow_cell = FlowCell(sample_volume_flow=SampleFlowRate.MEDIUM.value, sheath_volume_flow=SheathFlowRate.MEDIUM.value, width=400 * ureg.micrometer, height=150 * ureg.micrometer)
scatterers = ScattererCollection()

pop = populations.SpherePopulation(
    name="Cell", 
    medium_refractive_index=distributions.Delta(1.33),
    diameter=distributions.RosinRammler(scale=200 * ureg.nanometer, shape=10), 
    refractive_index=distributions.Normal(mean=1.44, standard_deviation=0.002, low_cutoff=1.33), 
    concentration=1e10 * ureg.particle / ureg.milliliter,
    sampling_method=populations.ExplicitModel()
)
scatterers.add_population(pop)
fluidics = Fluidics(scatterer_collection=scatterers, flow_cell=flow_cell)

# 2. Configure PMT Gain / Optics
detectors = [Detector(name="FSC", phi_angle=0*ureg.degree, numerical_aperture=0.3, responsivity=1.0*ureg.ampere/ureg.watt)]
ampl = Amplifier(
    gain=10 * ureg.volt / ureg.ampere, # ADJUST PMT gain here!
    bandwidth=10 * ureg.megahertz,
    voltage_noise_density=0.1 * ureg.nanovolt / ureg.sqrt_hertz,
    current_noise_density=0.0 * ureg.femtoampere / ureg.sqrt_hertz
)
opto_electronics = OptoElectronics(
    digitizer=Digitizer(sampling_rate=60 * ureg.megahertz, bit_depth=14, use_auto_range=True, channel_range_mode="shared"),
    detectors=detectors,
    source=source.Gaussian(waist_z=10e-6 * ureg.meter, waist_y=60e-6 * ureg.meter, wavelength=405 * ureg.nanometer, optical_power=200 * ureg.milliwatt, rin=-140 * ureg.dB_per_Hz, bandwidth=10 * ureg.megahertz),
    amplifier=ampl,
    analog_processing=[circuits.BesselLowPass(cutoff_frequency=2 * ureg.megahertz, order=4, gain=2)]
)

# 3. Simulate and save
digital_processing = DigitalProcessing(
    discriminator=discriminator.FixedWindow(trigger_channel="FSC", threshold="4sigma", pre_buffer=40, post_buffer=40, max_triggers=-1),
    peak_algorithm=peak_locator.GlobalPeakLocator()
)
cytometer = FlowCytometer(fluidics=fluidics, background_power=0.001 * ureg.milliwatt)
run_record = cytometer.run(opto_electronics=opto_electronics, digital_processing=digital_processing, run_time=1 * ureg.millisecond)

run_record.plot_analog(show=False, save_as="sim_analog.png")
```

## Best Practices
- **Variables**: Always use the built-in `ureg` unit registry (e.g., `ureg.micrometer`, `ureg.milliwatt`) for physical values (laser power, fluid volume, gain voltage).
- **Evaluating Results**: Rather than trying to change hardware settings *after* obtaining `.fcs` files (which is physically impossible), use this skill to run iterative *forward models* demonstrating what the same cell population looks like under varying noise, detector NA, or amplifier gain topologies.
