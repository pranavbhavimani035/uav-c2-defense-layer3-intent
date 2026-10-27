# Layer 3: Intent-Based Authorization for UAV Command and Control

## 1. Project Overview

This module implements Layer 3 of our UAV Command and Control (C2)
defense-in-depth security framework.

Its purpose is to verify whether incoming commands comply with the
UAV's mission rules before they are allowed to execute.

A command may be syntactically valid and authenticated by the
cryptographic layer but still violate mission restrictions. Layer 3
helps detect and reject such commands.

This module is developed and tested in a laptop-based simulation.
No physical drone or real radio communication is required.

## 2. Project Objectives

- Validate incoming UAV commands against mission rules.
- Enforce altitude and speed limits.
- Restrict commands to authorized waypoints.
- Prevent movement outside the mission geofence.
- Enforce valid command transitions based on UAV state.
- Record accepted and rejected commands in a security log.
- Test normal, unauthorized, and malformed commands.

## 3. Main Components

### Command Validator

Located in `validator/validator.py`.

Checks whether a command satisfies the mission's authorization rules,
including command type, waypoint, altitude, speed, and geofence.

### Geofence Module

Located in `geofence/geofence.py`.

Checks whether a target position lies within the permitted mission area.

### Mission State Machine

Located in `mission/state_machine.py`.

Tracks the UAV's simulated state and restricts commands according
to the current state.

### Mission Phase Policy

Located in `mission/phase_policy.py`.

Defines which commands are permitted during different mission phases.

### Security Logger

Located in `security/security_logger.py`.

Records security decisions, including timestamps, commands,
results, reasons, and UAV state.

### Mission Configuration

Located in `intent/mission.json`.

Contains the mission's configuration and authorization limits.

### Automated Tests

Located in the `tests/` directory.

Tests valid commands, invalid commands, geofence boundaries,
state transitions, malformed inputs, and security logging.

## 4. Project Structure

```text
layer3_intent/
├── geofence/
│   └── geofence.py
├── intent/
│   ├── intent_schema.json
│   └── mission.json
├── logs/
│   └── security_log.jsonl
├── mission/
│   ├── phase_policy.py
│   └── state_machine.py
├── security/
│   └── security_logger.py
├── tests/
│   ├── test_attacks.py
│   ├── test_automation.py
│   ├── test_edge_cases.py
│   ├── test_geofence_automation.py
│   ├── test_intent_schema.py
│   ├── test_invalid_command.py
│   ├── test_invalid_intent.py
│   ├── test_phase_policy.py
│   ├── test_rejected_command_state.py
│   ├── test_security_logger_automation.py
│   ├── test_state_machine_automation.py
│   └── test_validator.py
├── validator/
│   └── validator.py
├── demo_layer3.py
├── main.py
├── README.md
└── .gitignore
```

## 5. Requirements

- Python 3
- Visual Studio Code or another Python-compatible editor
- Git (for version control)

The current Layer 3 prototype primarily uses Python's standard library.

## 6. How to Run the Demonstration

Open a terminal in the `layer3_intent` directory.

Run:

```powershell
python demo_layer3.py
```

The demonstration shows how the module handles authorized and
unauthorized commands.

If your current demonstration is launched through `main.py` instead,
use:

```powershell
python main.py
```

## 7. How to Run the Automated Tests

Run the complete test suite:

```powershell
python -m unittest discover -s tests -v
```

A successful test run should end with output similar to:

```text
Ran 34 tests

OK
```

The exact number of tests may increase as the project develops.

## 8. Example Security Scenarios

### Scenario A: Authorized Command

A GOTO command targets an authorized waypoint, stays within the
altitude and speed limits, and remains inside the mission geofence.

Expected result: ACCEPT, provided the current UAV state permits it.

### Scenario B: Geofence Violation

A GOTO command targets a position outside the permitted mission area.

Expected result: REJECT.

### Scenario C: Altitude Violation

A command requests an altitude above the mission's maximum limit.

Expected result: REJECT.

### Scenario D: Invalid Mission State

A GOTO command is issued while the UAV is in the IDLE state.

Expected result: REJECT.

## 9. Security Logging

Security decisions are appended to:

`logs/security_log.jsonl`

Each event records information such as:

- Timestamp
- Command
- ACCEPT or REJECT result
- Reason for the decision
- UAV state

## 10. Role in the Overall Project

Layer 3 is responsible for mission-aware command authorization.

It complements the other security layers:

- Layer 1: Reinforcement-learning-based anti-jamming.
- Layer 2: Post-quantum cryptography and authenticated encryption.
- Layer 3: Intent-based command authorization.

Together, these layers aim to improve communication availability,
cryptographic protection, and mission-level command security.

## 11. Current Development Status

The Layer 3 prototype includes command validation, geofence checking,
mission state management, security logging, and automated tests.

The current automated test suite has passed in the local development
environment. Integration with the other layers remains a separate
project milestone.
## Layer 3 Integration Interface

### Purpose

Layer 3 validates UAV commands against mission constraints and the current mission state before allowing them to proceed.

### Function

`authorize_command(command, mission, machine)`

### Parameters

* `command`: A dictionary containing the requested command and its parameters.
* `mission`: A dictionary loaded from the mission configuration.
* `machine`: An initialized `MissionStateMachine` instance.

### Return Value

The function returns a dictionary containing:

* `result`: `ACCEPT` or `REJECT`
* `reason`: Explanation for the decision
* `state`: Current UAV state after processing the command
* `state_message`: State-transition message for accepted commands

### Expected Behavior

1. Validate the command against mission constraints.
2. Check whether the command is permitted in the current mission state.
3. Reject invalid or unauthorized commands.
4. Preserve the current state when a command is rejected.
5. Return a structured decision for the integration module.

### Example Usage

```python
import json

from integration_interface import authorize_command
from mission.state_machine import MissionStateMachine

with open("intent/mission.json", "r", encoding="utf-8") as file:
    mission = json.load(file)

machine = MissionStateMachine()

command = {
    "type": "TAKEOFF",
    "altitude": 80
}

result = authorize_command(command, mission, machine)

print(result)
```

Run this example from the `layer3_intent` project directory.
