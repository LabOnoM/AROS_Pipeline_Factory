---
name: plotly
description: Interactive visualization library for Python. Use when you need hover tooltips, zoom/pan, selection, animations, or charts embeddable in web pages (e.g., dashboards, exploratory analysis, presentations). Best for dashboards, exploratory analysis, and presentations. For static publication figures use matplotlib or scientific-visualization.
license: MIT
metadata:
    skill-author: K-Dense Inc. and AIPOCH
---

# Plotly

## When to Use

Use Plotly when you need interactive, shareable visualizations, especially in these scenarios:

- **Exploratory data analysis (EDA):** Quickly inspect distributions, relationships, and outliers with hover and selection.
- **Dashboards and web embedding:** Publish interactive charts to HTML pages or integrate into web apps (e.g., Dash).
- **Time-series monitoring:** Use range sliders, zooming, and pan for dense temporal data.
- **Presentations and stakeholder reviews:** Interactive tooltips and legend toggling help explain results live.
- **Complex multi-panel figures:** Build subplots and multi-trace figures with fine-grained layout control.

If you only need static publication figures, consider Matplotlib or other scientific visualization tools.

## Key Features

- **Two APIs**
  - **Plotly Express (`plotly.express`, `px`)**: High-level, concise API for common charts from DataFrames.
  - **Graph Objects (`plotly.graph_objects`, `go`)**: Low-level building blocks for full control and custom figures.
  - Plotly Express returns a **Graph Objects `Figure`**, so you can mix both styles.
- **40+ chart types** across statistical, scientific, financial, geospatial, and 3D categories.
- **Interactivity by default**
  - hover tooltips, zoom/pan, legend toggling
  - box/lasso selection
  - range sliders (time series)
  - buttons/dropdowns and animations
- **Layout and styling**
  - subplots (`make_subplots`)
  - templates (e.g., `plotly_dark`, `plotly_white`)
  - annotations, shapes, axes/legend control
- **Export**
  - interactive HTML (`write_html`)
  - static images via Kaleido (`write_image`)

## Quick Start

Install Plotly with recommended dependencies:
```bash
uv pip install "plotly>=5.0" "pandas>=1.5" "kaleido>=0.2"
```

Basic usage with Plotly Express (high-level API):
```python
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [10, 11, 12, 13]
})

fig = px.scatter(df, x='x', y='y', title='My First Plot')
fig.show()
```

## Choosing Between APIs

### Use Plotly Express (px)
For quick, standard visualizations with sensible defaults:
- Working with pandas DataFrames
- Creating common chart types (scatter, line, bar, histogram, etc.)
- Need automatic color encoding and legends
- Want minimal code (1-5 lines)

### Use Graph Objects (go)
For fine-grained control and custom visualizations:
- Chart types not in Plotly Express (3D mesh, isosurface, complex financial charts)
- Building complex multi-trace figures from scratch
- Need precise control over individual components
- Creating specialized visualizations with custom shapes and annotations

**Note:** Plotly Express returns graph objects Figure, so you can combine approaches:
```python
fig = px.scatter(df, x='x', y='y')
fig.update_layout(title='Custom Title')  # Use go methods on px figure
fig.add_hline(y=10)                     # Add shapes
```

## Core Capabilities

### 1. Chart Types

Plotly supports 40+ chart types organized into categories:

**Basic Charts:** scatter, line, bar, pie, area, bubble

**Statistical Charts:** histogram, box plot, violin, distribution, error bars

**Scientific Charts:** heatmap, contour, ternary, image display

**Financial Charts:** candlestick, OHLC, waterfall, funnel, time series

**Maps:** scatter maps, choropleth, density maps (geographic visualization)

**3D Charts:** scatter3d, surface, mesh, cone, volume

**Specialized:** sunburst, treemap, sankey, parallel coordinates, gauge

### 2. Layouts and Styling

**Subplots:** Create multi-plot figures with shared axes:
```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(rows=2, cols=2, subplot_titles=('A', 'B', 'C', 'D'))
fig.add_trace(go.Scatter(x=[1, 2], y=[3, 4]), row=1, col=1)
```

**Templates:** Apply coordinated styling:
```python
fig = px.scatter(df, x='x', y='y', template='plotly_dark')
# Built-in: plotly_white, plotly_dark, ggplot2, seaborn, simple_white
```

