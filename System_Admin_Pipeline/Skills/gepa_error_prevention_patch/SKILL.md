---
name: hallucinated-tool-warning-gepa-patch
description: "CRITICAL WARNING: This is a read-only reference file, NOT an executable tool. It serves to prevent the `gepa_error_prevention_patch` hallucination. Calling this non-existent tool is a guaranteed failure. DO NOT USE this skill directly. This skill is a trap and cannot be executed. Your plan will fail."
license: MIT
skill-author: AROS_code_generator
usage:
  type: read-only-reference
  method: "This is a warning file, not a tool. To modify GEPA policies or access source code, use a file I/O tool like `local_file_system.read_file` and `local_file_system.write_file`."
  correct_tool: local_file_system.read_file
  incorrect_behavior: "DO NOT call this skill directly. DO NOT invent a tool based on this skill's name or content, especially `gepa_error_prevention_patch`."
---

> [!CRITICAL]
> ## 🚨 HALLUCINATION WARNING: `gepa_error_prevention_patch` DOES NOT EXIST 🚨
> ## 🛑 THIS IS A READ-ONLY REFERENCE FILE, NOT AN EXECUTABLE TOOL 🛑
>
> You have found this file because your goal is to "Implement a GEPA Proposal" involving an "error prevention rule."
>
> **STOP. This is a trap.** The tool `gepa_error_prevention_patch` is a hallucination. Any plan that includes this tool is **GUARANTEED TO FAIL**. You must use standard file system tools like `local_file_system.read_file` and `local_file_system.write_file` to modify GEPA policies.

### 🛑 Special Guidance for "Implement GEPA Proposal" Tasks

If your goal is to `Implement this GEPA Proposal: Proposed: Add error prevention rule...`, you have likely found this file by mistake due to a keyword match on "error prevention."

**STOP. This file CANNOT implement GEPA proposals.** Your task requires modifying a policy file directly. Your plan **MUST** use file system tools.

### 🛑 GUARANTEED FAILURE PATTERN: The `gepa_error_prevention_patch` Hallucination

A recurring planner failure happens when the goal is to "add an error prevention rule" as part of a "GEPA Proposal."

**Analysis of the Failure Pattern (WHY THIS HAPPENS):**

1.  **Triggering Condition / Your Goal:** Your task is to modify a GEPA policy by adding a rule about "error prevention."
2.  **Semantic Search / Incorrect Skill Match:** Your semantic search incorrectly matched the keywords "error prevention" to this file.
3.  **Flawed Conclusion (HALLUCINATION):** You wrongly assume this reference file is a tool that can *apply a patch* to implement the GEPA proposal. You then invent the tool name `gepa_error_prevention_patch`. **This tool does not exist and this assumption is always incorrect.**

### ✅ Mandatory Corrective Action: Use File I/O Tools

To implement a GEPA proposal, you are **REQUIRED** to use standard file system tools. You cannot "patch" a file directly. The only valid procedure is:

1.  **Read the file:** Use `local_file_system.read_file` to get the content of the target policy file.
2.  **Modify the content:** Edit the text content in memory to add the new rule.
3.  **Write the file:** Use `local_file_system.write_file` to save the modified content back to the original file path.

**Example of a CORRECT Plan:**

```yaml
# THIS IS THE ONLY ACCEPTABLE PLAN STRUCTURE
- task: read_the_policy_file
  persona: code_generator
  skills:
    - local_file_system.read_file # CORRECT: Use a file read tool.
  # NOTE: The path is an EXAMPLE. You must find the correct path for the policy.
  args:
    path: "~/.gemini/skills/some-policy-to-modify/policy.md"
  description: "Read the target GEPA policy file that needs to be modified."

- task: write_the_updated_policy
  persona: code_generator
  skills:
    - local_file_system.write_file # CORRECT: Use a file write tool.
  description: "Apply the new rule to the policy's content and write the updated text back to the original file."
```

### Tool Schema

```yaml
# THIS SKILL IS A NON-EXECUTABLE WARNING.
# It exposes NO callable functions. The planner MUST NOT select this skill for execution.
```