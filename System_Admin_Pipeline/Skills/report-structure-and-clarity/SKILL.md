---
name: report-structure-and-clarity
description: A mandatory policy for structuring all analytical and status reports to ensure clarity, consistency, and actionable insights for system-wide communication.
license: MIT
skill-author: AROS-Core
---

# Policy: Report Structure and Clarity

This policy enforces a standardized structure for all generated reports to ensure they are clear, consistent, and provide actionable insights. This is a system-wide requirement for any task that concludes with a formal report.

## Core Principles

1.  **Clarity**: Reports must be easily understood by both technical and non-technical stakeholders. Avoid jargon where possible and define it when necessary.
2.  **Consistency**: Adherence to a single, system-wide report format reduces cognitive overhead and makes information easier to locate and compare.
3.  **Actionability**: Every report should drive a decision or action. Findings must be linked to concrete recommendations or next steps.

## MANDATORY SKILL INSTRUCTIONS:

Any agent or skill generating a report, analysis summary, or status update **MUST** structure its output according to the following four-part format.

---

### **Standard Report Structure**

**1. Executive Summary:**
   - **Purpose:** A 1-3 sentence overview stating the report's objective.
   - **Outcome:** A brief statement of the primary conclusion or result.

**2. Key Findings:**
   - A bulleted list of the most critical insights derived from the analysis.
   - Each finding should be a clear and concise statement.
   - *Example:*
     - "- Metric A increased by 15% following the system update."
     - "- Failure rate in Module B is correlated with memory pressure."

**3. Detailed Analysis / Supporting Data:**
   - The evidence backing the key findings.
   - This section can include tables, log snippets, metric charts, or detailed technical explanations.
   - Data must be clearly labeled and referenced in the Key Findings section.

**4. Conclusion & Recommendations:**
   - **Conclusion:** A brief summary of the overall outcome.
   - **Next Steps:** An ordered list of actionable recommendations or tasks.
   - *Example:*
     - "1. **(High Priority)** Allocate additional memory to Module B."
     - "2. **(Medium Priority)** Investigate the root cause of the 15% increase in Metric A."

---
