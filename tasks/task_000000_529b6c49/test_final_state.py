# test_final_state.py

import os
import pytest

HOME = '/home/user'
AUDIT_DIR = os.path.join(HOME, 'audit_reports')
PROJECTS_DIR = os.path.join(HOME, 'projects')
FILE_LISTING = os.path.join(AUDIT_DIR, 'file_listing.txt')

EXPECTED_PROJECTS_ENTRIES = [
    "alpha.txt",
    "beta",
    "delta.txt",
    "gamma.md",
    "zeta",
]

EXPECTED_FILE_LISTING_CONTENT = "\n".join(EXPECTED_PROJECTS_ENTRIES) + "\n"

def test_file_listing_txt_exists():
    assert os.path.isfile(FILE_LISTING), (
        f"The file '{FILE_LISTING}' does not exist. "
        "You must create this file in /home/user/audit_reports."
    )

def test_file_listing_txt_permissions():
    # Ensure the file is readable
    assert os.access(FILE_LISTING, os.R_OK), (
        f"The file '{FILE_LISTING}' exists but is not readable."
    )

def test_file_listing_txt_content_exact():
    with open(FILE_LISTING, 'r', encoding='utf-8') as f:
        content = f.read()
    assert content == EXPECTED_FILE_LISTING_CONTENT, (
        f"The contents of '{FILE_LISTING}' are incorrect.\n"
        "Expected (exact, including order and newlines):\n"
        f"{EXPECTED_FILE_LISTING_CONTENT!r}\n"
        "But found:\n"
        f"{content!r}"
    )

def test_file_listing_txt_content_lines_sorted_and_correct():
    with open(FILE_LISTING, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    assert lines == EXPECTED_PROJECTS_ENTRIES, (
        f"The lines in '{FILE_LISTING}' are not the expected lexicographically sorted list of immediate "
        f"entries from '{PROJECTS_DIR}'.\nExpected:\n{EXPECTED_PROJECTS_ENTRIES}\nFound:\n{lines}"
    )

def test_file_listing_txt_no_trailing_slashes():
    with open(FILE_LISTING, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    for line in lines:
        assert not line.endswith('/'), (
            f"Directory '{line}' in '{FILE_LISTING}' should not have a trailing slash."
        )

def test_file_listing_txt_no_extra_files_created():
    """
    Ensure that only /home/user/audit_reports/file_listing.txt was created or modified in audit_reports.
    """
    allowed_files = {'file_listing.txt'}
    found_files = set(
        entry for entry in os.listdir(AUDIT_DIR)
        if os.path.isfile(os.path.join(AUDIT_DIR, entry))
    )
    extra_files = found_files - allowed_files
    assert not extra_files, (
        f"Unexpected extra files found in '{AUDIT_DIR}': {sorted(extra_files)}. "
        "Only 'file_listing.txt' should exist as a file."
    )

def test_file_listing_txt_no_extra_directories_created():
    """
    Ensure that no new directories were created in /home/user/audit_reports.
    """
    found_dirs = [
        entry for entry in os.listdir(AUDIT_DIR)
        if os.path.isdir(os.path.join(AUDIT_DIR, entry))
    ]
    assert not found_dirs, (
        f"Unexpected directories found in '{AUDIT_DIR}': {found_dirs}. "
        "No directories should have been created in 'audit_reports'."
    )

def test_projects_directory_untouched():
    """
    Ensure /home/user/projects still contains the expected entries.
    """
    actual_entries = []
    for entry in os.listdir(PROJECTS_DIR):
        entry_path = os.path.join(PROJECTS_DIR, entry)
        if os.path.isfile(entry_path) or os.path.isdir(entry_path):
            actual_entries.append(entry)
    actual_entries_sorted = sorted(actual_entries)
    actual_entries_normalized = [entry.rstrip('/') for entry in actual_entries_sorted]
    assert actual_entries_normalized == EXPECTED_PROJECTS_ENTRIES, (
        f"Directory '{PROJECTS_DIR}' should still contain the following entries (sorted, no trailing slashes):\n"
        f"{EXPECTED_PROJECTS_ENTRIES}\n"
        f"Found: {actual_entries_normalized}"
    )