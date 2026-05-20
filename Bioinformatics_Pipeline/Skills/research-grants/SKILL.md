---
name: research-grants
description: Write competitive research proposals for NSF, NIH, DOE, DARPA, and Taiwan's NSTC when you need agency-compliant narratives, budgets, and review-criteria alignment for a specific solicitation/FOA/BAA.
license: MIT
skill-author: AIPOCH
allowed-tools: [Read, Write, Edit, Bash]
---

## Overview

This skill assists in developing competitive research proposals for various funding agencies, including NSF, NIH, DOE, DARPA, and Taiwan's NSTC. It focuses on agency-specific requirements, review criteria, narrative structure, budget preparation, and compliance with submission guidelines. A core principle is that grants are persuasive documents demonstrating scientific rigor, innovation, feasibility, and broader impact (or agency-equivalent "value").

## When to Use

Use this skill when you need to produce or revise a grant application that must meet strict agency rules and reviewer expectations, for example:

1. **Preparing a new submission** to NSF, NIH, DOE, DARPA, or Taiwan’s NSTC in response to a specific solicitation/FOA/BAA.
2. **Drafting core narrative sections** (NSF Project Description, NIH Research Strategy, DARPA Technical Volume, DOE Project Narrative, NSTC CM03).
3. **Building agency-specific “value” sections**, such as NSF Broader Impacts, NIH Significance/Innovation, or DARPA transition and milestone narratives.
4. **Creating a compliant budget + justification** aligned to scope, timeline, and agency constraints (e.g., NIH modular budgets, DARPA phase/task budgets).
5. **Resubmitting after reviews**, including structured responses to critiques (especially NIH A1) and targeted strengthening of weak criteria.

## Key Features

- **Agency-aware structure and compliance**
  - NSF: Intellectual Merit + Broader Impacts, typical 15-page Project Description norms
  - NIH: Specific Aims + Significance/Innovation/Approach framing, rigor/reproducibility expectations
  - DOE: office-dependent emphasis (Office of Science, ARPA-E, EERE), partnerships/cost-share where applicable
  - DARPA: high-risk/high-reward framing, measurable milestones, transition pathways, phased execution
  - NSTC (Taiwan): CM03-centered technical narrative, bilingual abstract expectations, feasibility emphasis

- **Review-criteria-driven writing**
  - Maps every major claim to what reviewers score (or discuss) and what program staff prioritize.

- **Budget-to-scope alignment**
  - Ensures personnel effort, equipment, travel, subawards, and indirects match the workplan and schedule.

- **Milestones, timeline, and management planning**
  - Produces Gantt-style schedules, go/no-go criteria, deliverables, and risk mitigation (especially important for DARPA/DOE).

- **Mandatory visual communication workflow**
  - Every proposal should include **at least 1–2 diagrams** (e.g., workflow, conceptual framework, timeline). Use the `scientific-schematics` skill to generate publication-quality figures.

- **Reference-driven drafting**
  - Leverages the repository’s detailed guides as needed:
    - `references/nsf_guidelines.md`
    - `references/nih_guidelines.md`
    - `references/doe_guidelines.md`
    - `references/darpa_guidelines.md`
    - `references/nstc_guidelines.md`
    - `references/specific_aims_guide.md`
    - `references/broader_impacts.md`
    - `references/budget_preparation.md`
    - `references/review_criteria.md`
    - `references/timeline_planning.md`
    - `references/team_building.md`
    - `references/resubmission_strategies.md`

## Dependencies

- **Python**: 3.10+ (recommended)
- **Optional local scripts (repository-provided)**:
  - `scripts/compliance_checker.py` (format checks)
  - `scripts/budget_calculator.py` (budget math support)
  - `scripts/deadline_tracker.py` (planning support)
  - `scripts/generate_schematic.py` (diagram generation wrapper; used with `scientific-schematics`)

> Note: Exact third-party Python package requirements are not specified in the source document. If you maintain this skill repository, add a `requirements.txt` (with pinned versions) and list them here.

## Visual Enhancement with Scientific Schematics

**⚠️ MANDATORY: Every research grant proposal MUST include at least 1-2 AI-generated figures using the scientific-schematics skill.**

