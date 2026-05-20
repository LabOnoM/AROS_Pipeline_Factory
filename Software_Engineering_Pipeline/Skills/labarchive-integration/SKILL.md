---
name: labarchive-integration
description: Transforms LabArchives notebook data, entry metadata, and authorized exports into academic writing outputs: Methods sections, data availability statements, reproducibility appendices, experiment timelines, and submission support notes. Optional bundled scripts collect/validate source data.
license: MIT
skill-author: AIPOCH
metadata:
    skill-author: K-Dense Inc.
---

# LabArchives Integration

This skill is an **Academic Writing** workflow centered on LabArchives evidence. It focuses on converting authorized ELN material into manuscript-ready writing deliverables, not just API access.

## When to Use This Skill

This skill should be used when:

- The user needs a **Methods** draft grounded in recorded LabArchives procedures.
- The user needs a **data availability statement**, **reproducibility appendix**, **experiment timeline**, or **submission support summary** based on ELN records.
- The user wants to gather authorized notebook data before converting it into academic writing outputs.
- The user needs a deterministic evidence-to-writing workflow instead of freeform summarization.
- Working with LabArchives REST API for notebook automation
- Backing up notebooks programmatically
- Creating or managing notebook entries and attachments
- Generating site reports and analytics
- Integrating LabArchives with third-party tools (Protocols.io, Jupyter, REDCap)
- Automating data upload to electronic lab notebooks
- Managing user access and permissions programmatically

## When Not to Use This Skill

This skill should NOT be used when:

- The user asks for unauthorized access to notebooks or other users' data.
- The user wants clinical recommendations, diagnosis, or treatment language.
- The user asks you to fabricate notebook records, timestamps, protocol details, or compliance statements that are not present in the source.
- The user has no authorized export, no notebook metadata, and no textual record to ground the writing output.

## Primary Writing Outputs

This skill supports these deliverables:

- **Methods Draft**
  Based on notebook entries, protocols, instrument logs, and sample-processing notes.
- **Data Availability Statement**
  Based on notebook identifiers, repository links, export status, and sharing constraints.
- **Reproducibility Appendix**
  Based on protocol versions, software environments, parameter logs, and file provenance.
- **Experiment Timeline Summary**
  Based on dated entries, milestones, and decision points.
- **Submission Support Note**
  Based on notebook scope, audit trail, and documentation completeness.

## Core Capabilities

### 1. Authentication and Configuration

Set up API access credentials and regional endpoints for LabArchives API integration.

**Prerequisites:**
- Enterprise LabArchives license with API access enabled
- API access key ID and password from LabArchives administrator
- User authentication credentials (email and external applications password)

**Configuration setup:**

Use the `scripts/setup_config.py` script to create a configuration file:

```bash
python3 scripts/setup_config.py
```

This creates a `config.yaml` file with the following structure:

```yaml
api_url: https://api.labarchives.com/api  # or regional endpoint
access_key_id: YOUR_ACCESS_KEY_ID
access_password: YOUR_ACCESS_PASSWORD
```

**Regional API endpoints:**
- US/International: `https://api.labarchives.com/api`
- Australia: `https://auapi.labarchives.com/api`
- UK: `https://ukapi.labarchives.com/api`

For detailed authentication instructions and troubleshooting, refer to `references/authentication_guide.md`.

### 2. Authorized Input Sources

Use one or more of:

- Exported notebook text or JSON
- Manually pasted LabArchives entry content
- Protocol summaries
- Experiment metadata tables
- Authorized backup output from bundled scripts

Optional collection step:

- `scripts/setup_config.py`
- `scripts/notebook_operations.py`
- `scripts/entry_operations.py`

### 3. Writing Output Contract

#### Output A: Methods Draft

Must include:

- Study material or sample context
- Experimental workflow in chronological order
- Instrument / assay / software mentions if present in source
- Quality-control or versioning note if present in source
- No invented parameter values

#### Output B: Data Availability Statement

Must include:

- What data are available
- Where they are stored or how they can be requested
- Any access restrictions
- Relationship to LabArchives or downstream repository

#### Output C: Reproducibility Appendix

Must include:

- Protocol version references
- Software or pipeline identifiers if present
- Provenance or notebook traceability note
- Missing-record warning if the audit trail is incomplete

#### Output D: Experiment Timeline Summary

Must include:

- Dated milestone order
- Major protocol transitions
- Validation / repeat / deviation points if documented

