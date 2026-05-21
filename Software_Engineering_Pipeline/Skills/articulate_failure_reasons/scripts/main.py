import argparse

def articulate_failure(exception: Exception, context: str, **kwargs) -> str:
    """
    Constructs a detailed failure report string from an exception, adhering to
    AROS agent communication policies.

    Args:
        exception: The exception object that was caught.
        context: A string describing the context in which the failure occurred
                 (e.g., 'accessing the file at /path/to/file').
        **kwargs: Additional key-value pairs to include in the report
                  (e.g., api_endpoint, parameters).

    Returns:
        A detailed, specific failure report string.
    """
    error_type = type(exception).__name__
    error_message = str(exception)
    
    # Build the report with specific details, as per GEPA rules.
    report = f"Operation failed. Context: {context}. "
    report += f"Reason: [{error_type}] {error_message}. "
    
    if kwargs:
        report += "Additional Details: "
        details = ", ".join([f"'{k}': '{v}'" for k, v in kwargs.items()])
        report += details + ". "
        
    # Provide actionable suggestions for common, recognizable error types.
    if isinstance(exception, FileNotFoundError):
        report += "Actionable Suggestion: Please verify that the file path is correct and the file exists."
    elif isinstance(exception, PermissionError):
        report += "Actionable Suggestion: Please check if the process has the necessary read/write permissions for the target path."
    elif isinstance(exception, (KeyError, IndexError)):
        report += "Actionable Suggestion: The code tried to access a missing key or index. Please check the input data structure (e.g., dictionary, list) for completeness."
    elif '401' in error_message or 'Unauthorized' in error_message.capitalize():
        report += "Actionable Suggestion: A '401 Unauthorized' error occurred. Please check if the API key or token is valid and has the required permissions."
    elif '404' in error_message or 'Not Found' in error_message.capitalize():
         report += "Actionable Suggestion: A '404 Not Found' error occurred. Please verify the API endpoint or resource URL is correct."
    elif isinstance(exception, ValueError):
        report += "Actionable Suggestion: An invalid value was provided. Please check the input parameters against the requirements."

    return report

def simulate_file_access(path: str):
    """A dummy function that simulates accessing a file and can fail."""
    if not path:
        raise ValueError("File path cannot be empty.")
    if "nonexistent" in path:
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    if "protected" in path:
        raise PermissionError(f"Permission denied: '{path}'")
    
    print(f"Successfully accessed file at '{path}'")
    return True

def main():
    """
    Main function to demonstrate the skill's failure articulation
    based on command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Demonstrates the articulate_failure_reasons skill by simulating failures."
    )
    parser.add_argument(
        "--path", 
        type=str, 
        required=True, 
        help="Path to simulate accessing. Use 'nonexistent', 'protected', or '' to trigger specific errors."
    )
    args = parser.parse_args()

    try:
        print(f"Attempting to simulate access to: '{args.path}'")
        simulate_file_access(args.path)
        print("\nOperation completed successfully.")
    except Exception as e:
        context = f"attempting to access the file at '{args.path}'"
        # Generate the detailed failure report using the skill's core logic
        failure_report = articulate_failure(e, context)
        print("\n--- FAILURE REPORT ---")
        print(failure_report)
        print("----------------------")

if __name__ == "__main__":
    main()
