# A2UI Interactive Form and Case Study (v0.9)

This pattern allows agents to guide users through complex configurations using native A2UI components like `TextField`, `Slider`, `CheckBox`, and `Button`.

## 1. Example Structure (v0.9)

A2UI v0.9 uses a flat component structure where properties are direct members of the component object.

```json
[
  {"id": "root", "component": "Column", "children": {"explicitList": [
    "title", "dataset_select", "pc_x_field", "update_btn"
  ]}},
  
  {"id": "title", "component": "Text", "text": "📊 PCA Configuration", "textStyle": "h2"},
  
  {"id": "dataset_select", "component": "TextField", "label": "Dataset", 
   "text": {"path": "/config/dataset"}, "hint": "options: GSE261849, GSE12345"},
  
  {"id": "pc_x_field", "component": "Slider", "label": "PC X", 
   "value": {"path": "/config/pc_x"}, "min": 1, "max": 10},
  
  {"id": "update_btn", "component": "Button", "label": "🔄 Update Plot",
   "action": {"event": {"name": "regenerate_plot", "context": {
     "plot_type": "pca"
   }}}}
]
```

## 2. Patterns for Interactivity

### Dynamic Config Persistence
To ensure user changes persist when a plot is regenerated (e.g., clicking "Update Plot"), the client must send its current data model state back to the agent.
- **Client Side**: Inject `surface.dataModel.get('/config')` into the action's `context`.
- **Server Side**: The agent extracts these `current_values` from the action context and uses them to pre-populate the `dataModel` of the newly created surface.

### Component Fallbacks
If a specific component (like `MultipleChoice`) is unsupported by a renderer, use a `TextField` with `hint` text (e.g., "choose from: option1, option2") to guide user input safely.

---

# Case Study: GSE261849 RNA-seq Explorer

The **GSE261849 Explorer** is a high-fidelity bioinformatics agent using **Gemini 2.0 Flash** and **A2UI v0.9**.

### 1. LLM-Powered Query Routing
The agent uses a "Routing and Classification" pattern:
- **Query**: "Show me gene expression of SOX9"
- **LLM Action**: Classifies as `expression`, extracts `genes=['SOX9']`.
- **Query**: "What's the difference between Day 5 and Day 17?"
- **LLM Action**: Classifies as `volcano`, selects appropriate comparison.
- **Query**: "Show me a clustering heatmap"
- **LLM Action**: Classifies as `custom_plot`, generates Python code.

### 2. Custom Plot Generation (The "Sandbox" Pattern)
For queries that don't fit predefined templates, the agent generates and executes Python code:
- **Data Sandbox**: Pre-loaded with `counts_df`, `metadata_df`, and `load_de()`.
- **Execution**: Runs `exec(code, namespace)` and saves the plot image.
- **Verification**: Executes on **real analysis results** (CSV) to prevent hallucinated trends.

### 3. Visual Polish and Accessibility
- **Light/Dark Resilience**: Slider tracks fixed with high-contrast colors (`#ccc`).
- **Clean Tables**: Markdown tables reformatted to bullet points for better rendering in `Text` components.
- **Title and Branding**: Uses emojis and clear headings (🧬, 📊, 🤖) for a professional dashboard feel.

### 4. Verified Analysis
The agent is grounded in `[WORKSPACE_ROOT]/GSE261849/analysis/results/`. It computes PCA on-the-fly using `scikit-learn` from the raw normalized count file, ensuring the A2UI dashboard matches the researcher's local analysis files exactly.
