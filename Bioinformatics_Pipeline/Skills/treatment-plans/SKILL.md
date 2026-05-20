---
name: treatment-plans
description: Generate concise (typically 1–4 pages) patient-centered medical treatment plans in LaTeX/PDF when a clinician needs an actionable plan with SMART goals, evidence-based interventions, monitoring, and HIPAA-aware documentation.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
skill-author: AIPOCH
---
---

## When to Use

Use this skill when you need to produce a **clinically actionable, professionally typeset** treatment plan (LaTeX → PDF), especially when:

1. You must create an **individualized plan** for a patient across any specialty (medicine, surgery, rehab, behavioral health).
2. You need a **concise “quick reference” plan** (often 1 page) for busy clinical workflows.
3. You are coordinating **multidisciplinary care** (e.g., PCP + specialists + PT/OT + behavioral health) with clear roles and follow-up.
4. You must document **chronic disease management** with measurable targets, monitoring cadence, and escalation thresholds.
5. You need a structured plan for **perioperative care** or **pain management** with safety checks and risk mitigation.

## Key Features

- **Concise formats by default**
  - Preferred: **1-page quick reference card**
  - Standard: **3–4 pages** (front-page executive summary + supporting detail)
  - Extended: **5–6 pages** only when complexity requires it
- **Front-page executive summary (Foundation-style)**
  - Page 1 contains only: title + patient/report info + 2–4 colored “key boxes” (goals, interventions, decision points, timeline)
- **SMART goals**
  - Short- and long-term goals with measurable targets and time bounds
- **Evidence-based interventions with minimal citations**
  - Typically **0–3 brief in-text citations** (e.g., “ADA 2024”)
- **HIPAA-aware documentation**
  - De-identification expectations and documentation hygiene
- **Validation workflow**
  - Completeness and quality checks via scripts (sections present, SMART goals, monitoring adequacy, safety/risk mitigation)
- **Professional LaTeX styling**
  - Custom style package with colored boxes and tables for scan-friendly clinical documents
- **Visual support**
  - Supports adding at least one diagram (e.g., pathway, timeline, decision algorithm) to improve usability

## Dependencies

> Versions may vary by environment; pin them in your project if you need reproducibility.

- **Python**: 3.10+
- **TeX distribution**: TeX Live 2022+ (or MiKTeX equivalent)
- **LaTeX engines**:
  - `xelatex` (recommended)
  - `pdflatex` (supported)
- **Key LaTeX packages** (commonly required by the style/templates):
  - `tcolorbox` (with `most` library), `tikz/pgf`, `geometry`, `xcolor`, `fontspec` (XeLaTeX/LuaLaTeX), `fancyhdr`, `titlesec`, `enumitem`, `booktabs`, `longtable`, `array`, `colortbl`, `hyperref`, `natbib`
- **Project scripts (as referenced by this skill)**:
  - `scripts/generate_template.py`
  - `check_completeness.py`
  - `validate_treatment_plan.py`
  - `timeline_generator.py`
  - (optional) `scripts/generate_schematic.py` for diagram generation

## Example Usage

Below is a complete, runnable example that (1) generates a template, (2) compiles to PDF, and (3) runs validation checks. Adjust paths to match your repository layout.

### 1) Generate a LaTeX template

```bash
cd .claude/skills/treatment-plans/scripts

# Generate a mental health plan template
python generate_template.py --type mental_health --output depression_treatment_plan.tex
```

### 2) (Optional) Generate a diagram for the plan

```bash
# Example: a simple treatment pathway flowchart
python scripts/generate_schematic.py "Depression treatment pathway: assessment -> CBT/SSRI -> monitoring -> escalation criteria" -o figures/depression_pathway.png
```

Include the figure in your `.tex` file (example snippet):

```latex
\begin{figure}[h]
  \centering
  \includegraphics[width=0.95\linewidth]{figures/depression_pathway.png}
  \caption{Treatment pathway overview.}
\end{figure}
```

