# Skills Library and MCP Integration

To scale an agent's expertise, it can be connected to an external library of specialized skills (e.g., bioinformatics, statistical analysis). This document covers the technical integration and design patterns for managing large skill sets.

## 1. The Skills Library Model

A skills library is a collection of "Skills" (directories) containing:
- `SKILL.md`: Main instructions and metadata (name, description, tags).
- `references/`: Supporting documents, API specs, and templates.

## 2. Technical Integration Tools

The agent uses three core tools to browse and utilize the 175+ available skills:

1.  **`search_skills`**: Uses weighted keyword scoring to find relevant skills.
    - **Name Match**: 3 points (highest relevance).
    - **Description Match**: 2 points.
    - **Body Preview**: 1 point.
2.  **`read_skill`**: Reads specific documents within a skill directory. It enforces security by preventing directory traversal and truncates large files (e.g., 15k chars) to protect the LLM's token window.
3.  **`list_skill_categories`**: Group skills into domains like "Databases", "Bioinformatics", or "Visualization" to make the library browsable for the user and LLM.

## 3. Semantic Search and MCP

Integration with an **MCP (Model Context Protocol)** server enables semantic search. The server indexes the skills and provides ranked results based on meaning rather than just keywords.

*   **Hybrid Approach**: Scientific agents should use the filesystem as the primary "Ground Truth" for reliability (low latency, zero external process dependency) while using MCP as a scalable backend for multiple agents.

## 4. Pattern: Protocol-as-a-Skill

As the A2UI protocol spec grows, including it in the system prompt becomes inefficient. The **Protocol-as-a-Skill** pattern offloads the specification to the skills library.

### Implementation
1.  **Create Skill**: Add an `a2ui-protocol` skill to `~/.gemini/skills/`.
2.  **Pointer**: Add a concise rule in the agent's prompt: *"Consult the A2UI Protocol Skill for standard component definitions and interactivity examples."*
3.  **On-Demand Retrieval**: The LLM calls `read_skill("a2ui-protocol", "references/form_example.md")` only when it needs to build a complex UI.

## 5. Benefits
- **Token Efficiency**: Prompts stay small and focused.
- **Accuracy**: The agent uses the provided `.md` files as the absolute ground truth.
- **Shared Standards**: Multiple agents (e.g., a "GSA Explorer" and a "Protein Searcher") can share the same protocol documentation.
