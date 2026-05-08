# test_initial_state.py

import os
import pytest

UPTIME_LOG_PATH = "/home/user/uptime_log.txt"

@pytest.mark.describe("Initial environment validation for uptime log extraction task")
def test_uptime_log_exists():
    """Check that the uptime log file exists at the expected location."""
    assert os.path.isfile(UPTIME_LOG_PATH), (
        f"Missing required log file: {UPTIME_LOG_PATH}. "
        "You must ensure this file exists before proceeding."
    )

def test_uptime_log_contents():
    """Check that the uptime log file contains the required contents."""
    expected_lines = [
        "2024-05-27 14:01:20 server01 12233",
        "2024-05-27 14:01:27 server02 9940",
        "2024-05-27 14:01:36 server03 5831"
    ]
    with open(UPTIME_LOG_PATH, "r", encoding="utf-8") as f:
        actual_lines = [line.rstrip('\n') for line in f]

    assert actual_lines == expected_lines, (
        f"The contents of {UPTIME_LOG_PATH} do not match the expected input.\n"
        f"Expected:\n"
        + "\n".join(expected_lines) +
        "\nActual:\n"
        + "\n".join(actual_lines)
    )