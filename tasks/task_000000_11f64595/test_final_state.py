# test_final_state.py

import os
import pytest

CERT_LOGS_DIR = "/home/user/cert_logs"
LOG1 = os.path.join(CERT_LOGS_DIR, "cert_activity_01.log")
LOG2 = os.path.join(CERT_LOGS_DIR, "cert_activity_02.log")
SUMMARY = os.path.join(CERT_LOGS_DIR, "self_signed_summary.log")

# The expected contents of the source log files (should be unmodified)
EXPECTED_LOG1 = [
    "2024-06-01T10:12:54Z alice self-signed",
    "2024-06-01T11:30:02Z carol ca-signed",
    "2024-06-02T08:07:23Z bob self-signed",
]

EXPECTED_LOG2 = [
    "2024-06-03T12:04:12Z eve self-signed",
    "2024-06-02T13:15:58Z dan ca-signed",
    "2024-06-02T20:09:40Z frank self-signed",
]

# The expected summary output, sorted by timestamp ascending (ISO8601)
EXPECTED_SUMMARY = [
    "2024-06-01T10:12:54Z alice",
    "2024-06-02T08:07:23Z bob",
    "2024-06-02T20:09:40Z frank",
    "2024-06-03T12:04:12Z eve",
]

def read_file_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f.readlines()]

def test_cert_logs_directory_exists():
    assert os.path.isdir(CERT_LOGS_DIR), (
        f"Directory '{CERT_LOGS_DIR}' is missing. "
        "The cert_logs directory must not be removed or renamed."
    )

@pytest.mark.parametrize("path,expected_lines", [
    (LOG1, EXPECTED_LOG1),
    (LOG2, EXPECTED_LOG2),
])
def test_source_log_files_exist_and_unchanged(path, expected_lines):
    assert os.path.isfile(path), (
        f"Source log file '{path}' is missing. "
        "Do not remove or rename the source log files."
    )
    actual_lines = read_file_lines(path)
    assert actual_lines == expected_lines, (
        f"Source log file '{path}' has been modified.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Actual lines:\n{actual_lines}\n"
        "Do not alter the contents of the source log files."
    )

def test_summary_file_exists():
    assert os.path.isfile(SUMMARY), (
        f"Output file '{SUMMARY}' does not exist.\n"
        "You must create this file as specified."
    )

def test_summary_file_content_and_format():
    lines = read_file_lines(SUMMARY)
    assert lines == EXPECTED_SUMMARY, (
        f"Output file '{SUMMARY}' does not have the expected content or order.\n"
        "Expected (in this exact order):\n"
        + "\n".join(EXPECTED_SUMMARY)
        + "\nActual:\n"
        + "\n".join(lines)
        + "\n\n"
        "Make sure:\n"
        "- Only matching 'self-signed' entries are included\n"
        "- Only the timestamp and username fields are present (no certificate type)\n"
        "- No extra headers, blank lines, or trailing spaces\n"
        "- Entries are sorted in strict ascending order by timestamp (ISO8601)"
    )

def test_summary_file_no_extra_lines():
    """Checks for blank lines or extra whitespace at the end of the summary file."""
    with open(SUMMARY, "rb") as f:
        data = f.read()
    # Should end with the last character of the last line, not a blank line
    assert data.endswith(b"eve"), (
        f"Output file '{SUMMARY}' should not end with a blank line or extra whitespace."
    )

def test_summary_file_no_extra_files():
    """Ensure no unexpected files were created in the directory."""
    expected_files = {"cert_activity_01.log", "cert_activity_02.log", "self_signed_summary.log"}
    actual_files = set(os.listdir(CERT_LOGS_DIR))
    extra_files = actual_files - expected_files
    assert not extra_files, (
        f"Unexpected files found in '{CERT_LOGS_DIR}': {extra_files}\n"
        "Only the two source logs and 'self_signed_summary.log' should be present."
    )