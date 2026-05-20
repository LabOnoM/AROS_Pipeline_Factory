---
name: brenda-database
---
description: Generated skill brenda-database

---
name: brenda-database
description: Access the BRENDA enzyme database via the SOAP API. Retrieve kinetic constants (Km, kcat, Vmax), reaction equations, enzyme properties (pH/temperature optima, stability), or perform enzyme discovery by EC/substrate/product.
license: MIT
metadata:
    skill-author: AIPOCH + K-Dense Inc.
---

## Overview

BRENDA (BRaunschweig ENzyme DAtabase) is a comprehensive enzyme information system containing detailed enzyme data from scientific literature. Query kinetic parameters (Km, kcat), reaction equations, substrate specificities, organism information, and optimal conditions for enzymes using the official SOAP API. Access over 45,000 enzymes with millions of kinetic data points for biochemical research, metabolic engineering, and enzyme discovery.  This skill leverages Python scripts to handle authentication, query construction, and parsing of BRENDA's delimited string responses.

## When to Use

This skill should be used when:

- Searching for enzyme kinetic parameters (Km, kcat, Vmax).
- Retrieving reaction equations and stoichiometry.
- Finding enzymes for specific substrates or reactions.
- Comparing enzyme properties across different organisms.
- Investigating optimal pH, temperature, and other conditions.
- Accessing enzyme inhibition and activation data.
- Supporting metabolic pathway reconstruction and retrosynthesis.
- Performing enzyme engineering and optimization studies.
- Analyzing substrate specificity and cofactor requirements.
- Automating BRENDA data retrieval in Python pipelines.

## Core Capabilities

The skill provides programmatic access to the BRENDA database through Python scripts, offering several key capabilities:

### 1. Kinetic Parameter Retrieval

Access comprehensive kinetic data for enzymes:

**Example**: Retrieve Km values for Alcohol dehydrogenase (EC 1.1.1.1):

```python
import os
from scripts.brenda_queries import BrendaClient

email = os.environ["BRENDA_EMAIL"]
password = os.environ["BRENDA_PASSWORD"]

client = BrendaClient(email=email, password=password)

km_data = client.get_km_values(ec_number="1.1.1.1")

for entry in km_data:
    print(entry)
```

**Explanation**: This code retrieves Km values for EC 1.1.1.1.  The `BrendaClient` handles authentication and the `get_km_values` function sends the query. Each `entry` is a delimited string containing the Km data and associated metadata.  See "Data Formats and Parsing" for details.

**Filtering**:
```python
km_data = client.get_km_values(ec_number="1.1.1.1", organism="Saccharomyces cerevisiae")
km_data = client.get_km_values(ec_number="1.1.1.1", substrate="ethanol")
```

### 2. Reaction Information

Retrieve reaction equations and details:

**Example**: Get reactions for EC 1.1.1.1:

```python
import os
from scripts.brenda_queries import BrendaClient

email = os.environ["BRENDA_EMAIL"]
password = os.environ["BRENDA_PASSWORD"]

client = BrendaClient(email=email, password=password)

reactions = client.get_reactions(ec_number="1.1.1.1")

for reaction in reactions:
    print(reaction)
```

**Explanation**:  Retrieves reaction data for the specified EC number. The output is a delimited string (see "Data Formats and Parsing") containing the reaction equation and associated information.

**Filtering**:

```python
reactions = client.get_reactions(ec_number="1.1.1.1", organism="Escherichia coli")
reactions = client.get_reactions(ec_number="1.1.1.1", reaction="ethanol + NAD+")
```

### 3. Enzyme Discovery

Find enzymes for specific biochemical transformations:

**Example**: Find enzymes acting on glucose:

```python
import os
from scripts.brenda_queries import BrendaClient

email = os.environ["BRENDA_EMAIL"]
password = os.environ["BRENDA_PASSWORD"]

client = BrendaClient(email=email, password=password)

enzymes = client.search_enzymes_by_substrate(substrate="glucose", limit=20)

for enzyme in enzymes:
    print(enzyme)
```

