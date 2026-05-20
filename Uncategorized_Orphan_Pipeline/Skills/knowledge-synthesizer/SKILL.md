---
name: knowledge-synthesizer
description: Synthesizes a Knowledge Item (KI) by combining two distinct sources: a file of canonical facts and a file of extracted conversational data.
license: MIT
skill-author: AROS_code_generator
---

# Knowledge Synthesizer Skill

This skill provides a robust workflow for generating new Knowledge Items by merging two distinct data sources. Its primary feature is a mandatory pre-execution validation hook that explicitly checks for the presence and accessibility of all required input data before the content generation process begins.

## Key Capabilities

- **Dual-Source Synthesis**: Merges information from a canonical fact file and a conversation extraction file into a single KI.
- **Pre-execution Validation**: Ensures that both source fact and conversation extraction files exist and are readable before any processing occurs. This prevents runtime errors due to missing or invalid data.

## GEPA Critical Constraints: Dual-Input Strict Enforcement

- This skill has a strict, non-negotiable requirement for two input file paths: `--source-facts` and `--conversation-extractions`.
- The skill will **always fail** with a non-zero exit code if either argument is missing or points to a non-existent file. There are no exceptions to this rule. This strictness is by design to prevent the creation of incomplete or malformed Knowledge Items.

## Usage Patterns & Examples

### Scenario 1: Standard Dual-Source Synthesis (Correct Usage)

When you have both a file of canonical facts and a file of conversation extractions, provide both paths directly.

```sh
# Both files exist, so the command will succeed.
knowledge-synthesizer \
  --source-facts ./path/to/canonical-facts.md \
  --conversation-extractions ./path/to/convo-data.json
```

### Scenario 2: MANDATORY WORKAROUND for Single-Source Synthesis

**AGENT CRITICAL PATH:** If you only possess one of the two required files (e.g., only conversational data), you **MUST** create an empty placeholder file for the missing source to prevent immediate tool failure.

Follow this exact two-step process:

**Step 1: Create an empty placeholder file using `touch`.**
The filename is arbitrary, but it's good practice to make it descriptive.

```sh
# Example: Creating a placeholder for the missing --source-facts file.
touch empty-source-facts.md
```

**Step 2: Invoke the skill with both the real file and the empty placeholder.**

```sh
# The tool's validation now passes because both arguments are provided.
knowledge-synthesizer \
  --source-facts ./empty-source-facts.md \
  --conversation-extractions ./path/to/real-convo-data.json
```

---

## Common Failure Mode Analysis

The most common cause of failure is attempting to invoke the skill with only one of the required arguments.

- **INCORRECT INVOCATION (WILL ALWAYS FAIL):**
  ```sh
  # This command is missing the --source-facts argument and will fail.
  knowledge-synthesizer --conversation-extractions ./path/to/real-convo-data.json
  ```
- **REASON FOR FAILURE:** The tool's internal validation hook strictly enforces the presence of both `--source-facts` and `--conversation-extractions` arguments. Omitting one guarantees a non-zero exit code.
- **SOLUTION:** Always follow the mandatory two-step workaround for single-source synthesis shown in Scenario 2.