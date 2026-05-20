# Skill-Based Documentation for A2UI Agents

As A2UI protocol complexity grows, including the full specification (messages, component catalog, data binding rules) in an agent's system prompt becomes inefficient and can confuse the LLM. 

## The Pattern: Protocol Skills

Instead of putting all documentation in the prompt, create a dedicated **A2UI Protocol Skill**. This skill acts as an external knowledge base that the LLM can "consult" or trigger upon when working with A2UI JSON.

### Benefits

1.  **Token Efficiency**: Only the most critical rules stay in the system prompt. Detailed examples and property references are stored in the skill.
2.  **Specialized Context**: Skills can contain large reference files (e.g., `standard_catalog.md`, `form_example.md`) that the LLM only reads when needed.
3.  **Consistency**: Multiple agents can share the same A2UI Protocol Skill, ensuring they all follow the same standards.
4.  **Troubleshooting Offloading**: Detailed troubleshooting guides for rare rendering errors can live in the skill, ready for the LLM to use when debugging a specific JSON failure.

### Implementation Checklist

*   **Trigger Phrases**: Ensure the skill description includes keywords like `surfaceUpdate`, `dataModelUpdate`, `MultipleChoice`, `action.context`, and `A2UI`.
*   **Prompt Pointer**: Add a concise note in the agent's system prompt: *"When generating A2UI JSON, follow the A2UI Protocol Skill standards for component structure and data binding."*
*   **Layered References**:
    *   `SKILL.md`: Core protocol rules and message types.
    *   `references/form_example.md`: Practical, copy-pasteable examples of interactive forms.
    *   `references/troubleshooting.md`: Manual fixes for common LLM generation errors.
    *   `references/agent_guide.md`: Server-side setup patterns (e.g., ADK usage).

## Evolution of the GSE261849 Explorer

The GSE261849 agent successfully transitioned to this model:
1.  **Initial State**: Huge prompt with all component rules.
2.  **Problem**: LLM occasionally halluncinated property names or forgot `surfaceId`.
3.  **Solution**: Created `~/.gemini/skills/a2ui-protocol/`.
4.  **Result**: Smaller, more focused system prompt for the agent, with the LLM using the skill to fetch specific JSON structures for complex plots and forms.
