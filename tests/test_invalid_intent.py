import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError


# Load schema
with open("intent/intent_schema.json", "r") as file:
    schema = json.load(file)


# Create an intentionally invalid mission
invalid_mission = {
    "schema_version": "1.0",
    "mission_id": "BAD_MISSION",
    "mission": "PATROL",

    # INVALID: negative altitude
    "max_altitude": -100,

    "max_speed": 15,
    "allowed_zone": "ZONE_A",

    "allowed_waypoints": [
        "WP1",
        "WP2"
    ],

    "geofence": {
        "min_x": 0,
        "max_x": 100,
        "min_y": 0,
        "max_y": 100
    },

    "allowed_commands": [
        "TAKEOFF",
        "GOTO",
        "LAND"
    ]
}


print("======================================")
print("INVALID MISSION SCHEMA TEST")
print("======================================")

try:

    validate(
        instance=invalid_mission,
        schema=schema
    )

    print("Result: UNEXPECTEDLY VALID")

except ValidationError as error:

    print("Result: INVALID")
    print("Schema correctly rejected the mission.")
    print("Reason:", error.message)
    