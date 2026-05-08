# test_initial_state.py

import os
import pytest

MONITORING_DIR = "/home/user/monitoring"

def test_monitoring_directory_exists():
    assert os.path.exists(MONITORING_DIR), (
        f"Expected directory '{MONITORING_DIR}' to exist, but it does not. "
        "Please create it before proceeding."
    )
    assert os.path.isdir(MONITORING_DIR), (
        f"'{MONITORING_DIR}' exists but is not a directory."
    )

def test_monitoring_directory_is_empty():
    contents = os.listdir(MONITORING_DIR)
    assert contents == [], (
        f"Expected '{MONITORING_DIR}' to be empty before starting the task, "
        f"but found: {contents}. Remove all files and directories before proceeding."
    )