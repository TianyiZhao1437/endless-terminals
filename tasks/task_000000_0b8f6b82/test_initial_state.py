# test_initial_state.py

import os
import pytest

APP_LOGS_DIR = "/home/user/app/logs"
APP_LOG_PATH = "/home/user/app/logs/app.log"

EXPECTED_APP_LOG_CONTENT = """[2024-05-01 12:05:21] ERROR: connection failed from 10.0.0.1
[2024-05-01 12:10:00] INFO: user login from 192.168.1.10
[2024-05-01 12:12:35] ERROR: timeout from 172.16.0.5
[2024-05-01 12:12:37] ERROR: DROP from 192.168.1.10
[2024-05-01 12:13:01] WARN: attempt from 172.16.0.5
[2024-05-01 12:13:10] ERROR: failed auth from 10.0.0.2
"""

def test_logs_directory_exists_and_writable():
    assert os.path.isdir(APP_LOGS_DIR), (
        f"Directory '{APP_LOGS_DIR}' does not exist. Please create it before running the task."
    )
    assert os.access(APP_LOGS_DIR, os.W_OK), (
        f"Directory '{APP_LOGS_DIR}' is not writable. Ensure the user has write permissions."
    )

def test_app_log_file_exists_and_permissions():
    assert os.path.isfile(APP_LOG_PATH), (
        f"Log file '{APP_LOG_PATH}' does not exist. Please create it before running the task."
    )
    assert os.access(APP_LOG_PATH, os.R_OK), (
        f"Log file '{APP_LOG_PATH}' is not readable. Ensure the user has read permissions."
    )
    assert os.access(APP_LOG_PATH, os.W_OK), (
        f"Log file '{APP_LOG_PATH}' is not writable. Ensure the user has write permissions."
    )

def test_app_log_file_content():
    with open(APP_LOG_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()
    # Remove trailing newline for comparison
    expected = EXPECTED_APP_LOG_CONTENT
    actual = actual_content
    # Normalize line endings, remove trailing whitespace
    expected_lines = [line.rstrip() for line in expected.splitlines()]
    actual_lines = [line.rstrip() for line in actual.splitlines()]
    assert actual_lines == expected_lines, (
        f"Log file '{APP_LOG_PATH}' does not have the expected content.\n"
        "Expected lines:\n" +
        "\n".join(expected_lines) +
        "\nActual lines:\n" +
        "\n".join(actual_lines) +
        "\nEnsure the log file matches the pre-task setup."
    )

def test_error_ips_file_does_not_exist_yet():
    error_ips_path = os.path.join(APP_LOGS_DIR, "error_ips.txt")
    assert not os.path.exists(error_ips_path), (
        f"File '{error_ips_path}' already exists. Please remove it before starting the task."
    )