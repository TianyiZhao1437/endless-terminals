# test_initial_state.py

import os
import pytest

ERROR_LOG_PATH = "/home/user/devserver/error.log"
EXPECTED_LOG_CONTENT = """[2024-06-01 10:05:21] ERROR: File not found: /about.html
[2024-06-01 10:06:30] ERROR: Database connection failed
[2024-06-01 10:07:42] ERROR: File not found: /about.html
[2024-06-01 10:10:01] ERROR: Invalid user input
[2024-06-01 10:11:09] ERROR: Database connection failed
[2024-06-01 10:13:42] ERROR: Server timeout
"""

def test_error_log_exists_and_is_file():
    assert os.path.isfile(ERROR_LOG_PATH), (
        f"Expected file '{ERROR_LOG_PATH}' to exist and be a file."
    )

def test_error_log_is_readable():
    try:
        with open(ERROR_LOG_PATH, "r") as f:
            # Just try to read one byte
            f.read(1)
    except Exception as e:
        pytest.fail(f"File '{ERROR_LOG_PATH}' is not readable: {e}")

def test_error_log_content_exact():
    with open(ERROR_LOG_PATH, "r") as f:
        actual_content = f.read()
    # Make sure to normalize line endings for robustness
    expected = EXPECTED_LOG_CONTENT.replace('\r\n', '\n').replace('\r', '\n')
    actual = actual_content.replace('\r\n', '\n').replace('\r', '\n')
    assert actual == expected, (
        f"Content of '{ERROR_LOG_PATH}' does not match expected content.\n"
        f"--- Expected ---\n{expected!r}\n--- Actual ---\n{actual!r}"
    )

def test_unique_errors_txt_does_not_exist_yet():
    unique_errors = "/home/user/devserver/unique_errors.txt"
    assert not os.path.exists(unique_errors), (
        f"File '{unique_errors}' should NOT exist before the task is performed."
    )