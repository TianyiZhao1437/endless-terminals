# test_final_state.py

import os
import pytest

HOME = "/home/user"
ENV_FILE = os.path.join(HOME, ".pg_backup.env")
COMMAND_LOG = os.path.join(HOME, "backup_command.log")

EXPECTED_ENV_LINES = [
    "PG_USER=backupuser",
    "PG_PASS=pgsecure123",
    "PG_DB=mydb"
]

EXPECTED_COMMAND_LINE = (
    "pg_dump -U backupuser -Wpgsecure123 mydb > /home/user/backup.sql"
)

def read_file_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()

def read_file_raw(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def test_pg_backup_env_exists():
    """
    The .pg_backup.env file must exist in /home/user.
    """
    assert os.path.isfile(ENV_FILE), (
        f"File '{ENV_FILE}' does not exist. "
        "You must create this file with the required variables."
    )

def test_pg_backup_env_contents():
    """
    The .pg_backup.env file must contain exactly the three required lines,
    in the correct order, with no extra whitespace or lines.
    """
    lines = read_file_lines(ENV_FILE)
    assert lines == EXPECTED_ENV_LINES, (
        f"File '{ENV_FILE}' contents are incorrect.\n"
        f"Expected exactly these three lines (no extra whitespace or lines):\n"
        + "\n".join(EXPECTED_ENV_LINES) +
        f"\nBut got:\n" +
        "\n".join(lines)
    )
    # Check for leading/trailing whitespace in each line
    for i, line in enumerate(lines):
        assert line == line.strip(), (
            f"Line {i+1} in '{ENV_FILE}' has unexpected leading/trailing whitespace: {repr(line)}"
        )

def test_pg_backup_env_no_extra_lines():
    """
    The .pg_backup.env file must not have any empty or extra lines.
    """
    raw = read_file_raw(ENV_FILE)
    if raw.endswith('\n'):
        assert raw.count('\n') == 2, (
            f"File '{ENV_FILE}' should have exactly three lines with no extra blank lines."
        )

def test_backup_command_log_exists():
    """
    The backup_command.log file must exist in /home/user.
    """
    assert os.path.isfile(COMMAND_LOG), (
        f"File '{COMMAND_LOG}' does not exist. "
        "You must create this file containing the correct pg_dump command."
    )

def test_backup_command_log_contents():
    """
    The backup_command.log file must contain exactly one line: the correct pg_dump command
    with all variables expanded and no extra whitespace or lines.
    """
    raw = read_file_raw(COMMAND_LOG)
    lines = raw.splitlines()
    assert len(lines) == 1, (
        f"File '{COMMAND_LOG}' must contain exactly one line, but has {len(lines)} lines."
    )
    command = lines[0]
    assert command == EXPECTED_COMMAND_LINE, (
        f"File '{COMMAND_LOG}' contains the wrong command.\n"
        f"Expected:\n{EXPECTED_COMMAND_LINE}\nBut got:\n{command}"
    )
    # Ensure there is no trailing newline at end of file
    assert not raw.endswith('\n'), (
        f"File '{COMMAND_LOG}' must not end with a newline. Remove any extra blank lines."
    )
    # Check for leading/trailing whitespace
    assert command == command.strip(), (
        f"Line in '{COMMAND_LOG}' has unexpected leading/trailing whitespace: {repr(command)}"
    )