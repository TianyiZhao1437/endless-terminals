# test_final_state.py

import os
import pytest
import stat
import pwd

APP_LOG_PATH = "/home/user/test_logs/app.log"
ERROR_REPORT_LOG_PATH = "/home/user/test_logs/error_report.log"
TEST_LOGS_DIR = "/home/user/test_logs"

EXPECTED_ERROR_LOG_CONTENT = (
    "[2024-06-01 12:01:22] [ERROR] Failed to connect to database\n"
    "[2024-06-01 12:02:10] [ERROR] Unable to open configuration file\n"
)

def test_error_report_log_exists():
    assert os.path.exists(ERROR_REPORT_LOG_PATH), (
        f"File '{ERROR_REPORT_LOG_PATH}' does not exist. "
        "You must create this file at the exact path."
    )
    assert os.path.isfile(ERROR_REPORT_LOG_PATH), (
        f"'{ERROR_REPORT_LOG_PATH}' exists but is not a file."
    )

def test_error_report_log_content_exact():
    with open(ERROR_REPORT_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_ERROR_LOG_CONTENT, (
        "Content of 'error_report.log' is incorrect.\n"
        "Expected:\n"
        f"{EXPECTED_ERROR_LOG_CONTENT!r}\n"
        "Actual:\n"
        f"{content!r}\n"
        "Make sure you include only the log lines with log level 'ERROR', "
        "in their original order and format, with no extra whitespace or empty lines."
    )

def test_error_report_log_only_error_lines():
    # Check that every line matches the 'ERROR' log format and nothing else is present.
    with open(ERROR_REPORT_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines):
        line = line.rstrip("\n")
        assert line.startswith("[2024-06-01 "), (
            f"Line {idx+1} in 'error_report.log' does not start with a valid timestamp: {line!r}"
        )
        assert "] [ERROR] " in line, (
            f"Line {idx+1} in 'error_report.log' does not have log level 'ERROR': {line!r}"
        )
    # Check for empty lines
    empty_lines = [i+1 for i, l in enumerate(lines) if l.strip() == ""]
    assert not empty_lines, (
        f"'error_report.log' contains empty line(s) at: {empty_lines}. "
        "There should be no empty lines."
    )

def test_error_report_log_permissions_and_owner():
    st = os.stat(ERROR_REPORT_LOG_PATH)
    owner_uid = st.st_uid
    current_uid = os.getuid()
    owner_name = pwd.getpwuid(owner_uid).pw_name
    current_name = pwd.getpwuid(current_uid).pw_name
    assert owner_uid == current_uid, (
        f"'error_report.log' is owned by '{owner_name}', but should be owned by the current user '{current_name}'."
    )
    mode = st.st_mode
    is_readable = bool(mode & stat.S_IRUSR)
    is_writable = bool(mode & stat.S_IWUSR)
    assert is_readable, (
        f"'error_report.log' is not readable by the owner."
    )
    assert is_writable, (
        f"'error_report.log' is not writable by the owner."
    )

def test_error_report_log_location():
    assert os.path.dirname(ERROR_REPORT_LOG_PATH) == TEST_LOGS_DIR, (
        f"'error_report.log' is not located in '{TEST_LOGS_DIR}'. "
        f"Found in '{os.path.dirname(ERROR_REPORT_LOG_PATH)}'."
    )