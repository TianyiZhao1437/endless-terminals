# test_initial_state.py

import os
import stat
import sqlite3
import pytest
import pwd

SECURITY_AUDIT_DIR = "/home/user/security_audit"
PERMISSIONS_DB = "/home/user/security_audit/permissions.db"

@pytest.mark.parametrize("path", [SECURITY_AUDIT_DIR])
def test_security_audit_directory_exists_and_is_directory(path):
    assert os.path.exists(path), f"Missing required directory: {path}"
    assert os.path.isdir(path), f"Path exists but is not a directory: {path}"

@pytest.mark.parametrize("path", [PERMISSIONS_DB])
def test_permissions_db_exists_and_is_file(path):
    assert os.path.exists(path), f"Missing required file: {path}"
    assert os.path.isfile(path), f"Path exists but is not a file: {path}"

def test_security_audit_dir_and_files_owned_by_user():
    user_info = pwd.getpwnam("user")
    dir_stat = os.stat(SECURITY_AUDIT_DIR)
    db_stat = os.stat(PERMISSIONS_DB)
    assert dir_stat.st_uid == user_info.pw_uid, f"Directory {SECURITY_AUDIT_DIR} is not owned by user 'user'"
    assert db_stat.st_uid == user_info.pw_uid, f"File {PERMISSIONS_DB} is not owned by user 'user'"
    assert os.access(SECURITY_AUDIT_DIR, os.W_OK), f"Directory {SECURITY_AUDIT_DIR} is not writable by user 'user'"
    assert os.access(PERMISSIONS_DB, os.W_OK), f"File {PERMISSIONS_DB} is not writable by user 'user'"

def test_permissions_db_structure_and_content():
    try:
        conn = sqlite3.connect(PERMISSIONS_DB)
        cursor = conn.cursor()
        # Check table structure
        cursor.execute("PRAGMA table_info(user_permissions);")
        columns = cursor.fetchall()
        expected_columns = [
            ('username', 'TEXT'),
            ('role', 'TEXT'),
            ('can_edit', 'INTEGER'),
        ]
        col_names_types = [(col[1], col[2]) for col in columns]
        for expected in expected_columns:
            assert expected in col_names_types, (
                f"Table 'user_permissions' missing column or type: {expected}"
            )
        # Check table rows
        cursor.execute("SELECT username, role, can_edit FROM user_permissions ORDER BY username;")
        rows = cursor.fetchall()
        expected_rows = [
            ('alice', 'admin', 1),
            ('bob', 'staff', 0),
            ('carol', 'editor', 1),
            ('dave', 'guest', 0),
        ]
        row_set = set(rows)
        expected_set = set(expected_rows)
        assert row_set == expected_set, (
            f"Table 'user_permissions' contents incorrect.\n"
            f"Expected rows: {expected_rows}\n"
            f"Actual rows: {rows}"
        )
    finally:
        if 'conn' in locals():
            conn.close()