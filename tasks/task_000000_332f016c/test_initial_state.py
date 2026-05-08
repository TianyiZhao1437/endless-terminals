# test_initial_state.py

import os
import pytest

AUTH_LOG_PATH = "/home/user/migration/auth.log"

EXPECTED_AUTH_LOG_CONTENT = """Jun 19 09:01:32 localhost sshd[13212]: Accepted password for alice from 192.168.1.10 port 54321 ssh2
Jun 19 09:01:33 localhost sshd[13213]: Failed password for bob from 192.168.1.20 port 43456 ssh2
Jun 19 09:02:00 localhost sshd[13215]: Failed password for root from 192.168.1.30 port 55321 ssh2
Jun 19 09:02:22 localhost sshd[13216]: Accepted publickey for carol from 192.168.1.11 port 34455 ssh2
Jun 19 09:02:47 localhost sshd[13217]: Failed password for dave from 192.168.1.22 port 65500 ssh2
"""

@pytest.mark.parametrize("path", [AUTH_LOG_PATH])
def test_auth_log_exists(path):
    assert os.path.isfile(path), (
        f"Required log file '{path}' does not exist. "
        "Please make sure the file is present before starting the task."
    )

def test_auth_log_content():
    if not os.path.isfile(AUTH_LOG_PATH):
        pytest.skip(f"{AUTH_LOG_PATH} does not exist, skipping content check.")
    with open(AUTH_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_AUTH_LOG_CONTENT, (
        f"The content of '{AUTH_LOG_PATH}' does not match the expected initial log. "
        "Ensure the file contains the exact lines as specified in the task description."
    )