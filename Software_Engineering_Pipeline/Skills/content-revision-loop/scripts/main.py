import argparse
import json
import time
import sys

# --- Mock Validator ---
# In a real scenario, this would be an external skill like 'gtb-validator'.
# For this script, we simulate its behavior.
def mock_validator(content):
    """
    A mock validator that fails on the first two attempts with specific feedback,
    and passes on the third attempt.
    """
    if "REVISED_FIX_FOR_ISSUE_1" not in content and "REVISED_FIX_FOR_ISSUE_2" not in content:
        print("MOCK_VALIDATOR: Initial draft failed validation.")
        return {
            "passed": False,
            "issues": [
                {"id": "issue-1", "description": "Missing a critical header section."},
                {"id": "issue-2", "description": "Conclusion is not supported by evidence."},
            ]
        }
    elif "REVISED_FIX_FOR_ISSUE_1" in content and "REVISED_FIX_FOR_ISSUE_2" not in content:
        print("MOCK_VALIDATOR: Second draft failed validation. Issue 2 is still open.")
        return {
            "passed": False,
            "issues": [
                {"id": "issue-2", "description": "Conclusion is not supported by evidence."},
            ]
        }
    elif "REVISED_FIX_FOR_ISSUE_1" in content and "REVISED_FIX_FOR_ISSUE_2" in content:
        print("MOCK_VALIDATOR: All issues addressed. Content has passed validation.")
        return {"passed": True, "issues": []}
    else: # Should not be reached in this simulation
        return {"passed": False, "issues": [{"id": "unknown", "description": "An unexpected error occurred."}]}

# --- Mock Revision Logic ---
def address_issues(content, issues):
    """
    A mock content revision function. In a real agent, this would involve
    an LLM call to regenerate content based on the feedback.
    This simulation applies a simple fix for each issue.
    """
    print(f"REVISION_LOGIC: Addressing {len(issues)} issues...")
    updated_content = content
    addressed_issue_ids = []
    for issue in issues:
        if issue['id'] == 'issue-1':
            updated_content += "\nREVISED_FIX_FOR_ISSUE_1: Added Header."
            addressed_issue_ids.append(issue['id'])
            print("REVISION_LOGIC: Fixed 'issue-1'.")
        elif issue['id'] == 'issue-2':
            updated_content += "\nREVISED_FIX_FOR_ISSUE_2: Strengthened Conclusion."
            addressed_issue_ids.append(issue['id'])
            print("REVISION_LOGIC: Fixed 'issue-2'.")
        time.sleep(0.5)
    return updated_content, addressed_issue_ids


class ContentRevisionLoop:
    """
    Implements the GEPA-mandated content revision loop state machine.
    """
    def __init__(self, initial_content, max_revisions=3):
        self.content = initial_content
        self.state = "DRAFTING"
        self.revision_count = 0
        self.max_revisions = max_revisions
        self.issues_to_address = []
        self.history = [("INITIALIZE", f"State set to {self.state}")]

    def log_history(self, action, detail):
        self.history.append((action, detail))
        print(f"STATE_MACHINE: [{action}] {detail}")

    def change_state(self, new_state):
        self.log_history("STATE_CHANGE", f"Transitioning from {self.state} to {new_state}")
        self.state = new_state

    def run(self):
        """
        Executes the entire revision loop from start to finish.
        """
        # Initial state is DRAFTING, immediately ready for validation
        self.change_state("PENDING_VALIDATION")

        while self.revision_count < self.max_revisions:
            if self.state == "PENDING_VALIDATION":
                # --- VALIDATION STEP ---
                self.log_history("ACTION", "Running content validator.")
                validation_result = mock_validator(self.content)

                if validation_result["passed"]:
                    self.change_state("COMMITTED")
                    self.log_history("SUCCESS", "Content passed validation and is now committed.")
                    print("\n--- FINAL COMMITTED CONTENT ---")
                    print(self.content)
                    print("------------------------------")
                    return True
                else:
                    # --- ENTER REVISION STEP ---
                    self.revision_count += 1
                    self.log_history("VALIDATION_FAILED", f"Validation failed. Revision cycle {self.revision_count}/{self.max_revisions}.")
                    self.issues_to_address = validation_result["issues"]
                    self.change_state("REVISING")

            if self.state == "REVISING":
                # --- MANDATORY REVISION CYCLE ---
                # This block enforces the GEPA proposal.
                # The agent CANNOT proceed to validation without clearing the issues list.
                self.log_history("ENFORCEMENT", f"Mandatory revision started. {len(self.issues_to_address)} issues to fix.")

                # Simulate the agent addressing the issues.
                revised_content, fixed_issue_ids = address_issues(self.content, self.issues_to_address)
                self.content = revised_content

                # --- EXPLICIT STATE CHECK ---
                # The system verifies that all identified issues were addressed.
                # This is the critical gate preventing premature re-validation.
                if set(fixed_issue_ids) == set(issue['id'] for issue in self.issues_to_address):
                    self.log_history("ENFORCEMENT_PASS", "All identified issues have been addressed.")
                    self.issues_to_address = []
                    self.change_state("PENDING_VALIDATION") # Cleared to attempt validation again
                else:
                    # This branch represents a policy violation or faulty agent logic, leading to escalation.
                    self.log_history("ENFORCEMENT_FAIL", "Agent failed to address all issues. This is a policy violation.")
                    self.change_state("ESCALATED")
                    print("\n--- ERROR: FAILED TO ADDRESS ALL ISSUES ---", file=sys.stderr)
                    print(f"Original Issues: {[i['id'] for i in self.issues_to_address]}", file=sys.stderr)
                    print(f"Addressed Issues: {fixed_issue_ids}", file=sys.stderr)
                    return False

        # If the loop finishes without success, it means we've exceeded max revisions
        if self.state != "COMMITTED":
            self.change_state("ESCALATED")
            self.log_history("FAILURE", f"Failed to validate content after {self.max_revisions} revisions.")
            print("\n--- FINAL FAILED CONTENT ---")
            print(self.content)
            print("----------------------------")
            return False


def main():
    parser = argparse.ArgumentParser(description="Demonstrates the GEPA Content Revision Loop.")
    parser.add_argument(
        '--content',
        type=str,
        default="This is the initial draft of the document.",
        help="The initial content to be processed."
    )
    args = parser.parse_args()

    print("--- Starting GEPA Content Revision Loop Simulation ---")
    loop = ContentRevisionLoop(initial_content=args.content)
    success = loop.run()

    print("\n--- Simulation Finished ---")
    if success:
        print("Result: SUCCESS (Content was successfully revised and committed)")
    else:
        print("Result: FAILED (Content was escalated after failing the revision process)")
    print("-------------------------")


if __name__ == "__main__":
    main()
