# test_initial_state.py

import os
import pytest

HOME = "/home/user"
DB_PATH = os.path.join(HOME, "alerts.db")
CSV_PATH = os.path.join(HOME, "alerts_export.csv")

def test_alerts_db_absent_before_task():
    """Before starting, alerts.db must NOT exist."""
    assert not os.path.exists(DB_PATH), (
        f"alerts.db exists at {DB_PATH}, but it should NOT be present before starting the task."
    )

def test_alerts_export_csv_absent_before_task():
    """Before starting, alerts_export.csv must NOT exist."""
    assert not os.path.exists(CSV_PATH), (
        f"alerts_export.csv exists at {CSV_PATH}, but it should NOT be present before starting the task."
    )