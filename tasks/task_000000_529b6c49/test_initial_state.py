# test_initial_state.py

import os
import pytest

HOME = '/home/user'
AUDIT_DIR = os.path.join(HOME, 'audit_reports')
PROJECTS_DIR = os.path.join(HOME, 'projects')
FILE_LISTING = os.path.join(AUDIT_DIR, 'file_listing.txt')

@pytest.mark.parametrize("path", [
    AUDIT_DIR,
    PROJECTS_DIR,
])
def test_required_directories_exist(path):
    assert os.path.isdir(path), f"Required directory '{path}' does not exist."

def test_audit_reports_directory_is_writable():
    assert os.access(AUDIT_DIR, os.W_OK), f"Directory '{AUDIT_DIR}' is not writable."

def test_projects_directory_contents():
    # Expected entries (files and directories, sorted lexicographically, no trailing slashes)
    expected_entries = [
        "alpha.txt",
        "beta",
        "delta.txt",
        "gamma.md",
        "zeta",
    ]
    actual_entries = []
    try:
        for entry in os.listdir(PROJECTS_DIR):
            entry_path = os.path.join(PROJECTS_DIR, entry)
            # Only include immediate entries (files or directories)
            if os.path.isfile(entry_path) or os.path.isdir(entry_path):
                actual_entries.append(entry)
    except FileNotFoundError:
        pytest.fail(f"Directory '{PROJECTS_DIR}' is missing.")

    actual_entries_sorted = sorted(actual_entries)
    # Remove trailing slashes from directories for comparison
    actual_entries_normalized = [entry.rstrip('/') for entry in actual_entries_sorted]
    assert actual_entries_normalized == expected_entries, (
        f"Directory '{PROJECTS_DIR}' should contain the following entries (sorted, no trailing slashes):\n"
        f"{expected_entries}\n"
        f"Found: {actual_entries_normalized}"
    )

def test_file_listing_txt_does_not_exist_yet():
    assert not os.path.exists(FILE_LISTING), (
        f"The file '{FILE_LISTING}' should not exist before the task is performed."
    )