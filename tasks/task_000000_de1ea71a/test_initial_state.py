# test_initial_state.py

import os
import pytest

BACKUP_LIST_PATH = "/home/user/documents/backup_list.txt"
REPORTS_DIR = "/home/user/reports"
EXPECTED_FILENAMES = ["picture1.jpg", "notes.docx", "archive.tar.gz"]

def test_backup_list_file_exists():
    assert os.path.isfile(BACKUP_LIST_PATH), (
        f"Missing required file: {BACKUP_LIST_PATH}. "
        "Create this file before proceeding."
    )

def test_backup_list_file_content():
    with open(BACKUP_LIST_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f]
    assert lines == EXPECTED_FILENAMES, (
        f"{BACKUP_LIST_PATH} has incorrect content.\n"
        f"Expected lines:\n  {EXPECTED_FILENAMES}\n"
        f"Found lines:\n  {lines}\n"
        "Ensure the file lists exactly these three filenames, one per line, in the correct order."
    )

def test_reports_directory_exists():
    assert os.path.isdir(REPORTS_DIR), (
        f"Missing required directory: {REPORTS_DIR}. "
        "Create this directory before proceeding."
    )