This is not optional. Grant proposals without visual elements are incomplete and less competitive. Before finalizing any document:

1. Generate at minimum ONE schematic or diagram (e.g., project timeline, methodology flowchart, or conceptual framework)
2. Prefer 2-3 figures for comprehensive proposals (research workflow, Gantt chart, preliminary data visualization)

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

- Research methodology and workflow diagrams
- Project timeline Gantt charts
- Conceptual framework illustrations
- System architecture diagrams (for technical proposals)
- Experimental design flowcharts
- Broader impacts activity diagrams
- Collaboration network diagrams
- Any complex concept that benefits from visualization

For detailed guidance on creating schematics, refer to the scientific-schematics skill documentation.

## Example Usage

The example below is a complete, runnable workflow that (1) generates required visuals, (2) drafts core sections, and (3) performs basic compliance checks using the included scripts.

### 1) Generate required diagrams (minimum 1–2)

```bash
# Conceptual framework / workflow diagram
python scripts/generate_schematic.py \
  "Conceptual workflow for a 3-aim biomedical project: Aim 1 data collection -> Aim 2 model development -> Aim 3 validation; include feedback loop and key deliverables" \
  -o figures/workflow.png

# Timeline / milestones diagram (recommended)
python scripts/generate_schematic.py \
  "Gantt chart for a 3-year project with quarterly milestones; include go/no-go at end of Year 1 and deliverables per aim" \
  -o figures/timeline.png
```

### 2) Draft an NIH-style proposal skeleton (Specific Aims + Strategy)

Create `proposal.md`:

```markdown
# Project Title
Mechanistic and Translational Study of X to Enable Y

## NIH Specific Aims (1 page target)
**Knowledge gap:** ...
**Long-term goal:** ...
**Objective:** ...
**Central hypothesis:** ...

**Aim 1 (verb-led):** ...
- Rationale:
- Approach (high level):
- Expected outcomes:

**Aim 2:** ...
**Aim 3:** ...

**Impact:** If successful, this work will ...

## Research Strategy (12 pages target for R01)

### Significance
- Problem and barrier to progress:
- Why now / why this team:
- Expected impact on health/biology:

### Innovation
- Conceptual innovation:
- Methodological innovation:
- Why current approaches are insufficient:

### Approach
#### Overview and rationale
#### Aim 1 Methods
- Design:
- Data:
- Analysis:
- Pitfalls and alternatives:
#### Aim 2 Methods
...
#### Aim 3 Methods
...

### Rigor and Reproducibility (as applicable)
- Controls, replicates, blinding/randomization:
- Power/statistics:
- Data management and sharing:
```

### 3) Run a basic formatting/compliance check (if available)

```bash
python scripts/compliance_checker.py proposal.md
```

### 4) Produce a budget justification draft (outline)

Create `budget_justification.md`:

```markdown
# Budget Justification (Draft)

## Personnel
- PI (X% effort): ...
- Postdoc (100%): ...
- Graduate student (50%): ...

## Equipment
- Item: purpose, necessity, and timing

## Travel
- Conference dissemination
- Collaboration meetings

## Materials and Supplies
- Consumables / software licenses

## Other Direct Costs
- Publication fees / participant incentives / consultants

## Subawards (if any)
- Scope and deliverables per partner

## Indirect Costs (F&A)
- Rate and base per institutional policy
```

## Agency-Specific Overview

### NSF (National Science Foundation)
**Mission**: Promote the progress of science and advance national health, prosperity, and welfare

**Key Features**:
- Intellectual Merit + Broader Impacts (equally weighted)
- 15-page project description limit (most programs)
- Emphasis on education, diversity, and societal benefit
- Collaborative research encouraged
- Open data and open science emphasis
- Merit review process with panel + ad hoc reviewers

### NIH (National Institutes of Health)
**Mission**: Enhance health, lengthen life, and reduce illness and disability

**Key Features**:
- Specific Aims (1 page) + Research Strategy (12 pages for R01)
- Significance, Innovation, Approach as core review criteria
- Preliminary data typically required for R01s
- Emphasis on rigor, reproducibility, and clinical relevance
- Modular budgets ($250K increments) for most R01s
- Multiple resubmission opportunities