### 3) Compile to PDF

```bash
# Recommended (better font support)
xelatex depression_treatment_plan.tex

# If you use bibliography features
bibtex depression_treatment_plan || true
xelatex depression_treatment_plan.tex
xelatex depression_treatment_plan.tex
```

### 4) Run completeness and quality validation

```bash
python check_completeness.py depression_treatment_plan.tex
python validate_treatment_plan.py depression_treatment_plan.tex
```

### 5) (Optional) Generate a timeline artifact

```bash
python timeline_generator.py --plan depression_treatment_plan.tex --output timeline.pdf
```

## Implementation Details

### Document length strategy

- Start with the **1-page format** whenever possible.
- Expand to **3–4 pages** only when you need supporting detail (education, coordination, safety monitoring).
- Use **5–6 pages** rarely (multiple comorbidities, complex monitoring, research protocols).

### First Page Summary (Foundation Medicine Model)

**CRITICAL REQUIREMENT: All treatment plans MUST have a complete executive summary on the first page ONLY, before any table of contents or detailed sections.**

Following the Foundation Medicine model for precision medicine reporting and clinical summary documents, treatment plans begin with a one-page executive summary that provides immediate access to key actionable information. This entire summary must fit on the first page.

**Required First Page Structure (in order):**

1. **Title and Subtitle**
   - Main title: Treatment plan type (e.g., "Comprehensive Treatment Plan")
   - Subtitle: Specific condition or focus (e.g., "Type 2 Diabetes Mellitus - Young Adult Patient")

2. **Report Information Box** (using `\begin{infobox}` or `\begin{patientinfo}`)
   - Report type/document purpose
   - Date of plan creation
   - Patient demographics (age, sex, de-identified)
   - Primary diagnosis with ICD-10 code
   - Report author/clinic (if applicable)
   - Analysis approach or framework used

3. **Key Findings or Treatment Highlights** (2-4 colored boxes using appropriate box types)
   - **Primary Treatment Goals** (using `\begin{goalbox}`)
     - 2-3 SMART goals in bullet format
   - **Main Interventions** (using `\begin{keybox}` or `\begin{infobox}`)
     - 2-3 key interventions (pharmacological, non-pharmacological, monitoring)
   - **Critical Decision Points** (using `\begin{warningbox}` if urgent)
     - Important monitoring thresholds or safety considerations
   - **Timeline Overview** (using `\begin{infobox}`)
     - Brief treatment duration/phases
     - Key milestone dates

Minimal LaTeX skeleton:

```latex
\maketitle
\thispagestyle{empty}

\begin{patientinfo}
  % De-identified demographics, diagnosis, date, framework
\end{patientinfo}

\begin{goalbox}[Primary Treatment Goals]
  \begin{itemize}
    \item Goal 1 (metric + timeframe)
    \item Goal 2 (metric + timeframe)
  \end{itemize}
\end{goalbox}

\begin{keybox}[Core Interventions]
  \begin{itemize}
    \item Intervention 1 (dose/frequency if applicable)
    \item Intervention 2 (visit cadence / therapy frequency)
  \end{itemize}
\end{keybox}

\begin{warningbox}[Critical Decision Points]
  \begin{itemize}
    \item Escalate if threshold X is met
  \end{itemize}
\end{warningbox}

\newpage
\tableofcontents
\newpage
```

### Core clinical sections (for standard 3–4 page plans)

Include only what changes decisions; prefer tables/bullets:

- Patient info (de-identified), diagnoses (ICD-10 where applicable)
- Assessment summary and risk stratification
- SMART goals (short- and long-term)
- Interventions:
  - pharmacologic (dose/route/frequency/titration + monitoring)
  - non-pharmacologic (lifestyle, therapy, education)
  - procedural/referrals/testing
