# test_final_state.py

import pytest
import os

IP_FREQUENCY_LOG_PATH = "/home/user/ip_frequency.log"

# The expected content of /home/user/ip_frequency.log after the task is completed.
EXPECTED_IP_FREQUENCY_LOG_CONTENT = """1 198.51.100.99
4 192.168.1.11
2 192.168.1.12
4 203.0.113.52
"""

@pytest.mark.final_state
def test_ip_frequency_log_exists():
    """Ensure the output file exists at the correct absolute path."""
    assert os.path.isfile(IP_FREQUENCY_LOG_PATH), (
        f"Missing output file: {IP_FREQUENCY_LOG_PATH}. "
        "You must create this file with the IP frequency results."
    )

@pytest.mark.final_state
def test_ip_frequency_log_content_exact():
    """
    Validate the contents of /home/user/ip_frequency.log:
    - Each line is in the format: <count> <IP>
    - Lines are sorted by IP address (ascending, as strings)
    - All IPs from the access log are present with correct counts
    - The file contains only the expected lines, in the correct order
    """
    with open(IP_FREQUENCY_LOG_PATH, "r", encoding="utf-8") as f:
        actual_content = f.read()

    # Normalize line endings and strip trailing whitespace for comparison
    expected_lines = EXPECTED_IP_FREQUENCY_LOG_CONTENT.strip().splitlines()
    actual_lines = actual_content.strip().splitlines()

    assert actual_lines == expected_lines, (
        f"The contents of {IP_FREQUENCY_LOG_PATH} do not match the expected results.\n"
        "Expected content:\n"
        + "\n".join(expected_lines)
        + "\nActual content:\n"
        + "\n".join(actual_lines)
        + "\n\n"
        "Make sure:\n"
        "- Each line is: <count> <IP>\n"
        "- All IPs from the access log are included, even if count is 1\n"
        "- Lines are sorted by IP address in ascending order\n"
        "- There are no extra, missing, or out-of-order lines\n"
    )

@pytest.mark.final_state
def test_ip_frequency_log_no_extra_blank_lines():
    """
    The output file must not have extra blank lines at the end or between lines.
    """
    with open(IP_FREQUENCY_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove possible trailing newline at end of file for this check
    stripped_lines = [line.rstrip('\r\n') for line in lines]

    # No lines should be empty
    for idx, line in enumerate(stripped_lines, 1):
        assert line.strip() != "", (
            f"Blank line detected at line {idx} in {IP_FREQUENCY_LOG_PATH}. "
            "There must be no empty lines in the output file."
        )

@pytest.mark.final_state
def test_ip_frequency_log_permissions():
    """
    The output file should be readable by the user.
    """
    assert os.access(IP_FREQUENCY_LOG_PATH, os.R_OK), (
        f"The file {IP_FREQUENCY_LOG_PATH} is not readable. "
        "Check file permissions."
    )