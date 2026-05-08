# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/old_project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "run_report.py")
LOG_PATH = os.path.join(PROJECT_DIR, "report_run.log")

EXPECTED_LOG_CONTENT = (
    "Starting legacy report generation...\n"
    "Processing record 1...\n"
    "Processing record 2...\n"
    "Processing record 3...\n"
    "Report completed successfully!\n"
)

@pytest.mark.describe("Final state validation for legacy code deployment task")
def test_report_run_log_exists_and_is_file():
    assert os.path.isfile(LOG_PATH), (
        f"File '{LOG_PATH}' is missing.\n"
        "The log file must exist after running the script for traceability."
    )

def test_report_run_log_permissions():
    # Should be readable by the owner at minimum
    assert os.access(LOG_PATH, os.R_OK), (
        f"File '{LOG_PATH}' is not readable.\n"
        "The log file must be readable for verification."
    )

def test_report_run_log_contents_exact():
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        actual_contents = f.read()

    # Check for exact match including newlines
    assert actual_contents == EXPECTED_LOG_CONTENT, (
        f"Contents of '{LOG_PATH}' do not match the expected combined output of the script.\n"
        "Expected log contents (with exact newlines):\n"
        f"{EXPECTED_LOG_CONTENT!r}\n"
        "Actual log contents:\n"
        f"{actual_contents!r}\n"
        "If stderr and stdout are not properly interleaved, or lines are missing/extra, "
        "the log will not match. Ensure you captured both streams in order using python3."
    )

def test_run_report_py_unchanged():
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
        f"Contents of '{SCRIPT_PATH}' have changed after the task.\n"
        "The source script must remain unchanged. Only the log file should be created.\n"
        "Expected contents:\n"
        f"{expected_contents}\n"
        "Actual contents:\n"
        f"{actual_contents}"
    )

def test_no_extra_files_created():
    files_expected = {"run_report.py", "report_run.log"}
    actual_files = set(os.listdir(PROJECT_DIR))
    extra_files = actual_files - files_expected
    assert not extra_files, (
        f"Unexpected files found in '{PROJECT_DIR}': {sorted(extra_files)}\n"
        "Only 'run_report.py' and 'report_run.log' should exist after completing the task."
    )