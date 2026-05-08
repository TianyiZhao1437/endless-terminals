# test_final_state.py

import os
import pytest

CONFIG_V1_PATH = "/home/user/configs/config_v1.conf"
CONFIG_V2_PATH = "/home/user/configs/config_v2.conf"
CHANGES_LOG_PATH = "/home/user/config_changes.log"

# The expected content of the summary file after correct completion.
EXPECTED_LOG_CONTENT = (
    "ADDED: server.port=8081\n"
    "ADDED: log.level=debug\n"
)

def read_file(path):
    """Read file and normalize line endings to Unix LF."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().replace('\r\n', '\n').replace('\r', '\n')

def test_config_changes_log_exists():
    assert os.path.isfile(CHANGES_LOG_PATH), (
        f"File '{CHANGES_LOG_PATH}' does not exist. "
        "You must create this summary file after completing the task."
    )

def test_config_changes_log_content_exact():
    actual = read_file(CHANGES_LOG_PATH)
    expected = EXPECTED_LOG_CONTENT
    assert actual == expected, (
        f"File '{CHANGES_LOG_PATH}' exists but its contents are incorrect.\n"
        f"Expected exactly:\n{expected}\nActual:\n{actual}\n"
        "Make sure only the added lines from config_v2.conf (compared to config_v1.conf) "
        "are listed, each prefixed by 'ADDED: ', and in the correct order."
    )

def test_config_changes_log_no_extra_lines():
    """
    Ensure that only the two expected lines are present, no extra blank lines or other content.
    """
    actual_lines = read_file(CHANGES_LOG_PATH).split('\n')
    # Remove possible trailing empty lines
    actual_lines = [line for line in actual_lines if line]
    expected_lines = [
        "ADDED: server.port=8081",
        "ADDED: log.level=debug",
    ]
    assert actual_lines == expected_lines, (
        f"File '{CHANGES_LOG_PATH}' contains extra lines or missing lines.\n"
        f"Expected lines:\n{expected_lines}\nActual lines:\n{actual_lines}\n"
        "There must be exactly two lines, each starting with 'ADDED: ', and nothing else."
    )

def test_config_changes_log_no_other_files_created():
    """
    Ensure that only /home/user/config_changes.log was created in /home/user/, no other .log or summary files.
    """
    user_dir = "/home/user/"
    files = [f for f in os.listdir(user_dir) if os.path.isfile(os.path.join(user_dir, f))]
    log_files = [f for f in files if f.endswith('.log')]
    assert log_files == ['config_changes.log'], (
        f"Unexpected log or summary files found in '{user_dir}'. "
        f"Only 'config_changes.log' should exist. Found: {log_files}"
    )

def test_config_changes_log_permissions():
    """
    Ensure the log file is readable by the user.
    """
    assert os.access(CHANGES_LOG_PATH, os.R_OK), (
        f"File '{CHANGES_LOG_PATH}' exists but is not readable. "
        "Check file permissions."
    )