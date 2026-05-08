# test_final_state.py

import os
import stat
import pytest
import re

APP_LOGS_DIR = "/home/user/app/logs"
APP_LOG_PATH = "/home/user/app/logs/app.log"
ERROR_IPS_PATH = "/home/user/app/logs/error_ips.txt"

EXPECTED_ERROR_IPS = [
    "10.0.0.1",
    "10.0.0.2",
    "172.16.0.5",
    "192.168.1.10",
]

def test_error_ips_file_created():
    assert os.path.isfile(ERROR_IPS_PATH), (
        f"File '{ERROR_IPS_PATH}' was not created. "
        "You must create this file with the extracted ERROR IPs."
    )

def test_error_ips_file_permissions():
    # Check that the file is readable (and writable, optional)
    assert os.access(ERROR_IPS_PATH, os.R_OK), (
        f"File '{ERROR_IPS_PATH}' is not readable. "
        "Ensure the user has read permissions."
    )
    assert os.access(ERROR_IPS_PATH, os.W_OK), (
        f"File '{ERROR_IPS_PATH}' is not writable. "
        "Ensure the user has write permissions."
    )

def test_error_ips_file_content_exact():
    with open(ERROR_IPS_PATH, "r", encoding="utf-8") as f:
        contents = f.read()
    # Split into lines and remove trailing whitespace from each line
    lines = [line.rstrip() for line in contents.splitlines()]
    expected_lines = EXPECTED_ERROR_IPS

    assert lines == expected_lines, (
        f"File '{ERROR_IPS_PATH}' does not have the expected content.\n"
        "Expected lines (sorted, unique, one IP per line):\n" +
        "\n".join(expected_lines) +
        "\nActual lines:\n" +
        "\n".join(lines) +
        "\nCheck that you are extracting only ERROR lines, finding all IPv4 addresses, "
        "removing duplicates, sorting, and writing one IP per line with no extra whitespace."
    )

def test_error_ips_file_no_blank_lines():
    with open(ERROR_IPS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for idx, line in enumerate(lines, 1):
        assert line.strip() != "", (
            f"File '{ERROR_IPS_PATH}' has a blank line at line {idx}. "
            "There should be no blank lines in the file."
        )

def test_error_ips_file_no_extra_lines():
    """
    Ensure that only the IPs from ERROR lines are present, and no others.
    """
    with open(ERROR_IPS_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    # Ensure no extra lines (should match exactly the expected set)
    extra = set(lines) - set(EXPECTED_ERROR_IPS)
    missing = set(EXPECTED_ERROR_IPS) - set(lines)
    assert not extra, (
        f"File '{ERROR_IPS_PATH}' contains unexpected IPs: {sorted(extra)}. "
        "Only IPs from ERROR lines in the log should be present."
    )
    assert not missing, (
        f"File '{ERROR_IPS_PATH}' is missing IPs: {sorted(missing)}. "
        "All IPs from ERROR lines in the log must be present."
    )

def test_error_ips_file_lines_are_valid_ipv4():
    ipv4_pattern = re.compile(
        r"^(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)$"
    )
    with open(ERROR_IPS_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip() for line in f.readlines()]
    for ip in lines:
        assert ipv4_pattern.match(ip), (
            f"File '{ERROR_IPS_PATH}' contains an invalid IPv4 address: '{ip}'. "
            "Each line must contain only a valid IPv4 address."
        )

def test_no_other_files_created():
    """
    Ensure that only 'error_ips.txt' was created, and no other new files exist in the logs directory.
    """
    expected_files = {"app.log", "error_ips.txt"}
    actual_files = set(os.listdir(APP_LOGS_DIR))
    unexpected = actual_files - expected_files
    assert not unexpected, (
        f"Unexpected files found in '{APP_LOGS_DIR}': {sorted(unexpected)}. "
        "Only 'app.log' and 'error_ips.txt' should be present after completing the task."
    )