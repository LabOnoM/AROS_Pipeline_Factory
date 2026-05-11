---
name: seaborn
description: Statistical visualization library for exploring data distributions, relationships, and categorical comparisons. Integrates with pandas and matplotlib for exploratory data analysis and publication-quality graphics. Best for box plots, violin plots, pair plots, and heatmaps.
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc. & AIPOCH
---

## Overview

Seaborn is a Python data visualization library built on top of matplotlib. It provides a high-level interface for creating informative and aesthetically pleasing statistical graphics. Use it for dataset-oriented plotting, multivariate analysis, automatic statistical estimation, and complex multi-panel figures with minimal code.

## When to Use

- Exploring relationships between variables in a DataFrame (e.g., scatter/line plots with `hue`, `size`, `style`).
- Comparing distributions across categories (e.g., box/violin/swarm plots for groups).
- Inspecting univariate/bivariate distributions (histograms, KDE, ECDF; joint and pairwise views).
- Visualizing correlation matrices or other rectangular data (heatmaps, clustered heatmaps).
- Building faceted "small multiples" quickly (split by `row`/`col` using figure-level APIs).

## Design Philosophy

Seaborn follows these core principles:

1. **DataFrame-oriented**: Works directly with DataFrames and named variables.
2. **Semantic mapping**: Automatically translates data values into visual properties (colors, sizes, styles).
3. **Statistical awareness**: Built-in aggregation, error estimation, and confidence intervals.
4. **Aesthetic defaults**: Publication-ready themes and color palettes out of the box.
5. **Matplotlib integration**: Full compatibility with matplotlib customization.

## Key Features

- **DataFrame-first API**: Works naturally with pandas "long-form/tidy" data and named columns.
- **Semantic mappings**: Encode extra dimensions via `hue`, `size`, `style`, and faceting (`row`, `col`).
- **Statistical awareness**: Built-in aggregation and uncertainty display (e.g., confidence intervals / error bars).
- **High-quality defaults**: Themes, contexts, and curated palettes for readable statistical graphics.
- **Two interfaces**:
  - **Axes-level** functions (return a matplotlib `Axes`, accept `ax=`) for custom layouts.
  - **Figure-level** functions (return Grid objects) for faceting and consistent multi-panel figures.
- **Matplotlib compatibility**: Fine-tune labels, annotations, and layout using matplotlib when needed.

## Dependencies

- `seaborn>=0.13`
- `matplotlib>=3.7`
- `pandas>=2.0`
- `numpy>=1.24`

## Quick Start

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load example dataset
df = sns.load_dataset('tips')

# Create a simple visualization
sns.scatterplot(data=df, x='total_bill', y='tip', hue='day')
plt.show()
```

## Core Plotting Interfaces

### Function Interface (Traditional)

The function interface provides specialized plotting functions organized by visualization type. Each category has **axes-level** functions (plot to single axes) and **figure-level** functions (manage entire figure with faceting).

**When to use:**
- Quick exploratory analysis
- Single-purpose visualizations
- When you need a specific plot type

### Objects Interface (Modern)

The `seaborn.objects` interface provides a declarative, composable API similar to ggplot2. Build visualizations by chaining methods to specify data mappings, marks, transformations, and scales.

**When to use:**
- Complex layered visualizations
- When you need fine-grained control over transformations
- Building custom plot types
- Programmatic plot generation

```python
from seaborn import objects as so

# Declarative syntax
(
    so.Plot(data=df, x='total_bill', y='tip')
    .add(so.Dot(), color='day')
    .add(so.Line(), so.PolyFit())
)
```

## Plotting Functions by Category

### Relational Plots (Relationships Between Variables)

**Use for:** Exploring how two or more variables relate to each other

- `scatterplot()` - Display individual observations as points
- `lineplot()` - Show trends and changes (automatically aggregates and computes CI)
- `relplot()` - Figure-level interface with automatic faceting

**Key parameters:**
- `x`, `y` - Primary variables
- `hue` - Color encoding for additional categorical/continuous variable
- `size` - Point/line size encoding
- `style` - Marker/line style encoding
- `col`, `row` - Facet into multiple subplots (figure-level only)

```python
# Scatter with multiple semantic mappings
import seaborn as sns
df = sns.load_dataset('tips')
sns.scatterplot(data=df, x='total_bill', y='tip',
                hue='time', size='size', style='sex')

