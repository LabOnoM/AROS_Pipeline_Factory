---
cpcp_asset: true
---
# Feature Detection and Linking

## Overview

Feature detection identifies persistent signals (chromatographic peaks) in LC-MS data. Feature linking combines features across multiple samples for quantitative comparison.

## Feature Detection Basics

A feature represents a chromatographic peak characterized by:
- m/z value (mass-to-charge ratio)
- Retention time (RT)
- Intensity
- Quality score
- Convex hull (spatial extent in RT-m/z space)

## Feature Finding

### Feature Finder Multiples (FFM)

Standard algorithm for feature detection in centroided data:

```python
import pyopenms as ms

# Load centroided data
exp = ms.MSExperiment()
ms.MzMLFile().load("centroided.mzML", exp)

# Create feature finder
ff = ms.FeatureFinder()

# Get default parameters
params = ff.getParameters("centroided")

# Modify key parameters
params.setValue("mass_trace:mz_tolerance", 10.0)  # ppm
params.setValue("mass_trace:min_spectra", 7)  # Min scans per feature
params.setValue("isotopic_pattern:charge_low", 1)
params.setValue("isotopic_pattern:charge_high", 4)

# Run feature detection
features = ms.FeatureMap()
ff.run("centroided", exp, features, params, ms.FeatureMap())

print(f"Detected {features.size()} features")

# Save features
ms.FeatureXMLFile().store("features.featureXML", features)
```

### Feature Finder for Metabolomics

Optimized for small molecules:

```python
# Create feature finder for metabolomics
ff = ms.FeatureFinder()

# Get metabolomics-specific parameters
params = ff.getParameters("centroided")

# Configure for metabolomics
params.setValue("mass_trace:mz_tolerance", 5.0)  # Lower tolerance
params.setValue("mass_trace:min_spectra", 5)
params.setValue("isotopic_pattern:charge_low", 1)  # Mostly singly charged
params.setValue("isotopic_pattern:charge_high", 2)

# Run detection
features = ms.FeatureMap()
ff.run("centroided", exp, features, params, ms.FeatureMap())
```

## Accessing Feature Data

### Iterate Through Features

```python
# Load features
feature_map = ms.FeatureMap()
ms.FeatureXMLFile().load("features.featureXML", feature_map)

# Access individual features
for feature in feature_map:
    print(f"m/z: {feature.getMZ():.4f}")
    print(f"RT: {feature.getRT():.2f}")
    print(f"Intensity: {feature.getIntensity():.0f}")
    print(f"Charge: {feature.getCharge()}")
    print(f"Quality: {feature.getOverallQuality():.3f}")
    print(f"Width (RT): {feature.getWidth():.2f}")

    # Get convex hull
    hull = feature.getConvexHull()
    print(f"Hull points: {hull.getHullPoints().size()}")
```

### Feature Subordinates (Isotope Pattern)

```python
# Access isotopic pattern
for feature in feature_map:
    # Get subordinate features (isotopes)
    subordinates = feature.getSubordinates()

    if subordinates:
        print(f"Main feature m/z: {feature.getMZ():.4f}")
        for sub in subordinates:
            print(f"  Isotope m/z: {sub.getMZ():.4f}")
            print(f"  Isotope intensity: {sub.getIntensity():.0f}")
```

### Export to Pandas

```python
# Example of how to export feature data to a Pandas DataFrame
# (Implementation details would go here)
```