- Timeline and follow-up schedule
- Monitoring parameters + escalation thresholds
- Expected outcomes (brief)
- Patient education (3–5 key takeaways + red flags)
- Risk mitigation (high-yield safety items only)
- Signature/date block

### Citation policy (minimalist)

- Use **brief in-text citations** only when needed (guidelines, nonstandard regimens, controversial interventions).
- Typical target: **0–3 citations** for a 3–4 page plan.
- Avoid long bibliographies unless explicitly required.

### Validation logic (what scripts should check)

- **Completeness**: required sections exist (goals, interventions, monitoring, follow-up, education, risk mitigation).
- **SMART quality**: goals include metric + timeframe; avoid vague phrasing.
- **Feasibility**: timeline cadence matches interventions; monitoring is realistic.
- **Safety**: contraindications, interaction checks, escalation thresholds, opioid safeguards (if applicable).
- **Compliance hygiene**: de-identification expectations and documentation defensibility.

### Template selection guidance

- `one_page_treatment_plan.tex`: default for most cases (quick reference)
- `general_medical_treatment_plan.tex`: internal medicine / general practice
- `rehabilitation_treatment_plan.tex`: PT/OT/SLP protocols and milestones
- `mental_health_treatment_plan.tex`: psychotherapy + pharmacotherapy + safety plan
- `chronic_disease_management_plan.tex`: long-term targets + coordination
- `perioperative_care_plan.tex`: pre/intra/post-op structure (ERAS, VTE, antibiotics)
- `pain_management_plan.tex`: multimodal analgesia + opioid risk mitigation

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every treatment plan MUST include at least 1 AI-generated figure using the scientific-schematics skill.**

This is not optional. Treatment plans benefit greatly from visual elements. Before finalizing any document:
1. Generate at minimum ONE schematic or diagram (e.g., treatment pathway flowchart, care coordination diagram, or therapy timeline)
2. For complex plans: include decision algorithm flowchart
3. For rehabilitation plans: include milestone progression diagram

**How to generate figures:**
- Use the **scientific-schematics** skill to generate AI-powered publication-quality diagrams
- Simply describe your desired diagram in natural language
- Nano Banana Pro will automatically generate, review, and refine the schematic

**How to generate schematics:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

The AI will automatically:
- Create publication-quality images with proper formatting
- Review and refine through multiple iterations
- Ensure accessibility (colorblind-friendly, high contrast)
- Save outputs in the figures/ directory

**When to add schematics:**
- Treatment pathway flowcharts
- Care coordination diagrams
- Therapy progression timelines
- Multidisciplinary team interaction diagrams
- Medication management flowcharts
- Rehabilitation protocol visualizations
- Clinical decision algorithm diagrams
- Any complex concept that benefits from visualization

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

## Professional Document Styling

### Overview

Treatment plans can be enhanced with professional medical document styling using the `medical_treatment_plan.sty` LaTeX package. This custom style transforms plain academic documents into visually appealing, color-coded clinical documents that maintain scientific rigor while improving readability and usability.

### Medical Treatment Plan Style Package

The `medical_treatment_plan.sty` package (located in `assets/medical_treatment_plan.sty`) provides:

**Professional Color Scheme**
- **Primary Blue** (RGB: 0, 102, 153): Headers, section titles, primary accents
- **Secondary Blue** (RGB: 102, 178, 204): Light backgrounds, subtle accents
- **Accent Blue** (RGB: 0, 153, 204): Hyperlinks, key highlights
- **Success Green** (RGB: 0, 153, 76): Goals, positive outcomes
- **Warning Red** (RGB: 204, 0, 0): Warnings, critical information
- **Dark Gray** (RGB: 64, 64, 64): Body text
- **Light Gray** (RGB: 245, 245, 245): Background fills

**Styled Elements**
- Custom colored headers and footers with professional rules
- Blue section titles with underlines for clear hierarchy
- Enhanced table formatting with colored headers and alternating rows
- Optimized list spacing with colored bullets and numbering
- Professional page layout with appropriate margins

