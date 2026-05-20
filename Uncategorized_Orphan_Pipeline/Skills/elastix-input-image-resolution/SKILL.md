---
name: elastix-input-image-resolution
description: Validates input image resolution for Elastix registration, ensuring reliable feature extraction.
license: MIT
skill-author: AROS_pipeline_engineer
status: beta
---
# Elastix Input Image Resolution

This skill ensures that input images for Elastix registration meet the minimum resolution requirements for reliable feature extraction and accurate registration.

## GEPA Error Prevention Rule: Input Image Resolution Check

To adhere to the GEPA principle of "Sub-task First-Attempt Success," this skill implements a mandatory pre-execution validation of input image dimensions. Images MUST be at least 1000x1000 pixels. If this criterion is not met, the task will halt immediately to prevent inefficient retries and unreliable registration outcomes.

### Implementation Details:

Before initiating any Elastix registration process, the following steps *MUST* be executed by the calling agent:

1.  **Identify Input Images**: Determine all image file paths designated for Elastix registration.
2.  **Validate Image Resolution**: For each identified input image, programmatically retrieve its dimensions (width and height).
    *   **Recommended Tool**: Python with the `Pillow` library (`PIL`).
    *   **Installation (if needed)**: `pip install Pillow`
    *   **Example Python Snippet for Resolution Check**:
        ```python
        from PIL import Image

        def check_image_resolution(image_path, min_width=1000, min_height=1000):
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    if width < min_width or height < min_height:
                        return False, f"Image '{image_path}' resolution ({width}x{height}) is below the required minimum ({min_width}x{min_height})."
                    return True, "Resolution check passed."
            except FileNotFoundError:
                return False, f"Error: Image file not found at '{image_path}'."
            except Exception as e:
                return False, f"Error processing image '{image_path}': {e}"

        # Example Usage:
        # image_file = "/path/to/your/input_image.tif"
        # passed, message = check_image_resolution(image_file)
        # if not passed:
        #     print(f"Validation Failed: {message}")
        #     # The agent MUST halt execution here.
        # else:
        #     print(f"Validation Passed: {message}")
        #     # Proceed with Elastix registration
        ```
3.  **Halt on Failure**: If any image fails the resolution check, the agent *MUST* halt the Elastix registration sub-task and report the specific failure message.

### Refusal Template for Low Resolution:

> "GEPA Validation Failed: Input image `[image_filepath]` has a resolution of `[width]x[height]` pixels, which is below the required minimum of 1000x1000 pixels for reliable Elastix registration. Please provide higher-resolution images."

## When to Use

-   Prior to initiating any image registration pipeline that uses Elastix.
-   As a pre-flight check for image analysis workflows requiring high-resolution inputs.
-   To ensure consistency and quality of input data in computational imaging tasks.

## Workflow

1.  Identify all input images for Elastix.
2.  Apply the `GEPA Error Prevention Rule: Input Image Resolution Check` for each image.
3.  If all checks pass, proceed with Elastix registration.
4.  If any check fails, halt execution and report the error using the refusal template.