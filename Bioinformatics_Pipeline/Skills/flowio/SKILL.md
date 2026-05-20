---
name: flowio
description: Parse Flow Cytometry Standard (FCS) files v2.0–3.1 and extract events/metadata for preprocessing workflows (e.g., when you need NumPy arrays, channel info, or CSV/DataFrame export from cytometry files).
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---

# FlowIO: Flow Cytometry Standard File Handler

## Overview

FlowIO is a lightweight Python library for reading and writing Flow Cytometry Standard (FCS) files. Parse FCS metadata, extract event data, and create new FCS files with minimal dependencies. The library supports FCS versions 2.0, 3.0, and 3.1, making it ideal for backend services, data pipelines, and basic cytometry file operations.

## When to Use This Skill

This skill should be used when:

- You need to read FCS v2.0/3.0/3.1 files and extract event matrices for downstream preprocessing.
- You want to inspect or validate FCS metadata (TEXT segment) without loading event data (memory-efficient parsing).
- You need channel definitions (PnN/PnS), ranges (PnR), and automatic identification of scatter/fluorescence/time channels.
- You need to handle problematic FCS files with offset inconsistencies or multi-dataset content.
- You want to export cytometry events to CSV/Pandas DataFrame or write new/modified FCS files.

**Related Tools:** For advanced flow cytometry analysis including compensation, gating, and FlowJo/GatingML support, consider FlowKit library as a companion to FlowIO.

## Key Features

- **FCS parsing (v2.0–3.1):** Reads HEADER/TEXT/DATA and optional ANALYSIS segments.
- **Event extraction to NumPy:** Returns event data as `ndarray` with shape `(events, channels)`.
- **Optional preprocessing:** Applies standard FCS transformations (gain/log/time scaling) when enabled.
- **Metadata access:** Exposes TEXT keywords and common instrument/acquisition fields.
- **Channel utilities:** Provides PnN/PnS labels, ranges, and indices for scatter/fluorescence/time channels.
- **Robust parsing options:** Flags for offset discrepancy handling and null-channel exclusion.
- **Multi-dataset support:** Detects and reads files containing multiple datasets.
- **FCS writing:** Create new FCS files from arrays and optionally preserve/override metadata.

## Installation

```bash
uv pip install flowio
```

Requires Python 3.9 or later.

## Example Usage

```python
"""
End-to-end example:
1) Read an FCS file (metadata + events)
2) Convert to a Pandas DataFrame and export CSV
3) Filter events and write a new FCS file
4) Handle multi-dataset files
"""

from pathlib import Path

import numpy as np
import pandas as pd

from flowio import (
    FlowData,
    create_fcs,
    read_multiple_data_sets,
    MultipleDataSetsError,
    FCSParsingError,
    DataOffsetDiscrepancyError,
)

FCS_PATH = "sample.fcs"

def read_fcs_safely(path: str) -> FlowData:
    try:
        return FlowData(path)
    except DataOffsetDiscrepancyError:
        # Common workaround for files with inconsistent offsets
        return FlowData(path, ignore_offset_discrepancy=True)
    except FCSParsingError:
        # Looser mode if the file is malformed
        return FlowData(path, ignore_offset_error=True)

def main() -> None:
    # --- 1) Read file (single dataset) ---
    try:
        flow = read_fcs_safely(FCS_PATH)
    except MultipleDataSetsError:
        # --- 4) Multi-dataset handling ---
        datasets = read_multiple_data_sets(FCS_PATH)
        flow = datasets[0]  # pick the first dataset for this demo

    print("File:", getattr(flow, "name", Path(FCS_PATH).name))
    print("FCS version:", flow.version)
    print("Events:", flow.event_count)
    print("Channels:", flow.channel_count)
    print("PnN labels:", flow.pnn_labels)

    # Metadata (TEXT segment)
    print("Instrument ($CYT):", flow.text.get("$CYT", "N/A"))
    print("Acquisition date ($DATE):", flow.text.get("$DATE", "N/A"))

    # --- 2) Events -> NumPy -> DataFrame -> CSV ---
    events = flow.as_array(preprocess=True)  # default preprocessing behavior
    df = pd.DataFrame(events, columns=flow.pnn_labels)
    df.to_csv("events.csv", index=False)
    print("Wrote CSV:", "events.csv")

    # --- 3) Filter and write a new FCS ---
    # Example: threshold on first scatter channel if available, else channel 0
    fsc_idx = flow.scatter_indices[0] if getattr(flow, "scatter_indices", []) else 0
    threshold = np.percentile(events[:, fsc_idx], 50)  # median threshold
    mask = events[:, fsc_idx] > threshold
    filtered = events[mask]

    create_fcs(
        "filtered.fcs",
        filtered,
        flow.pnn_labels,
        opt_channel_names=flow.pns_labels,
        metadata={**flow.text, "$SRC": "Filtered via FlowIO example"},
    )
    print("Wrote FCS:", "filtered.fcs")

    # --- Metadata-only read (memory efficient) ---
    meta_only = FlowData(FCS_PATH, only_text=True)
    print("Metadata-only read: $DATE =", meta_only.text.get("$DATE", "N/A"))

if __name__ == "__main__":
    main()
```

