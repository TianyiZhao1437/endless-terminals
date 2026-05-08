# test_initial_state.py

import os
import pytest

APP_DIR = "/home/user/app"
LOG_FILE = "/home/user/app/application.log"

EXPECTED_LOG_CONTENT = """2023-07-16 14:55:12 INFO - Starting application initialization
2023-07-16 14:55:12 ERROR - Failed to connect to database
2023-07-16 14:55:13 WARN - Retry connection
2023-07-16 14:55:15 ERROR - User 'admin' authentication failed
2023-07-16 14:56:01 INFO - Application running
2023-07-16 14:56:05 ERROR - Timeout while waiting for response
"""

def test_app_directory_exists_and_writable():
    assert os.path.isdir(APP_DIR), (
        f"Required directory '{APP_DIR}' does not exist. "
        "Please create it before proceeding."
    )
    assert os.access(APP_DIR, os.W_OK), (
        f"Directory '{APP_DIR}' exists but is not writable by the user. "
        "Please ensure correct permissions."
    )

def test_application_log_exists_and_content():
    assert os.path.isfile(LOG_FILE), (
        f"Required log file '{LOG_FILE}' does not exist. "
        "Please create it with the specified contents before proceeding."
    )
    assert os.access(LOG_FILE, os.R_OK), (
        f"Log file '{LOG_FILE}' exists but is not readable by the user. "
        "Please check permissions."
    )
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        actual_content = f.read()
    # Normalize line endings and trailing whitespace for comparison
    expected_lines = EXPECTED_LOG_CONTENT.strip().splitlines()
    actual_lines = actual_content.strip().splitlines()
    assert actual_lines == expected_lines, (
        f"Log file '{LOG_FILE}' does not have the expected contents.\n"
        "Expected contents:\n"
        + "\n".join(expected_lines)
        + "\nActual contents:\n"
        + "\n".join(actual_lines)
    )