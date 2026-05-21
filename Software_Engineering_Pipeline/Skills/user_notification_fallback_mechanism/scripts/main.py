
import argparse
import time
import random
import sys

class PrimaryNotificationError(Exception):
    """Custom exception for primary notification failures."""
    pass

def send_primary_notification(message: str, force_fail: bool):
    """
    Simulates sending a notification through the primary channel.
    Raises PrimaryNotificationError on failure.
    """
    print("[Primary] Attempting to send notification...")

    if force_fail or random.choice([True, False]):
        error_message = "[Primary] FAILED. Simulating a critical failure."
        print(error_message)
        raise PrimaryNotificationError(error_message)

    print(f"[Primary] SUCCESS. Notification sent: '{message}'")

def send_fallback_notification(message: str):
    """
    Sends a notification through the secondary (fallback) channel.
    """
    print("[Fallback] Primary method failed. Engaging fallback mechanism...")
    # In a real-world scenario, this would use a different, more reliable service.
    print(f"[Fallback] SUCCESS. Notification sent via fallback: '{message}'")
    return True

def main():
    """
    Main function to parse arguments and orchestrate the notification process.
    """
    parser = argparse.ArgumentParser(
        description="Send a notification with a fallback mechanism using exception handling."
    )
    parser.add_argument(
        "--message",
        type=str,
        required=True,
        help="The notification message to be sent."
    )
    parser.add_argument(
        "--force-fail",
        action="store_true",
        help="Force the primary notification method to fail to test the fallback."
    )
    args = parser.parse_args()

    message = args.message
    force_fail = args.force_fail

    try:
        # --- GEPA Error Prevention Rule ---
        # Attempt the primary method and catch exceptions to trigger the fallback.
        print("--- Initiating Notification Protocol ---")
        send_primary_notification(message, force_fail)
        print("--- Final Status: Notification sent successfully via PRIMARY channel. ---")
    except PrimaryNotificationError as e:
        print(f"Caught a primary notification failure: {e}")
        print("--- Engaging Fallback ---")
        if not send_fallback_notification(message):
            print("--- CRITICAL FAILURE: Both primary and fallback channels failed. ---", file=sys.stderr)
            sys.exit(1)
        else:
            print("--- Final Status: Notification sent successfully via FALLBACK channel. ---")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
