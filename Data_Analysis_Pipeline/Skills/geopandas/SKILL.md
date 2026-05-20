---
name: geopandas
description: Python library for reading, writing, and analyzing geospatial vector data. Use for spatial operations (buffer, overlay, join), CRS reprojection, and map visualization on Shapefile, GeoJSON, GeoPackage, PostGIS, or Parquet formats.
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc. / AIPOCH
---

# GeoPandas

GeoPandas extends pandas to enable spatial operations on geometric types, combining the capabilities of pandas and shapely for geospatial data analysis.

## When to Use

- Load and export vector geospatial data (Shapefile, GeoJSON, GeoPackage, Parquet) while preserving attributes and geometry.
- Perform geometric operations such as buffer, simplify, centroid, convex hull, or distance/area calculations.
- Conduct spatial analysis including spatial joins (intersects/within/nearest), overlay operations (intersection/union/difference), dissolve, or clipping.
- Manage coordinate reference systems (CRS): inspect, set missing metadata, or reproject between EPSG codes.
- Visualize geospatial data as static plots (matplotlib) or interactive maps (folium-backed `explore()`).

## Key Features

- **GeoDataFrame / GeoSeries**: pandas-like tabular structures with a geometry column and vectorized spatial methods.
- **Multi-format I/O**: Read/write common GIS formats and integrate with PostGIS.
- **CRS-aware transformations**: `set_crs()` for metadata, `to_crs()` for coordinate transformation.
- **Spatial operations**: buffer/simplify/centroid and higher-level analysis (sjoin, overlay, dissolve).
- **Mapping**: quick plotting and choropleths; optional interactive exploration.

## Installation

```bash
uv pip install geopandas
```

### Optional Dependencies

```bash
# For interactive maps
uv pip install folium

# For classification schemes in mapping
uv pip install mapclassify

# For faster I/O operations (2-4x speedup)
uv pip install pyarrow

# For PostGIS database support
uv pip install psycopg2
uv pip install geoalchemy2

# For basemaps
uv pip install contextily

# For cartographic projections
uv pip install cartopy
```

## Quick Start

```python
import geopandas as gpd

# Read spatial data
gdf = gpd.read_file("data.geojson")

# Basic exploration
print(gdf.head())
print("CRS:", gdf.crs)
print("Geometry types:", gdf.geometry.geom_type.unique())

# Simple plot
gdf.plot()

# Reproject to different CRS
gdf_projected = gdf.to_crs("EPSG:3857")

# Calculate area (use projected CRS for accuracy)
gdf_projected['area'] = gdf_projected.geometry.area

# Save to file
gdf.to_file("output.gpkg")
```

## Core Concepts

### Data Structures

- **GeoSeries**: Vector of geometries with spatial operations
- **GeoDataFrame**: Tabular data structure with geometry column

See [data-structures.md](references/data-structures.md) for details.

### Reading and Writing Data

GeoPandas reads/writes multiple formats: Shapefile, GeoJSON, GeoPackage, PostGIS, Parquet.

```python
# Read with filtering
gdf = gpd.read_file("data.gpkg", bbox=(...))
```
