# test_initial_state.py

import os
import stat
import pytest

APPDATA_DIR = '/home/user/appdata'
DB_PATH = '/home/user/appdata/diagnostics.db'
REPORT_PATH = '/home/user/diagnostics_report.txt'

def test_appdata_directory_exists():
    assert os.path.isdir(APPDATA_DIR), (
        f"Required directory '{APPDATA_DIR}' does not exist. "
        f"Please create this directory before proceeding."
    )

def test_diagnostics_db_exists_and_readable():
    assert os.path.isfile(DB_PATH), (
        f"Required SQLite database file '{DB_PATH}' does not exist. "
        f"Please ensure this file exists before proceeding."
    )
    st = os.stat(DB_PATH)
    # Check read permission for 'user'
    readable = bool(st.st_mode & stat.S_IRUSR)
    assert readable, (
        f"SQLite database file '{DB_PATH}' is not readable by the agent. "
        f"Please adjust permissions to allow read access."
    )

def test_diagnostics_report_not_present():
    assert not os.path.exists(REPORT_PATH), (
        f"The diagnostics report file '{REPORT_PATH}' already exists. "
        f"It should not be present before starting the task."
    )