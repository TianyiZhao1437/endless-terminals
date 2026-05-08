# test_initial_state.py

import os
import pytest

UPTIME_LOGS_DIR = "/home/user/uptime_logs"
PING_RESULTS_FILE = os.path.join(UPTIME_LOGS_DIR, "ping_results.txt")
STATUS_FREQUENCY_FILE = os.path.join(UPTIME_LOGS_DIR, "status_frequency.txt")

EXPECTED_PING_RESULTS = [
    "2024-06-11 10:00:00 UP",
    "2024-06-11 10:01:00 UP",
    "2024-06-11 10:02:00 UP",
    "2024-06-11 10:03:00 DOWN",
    "2024-06-11 10:04:00 UP",
    "2024-06-11 10:05:00 DOWN",
    "2024-06-11 10:06:00 UP",
    "2024-06-11 10:07:00 UP",
    "2024-06-11 10:08:00 UP",
    "2024-06-11 10:09:00 UP",
]

def test_uptime_logs_dir_exists():
    assert os.path.isdir(UPTIME_LOGS_DIR), (
        f"Required directory '{UPTIME_LOGS_DIR}' does not exist. "
        "Create this directory before proceeding."
    )

def test_ping_results_txt_exists():
    assert os.path.isfile(PING_RESULTS_FILE), (
        f"Required file '{PING_RESULTS_FILE}' does not exist. "
        "You must have this file in place before starting."
    )

def test_ping_results_txt_content():
    with open(PING_RESULTS_FILE, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    assert lines == EXPECTED_PING_RESULTS, (
        f"File '{PING_RESULTS_FILE}' does not contain the expected contents.\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_PING_RESULTS)
        + "\nActual lines:\n"
        + "\n".join(lines)
    )