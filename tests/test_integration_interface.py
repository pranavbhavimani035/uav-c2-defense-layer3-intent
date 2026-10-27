import json
import unittest
from pathlib import Path

from integration_interface import authorize_command
from mission.state_machine import MissionStateMachine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MISSION_FILE = PROJECT_ROOT / "intent" / "mission.json"


class TestIntegrationInterface(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with MISSION_FILE.open("r", encoding="utf-8") as file:
            cls.mission = json.load(file)

    def setUp(self):
        self.machine = MissionStateMachine()

    def test_goto_while_idle_is_rejected(self):
        command = {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "altitude": 80,
            "speed": 10
        }

        result = authorize_command(
            command, self.mission, self.machine
        )

        self.assertEqual(result["result"], "REJECT")
        self.assertEqual(result["state"], "IDLE")

    def test_authorized_takeoff_is_accepted(self):
        command = {
            "type": "TAKEOFF",
            "altitude": 80
        }

        result = authorize_command(
            command, self.mission, self.machine
        )

        self.assertEqual(result["result"], "ACCEPT")
        self.assertEqual(result["state"], "CRUISE")

    def test_geofence_violation_is_rejected(self):
        # Move the simulated UAV into CRUISE first.
        self.machine.transition("TAKEOFF")

        command = {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 150,
            "y": 50,
            "altitude": 80,
            "speed": 10
        }

        result = authorize_command(
            command, self.mission, self.machine
        )

        self.assertEqual(result["result"], "REJECT")
        self.assertEqual(result["state"], "CRUISE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    