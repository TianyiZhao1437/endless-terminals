# test_initial_state.py

import os
import pytest

ARCHIVE_DIR = '/home/user/archive'
FILE_LIST_PATH = '/home/user/archive/file_list.txt'
EXT_REPORT_PATH = '/home/user/archive/extension_report.txt'

@pytest.mark.describe("Initial OS/filesystem state for archive extension summary task")
def test_archive_directory_exists_and_writable():
    assert os.path.isdir(ARCHIVE_DIR), (
        f"Required directory '{ARCHIVE_DIR}' does not exist. "
        "Create this directory before proceeding."
    )
    assert os.access(ARCHIVE_DIR, os.W_OK), (
        f"Directory '{ARCHIVE_DIR}' is not writable. "
        "Ensure write permissions are set for the agent."
    )

def test_file_list_exists():
    assert os.path.isfile(FILE_LIST_PATH), (
        f"Required input file '{FILE_LIST_PATH}' does not exist. "
        "Create this file with the specified contents before starting the task."
    )

def test_file_list_contents():
    expected_lines = [
        "data.csv",
        "report.pdf",
        "notes.txt",
        "data.csv",
        "image.jpg",
        "slides.pdf",
        "archive.zip",
        "notes.txt",
        "data.csv",
        "photo.jpg",
        "backup.zip",
    ]
    with open(FILE_LIST_PATH, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    assert lines == expected_lines, (
        f"File '{FILE_LIST_PATH}' does not have the expected contents.\n"
        f"Expected lines:\n{expected_lines}\nActual lines:\n{lines}\n"
        "Ensure the file contains the above lines, in order, one per line."
    )

def test_extension_report_does_not_exist_yet():
    assert not os.path.exists(EXT_REPORT_PATH), (
        f"Output file '{EXT_REPORT_PATH}' already exists. "
        "Remove this file before starting the task to ensure a clean initial state."
    )