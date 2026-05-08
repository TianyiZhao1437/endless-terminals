# test_final_state.py

import os
import stat
import pytest

APPDATA_DIR = '/home/user/appdata'
DB_PATH = '/home/user/appdata/diagnostics.db'
REPORT_PATH = '/home/user/diagnostics_report.txt'

# The expected contents of diagnostics_report.txt, with UNIX line endings.
EXPECTED_REPORT = (
    "Diagnostics for /home/user/appdata/diagnostics.db\n"
    "Table: users\n"
    "Columns: id,name,email\n"
    "Row count: 5\n"
    "\n"
    "Table: logs\n"
    "Columns: id,user_id,message,timestamp\n"
    "Row count: 10\n"
)

def test_appdata_directory_still_exists():
    assert os.path.isdir(APPDATA_DIR), (
        f"Directory '{APPDATA_DIR}' is missing after the task. "
        f"This directory must exist for the application and diagnostics."
    )

def test_diagnostics_db_still_exists_and_readable():
    assert os.path.isfile(DB_PATH), (
        f"SQLite database file '{DB_PATH}' is missing after the task. "
        f"It must not be deleted or moved."
    )
    st = os.stat(DB_PATH)
    readable = bool(st.st_mode & stat.S_IRUSR)
    assert readable, (
        f"SQLite database file '{DB_PATH}' is not readable after the task. "
        f"Permissions must allow read access for diagnostics."
    )

def test_diagnostics_report_exists():
    assert os.path.isfile(REPORT_PATH), (
        f"The diagnostics report file '{REPORT_PATH}' was not created. "
        f"Please ensure the report is written to this exact path."
    )

def test_diagnostics_report_content_and_format():
    try:
        with open(REPORT_PATH, 'rb') as f:
            content_bytes = f.read()
    except Exception as e:
        pytest.fail(
            f"Could not read '{REPORT_PATH}': {e}"
        )

    # Check for UNIX line endings only
    if b'\r' in content_bytes:
        pytest.fail(
            f"Report file '{REPORT_PATH}' contains Windows-style line endings (\\r). "
            f"Please use UNIX line endings (\\n) only."
        )

    content = content_bytes.decode('utf-8')

    # Check for no leading/trailing blank lines
    lines = content.split('\n')
    assert lines[0] == "Diagnostics for /home/user/appdata/diagnostics.db", (
        f"The first line of '{REPORT_PATH}' must be exactly:\n"
        f"  Diagnostics for /home/user/appdata/diagnostics.db\n"
        f"Found:\n"
        f"  {lines[0]}"
    )
    assert content.endswith('\n'), (
        f"The report file '{REPORT_PATH}' must end with a newline."
    )
    # There must NOT be an extra blank line after the last table section.
    assert not content.endswith('\n\n'), (
        f"The report file '{REPORT_PATH}' must not have extra blank lines at the end."
    )

    # Check exact content
    if content != EXPECTED_REPORT:
        # Find first difference for useful error reporting
        expected_lines = EXPECTED_REPORT.split('\n')
        actual_lines = content.split('\n')
        min_len = min(len(expected_lines), len(actual_lines))
        for i in range(min_len):
            if expected_lines[i] != actual_lines[i]:
                pytest.fail(
                    f"Mismatch in '{REPORT_PATH}' at line {i+1}:\n"
                    f"Expected: {expected_lines[i]!r}\n"
                    f"Found:    {actual_lines[i]!r}\n"
                    f"Full expected content:\n{EXPECTED_REPORT}"
                )
        if len(expected_lines) != len(actual_lines):
            pytest.fail(
                f"Report file '{REPORT_PATH}' has {len(actual_lines)} lines, "
                f"but expected {len(expected_lines)} lines.\n"
                f"Full expected content:\n{EXPECTED_REPORT}"
            )
        # If content differs but no obvious line difference, generic error:
        pytest.fail(
            f"Report file '{REPORT_PATH}' does not match expected content.\n"
            f"Full expected content:\n{EXPECTED_REPORT}"
        )