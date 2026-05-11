
import os
import re

def create_batches(source_file, batch_size=10, output_dir="Reference/batches"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(source_file, 'r') as f:
        lines = f.readlines()
        
    current_batch = []
    batch_index = 1
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if it looks like a list item
        # We want to keep the whole line so the agent has all info
        if re.match(r'^\d+\.', line):
            current_batch.append(line)
            
        if len(current_batch) >= batch_size:
            batch_filename = os.path.join(output_dir, f"batch_{batch_index:02d}.txt")
            with open(batch_filename, 'w') as f_out:
                f_out.write("\n".join(current_batch))
            print(f"Created {batch_filename} with {len(current_batch)} items.")
            current_batch = []
            batch_index += 1
            
    # Remaining items
    if current_batch:
        batch_filename = os.path.join(output_dir, f"batch_{batch_index:02d}.txt")
        with open(batch_filename, 'w') as f_out:
            f_out.write("\n".join(current_batch))
        print(f"Created {batch_filename} with {len(current_batch)} items.")

if __name__ == "__main__":
    create_batches("Reference/list.md", batch_size=10)