**Explanation**: Searches BRENDA for enzymes that act on the specified substrate.  The `limit` parameter controls the maximum number of results returned. The output consists of delimited strings containing enzyme information.

**Search by Product or Pattern**:

```python
enzymes = client.search_enzymes_by_product(product="lactate", limit=10)
enzymes = client.search_by_pattern(pattern="oxidation", limit=15)
```

### 4. Organism-Specific Enzyme Data

Compare enzyme properties across organisms:

**Example**: Compare enzyme properties across organisms:

```python
import os
from scripts.brenda_queries import BrendaClient

email = os.environ["BRENDA_EMAIL"]
password = os.environ["BRENDA_PASSWORD"]

client = BrendaClient(email=email, password=password)

organisms = ["Escherichia coli", "Saccharomyces cerevisiae", "Homo sapiens"]
comparison = client.compare_across_organisms(ec_number="1.1.1.1", organisms=organisms)

for org_data in comparison:
    print(org_data)
```

**Explanation**: Compares enzyme data (e.g., Km, optimal pH, temperature) for the specified EC number across different organisms. The result is a series of delimited strings.

### 5. Environmental Parameters, Substrate Specificity, Inhibition/Activation, and Engineering Support

The `brenda_queries.py` script provides numerous functions to retrieve specific enzyme properties, find enzyme variants with specific characteristics (e.g., thermophilic homologs), and more.  Consult the script's documentation and available functions for detailed usage.  These functions leverage similar calling patterns as the examples above, using the `BrendaClient` to connect to BRENDA and retrieve data based on EC number and other parameters.

## Installation Requirements

- Python 3.x
- `zeep` (SOAP client)
- `requests`

Install dependencies:

```bash
uv pip install zeep requests pandas matplotlib seaborn
```

## Authentication Setup

BRENDA requires authentication credentials:

1. **Set environment variables**:

```bash
export BRENDA_EMAIL="your.email@example.com"
export BRENDA_PASSWORD="your_brenda_password"
```

2. **Alternatively, create a .env file**:

```
BRENDA_EMAIL=your.email@example.com
BRENDA_PASSWORD=your_brenda_password
```
(The script will attempt to load these variables from a `.env` file in the current directory).

3. **Register for BRENDA access**:
   - Visit https://www.brenda-enzymes.org/
   - Create an account
   - Check your email for credentials

## Helper Scripts

This skill includes a Python script (`scripts/brenda_queries.py`) for BRENDA database queries.

### `scripts/brenda_queries.py`

Provides a `BrendaClient` class with methods for querying and retrieving enzyme data from the BRENDA database.

**Key Class and Methods:**

- `BrendaClient(email, password)`:  Initializes the BRENDA SOAP client with your credentials.
- `get_km_values(ec_number, organism=None, substrate=None)`: Retrieves Km values.
- `get_reactions(ec_number, organism=None, reaction=None)`: Retrieves reaction information.
- `search_enzymes_by_substrate(substrate, limit=10)`: Finds enzymes by substrate.
- `search_enzymes_by_product(product, limit=10)`: Finds enzymes producing a specific product.
- `search_by_pattern(pattern, limit=10)`: Searches enzymes by a reaction pattern.
- `compare_across_organisms(ec_number, organisms)`: Compares enzyme properties across organisms.
- `get_environmental_parameters(ec_number)`: Retrieves pH and temperature data.
- `get_cofactor_requirements(ec_number)`: Retrieves cofactor information.
- `get_substrate_specificity(ec_number)`: Analyzes substrate preferences.
- `get_inhibitors(ec_number)`: Retrieves enzyme inhibition data.
- `get_activators(ec_number)`: Retrieves enzyme activation data.
- `find_thermophilic_homologs(ec_number, min_temp)`: Finds heat-stable variants.
- `get_modeling_parameters(ec_number, substrate)`: Retrieves parameters for kinetic modeling.