# Line plot with confidence intervals
#sns.lineplot(data=timeseries, x='date', y='value', hue='category') #Requires timeseries dataframe
#plt.show() #Add if there is no background plot.

# Faceted relational plot
sns.relplot(data=df, x='total_bill', y='tip',
            col='time', row='sex', hue='smoker', kind='scatter')
```

### Distribution Plots (Single and Bivariate Distributions)

**Use for:** Understanding data spread, shape, and probability density

- `histplot()` - Bar-based frequency distributions with flexible binning
- `kdeplot()` - Smooth density estimates using Gaussian kernels
- `ecdfplot()` - Empirical cumulative distribution (no parameters to tune)
- `rugplot()` - Individual observation tick marks
- `displot()` - Figure-level interface for univariate and bivariate distributions
- `jointplot()` - Bivariate plot with marginal distributions
- `pairplot()` - Matrix of pairwise relationships across dataset

**Key parameters:**
- `x`, `y` - Variables (y optional for univariate)
- `hue` - Separate distributions by category
- `stat` - Normalization: "count", "frequency", "probability", "density"
- `bins` / `binwidth` - Histogram binning control
- `bw_adjust` - KDE bandwidth multiplier (higher = smoother)
- `fill` - Fill area under curve
- `multiple` - How to handle hue: "layer", "stack", "dodge", "fill"

```python
# Histogram with density normalization
import seaborn as sns
df = sns.load_dataset('tips')
sns.histplot(data=df, x='total_bill', hue='time',
             stat='density', multiple='stack')

# Bivariate KDE with contours
sns.kdeplot(data=df, x='total_bill', y='tip',
            fill=True, levels=5, thresh=0.1)

# Joint plot with marginals
sns.jointplot(data=df, x='total_bill', y='tip',
              kind='scatter', hue='time')

# Pairwise relationships
df = sns.load_dataset('iris')
sns.pairplot(data=df, hue='species', corner=True)
```

### Categorical Plots (Comparisons Across Categories)

**Use for:** Comparing distributions or statistics across discrete categories

**Categorical scatterplots:**
- `stripplot()` - Points with jitter to show all observations
- `swarmplot()` - Non-overlapping points (beeswarm algorithm)

**Distribution comparisons:**
- `boxplot()` - Quartiles and outliers
- `violinplot()` - KDE + quartile information
- `boxenplot()` - Enhanced boxplot for larger datasets

**Statistical estimates:**
- `barplot()` - Mean/aggregate with confidence intervals
- `pointplot()` - Point estimates with connecting lines
- `countplot()` - Count of observations per category

**Figure-level:**
- `catplot()` - Faceted categorical plots (set `kind` parameter)

**Key parameters:**
- `x`, `y` - Variables (one typically categorical)
- `hue` - Additional categorical grouping
- `order`, `hue_order` - Control category ordering
- `dodge` - Separate hue levels side-by-side
- `orient` - "v" (vertical) or "h" (horizontal)
- `kind` - Plot type for catplot: "strip", "swarm", "box", "violin", "bar", "point"

```python
# Swarm plot showing all points
import seaborn as sns
df = sns.load_dataset('tips')
sns.swarmplot(data=df, x='day', y='total_bill', hue='sex')

# Violin plot with split for comparison
sns.violinplot(data=df, x='day', y='total_bill',
               hue='sex', split=True)

# Bar plot with error bars
sns.barplot(data=df, x='day', y='total_bill',
            hue='sex', estimator='mean', errorbar='ci')

# Faceted categorical plot
sns.catplot(data=df, x='day', y='total_bill',
            col='time', kind='box')
