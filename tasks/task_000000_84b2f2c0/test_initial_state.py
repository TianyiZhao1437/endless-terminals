# test_initial_state.py

import os
import pytest

MONITOR_CONFIG_PATH = "/home/user/network/monitor_config.ini"

EXPECTED_CONTENT = (
    "[network]\n"
    "interface=eth0\n"
    "gateway=192.168.59.1\n"
    "dns=8.8.8.8\n"
    "\n"
    "[alert]\n"
    "email=admin@example.com\n"
    "threshold=75\n"
)

def test_monitor_config_file_exists():
    """Verify that /home/user/network/monitor_config.ini exists before task starts."""
    assert os.path.isfile(MONITOR_CONFIG_PATH), (
        f"Missing required file: {MONITOR_CONFIG_PATH}. "
        "Ensure the configuration file exists before proceeding."
    )

def test_monitor_config_file_content():
    """Verify the contents of /home/user/network/monitor_config.ini are correct before task starts."""
    with open(MONITOR_CONFIG_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()
    assert actual_content == EXPECTED_CONTENT, (
        f"The contents of {MONITOR_CONFIG_PATH} do not match the expected configuration.\n"
        "Expected:\n"
        f"{EXPECTED_CONTENT!r}\n"
        "Actual:\n"
        f"{actual_content!r}\n"
        "Please ensure the file is present and contains the correct configuration."
    )