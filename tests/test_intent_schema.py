import json
from jsonschema import validate


# Load schema
with open("intent/intent_schema.json", "r") as file:
    schema = json.load(file)


# Load mission
with open("intent/mission.json", "r") as file:
    mission = json.load(file)


# Validate mission against schema
validate(instance=mission, schema=schema)


print("======================================")
print("MISSION INTENT SCHEMA TEST")
print("======================================")
print("Mission ID:", mission["mission_id"])
print("Mission Type:", mission["mission"])
print("Schema Version:", mission["schema_version"])
print()
print("Result: VALID")
print("Mission conforms to intent schema.")

