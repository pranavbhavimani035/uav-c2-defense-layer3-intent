# Mission-phase authorization policy


PHASE_POLICY = {

    "IDLE": [
        "TAKEOFF"
    ],

    "CRUISE": [
        "GOTO",
        "RETURN_HOME",
        "LAND"
    ],

    "LANDING": [
        "LAND"
    ],

    "LANDED": [
        "TAKEOFF"
    ]
}


def is_command_allowed(state, command_type):

    allowed_commands = PHASE_POLICY.get(state, [])

    if command_type in allowed_commands:
        return True, f"{command_type} is allowed in {state} state"

    return False, f"{command_type} is not allowed in {state} state"
