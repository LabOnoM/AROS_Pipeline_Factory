
import geopandas as gpd
import argparse
import sys
import os
import json

def read_file(filepath, **kwargs):
    """Reads a geospatial file into a GeoDataFrame."""
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}", file=sys.stderr)
        sys.exit(1)
    
    try:
        gdf = gpd.read_file(filepath, **kwargs)
        return gdf
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

def write_file(gdf, filepath, **kwargs):
    """Writes a GeoDataFrame to a geospatial file."""
    try:
        gdf.to_file(filepath, **kwargs)
        print(f"Successfully wrote file to {filepath}")
    except Exception as e:
        print(f"Error writing file: {e}", file=sys.stderr)
        sys.exit(1)

def get_info(gdf):
    """Prints summary information about a GeoDataFrame."""
    info = {
        "crs": str(gdf.crs),
        "total_features": len(gdf),
        "geometry_type": gdf.geometry.geom_type.unique().tolist(),
        "columns": gdf.columns.tolist(),
        "bounds": gdf.total_bounds.tolist()
    }
    return info
    
def reproject(gdf, target_crs):
    """Reprojects a GeoDataFrame to a new CRS."""
    try:
        gdf_projected = gdf.to_crs(target_crs)
        return gdf_projected
    except Exception as e:
        print(f"Error reprojecting GeoDataFrame: {e}", file=sys.stderr)
        sys.exit(1)

def buffer(gdf, distance):
    """Applies a buffer to the geometries in a GeoDataFrame."""
    try:
        # Note: Buffer distance is in the units of the CRS.
        # For accurate results, data should be in a projected CRS.
        gdf_buffered = gdf.copy()
        gdf_buffered['geometry'] = gdf.geometry.buffer(distance)
        return gdf_buffered
    except Exception as e:
        print(f"Error applying buffer: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="A Python wrapper for common GeoPandas operations.")
    subparsers = parser.add_subparsers(dest='operation', required=True, help='The GeoPandas operation to perform')

    # Subparser for 'info'
    info_parser = subparsers.add_parser('info', help='Get summary information about a geospatial file.')
    info_parser.add_argument('input_file', help='Path to the input geospatial file.')
    
    # Subparser for 'reproject'
    reproject_parser = subparsers.add_parser('reproject', help='Reproject a file to a new Coordinate Reference System (CRS).')
    reproject_parser.add_argument('input_file', help='Path to the input geospatial file.')
    reproject_parser.add_argument('output_file', help='Path to save the reprojected output file.')
    reproject_parser.add_argument('target_crs', help='The target CRS (e.g., "EPSG:4326").')

    # Subparser for 'buffer'
    buffer_parser = subparsers.add_parser('buffer', help='Apply a buffer to the geometries in a file.')
    buffer_parser.add_argument('input_file', help='Path to the input geospatial file.')
    buffer_parser.add_argument('output_file', help='Path to save the buffered output file.')
    buffer_parser.add_argument('distance', type=float, help='The buffer distance in the units of the file\'s CRS.')

    args = parser.parse_args()

    if args.operation == 'info':
        gdf = read_file(args.input_file)
        info = get_info(gdf)
        print(json.dumps(info, indent=2))
        
    elif args.operation == 'reproject':
        gdf = read_file(args.input_file)
        gdf_projected = reproject(gdf, args.target_crs)
        write_file(gdf_projected, args.output_file)
        
    elif args.operation == 'buffer':
        gdf = read_file(args.input_file)
        gdf_buffered = buffer(gdf, args.distance)
        write_file(gdf_buffered, args.output_file)
        
if __name__ == '__main__':
    main()
