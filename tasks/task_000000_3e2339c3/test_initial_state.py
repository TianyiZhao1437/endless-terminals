# test_initial_state.py

import os
import stat
import pytest

COMPLIANCE_DIR = "/home/user/compliance_check"
VENV_DIR = os.path.join(COMPLIANCE_DIR, "audit_env")
LOG_FILE = os.path.join(COMPLIANCE_DIR, "audit_env_creation.log")

def test_compliance_dir_exists_and_is_writable():
    assert os.path.isdir(COMPLIANCE_DIR), (
        f"Required directory {COMPLIANCE_DIR} does not exist. "
        "Please create it before proceeding."
    )
    # Check write permission for the user
    if not os.access(COMPLIANCE_DIR, os.W_OK):
        raise AssertionError(
            f"Directory {COMPLIANCE_DIR} exists but is not writable by the user."
        )

def test_compliance_dir_is_empty():
    contents = os.listdir(COMPLIANCE_DIR)
    assert contents == [], (
        f"Directory {COMPLIANCE_DIR} must be empty before starting the task, "
        f"but found: {contents}."
    )

def test_audit_env_dir_does_not_exist():
    assert not os.path.exists(VENV_DIR), (
        f"Directory {VENV_DIR} should not exist before starting the task."
    )

def test_log_file_does_not_exist():
    assert not os.path.exists(LOG_FILE), (
        f"Log file {LOG_FILE} should not exist before starting the task."
    )