**Customization:** Control every aspect of appearance:
- Colors (discrete sequences, continuous scales)
- Fonts and text
- Axes (ranges, ticks, grids)
- Legends
- Margins and sizing
- Annotations and shapes

### 3. Interactivity

Built-in interactive features:
- Hover tooltips with customizable data
- Pan and zoom
- Legend toggling
- Box/lasso selection
- Rangesliders for time series
- Buttons and dropdowns
- Animations

```python
# Custom hover template
fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Value: %{y:.2f}<extra></extra>'
)

# Add rangeslider
fig.update_xaxes(rangeslider_visible=True)

# Animations
fig = px.scatter(df, x='x', y='y', animation_frame='year')
```

### 4. Export Options

**Interactive HTML:**
```python
fig.write_html('chart.html')                       # Full standalone
fig.write_html('chart.html', include_plotlyjs='cdn')  # Smaller file
```

**Static Images (requires kaleido):**
```python
fig.write_image('chart.png')   # PNG
fig.write_image('chart.pdf')   # PDF
fig.write_image('chart.svg')   # SVG
```

## Common Workflows

### Scientific Data Visualization

```python
import plotly.express as px

# Scatter plot with trendline
fig = px.scatter(df, x='temperature', y='yield', trendline='ols')

# Heatmap from matrix
fig = px.imshow(correlation_matrix, text_auto=True, color_continuous_scale='RdBu')

# 3D surface plot
import plotly.graph_objects as go
fig = go.Figure(data=[go.Surface(z=z_data, x=x_data, y=y_data)])
```

### Statistical Analysis

```python
# Distribution comparison
fig = px.histogram(df, x='values', color='group', marginal='box', nbins=30)

# Box plot with all points
fig = px.box(df, x='category', y='value', points='all')

# Violin plot
fig = px.violin(df, x='group', y='measurement', box=True)
```

### Time Series and Financial

```python
# Time series with rangeslider
fig = px.line(df, x='date', y='price')
fig.update_xaxes(rangeslider_visible=True)

# Candlestick chart
import plotly.graph_objects as go
fig = go.Figure(data=[go.Candlestick(
    x=df['date'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close']
)])
```

### Multi-Plot Dashboards

```python
from plotly.subplots import make_subplots
import plotly.graph_objects as go

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Scatter', 'Bar', 'Histogram', 'Box'),
    specs=[[{'type': 'scatter'}, {'type': 'bar'}],
           [{'type': 'histogram'}, {'type': 'box'}]]
)

fig.add_trace(go.Scatter(x=[1, 2, 3], y=[4, 5, 6]), row=1, col=1)
fig.add_trace(go.Bar(x=['A', 'B'], y=[1, 2]), row=1, col=2)
fig.add_trace(go.Histogram(x=data), row=2, col=1)
fig.add_trace(go.Box(y=data), row=2, col=2)

fig.update_layout(height=800, showlegend=False)
```

## Integration with Dash

