# test_final_state.py

import os
import sqlite3
import pytest

HOME = "/home/user"
ARTIFACTS_DB = "/home/user/artifacts.db"
BINARIES_REPORT = "/home/user/binaries_report.txt"

TRUTH_ROW = (
    1,
    "libfoo",
    "1.2.3",
    "a54d88e06612d820bc3be72877c74f257b561b19d6e5b5a5b1e02f3f3ab8b511",
)
TRUTH_HEADER = "id|name|version|sha256"
TRUTH_REPORT = (
    "id|name|version|sha256\n"
    "1|libfoo|1.2.3|a54d88e06612d820bc3be72877c74f257b561b19d6e5b5a5b1e02f3f3ab8b511\n"
)

def test_artifacts_db_exists_and_is_sqlite():
    assert os.path.isfile(ARTIFACTS_DB), (
        f"Expected SQLite database file {ARTIFACTS_DB} to exist."
    )
    # SQLite files start with the magic header "SQLite format 3\0"
    with open(ARTIFACTS_DB, "rb") as f:
        magic = f.read(16)
    assert magic.startswith(b"SQLite format 3\x00"), (
        f"{ARTIFACTS_DB} does not appear to be a valid SQLite3 database file."
    )

def test_binaries_table_schema_and_content():
    conn = sqlite3.connect(ARTIFACTS_DB)
    try:
        # Check table exists
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='binaries';"
        )
        table_names = [row[0] for row in cursor.fetchall()]
        assert "binaries" in table_names, (
            "Table 'binaries' does not exist in artifacts.db."
        )

        # Check schema
        cursor = conn.execute("PRAGMA table_info(binaries);")
        columns = cursor.fetchall()
        expected_columns = [
            (0, 'id', 'INTEGER', 0, None, 1),
            (1, 'name', 'TEXT', 1, None, 0),
            (2, 'version', 'TEXT', 1, None, 0),
            (3, 'sha256', 'TEXT', 1, None, 0),
        ]
        # Compare column names, types, notnull, pk
        for idx, expected in enumerate(expected_columns):
            try:
                col = columns[idx]
            except IndexError:
                pytest.fail(
                    f"Column {expected[1]} is missing from 'binaries' table."
                )
            assert col[1] == expected[1], (
                f"Column {idx} should be named '{expected[1]}', found '{col[1]}'."
            )
            assert col[2].upper() == expected[2], (
                f"Column '{expected[1]}' should be of type {expected[2]}, found {col[2]}."
            )
            assert col[3] == expected[3], (
                f"Column '{expected[1]}' NOT NULL constraint mismatch."
            )
            assert col[5] == expected[5], (
                f"Column '{expected[1]}' PRIMARY KEY constraint mismatch."
            )

        # Check only one row, and its values
        cursor = conn.execute("SELECT * FROM binaries;")
        rows = cursor.fetchall()
        assert len(rows) == 1, (
            f"Table 'binaries' should contain exactly one row, found {len(rows)}."
        )
        row = rows[0]
        assert row == TRUTH_ROW, (
            "Row in 'binaries' table does not match expected values.\n"
            f"Expected: {TRUTH_ROW}\nFound:    {row}"
        )
    finally:
        conn.close()

def test_binaries_report_txt_exists_and_content():
    assert os.path.isfile(BINARIES_REPORT), (
        f"Expected report file {BINARIES_REPORT} to exist."
    )
    with open(BINARIES_REPORT, "rt", encoding="utf-8") as f:
        content = f.read()
    # Check for exact match, including newlines
    assert content == TRUTH_REPORT, (
        f"{BINARIES_REPORT} content is incorrect.\n"
        f"Expected:\n{TRUTH_REPORT!r}\nFound:\n{content!r}\n"
        "The report file must contain exactly two lines: headers and data, with no extra lines."
    )