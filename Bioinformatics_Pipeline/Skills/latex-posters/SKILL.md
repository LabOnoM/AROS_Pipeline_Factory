---
name: latex-posters
description: "Create professional research posters in LaTeX using beamerposter, tikzposter, or baposter. Generate poster-ready section copy, figure plans, captions, and package-specific layout decisions for conference or thesis posters."
allowed-tools: [Read, Write, Edit, Bash]
license: MIT
skill-author: AIPOCH
---

# LaTeX Academic Posters

This is an **Academic Writing** skill for turning research content into a poster-ready LaTeX brief. The core deliverable is a writing package that can be assembled directly in `beamerposter`, `tikzposter`, or `baposter`. It provides layout advice, section copy, figure plans, and captions.

## When to Use

- Creating research posters for conferences, symposia, or poster sessions.
- Designing academic posters for university events or thesis defenses.
- Preparing visual summaries of research for public engagement.
- Converting scientific papers, abstracts, or slide decks into a readable poster narrative.
- Help choosing between `beamerposter`, `tikzposter`, and `baposter`.
- Compressing a paper, abstract, or slide deck into a readable poster narrative.

## When Not to Use

- A PowerPoint-native workflow is desired with no LaTeX output at all.
- Full manuscript detail is to be crammed onto one poster.
- Requests for fake results, invented metrics, or nonexistent figures.

## Core Deliverables

This skill should produce one or more of these outputs:

- **Poster Brief:** poster size, audience, package choice, and section map.
- **Poster Copy Plan:** title, introduction, methods, results, conclusion, and acknowledgments text limits.
- **Figure Plan:** one-message-per-figure architecture, captions, and panel priorities.
- **LaTeX Assembly Guidance:** package-specific layout choices using bundled assets in `assets/`.
- **Concise Poster-Ready Wording (optional):** title, problem statement, methods block, results bullets (2-4), conclusion block, QR/data/contact block.

## Package Decision Matrix

- Use `tikzposter` when the user wants modern flexible block design and portrait conference style.
- Use `beamerposter` when the user wants a classic academic appearance or already knows Beamer.
- Use `baposter` when the user needs a box-based multi-column layout and explicit panel control.

If the user does not specify a package:

- Default to `tikzposter` for most modern research posters.
- Switch to `beamerposter` for formal thesis-defense aesthetics.
- Switch to `baposter` when the content is block-heavy and highly modular.

## Writing Output Contract

Always provide:

1. Recommended package.
2. Poster size / orientation.
3. Section list in display order.
4. Section-level word budget.
5. Figure plan with one message per figure.
6. Caption guidance.
7. Final quality-control checklist.

If the user asks for direct copy, provide concise poster-ready wording for:

- Title.
- One-sentence problem statement.
- Methods block.
- `2-4` results bullets.
- Conclusion block.
- Optional QR / data / contact block.

## Hard Constraints

- A0 poster: usually `300-800` words total.
- No more than `5-6` major content blocks on one poster.
- One figure = one message.
- Avoid dense paragraphs.
- Body text must remain poster-readable.

If the request violates these constraints, refuse the density request and propose a reduced architecture.

## AI-Powered Visual Element Generation (Recommended)

**STANDARD WORKFLOW: Generate ALL major visual elements using AI before creating the LaTeX poster.**

This is the recommended approach for creating visually compelling posters:
1. Plan all visual elements needed (title, intro, methods, results, conclusions).
2. Generate each element using scientific-schematics or Nano Banana Pro.
3. Assemble generated images in the LaTeX template.
4. Add text content around the visuals.

**Target: 60-70% of poster area should be AI-generated visuals, 30-40% text.**

---

### CRITICAL: Poster-Size Font Requirements

**⚠️ ALL text within AI-generated visualizations MUST be poster-readable.**

When generating graphics for posters, you MUST include font size specifications in EVERY prompt. Poster graphics are viewed from 4-6 feet away, so text must be LARGE.

**⚠️ COMMON PROBLEM: Content Overflow and Density**

