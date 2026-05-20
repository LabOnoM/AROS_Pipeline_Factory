# GEPA Proposal: Generated Content Completeness Heuristics

This document defines the technical heuristics and logic for detecting truncated, incomplete, or malformed generated text. These checks are designed to be run programmatically to ensure deliverables meet a minimum quality standard.

---

## 1. Abrupt Sentence Termination

This heuristic detects text that ends mid-sentence.

**Logic:**

1.  Trim all trailing whitespace from the content.
2.  Check if the last character is one of the standard sentence-terminating punctuation marks: `.`, `?`, `!`, `"`, `'`, `)`.
3.  If the content is Markdown, also check for valid non-sentence endings like a code block fence (`` ` ``) or a list item.
4.  **Trigger Condition:** The text fails the check if the last character is an alphanumeric character or common punctuation that does not terminate a sentence (e.g., `,`, `;`, `:`).

**Example Failure:**

> "The primary mechanism for this is the phosphorylation of the target protein, which in turn leads to a conformational change and"

---

## 2. Trailing Ellipsis

This is a strong and simple signal of deliberate or accidental truncation.

**Logic:**

1.  Trim all trailing whitespace from the content.
2.  Check if the content ends with an ellipsis (`...`). Note that some models may output a single '…' character, so both should be checked.

**Trigger Condition:** The text ends with `...` or `…`.

**Example Failure:**

> "To install the required packages, you first need to set up your environment and then run..."

---

## 3. Unbalanced Delimiters & Tags

This heuristic detects incomplete code blocks, lists, or other structured formats.

**Logic:**

1.  **Brackets/Parentheses:** Count the occurrences of opening brackets (`(`, `[`, `{`) and closing brackets (`)`, `]`, `}`).
2.  **HTML/XML Tags:** For each tag type (e.g., `<div>`, `<p>`), count opening and closing tags. This requires a more sophisticated parser to ignore self-closing tags (e.g., `<br />`).
3.  **Markdown Code Fences:** Count the number of lines that are exactly ` ``` `. The total count must be an even number.

**Trigger Condition:**

*   The count of any opening delimiter does not match the count of its corresponding closing delimiter.
*   The count of Markdown code fences (`` ` ``) is odd.

**Example Failures:**

> **Unbalanced Bracket:**  
> `const config = { "key": "value", "enabled": true `
>
> **Unclosed Markdown Fence:**  
> `Here is some code:
>  ```python
> print("Hello, World!")`

---

## 4. Incomplete Markdown Structures

This heuristic looks for common structural failures in Markdown formatting.

**Logic:**

1.  **Incomplete Tables:** If a line matches the Markdown table header format (`|...|`), check for the presence of the separator line (`|---|`) immediately following it.
2.  **Incomplete Lists:** If the last non-empty line starts with a list marker (`* `, `- `, `1. `), it may be an incomplete list, especially if the line itself is short or looks unfinished. This is a weaker signal and should be combined with other heuristics.

**Trigger Condition:**

*   A table header is present without a subsequent separator line.
*   (Lower confidence) The document ends on a line that is clearly a list item without subsequent content.

**Example Failure:**

> **Missing Table Separator:**  
> `| Header 1 | Header 2 |`  
> `Some other text...`
>
> **Hanging List Item:**  
> `The steps are:
>  * First, do this
>  * Second, do that
>  * Finally,`

---

## Implementation Priority

1.  **High Priority:** Trailing Ellipsis, Unbalanced Delimiters (especially code fences). These are high-confidence signals.
2.  **Medium Priority:** Abrupt Sentence Termination. This is a good signal but requires careful implementation to avoid false positives (e.g., on headings).
3.  **Low Priority:** Incomplete Markdown Structures. These are harder to detect reliably and have a higher risk of false positives.
