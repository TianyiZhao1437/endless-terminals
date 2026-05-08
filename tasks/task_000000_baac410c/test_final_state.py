# test_final_state.py

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

EXPECTED_ERROR_LOG_LINES = [
    "[2024-06-12 15:32:54] [ERROR] Database connection failed\n",
    "[2024-06-12 15:34:15] [ERROR] API timeout occurred\n",
    "[2024-06-12 15:37:22] [ERROR] Unauthorized access attempt\n"
]

@pytest.mark.describe("Final OS/filesystem state and console output for log extraction task")
class TestFinalState:

    def test_error_log_exists(self):
        assert os.path.isfile(ERROR_LOG_PATH), (
            f"Output file '{ERROR_LOG_PATH}' does not exist. It must exist after the extraction task."
        )

    def test_error_log_content(self):
        with open(ERROR_LOG_PATH, "r", encoding="utf-8") as f:
            error_log_lines = f.readlines()
        assert error_log_lines == EXPECTED_ERROR_LOG_LINES, (
            f"The content of '{ERROR_LOG_PATH}' does not match the expected extracted error log lines.\n"
            "Expected:\n"
            + "".join(EXPECTED_ERROR_LOG_LINES)
            + "Found:\n"
            + "".join(error_log_lines)
        )

    def test_app_log_unmodified(self):
        with open(APP_LOG_PATH, "r", encoding="utf-8") as f:
            app_log_content = f.read()
        assert app_log_content == EXPECTED_APP_LOG_CONTENT, (
            f"The content of '{APP_LOG_PATH}' was modified. It must remain unchanged after the extraction task.\n"
            "Expected:\n"
            f"{EXPECTED_APP_LOG_CONTENT}"
            "Found:\n"
            f"{app_log_content}"
        )

    def test_console_output_first_three_error_lines(monkeypatch, capsys):
        """
        The agent should print the first three error lines (all available in this case) to the console,
        exactly as they appear in error.log, in order.
        """
        # Simulate the agent's verification step
        with open(ERROR_LOG_PATH, "r", encoding="utf-8") as f:
            error_lines = f.readlines()

        # Print up to 3 lines, exactly as agent should
        for line in error_lines[:3]:
            print(line.rstrip('\n'))

        captured = capsys.readouterr()
        expected_console_output = "".join(
            [l.rstrip('\n') + "\n" for l in EXPECTED_ERROR_LOG_LINES[:3]]
        )

        assert captured.out == expected_console_output, (
            "The console output after verification does not match the expected first three error log lines.\n"
            "Expected:\n"
            f"{expected_console_output}"
            "Found:\n"
            f"{captured.out}"
        )

    def test_error_log_contains_only_error_lines(self):
        with open(ERROR_LOG_PATH, "r", encoding="utf-8") as f:
            error_log_lines = f.readlines()
        # Check that every line matches the error pattern exactly as in app.log
        for line in error_log_lines:
            assert line in EXPECTED_ERROR_LOG_LINES, (
                f"Unexpected line found in '{ERROR_LOG_PATH}':\n{line}"
                "Only lines with '[ERROR]' log level from 'app.log' should be present."
            )
        # Check that no error lines are missing
        missing = [l for l in EXPECTED_ERROR_LOG_LINES if l not in error_log_lines]
        assert not missing, (
            f"The following expected error lines are missing from '{ERROR_LOG_PATH}':\n" +
            "".join(missing)
        )

    def test_logs_dir_still_exists_and_writable(self):
        assert os.path.isdir(LOGS_DIR), (
            f"Directory '{LOGS_DIR}' does not exist after the task. It must remain intact."
        )
        assert os.access(LOGS_DIR, os.W_OK), (
            f"Directory '{LOGS_DIR}' is not writable after the task. It must remain writable."
        )