# test_initial_state.py

import os
import pytest

HOME = "/home/user"
DB_PATH = os.path.join(HOME, "pipeline.db")
LOG_PATH = os.path.join(HOME, "pipeline_status.log")

def test_pipeline_db_does_not_exist():
    """The SQLite database file should NOT exist before the task begins."""
    assert not os.path.exists(DB_PATH), (
        f"Expected '{DB_PATH}' NOT to exist before the task, but it does. "
        "Please remove this file before starting."
    )

def test_pipeline_status_log_does_not_exist():
    """The log file should NOT exist before the task begins."""
    assert not os.path.exists(LOG_PATH), (
        f"Expected '{LOG_PATH}' NOT to exist before the task, but it does. "
        "Please remove this file before starting."
    )