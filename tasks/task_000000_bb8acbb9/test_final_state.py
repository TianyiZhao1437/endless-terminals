# test_final_state.py

import os
import pytest

UPTIME_LOGS_DIR = "/home/user/uptime_logs"
PING_RESULTS_FILE = os.path.join(UPTIME_LOGS_DIR, "ping_results.txt")
STATUS_FREQUENCY_FILE = os.path.join(UPTIME_LOGS_DIR, "status_frequency.txt")

EXPECTED_STATUS_FREQUENCY_LINES = [
    "UP\t8",
    "DOWN\t2"
]

def test_status_frequency_file_exists():
    assert os.path.isfile(STATUS_FREQUENCY_FILE), (
        f"File '{STATUS_FREQUENCY_FILE}' does not exist. "
        "You must create this file in the specified location."
    )

def test_status_frequency_file_content():
    with open(STATUS_FREQUENCY_FILE, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    assert lines == EXPECTED_STATUS_FREQUENCY_LINES, (
        f"File '{STATUS_FREQUENCY_FILE}' does not have the exact expected contents.\n"
        "Expected lines (tab-separated, no extra spaces, no blank lines):\n"
        + "\n".join(EXPECTED_STATUS_FREQUENCY_LINES)
        + "\nActual lines:\n"
        + "\n".join(lines)
    )
    for idx, line in enumerate(lines):
        assert '\t' in line, (
            f"Line {idx+1} of '{STATUS_FREQUENCY_FILE}' does not contain a tab character "
            f"as a separator: {repr(line)}"
        )
        parts = line.split('\t')
        assert len(parts) == 2, (
            f"Line {idx+1} of '{STATUS_FREQUENCY_FILE}' must contain exactly one tab "
            f"character separating the status and count: {repr(line)}"
        )
        status, count = parts
        assert status in ("UP", "DOWN"), (
            f"Line {idx+1} of '{STATUS_FREQUENCY_FILE}' contains an invalid status: {repr(status)}"
        )
        assert count.isdigit(), (
            f"Line {idx+1} of '{STATUS_FREQUENCY_FILE}' has a non-numeric count: {repr(count)}"
        )
    assert len(lines) == 2, (
        f"File '{STATUS_FREQUENCY_FILE}' must have exactly 2 lines (one for UP, one for DOWN). "
        f"Found {len(lines)} lines."
    )

def test_status_frequency_file_no_blank_lines():
    with open(STATUS_FREQUENCY_FILE, 'r', encoding='utf-8') as f:
        raw = f.read()
    assert '\n\n' not in raw, (
        f"File '{STATUS_FREQUENCY_FILE}' contains blank lines. "
        "There should be exactly two lines and no blank lines."
    )
    # Also check for trailing newline
    assert not raw.endswith('\n\n'), (
        f"File '{STATUS_FREQUENCY_FILE}' ends with a blank line. "
        "Remove any trailing blank lines."
    )

def test_status_frequency_file_has_tabs_not_spaces():
    with open(STATUS_FREQUENCY_FILE, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            line_stripped = line.rstrip('\n')
            assert '\t' in line_stripped, (
                f"Line {idx} of '{STATUS_FREQUENCY_FILE}' does not use a tab character as a separator: {repr(line_stripped)}"
            )
            assert ' ' not in line_stripped.split('\t')[1], (
                f"Line {idx} of '{STATUS_FREQUENCY_FILE}' contains spaces after the tab. "
                "Only a tab should separate the status and the count."
            )

def test_status_frequency_file_displayed_in_terminal(monkeypatch):
    """
    This test checks that the content of status_frequency.txt was displayed
    in the terminal after creation. It does so by monkeypatching os.system
    and checking for a call like 'cat /home/user/uptime_logs/status_frequency.txt',
    or by verifying that the content appears in standard output.

    Since pytest cannot check retroactively what was displayed in the terminal,
    this test serves as a reminder and will always pass unless the agent
    can provide a log or capture output.
    """
    # This test is informational and will always pass.
    # In a real grading system, capturing terminal output would be required.
    pass