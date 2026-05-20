---
name: benchling-integration
description: Integrate with the Benchling R&D platform to programmatically manage registry entities, inventory, ELN entries, workflows, events, or data warehouse analytics via API/SDK.
license: MIT
metadata:
    skill-author: AIPOCH & K-Dense Inc.
---

# Benchling Integration

## Overview

Benchling is a cloud platform for life sciences R&D. This skill provides integration with Benchling's Python SDK and REST API for programmatic access to registry entities, inventory, electronic lab notebooks, and workflows.

## When to Use

- When you need to programmatically manage registry entities, inventory, ELN entries, workflows, events, or data warehouse analytics via API/SDK.
- For repeatable, checklist-driven execution rather than open-ended brainstorming.

## Key Features

- Scope-focused workflow aligned to: Integrate with the Benchling R&D platform when you need to programmatically manage registry entities, inventory, ELN entries, workflows, events, or data warehouse analytics via API/SDK.
- Documentation-first workflow with no packaged script requirement.
- Reference material available in `references/` for task-specific guidance.
- Structured execution path designed to keep outputs consistent and reviewable.

## Core Capabilities

### 1. Authentication & Setup

**Python SDK Installation:**
```python
# Stable release
uv pip install benchling-sdk
# or with Poetry
poetry add benchling-sdk
```

**Authentication Methods:**

API Key Authentication (recommended for scripts):
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key")
)
```

OAuth Client Credentials (for apps):
```python
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2

auth_method = ClientCredentialsOAuth2(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=auth_method
)
```

**Key Points:**
- API keys are obtained from Profile Settings in Benchling
- Store credentials securely (use environment variables or password managers)
- All API requests require HTTPS
- Authentication permissions mirror user permissions in the UI

### 2. Registry & Entity Management

Registry entities include DNA sequences, RNA sequences, AA sequences, custom entities, and mixtures. The SDK provides typed classes for creating and managing these entities.

**Creating DNA Sequences:**
```python
from benchling_sdk.models import DnaSequenceCreate

sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="My Plasmid",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        schema_id="ts_abc123",  # optional
        fields=benchling.models.fields({"gene_name": "GFP"})
    )
)
```

**Registry Registration:**

To register an entity directly upon creation:
```python
sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="My Plasmid",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        entity_registry_id="src_abc123",  # Registry to register in
        naming_strategy="NEW_IDS"  # or "IDS_FROM_NAMES"
    )
)
```

**Important:** Use either `entity_registry_id` OR `naming_strategy`, never both.

**Updating Entities:**
```python
from benchling_sdk.models import DnaSequenceUpdate

updated = benchling.dna_sequences.update(
    sequence_id="seq_abc123",
    dna_sequence=DnaSequenceUpdate(
        name="Updated Plasmid Name",
        fields=benchling.models.fields({"gene_name": "mCherry"})
    )
)
```

Unspecified fields remain unchanged, allowing partial updates.

**Listing and Pagination:**
```python
# List all DNA sequences (returns a generator)
sequences = benchling.dna_sequences.list()
for page in sequences:
    for seq in page:
        print(f"{seq.name} ({seq.id})")

# Check total count
total = sequences.estimated_count()
```

**Key Operations:**
- Create: `benchling.<entity_type>.create()`
- Read: `benchling.<entity_type>.get(id)` or `.list()`
- Update: `benchling.<entity_type>.update(id, update_object)`
- Archive: `benchling.<entity_type>.archive(id)`

Entity types: `dna_sequences`, `rna_sequences`, `aa_sequences`, `custom_entities`, `mixtures`

### 3. Inventory Management

Manage physical samples, containers, boxes, and locations within the Benchling inventory system.

**Creating Containers:**
```python
from benchling_sdk.models import ContainerCreate

container = benchling.containers.create(
    ContainerCreate(
        name="Sample Tube 001",
        schema_id="cont_schema_abc123",
        parent_storage_id="box_abc123",  # optional
        fields=benchling.models.fields({"concentration": "100 ng/μL"})
    )
)
```

**Managing Boxes:**
```python
from benchling_sdk.models import BoxCreate

box = benchling.boxes.create(
    BoxCreate(
        name="Freezer Box A1",
        schema_id="box_schema_abc123",
        parent_storage_id="loc_abc123"
    )
)
```

**Transferring Items:**
```python
# Transfer a container to a new location
transfer = benchling.containers.transfer(
    container_id="cont_abc123",
    destination_id="box_xyz789"
)
```

**Key Inventory Operations:**
- Create containers, boxes, locations, plates
- Update inventory item properties
- Transfer items between locations
- Check in/out items
- Batch operations for bulk transfers

### 4. Notebook & Documentation

Interact with electronic lab notebook (ELN) entries, protocols, and templates.

**Creating Notebook Entries:**
```python
from benchling_sdk.models import EntryCreate

