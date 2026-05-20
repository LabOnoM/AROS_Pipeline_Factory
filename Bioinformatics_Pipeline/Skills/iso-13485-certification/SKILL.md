---
name: iso-13485-certification
description: A toolkit for preparing ISO 13485:2016 certification documentation for medical device QMS. Use when you need to perform a documentation gap analysis, draft or update a Quality Manual, create required procedures/work instructions, build Medical Device Files (MDF), interpret ISO 13485 clauses, or identify missing documents for certification (often triggered by ISO 13485, QMS certification, FDA QMSR, EU MDR, or quality system documentation requests).
license: MIT
metadata:
    skill-author: K-Dense Inc. + AIPOCH
---

## When to Use

Use this skill in any of the following situations:

1. **Starting ISO 13485 implementation** and you need a structured documentation set (Quality Manual, procedures, records, templates).
2. **Assessing an existing QMS** and you want a **gap analysis** against ISO 13485:2016 requirements and mandatory documentation.
3. **Preparing for a certification audit** and you need readiness checks, evidence mapping, and prioritized remediation actions.
4. **Creating or updating specific SOPs** (e.g., CAPA, complaint handling, internal audit, document/record control) using consistent templates.
5. **Transitioning or harmonizing with regulations** (e.g., **FDA QMSR** alignment, **EU MDR** documentation expectations) and you need to reorganize device documentation (e.g., MDF).

## Key Features

- **Automated documentation gap analysis** via `scripts/gap_analyzer.py` to detect missing/covered QMS documents.
- **Clause-by-clause ISO 13485 reference guidance** using `references/iso-13485-requirements.md`.
- **Mandatory documentation mapping** (procedures and required documents) using `references/mandatory-documents.md`.
- **Comprehensive audit-style checklist** for detailed assessments using `references/gap-analysis-checklist.md`.
- **Template-based document generation** for Quality Manual and key procedures under `assets/templates/`.
- **Medical Device File (MDF) guidance** aligned to ISO 13485 Clause 4.2.3 and FDA QMSR harmonization concepts.

## Dependencies

- **Python**: 3.10+ (recommended)
- **pip**: 23+ (recommended)

> Note: This skill references a script (`scripts/gap_analyzer.py`). If it introduces additional third-party packages, install them per the repository’s `requirements.txt` (if present). If no `requirements.txt` exists, the script is expected to run on the Python standard library.

## Example Usage

### 1) Run an automated gap analysis (end-to-end)

```bash
# 1) (Optional) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows PowerShell

# 2) Run the gap analyzer against your existing QMS document folder
python scripts/gap_analyzer.py \
  --docs-dir ./my-qms-docs \
  --output ./gap-report.json

# 3) Review the output
cat ./gap-report.json
```

### 2) Use the references and templates to draft core documents

A typical workflow after generating `gap-report.json`:

1. Read ISO clause guidance:
   - `references/iso-13485-requirements.md`
2. Confirm mandatory documents and applicability:
   - `references/mandatory-documents.md`
3. Draft/update the Quality Manual:
   - `assets/templates/quality-manual-template.md`
   - Guidance: `references/quality-manual-guide.md`
4. Draft priority procedures (examples):
   - `assets/templates/procedures/document-control-procedure-template.md`
   - `assets/templates/procedures/CAPA-procedure-template.md`
5. Perform a detailed checklist-based assessment:
   - `references/gap-analysis-checklist.md`

## Core Workflow

### 1. Assess Current State (Gap Analysis)

**When to start here:** User has existing documentation and needs to identify gaps

**Process:**

1. **Collect existing documentation:**
   - Ask user to provide directory of current QMS documents
   - Documents can be in any format (.txt, .md, .doc, .docx, .pdf)
   - Include any procedures, manuals, work instructions, forms

2. **Run gap analysis script:**
   ```bash
   python scripts/gap_analyzer.py --docs-dir <path_to_docs> --output gap-report.json
   ```

3. **Review results:**
   - Identify which of the required procedures are present
   - Identify missing key documents (Quality Manual, MDF, etc.)
   - Calculate compliance percentage (estimated)
   - Prioritize missing documentation

4. **Present findings to user:**
   - Summarize what exists
   - Clearly list what's missing
   - Provide prioritized action plan
   - Estimate effort required

**Output:** Comprehensive gap analysis report with prioritized action items

### 2. Understand Requirements (Reference Consultation)

**When to use:** User needs to understand specific ISO 13485 requirements

**Available references:**
- `references/iso-13485-requirements.md` - Complete clause-by-clause breakdown
- `references/mandatory-documents.md` - All required procedures explained
- `references/gap-analysis-checklist.md` - Detailed compliance checklist
- `references/quality-manual-guide.md` - How to create Quality Manual