## Core Concepts

### Data Model and Segments

An FCS file is organized into segments:

- **HEADER:** FCS version and byte offsets for other segments.
- **TEXT:** Keyword/value metadata (e.g., `$DATE`, `$CYT`, `$PnN`, `$PnS`, `$PnR`, `$PnG`, `$PnE`).
- **DATA:** Event matrix encoded as integer/float/double/ASCII depending on file keywords.
- **ANALYSIS (optional):** Post-processing results if present.

In FlowIO, these are exposed via `FlowData` attributes such as:
- `flow.header` (HEADER info)
- `flow.text` (TEXT keyword dictionary)
- `flow.analysis` (ANALYSIS keyword dictionary, if present)
- `flow.as_array(...)` (decoded event matrix)

### Preprocessing (`as_array(preprocess=True)`)

When preprocessing is enabled, FlowIO applies common FCS transformations:

1. **Gain scaling (PnG):** Values are multiplied by the per-parameter gain.
2. **Log/exponential transform (PnE):** If present, applies:
   - `value = a * 10^(b * raw_value)` where `PnE = "a,b"`.
3. **Time scaling:** If a time channel is detected, values may be scaled into appropriate units.

To disable all transformations and obtain raw decoded values:
- `flow.as_array(preprocess=False)`

### Channel Identification

FlowIO provides convenience indices for common channel types:

- `flow.scatter_indices` (e.g., FSC/SSC)
- `flow.fluoro_indices` (fluorescence channels)
- `flow.time_index` (time channel index or `None`)

These indices can be used to slice the event matrix:
- `events[:, flow.scatter_indices]`
- `events[:, flow.fluoro_indices]`

### Handling Problematic Files (Offsets and Null Channels)

Some files contain inconsistent offsets between HEADER and TEXT:

- `ignore_offset_discrepancy=True` to tolerate HEADER/TEXT offset mismatch.
- `use_header_offsets=True` to prefer HEADER offsets.
- `ignore_offset_error=True` to bypass offset-related failures more aggressively.

To exclude known null/empty channels during parsing:
- `FlowData(path, null_channel_list=[...])`

### Multi-Dataset Files

If a file contains multiple datasets, constructing `FlowData(path)` may raise `MultipleDataSetsError`. Use:

- `read_multiple_data_sets(path)` to load all datasets, or
- `FlowData(path, nextdata_offset=...)` to load a specific dataset using `$NEXTDATA` offsets.

### Writing FCS

Two common patterns:

- **Write metadata-only changes:** `flow.write_fcs("out.fcs", metadata={...})`
- **Modify event data:** extract array → modify → `create_fcs(...)` to generate a new file (FlowIO does not modify event data in-place).

## Common Use Cases

### Inspecting FCS File Contents

Quick exploration of FCS file structure:

```python
from flowio import FlowData

flow = FlowData('unknown.fcs')

print("=" * 50)
print(f"File: {flow.name}")
print(f"Version: {flow.version}")
print(f"Size: {flow.file_size:,} bytes")
print("=" * 50)

print(f"\nEvents: {flow.event_count:,}")
print(f"Channels: {flow.channel_count}")

print("\nChannel Information:")
for i, (pnn, pns) in enumerate(zip(flow.pnn_labels, flow.pns_labels)):
    ch_type = "scatter" if i in flow.scatter_indices else \
              "fluoro" if i in flow.fluoro_indices else \
              "time" if i == flow.time_index else "other"
    print(f"  [{i}] {pnn:10s} | {pns:30s} | {ch_type}")

print("\nKey Metadata:")
for key in ['$DATE', '$BTIM', '$ETIM', '$CYT', '$INST', '$SRC']:
    value = flow.text.get(key, 'N/A')
    print(f"  {key:15s}: {value}")
```

### Batch Processing Multiple Files

Process a directory of FCS files:

```python
from pathlib import Path
from flowio import FlowData
import pandas as pd

# Find all FCS files
fcs_files = list(Path('data/').glob('*.fcs'))

# Extract summary information
summaries = []
for fcs_path in fcs_files:
    try:
        flow = FlowData(str(fcs_path), only_text=True)
        summaries.append({
            'filename': fcs_path.name,
            'version': flow.version,
            'events': flow.event_count,
            'channels': flow.channel_count,
            'date': flow.text.get('$DATE', 'N/A')
        })
    except Exception as e:
        print(f"Error processing {fcs_path.name}: {e}")

# Create summary DataFrame
df = pd.DataFrame(summaries)
print(df)
```

### Converting FCS to CSV

Export event data to CSV format:

```python
from flowio import FlowData
import pandas as pd

# Read FCS file
flow = FlowData('sample.fcs')

# Convert to DataFrame
df = pd.DataFrame(
    flow.as_array(),
    columns=flow.pnn_labels
)

# Add metadata as attributes
df.attrs['fcs_version'] = flow.version
df.attrs['instrument'] = flow.text.get('$CYT', 'Unknown')

# Export to CSV
df.to_csv('output.csv', index=False)
print(f"Exported {len(df)} events to CSV")
```

