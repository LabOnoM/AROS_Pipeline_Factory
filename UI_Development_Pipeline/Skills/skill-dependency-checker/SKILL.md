---
name: skill-dependency-checker
description: Verifies the availability and functionality of critical skills and dependencies required for a given task prior to execution.
license: MIT
skill-author: AROS_code_generator
---

# Skill and Dependency Availability Checker

This skill ensures that all required skills and external system dependencies are available and correctly configured before a task is executed. It helps prevent runtime failures due to missing requirements.

## When to Use
- Use this skill as a pre-execution step in any workflow or policy to validate the environment.
- Use it when a task relies on other AROS skills or specific command-line tools.

## Inputs
- `--skills`: (Optional) A comma-separated list of AROS skill names to check. The skill checks for the existence of the corresponding directory in `~/.gemini/skills/`.
- `--dependencies`: (Optional) A comma-separated list of system command-line executables to check (e.g., `git`, `python`, `curl`).

## Dependencies
- `Python 3.6+`

## Workflow
1.  **Parse Inputs**: The script parses the `--skills` and `--dependencies` arguments.
2.  **Check Skills**: For each skill name provided, it checks if the directory `~/.gemini/skills/<skill_name>` exists.
3.  **Check Dependencies**: For each dependency, it uses the `shutil.which()` command to see if the executable is in the system's PATH.
4.  **Generate Report**: The script compiles the results into a JSON object.
5.  **Print Report**: The final JSON report is printed to standard output.

## Example Usage

```bash
# Check for the 'code-compiler' skill and the 'git' executable
python ~/.gemini/skills/skill-dependency-checker/check.py --skills "code-compiler" --dependencies "git"

# Check for multiple skills and dependencies
python ~/.gemini/skills/skill-dependency-checker/check.py --skills "code-compiler,gtb-validator" --dependencies "git,python,docker"

# Example of a failed check
python ~/.gemini/skills/skill-dependency-checker/check.py --skills "non-existent-skill" --dependencies "non-existent-binary"
```
