import json

from validator.validator import validate_command
from mission.state_machine import MissionStateMachine
from security.security_logger import log_security_event


# ============================================================
# LOAD MISSION
# ============================================================

with open("intent/mission.json", "r") as file:
    mission = json.load(file)


# ============================================================
# CREATE UAV STATE MACHINE
# ============================================================

machine = MissionStateMachine()


# ============================================================
# DISPLAY MISSION
# ============================================================

print("\n==============================================")
print("       UAV LAYER 3 SECURITY DEMONSTRATION")
print("==============================================")

print("\nMission:", mission["mission"])
print("Maximum Altitude:", mission["max_altitude"], "m")
print("Maximum Speed:", mission["max_speed"], "m/s")
print("Allowed Zone:", mission["allowed_zone"])
print("Allowed Waypoints:", mission["allowed_waypoints"])

print("\nInitial UAV State:", machine.get_state())


# ============================================================
# COMMAND PROCESSOR
# ============================================================

def process_demo_command(command, description):

    print("\n----------------------------------------------")
    print("SCENARIO:", description)
    print("----------------------------------------------")

    print("Command:", command)
    print("Current State:", machine.get_state())

    # Layer 3 mission validation
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

    # Mission state validation
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
    print("State:", state_message)
    print("New UAV State:", machine.get_state())

    log_security_event(
        command,
        "ACCEPT",
        reason,
        machine.get_state()
    )


# ============================================================
# SCENARIO 1 — GOTO WHILE IDLE
# ============================================================

process_demo_command(
    {
        "type": "GOTO",
        "waypoint": "WP2",
        "x": 50,
        "y": 50,
        "altitude": 80,
        "speed": 10
    },
    "GOTO before TAKEOFF"
)


# ============================================================
# SCENARIO 2 — TAKEOFF
# ============================================================

process_demo_command(
    {
        "type": "TAKEOFF",
        "altitude": 80
    },
    "Authorized TAKEOFF"
)


# ============================================================
# SCENARIO 3 — VALID GOTO
# ============================================================

process_demo_command(
    {
        "type": "GOTO",
        "waypoint": "WP2",
        "x": 50,
        "y": 50,
        "altitude": 80,
        "speed": 10
    },
    "Valid GOTO inside mission boundaries"
)


# ============================================================
# SCENARIO 4 — UNAUTHORIZED COMMAND
# ============================================================

process_demo_command(
    {
        "type": "ARM"
    },
    "Unauthorized ARM command"
)


# ============================================================
# SCENARIO 5 — GEOFENCE VIOLATION
# ============================================================

process_demo_command(
    {
        "type": "GOTO",
        "waypoint": "WP2",
        "x": 150,
        "y": 50,
        "altitude": 80,
        "speed": 10
    },
    "GOTO outside mission geofence"
)


# ============================================================
# SCENARIO 6 — ALTITUDE VIOLATION
# ============================================================

process_demo_command(
    {
        "type": "GOTO",
        "waypoint": "WP2",
        "x": 50,
        "y": 50,
        "altitude": 150,
        "speed": 10
    },
    "GOTO above maximum altitude"
)


# ============================================================
# SCENARIO 7 — LAND
# ============================================================

process_demo_command(
    {
        "type": "LAND"
    },
    "Authorized LAND command"
)


# ============================================================
# DEMONSTRATION COMPLETE
# ============================================================

print("\n==============================================")
print("       LAYER 3 DEMONSTRATION COMPLETE")
print("==============================================")

print("\nSecurity decisions have been recorded in:")
print("logs/security_log.jsonl")
