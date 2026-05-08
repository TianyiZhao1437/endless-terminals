# test_initial_state.py

import os
import pytest

LOG_DIR = "/home/user/distributed_logs"
LOG_FILE = "/home/user/distributed_logs/system-events.log"
OUTPUT_FILE = "/home/user/distributed_logs/highest_latency.log"

EXPECTED_LOG_CONTENT = (
    "[2024-06-01T15:30:23Z] auth-service:REQUEST:87\n"
    "[2024-06-01T15:30:25Z] db-service:REQUEST:305\n"
    "[2024-06-01T15:31:10Z] cache-service:RESPONSE:22\n"
    "[2024-06-01T15:32:02Z] db-service:REQUEST:189\n"
    "[2024-06-01T15:32:30Z] auth-service:REQUEST:92\n"
)

@pytest.mark.describe("Initial OS and file state for distributed log analysis")
class TestInitialState:
    def test_log_directory_exists(self):
        assert os.path.isdir(LOG_DIR), (
            f"Directory '{LOG_DIR}' does not exist. "
            "Create this directory before proceeding."
        )

    def test_log_file_exists(self):
        assert os.path.isfile(LOG_FILE), (
            f"Log file '{LOG_FILE}' does not exist. "
            "Ensure the file is present at the correct path."
        )

    def test_log_file_contents(self):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            contents = f.read()
        assert contents == EXPECTED_LOG_CONTENT, (
            f"Contents of '{LOG_FILE}' do not match the expected initial state.\n"
            "Expected:\n"
            f"{EXPECTED_LOG_CONTENT!r}\n"
            "Found:\n"
            f"{contents!r}\n"
            "Do not modify this file before running your solution."
        )

    def test_output_file_does_not_exist(self):
        assert not os.path.exists(OUTPUT_FILE), (
            f"Output file '{OUTPUT_FILE}' already exists. "
            "Remove it before running your solution."
        )

    def test_directory_and_files_writable_by_user(self):
        # Check directory
        assert os.access(LOG_DIR, os.W_OK), (
            f"Directory '{LOG_DIR}' is not writable by the user."
        )
        # Check file
        assert os.access(LOG_FILE, os.W_OK), (
            f"File '{LOG_FILE}' is not writable by the user."
        )