---
name: napari
description: Interactive multi-dimensional image viewer for Python, specialized for spatial transcriptomics interactions via napari-spatialdata. Use this skill when the user needs to manually select cells, draw regions of interest (ROIs), or visually inspect spatial datasets (Visium, Xenium, etc.) and pass those annotations back into a Python workflow.
---

# Napari & SpatialData Integration

## Overview
[Napari](https://napari.org/) is a fast, interactive, multi-dimensional image viewer for Python. When dealing with spatial transcriptomics (10x Visium, Xenium, point-cloud data), napari combined with `spatialdata` and the `napari-spatialdata` plugin is the **gold standard** for visual interaction. 

It allows researchers to:
1. Visualize multi-terabyte images alongside single-cell boundaries and spatial transcripts.
2. Interactively draw polygons (Shapes) to define custom tissue regions.
3. Select specific clusters of cells using Lasso tools.
4. Extract those user-drawn shapes/selections directly back into the Python workflow for downstream analysis.

There are currently no better alternatives in the Python ecosystem for this level of scriptable, robust spatial interactivity. Alternative web-based viewers (like Vitessce or TissUUmaps) are great for static sharing but lack the dynamic "draw a region and instantly filter my AnnData in the next line of code" capability.

## Prerequisites & Installation

```bash
pip install "napari[all]" napari-spatialdata spatialdata spatialdata-io dask
```

## Workflow Pattern: Python ➔ Napari ➔ Python

This pattern allows the agent to spin up a GUI, instruct the user to make a selection, and then automatically process the user's selection once the GUI is closed.

### 1. Preparing the Data and Launching the Viewer

```python
import spatialdata as sd
import napari

# 1. Load the spatial dataset (e.g. Xenium, Visium)
sdata = sd.read_zarr("path/to/my_spatial_data.zarr")

# 2. Launch the Napari viewer
viewer = napari.Viewer()

# 3. Add the SpatialData object to the viewer
# The napari-spatialdata plugin allows direct plotting of sdata components
import napari_spatialdata
viewer.add_sdata(sdata)

# 4. Create an empty Shapes layer for the user to draw on
# This is explicitly for the user's custom ROIs
roi_layer = viewer.add_shapes(name="User Annotations", face_color="transparent", edge_color="red", edge_width=3)

print("GUI LAUNCHED. Please use the 'Add Polygon' tool in the 'User Annotations' layer to draw your regions of interest. Close the GUI window when finished.")

# 5. BLOCK script execution until the user closes the napari window
napari.run() 
```

### 2. Recovering User Annotations After GUI Closure

Once `napari.run()` finishes (because the user closed the window), the script resumes. You can now extract the shapes the user drew.

```python
# The viewer object still holds the layers, even after window closure
user_shapes_layer = viewer.layers["User Annotations"]
user_polygons = user_shapes_layer.data  # List of coordinates defining the shapes

if not user_polygons:
    print("User did not draw any regions.")
else:
    print(f"User drew {len(user_polygons)} regions.")
    
    # Example: Converting the napari shapes into Shapely polygons or a GeoDataFrame
    from shapely.geometry import Polygon
    import geopandas as gpd
    
    polys = [Polygon(p) for p in user_polygons]
    roi_gdf = gpd.GeoDataFrame(geometry=polys)
    
    # IMPORTANT: You can now use spatialdata functions to filter the original dataset
    # For example, bounding box or polygon querying
    filtered_sdata = sdata.query.polygon(roi_gdf.geometry[0])
    
    print(f"Cells originally: {len(sdata.tables['table'])}")
    print(f"Cells inside ROI: {len(filtered_sdata.tables['table'])}")
    
    # Save the subsetted data or the ROI shapes for later
    roi_gdf.to_file("user_selected_rois.geojson", driver="GeoJSON")
```

## Best Practices for Agent Usage

1. **Clear Instructions:** Whenever you write a script that opens Napari, use `print()` statements immediately before `napari.run()` to tell the user *exactly* what to do (e.g., "Select the Shapes layer, click the Polygon icon, draw your tumor border, then close the window").
2. **Blocking Execution:** Always use `napari.run()`. It halts the Python script until the user closes the UI, ensuring that the next lines of code have access to the finished drawings.
3. **Pre-populate Layers:** Always create a specifically named target layer (e.g., `viewer.add_shapes(name="Target")`) so your python script knows exactly which layer to pull data from when `napari.run()` yields.
4. **Coordinate Systems:** SpatialData handles transformations. Ensure the user draws in the global coordinate space if multiple images/points are aligned. Shapes extracted from napari are in image pixel space; `spatialdata` natively handles transforming these into physical coordinates.

## Common Annotations
* **Polygons / Shapes Layer:** Used for defining tissue boundaries, tumor zones, or morphological regions.
* **Points Layer:** Used for identifying specific cells or transcribing landmarks manually.
* **Labels Layer:** Used for painting pixel-wise semantic segmentation maps over the H&E image.