### Custom Information Boxes

The style package includes five specialized box environments for organizing clinical information:

#### 1. Info Box (Blue Border, Light Gray Background)

For general information, clinical assessments, and testing schedules:

```latex
\begin{infobox}[Title]
  \textbf{Key Information:}
  \begin{itemize}
    \item Clinical assessment details
    \item Testing schedules
    \item General guidance
  \end{itemize}
\end{infobox}
```

**Use cases**: Metabolic status, baseline assessments, monitoring schedules, titration protocols

#### 2. Warning Box (Red Border, Yellow Background)

For critical decision points, safety protocols, and alerts:

```latex
\begin{warningbox}[Alert Title]
  \textbf{Important Safety Information:}
  \begin{itemize}
    \item Critical drug interactions
    \item Safety monitoring requirements
    \item Red flag symptoms requiring immediate action
  \end{itemize}
\end{warningbox}
```

**Use cases**: Medication safety, decision points, contraindications, emergency protocols

#### 3. Goal Box (Green Border, Green-Tinted Background)

For treatment goals, targets, and success criteria:

```latex
\begin{goalbox}[Treatment Goals]
  \textbf{Primary Objectives:}
  \begin{itemize}
    \item Reduce HbA1c to <7\% within 3 months
    \item Achieve 5-7\% weight loss in 12 weeks
    \item Complete diabetes education program
  \end{itemize}
\end{goalbox}
```

**Use cases**: SMART goals, target outcomes, success metrics, CGM goals

#### 4. Key Points Box (Blue Background)

For executive summaries, key takeaways, and important recommendations:

```latex
\begin{keybox}[Key Highlights]
  \textbf{Essential Points:}
  \begin{itemize}
    \item Main therapeutic approach
    \item Critical patient instructions
    \item Priority interventions
  \end{itemize}
\end{keybox}
```

**Use cases**: Plan overview, plate method instructions, important dietary guidelines

#### 5. Emergency Box (Large Red Design)

For emergency contacts and urgent protocols:

```latex
\begin{emergencybox}
  \begin{itemize}
    \item \textbf{Emergency Services:} 911
    \item \textbf{Endocrinology Office:} [Phone] (business hours)
    \item \textbf{After-Hours Hotline:} [Phone] (nights/weekends)
    \item \textbf{Pharmacy:} [Phone and location]
  \end{itemize}
\end{emergencybox}
```

**Use cases**: Emergency contacts, critical hotlines, urgent resource information

#### 6. Patient Info Box (White with Blue Border)

For patient demographics and baseline information:

```latex
\begin{patientinfo}
  \begin{tabular}{ll}
    \textbf{Age:} & 23 years \\
    \textbf{Sex:} & Male \\
    \textbf{Diagnosis:} & Type 2 Diabetes Mellitus \\
    \textbf{Plan Start Date:} & \today \\
  \end{tabular}
\end{patientinfo}
```

**Use cases**: Patient information sections, demographic data

### Professional Table Formatting

Enhanced table environment with medical styling:

```latex
\begin{medtable}{Caption Text}
\begin{tabular}{|p{5cm}|p{4cm}|p{4.5cm}|}
\hline
\tableheadercolor  % Blue header with white text
\textcolor{white}{\textbf{Column 1}} & 
\textcolor{white}{\textbf{Column 2}} & 
\textcolor{white}{\textbf{Column 3}} \\
\hline
Data row 1 content & Value 1 & Details 1 \\
\hline
\tablerowcolor  % Alternating light gray row
Data row 2 content & Value 2 & Details 2 \\
\hline
Data row 3 content & Value 3 & Details 3 \\
\hline
\end{tabular}
\caption{Table caption}
\end{medtable}
```

**Features:**
- Blue headers with white text for visual prominence
- Alternating row colors (`\tablerowcolor`) for improved readability
- Automatic centering and spacing
- Professional borders and padding