### DOE (Department of Energy)
**Mission**: Ensure America's security and prosperity through energy, environmental, and nuclear challenges

**Key Features**:
- Focus on energy, climate, computational science, basic energy sciences
- Often requires cost sharing or industry partnerships
- Emphasis on national laboratory collaboration
- Strong computational and experimental integration
- Energy innovation and commercialization pathways
- Varies by office (ARPA-E, Office of Science, EERE, etc.)

### DARPA (Defense Advanced Research Projects Agency)
**Mission**: Make pivotal investments in breakthrough technologies for national security

**Key Features**:
- High-risk, high-reward transformative research
- Focus on "DARPA-hard" problems (what if true, who cares)
- Emphasis on prototypes, demonstrations, and transition paths
- Often requires multiple phases (feasibility, development, demonstration)
- Strong project management and milestone tracking
- Teaming and collaboration often required
- Varies dramatically by program manager and BAA (Broad Agency Announcement)

### NSTC (Taiwan National Science and Technology Council)

**Key Features:**
- CM03 is central; feasibility and preliminary evidence are critical.
- Plan for **bilingual abstracts** and include a clear **research architecture diagram**.

## Implementation Details

### 1) Agency-specific narrative mapping (what to write, where, and why)

- **NSF**
  - Two equal pillars: **Intellectual Merit** and **Broader Impacts**
  - Typical narrative pattern: problem → gap → approach → feasibility → outcomes → impacts
  - Ensure Broader Impacts are **specific, measurable, resourced, and scheduled** (not “bolt-on”).

- **NIH**
  - Core scored criteria: **Significance, Investigator(s), Innovation, Approach, Environment**
  - The **Specific Aims page** is the highest-leverage page: 2–4 aims, independent-but-complementary, each feasible with contingencies.
  - Approach must explicitly address **rigor, reproducibility, and risk mitigation**.

- **DOE**
  - Criteria vary by office; common expectations:
    - technical merit, mission relevance, team capability, facilities, and budget reasonableness
  - Often values **integration of computation + experiment**, partnerships, and (sometimes) cost share.

- **DARPA**
  - Emphasize: **transformative payoff**, measurable milestones, and transition.
  - Use phased plans with **deliverables, metrics, and go/no-go criteria**.
  - Answer DARPA-style questions in substance:
    - *What if it works? Who cares? How will it transition?*

- **NSTC (Taiwan)**
  - CM03 is central; feasibility and preliminary evidence are critical.
  - Plan for **bilingual abstracts** and include a clear **research architecture diagram**.

### 2) Visual requirement (mandatory minimum)

- Include **at least 1–2 diagrams**:
  - Workflow/method schematic (reduces reviewer cognitive load)
  - Timeline/Gantt with milestones and decision points
- Use consistent labeling, readable fonts, and captions that allow the figure to stand alone.

### 3) Milestones and risk control parameters

- Define milestones that are:
  - **Measurable** (metric + threshold)
  - **Time-bound** (quarter/year)
  - **Decision-linked** (go/no-go or pivot criteria)
- For each major risk, include:
  - failure mode → detection signal → mitigation → fallback method

### 4) Budget-to-workplan consistency checks

- Every major task should map to:
  - named personnel effort
  - required equipment/supplies
  - travel (if collaboration/fieldwork is claimed)
  - subaward scope (if partners are essential)
- Common rejection trigger: a narrative that promises outcomes without resourcing them in the budget.

### 5) Resubmission mechanics (especially NIH A1)

- Create a 1-page **Introduction to Resubmission** that:
  - lists major critiques
  - states exactly what changed and where
  - remains factual and respectful
- Strengthen the weakest scored criterion first (often Approach or Innovation), then tighten alignment across aims, methods, and milestones.

## Core Components of Research Proposals

### 1. Executive Summary / Project Summary / Abstract

Every proposal needs a concise overview that communicates the essential elements of the research to both technical reviewers and program officers.

**Purpose**: Provide a standalone summary that captures the research vision, significance, and approach

**Length**:
- NSF: 1 page (Project Summary with separate Overview, Intellectual Merit, Broader Impacts)
- NIH: 30 lines (Project Summary/Abstract)
- DOE: Varies (typically 1 page)
- DARPA: Varies (often 1-2 pages)
- NSTC: Varies

