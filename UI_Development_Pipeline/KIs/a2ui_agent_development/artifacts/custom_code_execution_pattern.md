# LLM-Driven Custom Analysis and Code Execution

This pattern enables users to request arbitrary visualizations and analyses that are not predefined in the agent's UI, by having the LLM generate and the agent execute Python code.

## 1. The Dynamic Analysis Flow

1.  **Request**: User asks for a novel visualization (e.g., "Heatmap of top 20 variable genes").
2.  **Intent Classification**: The LLM (e.g., Gemini 2.0 Flash) classifies the query as a `custom_plot` action.
3.  **Code Generation**: The LLM generates a self-contained Python script using pre-defined data variables.
4.  **Sandbox Execution**: The agent's `plot_generator` executes the code within a local namespace (`exec`) pre-populated with data handles.
5.  **Artifact Generation**: The plot is saved to disk, and the URL is returned in an A2UI `Image` component.
6.  **Interpretation**: The LLM-generated interpretation is displayed alongside the plot.

## 2. Sandbox Configuration

To ensure reliability and safety, provide the LLM with a stable execution environment:

### Pre-loaded Variables
- **DataFrames**: `counts_df` (normalized expression), `metadata_df` (sample conditions).
- **Functions**: `load_de(comparison)` (returns DE results as DataFrame).
- **Libraries**: `pd`, `np`, `plt`, `stats`.
- **Infrastructure**: `fig`, `ax` (pre-created matplotlib objects).
- **Constants**: `CONDITION_COLORS`, `CONDITION_LABELS`.

### System Prompt Guidelines (Safety & Stability)
- **Matplotlib Only**: Direct the LLM to use pure `matplotlib` (`ax.imshow()`, `ax.scatter()`) rather than complex high-level libraries like `seaborn` or `holoviews` which have brittle keyword arguments.
- **Manual Normalization**: Instruct the LLM to perform its own Z-score or log normalization within the script to avoid hidden state.
- **Interpretation Handling**: The LLM must set a local variable `ai_text = "..."` so the agent can extract the specific findings from the execution context.

## 3. Error Recovery and Robustness

Custom code execution is prone to runtime errors (e.g., `AttributeError`, `ValueError`).

- **Try/Except Wrappers**: Wrap the `exec()` call in a try/except block.
- **Error Feedback**: If a plot fails, capture the exception trace and display it as a code block to the user so they can adjust their query.
- **Fallback to Text**: If the UI part fails but the LLM provided text interpretation, ensure the text remains visible.

## 4. Implementation Example (`plot_generator.py`)

```python
def generate_custom_plot(code: str, title: str = "Custom Analysis") -> dict:
    # 1. Setup namespace with counts_df, metadata_df, plt, np, etc.
    fig, ax = plt.subplots(figsize=(10, 8))
    namespace = {
        "pd": pd, "np": np, "plt": plt, "ax": ax, "fig": fig,
        "counts_df": counts_df, "metadata_df": metadata_df,
    }

    # 2. Execute
    try:
        exec(code, namespace)
    except Exception as e:
        plt.close(fig)
        return {"url": "", "ai_text": f"Error executing code: {e}"}

    # 3. Save and Return
    url = _save_plot(fig, "custom")
    ai_text = namespace.get("ai_text", f"**{title}**\nCustom analysis results.")
    return {"url": url, "ai_text": ai_text}
```

## 5. Benefits of this Pattern
- **Infinite Flexibility**: Avoids "Button Bloat" by handling long-tail analysis requests.
- **Researcher Empowerment**: Users can experiment with novel visualization techniques (e.g., custom clustering or gene list comparisons) without developer intervention.
- **Grounding**: By executing on *real* local analysis files, the agent avoids the "hallucination" risk inherent in LLM-generated data.
