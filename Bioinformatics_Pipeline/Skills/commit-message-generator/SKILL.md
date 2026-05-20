---
name: commit-message-generator
description: Summarizes codebase and documentation updates into a GitHub commit message.
skill-author: AROS
original-source: addyosmani/agent-skills/git-workflow-and-versioning
---

## When to Use

- Use this skill to generate a commit message after making changes to a codebase or documentation.
- Use this skill when you need a well-formatted and informative commit message that summarizes the changes.

## Key Features

- Summarizes changes from a diff or a list of changes.
- Generates a commit message that follows conventional commit standards.
- Can be used to generate commit messages for both code and documentation.

## Persona

- **Persona:** manuscript_writer
- **Model:** gemini-3.1-pro-preview

## Skills

- multi-source-news-writer
- pdf-to-ppt-pack

## Validation

To validate the output of this skill, please ensure:
1. The generated commit message accurately summarizes the changes.
2. The commit message follows the conventional commit format.
3. The commit message is clear, concise, and easy to understand.


## Versioning & Branching Guidance (Merged from Osmani)

- **Semantic Versioning:** Adhere to semver rules when writing commit messages that trigger releases.
- **Branching Strategy:** Ensure messages align with the current branch context (feature/ bugfix/ hotfix/).