### Using the Style Package

#### Basic Setup

1. **Add to document preamble:**

```latex
% !TEX program = xelatex
\documentclass[11pt,letterpaper]{article}

% Use custom medical treatment plan style
\usepackage{medical_treatment_plan}
\usepackage{natbib}

\begin{document}
\maketitle
% Your content here
\end{document}
```

2. **Ensure style file is in same directory** as your `.tex` file, or install to LaTeX path

3. **Compile with XeLaTeX** (recommended for best results):

```bash
xelatex treatment_plan.tex
bibtex treatment_plan
xelatex treatment_plan.tex
xelatex treatment_plan.tex
```

#### Custom Title Page

The package automatically formats the title with a professional blue header:

```latex
\title{\textbf{Individualized Diabetes Treatment Plan}\\
\large{23-Year-Old Male Patient with Type 2 Diabetes}}
\author{Comprehensive Care Plan}
\date{\today}

\begin{document}
\maketitle
```

This creates an eye-catching blue box with white text and clear hierarchy.

### Compilation Requirements

**Required LaTeX Packages** (automatically loaded by the style):
- `geometry` - Page layout and margins
- `xcolor` - Color support
- `tcolorbox` with `[most]` library - Custom colored boxes
- `tikz` - Graphics and drawing
- `fontspec` - Font management (XeLaTeX/LuaLaTeX)
- `fancyhdr` - Custom headers and footers
- `titlesec` - Section styling
- `enumitem` - Enhanced list formatting
- `booktabs` - Professional table rules
- `longtable` - Multi-page tables
- `array` - Enhanced table features
- `colortbl` - Colored table cells
- `hyperref` - Hyperlinks and PDF metadata
- `natbib` - Bibliography management

**Recommended Compilation:**

```bash
# Using XeLaTeX (best font support)
xelatex document.tex
bibtex document
xelatex document.tex
xelatex document.tex

# Using PDFLaTeX (alternative)
pdflatex document.tex
bibtex document
pdflatex document.tex
pdflatex document.tex
```

### Customization Options

#### Changing Colors

Edit the style file to modify the color scheme:

```latex
% In medical_treatment_plan.sty
\definecolor{primaryblue}{RGB}{0, 102, 153}      % Modify these
\definecolor{secondaryblue}{RGB}{102, 178, 204}
\definecolor{accentblue}{RGB}{0, 153, 204}
\definecolor{successgreen}{RGB}{0, 153, 76}
\definecolor{warningred}{RGB}{204, 0, 0}
```

#### Adjusting Page Layout

Modify geometry settings in the style file:

```latex
\RequirePackage[margin=1in, top=1.2in, bottom=1.2in]{geometry}
```

#### Custom Fonts (XeLaTeX only)

Uncomment and modify in the style file:

```latex
\setmainfont{Your Preferred Font}
\setsansfont{Your Sans-Serif Font}
```

#### Header/Footer Customization

Modify in the style file:

```latex
\fancyhead[L]{\color{primaryblue}\sffamily\small\textbf{Treatment Plan Title}}
\fancyhead[R]{\color{darkgray}\sffamily\small Patient Info}
```

### Style Package Download and Installation

#### Option 1: Copy to Project Directory

Copy `assets/medical_treatment_plan.sty` to the same directory as your `.tex` file.

#### Option 2: Install to User TeX Directory

```bash
# Find your local texmf directory
kpsewhich -var-value TEXMFHOME

# Copy to appropriate location (usually ~/texmf/tex/latex/)
mkdir -p ~/texmf/tex/latex/medical_treatment_plan
cp assets/medical_treatment_plan.sty ~/texmf/tex/latex/medical_treatment_plan/

# Update TeX file database
texhash ~/texmf
```

#### Option 3: System-Wide Installation

```bash
# Copy to system texmf directory (requires sudo)
sudo cp assets/medical_treatment_plan.sty /usr/local/texlive/texmf-local/tex/latex/
sudo texhash
```

