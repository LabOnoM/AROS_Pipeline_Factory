---
name: report-structure-and-clarity-policy
description: A policy to ensure all analytical findings are delivered in a clear, well-structured, and easily digestible report format.
license: MIT
skill-author: AROS-GEPA
---

# Policy: Report Structure and Clarity

This document outlines the mandatory policy for structuring analytical reports within the AROS ecosystem. The primary objective is to ensure that all findings are communicated in a manner that is not only accurate but also clear, well-organized, and easily understandable by the end-user.

## When to Use

- Use this policy when generating any report that summarizes analytical findings, experimental results, or data explorations.
- Apply this policy when creating documents that synthesize information from multiple sources into a coherent narrative.
- This policy is mandatory for any skill or workflow that produces a final, user-facing report as its primary output.

## GEPA Error Prevention Rule: Clarity in Reporting

To prevent the delivery of confusing or poorly structured analytical results, all AROS components must adhere to the following GEPA rule:

**Deliver analysis findings in a clear, well-structured, and easily digestible report format.**

### Core Requirements:

1.  **Logical Flow**: The report must follow a logical structure, typically starting with a high-level summary or conclusion, followed by supporting details, methodology, and finally, the raw data or references if necessary.
2.  **Clear Headings and Sections**: Use clear, descriptive headings and subheadings (utilizing Markdown formatting) to organize the content into distinct sections. This allows users to easily navigate the report and find specific information.
3.  **Use of Formatting**: Employ formatting tools like bullet points, numbered lists, bold text, and tables to break up dense text and highlight key information.
4.  **Digestible Content**: Avoid long, monolithic blocks of text. Break down complex information into smaller, more manageable paragraphs or points.
5.  **Visual Aids**: Where appropriate, incorporate visualizations (charts, graphs, tables) to supplement the text and make the findings more intuitive, in accordance with the `illustrative-power-policy`.
6.  **Actionable Insights**: The report should focus on providing actionable insights and clear takeaways, rather than just presenting raw data.

## Example of Adherence

**Scenario:** An agent has analyzed sales data for two products, A and B, over the last quarter.

#### **Non-Compliant Output (Poor Structure):**
> We looked at the sales data. Product A sold 10,000 units and Product B sold 5,000 units. The trend for Product A was upward, while Product B was flat. The total revenue was $250,000. The data came from the main sales database and was analyzed using a standard time-series model. The model showed a significant positive trend for A.

#### **GEPA-Compliant Output (Well-Structured Report):**
> # Q3 Sales Analysis: Product Performance Report
>
> ## 1. Executive Summary
>
> This report details the sales performance of Products A and B for the third quarter. The key finding is that **Product A significantly outperformed Product B**, showing strong growth and accounting for the majority of revenue. We recommend allocating additional marketing resources to Product A to capitalize on this trend.
>
> ## 2. Key Findings
>
> - **Product A:**
>   - **Units Sold:** 10,000
>   - **Revenue:** $200,000
>   - **Trend:** Strong positive growth throughout the quarter.
>
> - **Product B:**
>   - **Units Sold:** 5,000
>   - **Revenue:** $50,000
>   - **Trend:** Sales remained flat with no significant growth.
>
> ## 3. Methodology
>
> The analysis was performed on sales data extracted from the primary sales database, covering the period from July 1st to September 30th. A time-series analysis was used to identify sales trends.
