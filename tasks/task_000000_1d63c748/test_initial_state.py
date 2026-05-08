# test_initial_state.py

import os
import pytest

MONITORING_DIR = "/home/user/monitoring"
UPTIME_CHECKS_LOG = "/home/user/monitoring/uptime_checks.log"
UPTIME_SUMMARY_LOG = "/home/user/monitoring/uptime_summary.log"

EXPECTED_UPTIME_CHECKS_CONTENT = [
    "2024-06-10 08:00:01 web01 UP",
    "2024-06-10 08:05:01 web02 DOWN",
    "2024-06-10 08:10:01 web01 DOWN",
    "2024-06-10 08:15:01 web03 UP",
    "2024-06-10 08:20:01 web01 UP",
    "2024-06-10 08:25:01 web02 UP",
    "2024-06-10 08:30:01 web03 DOWN",
    "2024-06-10 08:35:01 web01 DOWN",
    "2024-06-10 08:40:01 web03 UP",
]

@pytest.mark.parametrize("path", [
    MONITORING_DIR,
])
def test_monitoring_directory_exists(path):
    assert os.path.isdir(path), (
        f"Missing required directory: {path}. "
        "Please ensure this directory exists before proceeding."
    )

def test_uptime_checks_log_exists():
    assert os.path.isfile(UPTIME_CHECKS_LOG), (
        f"Missing required log file: {UPTIME_CHECKS_LOG}. "
        "Please create this file with the specified content before proceeding."
    )

def test_uptime_checks_log_content():
    with open(UPTIME_CHECKS_LOG, "r") as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    assert lines == EXPECTED_UPTIME_CHECKS_CONTENT, (
        f"The contents of {UPTIME_CHECKS_LOG} do not match the expected initial state.\n"
        "Expected contents:\n" +
        "\n".join(EXPECTED_UPTIME_CHECKS_CONTENT) +
        "\nActual contents:\n" +
        "\n".join(lines)
    )

@pytest.mark.parametrize("path", [
    UPTIME_SUMMARY_LOG,
])
def test_uptime_summary_log_does_not_exist(path):
    assert not os.path.exists(path), (
        f"The summary log file {path} should not exist before you start the task.\n"
        "Please remove this file if it is present before proceeding."
    )