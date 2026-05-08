# test_initial_state.py

import os
import pytest

PROJECT_DIR = "/home/user/old_project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "run_report.py")

@pytest.mark.describe("Initial state validation for legacy code deployment task")
def test_old_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Directory '{PROJECT_DIR}' is missing. "
        "Expected directory for legacy project not found."
    )

def test_run_report_py_exists_and_is_file():
    assert os.path.isfile(SCRIPT_PATH), (
        f"File '{SCRIPT_PATH}' is missing. "
        "Expected Python script 'run_report.py' not found in the legacy project directory."
    )

def test_run_report_py_contents():
    expected_contents = (
        'print("Starting legacy report generation...")\n'
        '# Simulate an error\n'
        'import sys\n'
        'print("Processing record 1...", file=sys.stderr)\n'
        'print("Processing record 2...")\n'
        'print("Processing record 3...", file=sys.stderr)\n'
        'print("Report completed successfully!")\n'
    )
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        actual_contents = f.read()
    assert actual_contents == expected_contents, (
        f"Contents of '{SCRIPT_PATH}' do not match the expected script.\n"
        "Expected contents:\n"
        f"{expected_contents}\n"
        "Actual contents:\n"
        f"{actual_contents}"
    )

def test_report_run_log_does_not_exist_yet():
    log_path = os.path.join(PROJECT_DIR, "report_run.log")
    assert not os.path.exists(log_path), (
        f"File '{log_path}' already exists. "
        "The log file should NOT exist before the task is performed."
    )