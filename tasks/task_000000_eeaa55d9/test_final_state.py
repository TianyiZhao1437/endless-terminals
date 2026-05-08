# test_final_state.py

import os
import pwd
import pytest

NETWORK_TEST_DIR = "/home/user/network_test"
RAW_PING = os.path.join(NETWORK_TEST_DIR, "raw_ping_output.txt")
FILTERED_PING = os.path.join(NETWORK_TEST_DIR, "filtered_ping_output.txt")
SUMMARY_LOG = os.path.join(NETWORK_TEST_DIR, "ping_summary.log")


def get_file_lines(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.rstrip('\n') for line in f.readlines()]


def test_network_test_directory_exists():
    assert os.path.isdir(NETWORK_TEST_DIR), (
        f"Directory '{NETWORK_TEST_DIR}' does not exist. "
        "The required directory must be created."
    )

def test_network_test_directory_ownership():
    stat_info = os.stat(NETWORK_TEST_DIR)
    user_name = pwd.getpwuid(stat_info.st_uid).pw_name
    assert user_name == "user", (
        f"Directory '{NETWORK_TEST_DIR}' is owned by '{user_name}', expected 'user'."
    )

@pytest.mark.parametrize("filename", [RAW_PING, FILTERED_PING, SUMMARY_LOG])
def test_required_files_exist(filename):
    assert os.path.isfile(filename), (
        f"File '{filename}' does not exist. All three required files must be present."
    )

def test_raw_ping_output_not_empty():
    lines = get_file_lines(RAW_PING)
    assert len(lines) > 0, (
        f"File '{RAW_PING}' is empty. It must contain the full output of 'ping -c 4 example.com'."
    )
    # Check for a plausible ping header
    header_found = any(line.startswith("PING ") and "example.com" in line for line in lines)
    assert header_found, (
        f"File '{RAW_PING}' does not appear to contain 'ping' output. "
        "Expected a line starting with 'PING example.com'."
    )

def test_filtered_ping_output_content():
    raw_lines = get_file_lines(RAW_PING)
    filtered_lines = get_file_lines(FILTERED_PING)
    expected_lines = [line for line in raw_lines if "time=" in line]
    assert filtered_lines == expected_lines, (
        f"File '{FILTERED_PING}' does not contain the correct filtered lines.\n"
        f"Expected lines with 'time=' from '{RAW_PING}', but got:\n{filtered_lines}\n"
        f"Expected:\n{expected_lines}"
    )

def test_ping_summary_log_content():
    summary_lines = get_file_lines(SUMMARY_LOG)
    assert len(summary_lines) == 2, (
        f"File '{SUMMARY_LOG}' must contain exactly two lines, but contains {len(summary_lines)}."
    )
    raw_count = len(get_file_lines(RAW_PING))
    filtered_count = len(get_file_lines(FILTERED_PING))
    expected_first = f"Total lines in raw_ping_output.txt: {raw_count}"
    expected_second = f"Total lines in filtered_ping_output.txt: {filtered_count}"

    assert summary_lines[0] == expected_first, (
        f"First line of '{SUMMARY_LOG}' is incorrect.\n"
        f"Expected: {expected_first}\n"
        f"Found:    {summary_lines[0]}"
    )
    assert summary_lines[1] == expected_second, (
        f"Second line of '{SUMMARY_LOG}' is incorrect.\n"
        f"Expected: {expected_second}\n"
        f"Found:    {summary_lines[1]}"
    )