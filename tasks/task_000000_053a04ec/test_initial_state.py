# test_initial_state.py

import os
import pytest

LOGS_DIR = "/home/user/logs"
APP_LOG = os.path.join(LOGS_DIR, "app.log")
ERROR_LOG = os.path.join(LOGS_DIR, "error.log")

@pytest.mark.parametrize("path", [LOGS_DIR])
def test_logs_directory_exists(path):
    assert os.path.isdir(path), (
        f"Required directory '{path}' does not exist. "
        "Make sure the logs directory exists at the specified path."
    )

@pytest.mark.parametrize("filepath", [APP_LOG, ERROR_LOG])
def test_log_file_exists(filepath):
    assert os.path.isfile(filepath), (
        f"Required log file '{filepath}' does not exist. "
        "Both app.log and error.log must exist in /home/user/logs/ before proceeding."
    )

@pytest.mark.parametrize("filepath", [APP_LOG, ERROR_LOG])
def test_log_file_not_empty(filepath):
    try:
        with open(filepath, "r") as f:
            contents = f.read()
        assert contents.strip() != "", (
            f"Log file '{filepath}' is empty. "
            "Each log file should contain arbitrary previous contents before the task."
        )
    except Exception as e:
        pytest.fail(f"Could not read '{filepath}': {e}")