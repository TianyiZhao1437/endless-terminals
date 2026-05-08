# test_final_state.py

import os
import pytest

OPEN_PORTS_FREQ_PATH = "/home/user/open_ports_frequencies.txt"

# The exact expected output after processing /home/user/scan_results.txt
EXPECTED_OUTPUT_LINES = [
    "22 3",
    "80 3",
    "443 2",
    "8080 1"
]

def test_open_ports_frequencies_file_exists():
    assert os.path.isfile(OPEN_PORTS_FREQ_PATH), (
        f"Expected output file '{OPEN_PORTS_FREQ_PATH}' does not exist.\n"
        f"You must create this file as the result of your processing."
    )

def test_open_ports_frequencies_file_content_exact():
    """
    Ensure the output file exists and contains exactly the expected lines,
    in the correct order and format.
    """
    with open(OPEN_PORTS_FREQ_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    # Check line count
    assert len(lines) == len(EXPECTED_OUTPUT_LINES), (
        f"'{OPEN_PORTS_FREQ_PATH}' should have exactly {len(EXPECTED_OUTPUT_LINES)} lines, "
        f"but it has {len(lines)}.\n"
        f"Expected lines:\n{chr(10).join(EXPECTED_OUTPUT_LINES)}\n"
        f"Actual lines:\n{chr(10).join(lines)}"
    )

    # Check each line, order and formatting
    for i, (expected, actual) in enumerate(zip(EXPECTED_OUTPUT_LINES, lines), 1):
        assert actual == expected, (
            f"Line {i} of '{OPEN_PORTS_FREQ_PATH}' is incorrect.\n"
            f"Expected: '{expected}'\n"
            f"Found:    '{actual}'\n"
            f"Make sure your output lines have exactly one space between the port and count, "
            f"no extra spaces, and appear in ascending port order."
        )

def test_open_ports_frequencies_file_has_no_extra_blank_lines():
    """
    Ensure there are no extra blank lines at the end or between lines.
    """
    with open(OPEN_PORTS_FREQ_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # There must not be any blank/empty line
    for i, line in enumerate(lines, 1):
        assert line.strip() != "", (
            f"Line {i} of '{OPEN_PORTS_FREQ_PATH}' is blank or empty. "
            f"Do not include blank lines in your output."
        )