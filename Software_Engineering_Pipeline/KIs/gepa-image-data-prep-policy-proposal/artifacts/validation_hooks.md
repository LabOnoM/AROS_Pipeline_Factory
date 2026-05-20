# GEPA Error Prevention Rule for Scientific Pipeline Integrity Policy

**Rule ID:** `GEPA-Rule-SciPipe-001: Holistic Pipeline Integrity Audit`

**Applies to:** `Scientific Computing Pipeline Review`, `Codebase Audit`, `Reproducibility Analysis` Policy

**Principle:** This KI provides a "shift-left" framework for building reliable, reproducible, and correct scientific computing pipelines. It should be used as a guide during development, not just as a checklist for final audits. By integrating these checks and patterns early, we prevent silent failures, data corruption, and reproducibility crises by adhering to the "Defense in Depth" GEPA principle.

### 1. The Hierarchy of Verification

A comprehensive pipeline audit must perform checks at three distinct levels, moving from static analysis to runtime validation. A failure at a lower level often invalidates any checks at a higher level.

1.  **Level 1: Static Code & Configuration Analysis:** Verifying the project's structure and code without execution. **Fix these first.**
2.  **Level 2: Data Flow & Format Integrity:** Verifying the data itself and its handling between pipeline stages. **Critical for preventing data loss.**
3.  **Level 3: Execution & Runtime Validation:** Verifying the correctness and quality of the pipeline's outputs. **Ensures scientific validity.**

### 2. Audit Conditions & Implementation Patterns

---

#### **Level 1: Static Code & Configuration Assertions**

These conditions ensure the project is well-configured, portable, and free of latent errors.

##### 1.1 Code Portability & Syntax

*   **Rationale:** Code that runs correctly within a Jupyter notebook cell can fail when executed as a `.py` script due to subtle parsing differences (e.g., IPython vs. standard Python interpreter). This is a common and critical portability failure.
*   **Verification & Tooling:** Always validate Python scripts for syntax errors without a full run. This is a perfect candidate for a pre-commit hook.
    ```bash
    # This command will check all .py files in the current directory and subdirectories
    find . -type f -name "*.py" -exec python -m py_compile {} +
    ```
*   **Best Practices & Implementation:**
    *   Avoid multi-statement lines using escaped newlines (`\n`) in your source code, as seen in the trace (`cropped_cells = {}\n    tracks = data['tracks']`).
    *   For projects that require both notebook and script formats, use a tool like `jupytext` to maintain a synchronized `.py` version of your `.ipynb` file, which can then be linted and tested in a standard CI/CD pipeline.

##### 1.2 Environment Consistency

*   **Rationale:** Mismatches between environment files (`environment.yml`), documentation (`README.md`), and notebook kernel metadata (`.ipynb` JSON) are a primary cause of "works on my machine" syndromes.
*   **Verification & Tooling:** Programmatically check that the notebook's kernel display name matches the environment name.
    ```bash
    # Requires 'jq' to be installed
    # Usage: ./check_kernel.sh my_notebook.ipynb iss-imaging
    NOTEBOOK_KERNEL_NAME=$(jq -r '.metadata.kernelspec.display_name' "$1")
    EXPECTED_ENV_NAME="$2"

    if [ "$NOTEBOOK_KERNEL_NAME" != "$EXPECTED_ENV_NAME" ]; then
      echo "FAIL: Kernel name mismatch in $1. Found '$NOTEBOOK_KERNEL_NAME', expected '$EXPECTED_ENV_NAME'."
      exit 1
    else
      echo "PASS: Kernel name in $1 matches '$EXPECTED_ENV_NAME'."
    fi
    ```
*   **Best Practices & Implementation:** Define a single, canonical environment name for the project (e.g., `iss-imaging`). Ensure this name is used consistently in `environment.yml`, the `README.md`, and is set as the `display_name` within the `kernelspec` of all `.ipynb` files.

##### 1.3 Portable Path Management

*   **Rationale:** Hardcoded absolute paths (e.g., `[WORKSPACE_ROOT]/...`, `C:\Users\...`) guarantee failure on any other machine. All paths must be relative or derived from environment variables.
*   **Verification & Tooling:** Use `grep` to scan for common absolute path patterns.
    ```bash
    # Scans for paths starting with '/', 'C:', 'D:', or a home tilde '~'
    grep -rE '(^|[^a-zA-Z])(/|~|[C-Z]:\\)' . --include='*.{py,ijm,sh,md}'
    ```
*   **Best Practices & Implementation:** Use Python's `pathlib` library to manage paths relative to the script's location or a well-defined project root.

    ```python
    # Bad: Hardcoded absolute path
    # DATA_DIR = "[WORKSPACE_ROOT]/data"

    # Good: Relative path using pathlib
    from pathlib import Path

    # Defines project root as the parent directory of the script's directory
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    DATA_DIR = PROJECT_ROOT / "data"
    RESULTS_DIR = PROJECT_ROOT / "results"

    print(f"Using data from: {DATA_DIR}")
    ```

##### 1.4 Version Control Hygiene