The #1 issue with AI-generated poster graphics is **TOO MUCH CONTENT**. This causes:
- Text overflow beyond boundaries.
- Unreadable small fonts.
- Cluttered, overwhelming visuals.
- Poor white space usage.

**SOLUTION: Generate SIMPLE graphics with MINIMAL content.**

**Required prompt additions for poster graphics:**

```
POSTER FORMAT REQUIREMENTS:
- MAXIMUM 3-5 elements per graphic (NOT 10+).
- MAXIMUM 10-15 words total per graphic.
- ALL text must be VERY LARGE and bold (readable from 6 feet away).
- Title text: minimum 72pt equivalent, bold.
- Key metrics/numbers: minimum 60pt equivalent, bold.
- Labels and captions: minimum 36pt equivalent.
- Use high contrast (dark text on light background or vice versa).
- GENEROUS white space (40-50% of graphic should be empty).
- Large icons and graphics with thick lines.
- ONE main message per graphic.
```

**Content limits per graphic type:**
| Graphic Type | Max Elements | Max Words | Example |
|--------------|--------------|-----------|---------|
| Flowchart | 4-5 boxes | 15 words | "DATA → PROCESS → MODEL → OUTPUT" |
| Key findings | 3 items | 12 words | "95% Accuracy, 2X Faster, Clinical Ready" |
| Comparison chart | 3-4 bars | 10 words | "Method A: 70%, Method B: 85%, Ours: 95%" |
| Diagram | 3-5 components | 15 words | Simple architecture with labeled parts |

**Font size reference for poster prompts:**
| Element | Minimum Size | Prompt Keywords |
|---------|--------------|-----------------|
| Main numbers/metrics | 72pt+ | "huge", "very large", "giant", "poster-size" |
| Section titles | 60pt+ | "large bold", "prominent" |
| Labels/captions | 36pt+ | "readable from 6 feet", "clear labels" |
| Body text | 24pt+ | "poster-readable", "large text" |

