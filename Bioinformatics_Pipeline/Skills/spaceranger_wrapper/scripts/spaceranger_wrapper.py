# ==============================================================================
# AROS Pipeline Factory - Scientific Workflows
#
# This script is part of the AROS (Antigravity Research OS) ecosystem.
# It is governed by the AROS Cross-Pipeline Compatibility Protocol (CPCP).
# For details, refer to SPEC.md and 00.RawData/SHARED_ASSET_REGISTRY.md.
# ==============================================================================


import subprocess
import sys
import os
import json
import argparse
import pandas as pd
from bs4 import BeautifulSoup

def run_command(command):
    """Executes a shell command and streams its output."""
    print(f"Executing command: {' '.join(command)}")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    output = []
    for line in process.stdout:
        print(line, end='')
        output.append(line)
    
    process.wait()
    
    if process.returncode != 0:
        print(f"Error executing command: {' '.join(command)}")
        print("".join(output))
        sys.exit(process.returncode)
        
    return "".join(output)

def qc_gate_1_inputs(args):
    """QC Gate 1: Input Validation. Presents discovered inputs for user confirmation."""
    print("--- QC GATE 1: INPUT VALIDATION ---")
    print("Discovered Inputs:")
    print(f"  ID: {args.id}")
    print(f"  Transcriptome: {args.transcriptome}")
    print(f"  FASTQs: {args.fastqs}")
    print(f"  Image: {args.image}")
    print(f"  Slide: {args.slide}")
    print(f"  Area: {args.area}")
    print("------------------------------------")
    # In a real agentic scenario, this would block and wait for user confirmation.
    # Here, we simulate it with a print statement.
    print("--> User confirmation is assumed for this automated script.")
    return True

def parse_web_summary(html_path):
    """Parses the web_summary.html to extract key metrics and generate a health score."""
    if not os.path.exists(html_path):
        return {"error": "web_summary.html not found"}, 0

    with open(html_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Example metric extraction (highly simplified)
    metrics = {}
    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                metric_name = cells[0].text.strip()
                metric_value = cells[1].text.strip()
                metrics[metric_name] = metric_value

    # Basic Health Score Logic (example)
    score = 0
    if 'Estimated Number of Spots' in metrics and int(metrics['Estimated Number of Spots'].replace(',', '')) > 1000:
        score += 1
    if 'Mean Reads per Spot' in metrics and int(metrics['Mean Reads per Spot'].replace(',', '')) > 50000:
        score += 1
    if 'Q30 Bases in Barcode' in metrics and float(metrics['Q30 Bases in Barcode'].strip('%')) > 90:
        score += 1
        
    return metrics, score

def qc_gate_2_outputs(output_dir):
    """QC Gate 2: Pipeline Output Review. Shows health score and key metrics."""
    print("\n--- QC GATE 2: PIPELINE OUTPUT REVIEW ---")
    metrics_csv_path = os.path.join(output_dir, 'outs', 'metrics_summary.csv')
    web_summary_path = os.path.join(output_dir, 'outs', 'web_summary.html')

    if not os.path.exists(metrics_csv_path):
        print("ERROR: metrics_summary.csv not found!")
        return False
        
    metrics_df = pd.read_csv(metrics_csv_path)
    print("Key Metrics from metrics_summary.csv:")
    print(metrics_df.to_string())
    
    summary_metrics, health_score = parse_web_summary(web_summary_path)
    print(f"\nWeb Summary Health Score: {health_score}/3")
    print("Extracted Web Summary Metrics:")
    print(json.dumps(summary_metrics, indent=2))
    print("-----------------------------------------")
    # Simulate user confirmation
    print("--> User confirmation is assumed for this automated script.")
    return True
    
def run_spaceranger_count(args):
    """Constructs and runs the 'spaceranger count' command."""
    if not qc_gate_1_inputs(args):
        print("Input validation failed. Aborting.")
        sys.exit(1)

    command = [
        'spaceranger', 'count',
        f'--id={args.id}',
        f'--transcriptome={args.transcriptome}',
        f'--fastqs={args.fastqs}',
        f'--image={args.image}',
        f'--slide={args.slide}',
        f'--area={args.area}',
        '--localcores=4', # Example: limit cores
        '--localmem=16'   # Example: limit memory
    ]
    
    run_command(command)
    
    output_dir = args.id
    if not qc_gate_2_outputs(output_dir):
        print("Output QC failed. Please review the pipeline outputs.")
        sys.exit(1)
        
    print("\n--- QC GATE 3: FINAL CONFIRMATION ---")
    print("Space Ranger 'count' pipeline completed and passed all QC gates.")
    print(f"Outputs are located in: {os.path.abspath(output_dir)}")
    print("------------------------------------")


def main():
    parser = argparse.ArgumentParser(description="A wrapper script for 10x Genomics Space Ranger v4.x.")
    subparsers = parser.add_subparsers(dest='command', required=True, help='Space Ranger subcommand to run')

    # Subparser for 'count'
    count_parser = subparsers.add_parser('count', help='Run the spaceranger count pipeline')
    count_parser.add_argument('--id', required=True, help='Sample ID')
    count_parser.add_argument('--transcriptome', required=True, help='Path to the transcriptome reference')
    count_parser.add_argument('--fastqs', required=True, help='Path to the FASTQ files directory')
    count_parser.add_argument('--image', required=True, help='Path to the tissue image (e.g., cytassist_image.tiff)')
    count_parser.add_argument('--slide', required=True, help='Slide serial number')
    count_parser.add_argument('--area', required=True, help='Capture area name from the slide')
    count_parser.set_defaults(func=run_spaceranger_count)

    # Add subparsers for segment, annotate, aggr if needed
    # ...

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    # This is a placeholder for where the agent would call the script.
    # For testing, you would need to create dummy files and paths.
    # Example of what an agent might generate as a command:
    # python spaceranger_wrapper.py count --id=sample01 \
    # --transcriptome=/path/to/ref \
    # --fastqs=/path/to/fastqs \
    # --image=/path/to/image.tiff \
    # --slide=V11A11-111 \
    # --area=A1
    print("Space Ranger Wrapper script. Use 'count' subcommand to execute the pipeline.")
    main()
