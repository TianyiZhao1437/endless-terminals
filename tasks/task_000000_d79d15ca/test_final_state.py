# test_final_state.py

import os
import pytest

WORKFLOWS_DB = '/home/user/workflows.db'
CSV_PATH = '/home/user/active_workflows.csv'

# The expected CSV output (as lines, no header, no extra spaces or lines)
EXPECTED_CSV_LINES = [
    "1,Email Sync,active",
    "3,Slack Notification,active",
    "5,FTP Transfer,active",
]

def test_active_workflows_csv_exists():
    """Check that the active_workflows.csv file was created."""
    assert os.path.isfile(CSV_PATH), (
        f"Required output file '{CSV_PATH}' does not exist. "
        "You must create this file with the extracted active workflows."
    )

def test_active_workflows_csv_contents_exact():
    """
    The CSV file must contain exactly three lines, one for each active workflow
    (id, name, status), comma-separated, with no header and no extra lines or spaces.
    """
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    assert lines == EXPECTED_CSV_LINES, (
        f"Contents of '{CSV_PATH}' do not match the expected active workflows.\n"
        f"Expected lines:\n{EXPECTED_CSV_LINES}\n"
        f"Found:\n{lines}\n"
        "Ensure the CSV contains only the active workflows, in order, with no header or extra lines."
    )

def test_active_workflows_csv_no_extra_content():
    """Check for no trailing blank lines or extra whitespace in the CSV."""
    with open(CSV_PATH, 'rb') as f:
        content = f.read()
    # Should end with the last record, not newline
    assert content.rstrip(b'\r\n').endswith(EXPECTED_CSV_LINES[-1].encode('utf-8')), (
        f"'{CSV_PATH}' has extra blank lines or whitespace at the end. "
        "There must be no trailing empty lines after the last record."
    )

def test_active_workflows_csv_overwritten(tmp_path):
    """
    If the CSV file existed before, it must be overwritten with only the current active workflows.
    This test checks that no lines from previous runs or other statuses are present.
    """
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    for line in lines:
        parts = line.split(',')
        assert len(parts) == 3, (
            f"Line '{line}' in '{CSV_PATH}' does not have exactly 3 comma-separated fields."
        )
        # Check id is one of the expected ones
        assert line in EXPECTED_CSV_LINES, (
            f"Unexpected line '{line}' found in '{CSV_PATH}'. "
            "Only the exact active workflows should be present."
        )