**Example Usage**:

```python
import os
from scripts.brenda_queries import BrendaClient

email = os.environ["BRENDA_EMAIL"]
password = os.environ["BRENDA_PASSWORD"]

client = BrendaClient(email=email, password=password)

# Search for enzymes that act on glucose
enzymes = client.search_enzymes_by_substrate(substrate="glucose", limit=20)

# Compare across organisms
comparison = client.compare_across_organisms(ec_number="1.1.1.1", organisms=["E. coli", "S. cerevisiae"])
```

### Additional Scripts

The original skill description also mentioned `brenda_visualization.py` and `enzyme_pathway_builder.py`. If these scripts exist, they should be documented similarly to `brenda_queries.py`, detailing their functions and usage with examples. If they are not present, the references to them should be removed.

## API Rate Limits and Best Practices

**Rate Limits**:
- BRENDA API has moderate rate limiting.
- Recommended: 1 request per second for sustained usage.
- Maximum: 5 requests per 10 seconds.

**Best Practices**:
1. **Cache results**: Store frequently accessed enzyme data locally.
2. **Batch queries**: Combine related requests when possible.
3. **Use specific searches**: Narrow down by organism, substrate when possible.
4. **Handle missing data**: Not all enzymes have complete data.
5. **Validate EC numbers**: Ensure EC numbers are in correct format.
6. **Implement delays**: Add delays between consecutive requests if necessary.
7. **Use wildcards wisely**: Use '*' for broader searches when appropriate.
8. **Monitor quota**: Track your API usage if available.

**Error Handling**:

```python
import os
from scripts.brenda_queries import BrendaClient
from zeep.exceptions import Fault, TransportError

email = os.environ["BRENDA_EMAIL"]
password = os.environ["BRENDA_PASSWORD"]

try:
    client = BrendaClient(email=email, password=password)
    km_data = client.get_km_values(ec_number="1.1.1.1")
except RuntimeError as e:
    print(f"Authentication error: {e}")
except Fault as e:
    print(f"BRENDA API error: {e}")
except TransportError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Workflows

(Examples from the original local file, adapted for the `BrendaClient` class).  These examples assume the existence of the `BrendaClient` class and the environment variable authentication setup.

### Workflow 1: Enzyme Discovery for New Substrate

Find suitable enzymes for a specific substrate:

```python
import os
from scripts.brenda_queries import BrendaClient

email = os.environ["BRENDA_EMAIL"]
password = os.environ["BRENDA_PASSWORD"]

client = BrendaClient(email=email, password=password)

# Search for enzymes that act on substrate
substrate = "2-phenylethanol"
enzymes = client.search_enzymes_by_substrate(substrate=substrate, limit=15)

print(f"Found {len(enzymes)} enzymes for {substrate}")
for enzyme in enzymes:
    print(enzyme) # Prints the delimited string

# Optionally, retrieve Km data for candidates
if enzymes:
    # Extract EC number from the first enzyme result string
    ec_number = enzymes[0].split("ecNumber*")[1].split("#")[0]
    km_data = client.get_km_values(ec_number=ec_number, substrate=substrate)

    if km_data:
        print(f"Kinetic data for {ec_number}:")
        for entry in km_data[:3]:  # First 3 entries
            print(f"  {entry}") # Prints the delimited string
```

### Workflow 2: Cross-Organism Enzyme Comparison

Compare enzyme properties across different organisms:

```python
import os
from scripts.brenda_queries import BrendaClient

email = os.environ["BRENDA_EMAIL"]
password = os.environ["BRENDA_PASSWORD"]

client = BrendaClient(email=email, password=password)

# Define organisms for comparison
organisms = [
    "Escherichia coli",
    "Saccharomyces cerevisiae",
    "Bacillus subtilis",
    "Thermus thermophilus"
]