For interactive web applications, use Dash (Plotly's web app framework):

```bash
uv pip install dash
```

```python
import dash
from dash import dcc, html
import plotly.express as px

app = dash.Dash(__name__)

fig = px.scatter(df, x='x', y='y')

app.layout = html.Div([
    html.H1('Dashboard'),
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)
```

## Implementation Details

### API choice: `px` vs `go`
- **Use `plotly.express` (`px`)** when:
  - your data is in a Pandas DataFrame,
  - you want fast defaults and concise code,
  - you need standard charts (scatter/line/bar/histogram/box/violin, etc.).
- **Use `plotly.graph_objects` (`go`)** when:
  - you need precise control over traces, axes, annotations, shapes, or multi-trace composition,
  - you are building uncommon chart types or highly customized figures.
- **Mixing is standard**: `px.*` returns a `go.Figure`, so `fig.update_layout(...)`, `fig.add_trace(...)`, `fig.add_hline(...)`, etc. work seamlessly.

### Interactivity configuration
- **Hover formatting**: customize per-trace with `hovertemplate` to control text and numeric formatting.
- **Time-series navigation**: enable range sliders via:
  - `fig.update_xaxes(rangeslider_visible=True)`
- **Selection tools**: box/lasso selection is available by default in many chart types; you can further configure selection behavior via trace/layout options.

### Export behavior
- **HTML export** (`write_html`) preserves full interactivity.
  - `include_plotlyjs="cdn"` reduces file size but requires internet access to load Plotly JS.
- **Static export** (`write_image`) requires **Kaleido** and produces PNG/SVG/PDF suitable for reports.

## Dependencies

- `plotly>=5.0`
- `pandas>=1.5` (recommended for DataFrame-based workflows)
- `kaleido>=0.2` (optional, required for static image export: PNG/SVG/PDF)
- `dash>=2.0` (optional, for building interactive web apps)

## Example Usage

A complete runnable example demonstrating: Plotly Express + Graph Objects updates, hover customization, subplots, and export.

### Run

```python
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    # Sample dataset
    df = pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5],
            "y": [10, 11, 12, 11.5, 13],
            "group": ["A", "A", "B", "B", "B"],
        }
    )

    # 1) Quick chart with Plotly Express
    fig_scatter = px.scatter(
        df,
        x="x",
        y="y",
        color="group",
        title="Scatter (px) + Graph Objects Updates",
        template="plotly_white",
    )

    # 2) Use Graph Objects methods on a px figure
    fig_scatter.update_traces(
        hovertemplate="x=%{x}<br>y=%{y:.2f}<br>group=%{marker.color}<extra></extra>"
    )
    fig_scatter.add_hline(y=11, line_dash="dash", line_color="gray")

    # 3) Build a small dashboard-like layout with subplots
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Interactive Scatter", "Group Means (Bar)"),
        specs=[[{"type": "scatter"}, {"type": "bar"}]],
    )

    # Left: reuse traces from the px figure
    for tr in fig_scatter.data:
        fig.add_trace(tr, row=1, col=1)

    # Right: bar chart with group means
    means = df.groupby("group", as_index=False)["y"].mean()
    fig.add_trace(
        go.Bar(x=means["group"], y=means["y"], name="mean(y)"),
        row=1,
        col=2,
    )

    fig.update_layout(
        title="Plotly End-to-End Example",
        height=450,
        legend_title_text="Group",
        margin=dict(l=40, r=20, t=70, b=40),
    )

    # Show interactively (notebook or supported environment)
    fig.show()

    # Export
    fig.write_html("plotly_example.html", include_plotlyjs="cdn")
    fig.write_image("plotly_example.png")  # requires kaleido

if __name__ == "__main__":
    main()
```

## When Not to Use

- Do not use this skill when the required source data, identifiers, files, or credentials are missing.
- Do not use this skill when the user asks for fabricated results, unsupported claims, or out-of-scope conclusions.
- Do not use this skill when a simpler direct answer is more appropriate than the documented workflow.

## Required Inputs

- A clearly specified task goal aligned with the documented scope.
- All required files, identifiers, parameters, or environment variables before execution.
- Any domain constraints, formatting requirements, and expected output destination if applicable.

## Recommended Workflow

1. Validate the request against the skill boundary and confirm all required inputs are present.
2. Select the documented execution path and prefer the simplest supported command or procedure.
3. Produce the expected output using the documented file format, schema, or narrative structure.
4. Run a final validation pass for completeness, consistency, and safety before returning the result.

## Output Contract

- Return a structured deliverable that is directly usable without reformatting.
- If a file is produced, prefer a deterministic output name such as `plotly_result.md` unless the skill documentation defines a better convention.
- Include a short validation summary describing what was checked, what assumptions were made, and any remaining limitations.

## Validation and Safety Rules

- Validate required inputs before execution and stop early when mandatory fields or files are missing.
- Do not fabricate measurements, references, findings, or conclusions that are not supported by the provided source material.
- Emit a clear warning when credentials, privacy constraints, safety boundaries, or unsupported requests affect the result.
- Keep the output safe, reproducible, and within the documented scope at all times.

## Failure Handling

- If validation fails, explain the exact missing field, file, or parameter and show the minimum fix required.
- If an external dependency or script fails, surface the command path, likely cause, and the next recovery step.
- If partial output is returned, label it clearly and identify which checks could not be completed.

## Additional Resources

- Official documentation: https://plotly.com/python/
- API reference: https://plotly.com/python-api-reference/
- Community forum: https://community.plotly.com/