```

### Regression Plots (Linear Relationships)

**Use for:** Visualizing linear regressions and residuals

- `regplot()` - Axes-level regression plot with scatter + fit line
- `lmplot()` - Figure-level with faceting support
- `residplot()` - Residual plot for assessing model fit

**Key parameters:**
- `x`, `y` - Variables to regress
- `order` - Polynomial regression order
- `logistic` - Fit logistic regression
- `robust` - Use robust regression (less sensitive to outliers)
- `ci` - Confidence interval width (default 95)
- `scatter_kws`, `line_kws` - Customize scatter and line properties

```python
# Simple linear regression
import seaborn as sns
df = sns.load_dataset('tips')
sns.regplot(data=df, x='total_bill', y='tip')

# Polynomial regression with faceting
sns.lmplot(data=df, x='total_bill', y='tip',
           col='time', order=2, ci=95)

# Check residuals
sns.residplot(data=df, x='total_bill', y='tip')
```

### Matrix Plots (Rectangular Data)

**Use for:** Visualizing matrices, correlations, and grid-structured data

- `heatmap()` - Color-encoded matrix with annotations
- `clustermap()` - Hierarchically-clustered heatmap

**Key parameters:**
- `data` - 2D rectangular dataset (DataFrame or array)
- `annot` - Display values in cells
- `fmt` - Format string for annotations (e.g., ".2f")
- `cmap` - Colormap name
- `center` - Value at colormap center (for diverging colormaps)
- `vmin`, `vmax` - Color scale limits
- `square` - Force square cells
- `linewidths` - Gap between cells

```python
# Correlation heatmap
import seaborn as sns
df = sns.load_dataset('tips')
corr = df.corr(numeric_only = True)
sns.heatmap(corr, annot=True, fmt='.2f',
            cmap='coolwarm', center=0, square=True)

# Clustered heatmap
#data = df.pivot_table(values='tip', index='size', columns='time')
#sns.clustermap(data, cmap='viridis',
#               standard_scale=1, figsize=(10, 10)) # Requires a pivot table
```

## Multi-Plot Grids

Seaborn provides grid objects for creating complex multi-panel figures:

### FacetGrid

Create subplots based on categorical variables. Most useful when called through figure-level functions (`relplot`, `displot`, `catplot`), but can be used directly for custom plots.

```python
import seaborn as sns
df = sns.load_dataset('tips')
g = sns.FacetGrid(df, col='time', row='sex', hue='smoker')
g.map(sns.scatterplot, 'total_bill', 'tip')
g.add_legend()
```

### PairGrid

Show pairwise relationships between all variables in a dataset.

```python
import seaborn as sns
df = sns.load_dataset('iris')
g = sns.PairGrid(df, hue='species')
g.map_upper(sns.scatterplot)
g.map_lower(sns.kdeplot)
g.map_diag(sns.histplot)
g.add_legend()
```

### JointGrid

Combine bivariate plot with marginal distributions.

```python
import seaborn as sns
df = sns.load_dataset('tips')
g = sns.JointGrid(data=df, x='total_bill', y='tip')
g.plot_joint(sns.scatterplot)
g.plot_marginals(sns.histplot)
```

## Figure-Level vs Axes-Level Functions

Understanding this distinction is crucial for effective seaborn usage:

### Axes-Level Functions
- Plot to a single matplotlib `Axes` object
- Integrate easily into complex matplotlib figures
- Accept `ax=` parameter for precise placement
- Return `Axes` object
- Examples: `scatterplot`, `histplot`, `boxplot`, `regplot`, `heatmap`

**When to use:**
- Building custom multi-plot layouts
- Combining different plot types
- Need matplotlib-level control
- Integrating with existing matplotlib code

```python
import matplotlib.pyplot as plt
import seaborn as sns
df = sns.load_dataset('iris')
fig, axes = plt.subplots(2, 2, figsize=(10, 10))
sns.scatterplot(data=df, x='sepal_length', y='sepal_width', ax=axes[0, 0])
sns.histplot(data=df, x='sepal_length', ax=axes[0, 1])
sns.boxplot(data=df, x='species', y='sepal_length', ax=axes[1, 0])
sns.kdeplot(data=df, x='sepal_length', y='sepal_width', ax=axes[1, 1])
```

### Figure-Level Functions
- Manage entire figure including all subplots
- Built-in faceting via `col` and `row` parameters
- Return `FacetGrid`, `JointGrid`, or `PairGrid` objects
- Use `height` and `aspect` for sizing (per subplot)
- Cannot be placed in existing figure
- Examples: `relplot`, `displot`, `catplot`, `lmplot`, `jointplot`, `pairplot`

**When to use:**
- Faceted visualizations (small multiples)
- Quick exploratory analysis
- Consistent multi-panel layouts
- Don't need to combine with other plot types

```python
# Automatic faceting
import seaborn as sns
df = sns.load_dataset('tips')
sns.relplot(data=df, x='total_bill', y='tip', col='time', row='sex',
            hue='smoker', height=3, aspect=1.2)
