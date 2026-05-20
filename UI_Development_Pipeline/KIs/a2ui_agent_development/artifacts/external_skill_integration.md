# External Skill Library and MCP Integration

To scale an agent's expertise, it can be connected to an external library of specialized skills (e.g., bioinformatics, statistical analysis, scientific databases). This allows the agent to remain lean while accessing "just-in-time" documentation for complex tasks.

## The Skills Library Model

A skills library is typically a flat directory structure where each subdirectory is a "Skill":
- `SKILL.md`: Main instructions and frontmatter (name, description).
- `references/`: Detailed documentation, API specs, or templates.

## Integration Tools

The agent uses three core tools to interact with the library:

1.  **`search_skills`**: Performs keyword or semantic search across the library. It parses the frontmatter of all `SKILL.md` files in the library directory to find relevant matches.
2.  **`read_skill`**: Reads the content of a specific document within a skill directory. This allows the LLM to get the full instructions once a relevant skill is identified.
3.  **`list_skill_categories`**: Provides a high-level overview of the library's contents, grouped by domain (e.g., "Databases", "Visualization").

## Semantic Search via MCP

While keyword search is a good fallback, integration with an **MCP (Model Context Protocol) server** like `claude-skills-mcp` enables true semantic search. The MCP server can index the skills library and provide ranked results based on the meaning of the user's query rather than just exact word matches.

### Implementation Pattern (`skills_tools.py`)

A robust search implementation (even without a vector DB) uses weighted keyword scoring:

```python
def search_skills(query, top_k):
    # 1. Scans ~/.gemini/skills for SKILL.md files.
    # 2. Scores matches based on weighted fields:
    #    - Name match: 3 points (Strongest intent match)
    #    - Description match: 2 points
    #    - Preview (First 200 chars of body): 1 point
    # 3. Sums scores per skill and returns top_k results.
    # 4. Returns JSON with skill_name, full description, and document manifest.

def read_skill(skill_name, document_path):
    # 1. Verifies the existence of the skill directory and document.
    # 2. Reads file content (truncating at 15k chars for token safety).
    # 3. Returns the document content for the LLM to use as ground truth.
```

### 3. Automated Categorization (`list_skill_categories`)

To make a large library (175+ skills) browsable, the agent can use automated categorization based on keyword patterns in the skill descriptions. This provides the user with high-level entry points (e.g., "Visualization", "Databases") without requiring manual tagging of every skill.

```python
def list_skill_categories():
    all_skills = _get_all_skills()
    categories = {"Databases": [], "Visualization": [], ...}
    for skill in all_skills:
        desc = skill.get("description", "").lower()
        if "database" in desc:
            categories["Databases"].append(skill["name"])
        elif any(kw in desc for kw in ["plot", "chart", "visual"]):
            categories["Visualization"].append(skill["name"])
        # ... fallback to "Other" ...
```

## 4. Reliability: Direct Filesystem vs. MCP

In production environments (especially within web-based agent executors), direct filesystem keyword scoring and parsing (`PyYAML`) often prove more robust than establishing an MCP-stdio or MCP-HTTP bridge for every user request. 

*   **Filesystem (Simpler)**: Low latency, no extra processes, zero external dependencies (other than PyYAML), highly reliable.
*   **MCP (Scalable)**: Better for centralizing multiple types of context retrieval across different agents, supports true semantic (vector) search.

Scientific agents benefit from a **Hybrid Approach**: Use weighted keyword scoring as the primary/fallback tool to ensure the agent always has access to its 175+ "Ground Truth" skills even if the MCP backend is slow or unreachable.

## Benefits for Scientific Agents

1.  **Domain Versatility**: An agent like the RNA-seq Explorer can quickly learn how to use `scanpy` or query `PubMed` by reading the respective skills.
2.  **Accuracy**: Instead of relying on its pre-trained knowledge which might be outdated or fuzzy on API details, the agent uses the provided `SKILL.md` as the "ground truth".
3.  **User Guidance**: The agent can suggest specialized tools to the user after searching the library, acting as a domain-aware consultant.
