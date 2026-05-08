# test_initial_state.py

import os
import pytest

ACCESS_LOG = "/home/user/logs/access.log"
POST_REQUESTS_LOG = "/home/user/logs/post_requests.log"

EXPECTED_ACCESS_LOG_LINES = [
    '192.168.1.5 - - [23/Jun/2024:15:10:55 +0000] "POST /api/login HTTP/1.1" 200 342\n',
    '192.168.1.6 - - [23/Jun/2024:15:11:01 +0000] "GET /index.html HTTP/1.1" 200 5120\n',
    '192.168.1.7 - - [23/Jun/2024:15:12:22 +0000] "POST /api/data HTTP/1.1" 201 120\n',
    '192.168.1.4 - - [23/Jun/2024:15:12:50 +0000] "HEAD /status HTTP/1.1" 200 0\n',
    '192.168.1.8 - - [23/Jun/2024:15:13:00 +0000] "GET /about HTTP/1.1" 404 234\n',
]

@pytest.mark.before
def test_access_log_exists_and_readable():
    assert os.path.isfile(ACCESS_LOG), (
        f"Missing required log file: {ACCESS_LOG}. "
        f"Please ensure the access log exists at this path."
    )
    assert os.access(ACCESS_LOG, os.R_OK), (
        f"Access log {ACCESS_LOG} is not readable. "
        f"Please check file permissions."
    )

@pytest.mark.before
def test_access_log_contents():
    with open(ACCESS_LOG, 'r') as f:
        actual_lines = f.readlines()
    assert actual_lines == EXPECTED_ACCESS_LOG_LINES, (
        f"{ACCESS_LOG} does not contain the expected log entries.\n"
        f"Expected lines:\n{repr(EXPECTED_ACCESS_LOG_LINES)}\n"
        f"Actual lines:\n{repr(actual_lines)}"
    )