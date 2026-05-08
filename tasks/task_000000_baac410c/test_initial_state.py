# test_initial_state.py

import os
import pytest

APP_LOG_PATH = "/home/user/logs/app.log"
ERROR_LOG_PATH = "/home/user/logs/error.log"
LOGS_DIR = "/home/user/logs"

EXPECTED_APP_LOG_CONTENT = (
    "[2024-06-12 15:31:10] [INFO] Application started\n"
    "[2024-06-12 15:32:54] [ERROR] Database connection failed\n"
    "[2024-06-12 15:33:02] [WARN] High memory usage\n"
    "[2024-06-12 15:34:15] [ERROR] API timeout occurred\n"
    "[2024-06-12 15:36:40] [INFO] Job completed\n"
    "[2024-06-12 15:37:22] [ERROR] Unauthorized access attempt\n"
)

@pytest.mark.describe("Initial OS/filesystem state for log extraction task")
class TestInitialState:

    def test_logs_dir_exists_and_is_writable(self):
        assert os.path.isdir(LOGS_DIR), (
            f"Directory '{LOGS_DIR}' does not exist. It must exist before starting the task."
        )
        # Check if writable by current user
        assert os.access(LOGS_DIR, os.W_OK), (
            f"Directory '{LOGS_DIR}' is not writable. It must be writable before starting the task."
        )

    def test_app_log_exists(self):
        assert os.path.isfile(APP_LOG_PATH), (
            f"Log file '{APP_LOG_PATH}' does not exist. It must exist before starting the task."
        )

    def test_app_log_content(self):
        with open(APP_LOG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        assert content == EXPECTED_APP_LOG_CONTENT, (
            f"The content of '{APP_LOG_PATH}' does not match the expected initial content.\n"
            "Expected:\n"
            f"{EXPECTED_APP_LOG_CONTENT}"
            "Found:\n"
            f"{content}"
        )

    def test_error_log_does_not_exist(self):
        assert not os.path.exists(ERROR_LOG_PATH), (
            f"Output file '{ERROR_LOG_PATH}' should NOT exist before performing the extraction task."
        )