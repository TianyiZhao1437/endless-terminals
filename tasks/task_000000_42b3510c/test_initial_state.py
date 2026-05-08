# test_initial_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/monitoring_app/dashboards.db"

@pytest.mark.describe("Initial OS and database state validation")
class TestInitialState:

    def test_dashboards_db_exists(self):
        """Check that the dashboards.db SQLite database exists at the expected location."""
        assert os.path.isfile(DB_PATH), (
            f"Expected SQLite database at '{DB_PATH}', but the file does not exist."
        )

    def test_dashboards_table_exists(self):
        """Check that the dashboards table exists in the SQLite database."""
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='dashboards'
            """)
            result = cur.fetchone()
            assert result is not None, (
                f"The table 'dashboards' does not exist in '{DB_PATH}'."
            )
        finally:
            con.close()

    def test_dashboards_table_schema(self):
        """Check that the dashboards table has the correct schema."""
        expected_schema = [
            ("id", "INTEGER"),
            ("name", "TEXT"),
            ("owner", "TEXT"),
        ]
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("PRAGMA table_info('dashboards')")
            schema_info = cur.fetchall()
            # schema_info columns: cid, name, type, notnull, dflt_value, pk
            actual_schema = [(row[1], row[2]) for row in schema_info]
            assert len(actual_schema) == len(expected_schema), (
                f"Expected {len(expected_schema)} columns in 'dashboards', found {len(actual_schema)}."
            )
            for (actual_col, expected_col) in zip(actual_schema, expected_schema):
                assert actual_col == expected_col, (
                    f"Expected column '{expected_col[0]}' of type '{expected_col[1]}', "
                    f"but got '{actual_col[0]}' of type '{actual_col[1]}'."
                )
        finally:
            con.close()

    def test_dashboards_table_initial_rows(self):
        """Check that the dashboards table contains exactly the three required rows."""
        expected_rows = [
            (1, "System Overview", "alice"),
            (2, "Network Traffic", "bob"),
            (3, "App Latency", "carol"),
        ]
        try:
            con = sqlite3.connect(DB_PATH)
            cur = con.cursor()
            cur.execute("SELECT id, name, owner FROM dashboards ORDER BY id ASC")
            actual_rows = cur.fetchall()
            assert actual_rows == expected_rows, (
                "The 'dashboards' table does not contain the expected rows.\n"
                f"Expected rows:\n{expected_rows}\nActual rows:\n{actual_rows}"
            )
        finally:
            con.close()