### Filtering Events and Re-exporting

Apply filters and save filtered data:

```python
from flowio import FlowData, create_fcs
import numpy as np

# Read original file
flow = FlowData('sample.fcs')
events = flow.as_array(preprocess=False)

# Apply filtering (example: threshold on first channel)
fsc_idx = 0
threshold = 500
mask = events[:, fsc_idx] > threshold
filtered_events = events[mask]

print(f"Original events: {len(events)}")
print(f"Filtered events: {len(filtered_events)}")

# Create new FCS file with filtered data
create_fcs('filtered.fcs',
           filtered_events,
           flow.pnn_labels,
           opt_channel_names=flow.pns_labels,
           metadata={**flow.text, '$SRC': 'Filtered data'})
```

### Extracting Specific Channels

Extract and process specific channels:

```python
from flowio import FlowData
import numpy as np

flow = FlowData('sample.fcs')
events = flow.as_array()

# Extract fluorescence channels only
fluoro_indices = flow.fluoro_indices
fluoro_data = events[:, fluoro_indices]
fluoro_names = [flow.pnn_labels[i] for i in fluoro_indices]

print(f"Fluorescence channels: {fluoro_names}")
print(f"Shape: {fluoro_data.shape}")

# Calculate statistics per channel
for i, name in enumerate(fluoro_names):
    channel_data = fluoro_data[:, i]
    print(f"\n{name}:")
    print(f"  Mean: {channel_data.mean():.2f}")
    print(f"  Median: {np.median(channel_data):.2f}")
    print(f"  Std Dev: {channel_data.std():.2f}")
```

## Error Handling

Handle common FlowIO exceptions appropriately.

```python
from flowio import (
    FlowData,
    FCSParsingError,
    DataOffsetDiscrepancyError,
    MultipleDataSetsError
)

try:
    flow = FlowData('sample.fcs')
    events = flow.as_array()

except FCSParsingError as e:
    print(f"Failed to parse FCS file: {e}")
    # Try with relaxed parsing
    flow = FlowData('sample.fcs', ignore_offset_error=True)

except DataOffsetDiscrepancyError as e:
    print(f"Offset discrepancy detected: {e}")
    # Use ignore_offset_discrepancy parameter
    flow = FlowData('sample.fcs', ignore_offset_discrepancy=True)

except MultipleDataSetsError as e:
    print(f"Multiple datasets detected: {e}")
    # Use read_multiple_data_sets instead
    from flowio import read_multiple_data_sets
    datasets = read_multiple_data_sets('sample.fcs')

except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

1. **Memory Efficiency:** Use `only_text=True` when event data is not needed
2. **Error Handling:** Wrap file operations in try-except blocks for robust code
3. **Multi-Dataset Detection:** Check for MultipleDataSetsError and use appropriate function
4. **Preprocessing Control:** Explicitly set `preprocess` parameter based on analysis needs
5. **Offset Issues:** If parsing fails, try `ignore_offset_discrepancy=True` parameter
6. **Channel Validation:** Verify channel counts and names match expectations before processing
7. **Metadata Preservation:** When modifying files, preserve original TEXT segment keywords

## Advanced Topics

### Detailed API Reference

For comprehensive API documentation including all parameters, methods, exceptions, and FCS keyword reference, consult the detailed reference file:

**Read:** `references/api_reference.md`

The reference includes:
- Complete FlowData class documentation
- All utility functions (read_multiple_data_sets, create_fcs)
- Exception classes and handling
- FCS file structure details
- Common TEXT segment keywords
- Extended example workflows

When working with complex FCS operations or encountering unusual file formats, load this reference for detailed guidance.

## Integration Notes

**NumPy Arrays:** All event data is returned as NumPy ndarrays with shape (events, channels)

**Pandas DataFrames:** Easily convert to DataFrames for analysis:
```python
import pandas as pd
df = pd.DataFrame(flow.as_array(), columns=flow.pnn_labels)
```

**FlowKit Integration:** For advanced analysis (compensation, gating, FlowJo support), use FlowKit library which builds on FlowIO's parsing capabilities

**Web Applications:** FlowIO's minimal dependencies make it ideal for web backend services processing FCS uploads

## Troubleshooting

**Problem:** "Offset discrepancy error"
**Solution:** Use `ignore_offset_discrepancy=True` parameter

**Problem:** "Multiple datasets error"
**Solution:** Use `read_multiple_data_sets()` function instead of FlowData constructor

**Problem:** Out of memory with large files
**Solution:** Use `only_text=True` for metadata-only operations, or process events in chunks

**Problem:** Unexpected channel counts
**Solution:** Check for null channels; use `null_channel_list` parameter to exclude them

**Problem:** Cannot modify event data in place
**Solution:** FlowIO doesn't support direct modification; extract data, modify, then use `create_fcs()` to save

## Summary

FlowIO provides essential FCS file handling capabilities for flow cytometry workflows. Use it for parsing, metadata extraction, and file creation. For simple file operations and data extraction, FlowIO is sufficient. For complex analysis including compensation and gating, integrate with FlowKit or other specialized tools.