### 4. Notebook Operations

Manage notebook access, backup, and metadata retrieval.

**Key operations:**

- **List notebooks:** Retrieve all notebooks accessible to a user
- **Backup notebooks:** Download complete notebook data with optional attachment inclusion
- **Get notebook IDs:** Retrieve institution-defined notebook identifiers for integration with grants/project management systems
- **Get notebook members:** List all users with access to a specific notebook
- **Get notebook settings:** Retrieve configuration and permissions for notebooks

**Notebook backup example:**

Use the `scripts/notebook_operations.py` script:

```bash
# Backup with attachments (default, creates 7z archive)
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID

# Backup without attachments, JSON format
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID --json --no-attachments
```

**API endpoint format:**
```
https://<api_url>/notebooks/notebook_backup?uid=<UID>&nbid=<NOTEBOOK_ID>&json=true&no_attachments=false
```

For comprehensive API method documentation, refer to `references/api_reference.md`.

### 5. Entry and Attachment Management

Create, modify, and manage notebook entries and file attachments.

**Entry operations:**
- Create new entries in notebooks
- Add comments to existing entries
- Create entry parts/components
- Upload file attachments to entries

**Attachment workflow:**

Use the `scripts/entry_operations.py` script:

```bash
# Upload attachment to an entry
python3 scripts/entry_operations.py upload --uid USER_ID --nbid NOTEBOOK_ID --entry-id ENTRY_ID --file /path/to/file.pdf

# Create a new entry with text content
python3 scripts/entry_operations.py create --uid USER_ID --nbid NOTEBOOK_ID --title "Experiment Results" --content "Results from today's experiment..."
```

**Supported file types:**
- Documents (PDF, DOCX, TXT)
- Images (PNG, JPG, TIFF)
- Data files (CSV, XLSX, HDF5)
- Scientific formats (CIF, MOL, PDB)
- Archives (ZIP, 7Z)

### 6. Workflow

#### 1. Validate authorization and source sufficiency

Confirm:

- The requester has authorized access to the notebook data
- The source contains enough grounded information for the requested writing output

If not, stop and use the refusal template in `## Refusal and Recovery Contract`.

#### 2. Choose the acquisition path

Use direct source text if already available. Prefer this path for speed.

If data must be collected first, use one of the bundled scripts:

```bash
python scripts/setup_config.py
python scripts/notebook_operations.py --help
python scripts/entry_operations.py --help
```

Use `--dry-run` where available before live execution.

#### 3. Normalize notebook evidence

Extract only writing-relevant elements:

- Dates
- Protocol names and versions
- Sample or cohort descriptors
- Software / pipeline names
- QC notes
- Repository / export details
- Compliance or sharing constraints

#### 4. Draft the requested academic writing output

Keep the prose:

- Factual
- Audit-trail grounded
- Publication appropriate
- Free of operational noise that does not belong in the manuscript deliverable

#### 5. Run the final writing safety pass

Check that:

- Every claim maps back to source evidence
- Missing evidence is labeled as missing
- No compliance statement is invented
- No unauthorized identifiers are surfaced

### 7. Site Reports and Analytics

Generate institutional reports on notebook usage, activity, and compliance (Enterprise feature).

**Available reports:**
- Detailed Usage Report: User activity metrics and engagement statistics
- Detailed Notebook Report: Notebook metadata, member lists, and settings
- PDF/Offline Notebook Generation Report: Export tracking for compliance
- Notebook Members Report: Access control and collaboration analytics
- Notebook Settings Report: Configuration and permission auditing

**Report generation:**

```python
# Generate detailed usage report
response = client.make_call('site_reports', 'detailed_usage_report',
                           params={'start_date': '2025-01-01', 'end_date': '2025-10-20'})
```

### 8. Third-Party Integrations

LabArchives integrates with numerous scientific software platforms. This skill provides guidance on leveraging these integrations programmatically.

**Supported integrations:**
- **Protocols.io:** Export protocols directly to LabArchives notebooks
- **GraphPad Prism:** Export analyses and figures (Version 8+)
- **SnapGene:** Direct molecular biology workflow integration
- **Geneious:** Bioinformatics analysis export
- **Jupyter:** Embed Jupyter notebooks as entries
- **REDCap:** Clinical data capture integration
- **Qeios:** Research publishing platform
- **SciSpace:** Literature management

