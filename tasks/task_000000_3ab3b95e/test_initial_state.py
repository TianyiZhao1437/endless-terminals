"""
test_initial_state.py

Pytest suite to validate the initial OS/filesystem state for the network diagnostics task.

This test ensures that the log file "/home/user/network_investigation.log" does NOT exist before the student begins,
so that automated grading and diagnostics are not contaminated by pre-existing output.
"""

import os
import pytest

LOG_PATH = "/home/user/network_investigation.log"

def test_network_investigation_log_absent():
    """
    The log file /home/user/network_investigation.log must NOT exist before the student starts.
    """
    assert not os.path.exists(LOG_PATH), (
        f"Output log file '{LOG_PATH}' already exists. Please remove it before starting the task."
    )