# test_final_state.py
"""
Pytest suite to validate the FINAL state of the OS/filesystem after organizing project files.

Checks:
1. /home/user/project/organized_files.txt exists and contains exactly:
    helper.py
    main.c
    math.c
    script.sh
   (Alphabetically sorted, deduped, no .md/.txt, no extra whitespace/newlines.)

2. /home/user/project/organization_log.txt exists and contains exactly:
    2024-06-17T15:45:22Z Processed: 7, Excluded: 3, Written: 4
   (Single line, exact timestamp, no extra whitespace or lines.)
"""

import os
import pytest

PROJECT_DIR = "/home/user/project"
ORGANIZED_FILES_PATH = "/home/user/project/organized_files.txt"
LOG_PATH = "/home/user/project/organization_log.txt"

EXPECTED_ORGANIZED_FILES = [
    "helper.py",
    "main.c",
    "math.c",
    "script.sh"
]

EXPECTED_LOG_LINE = "2024-06-17T15:45:22Z Processed: 7, Excluded: 3, Written: 4"

def test_organized_files_txt_exists():
    assert os.path.isfile(ORGANIZED_FILES_PATH), (
        f"Missing required file: {ORGANIZED_FILES_PATH}\n"
        "You must create this file with the required content."
    )

def test_organized_files_txt_content_exact():
    try:
        with open(ORGANIZED_FILES_PATH, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception as e:
        pytest.fail(f"Could not read {ORGANIZED_FILES_PATH}: {e}")

    if lines != EXPECTED_ORGANIZED_FILES:
        # Show unified diff for clarity
        import difflib
        diff = "\n".join(difflib.unified_diff(
            EXPECTED_ORGANIZED_FILES, lines,
            fromfile="expected", tofile="actual", lineterm=""
        ))
        pytest.fail(
            f"{ORGANIZED_FILES_PATH} does not have the exact required content.\n"
            "Expected content (no extra lines, sorted, deduped, no .md/.txt):\n"
            + "\n".join(EXPECTED_ORGANIZED_FILES)
            + "\n\nDifference:\n" + diff
        )

def test_organized_files_txt_no_trailing_empty_line():
    with open(ORGANIZED_FILES_PATH, "rb") as f:
        content = f.read()
    # The file should not end with a double newline or a trailing newline after the last line.
    # If there are lines, the total number of '\n' bytes should be len(EXPECTED_ORGANIZED_FILES)-1
    num_newlines = content.count(b'\n')
    expected_newlines = max(0, len(EXPECTED_ORGANIZED_FILES) - 1)
    assert num_newlines == expected_newlines, (
        f"{ORGANIZED_FILES_PATH} should contain exactly {expected_newlines} newline characters "
        f"(one per line, no trailing newline after the last line), but found {num_newlines}."
    )

def test_organization_log_txt_exists():
    assert os.path.isfile(LOG_PATH), (
        f"Missing required log file: {LOG_PATH}\n"
        "You must create this file with the required log line."
    )

def test_organization_log_txt_content_exact():
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except Exception as e:
        pytest.fail(f"Could not read {LOG_PATH}: {e}")

    if len(lines) != 1:
        pytest.fail(
            f"{LOG_PATH} must contain exactly one line (no blank lines before/after).\n"
            f"Found {len(lines)} lines: {lines}"
        )

    if lines[0] != EXPECTED_LOG_LINE:
        pytest.fail(
            f"{LOG_PATH} does not contain the exact required log line.\n"
            f"Expected:\n{EXPECTED_LOG_LINE}\n"
            f"Actual:\n{lines[0]}"
        )

def test_organization_log_txt_no_trailing_empty_line():
    with open(LOG_PATH, "rb") as f:
        content = f.read()
    # There should be no trailing newline after the log line
    assert not content.endswith(b'\n'), (
        f"{LOG_PATH} must NOT end with a trailing newline after the log line."
    )