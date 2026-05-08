# test_final_state.py

import pytest
import os

SCAN_REPORT_PATH = "/home/user/scan_report.log"
PASSWD_PATH = "/etc/passwd"

EXPECTED_REPORT = """--- User Enumeration ---
root
alice
eve
hacker

--- /etc/passwd Permissions ---
-rw-r--r-- 1 root root 1234 Jun  1 12:34 /etc/passwd

--- Non-root UID 0 Users ---
hacker
"""

def test_scan_report_exists():
    assert os.path.isfile(SCAN_REPORT_PATH), (
        f"Expected log file '{SCAN_REPORT_PATH}' does not exist."
    )

def test_scan_report_exact_content():
    with open(SCAN_REPORT_PATH, "r", encoding="utf-8") as f:
        actual = f.read()
    assert actual == EXPECTED_REPORT, (
        f"scan_report.log content does not match expected output.\n\n"
        f"--- Actual ---\n{actual}\n"
        f"--- Expected ---\n{EXPECTED_REPORT}"
    )

def test_scan_report_user_enumeration_section():
    with open(SCAN_REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    try:
        start = lines.index("--- User Enumeration ---\n") + 1
        end = lines.index("--- /etc/passwd Permissions ---\n")
    except ValueError:
        pytest.fail("scan_report.log is missing required section headers.")
    users = [line.strip() for line in lines[start:end] if line.strip()]
    expected_users = ["root", "alice", "eve", "hacker"]
    assert users == expected_users, (
        f"'User Enumeration' section incorrect.\n"
        f"Found:   {users}\n"
        f"Expected:{expected_users}"
    )

def test_scan_report_passwd_permissions_section():
    with open(SCAN_REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    try:
        start = lines.index("--- /etc/passwd Permissions ---\n") + 1
        end = lines.index("--- Non-root UID 0 Users ---\n")
    except ValueError:
        pytest.fail("scan_report.log is missing required section headers.")
    perms_lines = [line.rstrip('\n') for line in lines[start:end] if line.strip()]
    expected_line = "-rw-r--r-- 1 root root 1234 Jun  1 12:34 /etc/passwd"
    assert perms_lines == [expected_line], (
        f"'/etc/passwd Permissions' section incorrect.\n"
        f"Found:   {perms_lines}\n"
        f"Expected:[{expected_line}]"
    )

def test_scan_report_non_root_uid0_users_section():
    with open(SCAN_REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    try:
        start = lines.index("--- Non-root UID 0 Users ---\n") + 1
    except ValueError:
        pytest.fail("scan_report.log is missing '--- Non-root UID 0 Users ---' header.")
    users = [line.strip() for line in lines[start:] if line.strip()]
    expected = ["hacker"]
    assert users == expected, (
        f"'Non-root UID 0 Users' section incorrect.\n"
        f"Found:   {users}\n"
        f"Expected:{expected}"
    )

def test_scan_report_no_extra_content():
    """Ensure there is no extra content after the last section."""
    with open(SCAN_REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content.endswith("hacker\n"), (
        "scan_report.log contains extra content or missing trailing newline after last entry."
    )