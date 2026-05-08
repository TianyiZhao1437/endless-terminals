# test_final_state.py

import os
import pytest

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "project_files")
SRC_DIR = os.path.join(PROJECT_DIR, "src")
LOG_FILE = os.path.join(PROJECT_DIR, "organize_log.txt")

def test_src_directory_exists():
    assert os.path.isdir(SRC_DIR), (
        f"The directory {SRC_DIR} does not exist. "
        "You must create a 'src' directory inside '/home/user/project_files'."
    )

def test_main_py_moved_to_src():
    old_path = os.path.join(PROJECT_DIR, "main.py")
    new_path = os.path.join(SRC_DIR, "main.py")
    assert not os.path.exists(old_path), (
        f"The file {old_path} still exists. "
        "You must move 'main.py' into the 'src' directory."
    )
    assert os.path.isfile(new_path), (
        f"The file {new_path} does not exist. "
        "You must move 'main.py' into the 'src' directory."
    )

@pytest.mark.parametrize("filename", ["README.md", "notes.txt"])
def test_project_files_remain(filename):
    filepath = os.path.join(PROJECT_DIR, filename)
    assert os.path.isfile(filepath), (
        f"The file {filepath} is missing. "
        "You must NOT remove or move 'README.md' or 'notes.txt' from '/home/user/project_files'."
    )

def test_organize_log_exists():
    assert os.path.isfile(LOG_FILE), (
        f"The file {LOG_FILE} does not exist. "
        "You must create 'organize_log.txt' in '/home/user/project_files'."
    )

def test_organize_log_contents():
    expected = (
        "Project directory contents:\n"
        "README.md\n"
        "notes.txt\n"
        "\nsrc directory contents:\n"
        "main.py\n"
    )
    try:
        with open(LOG_FILE, "r") as f:
            contents = f.read()
    except Exception as e:
        pytest.fail(f"Could not read {LOG_FILE}: {e}")

    if contents != expected:
        # Show a diff-like message
        from difflib import unified_diff
        diff = ''.join(unified_diff(
            expected.splitlines(keepends=True),
            contents.splitlines(keepends=True),
            fromfile='expected',
            tofile='actual'
        ))
        pytest.fail(
            f"Contents of {LOG_FILE} do not match the required format and file listing.\n"
            f"--- Diff (expected vs actual) ---\n{diff}"
        )

def test_no_extra_files_in_project_dir():
    allowed = {"README.md", "notes.txt", "src", "organize_log.txt"}
    actual = set(os.listdir(PROJECT_DIR))
    extra = actual - allowed
    assert not extra, (
        f"Unexpected files or directories found in {PROJECT_DIR}: {sorted(extra)}. "
        "Only 'README.md', 'notes.txt', 'src', and 'organize_log.txt' should be present."
    )

def test_no_extra_files_in_src_dir():
    expected = {"main.py"}
    actual = set(os.listdir(SRC_DIR))
    extra = actual - expected
    missing = expected - actual
    assert not extra, (
        f"Unexpected files or directories found in {SRC_DIR}: {sorted(extra)}. "
        "Only 'main.py' should be present."
    )
    assert not missing, (
        f"Expected file(s) missing from {SRC_DIR}: {sorted(missing)}. "
        "'main.py' must be present."
    )