# test_final_state.py

import os
import pytest

PIPELINE_LOGS_DIR = "/home/user/pipeline_logs"
PIPELINE_LOG_FILE = os.path.join(PIPELINE_LOGS_DIR, "pipeline.log")
ERROR_REPORT_FILE = os.path.join(PIPELINE_LOGS_DIR, "error_report.txt")

EXPECTED_REPORT_LINES = [
    "2024-06-05 10:41:33 extract Unable to read data source",
    "2024-06-05 10:41:35 transform Data type mismatch in column 'age'",
    "2024-06-05 10:41:37 load Target database unreachable",
]

def test_error_report_file_exists():
    assert os.path.isfile(ERROR_REPORT_FILE), (
        f"File '{ERROR_REPORT_FILE}' does not exist. "
        "You must create error_report.txt in /home/user/pipeline_logs/."
    )

def test_error_report_contents_exact():
    """
    The error_report.txt file must contain exactly the expected lines, in order, no extra whitespace or lines.
    """
    with open(ERROR_REPORT_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Accept either the expected error lines or the "No errors found." case
    if lines == EXPECTED_REPORT_LINES:
        return  # Success, exact match
    elif lines == ["No errors found."]:
        pytest.fail(
            f"error_report.txt says 'No errors found.' but there are errors in pipeline.log.\n"
            "Expected lines:\n"
            + "\n".join(EXPECTED_REPORT_LINES)
        )
    else:
        # Figure out what went wrong for helpful error message
        if not lines:
            pytest.fail(
                f"error_report.txt is empty. It must contain the extracted error lines, one per line, exactly as specified.\n"
                "Expected lines:\n"
                + "\n".join(EXPECTED_REPORT_LINES)
            )
        # Check for extra/missing lines
        if len(lines) != len(EXPECTED_REPORT_LINES):
            pytest.fail(
                f"error_report.txt has {len(lines)} line(s), expected {len(EXPECTED_REPORT_LINES)}.\n"
                f"Actual lines:\n{lines}\n"
                "Expected lines:\n"
                + "\n".join(EXPECTED_REPORT_LINES)
            )
        # Find first line mismatch
        for i, (actual, expected) in enumerate(zip(lines, EXPECTED_REPORT_LINES), 1):
            if actual != expected:
                pytest.fail(
                    f"Line {i} in error_report.txt is incorrect.\n"
                    f"Expected: '{expected}'\n"
                    f"Actual:   '{actual}'\n"
                    "Check timestamp, stage, and error message formatting."
                )
        # Fallback error
        pytest.fail(
            "error_report.txt is not formatted as required.\n"
            f"Actual lines:\n{lines}\n"
            "Expected lines:\n"
            + "\n".join(EXPECTED_REPORT_LINES)
        )

def test_no_extra_whitespace_or_blank_lines():
    """
    Ensure there is no leading/trailing whitespace or blank lines in error_report.txt.
    """
    with open(ERROR_REPORT_FILE, "r", encoding="utf-8") as f:
        raw = f.read()
    # Should not have trailing or leading whitespace/newlines
    stripped = raw.strip('\n')
    assert raw == stripped or raw == stripped + '\n', (
        "error_report.txt contains extra blank lines at the start or end. "
        "There should be no leading/trailing newlines."
    )
    # Each line should not have leading/trailing whitespace
    for i, line in enumerate(raw.splitlines(), 1):
        assert line == line.strip(), (
            f"Line {i} in error_report.txt has leading or trailing whitespace:\n"
            f"'{line}'"
        )

def test_report_not_overwritten_with_wrong_message():
    """
    Ensure the fallback 'No errors found.' is not present if errors were present.
    """
    with open(ERROR_REPORT_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    if "No errors found." in lines and lines != ["No errors found."]:
        pytest.fail(
            "error_report.txt contains 'No errors found.' along with error lines. "
            "If errors are present, only the extracted error lines must be present."
        )