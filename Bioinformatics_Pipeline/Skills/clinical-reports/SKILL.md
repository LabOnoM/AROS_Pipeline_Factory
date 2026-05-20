---
name: clinical-reports
---
description: Generated skill clinical-reports

---
name: clinical-reports
description: "Write comprehensive clinical reports (case reports, diagnostic reports, clinical trial reports, and patient documentation) with accuracy, regulatory compliance (HIPAA/FDA/ICH-GCP), and validation tooling. Includes templates and scripting support."
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
skill-author: AIPOCH
---

## Overview

This skill facilitates the creation of various clinical reports, ensuring accuracy, regulatory compliance, and adherence to established standards. It covers case reports, diagnostic reports, clinical trial reports, and patient documentation. Use this skill for healthcare documentation, research dissemination, and regulatory compliance.

**Critical Principle: Clinical reports must be accurate, complete, objective, and compliant with applicable regulations (HIPAA, FDA, ICH-GCP). Patient privacy and data integrity are paramount. All clinical documentation must support evidence-based decision-making and meet professional standards. The final report must begin with a clear and concise summary of the key biological findings, providing an immediate understanding of the analysis's most important insights.**

## When to Use This Skill

This skill should be used when:

1.  Drafting a **journal-ready clinical case report** that follows **CARE** guidelines and includes consent/de-identification.
2.  Producing **diagnostic reports** (radiology, pathology, laboratory) that are structured, actionable, and consistent with common standards (e.g., ACR/CAP conventions).
3.  Preparing **clinical trial safety documentation**, especially **Serious Adverse Event (SAE)** narratives and submissions under regulatory timelines.
4.  Writing an **ICH E3–aligned Clinical Study Report (CSR)** for sponsor/regulatory submission, including appendices and traceable data presentation.
5.  Creating or QA **patient medical record documentation** (SOAP notes, H&P, discharge summaries) for continuity of care, billing support, and medico-legal defensibility.

## Key Features

-   **Template-driven authoring** for:
    -   Case reports (CARE)
    -   Radiology / pathology / lab reports
    -   SAE reports and CSR (ICH E3)
    -   SOAP, H&P, discharge summaries
-   **Compliance-first workflow**
    -   HIPAA de-identification (Safe Harbor identifiers checklist)
    -   FDA documentation awareness (e.g., 21 CFR Parts 11/50/56/312)
    -   ICH-GCP principles (data integrity, auditability, consent, protocol adherence)
-   **Validation and QA tooling**
    -   Completeness checks per report type
    -   De-identification scanning
    -   Consistency checks across sections (dates, identifiers, outcomes)
-   **Publication-quality data presentation guidance**
    -   Tables/figures conventions, labeling, precision, and safety summaries
    -   Trial flow diagrams and case timelines
-   **Reference and asset library integration**
    -   Uses supporting files under `references/` and `assets/` for standards and templates

## Dependencies

-   Python **3.10+**
-   (Optional, for automation scripts) Common Python tooling typically used in this repository:
    -   `argparse` (stdlib)
    -   `re` (stdlib)
    -   `json` (stdlib)

> Note: The provided scripts and templates are referenced by path (e.g., `scripts/validate_case_report.py`). If your repository defines additional pinned packages (e.g., in `requirements.txt`), use those versions as the source of truth.

## Example Usage

Below is a complete, runnable example that generates a report skeleton, validates it, and checks de-identification. Adjust paths to match your repository layout.

### 1) Generate a template (interactive or parameterized)

```bash
python scripts/generate_report_template.py
```

If the generator supports arguments in your repo, you can typically do something like:

```bash
python scripts/generate_report_template.py --type case-report --out reports/case_report.md
```

### 2) Validate a CARE case report draft

```bash
python scripts/validate_case_report.py reports/case_report.md
```

### 3) Check HIPAA de-identification (Safe Harbor scan)

```bash
python scripts/check_deidentification.py reports/case_report.md
```

### 4) (Optional) Validate a clinical trial report structure (ICH E3)

```bash
python scripts/validate_trial_report.py reports/csr.md
```

### 5) Use a template asset directly (copy and fill)

```bash
cp assets/soap_note_template.md reports/soap_note.md
```

Recommended supporting references while writing:

-   CARE and case report guidance: `references/case_report_guidelines.md`
-   Diagnostic reporting standards: `references/diagnostic_reports_standards.md`
-   Trial reporting (SAE/CSR, ICH E3): `references/clinical_trial_reporting.md`
-   Regulatory compliance (HIPAA/FDA/ICH-GCP): `references/regulatory_compliance.md`

## Core Capabilities

### 1. Clinical Case Reports for Journal Publication

Clinical case reports describe unusual clinical presentations, novel diagnoses, or rare complications. They contribute to medical knowledge and are published in peer-reviewed journals.

#### CARE Guidelines Compliance

The CARE (CAse REport) guidelines provide a standardiz