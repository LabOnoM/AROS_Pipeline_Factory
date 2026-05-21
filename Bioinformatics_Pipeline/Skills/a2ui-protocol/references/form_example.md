# A2UI Interactive Form Example

This is a complete, working A2UI JSON that creates an interactive bioinformatics plot configuration form. It demonstrates TextField, MultipleChoice, CheckBox, Button with data binding and action handling.

## The JSON Messages

```json
[
  {"surfaceId": "default", "surfaceUpdate": {"components": [
    {
      "id": "root",
      "component": {
        "Column": {
          "children": {
            "explicitList": [
              "title",
              "datasetNameField",
              "plotTypeField",
              "geneListField",
              "clusteringCheckBox",
              "colorSchemeField",
              "generateButton",
              "generateButtonText",
              "outputPlot"
            ]
          },
          "distribution": "start",
          "alignment": "stretch"
        }
      }
    },
    {
      "id": "title",
      "component": {
        "Text": {
          "text": {"literalString": "Bioinformatics Plot Generation Agent"},
          "usageHint": "h2"
        }
      }
    },
    {
      "id": "datasetNameField",
      "component": {
        "TextField": {
          "label": {"literalString": "Dataset Name"},
          "text": {"path": "/form/datasetName"},
          "textFieldType": "shortText"
        }
      }
    },
    {
      "id": "plotTypeField",
      "component": {
        "MultipleChoice": {
          "selections": {"path": "/form/plotType"},
          "options": [
            {"label": {"literalString": "Heatmap"}, "value": "heatmap"},
            {"label": {"literalString": "PCA"}, "value": "pca"},
            {"label": {"literalString": "Volcano Plot"}, "value": "volcano"},
            {"label": {"literalString": "Box Plot"}, "value": "boxplot"}
          ],
          "maxAllowedSelections": 1
        }
      }
    },
    {
      "id": "geneListField",
      "component": {
        "TextField": {
          "label": {"literalString": "Gene List (comma-separated)"},
          "text": {"path": "/form/geneList"},
          "textFieldType": "longText"
        }
      }
    },
    {
      "id": "clusteringCheckBox",
      "component": {
        "CheckBox": {
          "label": {"literalString": "Enable Clustering"},
          "value": {"path": "/form/clustering"}
        }
      }
    },
    {
      "id": "colorSchemeField",
      "component": {
        "MultipleChoice": {
          "selections": {"path": "/form/colorScheme"},
          "options": [
            {"label": {"literalString": "Viridis"}, "value": "viridis"},
            {"label": {"literalString": "Plasma"}, "value": "plasma"},
            {"label": {"literalString": "Magma"}, "value": "magma"},
            {"label": {"literalString": "Inferno"}, "value": "inferno"}
          ],
          "maxAllowedSelections": 1
        }
      }
    },
    {
      "id": "generateButton",
      "component": {
        "Button": {
          "child": "generateButtonText",
          "primary": true,
          "action": {
            "name": "generatePlot",
            "context": [
              {"key": "datasetName", "value": {"path": "/form/datasetName"}},
              {"key": "plotType", "value": {"path": "/form/plotType"}},
              {"key": "geneList", "value": {"path": "/form/geneList"}},
              {"key": "clustering", "value": {"path": "/form/clustering"}},
              {"key": "colorScheme", "value": {"path": "/form/colorScheme"}}
            ]
          }
        }
      }
    },
    {
      "id": "generateButtonText",
      "component": {
        "Text": {"text": {"literalString": "Generate Plot"}}
      }
    },
    {
      "id": "outputPlot",
      "component": {
        "Text": {
          "text": {"literalString": "Plot output will appear here after generation."},
          "usageHint": "caption"
        }
      }
    }
  ]}},
  {"surfaceId": "default", "beginRendering": {"root": "root"}}
]
```

## How It Works

1. **TextField** components bind to `/form/datasetName` and `/form/geneList` — user input is stored in the data model at those paths
2. **MultipleChoice** binds to `/form/plotType` and `/form/colorScheme` — selected values stored at those paths
3. **CheckBox** binds to `/form/clustering` — boolean stored at that path
4. **Button** action `generatePlot` reads all form values from the data model via `context` entries
5. When user clicks "Generate Plot", the client sends a `userAction` with all resolved form values

## Server-Side Action Handling

The agent receives the `userAction` and should:
1. Extract parameters from `context` (plotType, colorScheme, etc.)
2. Generate the plot server-side
3. Respond with new `surfaceUpdate` that replaces the `outputPlot` component with an Image showing the generated plot