### Additional Professional Styles (Optional)

Other medical/clinical document styles available from CTAN:

**Journal Styles:**
```bash
# Install via TeX Live Manager
tlmgr install nejm        # New England Journal of Medicine
tlmgr install jama        # JAMA style
tlmgr install bmj         # British Medical Journal
```

**General Professional Styles:**
```bash
tlmgr install apa7        # APA 7th edition (health sciences)
tlmgr install IEEEtran    # IEEE (medical devices/engineering)
tlmgr install springer    # Springer journals
```

**Download from CTAN:**
- Visit: https://ctan.org/
- Search for medical document classes
- Download and install per package instructions

### Troubleshooting

**Issue: Package not found**
```bash
# Install missing packages via TeX Live Manager
sudo tlmgr update --self
sudo tlmgr install tcolorbox tikz pgf
```

**Issue: Missing characters (✓, ≥, etc.)**
- Use XeLaTeX instead of PDFLaTeX
- Or replace with LaTeX commands: `$\checkmark$`, `$\geq$`
- Requires `amssymb` package for math symbols

**Issue: Header height warnings**
- Style file sets `\setlength{\headheight}{22pt}`
- Adjust if needed for your content

**Issue: Boxes not rendering**
```bash
# Ensure complete tcolorbox installation
sudo tlmgr install tcolorbox tikz pgf
```

**Issue: Font not found (XeLaTeX)**
- Comment out custom font lines in .sty file
- Or install specified fonts on your system

### Best Practices for Styled Documents

1. **Appropriate Box Usage**
   - Match box type to content purpose (goals→green, warnings→yellow/red)
   - Don't overuse boxes; reserve for truly important information
   - Keep box content concise and focused

2. **Visual Hierarchy**
   - Use section styling for structure
   - Boxes for emphasis and organization
   - Tables for comparative data
   - Lists for sequential or grouped items

3. **Color Consistency**
   - Stick to defined color scheme
   - Use `\textcolor{primaryblue}{\textbf{Text}}` for emphasis
   - Maintain consistent meaning (red=warning, green=goals)

4. **White Space**
   - Don't overcrowd pages with boxes
   - Use `\vspace{0.5cm}` between major sections
   - Allow breathing room around colored elements

5. **Professional Appearance**
   - Maintain readability as top priority
   - Ensure sufficient contrast for accessibility
   - Test print output in grayscale
   - Keep styling consistent throughout document

6. **Table Formatting**
   - Use `\tableheadercolor` for all header rows
   - Apply `\tablerowcolor` to alternating rows in tables >3 rows
   - Keep column widths balanced
   - Use `\small\sffamily` for large tables

### Example: Styled Treatment Plan Structure

```latex
% !TEX program = xelatex
\documentclass[11pt,letterpaper]{article}
\usepackage{medical_treatment_plan}
\usepackage{natbib}

\title{\textbf{Comprehensive Treatment Plan}\\
\large{Patient-Centered Care Strategy}}
\author{Multidisciplinary Care Team}
\date{\today}

\begin{document}
\maketitle

\section*{Patient Information}
\begin{patientinfo}
  % Demographics table
\end{patientinfo}

\section{Executive Summary}
\begin{keybox}[Plan Overview]
  % Key highlights
\end{keybox}

\section{Treatment Goals}
\begin{goalbox}[SMART Goals - 3 Months]
  \begin{medtable}{Primary Treatment Targets}
    % Goals table with colored headers
  \end{medtable}
\end{goalbox}

\section{Medication Plan}
\begin{infobox}[Titration Schedule]
  % Medication instructions
\end{infobox}

\begin{warningbox}[Critical Decision Point]
  % Important safety information
\end{warningbox}

\section{Emergency Protocols}
\begin{emergencybox}
  % Emergency contacts
\end{emergencybox}

\bibliographystyle{plainnat}
\bibliography{references}
\end{document}
```

