# test_final_state.py

import os
import pytest

UPTIME_REPORT_PATH = "/home/user/uptime_report.txt"

@pytest.mark.describe("Final environment validation for uptime report extraction task")
def test_uptime_report_file_exists():
    """Check that the uptime report file exists at the expected location."""
    assert os.path.isfile(UPTIME_REPORT_PATH), (
        f"Missing required report file: {UPTIME_REPORT_PATH}. "
        "You must generate this file using terminal column manipulation commands."
    )

@pytest.mark.describe("Final environment validation for uptime report extraction task")
def test_uptime_report_contents():
    """Check that the uptime report file contains only the correct columns and formatting."""
    expected_lines = [
        "server01 12233",
        "server02 9940",
        "server03 5831"
    ]
    with open(UPTIME_REPORT_PATH, "r", encoding="utf-8") as f:
        actual_lines = [line.rstrip('\n') for line in f]

    # Check line count
    assert len(actual_lines) == len(expected_lines), (
        f"{UPTIME_REPORT_PATH} has {len(actual_lines)} lines, expected {len(expected_lines)}.\n"
        f"Actual lines:\n" + "\n".join(actual_lines)
    )

    for idx, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        # Check for leading/trailing whitespace
        assert actual == actual.strip(), (
            f"Line {idx+1} in {UPTIME_REPORT_PATH} has leading or trailing whitespace.\n"
            f"Actual: '{actual}'"
        )
        # Check for single space between columns
        parts = actual.split(' ')
        assert len(parts) == 2, (
            f"Line {idx+1} in {UPTIME_REPORT_PATH} does not have exactly two columns separated by a single space.\n"
            f"Actual: '{actual}'"
        )
        # Check content
        assert actual == expected, (
            f"Line {idx+1} in {UPTIME_REPORT_PATH} does not match the expected output.\n"
            f"Expected: '{expected}'\n"
            f"Actual:   '{actual}'"
        )

    # Check that the file does not have extra trailing blank lines
    with open(UPTIME_REPORT_PATH, "rb") as f:
        content = f.read()
        assert content.endswith(b'\n'), (
            f"{UPTIME_REPORT_PATH} must end with a newline character."
        )
        if len(content) > 1:
            # Ensure no extra blank lines at end
            if content[-2:] == b'\n\n':
                assert False, (
                    f"{UPTIME_REPORT_PATH} ends with extra blank lines. "
                    "There must be exactly one newline at the end."
                )