**Essential Elements**:
- Clear statement of the problem or research question
- Why this problem matters (significance, urgency, impact)
- Novel approach or innovation
- Expected outcomes and deliverables
- Qualifications of the team
- Broader impacts or translational pathway

**Writing Strategy**:
- Open with a compelling hook that establishes importance
- Use accessible language (avoid jargon in opening sentences)
- State specific, measurable objectives
- Convey enthusiasm and confidence
- Ensure every sentence adds value (no filler)
- End with transformative vision or impact statement

**Common Mistakes to Avoid**:
- Being too technical or detailed (save for project description)
- Failing to articulate "why now" or "why this team"
- Vague objectives or outcomes
- Neglecting broader impacts or significance
- Generic statements that could apply to any proposal

### 2. Project Description / Research Strategy

The core technical narrative that presents the research plan in detail.

**Structure Varies by Agency:**

**NSF Project Description** (typically 15 pages):
- Introduction and background
- Research objectives and questions
- Preliminary results (if applicable)
- Research plan and methodology
- Timeline and milestones
- Broader impacts (integrated throughout or separate section)
- Prior NSF support (if applicable)

**NIH Research Strategy** (12 pages for R01):
- Significance (why the problem matters)
- Innovation (what's novel and transformative)
- Approach (detailed research plan)
  - Preliminary data
  - Research design and methods
  - Expected outcomes
  - Potential problems and alternative approaches

**DOE Project Narrative** (varies):
- Background and significance
- Technical approach and innovation
- Qualifications and experience
- Facilities and resources
- Project management and timeline

**DARPA Technical Volume** (varies):
- Technical challenge and innovation
- Approach and methodology
- Schedule and milestones
- Deliverables and metrics
- Team qualifications
- Risk assessment and mitigation

**NSTC CM03:**
- Follow NSTC guidelines

For detailed agency-specific guidance, refer to:
- `references/nsf_guidelines.md`
- `references/nih_guidelines.md`
- `references/doe_guidelines.md`
- `references/darpa_guidelines.md`
- `references/nstc_guidelines.md`

### 3. Specific Aims (NIH) or Objectives (NSF/DOE/DARPA/NSTC)

Clear, testable goals that structure the research plan.

**NIH Specific Aims Page** (1 page):
- Opening paragraph: Gap in knowledge and significance
- Long-term goal and immediate objectives
- Central hypothesis or research question
- 2-4 specific aims with sub-aims
- Expected outcomes and impact
- Payoff paragraph: Why this matters

**Structure for Each Aim:**
- Aim statement (1-2 sentences, starts with action verb)
- Rationale (why this aim, preliminary data support)
- Working hypothesis (testable prediction)
- Approach summary (brief methods overview)
- Expected outcomes and interpretation

**Writing Strategy**:
- Make aims independent but complementary
- Ensure each aim is achievable within timeline and budget
- Provide enough detail to judge feasibility
- Include contingency plans or alternative approaches
- Use parallel structure across aims
- Clearly state what will be learned from each aim

For detailed guidance, refer to `references/specific_aims_guide.md`.

### 4. Broader Impacts (NSF) / Significance (NIH)

Articulate the societal, educational, or translational value of the research.

**NSF Broader Impacts** (critical component, equal weight with Intellectual Merit):

NSF explicitly evaluates broader impacts. Address at least one of these areas:
1. **Advancing discovery and understanding while promoting teaching, training, and learning**
   - Integration of research and education
   - Training of students and postdocs
   - Curriculum development
   - Educational materials and resources

2. **Broadening participation of underrepresented groups**
   - Recruitment and retention strategies
   - Partnerships with minority-serving institutions
   - Outreach to underrepresented communities
   - Mentoring programs

3. **Enhancing infrastructure for research and education**
   - Shared facilities or instrumentation
   - Cyberinfrastructure and data resources
   - Community-wide tools or databases
   - Open-source software or methods

4. **Broad dissemination to enhance scientific and technological understanding**
   - Public outreach and science communication
   - K-12 educational programs
   - Museum exhibits or media engagement
   - Policy briefs or stakeholder engagement

5. **Benefits to society**
   - Economic impact or commercialization
   - Health, environment, or national security benefits
   - Informed decision-making
   - Workforce development

**Writing Strategy for NSF Broader Impacts**:
- Be specific with concrete activities, not vague statements
- Provide timeline and milestones for broader impacts activities
- Explain how impacts will be measured and assessed
- Connect to institutional resources and existing programs
- Show commitment through preliminary efforts or partnerships
- Integrate with research plan (not tacked on)

**NIH Significance**:
- Addresses important problem or critical barrier to progress
- Improves scientific knowledge, technical capability, or clinical practice
- Potential to lead to better outcomes, interventions, or understanding
- Rigor of prior research in the field
- Alignment with NIH mission and institute priorities

For detailed guidance, refer to `references/broader_impacts.md`.

### 5. Innovation and Transformative Potential

Articulate what is novel, creative, and paradigm-shifting about the research.

**Innovation Elements to Highlight**:
- **Conceptual Innovation**: New frameworks, models, or theories
- **Methodological Innovation**: Novel techniques, approaches, or technologies
- **Integrative Innovation**: Combining disciplines or approaches in new ways
- **Translational Innovation**: New pathways from discovery to application
- **Scale Innovation**: Unprecedented scope or resolution

**Writing Strategy**:
- Clearly state what is innovative (don't assume it's obvious)
- Explain why current approaches are insufficient
- Describe how your innovation overcomes limitations
- Provide evidence that innovation is feasible (preliminary data, proof-of-concept)
- Distinguish incremental from transformative advances
- Balance innovation with feasibility (not too risky)

**Common Mistakes**:
- Claiming novelty without demonstrating knowledge of prior work
- Confusing "new to me" with "new to the field"
- Over-promising without supporting evidence
- Being too incremental (minor variation on existing work)
- Being too speculative (no path to success)

### 6. Research Approach and Methods

Detailed description of how the research will be conducted.

**Essential Components**:
- Overall research design and framework
- Detailed methods for each aim/objective
- Sample sizes, statistical power, and analysis plans
- Timeline and sequence of activities
- Data collection, management, and analysis
- Quality control and validation approaches
- Potential problems and alternative strategies
- Rigor and reproducibility measures

**Writing Strategy**:
- Provide enough detail for reproducibility and feasibility assessment
- Use subheadings and figures to improve organization
- Justify choice of methods and approaches
- Address potential limitations proactively
- Include preliminary data demonstrating feasibility
- Show that you've thought through the research process
- Balance detail with readability (use supplementary materials for extensive details)

**For Experimental Research**:
- Describe experimental design (controls, replicates, blinding)
- Specify materials, reagents, and equipment
- Detail data collection protocols
- Explain statistical analysis plans
- Address rigor and reproducibility

**For Computational Research**:
- Describe algorithms, models, and software
- Specify datasets and validation approaches
- Explain computational resources required
- Address code availability and documentation
- Describe benchmarking and performance metrics

**For Clinical or Translational Research**:
- Describe study population and recruitment
- Detail intervention or treatment protocols
- Explain outcome measures and assessments
- Address regulatory approvals (IRB, IND, IDE)
- Describe clinical trial design and monitoring

For detailed methodology guidance by discipline, refer to `references/research_methods.md`.

### 7. Preliminary Data and Feasibility

Demonstrate that the research is achievable and the team is capable.

**Purpose**:
- Prove that the proposed approach can work
- Show that the team has necessary expertise
- Demonstrate access to required resources
- Reduce perceived risk for reviewers
- Provide foundation for proposed work

**What to Include**:
- Pilot studies or proof-of-concept results
- Method development or optimization
- Access to unique resources (samples, data, collaborators)
- Relevant publications from your team
- Preliminary models or simulations
- Feasibility assessments or power calculations

**NIH Requirements**:
- R01 applications typically require substantial preliminary data
- R21 applications may have less stringent requirements
- New investigators may have less preliminary data
- Preliminary data should directly support proposed aims

**NSF Approach**:
- Preliminary data less commonly required than NIH
- May be important for high-risk or novel approaches
- Can strengthen proposal for competitive programs

**Writing Strategy**:
- Present most compelling data that supports your approach
- Clearly connect preliminary data to proposed aims
- Acknowledge limitations and how proposed work will address them
- Use figures and data visualizations effectively
- Avoid over-interpreting or overstating preliminary findings
- Show trajectory of your research program

### 8. Timeline, Milestones, and Management Plan

Demonstrate that the project is well-planned and achievable within the proposed timeframe.

**Essential Elements**:
- Phased timeline with clear milestones
- Logical sequence and dependencies
- Realistic timeframes for each activity
- Decision points and go/no-go criteria
- Risk mitigation strategies
- Resource allocation across time
- Coordination plan for multi-institutional teams

**Presentation Formats**:
- Gantt charts showing overlapping activities
- Year-by-year breakdown of activities
- Quarterly milestones and deliverables
- Table of aims/tasks with timeline and personnel

**Writing Strategy**:
- Be realistic about what can be accomplished
- Build in time for unexpected delays or setbacks
- Show that timeline aligns with budget and personnel
- Demonstrate understanding of regulatory timelines (IRB, IACUC)
- Include time for dissemination and broader impacts
- Address how progress will be monitored and assessed

**DARPA Emphasis**:
- Particularly important for DARPA proposals
- Clear technical milestones with measurable metrics
- Quarterly deliverables and reporting
- Phase-based structure with exit criteria
- Demonstration and transition planning

For detailed guidance, refer to `references/timeline_planning.md`.

### 9. Team Qualifications and Collaboration

Demonstrate that the team has the expertise, experience, and resources to succeed.

**Essential Elements**:
- PI qualifications and relevant expertise
- Co-I and collaborator roles and contributions
- Track record in the research area
- Complementary expertise across team
- Institutional support and resources
- Prior collaboration history (if applicable)
- Mentoring and training plan (for students/postdocs)

**Writing Strategy**:
- Highlight most relevant publications and accomplishments
- Clearly define roles and responsibilities
- Show that team composition is necessary (not just convenient)
- Demonstrate successful prior collaborations
- Address how team will be managed and coordinated
- Explain institutional commitment and support

**Biosketches / CVs**:
- Follow agency-specific formats (NSF, NIH, DOE, DARPA differ)
- Highlight most relevant publications and accomplishments
- Include synergistic activities and collaborations
- Show trajectory and productivity
- Address any career gaps or interruptions

**Letters of Collaboration**:
- Specific commitments and contributions
- Demonstrates genuine partnership
- Includes resource sharing or access agreements
- Signed and on letterhead

For detailed guidance, refer to `references/team_building.md`.

### 10. Budget and Budget Justification

Develop realistic budgets that align with the proposed work and agency guidelines.

**Budget Categories** (typical):
- **Personnel**: Salary and fringe for PI, co-Is, postdocs, students, staff
- **Equipment**: Items >$5,000 (varies by agency)
- **Travel**: Conferences, collaborations, fieldwork
- **Materials and Supplies**: Consumables, reagents, software
- **Other Direct Costs**: Publication costs, participant incentives, consulting
- **Indirect Costs (F&A)**: Institutional overhead (rates vary)
- **Subawards**: Costs for collaborating institutions

**Agency-Specific Considerations**:

**NSF**:
- Full budget justification required
- Cost sharing generally not required (but may strengthen proposal)
- Up to 2 months summer salary for faculty
- Graduate student support encouraged

**NIH**:
- Modular budgets for ≤$250K direct costs per year (R01)
- Detailed budgets for >$250K or complex awards
- Salary cap applies (~$221,900 for 2024)
- Limited to 1 month (8.33% FTE) for most PIs

**DOE**:
- Often requires cost sharing (especially ARPA-E)
- Detailed budget with quarterly breakdown
- Requires institutional commitment letters
- National laboratory collaboration budgets separate

**DARPA**:
- Detailed budgets by phase and task
- Requires supporting cost data for large procurements
- Often requires cost-plus or firm-fixed-price structures
- Travel budget for program meetings

**Budget Justification Writing**:
- Justify each line item in terms of the research plan
- Explain effort percentages for personnel
- Describe specific equipment and why necessary
- Justify travel (conferences, collaborations)
- Explain consultant roles and rates
- Show how budget aligns with timeline

For detailed budget guidance, refer to `references/budget_preparation.md`.

## Review Criteria by Agency

Understanding how proposals are evaluated is critical for writing competitive applications.

### NSF Review Criteria

**Intellectual Merit** (primary):
- What is the potential for the proposed activity to advance knowledge?
- How well-conceived and organized is the proposed activity?
- Is there sufficient access to resources?
- How well-qualified is the individual, team, or institution to conduct proposed activities?

**Broader Impacts** (equally important):
- What is the potential for the proposed activity to benefit society?
- To what extent does the proposal address broader impacts in meaningful ways?

**Additional Considerations**:
- Integration of research and education
- Diversity and inclusion
- Results from prior NSF support (if applicable)

### NIH Review Criteria

**Scored Criteria** (1-9 scale, 1 = exceptional, 9 = poor):

1. **Significance**
   - Addresses important problem or critical barrier
   - Improves scientific knowledge, technical capability, or clinical practice
   - Aligns with NIH mission

2. **Investigator(s)**
   - Well-suited to the project
   - Track record of accomplishments
   - Adequate training and expertise

3. **Innovation**
   - Novel concepts, approaches, methodologies, or interventions
   - Challenges existing paradigms
   - Addresses important problem in creative ways

4. **Approach**
   - Well-reasoned and appropriate
   - Rigorous and reproducible
   - Adequately accounts for potential problems
   - Feasible within timeline

5. **Environment**
   - Institutional support and resources
   - Scientific environment contributes to probability of success

**Additional Review Considerations** (not scored but discussed):
- Protections for human subjects
- Inclusion of women, minorities, and children
- Vertebrate animal welfare
- Biohazards
- Resubmission response (if applicable)
- Budget and timeline appropriateness

### DOE Review Criteria

Varies by program office, but generally includes:
- Scientific and/or technical merit
- Appropriateness of proposed method or approach
- Competency of personnel and adequacy of facilities
- Reasonableness and appropriateness of budget
- Relevance to DOE mission and program goals

### DARPA Review Criteria

**DARPA-specific considerations**:
- Overall scientific and technical merit
- Potential contribution to DARPA mission
- Relevance to stated program goals
- Plans and capability to accomplish technology transition
- Qualifications and experience of proposed team
- Realism of proposed costs and availability of funds

**Key Questions DARPA Asks**:
- **What if you succeed?** (Impact if the research works)
- **What if you're right?** (Implications of your hypothesis)
- **Who cares?** (Why it matters for national security)

### NSTC Review Criteria
- CM03 alignment
- Feasibility
- Preliminary Data

For detailed review criteria by agency, refer to `references/review_criteria.md`.

## Writing Principles for Competitive Proposals

### Clarity and Accessibility

**Write for Multiple Audiences**:
- Technical reviewers in your field (will scrutinize methods)
- Reviewers in related but not identical fields (need context)
- Program officers (look for alignment with agency goals)
- Panel members reading 15+ proposals (need clear organization)

**Strategies**:
- Use clear section headings and subheadings
- Start sections with overview paragraphs
- Define technical terms and abbreviations
- Use figures, diagrams, and tables to clarify complex ideas
- Avoid jargon when possible; explain when necessary
- Use topic sentences to guide readers

### Persuasive Argumentation

**Build a Compelling Narrative**:
- Establish the problem and its importance
- Show gaps in current knowledge or approaches
- Present your solution as innovative and feasible
- Demonstrate that you're the right team
- Show that success will have significant impact

**Structure of Persuasion**:
1. **Hook**: Capture attention with significance
2. **Problem**: Establish what's not known or not working
3. **Solution**: Present your innovative approach
4. **Evidence**: Support with preliminary data
5. **Impact**: Show transformative potential
6. **Team**: Demonstrate capability to deliver

**Language Choices**:
- Use active voice for clarity and confidence
- Choose strong verbs (investigate, elucidate, discover vs. look at, study)
- Be confident but not arrogant (avoid "obviously," "clearly")
- Acknowledge uncertainty appropriately
- Use precise language (avoid vague terms like "several," "various")

### Visual Communication

**Effective Use of Figures**:
- Conceptual diagrams showing research framework
- Preliminary data demonstrating feasibility
- Timelines and Gantt charts
- Workflow diagrams showing methodology
- Expected results or predictions

**Design Principles**:
- Make figures self-explanatory with complete captions
- Use consistent color schemes and fonts
- Ensure readability (large enough fonts, clear labels)
- Integrate figures with text (refer to specific figures)
- Follow agency-specific formatting requirements

### Addressing Risk and Feasibility

**Balance Innovation and Risk**:
- Acknowledge potential challenges
- Provide alternative approaches
- Show preliminary data reducing risk
- Demonstrate expertise to handle challenges
- Include contingency plans

**Common Concerns**:
- Too ambitious for timeline/budget
- Technically infeasible
- Team lacks necessary expertise
- Preliminary data insufficient
- Methods not adequately described
- Lack of innovation or significance

### Integration and Coherence

**Ensure All Parts Align**:
- Budget supports activities in project description
- Timeline matches aims and milestones
- Team composition matches required expertise
- Broader impacts connect to research plan
- Letters of support confirm stated collaborations

**Avoid Contradictions**:
- Preliminary data vs. stated gaps
- Claimed expertise vs. publication record
- Stated aims vs. actual methods
- Budget vs. stated activities

## Common Proposal Types

### NSF Proposal Types

- **Standard Research Proposals**: Most common, up to $500K and 5 years
- **CAREER Awards**: Early career faculty, integrated research/education, $400-500K over 5 years
- **Collaborative Research**: Multiple institutions, separately submitted, shared research plan
- **RAPID**: Urgent research opportunities, up to $200K, no preliminary data required
- **EAGER**: High-risk, high-reward exploratory research, up to $300K

### NIH Award Mechanisms

- **R01**: Research Project Grant, $250K+ per year, 3-5 years, most common
- **R21**: Exploratory/Developmental Research, up to $275K over 2 years, no preliminary data
- **R03**: Small Grant Program, up to $100K over 2 years
- **R15**: Academic Research Enhancement Awards (AREA), for primarily undergraduate institutions
- **R35**: MIRA (Maximizing Investigators' Research Award), program-specific

**Fellowship Mechanisms**:
- **F30**: Predoctoral MD/PhD Fellowship
- **F31**: Predoctoral Fellowship
- **F32**: Postdoctoral Fellowship
- **K99/R00**: Pathway to Independence Award
- **K08**: Mentored Clinical Scientist Research Career Development Award

### DOE Programs

- **Office of Science**: Basic research in physical sciences, biological sciences, computing
- **ARPA-E**: Transformative energy technologies, requires cost sharing
- **EERE**: Applied research in renewable energy and energy efficiency
- **National Laboratories**: Collaborative research with DOE labs

### DARPA Programs

- **Varies by Office**: BTO, DSO, I2O, MTO, STO, TTO
- **Program-Specific BAAs**: Broad Agency Announcements for specific thrusts
- **Young Faculty Award (YFA)**: Early career researchers, up to $500K
- **Director's Fellowship**: High-risk, paradigm-shifting research

### NSTC Programs
- Varies based on the solicitation/FOA

For detailed program guidance, refer to `references/funding_mechanisms.md`.

## Resubmission Strategies

### NIH Resubmission (A1)

**Introduction to Resubmission** (1 page):
- Summarize major criticisms from previous review
- Describe specific changes made in response
- Use bullet points for clarity
- Be respectful of reviewers' comments
- Highlight substantial improvements

**Strategies**:
- Address every major criticism
- Make changes visible (but don't use track changes in final)
- Strengthen weak areas (preliminary data, methods, significance)
- Consider changing aims if fundamentally flawed
- Get external feedback before resubmitting
- Use full 37-month window if needed for new data

**When Not to Resubmit**:
- Fundamental conceptual flaws
- Lack of innovation or significance
- Missing key expertise or resources
- Extensive revisions needed (consider new submission)

### NSF Resubmission

**NSF allows resubmission after revision**:
- Address reviewer concerns in revised proposal
- No formal "introduction to resubmission" section
- May be reviewed by same or different panel
- Consider program officer feedback
- May need to wait for next submission cycle

For detailed resubmission guidance, refer to `references/resubmission_strategies.md`.

## Common Mistakes to Avoid

### Conceptual Mistakes

1. **Failing to Address Review Criteria