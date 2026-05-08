# test_final_state.py

import os
import stat
import pytest

APP_DIR = "/home/user/app"
LOG_FILE = "/home/user/app/application.log"
ERRORS_CSV = "/home/user/app/errors_extracted.csv"

EXPECTED_ERRORS = [
    "2023-07-16,14:55:12,Failed to connect to database",
    "2023-07-16,14:55:15,User 'admin' authentication failed",
    "2023-07-16,14:56:05,Timeout while waiting for response",
]

def test_errors_extracted_csv_exists():
    assert os.path.isfile(ERRORS_CSV), (
        f"Expected output file '{ERRORS_CSV}' does not exist.\n"
        "You must create this file with the extracted and formatted error data."
    )

def test_errors_extracted_csv_writable():
    assert os.access(ERRORS_CSV, os.W_OK), (
        f"File '{ERRORS_CSV}' exists but is not writable by the user.\n"
        "Please ensure correct permissions on the output file."
    )

def test_errors_extracted_csv_content():
    with open(ERRORS_CSV, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines == EXPECTED_ERRORS, (
        f"File '{ERRORS_CSV}' does not contain the expected extracted errors.\n"
        f"Expected:\n" +
        "\n".join(EXPECTED_ERRORS) +
        "\nActual:\n" +
        "\n".join(lines)
    )
    # Check for blank lines or extra whitespace
    for i, line in enumerate(lines):
        assert line.strip() == line, (
            f"Line {i+1} in '{ERRORS_CSV}' contains unexpected leading/trailing whitespace:\n"
            f"'{line}'"
        )
        assert line, (
            f"Line {i+1} in '{ERRORS_CSV}' is blank. There should be no blank lines."
        )

def test_errors_extracted_csv_no_extra_lines():
    with open(ERRORS_CSV, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == len(EXPECTED_ERRORS), (
        f"File '{ERRORS_CSV}' should have exactly {len(EXPECTED_ERRORS)} lines, but has {len(lines)}.\n"
        f"File content:\n{''.join(lines)}"
    )

def test_no_unexpected_files_created():
    # Only application.log and errors_extracted.csv are allowed in /home/user/app
    allowed_files = {"application.log", "errors_extracted.csv"}
    actual_files = set(os.listdir(APP_DIR))
    extra_files = actual_files - allowed_files
    assert not extra_files, (
        f"Unexpected files found in '{APP_DIR}': {sorted(extra_files)}\n"
        "Only 'application.log' and 'errors_extracted.csv' should exist after the task."
    )

def test_application_log_untouched():
    # Ensure the original log file is still present and unchanged
    expected_content = (
        "2023-07-16 14:55:12 INFO - Starting application initialization\n"
        "2023-07-16 14:55:12 ERROR - Failed to connect to database\n"
        "2023-07-16 14:55:13 WARN - Retry connection\n"
        "2023-07-16 14:55:15 ERROR - User 'admin' authentication failed\n"
        "2023-07-16 14:56:01 INFO - Application running\n"
        "2023-07-16 14:56:05 ERROR - Timeout while waiting for response\n"
    )
    assert os.path.isfile(LOG_FILE), (
        f"Original log file '{LOG_FILE}' is missing after task completion."
    )
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        actual_content = f.read()
    # Normalize line endings and trailing whitespace for comparison
    expected_lines = expected_content.strip().splitlines()
    actual_lines = actual_content.strip().splitlines()
    assert actual_lines == expected_lines, (
        f"Log file '{LOG_FILE}' should remain unchanged after the task.\n"
        "Expected contents:\n"
        + "\n".join(expected_lines)
        + "\nActual contents:\n"
        + "\n".join(actual_lines)
    )