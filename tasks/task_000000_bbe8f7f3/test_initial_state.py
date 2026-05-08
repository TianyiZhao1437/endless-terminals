# test_initial_state.py

import os
import sqlite3
import pytest

HOME = "/home/user"
SOURCE_DB = os.path.join(HOME, "source_docs.sqlite")
ARCHIVED_DB = os.path.join(HOME, "archived_docs.sqlite")
LOG_FILE = os.path.join(HOME, "migration_verification.log")


def test_source_db_exists():
    assert os.path.isfile(SOURCE_DB), (
        f"Required source database file does not exist: {SOURCE_DB}"
    )


def test_archived_db_does_not_exist():
    assert not os.path.exists(ARCHIVED_DB), (
        f"archived_docs.sqlite should NOT exist before the migration, but it does: {ARCHIVED_DB}"
    )


def test_source_db_has_pages_table_with_7_rows():
    assert os.path.isfile(SOURCE_DB), (
        f"Required source database file does not exist: {SOURCE_DB}"
    )
    try:
        conn = sqlite3.connect(SOURCE_DB)
        cur = conn.cursor()
        # Check that the pages table exists
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='pages';"
        )
        table = cur.fetchone()
        assert table is not None, (
            f"The database {SOURCE_DB} does not contain a table named 'pages'."
        )
        # Check row count
        cur.execute("SELECT COUNT(*) FROM pages;")
        row = cur.fetchone()
        assert row is not None, (
            f"Could not count rows in the 'pages' table in {SOURCE_DB}."
        )
        count = row[0]
        assert count == 7, (
            f"Expected 7 rows in the 'pages' table of {SOURCE_DB}, but found {count}."
        )
    finally:
        if 'conn' in locals():
            conn.close()


def test_log_file_does_not_exist():
    assert not os.path.exists(LOG_FILE), (
        f"migration_verification.log should NOT exist before the migration, but it does: {LOG_FILE}"
    )