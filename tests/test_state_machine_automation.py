import unittest

from mission.state_machine import MissionStateMachine


class TestMissionStateMachine(unittest.TestCase):

    def setUp(self):
        # Create a fresh state machine for each test
        self.machine = MissionStateMachine()

    def test_initial_state_is_idle(self):
        self.assertEqual(
            self.machine.get_state(),
            MissionStateMachine.IDLE
        )

    def test_goto_rejected_while_idle(self):
        success, message = self.machine.transition("GOTO")

        self.assertFalse(success)
        self.assertEqual(self.machine.get_state(), "IDLE")

    def test_takeoff_moves_idle_to_cruise(self):
        success, message = self.machine.transition("TAKEOFF")

        self.assertTrue(success)
        self.assertEqual(self.machine.get_state(), "CRUISE")

    def test_goto_allowed_while_cruising(self):
        self.machine.transition("TAKEOFF")

        success, message = self.machine.transition("GOTO")

        self.assertTrue(success)
        self.assertEqual(self.machine.get_state(), "CRUISE")

    def test_return_home_allowed_while_cruising(self):
        self.machine.transition("TAKEOFF")

        success, message = self.machine.transition("RETURN_HOME")

        self.assertTrue(success)
        self.assertEqual(self.machine.get_state(), "CRUISE")

    def test_land_moves_cruise_to_landing(self):
        self.machine.transition("TAKEOFF")

        success, message = self.machine.transition("LAND")

        self.assertTrue(success)
        self.assertEqual(self.machine.get_state(), "LANDING")

    def test_goto_rejected_while_landing(self):
        self.machine.transition("TAKEOFF")
        self.machine.transition("LAND")

        success, message = self.machine.transition("GOTO")

        self.assertFalse(success)
        self.assertEqual(self.machine.get_state(), "LANDING")

    def test_land_complete_moves_to_landed(self):
        self.machine.transition("TAKEOFF")
        self.machine.transition("LAND")

        success, message = self.machine.transition("LAND_COMPLETE")

        self.assertTrue(success)
        self.assertEqual(self.machine.get_state(), "LANDED")

    def test_goto_rejected_while_landed(self):
        self.machine.transition("TAKEOFF")
        self.machine.transition("LAND")
        self.machine.transition("LAND_COMPLETE")

        success, message = self.machine.transition("GOTO")

        self.assertFalse(success)
        self.assertEqual(self.machine.get_state(), "LANDED")

    def test_takeoff_rejected_while_cruising(self):
        self.machine.transition("TAKEOFF")

        success, message = self.machine.transition("TAKEOFF")

        self.assertFalse(success)
        self.assertEqual(self.machine.get_state(), "CRUISE")

    def test_takeoff_allowed_again_after_landing(self):
        self.machine.transition("TAKEOFF")
        self.machine.transition("LAND")
        self.machine.transition("LAND_COMPLETE")

        success, message = self.machine.transition("TAKEOFF")

        self.assertTrue(success)
        self.assertEqual(self.machine.get_state(), "CRUISE")

    def test_land_rejected_while_idle(self):
        success, message = self.machine.transition("LAND")

        self.assertFalse(success)
        self.assertEqual(self.machine.get_state(), "IDLE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    