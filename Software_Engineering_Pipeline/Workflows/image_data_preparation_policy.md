### GEPA Error Prevention Rule: Atlas Mapping Pre-computation Verification

This rule is designed to prevent failures during the atlas mapping stage by verifying the integrity of its inputs. It mandates two specific validation hooks that must pass before the core mapping function (e.g., `brainglobe_heatmap.Heatmap`) is invoked.

---

### **1. Policy Objective**

To increase the first-attempt success rate of neuroanatomical visualization tasks by ensuring that image data is correctly loaded and slice parameters are valid *before* attempting to map them to an atlas. This prevents common errors such as out-of-bounds slicing, invalid orientation requests, and operations on null data.

### **2. Validation Hooks and Assertions**

The following two validation hooks are now mandatory components of the 'Image Data Preparation' workflow.

---

#### **Validation Hook 1: Post-Import Data Integrity Check**

This check MUST be executed immediately after the image import attempt and before any other processing steps.

*   **Trigger:** After an image volume (e.g., a NIfTI or TIFF stack) is loaded into memory.
*   **Assertions:**
    1.  **Data Object Non-Null:** The in-memory object representing the image data MUST NOT be `None` or `null`.
    2.  **Correct Dimensionality:** The data object (e.g., NumPy array) MUST have the expected number of dimensions (typically 3 for volumetric data).
    3.  **Positive Dimensions:** All dimension sizes of the data array MUST be greater than zero.

*   **Failure Action:** If any assertion fails, the workflow MUST halt immediately and report an "Image Import Failed" error, specifying which assertion was not met. The process MUST NOT proceed to slice positioning.

---

#### **Validation Hook 2: Pre-Mapping Slice Parameter Validation**

This check MUST be executed after the user or an upstream process defines the slice parameters but *before* these parameters are used to generate a 2D slice or map data to an atlas.

*   **Trigger:** Before calling the atlas mapping or heatmap generation function (e.g., `bgh.Heatmap(...)`).
*   **Assertions:**
    1.  **Position-in-Bounds:** The specified slice `position` (e.g., `(8000, 5000, 5000)` in microns) MUST be geographically within the boundaries of the loaded image volume's coordinate space. The agent must compare the position parameter against the dimensions of the image data object validated in Hook 1.
    2.  **Valid Orientation:** The `orientation` parameter MUST be one of the accepted values supported by the tool (e.g., "frontal", "sagittal", "horizontal") or a valid numerical vector if custom orientations are permitted.
    3.  **Valid Thickness:** The slice `thickness` parameter MUST be a positive numerical value.

*   **Failure Action:** If any assertion fails, the workflow MUST halt and report an "Invalid Slice Parameter" error, specifying which parameter is incorrect and why (e.g., "Position X is out-of-bounds", "Orientation not recognized"). The process MUST NOT proceed to atlas mapping.
