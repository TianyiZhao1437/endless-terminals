# test_final_state.py

import os
import stat
import pwd
import pytest

SECURITY_AUDIT_DIR = "/home/user/security_audit"
PERMISSIONS_DB = "/home/user/security_audit/permissions.db"
CAN_EDIT_LOG = "/home/user/security_audit/can_edit_users.log"
EXPECTED_LOG_CONTENT = (
    "username | role | can_edit\n"
    "alice | admin | 1\n"
    "carol | editor | 1"
)

def test_can_edit_users_log_exists_and_is_file():
    assert os.path.exists(CAN_EDIT_LOG), (
        f"Missing required output file: {CAN_EDIT_LOG}"
    )
    assert os.path.isfile(CAN_EDIT_LOG), (
        f"{CAN_EDIT_LOG} exists but is not a file"
    )

def test_can_edit_users_log_content_exact():
    assert os.path.exists(CAN_EDIT_LOG), (
        f"Missing required output file: {CAN_EDIT_LOG}"
    )
    with open(CAN_EDIT_LOG, "r", encoding="utf-8") as f:
        content = f.read()
    # No trailing whitespace or blank lines
    if content.endswith('\n'):
        content = content.rstrip('\n')
    assert content == EXPECTED_LOG_CONTENT, (
        f"Incorrect content in {CAN_EDIT_LOG}.\n"
        f"Expected exactly:\n{EXPECTED_LOG_CONTENT!r}\n"
        f"Actual:\n{content!r}"
    )

def test_security_audit_dir_and_files_owned_by_user_and_writable():
    user_info = pwd.getpwnam("user")
    dir_stat = os.stat(SECURITY_AUDIT_DIR)
    db_stat = os.stat(PERMISSIONS_DB)
    log_stat = os.stat(CAN_EDIT_LOG)
    assert dir_stat.st_uid == user_info.pw_uid, (
        f"Directory {SECURITY_AUDIT_DIR} is not owned by user 'user'"
    )
    assert db_stat.st_uid == user_info.pw_uid, (
        f"File {PERMISSIONS_DB} is not owned by user 'user'"
    )
    assert log_stat.st_uid == user_info.pw_uid, (
        f"File {CAN_EDIT_LOG} is not owned by user 'user'"
    )
    assert os.access(SECURITY_AUDIT_DIR, os.W_OK), (
        f"Directory {SECURITY_AUDIT_DIR} is not writable by user 'user'"
    )
    assert os.access(PERMISSIONS_DB, os.W_OK), (
        f"File {PERMISSIONS_DB} is not writable by user 'user'"
    )
    assert os.access(CAN_EDIT_LOG, os.W_OK), (
        f"File {CAN_EDIT_LOG} is not writable by user 'user'"
    )

def test_can_edit_users_log_does_not_have_extra_blank_lines():
    with open(CAN_EDIT_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Strip trailing newlines for check
    stripped_lines = [line.rstrip('\n') for line in lines]
    expected_lines = EXPECTED_LOG_CONTENT.split('\n')
    assert stripped_lines == expected_lines, (
        f"{CAN_EDIT_LOG} contains extra blank lines or trailing whitespace.\n"
        f"Expected lines: {expected_lines}\n"
        f"Actual lines: {stripped_lines}"
    )

def test_can_edit_users_log_pipe_separator_and_no_extra_whitespace():
    with open(CAN_EDIT_LOG, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            line = line.rstrip('\n')
            # Each line should have exactly 2 pipes, and no extra whitespace around pipes
            parts = line.split('|')
            assert len(parts) == 3, (
                f"Line {lineno} in {CAN_EDIT_LOG} does not have exactly 2 pipe separators: {line!r}"
            )
            for part in parts:
                stripped = part.strip()
                assert part == stripped, (
                    f"Line {lineno} in {CAN_EDIT_LOG} has extra whitespace around '|' separator: {line!r}"
                )