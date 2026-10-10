def is_inside_geofence(x, y, geofence):
    """
    Check whether a position is inside the mission geofence.

    Returns:
        True  -> position is inside
        False -> position is outside
    """

    if x < geofence["min_x"]:
        return False

    if x > geofence["max_x"]:
        return False

    if y < geofence["min_y"]:
        return False

    if y > geofence["max_y"]:
        return False

    return True

if __name__ == "__main__":

    geofence = {
        "min_x": 0,
        "max_x": 100,
        "min_y": 0,
        "max_y": 100
    }

    test_positions = [
        (50, 50),
        (20, 80),
        (100, 100),
        (120, 50),
        (-10, 40)
    ]

    print("===== GEOFENCE TESTS =====")

    for x, y in test_positions:

        inside = is_inside_geofence(x, y, geofence)

        result = "INSIDE" if inside else "OUTSIDE"

        print(f"Position ({x}, {y}) -> {result}")