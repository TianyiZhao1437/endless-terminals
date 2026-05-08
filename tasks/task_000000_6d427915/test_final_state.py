# test_final_state.py

import os
import sqlite3
import pytest

HOME = "/home/user"
DB_PATH = os.path.join(HOME, "pipeline.db")
LOG_PATH = os.path.join(HOME, "pipeline_status.log")

EXPECTED_TABLE = "builds"
EXPECTED_COLUMNS = [
    ("id", "INTEGER", 1, None, 1),      # (name, type, notnull, dflt_value, pk)
    ("branch", "TEXT", 0, None, 0),
    ("status", "TEXT", 0, None, 0),
]
EXPECTED_ROWS = [
    (1, "develop", "success"),
    (2, "release", "failed"),
]
EXPECTED_LOG = (
    "id|branch|status\n"
    "1|develop|success\n"
    "2|release|failed\n"
)

def test_pipeline_db_exists():
    """The SQLite database file must exist after the task is completed."""
    assert os.path.isfile(DB_PATH), (
        f"Expected database file '{DB_PATH}' to exist, but it does not."
    )

def test_pipeline_db_has_builds_table_and_schema():
    """The database must contain a 'builds' table with the exact schema."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Check that the builds table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (EXPECTED_TABLE,)
        )
        table = cursor.fetchone()
        assert table is not None, (
            f"Database '{DB_PATH}' does not contain the required table '{EXPECTED_TABLE}'."
        )

        # Check the schema of the builds table
        cursor.execute(f"PRAGMA table_info({EXPECTED_TABLE});")
        columns = cursor.fetchall()  # cid, name, type, notnull, dflt_value, pk
        assert len(columns) == len(EXPECTED_COLUMNS), (
            f"Table '{EXPECTED_TABLE}' should have {len(EXPECTED_COLUMNS)} columns, "
            f"but has {len(columns)}. Schema: {columns}"
        )
        for idx, expected in enumerate(EXPECTED_COLUMNS):
            col = columns[idx]
            assert (col[1], col[2], col[3], col[4], col[5]) == expected, (
                f"Column {idx+1} in table '{EXPECTED_TABLE}' is {col[1:]}, "
                f"expected {expected}."
            )

def test_builds_table_contains_expected_rows():
    """The 'builds' table must contain exactly the specified rows in order."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, branch, status FROM {EXPECTED_TABLE} ORDER BY id;")
        rows = cursor.fetchall()
        assert rows == EXPECTED_ROWS, (
            f"Table '{EXPECTED_TABLE}' contains rows:\n{rows}\n"
            f"but expected exactly:\n{EXPECTED_ROWS}"
        )

def test_pipeline_status_log_exists():
    """The log file must exist after the task is completed."""
    assert os.path.isfile(LOG_PATH), (
        f"Expected log file '{LOG_PATH}' to exist, but it does not."
    )

def test_pipeline_status_log_content_exact():
    """The log file must contain the exact output from the SELECT query, including the header."""
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_LOG, (
        f"Log file '{LOG_PATH}' has unexpected content.\n"
        f"Expected:\n{EXPECTED_LOG!r}\n"
        f"Got:\n{content!r}"
    )