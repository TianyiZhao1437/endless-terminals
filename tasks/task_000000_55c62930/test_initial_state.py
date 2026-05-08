# test_initial_state.py

import os
import pytest

HOME_DIR = "/home/user"
DISK_USAGE_LOG = "/home/user/disk_usage.log"

def test_home_user_directory_exists():
    """Check that /home/user directory exists before the task."""
    assert os.path.isdir(HOME_DIR), (
        f"Missing directory: {HOME_DIR}. "
        "The directory must exist before starting the task."
    )

def test_disk_usage_log_not_present_before_task():
    """Check that /home/user/disk_usage.log does NOT exist before the task."""
    assert not os.path.exists(DISK_USAGE_LOG), (
        f"File should not exist before the task: {DISK_USAGE_LOG}. "
        "Please ensure this log file is created only after the task is performed."
    )