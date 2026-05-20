# R Script Templates for Bibliometrix

Use these R script templates as a baseline for creating execution scripts. Modify the file paths, database sources, and plot parameters based on the specific user request.

## 1. Load Data & Basic Summary

```R
library(bibliometrix)

# Specify the data file and its source format
# Supported dbsource: "wos", "scopus", "pubmed", "openalex", etc.
# Supported format: "plaintext", "bibtex", "csv", "excel"
file_path <- "insert_file_path_here"
M <- convert2df(file = file_path, dbsource = "wos", format = "plaintext")

# Calculate main bibliometric measures
results <- biblioAnalysis(M, sep = ";")

# Extract detailed summary
S <- summary(object = results, k = 10, pause = FALSE)

# Generate basic plots and save to PNG
png("basic_plots.png", width=800, height=800)
plot(x = results, k = 10, pause = FALSE)
dev.off()
```

## 2. Bibliographic Network Analysis (e.g., Collaboration)

```R
library(bibliometrix)

# Load data (assuming dataframe M exists)
M <- convert2df(file = "insert_file_path_here", dbsource = "wos", format = "plaintext")

# Create network matrix for Co-authorship
# analysis can be "collaboration", "co-occurrences", "co-citation", "coupling"
# network can be "authors", "universities", "countries", "keywords", "references", "sources"
NetMatrix <- biblioNetwork(M, analysis = "collaboration", network = "authors", sep = ";")

# Plot the network array
png("collaboration_network.png", width=1000, height=1000)
net <- networkPlot(NetMatrix, n = 30, Title = "Author Collaboration Network", type = "auto", size=T, edgesize = 5, labelsize=0.7)
dev.off()
```

## 3. Conceptual Structure (Thematic Map)

```R
library(bibliometrix)

M <- convert2df(file = "insert_file_path_here", dbsource = "scopus", format = "bibtex")

# Thematic map generation based on keywords (ID: Keywords Plus, DE: Author Keywords)
png("thematic_map.png", width=800, height=800)
Map <- thematicMap(M, field = "ID", n = 250, minfreq = 5, size = 0.5, repel = TRUE)
plot(Map$map)
dev.off()
```

## 4. Life Cycle Analysis

```R
library(bibliometrix)
library(dplyr)

M <- convert2df(file = "insert_file_path_here", dbsource = "wos", format = "plaintext")

# Perform life cycle analysis via logistic growth model
data <- M %>% group_by(PY) %>% count()
LC <- lifeCycle(data, forecast_years = 20, plot = FALSE, verbose = FALSE)

# Save growth curve plot
png("life_cycle_curve.png", width=800, height=600)
plot(LC$plot)
dev.off()

# Print growth metrics to console for the AI to interpret
print("Life Cycle Parameters:")
print(LC$parameters)
print("Life Cycle Metrics:")
print(LC$metrics)
```
