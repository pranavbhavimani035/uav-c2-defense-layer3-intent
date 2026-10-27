from validator.validator import validate_command
from mission.state_machine import MissionStateMachine


def authorize_command(command, mission, machine):
    """
    Check a UAV command against mission rules and the current UAV state.

    Returns a dictionary containing:
    result, reason, and state.
    """

    # Step 1: Validate the command against mission rules.
    valid, reason = validate_command(command, mission)

    if not valid:
        return {
            "result": "REJECT",
            "reason": reason,
            "state": machine.get_state()
        }

    # Step 2: Check whether the command is allowed
    # in the current mission state.
    allowed, state_message = machine.transition(command["type"])

    if not allowed:
        return {
            "result": "REJECT",
            "reason": state_message,
            "state": machine.get_state()
        }

    # Step 3: Return the authorization decision.
    return {
        "result": "ACCEPT",
        "reason": reason,
        "state": machine.get_state()
    }
