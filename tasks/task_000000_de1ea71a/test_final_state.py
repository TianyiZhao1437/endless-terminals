# test_final_state.py

import os
import re
import pytest

REPORT_PATH = "/home/user/reports/restore_report.txt"
EXPECTED_FILENAMES = ["picture1.jpg", "notes.docx", "archive.tar.gz"]

DATETIME_REGEX = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
LINE_PATTERN_TEMPLATE = r"^{filename}, {datetime}$"


def test_restore_report_exists():
    assert os.path.isfile(REPORT_PATH), (
        f"Missing required report file: {REPORT_PATH}.\n"
        "You must create this file as the report after restoring."
    )


def test_restore_report_line_count():
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 3, (
        f"{REPORT_PATH} should contain exactly three lines (one per file in the backup list).\n"
        f"Found {len(lines)} lines.\n"
        f"Lines found:\n{''.join(lines)}"
    )


@pytest.mark.parametrize("lineno,expected_filename", enumerate(EXPECTED_FILENAMES))
def test_restore_report_line_format(lineno, expected_filename):
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Defensive: already checked file exists and line count is 3 in previous tests.
    line = lines[lineno].rstrip("\n")

    # Build expected regex for this line
    pattern = LINE_PATTERN_TEMPLATE.format(
        filename=re.escape(expected_filename),
        datetime=DATETIME_REGEX
    )

    if not re.match(pattern, line):
        msg = (
            f"Line {lineno+1} of {REPORT_PATH} is malformed or incorrect.\n"
            f"Expected format: '{expected_filename}, YYYY-MM-DD HH:MM:SS'\n"
            f"Actual line: '{line}'\n"
            "Ensure the filename is correct, followed by a comma and a single space, then the date/time in 'YYYY-MM-DD HH:MM:SS' 24-hour format."
        )
        assert False, msg