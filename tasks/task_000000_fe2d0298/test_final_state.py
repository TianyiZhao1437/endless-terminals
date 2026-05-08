# test_final_state.py

import os
import pytest

ERROR_LOG_PATH = "/home/user/devserver/error.log"
UNIQUE_ERRORS_PATH = "/home/user/devserver/unique_errors.txt"

EXPECTED_UNIQUE_ERRORS = [
    "Database connection failed",
    "File not found: /about.html",
    "Invalid user input",
    "Server timeout"
]

def test_unique_errors_txt_exists_and_is_file():
    assert os.path.isfile(UNIQUE_ERRORS_PATH), (
        f"Expected file '{UNIQUE_ERRORS_PATH}' to exist and be a file after the task is completed."
    )

def test_unique_errors_txt_is_readable():
    try:
        with open(UNIQUE_ERRORS_PATH, "r") as f:
            f.read(1)
    except Exception as e:
        pytest.fail(f"File '{UNIQUE_ERRORS_PATH}' is not readable after the task is completed: {e}")

def test_unique_errors_txt_content_exact():
    with open(UNIQUE_ERRORS_PATH, "r") as f:
        actual_lines = f.readlines()
    # Strip line endings and whitespace for each line
    actual_lines = [line.rstrip('\r\n') for line in actual_lines]

    assert actual_lines == EXPECTED_UNIQUE_ERRORS, (
        f"Content of '{UNIQUE_ERRORS_PATH}' is not correct after the task is completed.\n"
        f"--- Expected ---\n{EXPECTED_UNIQUE_ERRORS!r}\n"
        f"--- Actual ---\n{actual_lines!r}\n"
        f"Each line should be a unique error message, sorted alphabetically, with no blank lines or extra spaces."
    )

def test_no_blank_lines_or_extra_spaces():
    with open(UNIQUE_ERRORS_PATH, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        stripped = line.rstrip('\r\n')
        assert stripped == stripped.strip(), (
            f"Line {i+1} in '{UNIQUE_ERRORS_PATH}' has leading or trailing whitespace: {repr(stripped)}"
        )
        assert stripped != "", (
            f"Line {i+1} in '{UNIQUE_ERRORS_PATH}' is blank."
        )

def test_unique_errors_txt_has_no_extra_lines():
    with open(UNIQUE_ERRORS_PATH, "rb") as f:
        content = f.read()
    # No trailing blank lines or whitespace
    if not content:
        pytest.fail(f"File '{UNIQUE_ERRORS_PATH}' is empty.")
    if content.endswith(b"\n\n"):
        pytest.fail(
            f"File '{UNIQUE_ERRORS_PATH}' has extra blank lines at the end."
        )

def test_error_log_untouched():
    # Ensure the error log still exists and is readable
    assert os.path.isfile(ERROR_LOG_PATH), (
        f"Expected file '{ERROR_LOG_PATH}' to still exist after the task."
    )
    try:
        with open(ERROR_LOG_PATH, "r") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"File '{ERROR_LOG_PATH}' is not readable after the task: {e}")
    # Expected content (copied from the task description)
    expected_content = (
        "[2024-06-01 10:05:21] ERROR: File not found: /about.html\n"
        "[2024-06-01 10:06:30] ERROR: Database connection failed\n"
        "[2024-06-01 10:07:42] ERROR: File not found: /about.html\n"
        "[2024-06-01 10:10:01] ERROR: Invalid user input\n"
        "[2024-06-01 10:11:09] ERROR: Database connection failed\n"
        "[2024-06-01 10:13:42] ERROR: Server timeout\n"
    )
    # Normalize line endings for robustness
    expected = expected_content.replace('\r\n', '\n').replace('\r', '\n')
    actual = content.replace('\r\n', '\n').replace('\r', '\n')
    assert actual == expected, (
        f"Content of '{ERROR_LOG_PATH}' has changed after the task. It should remain unchanged.\n"
        f"--- Expected ---\n{expected!r}\n--- Actual ---\n{actual!r}"
    )