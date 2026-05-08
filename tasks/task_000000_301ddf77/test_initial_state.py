# test_initial_state.py

import os
import pytest

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "project_files")
FILES = [
    os.path.join(PROJECT_DIR, "main.py"),
    os.path.join(PROJECT_DIR, "README.md"),
    os.path.join(PROJECT_DIR, "notes.txt"),
]

def test_project_dir_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Required directory {PROJECT_DIR} does not exist. "
        "Please ensure the initial project directory is present."
    )

@pytest.mark.parametrize("filepath", FILES)
def test_project_files_exist(filepath):
    assert os.path.isfile(filepath), (
        f"Required file {filepath} does not exist in {PROJECT_DIR}. "
        "Please ensure all required files are present."
    )

def test_no_src_directory_yet():
    src_dir = os.path.join(PROJECT_DIR, "src")
    assert not os.path.exists(src_dir), (
        f"The directory {src_dir} already exists. "
        "It should not be created before the task."
    )

def test_no_organize_log_yet():
    log_file = os.path.join(PROJECT_DIR, "organize_log.txt")
    assert not os.path.exists(log_file), (
        f"The file {log_file} already exists. "
        "It should not be created before the task."
    )