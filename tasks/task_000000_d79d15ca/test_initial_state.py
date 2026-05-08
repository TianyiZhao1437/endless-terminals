# test_initial_state.py

import os
import sqlite3
import pytest

WORKFLOWS_DB = '/home/user/workflows.db'
EXPECTED_TABLE = 'workflows'
EXPECTED_ROWS = [
    (1, "Email Sync", "active"),
    (2, "Data Backup", "inactive"),
    (3, "Slack Notification", "active"),
    (4, "Server Health Check", "completed"),
    (5, "FTP Transfer", "active"),
]

def test_workflows_db_exists():
    """Check that the database file exists before the student starts."""
    assert os.path.isfile(WORKFLOWS_DB), (
        f"Required database file '{WORKFLOWS_DB}' does not exist. "
        "Make sure the SQLite database is present before you begin."
    )

def test_workflows_table_and_contents():
    """Check the 'workflows' table exists and contains the expected records."""
    try:
        conn = sqlite3.connect(WORKFLOWS_DB)
    except Exception as e:
        pytest.fail(f"Could not open the database file at '{WORKFLOWS_DB}': {e}")

    try:
        cur = conn.cursor()
        # Check table existence
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (EXPECTED_TABLE,)
        )
        table = cur.fetchone()
        assert table is not None, (
            f"Database '{WORKFLOWS_DB}' does not contain the required table '{EXPECTED_TABLE}'."
        )

        # Fetch all records and compare
        cur.execute(f"SELECT id, name, status FROM {EXPECTED_TABLE} ORDER BY id ASC;")
        rows = cur.fetchall()
        assert rows == EXPECTED_ROWS, (
            f"The '{EXPECTED_TABLE}' table does not contain the expected records.\n"
            f"Expected:\n{EXPECTED_ROWS}\nFound:\n{rows}\n"
            "Ensure the table contains all the required records before starting."
        )
    finally:
        conn.close()