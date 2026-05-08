# test_initial_state.py

import os
import pytest

LOG_DIR = "/home/user/uptime_logs"
LOG_FILE = "/home/user/uptime_logs/service_status.log"

@pytest.mark.describe("Initial OS and filesystem state before uptime monitoring task")
class TestInitialState:
    def test_uptime_logs_directory_exists_and_permissions(self):
        assert os.path.isdir(LOG_DIR), (
            f"Required directory '{LOG_DIR}' does not exist. "
            "Create this directory with user-write permissions before running the task."
        )
        # Check for user-write permission
        if hasattr(os, "access"):
            assert os.access(LOG_DIR, os.W_OK), (
                f"Directory '{LOG_DIR}' is not writable by the current user. "
                "Set appropriate permissions (e.g., chmod u+w /home/user/uptime_logs)."
            )

    def test_log_file_does_not_exist(self):
        assert not os.path.exists(LOG_FILE), (
            f"Log file '{LOG_FILE}' already exists. "
            "Please ensure the log file does not exist before starting the task."
        )