### 3. Create Documentation (Template-Based Generation)

**When to use:** User needs to create specific QMS documents

**Available templates:**
- Quality Manual: `assets/templates/quality-manual-template.md`
- CAPA Procedure: `assets/templates/procedures/CAPA-procedure-template.md`
- Document Control: `assets/templates/procedures/document-control-procedure-template.md`

#### Document creation priority order:

**Phase 1 - Foundation (Critical):**
1. Quality Manual
2. Quality Policy and Objectives
3. Document Control procedure
4. Record Control procedure

**Phase 2 - Core Processes (High Priority):**
5. Corrective and Preventive Action (CAPA)
6. Complaint Handling
7. Internal Audit
8. Management Review
9. Risk Management

**Phase 3 - Product Realization (High Priority):**
10. Design and Development (if applicable)
11. Purchasing
12. Production and Service Provision
13. Control of Nonconforming Product

**Phase 4 - Supporting Processes (Medium Priority):**
14. Training and Competence
15. Calibration/Control of M&M Equipment
16. Process Validation
17. Product Identification and Traceability

**Phase 5 - Additional Requirements (Medium Priority):**
18. Feedback and Post-Market Surveillance
19. Regulatory Reporting
20. Customer Communication
21. Data Analysis

**Phase 6 - Specialized (If Applicable):**
22. Installation (if applicable)
23. Servicing (if applicable)
24. Sterilization (if applicable)
25. Contamination Control (if applicable)

### 4. Develop Specific Documents

#### Creating Medical Device Files (MDF)

**What is an MDF:**
- File for each medical device type or family
- Replaces separate DHF, DMR, DHR (per FDA QMSR harmonization)
- Contains all documentation about the device

**Required contents per ISO 13485 Clause 4.2.3:**

1. General description and intended use
2. Label and instructions for use specifications
3. Product specifications
4. Manufacturing specifications
5. Procedures for purchasing, manufacturing, servicing
6. Procedures for measuring and monitoring
7. Installation requirements (if applicable)
8. Risk management file(s)
9. Verification and validation information
10. Design and development file(s) (when applicable)

### 5. Conduct Comprehensive Gap Analysis

**When to use:** User wants detailed assessment of all requirements

**Process:**

1. **Use comprehensive checklist:**
   - Open `references/gap-analysis-checklist.md`
   - Work through clause by clause
   - Mark status for each requirement: Compliant, Partial, Non-compliant, N/A

## Implementation Details

### 1) Gap analysis logic (practical model)

The gap analysis workflow is designed to answer:

- **Existence**: Do required documents/procedures appear to exist in the provided document set?
- **Coverage**: Which ISO 13485 clauses and mandatory procedures are addressed?
- **Prioritization**: What should be created/updated first to reduce audit risk?

**Typical inputs**
- A directory containing QMS documentation (e.g., `.md`, `.txt`, `.docx`, `.pdf`), including manuals, SOPs, work instructions, and forms.

**Typical outputs**
- A machine-readable report (e.g., `gap-report.json`) that can be summarized into:
  - Present vs. missing procedures/documents
  - Clause coverage estimates
  - A prioritized action list (Critical/High/Medium/Low)

### 2) ISO 13485 documentation structure (recommended hierarchy)

- **Level 1**: Quality Manual (policy-level mapping to Clauses 4–8)
- **Level 2**: Procedures / SOPs (who/what/when; stable process requirements)
- **Level 3**: Work Instructions (how-to steps; task-level detail)
- **Level 4**: Forms / Records (evidence of implementation)

This skill emphasizes writing procedures that define **what must be done** and **who is responsible**, while keeping detailed step-by-step instructions in work instructions.

### 3) Quality Manual requirements (key checkpoints)

When drafting with `assets/templates/quality-manual-template.md` and `references/quality-manual-guide.md`, ensure:

- The manual includes required content aligned to **ISO 13485 Clause 4.2.2**.
- The **scope** is explicit and any **exclusions** are justified (only where permitted and not impacting safety/effectiveness).
- The manual references the supporting procedures and describes **process interactions** (e.g., a process map).
- Approval/signature expectations are met (top management ownership of policy-level commitments).

### 4) Medical Device File (MDF) content model (Clause 4.2.3)

For each device type/family, the MDF should consolidate or reference:

1. Device description and intended use
2. Labeling and IFU specifications
3. Product and manufacturing specifications
4. Purchasing/manufacturing/servicing procedures (as applicable)
5. Monitoring and measurement procedures
6. Installation requirements (if applicable)
7. Risk management documentation
8. Verification and validation evidence
9. Design and development documentation (if applicable)

