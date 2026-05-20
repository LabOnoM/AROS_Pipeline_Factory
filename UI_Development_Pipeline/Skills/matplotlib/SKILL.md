---
name: matplotlib
description: A low-level plotting library for comprehensive customization, ideal when fine-grained control is needed for novel charts or integrating into scientific workflows. Exports to PNG/PDF/SVG. Use seaborn for quick statistics, plotly for interactivity, and scientific-visualization for publication-ready multi-panel figures.
license: https://github.com/matplotlib/matplotlib/tree/main/LICENSE
metadata:
    skill-author: K-Dense Inc.
---
---
# Matplotlib

## Overview

Matplotlib is Python's foundational visualization library. This skill guides effective Matplotlib use, covering both the `pyplot` (MATLAB-style) and object-oriented (Figure/Axes) interfaces, plus best practices for publication-quality visuals.

## When to Use

-   Creating static plots (line, scatter, bar, histogram, etc.) needing high customization.
-   Generating publication-quality figures for export to PNG, PDF, or SVG.
-   Creating complex, multi-panel figures or novel plot types.
-   When `scripts/plot_template.py` directly addresses the request.

## Execution Workflow

1.  **Verify Requirements**: Confirm data source, plot type, output path, and customizations (labels, titles, colors, styling).
2.  **Select Method**: Use `scripts/plot_template.py` or write a new script following best practices.
3.  **Execute**: Run the script to generate the plot file.
4.  **Deliver**: Present the generated file, explicitly stating any assumptions.

## Dependencies

-   **Python**: 3.10+
-   **Packages**: `matplotlib`, `numpy`

## Core Concepts

### Matplotlib Hierarchy

1.  **Figure** - Top-level container for all plot elements.
2.  **Axes** - Plotting area where data is displayed. One Figure can have multiple Axes.
3.  **Artist** - Everything visible on the figure (lines, text, ticks).
4.  **Axis** - Number-line objects (x-axis, y-axis) handling ticks and labels.

### Two Interfaces

**1. pyplot Interface (Implicit, MATLAB-style)**

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()
```

-   Convenient for quick, simple plots and interactive work.

**2. Object-Oriented Interface (Explicit)**

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4])
ax.set_ylabel('some numbers')
plt.show()
```

-   **Recommended for most use cases.** More explicit, maintainable, and better for complex figures.

## Common Workflows

### 1. Basic Plot Creation

**Single plot workflow (Object-Oriented):**

```python
import matplotlib.pyplot as plt
import numpy as np

# Create figure and axes (RECOMMENDED)
fig, ax = plt.subplots(figsize=(10, 6))

# Generate and plot data
x = np.linspace(0, 2*np.pi, 100)
ax.plot(x, np.sin(x), label='sin(x)')
ax.plot(x, np.cos(x), label='cos(x)')

# Customize
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Trigonometric Functions')
ax.legend()
ax.grid(True, alpha=0.3)

# Save and/or display
plt.savefig('plot.png', dpi=300, bbox_inches='tight')
plt.show()
```

### 2. Multiple Subplots

**Creating subplot layouts:**

```python
import matplotlib.pyplot as plt

# Method 1: Regular grid
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
# (plotting commands for each subplot go here)

# Method 2: Mosaic layout (more flexible)
fig, axes = plt.subplot_mosaic([['left', 'right_top'],
                                ['left', 'right_bottom']],
                               figsize=(10, 8))
# (plotting commands for each subplot go here, referencing axes['left'], etc.)

# Method 3: GridSpec (maximum control)
from matplotlib.gridspec import GridSpec
fig = plt.figure(figsize=(12, 8))
gs = GridSpec(3, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, :])  # Top row, all columns
ax2 = fig.add_subplot(gs[1:, 0]) # Bottom two rows, first column
ax3 = fig.add_subplot(gs[1:, 1:]) # Bottom two rows, last two columns
# (plotting commands for each subplot go here, referencing ax1, etc.)
```

### 3. Plot Types and Use Cases