### Benefits of Professional Styling

**Clinical Practice:**
- Faster information scanning during patient encounters
- Clear visual hierarchy for critical vs. routine information
- Professional appearance suitable for patient-facing documents
- Color-coded sections reduce cognitive load

**Educational Use:**
- Enhanced readability for teaching materials
- Visual differentiation of concept types (goals, warnings, procedures)
- Professional presentation for case discussions
- Print and digital-ready formats

**Documentation Quality:**
- Modern, polished appearance
- Maintains clinical accuracy while improving aesthetics
- Standardized formatting across treatment plans
- Easy to customize for institutional branding

**Patient Engagement:**
- More approachable than dense text documents
- Color coding helps patients identify key sections
- Professional appearance builds trust
- Clear organization facilitates understanding

## Ethical Considerations

### Informed Consent
All treatment plans should involve patient understanding and voluntary agreement to proposed interventions.

### Cultural Sensitivity
Treatment plans must respect diverse cultural beliefs, health practices, and communication styles.

### Health Equity
Consider social determinants of health, access barriers, and health disparities when developing plans.

### Privacy Protection
Maintain strict HIPAA compliance; de-identify all protected health information in shared documents.

### Autonomy and Beneficence
Balance medical recommendations with patient autonomy and values while promoting patient welfare.

## Common Use Cases

### Example 1: Type 2 Diabetes Management

**Scenario**: 58-year-old patient with newly diagnosed Type 2 diabetes, HbA1c 8.5%, BMI 32

**Template**: `general_medical_treatment_plan.tex`

**Goals**:
- Short-term: Reduce HbA1c to <7.5% in 3 months
- Long-term: Achieve HbA1c <7%, lose 15 pounds in 6 months

**Interventions**:
- Pharmacological: Metformin 500mg BID, titrate to 1000mg BID
- Lifestyle: Mediterranean diet, 150 min/week moderate exercise
- Education: Diabetes self-management education, glucose monitoring

### Example 2: Post-Stroke Rehabilitation

**Scenario**: 70-year-old patient s/p left MCA stroke with right hemiparesis

**Template**: `rehabilitation_treatment_plan.tex`

**Goals**:
- Short-term: Improve right arm strength 2/5 to 3/5 in 4 weeks
- Long-term: Independent ambulation 150 feet with cane in 12 weeks

**Interventions**:
- PT 3x/week: Gait training, balance, strengthening
- OT 3x/week: ADL training, upper extremity function
- SLP 2x/week: Dysphagia therapy

### Example 3: Major Depressive Disorder

**Scenario**: 35-year-old with moderate depression, PHQ-9 score 16

**Template**: `mental_health_treatment_plan.tex`

**Goals**:
- Short-term: Reduce PHQ-9 to <10 in 8 weeks
- Long-term: Achieve remission (PHQ-9 <5), return to work

**Interventions**:
- Psychotherapy: CBT weekly sessions
- Medication: Sertraline 50mg daily, titrate to 100mg
- Lifestyle: Sleep hygiene, exercise 30 min 5x/week

### Example 4: Total Knee Arthroplasty

**Scenario**: 68-year-old scheduled for right TKA for osteoarthritis

**Template**: `perioperative_care_plan.tex`

**Preoperative Goals**:
- Optimize diabetes control (glucose <180)
- Discontinue anticoagulation per protocol
- Complete medical clearance

**Postoperative Goals**:
- Ambulate 50 feet by POD 1
- 90-degree knee flexion by POD 3
- Discharge home with PT services by POD 2-3

### Example 5: Chronic Low Back Pain

**Scenario**: 45-year-old with chronic non-specific low back pain, pain 7/10

**Template**: `pain_management_plan.tex`

**Goals**:
- Short-term: Reduce pain to 4/10 in 6 weeks
- Long-term: Return to work full-time, pain 2-3/10