```

## Data Structure Requirements

### Long-Form Data (Preferred)

Each variable is a column, each observation is a row. This "tidy" format provides maximum flexibility:

```python
# Long-form structure
import pandas as pd
data = {'subject': [1, 1, 2, 2],
        'condition': ['control', 'treatment', 'control', 'treatment'],
        'measurement': [10.5, 12.3, 9.8, 13.1]}
df = pd.DataFrame(data)

print(df)
```

**Advantages:**
- Works with all seaborn functions
- Easy to remap variables to visual properties
- Supports arbitrary complexity
- Natural for DataFrame operations

### Wide-Form Data

Variables are spread across columns. Useful for simple rectangular data:

```python
# Wide-form structure
import pandas as pd

data = {'control': [10.5, 9.8], 'treatment': [12.3, 13.1]}
df = pd.DataFrame(data)

print(df)
```

**Use cases:**
- Simple time series
- Correlation matrices
- Heatmaps
- Quick plots of array data

**Converting wide to long:**
```python
import pandas as pd
data = {'control': [10.5, 9.8], 'treatment': [12.3, 13.1]}
df = pd.DataFrame(data)

df_long = df.melt(var_name='condition', value_name='measurement')
print(df_long)
```

## Color Palettes

Seaborn provides carefully designed color palettes for different data types:

### Qualitative Palettes (Categorical Data)

Distinguish categories through hue variation:
- `"deep"` - Default, vivid colors
- `"muted"` - Softer, less saturated
- `"pastel"` - Light, desaturated
- `"bright"` - Highly saturated
- `"dark"` - Dark values
- `"colorblind"` - Safe for color vision deficiency

```python
import seaborn as sns
sns.set_palette("colorblind")
sns.color_palette("Set2")
```

### Sequential Palettes (Ordered Data)

Show progression from low to high values:
- `"rocket"`, `"mako"` - Wide luminance range (good for heatmaps)
- `"flare"`, `"crest"` - Restricted luminance (good for points/lines)
- `"viridis"`, `"magma"`, `"plasma"` - Matplotlib perceptually uniform

```python
import seaborn as sns
import pandas as pd
import numpy as np
data = np.random.rand(10,10)
sns.heatmap(data, cmap='rocket')
#sns.kdeplot(data=df, x='x', y='y', cmap='mako', fill=True) #Requires dataframe
```

### Diverging Palettes (Centered Data)

Emphasize deviations from a midpoint:
- `"vlag"` - Blue to red
- `"icefire"` - Blue to orange
- `"coolwarm"` - Cool to warm
- `"Spectral"` - Rainbow diverging

```python
import seaborn as sns
import pandas as pd
import numpy as np
data = np.random.rand(10,10)
correlation_matrix = np.corrcoef(data)
sns.heatmap(correlation_matrix, cmap='vlag', center=0)
```

### Custom Palettes

```python
import seaborn as sns
# Create custom palette
custom = sns.color_palette("husl", 8)

# Light to dark gradient
palette = sns.light_palette("seagreen", as_cmap=True)

# Diverging palette from hues
palette = sns.diverging_palette(250, 10, as_cmap=True)
```

## Theming and Aesthetics

### Set Theme

`set_theme()` controls overall appearance:

```python
# Set complete theme
import seaborn as sns
sns.set_theme(style='whitegrid', palette='pastel', font='sans-serif')

# Reset to defaults
sns.set_theme()
```

### Styles

Control background and grid appearance:
- `"darkgrid"` - Gray background with white grid (default)
- `"whitegrid"` - White background with gray grid
- `"dark"` - Gray background, no grid
- `"white"` - White background, no grid
- `"ticks"` - White background with axis ticks

```python
import seaborn as sns
sns.set_style("whitegrid")

