import pandas as pd
import sys
import os
import io
import contextlib

# This is a conceptual placeholder for a real LLM call.
# In a real AROS environment, this would be replaced with a call
# to a dedicated LLM tool or service.
def llm_generate_plot_code(df_info, goal):
    """
    Generates Python plotting code using a conceptual LLM.
    """
    prompt = f"""
You are an expert data visualization assistant. Your task is to generate Python code to create a plot that meets a specific user goal, based on the provided data schema.

**Data Schema:**
{df_info}

**User Goal:**
"{goal}"

**Instructions:**
1.  Write Python code using pandas, matplotlib.pyplot, and seaborn.
2.  The data is available in a pandas DataFrame variable named `df`.
3.  Assume the following imports are already present:
    - `import pandas as pd`
    - `import matplotlib.pyplot as plt`
    - `import seaborn as sns`
4.  Do NOT include any code to load data (e.g., `pd.read_csv`).
5.  Do NOT include the boilerplate imports.
6.  The code should generate a single, insightful plot.
7.  End the code with `plt.show()` to display the plot.
8.  Provide only the Python code, without any explanation or surrounding text.

**Example:**
If the goal is "Show the distribution of age", the code might be:
```python
sns.histplot(df['age'])
plt.title('Distribution of Age')
plt.show()
```
"""
    # In a real implementation, this prompt would be sent to an LLM API.
    # For this placeholder, we will generate a simple, default plot.
    print(f"--- LLM Prompt ---\n{prompt}\n------------------", file=sys.stderr)
    
    # --- Conceptual LLM Response ---
    # This section simulates the LLM's output based on the goal.
    # A real implementation would involve a network request to an LLM service.
    if "distribution" in goal.lower():
        # A simple heuristic to find a numeric column for a histogram
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]
            return f"""
plt.figure(figsize=(10, 6))
sns.histplot(df['{col}'], kde=True)
plt.title('Distribution of {col}')
plt.xlabel('{col}')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
"""
    elif "correlation" in goal.lower() or "heatmap" in goal.lower():
        return """
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap='viridis', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()
"""
    else: # Default to a pairplot for general exploration
        return """
sns.pairplot(df)
plt.suptitle('Pairwise Relationships', y=1.02)
plt.show()
"""


def main(data_path, goal):
    """
    Dynamically generates and executes plotting code for the given data and goal.
    """
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}", file=sys.stderr)
        return

    try:
        # Load the data
        df = pd.read_csv(data_path)

        # Get data schema for the LLM prompt
        buffer = io.StringIO()
        df.info(buf=buffer)
        df_info = buffer.getvalue()

        # Generate the plotting code
        print("Generating plotting code...", file=sys.stderr)
        plot_code = llm_generate_plot_code(df_info, goal)
        print(f"--- Generated Code ---\n{plot_code}\n--------------------", file=sys.stderr)


        # Execute the generated code
        print("Executing generated code...", file=sys.stderr)
        # Create a safe execution environment with access to the df variable
        exec_globals = {
            'df': df,
            'pd': pd,
            'plt': __import__('matplotlib.pyplot'),
            'sns': __import__('seaborn')
        }
        
        # Use contextlib to redirect stdout/stderr if the generated code is noisy
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
             exec(plot_code, exec_globals)

        print("Plot generation complete.", file=sys.stderr)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <path_to_csv_data> \"<visualization_goal>\"", file=sys.stderr)
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    user_goal = sys.argv[2]
    main(csv_file_path, user_goal)
