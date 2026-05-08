# test_final_state.py

import os
import pytest

HOME = "/home/user"
SEC_SCAN_DIR = os.path.join(HOME, "sec_scan")
TARGETS_TXT = os.path.join(SEC_SCAN_DIR, "targets.txt")
SCAN_REPORT = os.path.join(SEC_SCAN_DIR, "scan_report.log")

# Canonical truth values
TARGETS_TXT_CONTENT = [
    "192.168.1.1",
    "scanme.nmap.org",
    "127.0.0.1",
]

SCAN_REPORT_CANONICAL = (
    "Target: 192.168.1.1\n"
    "Open Ports: None\n"
    "Target: scanme.nmap.org\n"
    "Open Ports: 22,80\n"
    "Target: 127.0.0.1\n"
    "Open Ports: 22\n"
)

def test_sec_scan_directory_exists_and_is_directory():
    """The /home/user/sec_scan directory must exist and be a directory."""
    assert os.path.exists(SEC_SCAN_DIR), (
        f"Directory '{SEC_SCAN_DIR}' does not exist. The directory must be created as part of the task."
    )
    assert os.path.isdir(SEC_SCAN_DIR), (
        f"'{SEC_SCAN_DIR}' exists but is not a directory."
    )

def test_targets_txt_exists_and_content():
    """The /home/user/sec_scan/targets.txt file must exist and have exactly the three required lines."""
    assert os.path.exists(TARGETS_TXT), (
        f"File '{TARGETS_TXT}' does not exist. The targets file must be created."
    )
    assert os.path.isfile(TARGETS_TXT), (
        f"'{TARGETS_TXT}' exists but is not a file."
    )
    with open(TARGETS_TXT, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    assert lines == TARGETS_TXT_CONTENT, (
        f"'{TARGETS_TXT}' must contain exactly these three lines, in order:\n"
        f"{TARGETS_TXT_CONTENT}\n"
        f"Actual content:\n{lines}"
    )

def test_scan_report_log_exists_and_content():
    """The /home/user/sec_scan/scan_report.log file must exist and match the canonical format/result."""
    assert os.path.exists(SCAN_REPORT), (
        f"File '{SCAN_REPORT}' does not exist. The scan report log must be created."
    )
    assert os.path.isfile(SCAN_REPORT), (
        f"'{SCAN_REPORT}' exists but is not a file."
    )
    with open(SCAN_REPORT, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content == SCAN_REPORT_CANONICAL, (
        f"'{SCAN_REPORT}' does not match the required canonical format and content.\n"
        "Expected:\n"
        f"{SCAN_REPORT_CANONICAL!r}\n"
        "Actual:\n"
        f"{content!r}\n"
        "Differences may be due to incorrect port reporting, ordering, formatting, or whitespace."
    )