# test_final_state.py

import os
import pytest

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "weather_app")
SRC_DIR = os.path.join(PROJECT_DIR, "src")
TESTS_DIR = os.path.join(PROJECT_DIR, "tests")
LOG_FILE = os.path.join(PROJECT_DIR, "project_structure.log")

EXPECTED_LOG_CONTENT = (
    "weather_app/\n"
    "├── src/\n"
    "├── tests/\n"
    "└── project_structure.log\n"
)

def _list_dir_abs(path):
    """Returns a set of absolute paths (files and dirs) in the directory, non-recursive."""
    return set(os.path.join(path, entry) for entry in os.listdir(path))

@pytest.mark.order(1)
def test_weather_app_directory_exists():
    """weather_app directory must exist at the correct absolute path."""
    assert os.path.isdir(PROJECT_DIR), (
        f"Directory {PROJECT_DIR} does not exist. "
        "The main project directory must be created."
    )

@pytest.mark.order(2)
def test_subdirectories_exist():
    """src and tests subdirectories must exist and be directories."""
    assert os.path.isdir(SRC_DIR), (
        f"Directory {SRC_DIR} does not exist. "
        "Please create the 'src' subdirectory inside the project."
    )
    assert os.path.isdir(TESTS_DIR), (
        f"Directory {TESTS_DIR} does not exist. "
        "Please create the 'tests' subdirectory inside the project."
    )

@pytest.mark.order(3)
def test_log_file_exists_and_is_readable():
    """project_structure.log must exist, be a file, and be readable."""
    assert os.path.isfile(LOG_FILE), (
        f"File {LOG_FILE} does not exist. "
        "Please create the log file in the project directory."
    )
    assert os.access(LOG_FILE, os.R_OK), (
        f"File {LOG_FILE} is not readable. "
        "Ensure it has correct permissions."
    )

@pytest.mark.order(4)
def test_no_extra_files_or_directories():
    """No extra files or directories should exist under /home/user/weather_app."""
    expected_entries = {SRC_DIR, TESTS_DIR, LOG_FILE}
    actual_entries = _list_dir_abs(PROJECT_DIR)
    extra_entries = actual_entries - expected_entries
    missing_entries = expected_entries - actual_entries
    assert not missing_entries, (
        f"Missing expected entries: {', '.join(missing_entries)}. "
        "Please ensure all required directories and files are present."
    )
    assert not extra_entries, (
        f"Extra files/directories found: {', '.join(extra_entries)}. "
        "Remove any files or directories not specified in the requirements."
    )

@pytest.mark.order(5)
def test_log_file_content_exact():
    """project_structure.log must have exactly the required tree-like content."""
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read {LOG_FILE}: {e}")
    if content != EXPECTED_LOG_CONTENT:
        diff_lines = [
            f"Expected:\n{EXPECTED_LOG_CONTENT}",
            f"Found:\n{content}"
        ]
        pytest.fail(
            "Content of project_structure.log does not match the required format.\n"
            + "\n".join(diff_lines)
        )