**OAuth authentication:**
LabArchives now uses OAuth for all new integrations. Legacy integrations may use API key authentication.

For detailed integration setup instructions and use cases, refer to `references/integrations.md`.

## Refusal and Recovery Contract

If the workflow cannot proceed safely, respond with:

```text
Cannot generate the requested LabArchives-based writing output yet.
Reason: <missing authorization / insufficient export / incomplete metadata / unsupported request>
Minimum next step:
- <step 1>
- <step 2>
```

Use this contract for:

- Missing notebook authorization
- No usable export or pasted content
- Requests to infer missing protocol details
- Requests to expose restricted data

## Common Workflows

### Complete notebook backup workflow

1. Authenticate and obtain user ID
2. List all accessible notebooks
3. Iterate through notebooks and backup each one
4. Store backups with timestamp metadata

```bash
# Complete backup script
python3 scripts/notebook_operations.py backup-all --email user@example.edu --password AUTH_TOKEN
```

### Automated data upload workflow

1. Authenticate with LabArchives API
2. Identify target notebook and entry
3. Upload experimental data files
4. Add metadata comments to entries
5. Generate activity report

### Integration workflow example (Jupyter → LabArchives)

1. Export Jupyter notebook to HTML or PDF
2. Use entry_operations.py to upload to LabArchives
3. Add comment with execution timestamp and environment info
4. Tag entry for easy retrieval

## Script Usage Notes

The bundled scripts are **supporting collection utilities**, not the final output themselves.

- `setup_config.py`: create or validate configuration
- `notebook_operations.py`: list notebooks, plan backups, or perform authorized exports
- `entry_operations.py`: inspect entry-level content or upload artifacts when explicitly needed

If a script path fails:

- Report the exact command
- Report the exact failure
- Continue with direct writing only if enough grounded notebook text is already available

## Academic Writing Style Rules

- Write in neutral, methods-oriented academic prose
- Prefer verifiable chronology over interpretive narrative
- Do not overclaim documentation quality if the notebook trail is partial
- Clearly distinguish `documented`, `not documented`, and `not provided`

## Python Package Installation

Install the `labarchives-py` wrapper for simplified API access:

```bash
git clone https://github.com/mcmero/labarchives-py
cd labarchives-py
uv pip install .
```

Alternatively, use direct HTTP requests via Python's `requests` library for custom implementations.

## Recommended Templates

Use `assets/writing_outputs_template.md` as the default skeleton for the four main writing deliverables.

## Deterministic Rules

- Keep output headings stable
- Do not expose raw credentials, tokens, or private notebook identifiers unless the user explicitly needs authorized internal formatting
- If a timestamp or version is missing, say it is not documented
- Treat data availability and reproducibility statements as formal manuscript components, not casual notes

## Best Practices

1. **Rate limiting:** Implement appropriate delays between API calls to avoid throttling
2. **Error handling:** Always wrap API calls in try-except blocks with appropriate logging
3. **Authentication security:** Store credentials in environment variables or secure config files (never in code)
4. **Backup verification:** After notebook backup, verify file integrity and completeness
5. **Incremental operations:** For large notebooks, use pagination and batch processing
6. **Regional endpoints:** Use the correct regional API endpoint for optimal performance

## Completion Checklist

- Authorization boundary checked
- Source sufficiency checked
- Requested writing deliverable selected explicitly
- All statements grounded in notebook evidence
- Missing evidence labeled rather than invented

## Troubleshooting

**Common issues:**

- **401 Unauthorized:** Verify access key ID and password are correct; check API access is enabled for your account
- **404 Not Found:** Confirm notebook ID (nbid) exists and user has access permissions
- **403 Forbidden:** Check user permissions for the requested operation
- **Empty response:** Ensure required parameters (uid, nbid) are provided correctly
- **Attachment upload failures:** Verify file size limits and format compatibility

For additional support, contact LabArchives at support@labarchives.com.

## Resources

This skill includes bundled resources to support LabArchives API integration:

### scripts/

- `setup_config.py`: Interactive configuration file generator for API credentials
- `notebook_operations.py`: Utilities for listing, backing up, and managing notebooks
- `entry_operations.py`: Tools for creating entries and uploading attachments

### references/

- `api_reference.md`: Comprehensive API endpoint documentation with parameters and examples
- `authentication_guide.md`: Detailed authentication setup and configuration instructions
- `integrations.md`: Third-party integration setup guides and use cases