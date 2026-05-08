# test_final_state.py

import os
import sqlite3
import filecmp
import pytest

HOME = "/home/user"
SOURCE_DB = os.path.join(HOME, "source_docs.sqlite")
ARCHIVED_DB = os.path.join(HOME, "archived_docs.sqlite")
LOG_FILE = os.path.join(HOME, "migration_verification.log")
EXPECTED_LOG_CONTENT = (
    "source_docs.sqlite: 7\n"
    "archived_docs.sqlite: 7\n"
)


def test_archived_db_exists():
    assert os.path.isfile(ARCHIVED_DB), (
        f"Expected database file {ARCHIVED_DB} does not exist after migration."
    )


def test_archived_db_is_exact_copy_of_source():
    assert os.path.isfile(SOURCE_DB), (
        f"Source database {SOURCE_DB} does not exist, cannot compare."
    )
    assert os.path.isfile(ARCHIVED_DB), (
        f"Archived database {ARCHIVED_DB} does not exist, cannot compare."
    )
    # Binary comparison of the two files
    are_same = filecmp.cmp(SOURCE_DB, ARCHIVED_DB, shallow=False)
    assert are_same, (
        f"{ARCHIVED_DB} is not an exact copy of {SOURCE_DB} after migration."
    )


@pytest.mark.parametrize("db_path, db_label", [
    (SOURCE_DB, "source_docs.sqlite"),
    (ARCHIVED_DB, "archived_docs.sqlite"),
])
def test_pages_table_exists_and_has_7_rows(db_path, db_label):
    assert os.path.isfile(db_path), (
        f"Expected database file does not exist: {db_path}"
    )
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        # Check the table exists
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='pages';"
        )
        table = cur.fetchone()
        assert table is not None, (
            f"The database {db_label} does not contain a table named 'pages'."
        )
        # Check row count
        cur.execute("SELECT COUNT(*) FROM pages;")
        row = cur.fetchone()
        assert row is not None, (
            f"Could not count rows in the 'pages' table in {db_label}."
        )
        count = row[0]
        assert count == 7, (
            f"Expected 7 rows in the 'pages' table of {db_label}, but found {count}."
        )
    finally:
        if 'conn' in locals():
            conn.close()


def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"Expected log file {LOG_FILE} does not exist after migration."
    )


def test_log_file_content():
    assert os.path.isfile(LOG_FILE), (
        f"Expected log file {LOG_FILE} does not exist after migration."
    )
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_LOG_CONTENT, (
        f"{LOG_FILE} content is incorrect.\n"
        f"Expected:\n{EXPECTED_LOG_CONTENT!r}\n"
        f"Found:\n{content!r}\n"
        "Log file must contain exactly two lines, each with the database name and row count, ending with a newline."
    )