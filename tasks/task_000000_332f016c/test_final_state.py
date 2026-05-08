# test_final_state.py

import os
import pytest

FAILED_LOG_PATH = "/home/user/migration/failed_ssh.log"
AUTH_LOG_PATH = "/home/user/migration/auth.log"

EXPECTED_FAILED_LOG_CONTENT = (
    "Jun 19 09:01:33 localhost sshd[13213]: Failed password for bob from 192.168.1.20 port 43456 ssh2\n"
    "Jun 19 09:02:00 localhost sshd[13215]: Failed password for root from 192.168.1.30 port 55321 ssh2\n"
    "Jun 19 09:02:47 localhost sshd[13217]: Failed password for dave from 192.168.1.22 port 65500 ssh2\n"
)

def test_failed_log_exists():
    assert os.path.isfile(FAILED_LOG_PATH), (
        f"Expected output file '{FAILED_LOG_PATH}' does not exist. "
        "You must create this file containing only failed SSH login attempts."
    )

def test_failed_log_content_exact():
    with open(FAILED_LOG_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()
    assert actual_content == EXPECTED_FAILED_LOG_CONTENT, (
        f"The contents of '{FAILED_LOG_PATH}' do not match the expected lines.\n"
        "Expected:\n"
        f"{EXPECTED_FAILED_LOG_CONTENT!r}\n"
        "Actual:\n"
        f"{actual_content!r}\n"
        "Ensure only lines containing 'Failed password' are present, in the correct order, "
        "with no extra or missing lines, and that each line is unmodified."
    )

def test_failed_log_no_extra_lines():
    # This test is defensive against lines that do not match the required pattern.
    import re

    failed_line_regex = re.compile(r"Failed password")
    with open(FAILED_LOG_PATH, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            assert failed_line_regex.search(line), (
                f"Line {idx} in '{FAILED_LOG_PATH}' does not contain 'Failed password':\n"
                f"{line!r}\n"
                "All lines in the output must be failed SSH login attempts only."
            )

def test_failed_log_matches_auth_log_source():
    # Ensure that every line in the failed log is present verbatim in the source log.
    with open(AUTH_LOG_PATH, "r", encoding="utf-8") as f:
        source_lines = f.readlines()
    with open(FAILED_LOG_PATH, "r", encoding="utf-8") as f:
        failed_lines = f.readlines()

    source_set = set(source_lines)
    for idx, line in enumerate(failed_lines, 1):
        assert line in source_set, (
            f"Line {idx} in '{FAILED_LOG_PATH}' is not present verbatim in '{AUTH_LOG_PATH}':\n"
            f"{line!r}\n"
            "All lines in the output must be copied exactly from the source log."
        )

def test_failed_log_line_order_matches_source():
    # Ensure the failed lines appear in the same order as in the source log.
    with open(AUTH_LOG_PATH, "r", encoding="utf-8") as f:
        source_lines = f.readlines()
    with open(FAILED_LOG_PATH, "r", encoding="utf-8") as f:
        failed_lines = f.readlines()

    # Build a list of the source lines that should be in the failed log
    import re
    failed_line_regex = re.compile(r"Failed password")
    expected_lines = [line for line in source_lines if failed_line_regex.search(line)]

    assert failed_lines == expected_lines, (
        "The lines in '{FAILED_LOG_PATH}' are not in the same order as in the source log, "
        "or do not match exactly. Ensure the output is line-for-line identical in order and content."
    )