# Compare alcohol dehydrogenase
comparison = client.compare_across_organisms(ec_number="1.1.1.1", organisms=organisms)

print("Cross-organism comparison:")
for org_data in comparison:
    print(org_data) # Prints the delimited string
```

(Adapt the remaining workflows from the LOCAL version similarly, ensuring they use the `BrendaClient` class and focus on retrieving and printing the raw BRENDA response strings).

## Data Formats and Parsing

### BRENDA Response Format

BRENDA returns data in specific formats that need parsing. The skill focuses on *retrieving* the data; downstream parsing is the user's responsibility.

**Km Value Format**:
```
organism*Escherichia coli#substrate*ethanol#kmValue*1.2#kmValueMaximum*#commentary*pH 7.4, 25°C#ligandStructureId*#literature*
```

**Reaction Format**:
```
ecNumber*1.1.1.1#organism*Saccharomyces cerevisiae#reaction*ethanol + NAD+ <=> acetaldehyde + NADH + H+#commentary*#literature*
```

The scripts in this skill *do not* automatically parse these strings into structured data. The user is expected to implement their own parsing logic based on their specific needs. Example:

```python
def parse_brenda_string(data):
    """Simple example of parsing a BRENDA delimited string"""
    fields = data.split("#")
    parsed_data = {}
    for field in fields:
        if "*" in field:
            key, value = field.split("*", 1)
            parsed_data[key] = value
    return parsed_data

# Example usage (assuming 'km_data' contains BRENDA response strings)
parsed_entry = parse_brenda_string(km_data[0])
print(parsed_entry.get("substrate", "N/A"))
print(parsed_entry.get("kmValue", "N/A"))
```

## Reference Documentation

For detailed BRENDA documentation, see `references/api_reference.md`. This includes:
- Complete SOAP API method documentation
- Full parameter lists and formats
- EC number structure and validation
- Response format specifications
- Error codes and handling
- Data field definitions
- Literature citation formats

## Troubleshooting

**Authentication Errors**:
- Verify `BRENDA_EMAIL` and `BRENDA_PASSWORD` are correctly set in environment variables or .env file.
- Ensure the BRENDA account is active and has API access.

**No Results Returned**:
- Try broader searches with wildcards (*).
- Check EC number format (e.g., "1.1.1.1" not "1.1.1").
- Verify substrate spelling and naming.
- Some enzymes may have limited data in BRENDA.

**Rate Limiting**:
- Add delays between requests (0.5-1 second).
- Use more specific queries to reduce data volume.

**Network Errors**:
- Check internet connection.
- BRENDA server may be temporarily unavailable.
- Try again after a few minutes.

**Data Format Issues**:
- BRENDA data can be inconsistent in formatting.
- Handle missing fields gracefully when parsing results.

## Additional Resources

- BRENDA Home: https://www.brenda-enzymes.org/
- BRENDA SOAP API Documentation: https://www.brenda-enzymes.org/soap.php
- Enzyme Commission (EC) Numbers: https://www.qmul.ac.uk/sbcs/iubmb/enzyme/
- Zeep SOAP Client: https://python-zeep.readthedocs.io/
- Enzyme Nomenclature: https://www.iubmb.org/enzyme/

## Validation and Safety Rules

- Validate required inputs before execution; stop early if mandatory fields or files are missing.
- Do not fabricate measurements, references, findings, or conclusions not supported by the BRENDA database.
- Emit a clear warning when credentials, privacy constraints, or unsupported requests affect the result.
- Keep the output safe, reproducible, and within the documented scope at all times. The output of this skill are raw delimited strings from BRENDA, requiring user-implemented parsing for structured access.

## Failure Handling

- If validation fails, explain the exact missing field, file, or parameter and show the minimum fix required.
- If an external dependency or script fails, surface the command path, likely cause, and the next recovery step.
- If partial output is returned, label it clearly and identify which checks could not be completed.
- Handle `zeep` and network exceptions gracefully (see error handling example).