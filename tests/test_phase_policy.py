from mission.phase_policy import is_command_allowed


print("======================================")
print("MISSION PHASE AUTHORIZATION TEST")
print("======================================")


tests = [

    ("IDLE", "TAKEOFF"),
    ("IDLE", "GOTO"),

    ("CRUISE", "GOTO"),
    ("CRUISE", "RETURN_HOME"),
    ("CRUISE", "LAND"),
    ("CRUISE", "TAKEOFF"),

    ("LANDING", "LAND"),
    ("LANDING", "GOTO"),

    ("LANDED", "TAKEOFF"),
    ("LANDED", "GOTO")
]


for state, command in tests:

    allowed, reason = is_command_allowed(
        state,
        command
    )

    print()
    print("State:", state)
    print("Command:", command)

    if allowed:
        print("Result: ACCEPT")
    else:
        print("Result: REJECT")

    print("Reason:", reason)

print("\n======================================")
print("INVALID STATE TESTS")
print("======================================")


invalid_tests = [

    ("UNKNOWN", "GOTO"),
    ("UNKNOWN", "TAKEOFF"),
    ("UNKNOWN", "LAND"),
    ("", "GOTO"),
    ("INVALID_STATE", "TAKEOFF")
]


for state, command in invalid_tests:

    allowed, reason = is_command_allowed(
        state,
        command
    )

    print()
    print("State:", state)
    print("Command:", command)

    if allowed:
        print("Result: UNEXPECTED ACCEPT")
    else:
        print("Result: REJECT")

    print("Reason:", reason)