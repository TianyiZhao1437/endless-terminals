# test_final_state.py

import os
import pytest

POST_REQUESTS_LOG = "/home/user/logs/post_requests.log"

EXPECTED_POST_REQUESTS_LOG_LINES = [
    '192.168.1.5 - - [23/Jun/2024:15:10:55 +0000] "POST /api/login HTTP/1.1" 200 342\n',
    '192.168.1.7 - - [23/Jun/2024:15:12:22 +0000] "POST /api/data HTTP/1.1" 201 120\n',
]


def get_file_lines(path):
    """Read all lines from a file, preserving line endings."""
    with open(path, "r") as f:
        return f.readlines()


def describe_post_requests_log():
    def test_post_requests_log_exists():
        assert os.path.isfile(POST_REQUESTS_LOG), (
            f"Expected file {POST_REQUESTS_LOG} does not exist.\n"
            f"Create the output file at the exact path: {POST_REQUESTS_LOG}"
        )

    def test_post_requests_log_readable():
        assert os.access(POST_REQUESTS_LOG, os.R_OK), (
            f"Output file {POST_REQUESTS_LOG} is not readable.\n"
            f"Check file permissions."
        )

    def test_post_requests_log_contents_exact():
        actual_lines = get_file_lines(POST_REQUESTS_LOG)
        assert actual_lines == EXPECTED_POST_REQUESTS_LOG_LINES, (
            f"{POST_REQUESTS_LOG} does not contain exactly the expected POST request lines.\n"
            f"Expected lines:\n{repr(EXPECTED_POST_REQUESTS_LOG_LINES)}\n"
            f"Actual lines:\n{repr(actual_lines)}\n"
            f"Make sure:\n"
            f"- Only lines with 'POST' as the method in the quoted request are included.\n"
            f"- The lines are unmodified from the original access log.\n"
            f"- No extra lines, whitespace, or blank lines are present.\n"
        )

    def test_post_requests_log_no_extra_lines():
        # Check that there are no extra blank lines at end of file
        actual_lines = get_file_lines(POST_REQUESTS_LOG)
        if actual_lines:
            last_line = actual_lines[-1]
            assert last_line.endswith('\n'), (
                f"The last line of {POST_REQUESTS_LOG} must end with a newline character ('\\n').\n"
                f"Found: {repr(last_line)}"
            )
        # Ensure no extra lines beyond expected
        assert len(actual_lines) == len(EXPECTED_POST_REQUESTS_LOG_LINES), (
            f"{POST_REQUESTS_LOG} contains {len(actual_lines)} lines, but {len(EXPECTED_POST_REQUESTS_LOG_LINES)} were expected.\n"
            f"Remove any extra lines or blank lines."
        )