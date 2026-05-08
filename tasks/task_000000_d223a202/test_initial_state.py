# test_initial_state.py

import os
import pytest

LOG_DIR = "/home/user/test_logs"
LOG_FILE = "/home/user/test_logs/test_suite.log"
FAILED_TESTS_FILE = "/home/user/test_logs/failed_tests.txt"

EXPECTED_LOG_CONTENT = (
    "test_login: PASSED\n"
    "test_payment: FAILED\n"
    "test_logout: FAILED\n"
    "test_signup: PASSED\n"
)

@pytest.mark.describe("Initial OS and filesystem state before student action")
def test_log_directory_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory '{LOG_DIR}' does not exist. "
        "Please ensure the directory is present before proceeding."
    )

def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"Required log file '{LOG_FILE}' does not exist. "
        "Please ensure the log file is present before proceeding."
    )

def test_log_file_contents():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        contents = f.read()
    assert contents == EXPECTED_LOG_CONTENT, (
        f"Log file '{LOG_FILE}' does not contain the expected contents.\n"
        "Expected:\n"
        f"{EXPECTED_LOG_CONTENT!r}\n"
        "Actual:\n"
        f"{contents!r}\n"
        "Please ensure the log file matches exactly, including blank lines and order."
    )

def test_failed_tests_file_does_not_exist():
    assert not os.path.exists(FAILED_TESTS_FILE), (
        f"Output file '{FAILED_TESTS_FILE}' already exists. "
        "It should not exist before the task is performed."
    )