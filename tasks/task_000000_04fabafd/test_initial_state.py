# test_initial_state.py

import os
import pytest

APP_LOGS_DIR = "/home/user/app_logs"
ERROR_LOG = "/home/user/app_logs/error.log"
ACCESS_LOG = "/home/user/app_logs/access.log"
DEBUG_LOG = "/home/user/app_logs/debug.log"
REPORT_FILE = "/home/user/log_disk_usage_report.txt"

def check_file_size(path, expected_size):
    if not os.path.isfile(path):
        return False, f"File {path} does not exist."
    actual_size = os.path.getsize(path)
    if actual_size != expected_size:
        return False, f"File {path} exists but has size {actual_size} bytes (expected {expected_size} bytes)."
    return True, ""

def test_app_logs_directory_exists():
    assert os.path.isdir(APP_LOGS_DIR), (
        f"Directory {APP_LOGS_DIR} does not exist. "
        "It must be present before the task begins."
    )

@pytest.mark.parametrize("file_path,expected_size", [
    (ERROR_LOG, 12288),
    (ACCESS_LOG, 20480),
    (DEBUG_LOG, 10240),
])
def test_log_file_exists_with_correct_size(file_path, expected_size):
    exists_and_size, msg = check_file_size(file_path, expected_size)
    assert exists_and_size, msg

def test_report_file_does_not_exist_yet():
    assert not os.path.exists(REPORT_FILE), (
        f"File {REPORT_FILE} should NOT exist before the task begins."
    )