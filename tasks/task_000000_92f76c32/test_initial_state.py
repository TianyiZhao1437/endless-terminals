"""
test_initial_state.py

Pytest suite to validate the initial OS and filesystem state
for the "securely transfer processed CSV files to a remote server using SSH key-based authentication" task.

This suite checks ONLY the required pre-existing files/directories,
as specified in the task description.

DO NOT check for any files that are supposed to be created by the student.

Author: Senior Python Engineer
"""

import os
import pytest

HOME = "/home/user"
CSV_DIR = f"{HOME}/csv_files"
RAW_CSV = f"{CSV_DIR}/data_raw.csv"
SSH_DIR = f"{HOME}/.ssh"

@pytest.mark.parametrize("path", [
    CSV_DIR,
    SSH_DIR,
])
def test_required_directories_exist_and_writable(path):
    assert os.path.isdir(path), (
        f"Required directory does not exist: {path}\n"
        f"Please ensure '{path}' exists before starting the task."
    )
    assert os.access(path, os.W_OK), (
        f"Required directory is not writable: {path}\n"
        f"Ensure the user has write permissions for '{path}'."
    )

def test_data_raw_csv_exists_and_content():
    assert os.path.isfile(RAW_CSV), (
        f"Required file does not exist: {RAW_CSV}\n"
        f"Please ensure '{RAW_CSV}' exists before starting."
    )
    # Check file is non-empty and matches expected content (exact check)
    expected_lines = [
        "id,name,status\n",
        "1,Alice,SUCCESS\n",
        "2,Bob,FAILED\n",
        "3,Charlie,SUCCESS\n",
        "4,David,PENDING\n",
        "5,Eve,SUCCESS\n",
    ]
    with open(RAW_CSV, "r", encoding="utf-8") as f:
        actual_lines = f.readlines()
    assert actual_lines == expected_lines, (
        f"The content of '{RAW_CSV}' is incorrect.\n"
        f"Expected content:\n{''.join(expected_lines)}\n"
        f"Actual content:\n{''.join(actual_lines)}\n"
        f"Please ensure the file contains the exact lines as specified."
    )