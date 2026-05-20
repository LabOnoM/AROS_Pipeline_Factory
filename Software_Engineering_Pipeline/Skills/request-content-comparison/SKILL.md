---
name: request-content-comparison
description: A policy to prevent task execution errors by ensuring the user's request is fully supported by the provided instructional content.
license: MIT
skill-author: AROS-Core
---

# Policy: Request-Content Comparison

This policy mandates a strict validation step to prevent errors that arise when a user's request cannot be fully satisfied by the provided instructional content (e.g., a walkthrough, README, or tutorial). The primary goal is to halt execution and report discrepancies *before* taking action, rather than failing midway through a task.

## GEPA Rule

### **GEPA-Rule-005: Request-Walkthrough Fidelity**

Before execution, the agent must perform a precise, three-way comparison between the user's request, the user's implied intent, and the literal content of the provided walkthrough document. The agent is forbidden from proceeding if the walkthrough does not explicitly contain the commands, parameters, or steps required to fulfill the request.

## Validation Workflow

1.  **Deconstruct the User Request:**
    *   Identify all explicit named entities (e.g., functions, tools, filenames, features).
    *   Identify the primary action verb and the implied goal.

2.  **Scan the Walkthrough for Support:**
    *   Systematically scan the provided instructional document for direct mentions of the named entities from the user's request.
    *   Verify that the sequence of commands or steps described in the walkthrough aligns with the user's implied goal.

3.  **Perform the Fidelity Check:**
    *   **Direct Match:** Does the walkthrough contain the *exact* commands, flags, and filenames mentioned in the user's request?
    *   **Intent Match:** Does the procedure in the walkthrough actually achieve the user's implied goal?
    *   **Completeness Match:** Are all parts of the user's request serviceable by the information in the walkthrough?

4.  **Act or Report:**
    *   **If Fidelity is High:** Proceed with execution, strictly following the steps from the walkthrough.
    *   **If Fidelity is Low:** Halt execution. Report the specific discrepancy to the user. Explain *what* is missing from the walkthrough and why you cannot proceed. Do not attempt to guess or hallucinate the missing steps.

## Example Application

**Context:** The agent is provided with `walkthrough.md`.

**`walkthrough.md` Content:**
"To get started, first run the setup script to install dependencies: `./setup.sh`. Then, start the service using the default configuration: `systemctl start my-service`."

**User Request:** "Use the walkthrough to run the setup script and then start the service with the `--debug` flag enabled."

**INCORRECT / NON-COMPLIANT Action:**
The agent runs `./setup.sh` and then attempts to run `systemctl start my-service --debug`, assuming the flag is valid. This action fails because the agent hallucinated a parameter not supported by the documentation.

**CORRECT / GEPA-COMPLIANT Response:**
"I cannot fully comply with your request. The provided walkthrough document details how to run the setup script and start the service. However, it does not contain any information or instructions for enabling a `--debug` flag.

To prevent errors, I have halted execution. Shall I proceed with starting the service using the default configuration as described in the walkthrough?"
