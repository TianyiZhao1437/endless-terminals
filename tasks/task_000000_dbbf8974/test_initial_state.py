# test_initial_state.py

import os
import pytest

DB_PATH = "/home/user/mlops_experiments.db"
LOG_PATH = "/home/user/artifact_log.txt"

def test_database_does_not_exist_initially():
    """
    Before the student starts, the SQLite database file should NOT exist.
    """
    assert not os.path.exists(DB_PATH), (
        f"Expected the database file '{DB_PATH}' to NOT exist before starting. "
        "Please ensure you have not created the database yet."
    )

def test_log_file_does_not_exist_initially():
    """
    Before the student starts, the artifact log file should NOT exist.
    """
    assert not os.path.exists(LOG_PATH), (
        f"Expected the log file '{LOG_PATH}' to NOT exist before starting. "
        "Please ensure you have not created the log file yet."
    )