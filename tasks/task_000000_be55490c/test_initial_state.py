# test_initial_state.py

import os
import pytest

DEV_PROJECT_DIR = "/home/user/dev_project"
FILENAMES_TXT = os.path.join(DEV_PROJECT_DIR, "filenames.txt")
FILENAME_COUNTS_TXT = os.path.join(DEV_PROJECT_DIR, "filename_counts.txt")

@pytest.mark.initial_state
def test_dev_project_directory_exists():
    assert os.path.isdir(DEV_PROJECT_DIR), (
        f"Missing required directory: '{DEV_PROJECT_DIR}'. "
        "Create this directory before proceeding."
    )

@pytest.mark.initial_state
def test_filenames_txt_exists():
    assert os.path.isfile(FILENAMES_TXT), (
        f"Missing required file: '{FILENAMES_TXT}'. "
        "Create this file containing the list of file names (one per line) before proceeding."
    )

@pytest.mark.initial_state
def test_filenames_txt_content():
    expected_lines = [
        "README.md",
        "main.py",
        "main.py",
        "test_utils.py",
        "test_utils.py",
        "test_utils.py",
        "README.md",
        "test_utils.py",
        "main.py",
        "test_utils.py",
        "test_utils.py",
        "test_utils.py",
    ]

    try:
        with open(FILENAMES_TXT, "r", encoding="utf-8") as f:
            actual_lines = [line.rstrip('\n') for line in f.readlines()]
    except Exception as e:
        pytest.fail(
            f"Could not read '{FILENAMES_TXT}': {e}. "
            "Ensure the file is readable and contains the required content."
        )

    assert actual_lines == expected_lines, (
        f"The content of '{FILENAMES_TXT}' is incorrect.\n"
        f"Expected lines (in order):\n{expected_lines}\n"
        f"Found lines (in order):\n{actual_lines}\n"
        "Ensure the file contains exactly the specified lines, one file name per line, in the correct order."
    )

@pytest.mark.initial_state
def test_filename_counts_txt_does_not_exist():
    assert not os.path.exists(FILENAME_COUNTS_TXT), (
        f"Output file '{FILENAME_COUNTS_TXT}' already exists. "
        "Remove this file before starting the task; it must be created as part of the solution."
    )