# Remove spines
sns.despine(left=False, bottom=False, offset=10, trim=True)

# Temporary style
with sns.axes_style("white"):
    import matplotlib.pyplot as plt
    df = sns.load_dataset('iris')
    sns.scatterplot(data=df, x='sepal_length', y='sepal_width')
    plt.show()
```

### Contexts

Scale elements for different use cases:
- `"paper"` - Smallest (default)
- `"notebook"` - Slightly larger
- `"talk"` - Presentation slides
- `"poster"` - Large format

```python
import seaborn as sns
sns.set_context("talk", font_scale=1.2)

# Temporary context
with sns.plotting_context("poster"):
    import matplotlib.pyplot as plt
    df = sns.load_dataset('iris')
    sns.barplot(data=df, x='species', y='sepal_length')
    plt.show()
```

## Best Practices

### 1. Data Preparation

Always use well-structured DataFrames with meaningful column names:

```python
# Good: Named columns in DataFrame
import pandas as pd
import seaborn as sns
bills = [10, 20, 30]
tips = [1, 2, 3]
days = ['Mon', 'Tue', 'Wed']
df = pd.DataFrame({'bill': bills, 'tip': tips, 'day': days})
sns.scatterplot(data=df, x='bill', y='tip', hue='day')

# Avoid: Unnamed arrays
#sns.scatterplot(x=x_array, y=y_array)  # Loses axis labels #Requires x_array and y_array.
```

### 2. Choose the Right Plot Type

**Continuous x, continuous y:** `scatterplot`, `lineplot`, `kdeplot`, `regplot`
**Continuous x, categorical y:** `violinplot`, `boxplot`, `stripplot`, `swarmplot`
**One continuous variable:** `histplot`, `kdeplot`, `ecdfplot`
**Correlations/matrices:** `heatmap`, `clustermap`
**Pairwise relationships:** `pairplot`, `jointplot`

### 3. Use Figure-Level Functions for Faceting

```python
# Instead of manual subplot creation
import seaborn as sns
df = sns.load_dataset('tips')
sns.relplot(data=df, x='total_bill', y='tip', col='time', col_wrap=3)

# Not: Creating subplots manually for simple faceting
```

### 4. Leverage Semantic Mappings

Use `hue`, `size`, and `style` to encode additional dimensions:

```python
import seaborn as sns
df = sns.load_dataset('tips')
sns.scatterplot(data=df, x='total_bill', y='tip',
                hue='time',      # Color by category
                size='size',    # Size by continuous variable
                style='sex')         # Marker style by type
```

### 5. Control Statistical Estimation

Many functions compute statistics automatically. Understand and customize:

```python
import seaborn as sns
import pandas as pd
# Lineplot computes mean and 95% CI by default
data = {'time': [1,2,3,1,2,3], 'value':[4,5,6,7,8,9]}
df = pd.DataFrame(data)
sns.lineplot(data=df, x='time', y='value',
             errorbar='sd')  # Use standard deviation instead

# Barplot computes mean by default
sns.barplot(data=df, x='time', y='value',
            estimator='median',  # Use median instead
            errorbar=('ci', 95))  # Bootstrapped CI
```

### 6. Combine with Matplotlib

Seaborn integrates seamlessly with matplotlib for fine-tuning:

```python
import seaborn as sns
import matplotlib.pyplot as plt
df = sns.load_dataset('iris')
ax = sns.scatterplot(data=df, x='sepal_length', y='sepal_width')
ax.set(xlabel='Custom X Label', ylabel='Custom Y Label',
       title='Custom Title')
ax.axhline(y=0, color='r', linestyle='--')
plt.tight_layout()
```

### 7. Save High-Quality Figures

```python
import seaborn as sns
df = sns.load_dataset('iris')
fig = sns.relplot(data=df, x='sepal_length', y='sepal_width', col='species')
fig.savefig('figure.png', dpi=300, bbox_inches='tight')
fig.savefig('figure.pdf')  # Vector format for publications
```

## Common Patterns

### Exploratory Data Analysis

```python
import seaborn as sns
df = sns.load_dataset('iris')
# Quick overview of all relationships
sns.pairplot(data=df, hue='species', corner=True)

