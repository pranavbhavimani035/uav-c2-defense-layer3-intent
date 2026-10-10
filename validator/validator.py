from geofence.geofence import is_inside_geofence
from mission.phase_policy import is_command_allowed


def validate_command(command, mission):
    """
    Validate a UAV command against mission rules.

    Returns:
        (True, reason)  -> command passes validation
        (False, reason) -> command is rejected
    """

    # 1. Validate the input structures
    if not isinstance(command, dict):
        return False, "Command must be a dictionary"

    if not isinstance(mission, dict):
        return False, "Mission configuration must be a dictionary"

    # 2. Validate required mission configuration
    required_mission_fields = [
        "allowed_commands",
        "allowed_waypoints",
        "max_altitude",
        "max_speed",
        "geofence"
    ]

    for field in required_mission_fields:
        if field not in mission:
            return False, f"Mission configuration is missing {field}"

    if not isinstance(mission["allowed_commands"], list):
        return False, "Mission allowed_commands must be a list"

    if not isinstance(mission["allowed_waypoints"], list):
        return False, "Mission allowed_waypoints must be a list"

    # 3. Validate mission limits
    for field in ["max_altitude", "max_speed"]:
        value = mission[field]

        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
        ):
            return False, f"Mission {field} must be a number"

        if value < 0:
            return False, f"Mission {field} cannot be negative"

    # 4. Validate command type
    command_type = command.get("type")

    if not isinstance(command_type, str) or not command_type:
        return False, "Command type must be a non-empty string"

    supported_commands = [
        "GOTO",
        "TAKEOFF",
        "LAND",
        "RETURN_HOME"
    ]

    if command_type not in supported_commands:
        return False, "Unknown command type"

    # 5. Check mission command policy
    if command_type not in mission["allowed_commands"]:
        return False, "Command is not allowed by current mission policy"

    # --------------------------------
    # GOTO command
    # --------------------------------
    if command_type == "GOTO":

        # Required fields
        required_fields = [
            "waypoint",
            "altitude",
            "speed",
            "x",
            "y"
        ]

        for field in required_fields:
            if field not in command:
                return False, f"GOTO command requires {field}"

        # Validate waypoint type
        if not isinstance(command["waypoint"], str):
            return False, "Waypoint must be a string"

        if command["waypoint"] not in mission["allowed_waypoints"]:
            return False, "Waypoint is not authorized"

        # Validate numeric fields before comparing them
        numeric_fields = ["altitude", "speed", "x", "y"]

        for field in numeric_fields:
            value = command[field]

            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
            ):
                return False, f"{field.capitalize()} must be a number"

            if field in ["altitude", "speed"] and value < 0:
                return False, f"{field.capitalize()} cannot be negative"

        # Check altitude limit
        if command["altitude"] > mission["max_altitude"]:
            return False, "Altitude exceeds mission limit"

        # Check speed limit
        if command["speed"] > mission["max_speed"]:
            return False, "Speed exceeds mission limit"

        # Check geofence
        if not is_inside_geofence(
            command["x"],
            command["y"],
            mission["geofence"]
        ):
            return False, "Target position is outside mission geofence"

        return True, "GOTO command is authorized"

    # --------------------------------
    # TAKEOFF command
    # --------------------------------
    if command_type == "TAKEOFF":

        if "altitude" not in command:
            return False, "TAKEOFF command requires an altitude"

        altitude = command["altitude"]

        if (
            isinstance(altitude, bool)
            or not isinstance(altitude, (int, float))
        ):
            return False, "Takeoff altitude must be a number"

        if altitude < 0:
            return False, "Takeoff altitude cannot be negative"

        if altitude > mission["max_altitude"]:
            return False, "Takeoff altitude exceeds mission limit"

        return True, "TAKEOFF command is authorized"

    # --------------------------------
    # LAND command
    # --------------------------------
    if command_type == "LAND":
        return True, "LAND command is authorized"

    # --------------------------------
    # RETURN_HOME command
    # --------------------------------
    if command_type == "RETURN_HOME":
        return True, "RETURN_HOME command is authorized"

    return False, "Command rejected"