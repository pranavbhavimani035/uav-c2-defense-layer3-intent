import json
import unittest
from pathlib import Path

from validator.validator import validate_command
from mission.state_machine import MissionStateMachine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MISSION_FILE = PROJECT_ROOT / "intent" / "mission.json"


class TestRejectedCommandState(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with MISSION_FILE.open("r", encoding="utf-8") as file:
            cls.mission = json.load(file)

    def setUp(self):
        self.machine = MissionStateMachine()

        # Move the simulated UAV from IDLE to CRUISE.
        accepted, _ = self.machine.transition("TAKEOFF")
        self.assertTrue(accepted)

    def test_outside_geofence_does_not_change_state(self):
        command = {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 150,
            "y": 50,
            "altitude": 80,
            "speed": 10
        }

        original_state = self.machine.get_state()

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid, "Out-of-geofence command should be rejected")

        # The state machine must not process a rejected command.
        if valid:
            self.machine.transition(command["type"])

        self.assertEqual(
            self.machine.get_state(),
            original_state,
            "Rejected command changed the UAV state"
        )

        print("\nOut-of-geofence command:", "REJECT")
        print("Reason:", reason)
        print("State before:", original_state)
        print("State after:", self.machine.get_state())

    def test_excessive_altitude_does_not_change_state(self):
        command = {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "altitude": 150,
            "speed": 10
        }

        original_state = self.machine.get_state()

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid, "Excessive-altitude command should be rejected")

        if valid:
            self.machine.transition(command["type"])

        self.assertEqual(
            self.machine.get_state(),
            original_state,
            "Rejected command changed the UAV state"
        )

        print("\nExcessive-altitude command:", "REJECT")
        print("Reason:", reason)
        print("State before:", original_state)
        print("State after:", self.machine.get_state())


if __name__ == "__main__":
    unittest.main(verbosity=2)
        