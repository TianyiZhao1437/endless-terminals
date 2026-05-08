# test_final_state.py

import os
import pytest

DIAGNOSTICS_DIR = "/home/user/diagnostics"
ERROR_LOG_PATH = os.path.join(DIAGNOSTICS_DIR, "error.log")
EXTRACTED_ERRORS_PATH = os.path.join(DIAGNOSTICS_DIR, "extracted_errors.txt")

expected_extracted_errors = (
    "2024-06-01 08:15:23 Disk failure detected on /dev/sda\n"
    "2024-06-01 09:02:11 Connection timed out while accessing database\n"
)


def test_extracted_errors_file_exists():
    assert os.path.isfile(EXTRACTED_ERRORS_PATH), (
        f"File '{EXTRACTED_ERRORS_PATH}' does not exist. "
        "You must create this file containing the extracted ERROR-level log entries."
    )


def test_extracted_errors_file_contents():
    if not os.path.isfile(EXTRACTED_ERRORS_PATH):
        pytest.skip(f"File '{EXTRACTED_ERRORS_PATH}' does not exist. Skipping content check.")

    with open(EXTRACTED_ERRORS_PATH, "r", encoding="utf-8") as f:
        contents = f.read()

    assert contents == expected_extracted_errors, (
        f"File '{EXTRACTED_ERRORS_PATH}' contents do not match the expected extracted errors.\n"
        "Expected:\n"
        f"{expected_extracted_errors!r}\n"
        "Found:\n"
        f"{contents!r}\n"
        "Ensure:\n"
        "- Only lines with log level ERROR are included\n"
        "- Each line contains the timestamp, a single space, then the log message (excluding 'ERROR:' and any extra spaces)\n"
        "- The order of lines matches the order in error.log\n"
        "- There are no extra blank lines or spaces"
    )

def test_extracted_errors_no_extra_lines():
    # Check that there are exactly two non-blank lines, and both match the required format.
    with open(EXTRACTED_ERRORS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove any trailing newlines for comparison
    stripped_lines = [line.rstrip('\n') for line in lines]

    assert len(stripped_lines) == 2, (
        f"File '{EXTRACTED_ERRORS_PATH}' should contain exactly 2 lines, "
        f"found {len(stripped_lines)}."
    )
    assert all(line for line in stripped_lines), (
        f"File '{EXTRACTED_ERRORS_PATH}' contains empty lines. "
        "There must be no empty or blank lines."
    )

    # Check for leading/trailing spaces
    for idx, line in enumerate(stripped_lines, 1):
        assert line == line.strip(), (
            f"Line {idx} in '{EXTRACTED_ERRORS_PATH}' has unexpected leading or trailing spaces: {line!r}"
        )

def test_extracted_errors_format_matches():
    # Each line must match the expected format: TIMESTAMP MESSAGE (no ERROR, no colon, no extra spaces)
    import re

    error_lines_expected = [
        ("2024-06-01 08:15:23", "Disk failure detected on /dev/sda"),
        ("2024-06-01 09:02:11", "Connection timed out while accessing database"),
    ]

    with open(EXTRACTED_ERRORS_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    timestamp_re = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    for idx, (expected_ts, expected_msg) in enumerate(error_lines_expected):
        if idx >= len(lines):
            pytest.fail(
                f"Line {idx+1} missing in '{EXTRACTED_ERRORS_PATH}'. "
                "Expected all ERROR entries to be present in order."
            )
        line = lines[idx]
        m = re.match(rf"^({timestamp_re}) (.+)$", line)
        assert m, (
            f"Line {idx+1} in '{EXTRACTED_ERRORS_PATH}' does not match the required format "
            f"'YYYY-MM-DD HH:MM:SS <message>': {line!r}"
        )
        ts, msg = m.groups()
        assert ts == expected_ts, (
            f"Line {idx+1} timestamp incorrect in '{EXTRACTED_ERRORS_PATH}': "
            f"expected '{expected_ts}', found '{ts}'."
        )
        assert msg == expected_msg, (
            f"Line {idx+1} message incorrect in '{EXTRACTED_ERRORS_PATH}': "
            f"expected '{expected_msg}', found '{msg}'."
        )