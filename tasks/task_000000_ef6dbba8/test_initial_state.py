"""
test_initial_state.py

Pytest suite to validate the initial state of the OS/filesystem for the "Organize Project Files" task.

Checks:
- Directory /home/user/project exists.
- File /home/user/project/file_list.txt exists and contains exactly the expected content (including comments, order, and duplicates).

Does NOT check for any output files or directories.
"""

import os
import pytest

PROJECT_DIR = "/home/user/project"
FILE_LIST_PATH = "/home/user/project/file_list.txt"

EXPECTED_FILE_LIST_CONTENT = [
    "# Source files list",
    "src/main.c",
    "src/utils/data.txt",
    "src/helpers/helper.py",
    "README.md",
    "src/helpers/helper.py",
    "docs/manual.md",
    "src/utils/math.c",
    "src/utils/script.sh"
]

def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Missing required directory: {PROJECT_DIR}\n"
        "Please create the directory before proceeding."
    )

def test_file_list_txt_exists():
    assert os.path.isfile(FILE_LIST_PATH), (
        f"Missing required file: {FILE_LIST_PATH}\n"
        "Please create the file with the required content before proceeding."
    )

def test_file_list_txt_content_exact():
    try:
        with open(FILE_LIST_PATH, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception as e:
        pytest.fail(
            f"Could not read {FILE_LIST_PATH}: {e}"
        )
    # Check for exact content (order, lines, including comments and duplicates)
    if lines != EXPECTED_FILE_LIST_CONTENT:
        # Show difference in content
        import difflib
        diff = "\n".join(difflib.unified_diff(
            EXPECTED_FILE_LIST_CONTENT, lines,
            fromfile="expected", tofile="actual", lineterm=""
        ))
        pytest.fail(
            f"{FILE_LIST_PATH} does not have the exact required content.\n"
            "Please ensure the file contains exactly:\n"
            + "\n".join(EXPECTED_FILE_LIST_CONTENT)
            + "\n\nDifference:\n" + diff
        )