This structure supports ISO 13485 expectations and aligns with FDA QMSR’s direction toward consolidated device documentation.

### 5) Procedure customization parameters (what must be decided)

When generating SOPs from templates (e.g., CAPA, document control), the organization must define:

- **Roles and responsibilities** (role-based, not person-based)
- **Triggers and inputs** (complaints, audit findings, nonconformities, feedback)
- **Timeframes** (triage, investigation, closure, effectiveness checks)
- **Decision criteria** (severity, risk, escalation thresholds)
- **Records and retention** (what evidence is kept and for how long)
- **Interfaces** (how CAPA links to complaints, audits, risk management, change control)

### 6) Mandatory procedures list (reference-driven)

Use `references/mandatory-documents.md` as the source of truth for:
- Which procedures are required vs. conditional (“if applicable”)
- How to justify non-applicability
- What evidence/records each procedure should produce

For detailed clause interpretation, use `references/iso-13485-requirements.md`.

## Best Practices

### Exclusions

**When you can exclude:**
- Design and development (if contract manufacturer only)
- Installation (if product requires no installation)
- Servicing (if not offered)
- Sterilization (if non-sterile product)

**Justification requirements:**
- Must be in Quality Manual
- Must explain why excluded
- Cannot exclude if process performed
- Cannot affect ability to provide safe, effective devices

### Document Development

1. **Start at policy level, then add detail:**
   - Quality Manual = policy level
   - Procedures = what, who, when
   - Work Instructions = detailed how-to
   - Forms = data collection

2. **Maintain consistency:**
   - Use same terminology throughout
   - Cross-reference related documents
   - Keep numbering scheme consistent
   - Update all related documents together

3. **Write for your audience:**
   - Clear, simple language
   - Avoid jargon
   - Define technical terms
   - Provide examples where helpful

4. **Make procedures usable:**
   - Action-oriented language
   - Logical flow
   - Clear responsibilities
   - Realistic timeframes

## Resources

### scripts/
- `gap_analyzer.py` - Automated tool to analyze existing documentation and identify gaps against ISO 13485 requirements

### references/
- `iso-13485-requirements.md` - Complete breakdown of ISO 13485:2016 requirements clause by clause
- `mandatory-documents.md` - Detailed list of all required procedures plus other mandatory documents
- `gap-analysis-checklist.md` - Comprehensive checklist for detailed gap assessment
- `quality-manual-guide.md` - Step-by-step guide for creating a compliant Quality Manual

### assets/templates/
- `quality-manual-template.md` - Complete template for Quality Manual with all required sections
- `procedures/CAPA-procedure-template.md` - Example CAPA procedure following best practices
- `procedures/document-control-procedure-template.md` - Example document control procedure

## Quick Reference

### The Required Documented Procedures (See references/mandatory-documents.md for detailed list & applicability)
*(Note: Traditional count is "31 procedures" though list shows more because some are conditional)*

### Key Regulatory Requirements

**FDA (United States):**
- 21 CFR Part 820 (now QMSR) - harmonized with ISO 13485 as of Feb 2026
- Device classification determines requirements
- Establishment registration and device listing required

**EU (European Union):**
- MDR 2017/745 (Medical Devices Regulation)
- IVDR 2017/746 (In Vitro Diagnostic Regulation)
- Technical documentation requirements
- CE marking requirements

**Canada:**
- Canadian Medical Devices Regulations (SOR/98-282)
- Device classification system
- Medical Device Establishment License (MDEL)

**Other Regions:**
- Australia TGA, Japan PMDA, China NMPA, etc.
- Often require or recognize ISO 13485 certification

### Document Retention

**Minimum retention:** Lifetime of medical device as defined by organization

**Typical retention periods:**
- Design documents: Life of device + 5-10 years
- Manufacturing records: Life of device
- Complaint records: Life of device + 5-10 years
- CAPA records: 5-10 years minimum
- Calibration records: Retention period of equipment + 1 calibration cycle

**Always comply with applicable regulatory requirements which may specify longer periods.**

---

## Getting Started

**First-time users should:**

1. Read `references/iso-13485-requirements.md` to understand the standard
2. If you have existing documentation, run gap analysis script
3. Create Quality Manual using template and guide
4. Develop procedures in priority order
5. Use comprehensive checklist for final validation

**For specific tasks:**
- Creating Quality Manual → See Section 3 and use quality-manual-guide.md
- Creating CAPA procedure → See Section 3 and use CAPA template
- Gap analysis → See Section 1 and 5
- Understanding requirements → See Section 2

**Need help?** Start by describing your situation: what stage you're at, what you have, and what you need to create.