# test_final_state.py

import os
import pytest

HOME = "/home/user"
OUTPUT_DIR = os.path.join(HOME, "services", "output")
AUDIT_REPORT_PATH = os.path.join(OUTPUT_DIR, "audit_report.txt")

EXPECTED_AUDIT_REPORT_CONTENT = (
    "Service Name: auth\n"
    "Database Port: 5432\n"
)

def test_audit_report_exists():
    assert os.path.isfile(AUDIT_REPORT_PATH), (
        f"Output file not found: {AUDIT_REPORT_PATH}"
    )

def test_audit_report_content_exact():
    with open(AUDIT_REPORT_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()
    assert actual_content == EXPECTED_AUDIT_REPORT_CONTENT, (
        f"File {AUDIT_REPORT_PATH} does not contain the expected content.\n"
        "Expected content:\n"
        f"{EXPECTED_AUDIT_REPORT_CONTENT!r}\n"
        "Actual content:\n"
        f"{actual_content!r}\n"
        "Ensure there are no extra lines or spaces, and the formatting matches exactly."
    )

def test_audit_report_no_extra_lines():
    with open(AUDIT_REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 2, (
        f"File {AUDIT_REPORT_PATH} should contain exactly 2 lines, found {len(lines)} lines.\n"
        f"Lines: {lines}"
    )
    for idx, line in enumerate(lines, 1):
        assert line.endswith('\n'), (
            f"Line {idx} in {AUDIT_REPORT_PATH} does not end with a newline character: {line!r}"
        )
        assert line.strip() == line.rstrip('\n'), (
            f"Line {idx} in {AUDIT_REPORT_PATH} contains extra spaces: {line!r}"
        )