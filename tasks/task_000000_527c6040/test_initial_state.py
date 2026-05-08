# test_initial_state.py

import os
import pytest

TARGETS_TXT_PATH = "/home/user/targets.txt"
EXPECTED_TARGETS = [
    "192.168.0.10",
    "192.168.0.20",
    "test-host.local"
]

SCAN_SCRIPT_PATH = "/home/user/scan_targets.sh"
SCAN_LOG_PATH = "/home/user/scan_log.txt"

def test_targets_txt_exists():
    assert os.path.isfile(TARGETS_TXT_PATH), (
        f"Required file not found: {TARGETS_TXT_PATH}. "
        "Please ensure the target list file exists at this path."
    )

def test_targets_txt_contents():
    with open(TARGETS_TXT_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\r\n") for line in f.readlines()]
    assert lines == EXPECTED_TARGETS, (
        f"The file {TARGETS_TXT_PATH} does not have the expected contents.\n"
        f"Expected:\n" +
        "\n".join(EXPECTED_TARGETS) +
        "\nFound:\n" +
        "\n".join(lines)
    )

def test_scan_targets_script_not_present():
    assert not os.path.exists(SCAN_SCRIPT_PATH), (
        f"The script {SCAN_SCRIPT_PATH} already exists. "
        "Please remove it before starting the task."
    )

def test_scan_log_not_present():
    assert not os.path.exists(SCAN_LOG_PATH), (
        f"The log file {SCAN_LOG_PATH} already exists. "
        "Please remove it before starting the task."
    )