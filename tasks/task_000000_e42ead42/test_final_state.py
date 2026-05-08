# test_final_state.py

import os
import pytest

LOG_DIR = "/home/user/uptime_logs"
LOG_FILE = "/home/user/uptime_logs/service_status.log"
EXPECTED_TIMESTAMP = "2024-06-14T15:00:00Z"
EXPECTED_SERVICES = [
    ("auth-service", "UP"),
    ("data-service", "DOWN"),
    ("web-frontend", "DOWN"),
]
EXPECTED_LOG_LINES = [
    f"{EXPECTED_TIMESTAMP} {service} {status}"
    for service, status in EXPECTED_SERVICES
]

@pytest.mark.describe("Final OS and filesystem state after uptime monitoring task")
class TestFinalState:
    def test_uptime_logs_directory_exists_and_permissions(self):
        assert os.path.isdir(LOG_DIR), (
            f"Required directory '{LOG_DIR}' does not exist after the task. "
            "It must exist and be user-writable."
        )
        # Check for user-write permission
        if hasattr(os, "access"):
            assert os.access(LOG_DIR, os.W_OK), (
                f"Directory '{LOG_DIR}' is not writable by the current user after the task. "
                "Set appropriate permissions (e.g., chmod u+w /home/user/uptime_logs)."
            )

    def test_log_file_exists(self):
        assert os.path.isfile(LOG_FILE), (
            f"Log file '{LOG_FILE}' does not exist after the task. "
            "You must create this file with the correct log entries."
        )

    def test_log_file_has_correct_content_and_order(self):
        assert os.path.isfile(LOG_FILE), (
            f"Log file '{LOG_FILE}' not found when checking contents."
        )
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
        assert len(lines) == 3, (
            f"Log file '{LOG_FILE}' must have exactly 3 lines (one per service). "
            f"Found {len(lines)} lines."
        )
        for idx, (expected, actual) in enumerate(zip(EXPECTED_LOG_LINES, lines)):
            assert actual == expected, (
                f"Line {idx+1} of log file is incorrect.\n"
                f"Expected: '{expected}'\n"
                f"Actual:   '{actual}'\n"
                "Each line must match the exact format: "
                "<timestamp> <service_name> <status> (see instructions)."
            )

    def test_log_file_has_no_extra_lines(self):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        assert len(lines) == 3, (
            f"Log file '{LOG_FILE}' must have exactly 3 lines, but found {len(lines)}."
        )

    def test_log_file_location_and_no_other_files(self):
        # The only file in the LOG_DIR should be service_status.log
        files = [f for f in os.listdir(LOG_DIR) if os.path.isfile(os.path.join(LOG_DIR, f))]
        assert files == ["service_status.log"], (
            f"Directory '{LOG_DIR}' contains unexpected files: {files}. "
            "Only 'service_status.log' should be present after the task."
        )