-   **Line plots** (`ax.plot`): Time series, continuous data, trends.
-   **Scatter plots** (`ax.scatter`): Relationships between variables, correlations.
-   **Bar charts** (`ax.bar`, `ax.barh`): Categorical comparisons.
-   **Histograms** (`ax.hist`): Data distributions.
-   **Heatmaps** (`ax.imshow`): Matrix data, correlations.
-   **Contour plots** (`ax.contour`): 3D data on a 2D plane.
-   **Box plots** (`ax.boxplot`): Statistical distributions.
-   **Violin plots** (`ax.violinplot`): Distribution densities.

See `references/plot_types.md` for complete examples.

### 4. Styling and Customization

**Using style sheets:**

```python
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-darkgrid')  # Apply predefined style
# Other styles: 'ggplot', 'bmh', 'fivethirtyeight'
# print(plt.style.available) to list all
```

**Customizing with rcParams:**

```python
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
```

**Text and annotations:**

```python
import matplotlib.pyplot as plt

ax.text(x, y, 'annotation', fontsize=12, ha='center')
ax.annotate('important point', xy=(x, y), xytext=(x+1, y+1),
            arrowprops=dict(arrowstyle='->', color='red'))
```

See `references/styling_guide.md` for details.

### 5. Saving Figures

**Export to various formats:**

```python
import matplotlib.pyplot as plt

# High-resolution PNG
plt.savefig('figure.png', dpi=300, bbox_inches='tight', facecolor='white')

# Vector formats
plt.savefig('figure.pdf', bbox_inches='tight')
plt.savefig('figure.svg', bbox_inches='tight')

# Transparent background
plt.savefig('figure.png', dpi=300, bbox_inches='tight', transparent=True)
```

-   `dpi`: Resolution. Use 300 for print, 150 for web.
-   `bbox_inches='tight'`: Removes excess whitespace.
-   `transparent=True`: For a transparent background.

### 6. Working with 3D Plots

```python
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Surface plot
ax.plot_surface(X, Y, Z, cmap='viridis')

# Set labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
```

## Best Practices

1.  **Interface Selection**: Use the object-oriented interface (`fig, ax = plt.subplots()`) for non-interactive work.
2.  **Figure Size and DPI**: Set `figsize` at creation. Use appropriate `dpi` for the output medium.
3.  **Layout Management**: Use `constrained_layout=True` or `fig.tight_layout()` to prevent overlapping elements.
4.  **Colormap Selection**: Use perceptually uniform colormaps. Sequential (e.g., `viridis`) for ordered data, diverging (e.g., `coolwarm`) for data with a meaningful center, and qualitative (e.g., `tab10`) for categorical data. Avoid `jet`.
5.  **Accessibility**: Use colorblind-friendly colormaps, add patterns/hatching to bars, and ensure sufficient contrast.
6.  **Performance**: For large datasets, consider `rasterized=True` or downsample data.
7.  **Code Organization**: Encapsulate plotting logic in functions.

## Provided Scripts

-   **`plot_template.py`**: Demonstrates various plot types with best practices. Use as a starting point.
-   **`style_configurator.py`**: Interactive utility to configure style preferences and generate custom style sheets.

## Provided References

-   **`plot_types.md`**: Complete catalog of plot types with code examples and use cases.
-   **`styling_guide.md`**: Detailed styling options, colormaps, and customization.
-   **`api_reference.md`**: Core classes and methods reference.
-   **`common_issues.md`**: Troubleshooting guide for common problems.

## Integration with Other Tools

-   **NumPy/Pandas**: Direct plotting from arrays and DataFrames.
-   **Seaborn**: High-level statistical visualizations built on top of matplotlib.
-   **Jupyter**: Interactive plotting with `%matplotlib inline` or `%matplotlib widget`.
-   **GUI frameworks**: Embedding in Tkinter, Qt, wxPython applications.

## Common Gotchas

1.  **Overlapping elements**: Use `constrained_layout=True` or `fig.tight_layout()`.
2.  **State confusion**: Use the OO interface to avoid issues with pyplot's implicit state.
3.  **Memory issues**: Explicitly close figures with `plt.close(fig)`.
4.  **DPI confusion**: `figsize` is in inches; final pixel size is `dpi * inches`.

## Additional Resources

-   Official Documentation: https://matplotlib.org/
-   Gallery: https://matplotlib.org/stable/gallery/index.html
-   Cheatsheets: https://matplotlib.org/cheatsheets/
-   Tutorials: https://matplotlib.org/stable/tutorials/index.html