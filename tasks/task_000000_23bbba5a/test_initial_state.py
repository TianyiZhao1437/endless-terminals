# test_initial_state.py

import os
import stat
import pytest
import sqlite3

DB_PATH = '/home/user/deployment/db/app_release.db'
LOGS_DIR = '/home/user/deployment/logs'

@pytest.mark.describe("Initial state validation for SQLite deployment database task")
class TestInitialState:
    def test_db_file_exists(self):
        assert os.path.isfile(DB_PATH), (
            f"Missing required SQLite database file at {DB_PATH}. "
            "Ensure the database file exists before proceeding."
        )

    def test_logs_directory_exists(self):
        assert os.path.isdir(LOGS_DIR), (
            f"Missing required logs directory at {LOGS_DIR}. "
            "Create this directory so the output file can be written."
        )

    def test_logs_directory_is_writable(self):
        # Check that the logs directory is writable by current user
        assert os.access(LOGS_DIR, os.W_OK), (
            f"The logs directory at {LOGS_DIR} is not writable. "
            "Ensure correct permissions are set so files can be written there."
        )

    def test_db_has_expected_tables(self):
        """
        Check that the database file contains exactly the tables 'users' and 'settings'
        in that order, and no others.
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
            tables = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            pytest.fail(
                f"Could not open or query the SQLite database at {DB_PATH}: {e}"
            )
        finally:
            if 'conn' in locals():
                conn.close()

        expected_tables = ['settings', 'users']
        # The task expects users first, then settings, but SQLite default ORDER BY name gives alphabetical.
        # So instead, let's fetch all tables and then check for presence and order separately.
        # First, check that both 'users' and 'settings' are present and no extra tables.
        required_tables = {'users', 'settings'}
        actual_tables = set(tables)
        extra_tables = actual_tables - required_tables
        missing_tables = required_tables - actual_tables

        assert not missing_tables, (
            f"Database {DB_PATH} is missing required tables: {', '.join(sorted(missing_tables))}."
        )
        assert not extra_tables, (
            f"Database {DB_PATH} contains unexpected tables: {', '.join(sorted(extra_tables))}."
        )

        # Now, fetch the table names in the order they should appear in output
        # (users first, then settings)
        # The task expects users first, then settings.
        # We'll re-query for table order as in output.
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            )
            tables_in_db = [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()

        expected_order = ['users', 'settings']
        # Find the indices of the expected tables in the fetched list
        order_indices = []
        for tname in expected_order:
            if tname in tables_in_db:
                order_indices.append(tables_in_db.index(tname))
            else:
                order_indices.append(-1)
        # Check that users comes before settings
        assert order_indices[0] != -1 and order_indices[1] != -1, (
            f"Could not find both 'users' and 'settings' tables in the database {DB_PATH}."
        )
        assert order_indices[0] < order_indices[1], (
            f"Table 'users' must appear before 'settings' in the database {DB_PATH}. "
            f"Found table order: {tables_in_db}"
        )