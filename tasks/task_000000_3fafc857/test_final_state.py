# test_final_state.py

import os
import pytest

LOG_FILE = "/home/user/process_investigation.log"
EXPECTED_CONTENT = (
    "PID,USER,COMMAND,%MEM\n"
    "382,user,firefox,12.88\n"
    "1893,user,python3,6.17\n"
    "443,user,code,4.78\n"
)

def test_log_file_exists():
    """The process investigation log file must exist after the investigation."""
    assert os.path.isfile(LOG_FILE), (
        f"The log file '{LOG_FILE}' does not exist.\n"
        "You must create this file after completing the investigation."
    )

def test_log_file_permissions():
    """The log file must be readable and writable by the owner."""
    assert os.access(LOG_FILE, os.R_OK), (
        f"The log file '{LOG_FILE}' is not readable."
    )
    assert os.access(LOG_FILE, os.W_OK), (
        f"The log file '{LOG_FILE}' is not writable."
    )

def test_log_file_content_exact():
    """The log file must contain exactly the expected CSV content and format."""
    with open(LOG_FILE, "r", encoding="ascii") as f:
        actual = f.read()

    # Check for exact match
    if actual != EXPECTED_CONTENT:
        # Determine what's wrong with the file content
        actual_lines = actual.splitlines()
        expected_lines = EXPECTED_CONTENT.splitlines()
        if len(actual_lines) != 4:
            pytest.fail(
                f"The log file must contain exactly 4 lines: "
                f"1 header + 3 process entries.\n"
                f"Found {len(actual_lines)} lines.\n"
                f"Actual content:\n{actual}"
            )
        for i, (exp, act) in enumerate(zip(expected_lines, actual_lines)):
            if exp != act:
                pytest.fail(
                    f"Line {i+1} does not match expected format/content.\n"
                    f"Expected: '{exp}'\n"
                    f"Actual  : '{act}'\n"
                    "Ensure fields are comma-separated, no extra whitespace, and values are correct."
                )
        # If the lines match but the file differs, it's probably trailing newlines or encoding
        pytest.fail(
            "The log file content does not match exactly.\n"
            "Check for extra whitespace, trailing newlines, or encoding issues.\n"
            f"Expected content:\n{EXPECTED_CONTENT}\n"
            f"Actual content:\n{actual}"
        )

def test_log_file_ascii():
    """The log file must contain only ASCII characters."""
    with open(LOG_FILE, "rb") as f:
        content = f.read()
    try:
        content.decode("ascii")
    except UnicodeDecodeError:
        pytest.fail(
            f"The log file '{LOG_FILE}' contains non-ASCII characters.\n"
            "Only plain ASCII text is allowed."
        )

def test_log_file_no_trailing_spaces():
    """No line in the log file should have trailing spaces."""
    with open(LOG_FILE, "r", encoding="ascii") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.rstrip("\n") != line.rstrip("\n").rstrip(" "):
            pytest.fail(
                f"Line {i+1} in '{LOG_FILE}' has trailing spaces.\n"
                f"Line content: '{line.rstrip()}'"
            )

def test_log_file_no_extra_files():
    """No extra files or directories related to the investigation should exist."""
    for path in [
        "/home/user/firefox",
        "/home/user/python3",
        "/home/user/code",
    ]:
        assert not os.path.exists(path), (
            f"The file or directory '{path}' should NOT exist after the investigation.\n"
            "Only the log file at /home/user/process_investigation.log should be created."
        )