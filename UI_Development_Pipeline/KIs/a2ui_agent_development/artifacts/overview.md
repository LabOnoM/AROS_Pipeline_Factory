# A2UI Agent Development Overview

This Knowledge Item contains detailed design patterns, implementation strategies, and troubleshooting guides for building AI agents that use the **A2UI (Agent to UI) protocol**.

## Artifacts Roadmap

### 1. Protocol and Architecture
- [protocol_and_architecture.md](./protocol_and_architecture.md): Core concepts of A2UI, including the Adjacency List model, message types (surfaceUpdate, beginRendering), and data binding.

### 2. Implementation Patterns
- [agent_implementation_patterns.md](./agent_implementation_patterns.md): Best practices for prompt engineering, LLM-powered query routing, session continuity, and grounding in real data.
- [custom_code_execution_pattern.md](./custom_code_execution_pattern.md): Advanced pattern for allowing LLMs to generate and execute Python code for arbitrary visualizations.
- [scientific_interpretation.md](./scientific_interpretation.md): Presenting scientific context, findings, and expert AI suggestions within the UI.

### 3. Case Studies
- [interactive_form_and_case_study.md](./interactive_form_and_case_study.md): A deep dive into the GSE261849 RNA-seq Explorer (v0.9), demonstrating interactive plot configuration, intent classification, and custom analytics.

### 4. Integration and Expertise
- [external_skill_integration.md](./external_skill_integration.md): Patterns for connecting agents to large external libraries (175+ skills) and MCP servers.
- [skill_based_documentation.md](./skill_based_documentation.md): The "Protocol-as-a-Skill" pattern to offload specs to an external skill.

### 5. Maintenance
- [troubleshooting_rendering.md](./troubleshooting_rendering.md): Log of common pitfalls (slider visibility, table formatting, icon bugs, persistence issues) and their solutions.