**Always include in prompts:**
- "POSTER FORMAT" or "for A0 poster" or "readable from 6 feet".
- "VERY LARGE TEXT" or "huge bold fonts".
- Specific text that should appear (so it's baked into the image).
- "minimal text, maximum impact".
- "high contrast" for readability.

---

### Visual Element Guidelines

**⚠️ CRITICAL: Each graphic should have ONE main message and MINIMAL content.**

**Content limits - NEVER exceed these:**
- **Maximum 5 boxes/elements** per flowchart.
- **Maximum 3-4 bars** per chart.
- **Maximum 3 key findings** per infographic.
- **Maximum 15 words** total per graphic.
- **50% white space** minimum.

**For each poster section, generate SIMPLE visuals with POSTER FORMAT:**

| Section | Max Elements | Example Prompt |
|---------|--------------|----------------|
| **Introduction** | 3-4 icons | "POSTER FORMAT for A0: SIMPLE problem visual with 3 large icons and 3 word labels. 50% white space." |
| **Methods** | 4-5 boxes max | "POSTER FORMAT for A0: SIMPLE flowchart with ONLY 4 steps: A → B → C → D. GIANT labels (80pt+). 50% white space." |
| **Results** | 3-4 bars max | "POSTER FORMAT for A0: SIMPLE bar chart with ONLY 3 bars. GIANT percentages (100pt+). NO legend, direct labels." |
| **Conclusions** | 3 items only | "POSTER FORMAT for A0: ONLY 3 key findings. GIANT numbers (120pt+). One word labels. 50% white space." |

**MANDATORY prompt elements for poster graphics:**
1. **"POSTER FORMAT for A0"** - size indicator.
2. **"SIMPLE"** or **"ONLY X elements"** - content limit.
3. **"GIANT (80pt+)"** or **"HUGE (100pt+)"** - font sizes.
4. **"50% white space"** - prevent crowding.
5. **"readable from 6-8 feet"** - viewing distance.
6. **Exact text** that should appear (keep minimal!).

**ANTI-PATTERNS TO AVOID:**
- ❌ "Show all the steps in the methodology" → Too many elements
- ❌ "Include accuracy, precision, recall, F1, AUC" → Too many metrics
- ❌ "Comparison of 6 different methods" → Too many comparisons
- ❌ "Detailed architecture with all layers" → Too complex

**CORRECT PATTERNS:**
- ✅ "ONLY 4 main steps" → Limited elements
- ✅ "ONLY the top 3 metrics" → Focused content
- ✅ "Compare ONLY our method vs baseline" → Simple comparison
- ✅ "HIGH-LEVEL architecture with 4 components" → Simplified view

## Workflow

### 1. Collect poster context

Confirm:

- Poster size and orientation.
- Audience.
- Source material type (paper, abstract, slides).
- Required figures or logos.
- Whether the user needs only a brief, or also section copy.

### 2. Choose the package

Use `## Package Decision Matrix`.

### 3. Compress the narrative

Convert the source into:

- One central message.
- One methods summary.
- `2-3` strongest results.
- One clear conclusion.

Do not preserve every subsection from the manuscript.

### 4. Plan the figures

For each figure:

- Define one message only.
- Keep labels minimal.
- Assign where it belongs in the poster flow.
- Define whether it needs a caption or only a headline.

### 5. Assemble the writing package

Return:

- Poster brief.
- Section order.
- Section copy limits.
- Figure plan.
- LaTeX asset recommendation from `assets/`.

### Example: Complete Poster Generation Workflow

**Remember: SIMPLE graphics with MINIMAL content. Each graphic = ONE message.**

```bash
# 1. Create figures directory
mkdir -p figures

# 2. Generate SIMPLE visual elements - MAXIMUM 5 elements per graphic

# Problem statement - ONLY 3 icons
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE visual with 3 icons only: PATIENT icon → DELAY icon → RISK icon. ONE word label each (80pt+). 50% white space. Readable from 8 feet." -o figures/problem.png

# Methods pipeline - ONLY 4 steps
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE flowchart with ONLY 4 boxes: IMAGES → PROCESS → MODEL → DIAGNOSIS. GIANT labels (100pt+). 50% white space. NO sub-steps. Readable from 8 feet." -o figures/methods.png

# Architecture diagram - ONLY 4 components
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE architecture with ONLY 4 blocks: INPUT → CNN → DENSE → OUTPUT. GIANT labels (80pt+). Thick lines. 50% white space. NO layer details. Readable from 8 feet." -o figures/architecture.png

# Results - ONLY 3 bars
python scripts/generate_schematic.py "POSTER FORMAT for A0. SIMPLE bar chart with ONLY 3 bars: 82% BASELINE, 88% EXISTING, 95% OURS (highlighted). GIANT percentages ON bars (120pt+). NO axis, NO legend. 40% white space. Readable from 10 feet." -o figures/results.png

# Key findings - ONLY 3 items with GIANT numbers
python scripts/generate_schematic.py "POSTER FORMAT for A0. EXACTLY 3 cards only: '95%' (150pt) 'ACCURACY' (60pt), '2X' (150pt) 'FASTER' (60pt), checkmark 'VALIDATED' (60pt). 50% white space. NO other text. Readable from 10 feet." -o figures/conclusions.png

# 3. Compile LaTeX poster with all figures
pdflatex poster.tex
```

**If graphics still overflow or have small text:**
1. Reduce number of elements further (try 3 instead of 5).
2. Add "EVEN SIMPLER" or "ONLY 3 elements" to prompt.
3. Increase font size requirements (try 150pt+ for key numbers).
4. Add "60% white space" instead of 50%.

## Refusal and Recovery Contract

If the user asks for an unreadable or off-scope poster, respond with:

```text
Cannot produce a readable poster plan as requested.
Reason: <too much content / unsupported non-LaTeX workflow / missing source information>
Suggested recovery:
- <step 1>
- <step 2>
```

Use this when:

- The user wants tiny-font dense content.
- The user wants a non-LaTeX-native deliverable.
- The source is too incomplete to plan poster copy.

## Asset Usage

Bundled assets:

- `assets/beamerposter_template.tex`
- `assets/tikzposter_template.tex`
- `assets/baposter_template.tex`
- `assets/poster_quality_checklist.md`

Use these assets as the implementation anchor. Do **not** reference nonexistent local scripts.

## Academic Writing Rules

- Keep the tone neutral and conference-appropriate.
- Prefer short declarative statements over abstract-like paragraphs.
- Results language must stay grounded in source evidence.
- Captions should interpret the figure's role, not repeat every numeric detail.

## Final Quality Checklist

Before returning:

- Package choice is explicit.
- Section order is clear.
- Word budget is realistic.
- Figure plan is readable.
- No fake script requirement appears.
- No impossible density request is accepted.

## Scientific Schematics Integration

For detailed guidance on creating schematics, refer to the **scientific-schematics** skill documentation.

**Key capabilities:**
- Nano Banana Pro automatically generates, reviews, and refines diagrams.
- Creates publication-quality images with proper formatting.
- Ensures accessibility (colorblind-friendly, high contrast).
- Supports iterative refinement for complex diagrams.

## Core Capabilities

### 1. LaTeX Poster Packages

Support for three major LaTeX poster packages, each with distinct advantages. For detailed comparison and package-specific guidance, refer to `references/latex_poster_packages.md`.

**beamerposter**:
- Extension of the Beamer presentation class.
- Familiar syntax for Beamer users.
- Excellent theme support and customization.
- Best for: Traditional academic posters, institutional branding.

**tikzposter**:
- Modern, flexible design with TikZ integration.
- Built-in color themes and layout templates.
- Extensive customization through TikZ commands.
- Best for: Colorful, modern designs, custom graphics.

**baposter**:
- Box-based layout system.
- Automatic spacing and positioning.
- Professional-looking default styles.
- Best for: Multi-column layouts, consistent spacing.

### 2. Poster Layout and Structure

Create effective poster layouts following visual communication principles. For comprehensive layout guidance, refer to `references/poster_layout_design.md`.

**Common Poster Sections**:
- **Header/Title**: Title, authors, affiliations, logos.
- **Introduction/Background**: Research context and motivation.
- **Methods/Approach**: Methodology and experimental design.
- **Results**: Key findings with figures and data visualizations.
- **Conclusions**: Main takeaways and implications.
- **References**: Key citations (typically abbreviated).
- **Acknowledgments**: Funding, collaborators, institutions.

**Layout Strategies**:
- **Column-based layouts**: 2-column, 3-column, or 4-column grids.
- **Block-based layouts**: Flexible arrangement of content blocks.
- **Z-pattern flow**: Guide readers through content logically.
- **Visual hierarchy**: Use size, color, and spacing to emphasize key points.

### 3. Design Principles for Research Posters

Apply evidence-based design principles for maximum impact. For detailed design guidance, refer to `references/poster_design_principles.md`.

**Typography**:
- Title: 72-120pt for visibility from distance.
- Section headers: 48-72pt.
- Body text: 24-36pt minimum for readability from 4-6 feet.
- Use sans-serif fonts (Arial, Helvetica, Calibri) for clarity.
- Limit to 2-3 font families maximum.

**Color and Contrast**:
- Use high-contrast color schemes for readability.
- Institutional color palettes for branding.
- Color-blind friendly palettes (avoid red-green combinations).
- White space is active space—don't overcrowd.

**Visual Elements**:
- High-resolution figures (300 DPI minimum for print).
- Large, clear labels on all figures.
- Consistent figure styling throughout.
- Strategic use of icons and graphics.
- Balance text with visual content (40-50% visual recommended).

**Content Guidelines**:
- **Less is more**: 300-800 words total recommended.
- Bullet points over paragraphs for scannability.
- Clear, concise messaging.
- Self-explanatory figures with minimal text explanation.
- QR codes for supplementary materials or online resources.

### 4. Standard Poster Sizes

Support for international and conference-specific poster dimensions:

**International Standards**:
- A0 (841 × 1189 mm / 33.1 × 46.8 inches) - Most common European standard.
- A1 (594 × 841 mm / 23.4 × 33.1 inches) - Smaller format.
- A2 (420 × 594 mm / 16.5 × 23.4 inches) - Compact posters.

**North American Standards**:
- 36 × 48 inches (914 × 1219 mm) - Common US conference size.
- 42 × 56 inches (1067 × 1422 mm) - Large format.
- 48 × 72 inches (1219 × 1829 mm) - Extra large.

**Orientation**:
- Portrait (vertical) - Most common, traditional.
- Landscape (horizontal) - Better for wide content, timelines.

### 5. Package-Specific Templates

Provide ready-to-use templates for each major package. Templates available in `assets/` directory.

**beamerposter Templates**:
- `beamerposter_classic.tex` - Traditional academic style.
- `beamerposter_modern.tex` - Clean, minimal design.
- `beamerposter_colorful.tex` - Vibrant theme with blocks.

**tikzposter Templates**:
- `tikzposter_default.tex` - Standard tikzposter layout.
- `tikzposter_rays.tex` - Modern design with ray theme.
- `tikzposter_wave.tex` - Professional wave-style theme.

**baposter Templates**:
- `baposter_portrait.tex` - Classic portrait layout.
- `baposter_landscape.tex` - Landscape multi-column.
- `baposter_minimal.tex` - Minimalist design.

### 6. Figure and Image Integration

Optimize visual content for poster presentations:

**Best Practices**:
- Use vector graphics (PDF, SVG) when possible for scalability.
- Raster images: minimum 300 DPI at final print size.
- Consistent image styling (borders, captions, sizes).
- Group related figures together.
- Use subfigures for comparisons.

### 7. Color Schemes and Themes

Provide professional color palettes for various contexts:

**Academic Institution Colors**:
- Match university or department branding.
- Use official color codes (RGB, CMYK, or LaTeX color definitions).

**Scientific Color Palettes** (color-blind friendly):
- Viridis: Professional gradient from purple to yellow.
- ColorBrewer: Research-tested palettes for data visualization.
- IBM Color Blind Safe: Accessible corporate palette.

### 8. Typography and Text Formatting

Ensure readability and visual appeal:

**Emphasis and Highlighting**:
- Use bold for key terms: `\textbf{important}`
- Color highlights sparingly: `\textcolor{blue}{highlight}`
- Boxes for critical information
- Avoid italics (harder to read from distance)

### 9. QR Codes and Interactive Elements

Enhance poster interactivity for modern conferences:

**QR Code Integration**:
- Link to paper, code repository, or supplementary materials.

### 10. Compilation and Output

Generate high-quality PDF output for printing or digital display:

### 11. PDF Review and Quality Control

**CRITICAL**: Always review the generated PDF before printing or presenting. Use this systematic checklist:

### 11. Common Poster Content Patterns

Effective content organization for different research types:

**Experimental Research Poster**:
1. Title and authors.
2. Introduction: Problem and hypothesis.
3. Methods: Experimental design (with diagram).
4. Results: Key findings (2-4 main figures).
5. Conclusions: Main takeaways (3-5 bullet points).
6. Future work (optional).
7. References and acknowledgments.

**Computational/Modeling Poster**:
1. Title and authors.
2. Motivation: Problem statement.
3. Approach: Algorithm or model (with flowchart).
4. Implementation: Technical details.
5. Results: Performance metrics and comparisons.
6. Applications: Use cases.
7. Code availability (QR code to GitHub).
8. References.

**Review/Survey Poster**:
1. Title and authors.
2. Scope: Topic overview.
3. Methods: Literature search strategy.
4. Key findings: Main themes (organized by category).
5. Trends: Visualizations of publication patterns.
6. Gaps: Identified research needs.
7. Conclusions: Summary and implications.
8. References.

### 12. Accessibility and Inclusive Design

Design posters that are accessible to diverse audiences:

**Color Blindness Considerations**:
- Avoid red-green combinations (most common color blindness).
- Use patterns or shapes in addition to color.
- Test with color-blindness simulators.
- Provide high contrast (WCAG AA standard: 4.5:1 minimum).

**Visual Impairment Accommodations**:
- Large, clear fonts (minimum 24pt body text).
- High contrast text and background.
- Clear visual hierarchy.
- Avoid complex textures or patterns in backgrounds.

### 13. Poster Presentation Best Practices

Guidance beyond LaTeX for effective poster sessions:

**Content Strategy**:
- Tell a story, don't just list facts.
- Focus on 1-3 main messages.
- Use visual abstract or graphical summary.
- Leave room for conversation (don't over-explain).

## Integration with Other Skills

This skill works effectively with:
- **Scientific Schematics**: CRITICAL - Use for generating all poster diagrams and flowcharts.
- **Generate Image / Nano Banana Pro**: For stylized graphics, conceptual illustrations, and summary visuals.
- **Scientific Writing**: For developing poster content from papers.
- **Literature Review**: For contextualizing research.
- **Data Analysis**: For creating result figures and charts.

**Recommended workflow**: Always use scientific-schematics and generate-image skills BEFORE creating the LaTeX poster to generate all visual elements.

## Common Pitfalls to Avoid

**AI-Generated Graphics Mistakes (MOST COMMON):**
- ❌ Too many elements in one graphic (10+ items) → Keep to 3-5 max
- ❌ Text too small in AI graphics → Specify "GIANT (100pt+)" or "HUGE (150pt+)"
- ❌ Too much detail in prompts → Use "SIMPLE" and "ONLY X elements"
- ❌ No white space specification → Add "50% white space" to every prompt
- ❌ Complex flowcharts with 8+ steps → Limit to 4-5 steps maximum
- ❌ Comparison charts with 6+ items → Limit to 3 items maximum
- ❌ Key findings with 5+ metrics → Show only top 3

**Fixing Overflow in AI Graphics:**
If your AI-generated graphics are overflowing or have small text:
1. Add "SIMPLER" or "ONLY 3 elements" to prompt.
2. Increase font sizes: "150pt+" instead of "80pt+".
3. Add "60% white space" instead of "50%".
4. Remove sub-details: "NO sub-steps", "NO axis labels", "NO legend".
5. Regenerate with fewer elements.

**Design Mistakes**:
- ❌ Too much text (over 1000 words).
- ❌ Font sizes too small (under 24pt body text).
- ❌ Low-contrast color combinations.
- ❌ Cluttered layout with no white space.
- ❌ Inconsistent styling across sections.
- ❌ Poor quality or pixelated images.

**Content Mistakes**:
- ❌ No clear narrative or message.
- ❌ Too many research questions or objectives.
- ❌ Overuse of jargon without definitions.
- ❌ Results without context or interpretation.
- ❌ Missing author contact information.

**Technical Mistakes**:
- ❌ Wrong poster dimensions for conference requirements.
- ❌ RGB colors sent to CMYK printer (color shift).
- ❌ Fonts not embedded in PDF.
- ❌ File size too large for submission portal.
- ❌ QR codes too small or not tested.

**Best Practices**:
- ✅ Generate SIMPLE AI graphics with 3-5 elements max.
- ✅ Use GIANT fonts (100pt+) for key numbers in graphics.
- ✅ Specify "50% white space" in every AI prompt.
- ✅ Follow conference size specifications exactly.
- ✅ Test print at reduced scale before final printing.
- ✅ Use high-contrast, accessible color schemes.
- ✅ Keep text minimal and highly scannable.
- ✅ Include clear contact information and QR codes.
- ✅ Proofread carefully (errors are magnified on posters!).

## Package Installation

Ensure required LaTeX packages are installed:

## Scripts and Automation

Helper scripts available in `scripts/` directory:

## References

Comprehensive reference files for detailed guidance:

## Templates

Ready-to-use poster templates in `assets/` directory:

Load these templates and customize for your specific research and conference requirements.