# test_final_state.py

import os
import pytest
import sqlite3

HOME = "/home/user"
DB_PATH = os.path.join(HOME, "alerts.db")
CSV_PATH = os.path.join(HOME, "alerts_export.csv")

EXPECTED_DB_SCHEMA = [
    ('id', 'INTEGER', 1, None, 1, 1),
    ('service', 'TEXT', 0, None, 0, 0),
    ('level', 'TEXT', 0, None, 0, 0),
    ('message', 'TEXT', 0, None, 0, 0),
    ('timestamp', 'TEXT', 0, None, 0, 0)
]

EXPECTED_DB_ROW = (
    1,
    "webserver",
    "critical",
    "Web service unreachable",
    "2024-06-13T08:00:00Z"
)

EXPECTED_CSV_CONTENT = (
    "id,service,level,message,timestamp\n"
    "1,webserver,critical,Web service unreachable,2024-06-13T08:00:00Z\n"
)


def test_alerts_db_exists():
    """alerts.db must exist at the correct absolute path."""
    assert os.path.exists(DB_PATH), (
        f"alerts.db is missing at {DB_PATH}. The database file must be present after completing the task."
    )


def test_alerts_db_has_alerts_table():
    """alerts.db must contain a single table 'alerts' with the correct schema."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check for alerts table existence
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='alerts';"
        )
        result = cursor.fetchone()
        assert result is not None, (
            f"'alerts' table does not exist in {DB_PATH}."
        )

        # Check schema
        cursor.execute("PRAGMA table_info(alerts);")
        schema = cursor.fetchall()
        # Schema is a list of tuples: (cid, name, type, notnull, dflt_value, pk)
        # We ignore cid (column index), and compare the rest.
        schema_reduced = [(col[1], col[2], col[3], col[4], col[5], col[6]) for col in schema]
        assert len(schema_reduced) == len(EXPECTED_DB_SCHEMA), (
            f"'alerts' table schema has {len(schema_reduced)} columns, expected {len(EXPECTED_DB_SCHEMA)}: {schema_reduced}"
        )
        for actual, expected in zip(schema_reduced, EXPECTED_DB_SCHEMA):
            assert actual == expected, (
                f"Column schema mismatch: got {actual}, expected {expected}."
            )
    finally:
        conn.close()


def test_alerts_db_single_row():
    """alerts.db must contain exactly one row in the alerts table, with correct data."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alerts;")
        rows = cursor.fetchall()
        assert len(rows) == 1, (
            f"'alerts' table must contain exactly one row, found {len(rows)}."
        )
        row = rows[0]
        assert row == EXPECTED_DB_ROW, (
            f"'alerts' table row does not match expected:\n"
            f"  Actual:   {row}\n"
            f"  Expected: {EXPECTED_DB_ROW}"
        )
    finally:
        conn.close()


def test_alerts_export_csv_exists():
    """alerts_export.csv must exist at the correct absolute path."""
    assert os.path.exists(CSV_PATH), (
        f"alerts_export.csv is missing at {CSV_PATH}. The CSV export file must be present after completing the task."
    )


def test_alerts_export_csv_content():
    """alerts_export.csv must have correct header and exactly one row, with standard comma-separated format."""
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_CSV_CONTENT, (
        "alerts_export.csv content is incorrect.\n"
        "Expected exactly:\n"
        f"{EXPECTED_CSV_CONTENT!r}\n"
        "But got:\n"
        f"{content!r}\n"
        "Check header, row values, separators, and line endings (should be Unix '\\n')."
    )