# Distribution exploration
sns.displot(data=df, x='sepal_length', hue='species',
            kind='kde', fill=True, col='species')

# Correlation analysis
corr = df.corr(numeric_only = True)
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
```

### Publication-Quality Figures

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
sns.set_theme(style='ticks', context='paper', font_scale=1.1)
data = {'treatment': ['A', 'B', 'A', 'B'],
        'response': [10, 12, 15, 18],
        'cell_line': ['X', 'X', 'Y', 'Y']}

df = pd.DataFrame(data)

g = sns.catplot(data=df, x='treatment', y='response',
                col='cell_line', kind='box', height=3, aspect=1.2)
g.set_axis_labels('Treatment Condition', 'Response (μM)')
g.set_titles('{col_name}')
sns.despine(trim=True)

g.savefig('figure.pdf', dpi=300, bbox_inches='tight')
plt.show()
```

### Complex Multi-Panel Figures

```python
# Using matplotlib subplots with seaborn
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

data = {'x1': [1, 2, 3, 1, 2, 3],
        'x2': [4, 5, 6, 4, 5, 6],
        'y': [7, 8, 9, 10, 11, 12],
        'group': ['A', 'A', 'A', 'B', 'B', 'B']}

df = pd.DataFrame(data)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

sns.scatterplot(data=df, x='x1', y='y', hue='group', ax=axes[0, 0])
sns.histplot(data=df, x='x1', hue='group', ax=axes[0, 1])
sns.violinplot(data=df, x='group', y='y', ax=axes[1, 0])
import numpy as np
pivot_data = df.pivot_table(values='y', index='x1', columns='x2')
sns.heatmap(pivot_data,
            ax=axes[1, 1], cmap='viridis')

plt.tight_layout()
```

### Time Series with Confidence Bands

```python
import seaborn as sns
import pandas as pd

# Lineplot automatically aggregates and shows CI
data = {'date': [1, 2, 3, 1, 2, 3],
        'measurement': [4, 5, 6, 7, 8, 9],
        'sensor': ['A', 'A', 'A', 'B', 'B', 'B'],
        'location': ['X', 'X', 'X', 'Y', 'Y', 'Y']}

timeseries = pd.DataFrame(data)
sns.lineplot(data=timeseries, x='date', y='measurement',
             hue='sensor', style='location', errorbar='sd')

# For more control
g = sns.relplot(data=timeseries, x='date', y='measurement',
                col='location', hue='sensor', kind='line',
                height=4, aspect=1.5, errorbar=('ci', 95))
g.set_axis_labels('Date', 'Measurement (units)')
```

## Troubleshooting

### Issue: Legend Outside Plot Area

Figure-level functions place legends outside by default. To move inside:

```python
import seaborn as sns
df = sns.load_dataset('iris')
g = sns.relplot(data=df, x='sepal_length', y='sepal_width', hue='species')
g._legend.set_bbox_to_anchor((0.9, 0.5))  # Adjust position
```

### Issue: Overlapping Labels

```python
import matplotlib.pyplot as plt
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
```

### Issue: Figure Too Small

For figure-level functions:
```python
import seaborn as sns
df = sns.load_dataset('iris')
sns.relplot(data=df, x='sepal_length', y='sepal_width', height=6, aspect=1.5)
```

For axes-level functions:
```python
import matplotlib.pyplot as plt
import seaborn as sns
df = sns.load_dataset('iris')
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='sepal_length', y='sepal_width', ax=ax)
```

### Issue: Colors Not Distinct Enough

```python
import seaborn as sns
df = sns.load_dataset('iris')
# Use a different palette
sns.set_palette("bright")

# Or specify number of colors
palette = sns.color_palette("husl", n_colors=len(df['species'].unique()))
sns.scatterplot(data=df, x='sepal_length', y='sepal_width', hue='species', palette=palette)
```

### Issue: KDE Too Smooth or Jagged

