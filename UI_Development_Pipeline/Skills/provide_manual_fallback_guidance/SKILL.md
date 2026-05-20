---
name: provide_manual_fallback_guidance
description: A policy to provide actionable, manual guidance when a user's intent cannot be directly executed by the agent's current capabilities.
license: MIT
skill-author: AROS_code_generator
---

# Provide Manual Fallback Guidance Policy

This document outlines the policy for providing users with clear, actionable, and manual instructions when their request cannot be fulfilled automatically.

## GEPA Rule

**GEPA-Rule-003: Actionable Manual Guidance for Unexecutable Intents**

When an agent encounters a user request that it cannot execute due to limitations in its tools, skills, or environmental access, it MUST NOT simply state the failure. Instead, it must analyze the intent, identify the specific blocker, and provide a step-by-step manual guide that the user can follow to achieve their objective.

## Error Handling and Graceful Routing

This policy is grounded in the principle of robust error handling. The agent's logic must be designed to catch exceptions and identify limitations gracefully. Instead of terminating a workflow upon encountering an error (e.g., a `PermissionError` in Python, a non-zero exit code from a shell command), the agent must route the execution to this manual guidance protocol.

**Core Principle:** An inability to perform an action is not a failure of the task, but a trigger to provide the user with the necessary manual steps.

**GEPA-Proposed Rule: Actionable Guidance for Understood but Unexecutable Intents**

> If the agent understands the user's intent but cannot directly execute an action due to limitations, it should provide actionable manual guidance or alternative steps to the user.

This rule serves as a direct implementation of the graceful routing principle, ensuring that exceptions or permission boundaries are handled by providing clear, manual fallback steps.

## Core Logic: Identifying Unexecutable Intents

This policy is triggered when one or more of the following conditions are met. The agent must evaluate these conditions to decide whether to provide manual guidance.

1.  **Permission Denied:** The agent attempts an action (e.g., file access, command execution) and receives a "Permission Denied," "Access Denied," or "Forbidden" (e.g., HTTP 403) error. This is a clear signal that the agent lacks the authority to complete the task.

2.  **Missing Tools or Skills:** The user's request requires a tool or skill that is not present in the agent's current environment. The agent should verify this by searching its available skills.

3.  **Requires GUI Interaction:** The task requires interacting with a graphical user interface (GUI), such as filling out a web form, clicking a button, or using a desktop application. Agents are typically command-line based and cannot perform these actions.

4.  **Physical World Interaction:** The user asks for an action that requires physical presence or manipulation of a real-world object (e.g., "unplug the server," "press the reset button on the router").

5.  **CAPTCHA or Human Verification:** The workflow is blocked by a CAPTCHA, 2FA prompt, or other mechanism designed to verify a human user.

## Guiding Principles

-   **Be Specific and Clear:** The guidance should be unambiguous and easy to follow. Use numbered lists or clear steps.
-   **Provide Context:** Briefly explain *why* the manual steps are necessary by referencing the specific condition met (e.g., "I cannot proceed because I lack the necessary file permissions.").
-   **Include Verification Steps:** Tell the user how to confirm that their manual actions were successful.
-   **Don't Give Up:** The goal is to empower the user to complete the task, even if you can't do it for them.

## Example Applications

### Scenario 1: File Permission Error

**User Query:** "Append the latest log entries from a protected system file to my analysis document."

**GEPA-Compliant Response (Adheres to the rule):**

"I was unable to access `/var/log/secure.log` because of file permissions. To proceed, you will need to manually copy the logs. Here are the steps:

1.  **Log into the server:** Open a terminal and SSH into the server with appropriate credentials.
    ```bash
    ssh your_username@server_ip_address
    ```
2.  **Copy the log file with elevated privileges:** Use `sudo` to copy the file to a location you can access, like your home directory.
    ```bash
    sudo cp /var/log/secure.log ~/secure_log_copy.txt
    ```
3.  **Grant me access:** Once the file is copied, please grant me read access or provide the contents in a follow-up message so I can complete the analysis."

### Scenario 2: GUI-Based Action

**User Query:** "Go to the project management dashboard and export the quarterly report as a PDF."

**GEPA-Compliant Response (Adheres to the rule):**

"I cannot interact with the web-based dashboard directly. You will need to export the report manually.

1.  **Navigate to the Dashboard:** Open your web browser and go to `https://project-dashboard.example.com`.
2.  **Find the 'Reports' Section:** In the main navigation menu, click on "Reports".
3.  **Generate the Report:** Select the desired date range (e.g., Q3 2023) and click the "Generate" button.
4.  **Export as PDF:** Look for an "Export" or "Download" button and choose the "PDF" format.
5.  **Provide the File:** Once downloaded, please provide the PDF file to me for further processing."
