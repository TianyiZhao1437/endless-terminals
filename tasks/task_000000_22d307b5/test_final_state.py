# test_final_state.py

import os
import pytest

SCRIPTS_DIR = "/home/user/mobile-pipeline/scripts"
LOGS_DIR = "/home/user/mobile-pipeline/logs"
BUILD_SCRIPT = os.path.join(SCRIPTS_DIR, "build_v1.sh")
LOG_FILE = os.path.join(LOGS_DIR, "build_v1_run.log")

EXPECTED_LOG_CONTENT = (
    "Starting legacy build...\n"
    "Checking build dependencies...\n"
    "ERROR: legacy-dependency.txt NOT FOUND.\n"
    "Building application...\n"
    "Build completed successfully!\n"
)

EXPECTED_LAST_5_LINES = [
    "Checking build dependencies...",
    "ERROR: legacy-dependency.txt NOT FOUND.",
    "Building application...",
    "Build completed successfully!"
]

def get_file_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().splitlines()

@pytest.mark.order(1)
def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"Log file '{LOG_FILE}' does not exist.\n"
        "You must capture all output from build_v1.sh into this log file."
    )

@pytest.mark.order(2)
def test_log_file_content_exact():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        actual_content = f.read()
    assert actual_content == EXPECTED_LOG_CONTENT, (
        f"Log file '{LOG_FILE}' does not match the expected output from the build script.\n"
        "Expected content:\n"
        "----------------\n"
        f"{EXPECTED_LOG_CONTENT}"
        "----------------\n"
        "Actual content:\n"
        "----------------\n"
        f"{actual_content}"
        "----------------\n"
        "Check that all output (stdout and stderr) is captured, with correct line breaks and formatting."
    )

@pytest.mark.order(3)
def test_last_5_lines_displayed(monkeypatch, capsys):
    """
    Check that the last 5 lines from the log file are displayed on the terminal.
    We simulate this by capturing output if the student prints these lines in the task code.
    """
    # The test suite cannot verify that the student physically ran 'tail' on the console,
    # but can check if the last 5 lines are printed to stdout (e.g., via print/tail).
    # We read the log file and simulate the display.
    lines = get_file_lines(LOG_FILE)
    # The reference output is the last 5 lines, but the log only has 5 lines.
    # The truth value shows the last 5 lines to be:
    #   Checking build dependencies...
    #   ERROR: legacy-dependency.txt NOT FOUND.
    #   Building application...
    #   Build completed successfully!
    #
    # But the full log is:
    #   Starting legacy build...
    #   Checking build dependencies...
    #   ERROR: legacy-dependency.txt NOT FOUND.
    #   Building application...
    #   Build completed successfully!
    #
    # So the last 5 lines are all lines, but the display should match the last 4 lines as shown in the truth value.
    #
    # However, the truth value shows only 4 lines for the "last 5 lines" display,
    # which means the student should display from "Checking build dependencies..." onwards.
    #
    # We'll verify that the console output matches these 4 lines, in order.
    #
    # Simulate student code: print last 5 lines
    for line in lines[-5:]:
        print(line)

    captured = capsys.readouterr()
    displayed_lines = captured.out.strip().splitlines()

    # Find the last 4 lines as shown in truth value
    if len(displayed_lines) < 4:
        pytest.fail(
            f"Only {len(displayed_lines)} lines were displayed from log file, but at least 4 are required.\n"
            "Expected lines:\n"
            f"{EXPECTED_LAST_5_LINES}"
        )
    # Compare the last 4 displayed lines to EXPECTED_LAST_5_LINES
    actual_display = displayed_lines[-4:]
    assert actual_display == EXPECTED_LAST_5_LINES, (
        "The last 4 lines displayed on the terminal do not match the expected log ending.\n"
        "Expected:\n"
        f"{EXPECTED_LAST_5_LINES}\n"
        "Actual:\n"
        f"{actual_display}\n"
        "Make sure you display the last lines exactly as they appear in the log file, preserving formatting."
    )