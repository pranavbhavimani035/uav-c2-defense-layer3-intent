class MissionStateMachine:

    # UAV states
    IDLE = "IDLE"
    CRUISE = "CRUISE"
    LANDING = "LANDING"
    LANDED = "LANDED"

    def __init__(self):
        # UAV starts on the ground
        self.current_state = self.IDLE

    def get_state(self):
        return self.current_state

    def transition(self, command_type):

        # IDLE state
        if self.current_state == self.IDLE:

            if command_type == "TAKEOFF":
                self.current_state = self.CRUISE
                return True, "UAV took off and entered CRUISE state"

            return False, f"{command_type} is not allowed in IDLE state"

        # CRUISE state
        if self.current_state == self.CRUISE:

            if command_type == "LAND":
                self.current_state = self.LANDING
                return True, "UAV entered LANDING state"

            if command_type == "GOTO":
                return True, "GOTO command allowed in CRUISE state"
            if command_type == "RETURN_HOME":
                return True, "RETURN_HOME command allowed in CRUISE state"

            return False, f"{command_type} is not allowed in CRUISE state"

        # LANDING state
        if self.current_state == self.LANDING:

            if command_type == "LAND_COMPLETE":
                self.current_state = self.LANDED
                return True, "UAV has landed"

            return False, f"{command_type} is not allowed while LANDING"

        # LANDED state
        if self.current_state == self.LANDED:

            if command_type == "TAKEOFF":
                self.current_state = self.CRUISE
                return True, "UAV took off again and entered CRUISE state"

            return False, f"{command_type} is not allowed in LANDED state"

        return False, "Unknown UAV state"


# Test the state machine
if __name__ == "__main__":

    print("===== INVALID STATE TESTS =====")

    # Test 1: GOTO while IDLE
    machine = MissionStateMachine()

    success, message = machine.transition("GOTO")
    print("\nTest 1: GOTO while IDLE")
    print("Result:", "ACCEPT" if success else "REJECT")
    print("Reason:", message)


    # Test 2: LAND while IDLE
    machine = MissionStateMachine()

    success, message = machine.transition("LAND")
    print("\nTest 2: LAND while IDLE")
    print("Result:", "ACCEPT" if success else "REJECT")
    print("Reason:", message)


    # Test 3: TAKEOFF while CRUISE
    machine = MissionStateMachine()

    machine.transition("TAKEOFF")

    success, message = machine.transition("TAKEOFF")
    print("\nTest 3: TAKEOFF while CRUISE")
    print("Result:", "ACCEPT" if success else "REJECT")
    print("Reason:", message)


    # Test 4: GOTO while LANDING
    machine = MissionStateMachine()

    machine.transition("TAKEOFF")
    machine.transition("LAND")

    success, message = machine.transition("GOTO")
    print("\nTest 4: GOTO while LANDING")
    print("Result:", "ACCEPT" if success else "REJECT")
    print("Reason:", message)


    # Test 5: GOTO while LANDED
    machine = MissionStateMachine()

    machine.transition("TAKEOFF")
    machine.transition("LAND")
    machine.transition("LAND_COMPLETE")

    success, message = machine.transition("GOTO")
    print("\nTest 5: GOTO while LANDED")
    print("Result:", "ACCEPT" if success else "REJECT")
    print("Reason:", message)