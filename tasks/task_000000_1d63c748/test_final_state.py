# test_final_state.py

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

EXPECTED_UPTIME_SUMMARY_CONTENT = [
    "web01 DOWN 2",
    "web01 UP 2",
    "web02 DOWN 1",
    "web02 UP 1",
    "web03 DOWN 1",
    "web03 UP 2",
]

@pytest.mark.parametrize("path", [
    MONITORING_DIR,
])
def test_monitoring_directory_exists(path):
    assert os.path.isdir(path), (
        f"Missing required directory: {path}. "
        "The final state must include this directory."
    )

def test_uptime_checks_log_exists_and_unchanged():
    assert os.path.isfile(UPTIME_CHECKS_LOG), (
        f"Missing required log file: {UPTIME_CHECKS_LOG}. "
        "This file must remain present after the task."
    )
    with open(UPTIME_CHECKS_LOG, "r") as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    assert lines == EXPECTED_UPTIME_CHECKS_CONTENT, (
        f"The contents of {UPTIME_CHECKS_LOG} have changed after the task.\n"
        "This file must not be modified.\n"
        "Expected contents:\n" +
        "\n".join(EXPECTED_UPTIME_CHECKS_CONTENT) +
        "\nActual contents:\n" +
        "\n".join(lines)
    )

def test_uptime_summary_log_exists():
    assert os.path.isfile(UPTIME_SUMMARY_LOG), (
        f"The summary log file {UPTIME_SUMMARY_LOG} does not exist.\n"
        "You must create this file as part of the task."
    )

def test_uptime_summary_log_content_exact():
    assert os.path.isfile(UPTIME_SUMMARY_LOG), (
        f"The summary log file {UPTIME_SUMMARY_LOG} does not exist."
    )
    with open(UPTIME_SUMMARY_LOG, "r") as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    assert lines == EXPECTED_UPTIME_SUMMARY_CONTENT, (
        f"The contents of {UPTIME_SUMMARY_LOG} do not match the expected summary.\n"
        "Expected contents (in order):\n" +
        "\n".join(EXPECTED_UPTIME_SUMMARY_CONTENT) +
        "\nActual contents:\n" +
        "\n".join(lines) +
        "\n\n"
        "Check that you are:\n"
        "- Counting each server's UP and DOWN lines correctly.\n"
        "- Writing one line per server+status in the format: '<server> <status> <count>'.\n"
        "- Sorting by server name, then by status ('DOWN' before 'UP')."
    )

def test_uptime_summary_log_no_extra_lines():
    with open(UPTIME_SUMMARY_LOG, "r") as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
    assert len(lines) == 6, (
        f"{UPTIME_SUMMARY_LOG} should have exactly 6 lines "
        f"(one for each server/status combination), but found {len(lines)} lines."
    )
    # Check for duplicate server/status combinations
    seen = set()
    for line in lines:
        parts = line.split()
        assert len(parts) == 3, (
            f"Line in {UPTIME_SUMMARY_LOG} does not have 3 fields: '{line}'"
        )
        key = (parts[0], parts[1])
        assert key not in seen, (
            f"Duplicate entry for server/status '{parts[0]} {parts[1]}' in {UPTIME_SUMMARY_LOG}."
        )
        seen.add(key)