*   **Rationale:** Raw data, large models, environment caches, and intermediate files must be excluded from Git to keep the repository lightweight and portable.
*   **Verification & Tooling:** Ensure a `.gitignore` file exists and is not empty. Check for large, unignored files in the repository status.
*   **Best Practices & Implementation:** Use a comprehensive `.gitignore` template for scientific projects. Store large data/model files in a dedicated object storage service (e.g., S3, Artifactory) and reference them by ID or URL in the repository.

    ```gitignore
    # .gitignore for a Python Scientific Computing Project

    # Data and Results
    data/
    results/
    output/
    figures/
    *.npz
    *.h5
    *.tif
    *.tiff

    # Python environments and caches
    .env
    .venv
    env/
    venv/
    __pycache__/
    *.pyc

    # IDE and OS files
    .vscode/
    .idea/
    .DS_Store
    ```

---

#### **Level 2: Data Flow & Format Integrity Assertions**

##### 2.1 Awareness of Data Format Limitations

*   **Rationale:** Many file formats have silent failure modes. For example, the standard TIFF format has a 4GB size limit. Writing data beyond this limit causes silent truncation (data loss) without a fatal error, corrupting all downstream results.
*   **Verification & Tooling:** During code review, inspect file-writing operations. For TIFF files, check if the library call includes an option for "BigTIFF" when file sizes are expected to be large.
*   **Best Practices & Implementation:** When saving large image stacks (>2GB) with Python's `tifffile` library, explicitly enable the BigTIFF format. For extremely large datasets, consider more scalable formats like Zarr or HDF5.
    ```python
    import tifffile
    import numpy as np

    # Assume large_image_stack is a NumPy array > 4GB
    large_image_stack = np.zeros((1024, 1024, 4000), dtype=np.uint16) # ~8GB

    # Bad: Prone to silent truncation
    # tifffile.imwrite('output.tif', large_image_stack, imagej=True)

    # Good: Explicitly uses BigTIFF format, preventing truncation
    tifffile.imwrite('output_safe.tif', large_image_stack, imagej=True, bigtiff=True)
    ```

##### 2.2 Output Directory Hygiene

*   **Rationale:** Leaving old test outputs, temporary files, or experimental runs in the main results directory creates ambiguity and risks the accidental use of incorrect data in downstream analysis.
*   **Verification & Tooling:** The output directory structure should be predictable. Write a simple utility script to list the contents of the `results/` directory and flag any unexpected files or folders that don't match the expected final output pattern.
*   **Best Practices & Implementation:**
    *   Structure your project with clear separation: `results/final/` for production outputs and `results/tmp/` or a separate `scratch/` directory for experiments.
    *   Use `.gitignore` to explicitly ignore the temporary/scratch directories.
    *   Consider adding a "cleanup" step or function at the beginning of a pipeline run to archive old results or clear temporary directories.

---

#### **Level 3: Execution & Runtime Validation Assertions**

##### 3.1 Quantitative Quality Control (QC)

*   **Rationale:** Without objective metrics, assessing algorithm performance is subjective. Metrics provide auditable proof of performance and guard against silent regressions.
*   **Verification & Tooling:** Check for the presence of a `qc/` directory or summary files (e.g., `results.csv`, `qc_metrics.json`) containing quality scores.
*   **Best Practices & Implementation:** For image-to-image tasks like denoising, calculate standard metrics and log them.

    ```python
    from skimage.metrics import peak_signal_to_noise_ratio as psnr
    from skimage.metrics import structural_similarity as ssim
    import pandas as pd

    # Assume ground_truth and denoised_image are NumPy arrays
    psnr_score = psnr(ground_truth, denoised_image, data_range=denoised_image.max() - denoised_image.min())
    ssim_score = ssim(ground_truth, denoised_image, data_range=denoised_image.max() - denoised_image.min())

    print(f"PSNR: {psnr_score:.2f}, SSIM: {ssim_score:.3f}")

    # Log to a CSV file
    qc_data = pd.DataFrame([{'image_id': 'C1_RFP_01', 'psnr': psnr_score, 'ssim': ssim_score}])
    qc_data.to_csv('results/qc_metrics.csv', mode='a', header=False, index=False)
    ```

##### 3.2 Qualitative Quality Control (QC)

*   **Rationale:** Metrics alone can be misleading. Visual checks are essential for sanity-checking outputs and catching unexpected artifacts that metrics might miss.
*   **Verification & Tooling:** Ensure the pipeline saves visual artifacts (images, plots) to a dedicated and predictable location like `results/qc_plots/`.
*   **Best Practices & Implementation:** Generate and save side-by-side or overlay comparisons of "before" and "after" images.

    ```python
    import matplotlib.pyplot as plt

    # Assume raw_patch and denoised_patch are 2D image slices
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(raw_patch, cmap='gray')
    axes[0].set_title('Raw Input')
    axes[1].imshow(denoised_patch, cmap='gray')
    axes[1].set_title(f'Denoised Output (PSNR: {psnr_score:.2f})')

    # Save the figure to a dedicated QC directory
    output_path = Path("results/qc_plots/comparison_C1_RFP_01.png")
    output_path.parent.mkdir(parents=True, exist_ok=True) # Ensure directory exists
    plt.savefig(output_path)
    plt.close(fig) # Close figure to free memory
    ```