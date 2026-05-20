---
name: user_notification_fallback_mechanism
description: Implements a robust user notification system with a fallback mechanism. It attempts a primary notification method and, upon failure, automatically triggers a secondary method to ensure message delivery.
license: MIT
skill-author: AROS_code_generator
---

# User Notification Fallback Mechanism

This skill provides a reliable notification system by implementing a primary and a secondary (fallback) communication channel. If the first attempt at sending a notification fails, it automatically switches to the backup method.

## Key Capabilities
- **Primary Notification Attempt**: Tries to send a message using the default, preferred method.
- **Failure Detection**: Catches failures from the primary method.
- **Fallback Trigger**: Automatically sends the message using a secondary method if the primary one fails.
- **Testability**: Includes a `--force-fail` flag to easily test the fallback logic.

## Workflow
1.  **Receive Message**: The skill is invoked with a message to be sent.
2.  **Attempt Primary Send**: The script calls the primary notification function. For this simulation, the primary method can be made to fail for testing purposes.
3.  **Check for Failure**: The script evaluates the success of the primary attempt. This is done via a boolean return value.
4.  **Engage Fallback (If Needed)**: If the primary attempt failed, the script logs the failure and immediately calls the secondary (fallback) notification function.
5.  **Report Status**: The script prints the final outcome, indicating whether the notification was sent via the primary or fallback method.

## Quick Check

Use this command to verify that the packaged script is syntactically correct.
```bash
python -m py_compile ~/.gemini/skills/user_notification_fallback_mechanism/scripts/main.py
```

## Audit-Ready Commands

These commands demonstrate the core functionality, including the successful and fallback paths.

```bash
# Standard execution (primary method may succeed or fail)
python ~/.gemini/skills/user_notification_fallback_mechanism/scripts/main.py --message "Critical Alert: Main power failure in Sector 4."

# Force the primary method to fail to test the fallback mechanism
python ~/.gemini/skills/user_notification_fallback_mechanism/scripts/main.py --message "Warning: Inventory for reagent '7A-D' is below threshold." --force-fail
```
