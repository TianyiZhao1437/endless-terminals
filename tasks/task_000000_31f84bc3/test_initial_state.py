# test_initial_state.py

import pytest
import os

ACCESS_LOG_PATH = "/home/user/access.log"
EXPECTED_ACCESS_LOG_CONTENT = """192.168.1.11 - - [08/Jun/2024:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 512
203.0.113.52 - - [08/Jun/2024:10:01:22 +0000] "POST /login HTTP/1.1" 200 234
192.168.1.12 - - [08/Jun/2024:10:02:09 +0000] "GET /products HTTP/1.1" 200 1624
192.168.1.11 - - [08/Jun/2024:10:03:15 +0000] "GET /about HTTP/1.1" 200 428
203.0.113.52 - - [08/Jun/2024:10:04:18 +0000] "GET /index.html HTTP/1.1" 200 512
192.168.1.11 - - [08/Jun/2024:10:05:31 +0000] "POST /cart HTTP/1.1" 200 124
192.168.1.12 - - [08/Jun/2024:10:06:44 +0000] "GET /contact HTTP/1.1" 200 360
198.51.100.99 - - [08/Jun/2024:10:07:55 +0000] "GET /index.html HTTP/1.1" 200 512
203.0.113.52 - - [08/Jun/2024:10:08:12 +0000] "GET /products HTTP/1.1" 200 1624
192.168.1.11 - - [08/Jun/2024:10:09:21 +0000] "GET /faq HTTP/1.1" 200 256
203.0.113.52 - - [08/Jun/2024:10:10:40 +0000] "GET /home HTTP/1.1" 200 512
"""

IP_FREQUENCY_LOG_PATH = "/home/user/ip_frequency.log"

@pytest.mark.initial_state
def test_access_log_exists_and_content():
    # Check that /home/user/access.log exists as a file
    assert os.path.isfile(ACCESS_LOG_PATH), (
        f"Missing required file: {ACCESS_LOG_PATH}. "
        "You must have your site's access log at this path before starting the task."
    )

    # Check that the contents of /home/user/access.log match the expected content
    with open(ACCESS_LOG_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()

    # Normalize line endings and strip trailing whitespace for comparison
    expected_lines = EXPECTED_ACCESS_LOG_CONTENT.strip().splitlines()
    actual_lines = actual_content.strip().splitlines()

    assert actual_lines == expected_lines, (
        f"The contents of {ACCESS_LOG_PATH} do not match the expected log entries.\n"
        "Expected content:\n"
        + "\n".join(expected_lines)
        + "\nActual content:\n"
        + "\n".join(actual_lines)
        + "\nPlease ensure the access log contains only the specified entries, in the correct order."
    )

@pytest.mark.initial_state
def test_ip_frequency_log_does_not_exist_yet():
    # The output file must NOT exist before the task.
    assert not os.path.exists(IP_FREQUENCY_LOG_PATH), (
        f"The output file {IP_FREQUENCY_LOG_PATH} already exists before you start. "
        "Please remove it before running your solution."
    )