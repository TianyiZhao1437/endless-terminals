# test_final_state.py

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

EXPECTED_FAILED_TESTS_CONTENT = (
    "test_payment\n"
    "test_logout\n"
)

@pytest.mark.describe("Final OS and filesystem state after student action")
def test_log_directory_still_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory '{LOG_DIR}' does not exist after the task. "
        "It must remain present."
    )

def test_log_file_still_exists_and_unchanged():
    assert os.path.isfile(LOG_FILE), (
        f"Log file '{LOG_FILE}' is missing after the task. "
        "It must not be deleted or moved."
    )
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        contents = f.read()
    assert contents == EXPECTED_LOG_CONTENT, (
        f"Log file '{LOG_FILE}' was modified during the task.\n"
        "Expected contents (including exact newlines):\n"
        f"{EXPECTED_LOG_CONTENT!r}\n"
        "Actual contents:\n"
        f"{contents!r}\n"
        "The log file must remain unchanged."
    )

def test_failed_tests_file_created_with_correct_content_and_format():
    assert os.path.isfile(FAILED_TESTS_FILE), (
        f"Output file '{FAILED_TESTS_FILE}' was not created. "
        "You must create this file as specified."
    )
    with open(FAILED_TESTS_FILE, "r", encoding="utf-8") as f:
        actual = f.read()
    assert actual == EXPECTED_FAILED_TESTS_CONTENT, (
        f"Output file '{FAILED_TESTS_FILE}' does not contain the expected failed test names.\n"
        "Expected (including exact newlines, no extra whitespace):\n"
        f"{EXPECTED_FAILED_TESTS_CONTENT!r}\n"
        "Actual:\n"
        f"{actual!r}\n"
        "Ensure you write only the failed test names, one per line, in the correct order, "
        "with no extra whitespace or blank lines."
    )

def test_failed_tests_file_has_only_failed_test_names():
    with open(FAILED_TESTS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Remove trailing newlines for comparison
    stripped_lines = [line.rstrip('\n') for line in lines]
    expected_lines = ["test_payment", "test_logout"]
    assert stripped_lines == expected_lines, (
        f"'{FAILED_TESTS_FILE}' must contain only the names of failed tests, "
        "in the correct order, one per line.\n"
        f"Expected lines: {expected_lines}\n"
        f"Actual lines:   {stripped_lines}"
    )

def test_failed_tests_file_has_no_extra_whitespace():
    with open(FAILED_TESTS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        assert line == line.strip() + "\n", (
            f"Line {i+1} in '{FAILED_TESTS_FILE}' has extra whitespace: {repr(line)}\n"
            "Each line must contain only the test name, with no leading or trailing spaces."
        )