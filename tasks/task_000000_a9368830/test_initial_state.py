# test_initial_state.py

import os
import stat
import pytest

SAMPLE_APP_PATH = "/home/user/applications/sample_app.py"
APPLICATIONS_DIR = "/home/user/applications/"

def test_sample_app_py_exists_and_executable():
    """Check that /home/user/applications/sample_app.py exists and is executable."""
    assert os.path.isfile(SAMPLE_APP_PATH), (
        f"Required file not found: {SAMPLE_APP_PATH}. "
        "Please ensure the sample_app.py script exists at the specified location."
    )
    st = os.stat(SAMPLE_APP_PATH)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"The file {SAMPLE_APP_PATH} exists but is not executable. "
        "Please ensure it has executable permissions (chmod +x)."
    )

def test_applications_dir_writable_by_user():
    """Check that /home/user/applications/ directory exists and is writable by the user."""
    assert os.path.isdir(APPLICATIONS_DIR), (
        f"Directory not found: {APPLICATIONS_DIR}. "
        "Please ensure the applications directory exists at the specified location."
    )
    is_writable = os.access(APPLICATIONS_DIR, os.W_OK)
    assert is_writable, (
        f"Directory {APPLICATIONS_DIR} is not writable by the user. "
        "Please ensure the user has write permissions to this directory."
    )