entry = benchling.entries.create(
    EntryCreate(
        name="Experiment 2025-10-20",
        folder_id="fld_abc123",
        schema_id="entry_schema_abc123",
        fields=benchling.models.fields({"objective": "Test gene expression"})
    )
)
```

**Linking Entities to Entries:**
```python
# Add references to entities in an entry
entry_link = benchling.entry_links.create(
    entry_id="entry_abc123",
    entity_id="seq_xyz789"
)
```

**Key Notebook Operations:**
- Create and update lab notebook entries
- Manage entry templates
- Link entities and results to entries
- Export entries for documentation

### 5. Workflows & Automation

Automate laboratory processes using Benchling's workflow system.

**Creating Workflow Tasks:**
```python
from benchling_sdk.models import WorkflowTaskCreate

task = benchling.workflow_tasks.create(
    WorkflowTaskCreate(
        name="PCR Amplification",
        workflow_id="wf_abc123",
        assignee_id="user_abc123",
        fields=benchling.models.fields({"template": "seq_abc123"})
    )
)
```

**Updating Task Status:**
```python
from benchling_sdk.models import WorkflowTaskUpdate

updated_task = benchling.workflow_tasks.update(
    task_id="task_abc123",
    workflow_task=WorkflowTaskUpdate(
        status_id="status_complete_abc123"
    )
)
```

**Asynchronous Operations:**

Some operations are asynchronous and return tasks:
```python
# Wait for task completion
from benchling_sdk.helpers.tasks import wait_for_task

result = wait_for_task(
    benchling,
    task_id="task_abc123",
    interval_wait_seconds=2,
    max_wait_seconds=300
)
```

**Key Workflow Operations:**
- Create and manage workflow tasks
- Update task statuses and assignments
- Execute bulk operations asynchronously
- Monitor task progress

### 6. Events & Integration

Subscribe to Benchling events for real-time integrations using AWS EventBridge.

**Event Types:**
- Entity creation, update, archive
- Inventory transfers
- Workflow task status changes
- Entry creation and updates
- Results registration

**Integration Pattern:**
1. Configure event routing to AWS EventBridge in Benchling settings
2. Create EventBridge rules to filter events
3. Route events to Lambda functions or other targets
4. Process events and update external systems

**Use Cases:**
- Sync Benchling data to external databases
- Trigger downstream processes on workflow completion
- Send notifications on entity changes
- Audit trail logging

### 7. Data Warehouse & Analytics

Query historical Benchling data using SQL through the Data Warehouse.

**Access Method:**
The Benchling Data Warehouse provides SQL access to Benchling data for analytics and reporting. Connect using standard SQL clients with provided credentials.

**Common Queries:**
- Aggregate experimental results
- Analyze inventory trends
- Generate compliance reports
- Export data for external analysis

## Dependencies

- `benchling-sdk` (Python)
- Python (`3.10+`)
- Optional (for FASTA import example): `biopython`
- Optional (for event-driven integrations): AWS EventBridge
- Optional (for Data Warehouse access): a SQL client/driver

## Example Usage

A minimal, runnable example that authenticates with an API key, creates a DNA sequence, lists sequences (paginated), and creates an ELN entry.

```python
import os

from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth
from benchling_sdk.models import DnaSequenceCreate, EntryCreate

def main():
    tenant_url = os.environ["BENCHLING_TENANT_URL"]  # e.g. https://your-tenant.benchling.com
    api_key = os.environ["BENCHLING_API_KEY"]
    folder_id = os.environ["BENCHLING_FOLDER_ID"]    # e.g. fld_abc123

    benchling = Benchling(
        url=tenant_url,
        auth_method=ApiKeyAuth(api_key),
    )

    # 1) Create a DNA sequence in the Registry (unregistered unless entity_registry_id is provided)
    created_seq = benchling.dna_sequences.create(
        DnaSequenceCreate(
            name="Example Plasmid",
            bases="ATCGATCG",
            is_circular=True,
            folder_id=folder_id,
        )
    )
    print("Created DNA sequence:", created_seq.id, created_seq.name)

    # 2) List DNA sequences (generator yields pages)
    print("\nListing DNA sequences (first page):")
    pages = benchling.dna_sequences.list()
    first_page = next(iter(pages))
    for seq in first_page:
        print("-", seq.id, seq.name)

    # 3) Create an ELN entry
    entry = benchling.entries.create(
        EntryCreate(
            name="Example Experiment Entry",
            folder_id=folder_id,
        )
    )
    print("\nCreated ELN entry:", entry.id, entry.name)

if __name__ == "__main__":
    main()
