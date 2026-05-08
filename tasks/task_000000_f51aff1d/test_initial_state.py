# test_initial_state.py

import os
import stat
import pwd
import pytest

LOG_DIR = "/home/user/logs"
LOG_FILE = "/home/user/logs/uptime.log"

def test_logs_directory_exists_and_writable():
    assert os.path.isdir(LOG_DIR), (
        f"Required directory {LOG_DIR} does not exist. "
        "Create this directory before proceeding."
    )
    assert os.access(LOG_DIR, os.W_OK), (
        f"Directory {LOG_DIR} is not writable by the user. "
        "Ensure correct permissions are set."
    )

def test_uptime_log_exists_and_properties():
    assert os.path.isfile(LOG_FILE), (
        f"Required log file {LOG_FILE} does not exist. "
        "Create this file before proceeding."
    )
    st = os.stat(LOG_FILE)
    # Check ownership: file should be owned by 'user'
    try:
        file_owner = pwd.getpwuid(st.st_uid).pw_name
    except KeyError:
        file_owner = None
    assert file_owner == "user", (
        f"{LOG_FILE} is not owned by 'user'. "
        f"It is owned by '{file_owner}'. Change ownership to 'user'."
    )
    # Check permissions: should be 0644 (-rw-r--r--)
    expected_mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH  # 0o644
    actual_mode = stat.S_IMODE(st.st_mode)
    assert actual_mode == expected_mode, (
        f"{LOG_FILE} permissions are {oct(actual_mode)}, expected 0o644 (-rw-r--r--). "
        "Set permissions to 0644 before proceeding."
    )

def test_uptime_log_contains_sample_data():
    with open(LOG_FILE, "r") as f:
        lines = [line.rstrip("\n") for line in f]
    # Should have at least 2 lines of historical data
    assert len(lines) >= 2, (
        f"{LOG_FILE} should contain at least two lines of historical uptime data. "
        "Sample:\n2024-06-10 10:00:01 - uptime: up 2 hours, 12 minutes\n"
        "2024-06-10 12:30:01 - uptime: up 4 hours, 42 minutes"
    )
    # Check format of the first two lines
    import re
    line_re = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} - uptime: .+$")
    for i, line in enumerate(lines[:2]):
        assert line_re.match(line), (
            f"Line {i+1} of {LOG_FILE} is not in the required format:\n"
            f"YYYY-MM-DD HH:MM:SS - uptime: UPTIME_VALUE\n"
            f"Found: {line}"
        )