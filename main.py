import json

from security.security_logger import log_security_event
from validator.validator import validate_command
from mission.state_machine import MissionStateMachine
from mission.phase_policy import is_command_allowed


# -------------------------
# Load mission configuration
# -------------------------

with open("intent/mission.json", "r") as file:
    mission = json.load(file)


# -------------------------
# Create state machine
# -------------------------

machine = MissionStateMachine()


# -------------------------
# Display mission
# -------------------------

print("===== UAV MISSION =====")

print("Mission:", mission["mission"])
print("Maximum Altitude:", mission["max_altitude"], "m")
print("Maximum Speed:", mission["max_speed"], "m/s")
print("Allowed Zone:", mission["allowed_zone"])
print("Allowed Waypoints:", mission["allowed_waypoints"])

print("\nInitial UAV State:", machine.get_state())


# -------------------------
# Command processing function
# -------------------------

def process_command(command):

    print("\n===== NEW COMMAND =====")
    print("Command:", command)
    print("Current State:", machine.get_state())

    # Step 1: Mission constraints
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

    # Step 2: Mission phase authorization
    allowed, phase_reason = is_command_allowed(
        machine.get_state(),
        command["type"]
    )

    if not allowed:

        print("Result: REJECT")
        print("Reason:", phase_reason)

        log_security_event(
            command,
            "REJECT",
            phase_reason,
            machine.get_state()
        )

        return

    # Step 3: State transition
    allowed, state_message = machine.transition(
        command["type"]
    )

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

    # Command accepted
    print("Result: ACCEPT")
    print("Reason:", reason)
    print("State:", state_message)
    print("New UAV State:", machine.get_state())

    log_security_event(
        command,
        "ACCEPT",
        reason,
        machine.get_state()
    )

# -------------------------
# Test command sequence
# -------------------------

commands = [

    
    {

    "type": "GOTO",
    "waypoint": "WP2",
    "x": 100,
    "y": 100,
    "altitude": -20,
    "speed": 10
    },

    {
        "type": "TAKEOFF",
        "altitude": 80
    },

    {    
        "type": "GOTO",
        "waypoint": "WP2",
        "x": 50,
        "y": 50,
        "altitude": 80,
        "speed": 10
    
    },
    {
        "type": "ARM"

    },
    {
        "type": "RETURN_HOME"
    },
    {
        "type": "LAND"
    }
]


# Process commands one by one
for command in commands:
    process_command(command)
    