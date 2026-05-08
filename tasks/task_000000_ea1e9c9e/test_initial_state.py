# test_initial_state.py

import os
import pytest

ERROR_LOG_PATH = "/home/user/diagnostics/error.log"
DIAGNOSTICS_DIR = "/home/user/diagnostics"

expected_error_log_contents = (
    "2024-06-01 08:15:23 ERROR: Disk failure detected on /dev/sda\n"
    "2024-06-01 08:16:00 INFO: System check started\n"
    "2024-06-01 09:02:11 ERROR: Connection timed out while accessing database\n"
    "2024-06-01 11:00:00 WARNING: High CPU usage detected\n"
)


def test_diagnostics_directory_exists():
    assert os.path.isdir(DIAGNOSTICS_DIR), (
        f"Required directory '{DIAGNOSTICS_DIR}' does not exist. "
        "Please create it before proceeding."
    )


def test_error_log_file_exists():
    assert os.path.isfile(ERROR_LOG_PATH), (
        f"Required file '{ERROR_LOG_PATH}' does not exist. "
        "Please ensure the log file is present before proceeding."
    )


def test_error_log_file_contents():
    if not os.path.isfile(ERROR_LOG_PATH):
        pytest.skip(f"File '{ERROR_LOG_PATH}' does not exist. Skipping content check.")
    with open(ERROR_LOG_PATH, "r", encoding="utf-8") as f:
        contents = f.read()
    assert contents == expected_error_log_contents, (
        f"File '{ERROR_LOG_PATH}' contents do not match the expected contents.\n"
        "Expected:\n"
        f"{expected_error_log_contents!r}\n"
        "Found:\n"
        f"{contents!r}\n"
        "Please ensure the file contains exactly the expected log entries, with no extra or missing lines or spaces."
    )