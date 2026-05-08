# test_final_state.py

import os
import pytest

DB_CONFIG_DIR = "/home/user/db_config"
ENV_FILE = os.path.join(DB_CONFIG_DIR, ".env")
LOG_FILE = os.path.join(DB_CONFIG_DIR, "query_optimization.log")

ENV_EXPECTED_LINES = [
    "DB_HOST=127.0.0.1",
    "DB_USER=admin",
    "QUERY_OPTIMIZATION_LEVEL=high"
]

LOG_EXPECTED_LINES = [
    "DB_HOST: 127.0.0.1",
    "DB_USER: admin",
    "QUERY_OPTIMIZATION_LEVEL: high"
]


def read_file_lines_stripped(path):
    """Read file lines, stripping trailing newlines and whitespace."""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Remove only trailing newlines, preserve inner whitespace for accuracy
    return [line.rstrip('\n\r') for line in lines]


def test_env_file_exists_and_correct_content():
    assert os.path.exists(ENV_FILE), (
        f"File '{ENV_FILE}' does not exist. You must create this file."
    )
    assert os.path.isfile(ENV_FILE), (
        f"'{ENV_FILE}' exists but is not a regular file."
    )

    lines = read_file_lines_stripped(ENV_FILE)
    assert lines == ENV_EXPECTED_LINES, (
        f"File '{ENV_FILE}' has incorrect content.\n"
        f"Expected lines:\n{ENV_EXPECTED_LINES}\n"
        f"Actual lines:\n{lines}\n"
        "Each variable must appear exactly once, on its own line, "
        "with no extra whitespace or blank lines."
    )

    # Check for trailing blank line (file should NOT end with a blank line)
    with open(ENV_FILE, "rb") as f:
        content = f.read()
    if content.endswith(b"\n"):
        # Allow if the file ends with exactly one newline (POSIX style)
        # But not two newlines (no blank line at end)
        if content.endswith(b"\n\n"):
            pytest.fail(
                f"File '{ENV_FILE}' ends with a blank line. "
                "There must be no trailing blank line at the end."
            )


def test_log_file_exists_and_correct_content():
    assert os.path.exists(LOG_FILE), (
        f"File '{LOG_FILE}' does not exist. You must create this file."
    )
    assert os.path.isfile(LOG_FILE), (
        f"'{LOG_FILE}' exists but is not a regular file."
    )

    lines = read_file_lines_stripped(LOG_FILE)
    assert lines == LOG_EXPECTED_LINES, (
        f"File '{LOG_FILE}' has incorrect content.\n"
        f"Expected lines:\n{LOG_EXPECTED_LINES}\n"
        f"Actual lines:\n{lines}\n"
        "Each line must be exactly as shown, with variable name, colon, single space, and value. "
        "There must be no extra lines or blank lines."
    )

    # Check for trailing blank line (file should NOT end with a blank line)
    with open(LOG_FILE, "rb") as f:
        content = f.read()
    if content.endswith(b"\n"):
        # Allow if the file ends with exactly one newline (POSIX style)
        # But not two newlines (no blank line at end)
        if content.endswith(b"\n\n"):
            pytest.fail(
                f"File '{LOG_FILE}' ends with a blank line. "
                "There must be no trailing blank line at the end."
            )


def test_env_file_permissions():
    """Optional: .env file should not be world-writable."""
    mode = os.stat(ENV_FILE).st_mode
    assert not (mode & 0o002), (
        f"File '{ENV_FILE}' is world-writable. "
        "This is not secure; remove write permissions for others."
    )


def test_log_file_permissions():
    """Optional: Log file should not be world-writable."""
    mode = os.stat(LOG_FILE).st_mode
    assert not (mode & 0o002), (
        f"File '{LOG_FILE}' is world-writable. "
        "This is not secure; remove write permissions for others."
    )