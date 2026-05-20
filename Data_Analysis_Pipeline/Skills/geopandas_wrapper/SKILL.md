---
name: geopandas_wrapper
description: >
  A Python-based skill for performing common geospatial data operations using the GeoPandas
  library. This skill provides a command-line interface to read, write, and manipulate
  geospatial vector data. Use this skill for tasks like getting information about a
  geospatial file, reprojecting it to a new Coordinate Reference System (CRS), or applying
  geometric operations like buffering. It supports formats like Shapefile, GeoJSON, and GeoPackage.

MANDATORY SKILL INSTRUCTIONS:

This skill executes the `geopandas_wrapper.py` script to perform geospatial analysis. The agent must
construct the correct command-line arguments based on the user's request.

## How to Use

The agent must call the python script with one of the available subcommands and the required
arguments.

### Example Workflow:

1.  **Identify the user's goal**: Determine which geospatial operation the user wants to perform
    (e.g., "reproject this shapefile", "get information about this GeoJSON", "create a buffer").
2.  **Gather the parameters**: Identify the input file path, output file path (if needed),
    and any other parameters like the target CRS or buffer distance.
3.  **Construct and execute the command**: Build the full command and run it using the shell.
4.  **Parse and report the output**: For the `info` command, parse the JSON output to answer
    user questions. For other commands, confirm that the output file was created successfully.

## Available Operations

### `info`
Gets summary information about a geospatial file and prints it as a JSON object.

**Parameters:**
-   `input_file`: The path to the source geospatial file.

**Example:**
```bash
python ~/.gemini/skills/geopandas_wrapper/scripts/geopandas_wrapper.py info /path/to/data.geojson
```
**Output (Example):**
```json
{
  "crs": "EPSG:4326",
  "total_features": 150,
  "geometry_type": [
    "Polygon"
  ],
  "columns": [
    "id",
    "name",
    "value",
    "geometry"
  ],
  "bounds": [
    -122.5,
    37.7,
    -122.3,
    37.8
  ]
}
```

### `reproject`
Reprojects a geospatial file to a new Coordinate Reference System (CRS).

**Parameters:**
-   `input_file`: The path to the source geospatial file.
-   `output_file`: The path where the new, reprojected file will be saved.
-   `target_crs`: The desired CRS for the output, in a format GeoPandas understands (e.g., "EPSG:3857").

**Example:**
```bash
python ~/.gemini/skills/geopandas_wrapper/scripts/geopandas_wrapper.py reproject /path/to/data.shp /path/to/data_reprojected.shp "EPSG:3857"
```

### `buffer`
Creates a buffer around the geometries in a geospatial file.

**Parameters:**
-   `input_file`: The path to the source geospatial file.
-   `output_file`: The path where the new, buffered file will be saved.
-   `distance`: The buffer distance. **Important**: The distance is in the units of the file's
    current CRS (e.g., degrees for EPSG:4326, meters for projected systems like EPSG:3857).
    For accurate meter-based buffers, reproject the data first.

**Example:**
```bash
python ~/.gemini/skills/geopandas_wrapper/scripts/geopandas_wrapper.py buffer /path/to/points.gpkg /path/to/points_buffered.gpkg 100
```
---
