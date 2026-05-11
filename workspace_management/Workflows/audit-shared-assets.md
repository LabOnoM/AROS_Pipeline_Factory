# Workflow: `/audit-shared-assets`

**Description**: Programmatically verifies the integrity of the Shared Asset Management System (SAMS) and enforces Cross-Pipeline Compatibility Protocol (CPCP) compliance.

**When to use**: 
- After merging PRs affecting `01.Shared_Assets/` or `00.RawData/SHARED_ASSET_REGISTRY.md`.
- As a routine health check of the AROS Pipeline Factory repository.
- During project onboarding to verify SAMS state.

**Pre-requisites**:
- Must run on a Linux/macOS environment (Windows OS is not supported due to symlink requirements).
- `pyyaml` installed.

## Step 1: Run the Audit Script
// turbo
Execute the programmatic Python audit:
```bash
python3 01.Shared_Assets/Scripts/audit_shared_assets.py
```

## Step 2: Remediate Findings
If the script outputs an error, take corrective action:
- **Missing frontmatter**: Inject the `cpcp_asset: true` YAML block into the flagged shared asset.
- **Broken symlink**: Verify the target in `01.Shared_Assets/` and recreate the relative symlink.
- **Duplicate physical file**: If a pipeline has a physical copy of a shared asset, replace it with a relative symlink pointing to the canonical asset in `01.Shared_Assets/`.
- **Pre-commit hook missing/invalid**: Re-run the installation or `chmod +x .git/hooks/pre-commit`.

## Step 3: Record Audit Result
Once Step 1 passes cleanly (`✅ SAMS Audit Passed!`), output the success status to the user and consider the repository healthy.