```python
import seaborn as sns
df = sns.load_dataset('iris')
# Adjust bandwidth
sns.kdeplot(data=df, x='sepal_length', bw_adjust=0.5)  # Less smooth
sns.kdeplot(data=df, x='sepal_length', bw_adjust=2)    # More smooth
```

## Example Usage

```python
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    # Built-in example dataset (requires internet on first use in some environments)
    df = sns.load_dataset("tips")

    sns.set_theme(style="whitegrid", palette="colorblind")

    # 1) Relationship exploration with semantic mapping
    ax = sns.scatterplot(
        data=df,
        x="total_bill",
        y="tip",
        hue="day",
        style="sex",
        size="size",
        sizes=(30, 200),
        alpha=0.8,
    )
    ax.set(title="Tips: Total Bill vs Tip", xlabel="Total bill ($)", ylabel="Tip ($)")
    plt.tight_layout()
    plt.show()

    # 2) Faceted categorical comparison (figure-level)
    g = sns.catplot(
        data=df,
        x="day",
        y="total_bill",
        col="time",
        kind="violin",
        inner="quartile",
        height=3.5,
        aspect=1.1,
    )
    g.set_axis_labels("Day", "Total bill ($)")
    g.set_titles("{col_name}")
    plt.tight_layout()
    plt.show()

    # 3) Correlation heatmap (matrix plot)
    corr = df.select_dtypes("number").corr(numeric_only=True)
    plt.figure(figsize=(5.5, 4.5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True)
    plt.title("Numeric Correlations (tips)")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

## Implementation Details

- **Axes-level vs Figure-level**
  - *Axes-level* (e.g., `scatterplot`, `histplot`, `boxplot`, `regplot`, `heatmap`) draw onto one matplotlib `Axes`, accept `ax=`, and are best for custom subplot grids.
  - *Figure-level* (e.g., `relplot`, `displot`, `catplot`, `lmplot`, `jointplot`, `pairplot`) manage the full figure and faceting; they return Grid objects (e.g., `FacetGrid`, `JointGrid`, `PairGrid`) and are not designed to be embedded into an existing matplotlib figure.

- **Data shape expectations**
  - Prefer **long-form (tidy)** data: one column per variable, one row per observation. This maximizes compatibility with semantic mappings and faceting.
  - **Wide-form** data is supported for some plots (notably matrix-like inputs such as heatmaps), but may require reshaping via `pandas.melt()` for general-purpose plotting.

- **Statistical estimation controls**
  - Many functions compute summaries automatically (e.g., `lineplot` aggregates and can display uncertainty bands; `barplot` estimates a central tendency with error bars).
  - Key parameters to control estimation/uncertainty include `estimator=`, `errorbar=` (or legacy `ci=`), and for KDE smoothing `bw_adjust=`.

- **Distribution and smoothing parameters**
  - Histograms: `bins=` / `binwidth=`, `stat=` (`"count"`, `"frequency"`, `"probability"`, `"density"`), and `multiple=` for hue handling (`"layer"`, `"stack"`, `"dodge"`, `"fill"`).
  - KDE: `bw_adjust` (higher = smoother), `fill=True`, `levels=` for contour density plots.

- **Color and theme system**
  - Palettes: qualitative (categorical), sequential (ordered), diverging (centered at a reference via `center=` in heatmaps).
  - Global styling: `sns.set_theme(style=..., context=..., palette=...)`; use matplotlib calls for final layout (`plt.tight_layout()`) and export (`savefig(dpi=300, bbox_inches="tight")`).

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

## Deterministic Output Rules

- Use the same section order for every supported request of this skill.
- Keep output field names stable and do not rename documented keys across examples.
- If a value is unavailable, emit an explicit placeholder instead of omitting the field.

## Output Contract

- Return a structured deliverable that is directly usable without reformatting.
- If a file is produced, prefer a deterministic output name such as `seaborn_result.md` unless the skill documentation defines a better convention.
- Include a short validation summary describing what was checked, what assumptions were made, and any remaining limitations.

## Validation and Safety Rules

- Validate required inputs before execution and stop early when mandatory fields or files are missing.
- Do not fabricate measurements, references, findings, or conclusions that are not supported by the provided source material.