**Interventions**:
- Pharmacological: Gabapentin 300mg TID, duloxetine 60mg daily
- PT: Core strengthening, McKenzie exercises 2x/week x 8 weeks
- Behavioral: CBT for pain, mindfulness meditation
- Interventional: Consider lumbar ESI if inadequate response

## Professional Standards and Guidelines

Treatment plans should align with:

### General Medicine
- American Diabetes Association (ADA) Standards of Care
- ACC/AHA Cardiovascular Guidelines
- GOLD COPD Guidelines
- JNC-8 Hypertension Guidelines
- KDIGO Chronic Kidney Disease Guidelines

### Rehabilitation
- APTA Clinical Practice Guidelines
- AOTA Practice Guidelines
- Cardiac Rehabilitation Guidelines (AHA/AACVPR)
- Stroke Rehabilitation Guidelines

### Mental Health
- APA Practice Guidelines
- VA/DoD Clinical Practice Guidelines
- NICE Guidelines (National Institute for Health and Care Excellence)
- Cochrane Reviews for psychiatric interventions

### Pain Management
- CDC Opioid Prescribing Guidelines
- AAPM/APS Chronic Pain Guidelines
- WHO Pain Ladder
- Multimodal Analgesia Best Practices

## Timeline Generation

Use the timeline generator script to create visual treatment timelines:

```bash
python timeline_generator.py --plan my_treatment_plan.tex --output timeline.pdf
```

Generates:
- Gantt chart of treatment phases
- Milestone markers for goal assessments
- Medication titration schedules
- Follow-up appointment calendar
- Intervention intensity over time

## Support and Resources

### Template Generation

Interactive template selection:

```bash
cd .claude/skills/treatment-plans/scripts
python generate_template.py

# Or specify type directly
python generate_template.py --type mental_health --output depression_treatment_plan.tex
```

### Validation Workflow

1. **Create treatment plan** using appropriate LaTeX template
2. **Check completeness**: `python check_completeness.py plan.tex`
3. **Validate quality**: `python validate_treatment_plan.py plan.tex`
4. **Review checklist**: Compare against `quality_checklist.md`
5. **Generate PDF**: `pdflatex plan.tex`
6. **Review with patient**: Ensure understanding and agreement
7. **Implement and document**: Track progress in clinical notes

### Additional Resources

- Clinical practice guidelines from specialty societies
- AHRQ Effective Health Care Program
- Cochrane Library for intervention evidence
- UpToDate and DynaMed for treatment recommendations
- CMS Quality Measures and HEDIS specifications

## Integration with Other Skills

### Clinical Reports Integration

Treatment plans often accompany other clinical documentation:

- **SOAP Notes** (`clinical-reports` skill): Document ongoing implementation
- **H&P** (`clinical-reports` skill): Initial assessment informs treatment plan
- **Discharge Summaries** (`clinical-reports` skill): Summarize treatment plan execution
- **Progress Notes**: Track goal achievement and plan modifications

### Scientific Writing Integration

Evidence-based treatment planning requires literature support:

- **Citation Management** (`citation-management` skill): Reference clinical guidelines
- **Literature Review** (`literature-review` skill): Understand treatment evidence base
- **Research Lookup** (`research-lookup` skill): Find current best practices
- **Venue Templates** (`venue-templates` skill): For publication-ready medical writing style

**Medical Writing Style:** When preparing treatment-related content for publication (case reports, clinical guidelines), consult the venue-templates skill's `medical_journal_styles.md` for guidance on evidence-graded language, patient-centered terminology, and structured abstract formats used in NEJM, Lancet, JAMA, and BMJ.

### Research Integration

Treatment plans may be developed for clinical trials or research studies:

- **Research Grants** (`research-grants` skill): Treatment protocols for funded studies
- **Clinical Trial Reports** (`clinical-reports` skill): Intervention documentation

## License

Part of the Claude Scientific Writer project. See main LICENSE file.