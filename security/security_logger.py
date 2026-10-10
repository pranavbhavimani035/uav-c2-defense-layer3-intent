import json
from datetime import datetime, timezone
from pathlib import Path


# Store logs inside the Layer 3 project
LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "security_log.jsonl"


def log_security_event(command, result, reason, state):
    """
    Record a security decision made by Layer 3.

    Each event is stored as one JSON object per line.

    Returns:
        True  -> event recorded successfully
        False -> event could not be recorded
    """

    # Validate the decision result
    if result not in ("ACCEPT", "REJECT"):
        raise ValueError("Result must be ACCEPT or REJECT")

    # Validate the command structure
    if not isinstance(command, dict):
        raise TypeError("Command must be a dictionary")

    if not isinstance(reason, str):
        raise TypeError("Reason must be a string")

    if not isinstance(state, str):
        raise TypeError("State must be a string")

    # Build the audit event
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(
            timespec="seconds"
        ),
        "command": command,
        "result": result,
        "reason": reason,
        "state": state
    }

    try:
        # Create the logs directory if it doesn't exist
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        # Append one JSON record to the log
        with LOG_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(event, allow_nan=False) + "\n")

        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"SECURITY LOGGING FAILURE: {error}")
        return False


if __name__ == "__main__":

    test_command = {
        "type": "ARM"
    }

    success = log_security_event(
        test_command,
        "REJECT",
        "Command is not allowed by current mission policy",
        "CRUISE"
    )

    if success:
        print("Security event logged successfully.")
    else:
        print("Security event could not be recorded.")