# test_initial_state.py
import os
import pytest

LOG_DIR = "/home/user/iot_deploy_logs"
LOG_FILE = "/home/user/iot_deploy_logs/sensor_agent_pull.log"

def test_log_dir_does_not_exist_before_task():
    """
    The log directory should NOT exist before the task.
    """
    assert not os.path.exists(LOG_DIR), (
        f"The directory {LOG_DIR} should not exist before the task starts. "
        "Please ensure the initial state is correct."
    )

def test_log_file_does_not_exist_before_task():
    """
    The log file should NOT exist before the task.
    """
    assert not os.path.exists(LOG_FILE), (
        f"The log file {LOG_FILE} should not exist before the task starts. "
        "Please ensure the initial state is correct."
    )