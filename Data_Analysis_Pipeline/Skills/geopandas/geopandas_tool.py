# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import geopandas as gpd
import argparse
import os

def load_data(filepath):
    """Loads geospatial data from a file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return gpd.read_file(filepath)

def save_data(gdf, filepath):
    """Saves a GeoDataFrame to a file."""
    gdf.to_file(filepath)

def main():
    parser = argparse.ArgumentParser(description="GeoPandas Agent Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # read command
    read_parser = subparsers.add_parser("read", help="Read a geospatial file.")
    read_parser.add_argument("filepath", type=str, help="Path to the input file.")

    # write command
    write_parser = subparsers.add_parser("write", help="Write a GeoDataFrame to a file.")
    write_parser.add_argument("input_file", type=str, help="Path to the input file.")
    write_parser.add_argument("output_file", type=str, help="Path to the output file.")

    # reproject command
    reproject_parser = subparsers.add_parser("reproject", help="Reproject a GeoDataFrame.")
    reproject_parser.add_argument("input_file", type=str, help="Path to the input file.")
    reproject_parser.add_argument("output_file", type=str, help="Path to the output file.")
    reproject_parser.add_argument("target_crs", type=str, help="Target CRS (e.g., 'EPSG:4326').")

    args = parser.parse_args()

    if args.command == "read":
        gdf = load_data(args.filepath)
        print(gdf.head())
        print(f"CRS: {gdf.crs}")

    elif args.command == "write":
        gdf = load_data(args.input_file)
        save_data(gdf, args.output_file)
        print(f"File saved to {args.output_file}")

    elif args.command == "reproject":
        gdf = load_data(args.input_file)
        reprojected_gdf = gdf.to_crs(args.target_crs)
        save_data(reprojected_gdf, args.output_file)
        print(f"File reprojected to {args.target_crs} and saved to {args.output_file}")

if __name__ == "__main__":
    main()