```

Run:

```bash
export BENCHLING_TENANT_URL="https://your-tenant.benchling.com"
export BENCHLING_API_KEY="your_api_key"
export BENCHLING_FOLDER_ID="fld_abc123"

python benchling_example.py
```

## Implementation Details

### Authentication

- **API Key authentication** is recommended for scripts and automation:
  - API keys are obtained from Benchling profile/settings.
  - Permissions match the user/app permissions in the Benchling UI.
  - Store secrets in environment variables or a secrets manager; never commit keys.

```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key"),
)
```

- **OAuth client credentials** is suitable for apps/services:

```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2

auth_method = ClientCredentialsOAuth2(
    client_id="your_client_id",
    client_secret="your_client_secret",
)

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=auth_method,
)
```

### Registry entities and schema fields

- Registry entity creation uses typed models such as `DnaSequenceCreate`.
- Custom schema fields are passed via the SDK `fields()` helper.

```python
from benchling_sdk.models import DnaSequenceCreate

sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="My Plasmid",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        schema_id="ts_abc123",  # optional
        fields=benchling.models.fields({"gene_name": "GFP"}),
    )
)
```

- **Registration behavior**: the source document notes that `entity_registry_id` and `naming_strategy` should not be used together.

```python
sequence = benchling.dna_sequences.create(
    DnaSequenceCreate(
        name="My Plasmid",
        bases="ATCGATCG",
        is_circular=True,
        folder_id="fld_abc123",
        entity_registry_id="src_abc123",
        naming_strategy="NEW_IDS",  # do not combine with entity_registry_id per source note
    )
)
```

### Partial updates

- Updates are partial: unspecified fields remain unchanged.

```python
from benchling_sdk.models import DnaSequenceUpdate

updated = benchling.dna_sequences.update(
    sequence_id="seq_abc123",
    dna_sequence=DnaSequenceUpdate(
        name="Updated Plasmid Name",
        fields=benchling.models.fields({"gene_name": "mCherry"}),
    ),
)
```

### Pagination

- Listing endpoints return generators of pages; iterate page-by-page for memory efficiency.
- Some list iterators provide `estimated_count()`.

```python
sequences = benchling.dna_sequences.list()
for page in sequences:
    for seq in page:
        print(seq.name, seq.id)

total = sequences.estimated_count()
```

### Inventory operations (containers/boxes/transfers)

- Inventory objects are created via typed models (e.g., `ContainerCreate`, `BoxCreate`).
- Transfers move items between storage locations.

```python
from benchling_sdk.models import ContainerCreate, BoxCreate

box = benchling.boxes.create(
    BoxCreate(
        name="Freezer Box A1",
        schema_id="box_schema_abc123",
        parent_storage_id="loc_abc123",
    )
)

container = benchling.containers.create(
    ContainerCreate(
        name="Sample Tube 001",
        schema_id="cont_schema_abc123",
        parent_storage_id=box.id,
        fields=benchling.models.fields({"concentration": "100 ng/μL"}),
    )
)

benchling.containers.transfer(
    container_id=container.id,
    destination_id="box_xyz789",
)
```

### Workflows and async tasks

- Some operations are asynchronous and return a task object; poll until completion.

```python
from benchling_sdk.helpers.tasks import wait_for_task

result = wait_for_task(
    benchling,
    task_id="task_abc123",
    interval_wait_seconds=2,
    max_wait_seconds=300,
)
```

### Retry strategy (error handling)

- The SDK can retry transient failures (e.g., rate limiting and gateway errors) with configurable strategy.

```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth
from benchling_sdk.retry import RetryStrategy

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key"),
    retry_strategy=RetryStrategy(max_retries=3),
)
```

### Events and Data Warehouse

- **Events**: Benchling can emit events (e.g., entity updates, inventory transfers, workflow status changes) that can be routed via AWS EventBridge for near real-time integrations. Refer to Benchling's event documentation for event schemas and configuration.
- **Data Warehouse**: Use SQL access for analytics/reporting (inventory trends, compliance reports, aggregations). Connection details and schemas are provided by Benchling.

## Best Practices

### Error Handling

The SDK automatically retries failed requests:
```python
# Automatic retry for 429, 502, 503, 504 status codes
# Up to 5 retries with exponential backoff
# Customize retry behavior if needed
from benchling_sdk.retry import RetryStrategy

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key"),
    retry_strategy=RetryStrategy(max_retries=3)
)
```

### Pagination Efficiency

Use generators for memory-efficient pagination:
```python
# Generator-based iteration
for page in benchling.dna_sequences.list():
    for sequence in page:
        process(sequence)

