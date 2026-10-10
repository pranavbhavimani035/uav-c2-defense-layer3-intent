import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from security.security_logger import log_security_event


class TestSecurityLoggerAutomation(unittest.TestCase):

    def test_accepted_event_is_logged(self):
        command = {
            "type": "GOTO",
            "waypoint": "WP2"
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "security_log.jsonl"

            with patch(
                "security.security_logger.LOG_FILE",
                log_file
            ):
                log_security_event(
                    command,
                    "ACCEPT",
                    "GOTO command is authorized",
                    "CRUISE"
                )

            with log_file.open("r", encoding="utf-8") as file:
                event = json.loads(file.readline())

        self.assertEqual(event["command"], command)
        self.assertEqual(event["result"], "ACCEPT")
        self.assertEqual(event["reason"], "GOTO command is authorized")
        self.assertEqual(event["state"], "CRUISE")
        self.assertIn("timestamp", event)

    def test_rejected_event_is_logged(self):
        command = {"type": "ARM"}

        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "security_log.jsonl"

            with patch(
                "security.security_logger.LOG_FILE",
                log_file
            ):
                log_security_event(
                    command,
                    "REJECT",
                    "Command is not allowed",
                    "CRUISE"
                )

            with log_file.open("r", encoding="utf-8") as file:
                event = json.loads(file.readline())

        self.assertEqual(event["command"], command)
        self.assertEqual(event["result"], "REJECT")
        self.assertEqual(event["reason"], "Command is not allowed")
        self.assertEqual(event["state"], "CRUISE")
        self.assertIn("timestamp", event)

    def test_multiple_events_are_appended(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            log_file = Path(temp_dir) / "security_log.jsonl"

            with patch(
                "security.security_logger.LOG_FILE",
                log_file
            ):
                log_security_event(
                    {"type": "GOTO"},
                    "ACCEPT",
                    "Authorized",
                    "CRUISE"
                )

                log_security_event(
                    {"type": "ARM"},
                    "REJECT",
                    "Unauthorized",
                    "CRUISE"
                )

            with log_file.open("r", encoding="utf-8") as file:
                lines = file.readlines()

        self.assertEqual(len(lines), 2)

        first_event = json.loads(lines[0])
        second_event = json.loads(lines[1])

        self.assertEqual(first_event["result"], "ACCEPT")
        self.assertEqual(second_event["result"], "REJECT")


if __name__ == "__main__":
    unittest.main(verbosity=2)
    