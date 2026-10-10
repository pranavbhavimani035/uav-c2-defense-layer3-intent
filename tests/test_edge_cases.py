import json

from validator.validator import validate_command


# Load mission configuration
with open("intent/mission.json", "r") as file:
    mission = json.load(file)


# Test cases for unexpected commands
test_cases = [

    (
        "Missing altitude",
        {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "speed": 10
        }
    ),

    (
        "Missing waypoint",
        {
            "type": "GOTO",
            "x": 50,
            "y": 50,
            "altitude": 80,
            "speed": 10
        }
    ),

    (
        "Negative altitude",
        {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "altitude": -20,
            "speed": 10
        }
    ),

    (
        "Negative speed",
        {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "altitude": 80,
            "speed": -5
        }
    ),

    (
        "Altitude is text",
        {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "altitude": "high",
            "speed": 10
        }
    ),

    (
        "Speed is text",
        {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "altitude": 80,
            "speed": "fast"
        }
    ),

    (
        "Unknown command",
        {
            "type": "DESTROY"
        }
    ),

    (
        "Empty command",
        {}
    ),

    (
        "Waypoint not authorized",
        {
            "type": "GOTO",
            "waypoint": "WP99",
            "x": 50,
            "y": 50,
            "altitude": 80,
            "speed": 10
        }
    ),

    (
        "Altitude exactly at maximum",
        {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "altitude": 100,
            "speed": 10
        }
    ),

    (
        "Speed exactly at maximum",
        {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "altitude": 80,
            "speed": 15
        }
    )
]


print("======================================")
print("LAYER 3 EDGE-CASE TESTS")
print("======================================")


for test_name, command in test_cases:

    print("\nTest:", test_name)

    try:

        valid, reason = validate_command(
            command,
            mission
        )

        if valid:
            print("Result: ACCEPT")
        else:
            print("Result: REJECT")

        print("Reason:", reason)

    except Exception as error:

        print("Result: ERROR")
        print("Exception:", type(error).__name__)
        print("Message:", error)
print("\n======================================")
print("ADDITIONAL MALFORMED INPUT TESTS")
print("======================================")


additional_tests = [
    ("None input", None),

    ("List instead of dictionary", []),

    ("Missing command type", {
        "altitude": 50
    }),

    ("Invalid TAKEOFF altitude", {
        "type": "TAKEOFF",
        "altitude": "high"
    }),

    ("Negative TAKEOFF altitude", {
        "type": "TAKEOFF",
        "altitude": -10
    })
]


for test_name, command in additional_tests:

    print("\nTest:", test_name)

    try:
        valid, reason = validate_command(command, mission)

        if valid:
            print("Result: ACCEPT")
        else:
            print("Result: REJECT")

        print("Reason:", reason)

    except Exception as error:
        print("Result: ERROR")
        print("Exception:", type(error).__name__)
        print("Message:", error)
        