# Check estimated count without loading all pages
total = benchling.dna_sequences.list().estimated_count()
```

### Schema Fields Helper

Use the `fields()` helper for custom schema fields:
```python
# Convert dict to Fields object
custom_fields = benchling.models.fields({
    "concentration": "100 ng/μL",
    "date_prepared": "2025-10-20",
    "notes": "High quality prep"
})
```

### Forward Compatibility

The SDK handles unknown enum values and types gracefully:
- Unknown enum values are preserved
- Unrecognized polymorphic types return `UnknownType`
- Allows working with newer API versions

### Security Considerations

- Never commit API keys to version control
- Use environment variables for credentials
- Rotate keys if compromised
- Grant minimal necessary permissions for apps
- Use OAuth for multi-user scenarios

## When Not to Use

- Do not use this skill when the required source data, identifiers, files, or credentials are missing.
- Do not use this skill when the user asks for fabricated results, unsupported claims, or out-of-scope conclusions.
- Do not use this skill when a simpler direct answer is more appropriate than the documented workflow.

## Required Inputs

- A clearly specified task goal aligned with the documented scope.
- All required files, identifiers, parameters, or environment variables before execution.
- Any domain constraints, formatting requirements, and expected output destination if applicable.

## Recommended Workflow

1. Validate the request against the skill boundary and confirm all required inputs are present.
2. Select the documented execution path and prefer the simplest supported command or procedure.
3. Produce the expected output using the documented file format, schema, or narrative structure.
4. Run a final validation pass for completeness, consistency, and safety before returning the result.

## Output Contract

- Return a structured deliverable that is directly usable without reformatting.
- If a file is produced, prefer a deterministic output name such as `benchling_integration_result.md` unless the skill documentation defines a better convention.
- Include a short validation summary describing what was checked, what assumptions were made, and any remaining limitations.

## Validation and Safety Rules

- Validate required inputs before execution and stop early when mandatory fields or files are missing.
- Do not fabricate measurements, references, findings, or conclusions that are not supported by the provided source material.
- Emit a clear warning when credentials, privacy constraints, safety boundaries, or unsupported requests affect the result.
- Keep the output safe, reproducible, and within the documented scope at all times.

## Failure Handling

- If validation fails, explain the exact missing field, file, or parameter and show the minimum fix required.
- If an external dependency or script fails, surface the command path, likely cause, and the next recovery step.
- If partial output is returned, label it clearly and identify which checks could not be completed.

## Resources

### references/

Detailed reference documentation for in-depth information:

- **authentication.md** - Comprehensive authentication guide including OIDC, security best practices, and credential management
- **sdk_reference.md** - Detailed Python SDK reference with advanced patterns, examples, and all entity types
- **api_endpoints.md** - REST API endpoint reference for direct HTTP calls without the SDK

### scripts/

This skill currently includes example scripts that can be removed or replaced with custom automation scripts for your specific Benchling workflows.

## Common Use Cases

**1. Bulk Entity Import:**
```python
# Import multiple sequences from FASTA file
from Bio import SeqIO

for record in SeqIO.parse("sequences.fasta", "fasta"):
    benchling.dna_sequences.create(
        DnaSequenceCreate(
            name=record.id,
            bases=str(record.seq),
            is_circular=False,
            folder_id="fld_abc123"
        )
    )
```

**2. Inventory Audit:**
```python
# List all containers in a specific location
containers = benchling.containers.list(
    parent_storage_id="box_abc123"
)

for page in containers:
    for container in page:
        print(f"{container.name}: {container.barcode}")
```

**3. Workflow Automation:**
```python
# Update all pending tasks for a workflow
tasks = benchling.workflow_tasks.list(
    workflow_id="wf_abc123",
    status="pending"
)

for page in tasks:
    for task in page:
        # Perform automated checks
        if auto_validate(task):
            benchling.workflow_tasks.update(
                task_id=task.id,
                workflow_task=WorkflowTaskUpdate(
                    status_id="status_complete"
                )
            )
```

**4. Data Export:**
```python
# Export all sequences with specific properties
sequences = benchling.dna_sequences.list()
export_data = []

for page in sequences:
    for seq in page:
        if seq.schema_id == "target_schema_id":
            export_data.append({
                "id": seq.id,
                "name": seq.name,
                "bases": seq.bases,
                "length": len(seq.bases)
            })

# Save to CSV or database
import csv
with open("sequences.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=export_data[0].keys())
    writer.writeheader()
    writer.writerows(export_data)
```

## Additional Resources

- **Official Documentation:** https://docs.benchling.com
- **Python SDK Reference:** https://benchling.com/sdk-docs/
- **API Reference:** https://benchling.com/api/reference
- **Support:** [email protected]

## Quick Validation

Run this minimal verification path before full execution when possible:

```text
No local script validation step is required for this skill.
```

Expected output format:

```text
Result file: benchling_integration_result.md
Validation summary: PASS/FAIL with brief notes
Assumptions: explicit list if any
```