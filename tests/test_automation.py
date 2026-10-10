import json
import unittest
from pathlib import Path

from validator.validator import validate_command


# Find the mission configuration relative to this test file
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MISSION_FILE = PROJECT_ROOT / "intent" / "mission.json"


class TestLayer3Automation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load mission configuration once for all tests."""

        with MISSION_FILE.open("r", encoding="utf-8") as file:
            cls.mission = json.load(file)

    def make_goto_command(self, **overrides):
        """Create a valid GOTO command and apply test changes."""

        command = {
            "type": "GOTO",
            "waypoint": "WP2",
            "x": 50,
            "y": 50,
            "altitude": 80,
            "speed": 10
        }

        command.update(overrides)
        return command

    def test_valid_goto_is_accepted(self):
        command = self.make_goto_command()

        valid, reason = validate_command(command, self.mission)

        self.assertTrue(valid, reason)

    def test_unauthorized_waypoint_is_rejected(self):
        command = self.make_goto_command(waypoint="WP99")

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid)
        self.assertIn("waypoint", reason.lower())

    def test_altitude_above_limit_is_rejected(self):
        command = self.make_goto_command(altitude=150)

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid)
        self.assertIn("altitude", reason.lower())

    def test_negative_altitude_is_rejected(self):
        command = self.make_goto_command(altitude=-10)

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid)
        self.assertIn("altitude", reason.lower())

    def test_negative_speed_is_rejected(self):
        command = self.make_goto_command(speed=-5)

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid)
        self.assertIn("speed", reason.lower())

    def test_text_altitude_is_rejected_without_crashing(self):
        command = self.make_goto_command(altitude="high")

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid)
        self.assertIn("altitude", reason.lower())

    def test_text_speed_is_rejected_without_crashing(self):
        command = self.make_goto_command(speed="fast")

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid)
        self.assertIn("speed", reason.lower())

    def test_missing_altitude_is_rejected(self):
        command = self.make_goto_command()
        del command["altitude"]

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid)
        self.assertIn("altitude", reason.lower())

    def test_missing_waypoint_is_rejected(self):
        command = self.make_goto_command()
        del command["waypoint"]

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid)
        self.assertIn("waypoint", reason.lower())

    def test_unknown_command_is_rejected(self):
        command = {"type": "DESTROY"}

        valid, reason = validate_command(command, self.mission)

        self.assertFalse(valid)

    def test_none_command_is_rejected(self):
        valid, reason = validate_command(None, self.mission)

        self.assertFalse(valid)
        self.assertIn("dictionary", reason.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
    