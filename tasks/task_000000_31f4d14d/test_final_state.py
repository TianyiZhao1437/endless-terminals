# test_final_state.py

import os
import pytest

BINARY_PATH = "/home/user/builds/myapp"
LOG_PATH = "/home/user/builds/myapp_security_scan.log"
SCAN_TOOL = "echo"
SCAN_OUTPUT = "No vulnerabilities found in /home/user/builds/myapp"
EXPECTED_COMMAND_LINE = f"{SCAN_TOOL} {SCAN_OUTPUT}"
EXPECTED_LOG_CONTENT = f"COMMAND: {EXPECTED_COMMAND_LINE}\n\n{SCAN_OUTPUT}\n"

def test_log_file_exists():
    assert os.path.isfile(LOG_PATH), (
        f"Scan log file '{LOG_PATH}' does not exist. "
        "You must create this file after scanning."
    )

def test_log_file_content_exact():
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read log file '{LOG_PATH}': {e}")

    if content != EXPECTED_LOG_CONTENT:
        # Detailed diff for developer
        import difflib
        diff = "\n".join(difflib.ndiff(EXPECTED_LOG_CONTENT.splitlines(), content.splitlines()))
        pytest.fail(
            f"The contents of '{LOG_PATH}' do not match the expected format.\n"
            "Expected:\n"
            f"---\n{EXPECTED_LOG_CONTENT}---\n"
            "Got:\n"
            f"---\n{content}---\n"
            f"Diff:\n{diff}\n"
            "Ensure the file includes:\n"
            " - The exact command line you ran, as the first line, prefixed by 'COMMAND:'\n"
            " - One blank line\n"
            " - The raw scanner output, exactly as produced, with no extra or missing blank lines or characters.\n"
        )

def test_log_file_command_line_first():
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert lines, (
        f"'{LOG_PATH}' is empty. It must contain the command and scan output."
    )
    assert lines[0] == f"COMMAND: {EXPECTED_COMMAND_LINE}\n", (
        f"First line of '{LOG_PATH}' must be 'COMMAND: {EXPECTED_COMMAND_LINE}'\n"
        f"Found: {lines[0].rstrip()!r}"
    )

def test_log_file_blank_line_after_command():
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) >= 2, (
        f"'{LOG_PATH}' must have at least two lines: command and blank line."
    )
    assert lines[1] == "\n", (
        f"Second line of '{LOG_PATH}' must be a blank line after the command.\n"
        f"Found: {lines[1]!r}"
    )

def test_log_file_scan_output():
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) >= 3, (
        f"'{LOG_PATH}' must include scan output as the third line."
    )
    output_line = lines[2].rstrip("\n")
    assert output_line == SCAN_OUTPUT, (
        f"Third line of '{LOG_PATH}' must be the scanner's raw output: '{SCAN_OUTPUT}'.\n"
        f"Found: '{output_line}'"
    )
    # Ensure there are no extra lines after the expected output
    if len(lines) > 3:
        extra = lines[3:]
        # Accept a single trailing newline, but not more
        if not (len(extra) == 1 and extra[0] == ""):
            pytest.fail(
                f"'{LOG_PATH}' contains extra lines after the scan output. "
                "No additional blank lines or text are allowed after the scan output."
            )