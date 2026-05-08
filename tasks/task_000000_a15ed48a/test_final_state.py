# test_final_state.py

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

EXPECTED_OUTPUT_LINE = "db-service 305 2024-06-01T15:30:25Z"

@pytest.mark.describe("Final OS and file state after distributed log analysis task is complete")
class TestFinalState:
    def test_log_directory_exists(self):
        assert os.path.isdir(LOG_DIR), (
            f"Directory '{LOG_DIR}' does not exist. "
            "It must remain present after the task."
        )

    def test_log_file_exists_and_unchanged(self):
        assert os.path.isfile(LOG_FILE), (
            f"Log file '{LOG_FILE}' is missing after the task. "
            "Do not delete or move the input file."
        )
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            contents = f.read()
        assert contents == EXPECTED_LOG_CONTENT, (
            f"Contents of '{LOG_FILE}' have changed after the task.\n"
            "Do not modify the input log file.\n"
            "Expected:\n"
            f"{EXPECTED_LOG_CONTENT!r}\n"
            "Found:\n"
            f"{contents!r}"
        )

    def test_output_file_exists(self):
        assert os.path.isfile(OUTPUT_FILE), (
            f"Output file '{OUTPUT_FILE}' does not exist after the task. "
            "You must create this file as specified."
        )

    def test_output_file_permissions(self):
        assert os.access(OUTPUT_FILE, os.W_OK), (
            f"Output file '{OUTPUT_FILE}' is not writable by the user."
        )
        assert os.access(OUTPUT_FILE, os.R_OK), (
            f"Output file '{OUTPUT_FILE}' is not readable by the user."
        )

    def test_output_file_content_exact(self):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        assert len(lines) == 1, (
            f"Output file '{OUTPUT_FILE}' must contain exactly one line.\n"
            f"Found {len(lines)} lines: {lines!r}\n"
            "Ensure there are no blank lines or extra output."
        )
        output_line = lines[0].rstrip('\n')
        assert output_line == EXPECTED_OUTPUT_LINE, (
            f"Output file '{OUTPUT_FILE}' does not match the expected result.\n"
            f"Expected:\n{EXPECTED_OUTPUT_LINE!r}\n"
            f"Found:\n{output_line!r}\n"
            "Make sure to match the required format: SERVICE_NAME LATENCY_MS TIMESTAMP "
            "from the log line with the highest REQUEST latency."
        )

    def test_output_file_no_trailing_blank_lines(self):
        with open(OUTPUT_FILE, "rb") as f:
            content = f.read()
        # Should end with exactly one \n (since written with writeln), and nothing more
        assert content.endswith(b"\n"), (
            f"Output file '{OUTPUT_FILE}' must end with a single newline character."
        )
        # Only one line, so only one newline at end
        assert content.count(b"\n") == 1, (
            f"Output file '{OUTPUT_FILE}' must have exactly one newline (one line).\n"
            f"Found {content.count(b'\\n')} newlines."
        )

    def test_no_extra_output_files(self):
        # Only the two files should exist in the directory (system-events.log and highest_latency.log)
        files = sorted([
            f for f in os.listdir(LOG_DIR)
            if os.path.isfile(os.path.join(LOG_DIR, f))
        ])
        expected = sorted([
            os.path.basename(LOG_FILE),
            os.path.basename(OUTPUT_FILE),
        ])
        assert files == expected, (
            f"Directory '{LOG_DIR}' contains unexpected files after the task.\n"
            f"Expected only: {expected}\n"
            f"Found: {files}\n"
            "Do not create any extra files in the log directory."
        )