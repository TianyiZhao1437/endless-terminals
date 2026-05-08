# test_initial_state.py

import os
import pytest

APP_LOG_PATH = "/home/user/test_logs/app.log"
ERROR_REPORT_LOG_PATH = "/home/user/test_logs/error_report.log"
TEST_LOGS_DIR = "/home/user/test_logs"

EXPECTED_APP_LOG_CONTENT = (
    "[2024-06-01 12:00:14] [INFO] Service started successfully\n"
    "[2024-06-01 12:01:22] [ERROR] Failed to connect to database\n"
    "[2024-06-01 12:02:05] [WARNING] Database retrying connection\n"
    "[2024-06-01 12:02:10] [ERROR] Unable to open configuration file\n"
    "[2024-06-01 12:03:45] [INFO] Service is running\n"
)

def test_test_logs_directory_exists_and_is_directory():
    assert os.path.exists(TEST_LOGS_DIR), (
        f"Required directory '{TEST_LOGS_DIR}' does not exist. "
        "Create it before proceeding."
    )
    assert os.path.isdir(TEST_LOGS_DIR), (
        f"'{TEST_LOGS_DIR}' exists but is not a directory."
    )

def test_app_log_exists_and_content():
    assert os.path.exists(APP_LOG_PATH), (
        f"Required log file '{APP_LOG_PATH}' does not exist. "
        "Create it with the specified content before proceeding."
    )
    assert os.path.isfile(APP_LOG_PATH), (
        f"'{APP_LOG_PATH}' exists but is not a file."
    )
    with open(APP_LOG_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()
    assert actual_content == EXPECTED_APP_LOG_CONTENT, (
        f"File '{APP_LOG_PATH}' does not have the expected content.\n"
        "Expected content:\n"
        f"{EXPECTED_APP_LOG_CONTENT!r}\n"
        "Actual content:\n"
        f"{actual_content!r}"
    )

def test_error_report_log_does_not_exist_yet():
    assert not os.path.exists(ERROR_REPORT_LOG_PATH), (
        f"Output file '{ERROR_REPORT_LOG_PATH}' already exists. "
        "Remove it before running the task to ensure a clean state."
    )