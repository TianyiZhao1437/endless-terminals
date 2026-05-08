# test_final_state.py

import os
import pytest

SERVICE_UPDATES_PATH = "/home/user/deployment_data/service_updates.log"
SERVICE_UPDATE_FREQ_PATH = "/home/user/deployment_data/service_update_frequencies.log"

@pytest.mark.describe("Final OS/filesystem state after student action")
def test_service_update_frequencies_log_exists():
    """Verify that the output frequency file exists after processing."""
    assert os.path.isfile(SERVICE_UPDATE_FREQ_PATH), (
        f"Missing required file: {SERVICE_UPDATE_FREQ_PATH}. "
        "You must create this file as the frequency report."
    )

@pytest.mark.describe("Final OS/filesystem state after student action")
def test_service_update_frequencies_log_content():
    """
    Verify the frequency report file contents:
    - Sorted alphabetically by service name.
    - Format: <service_name>: <frequency>
    - No extra blank lines, spaces, or headers/footers.
    """
    expected_lines = [
        "auth: 3",
        "cache: 1",
        "db: 1",
        "webserver: 3",
    ]

    # Check file existence
    assert os.path.isfile(SERVICE_UPDATE_FREQ_PATH), (
        f"{SERVICE_UPDATE_FREQ_PATH} does not exist. "
        "You must create this file with the correct frequency counts."
    )

    # Read actual file contents
    with open(SERVICE_UPDATE_FREQ_PATH, "rt", encoding="utf-8") as f:
        actual_lines = [line.rstrip('\n') for line in f]

    # Check for extra blank lines
    if any(line.strip() == "" for line in actual_lines):
        pytest.fail(
            f"{SERVICE_UPDATE_FREQ_PATH} contains extra blank lines. "
            "Remove any blank lines from the output file."
        )

    # Check for leading/trailing spaces
    for idx, line in enumerate(actual_lines):
        if line != line.strip():
            pytest.fail(
                f"Line {idx+1} in {SERVICE_UPDATE_FREQ_PATH} has leading/trailing spaces: '{line}'\n"
                "Remove any extra spaces at the start or end of lines."
            )

    # Check for correct lines and order
    assert actual_lines == expected_lines, (
        f"{SERVICE_UPDATE_FREQ_PATH} contents are incorrect.\n"
        f"Expected lines (order matters):\n{expected_lines}\n"
        f"Actual lines:\n{actual_lines}\n"
        "Ensure the file contains exactly these lines, in this order, one per line, "
        "with no extra blank lines, spaces, or headers/footers."
    )

@pytest.mark.describe("Final OS/filesystem state after student action")
def test_service_update_frequencies_log_line_endings():
    """Verify that the output file uses LF line endings only (no CRLF or CR)."""
    with open(SERVICE_UPDATE_FREQ_PATH, "rb") as f:
        content = f.read()
    if b"\r\n" in content:
        pytest.fail(
            f"{SERVICE_UPDATE_FREQ_PATH} contains CRLF (Windows) line endings. "
            "Use only LF (Unix) line endings."
        )
    if b"\r" in content:
        pytest.fail(
            f"{SERVICE_UPDATE_FREQ_PATH} contains CR (old Mac) line endings. "
            "Use only LF (Unix) line endings."
        )