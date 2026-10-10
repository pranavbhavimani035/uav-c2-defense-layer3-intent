import json

from validator.validator import validate_command
from mission.state_machine import MissionStateMachine
from security.security_logger import log_security_event


# Load mission configuration
with open("intent/mission.json", "r") as file:
    mission = json.load(file)


# Create UAV state machine
machine = MissionStateMachine()


def test_attack(command, attack_name):

    print("\n==============================")
    print("ATTACK:", attack_name)
    print("Command:", command)
    print("Current State:", machine.get_state())

    # Check mission rules
    valid, reason = validate_command(command, mission)

    if not valid:

        print("Result: REJECT")
        print("Reason:", reason)

        log_security_event(
            command,
            "REJECT",
            reason,
            machine.get_state()
        )

        return

    # Check mission state
    allowed, state_message = machine.transition(command["type"])

    if not allowed:

        print("Result: REJECT")
        print("Reason:", state_message)

        log_security_event(
            command,
            "REJECT",
            state_message,
            machine.get_state()
        )

        return

    print("Result: ACCEPT")
    print("Reason:", reason)

    log_security_event(
        command,
        "ACCEPT",
        reason,
        machine.get_state()
    )


# -----------------------------
# Prepare UAV for attack tests
# -----------------------------

machine.transition("TAKEOFF")


# -----------------------------
# Attack 1
# Unauthorized command
# -----------------------------

test_attack(
    {
        "type": "ARM"
    },
    "Unauthorized ARM command"
)


# -----------------------------
# Attack 2
# Geofence violation
# -----------------------------

test_attack(
    {
        "type": "GOTO",
        "waypoint": "WP2",
        "x": 150,
        "y": 50,
        "altitude": 80,
        "speed": 10
    },
    "Geofence violation"
)


# -----------------------------
# Attack 3
# Altitude violation
# -----------------------------

test_attack(
    {
        "type": "GOTO",
        "waypoint": "WP2",
        "x": 50,
        "y": 50,
        "altitude": 150,
        "speed": 10
    },
    "Altitude violation"
)


# -----------------------------
# Attack 4
# Speed violation
# -----------------------------

test_attack(
    {
        "type": "GOTO",
        "waypoint": "WP2",
        "x": 50,
        "y": 50,
        "altitude": 80,
        "speed": 30
    },
    "Speed violation"
)
