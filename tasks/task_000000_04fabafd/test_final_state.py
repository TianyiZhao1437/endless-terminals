# test_final_state.py

import os
import pytest

APP_LOGS_DIR = "/home/user/app_logs"
ERROR_LOG = "/home/user/app_logs/error.log"
ACCESS_LOG = "/home/user/app_logs/access.log"
DEBUG_LOG = "/home/user/app_logs/debug.log"
REPORT_FILE = "/home/user/log_disk_usage_report.txt"
EXPECTED_REPORT_LINE = "Total disk usage of /home/user/app_logs: 41K"


def test_app_logs_directory_still_exists():
    assert os.path.isdir(APP_LOGS_DIR), (
        f"Directory {APP_LOGS_DIR} is missing after the task. "
        "It must not be deleted or moved."
    )

@pytest.mark.parametrize("file_path,expected_size", [
    (ERROR_LOG, 12288),
    (ACCESS_LOG, 20480),
    (DEBUG_LOG, 10240),
])
def test_log_file_still_exists_with_correct_size(file_path, expected_size):
    assert os.path.isfile(file_path), (
        f"Log file {file_path} is missing after the task. It must not be removed."
    )
    actual_size = os.path.getsize(file_path)
    assert actual_size == expected_size, (
        f"Log file {file_path} has size {actual_size} bytes after the task; "
        f"expected {expected_size} bytes. The contents and size must not be changed."
    )

def test_report_file_exists():
    assert os.path.isfile(REPORT_FILE), (
        f"Report file {REPORT_FILE} was not created. "
        "You must create this file with the required summary."
    )

def test_report_file_content_and_format():
    assert os.path.isfile(REPORT_FILE), (
        f"Report file {REPORT_FILE} does not exist."
    )
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1, (
        f"Report file {REPORT_FILE} must contain exactly one line, but has {len(lines)} lines."
    )
    line = lines[0].rstrip("\n")
    assert line == EXPECTED_REPORT_LINE, (
        f"Report file {REPORT_FILE} has incorrect contents.\n"
        f"Expected exactly:\n{EXPECTED_REPORT_LINE!r}\n"
        f"But got:\n{line!r}\n"
        "Check the format, spacing, and the reported size."
    )

def test_report_file_has_no_extra_spaces_or_lines():
    with open(REPORT_FILE, "rb") as f:
        content = f.read()
    # Should end with a single newline, no extra blank lines or trailing spaces
    decoded = content.decode("utf-8")
    assert decoded.endswith("\n"), (
        f"Report file {REPORT_FILE} must end with a single newline."
    )
    # No extra blank lines at end
    lines = decoded.splitlines()
    assert len(lines) == 1, (
        f"Report file {REPORT_FILE} must contain exactly one line, but has {len(lines)} lines."
    )
    # No trailing spaces
    if lines:
        assert lines[0] == lines[0].strip(), (
            f"Report file {REPORT_FILE} contains leading or trailing spaces in the line."
        )