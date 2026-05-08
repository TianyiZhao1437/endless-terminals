# test_initial_state.py

import os
import pytest

SCAN_RESULTS_PATH = "/home/user/scan_results.txt"
OPEN_PORTS_FREQ_PATH = "/home/user/open_ports_frequencies.txt"

EXPECTED_SCAN_RESULTS = [
    "192.168.1.10 22",
    "192.168.1.12 80",
    "192.168.1.15 22",
    "192.168.1.18 443",
    "192.168.1.20 80",
    "192.168.1.21 443",
    "192.168.1.22 8080",
    "192.168.1.23 22",
    "192.168.1.30 80"
]

@pytest.mark.parametrize("path", [SCAN_RESULTS_PATH])
def test_scan_results_file_exists(path):
    assert os.path.isfile(path), (
        f"Required input file '{path}' does not exist. "
        f"Please ensure you have the correct scan results file before starting."
    )

def test_scan_results_file_content():
    assert os.path.isfile(SCAN_RESULTS_PATH), (
        f"Required input file '{SCAN_RESULTS_PATH}' does not exist. "
        f"Please ensure you have the correct scan results file before starting."
    )
    with open(SCAN_RESULTS_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    assert lines == EXPECTED_SCAN_RESULTS, (
        f"The contents of '{SCAN_RESULTS_PATH}' do not match the expected scan results.\n"
        f"Expected:\n{chr(10).join(EXPECTED_SCAN_RESULTS)}\n"
        f"Found:\n{chr(10).join(lines)}"
    )

def test_open_ports_frequencies_file_not_present_yet():
    assert not os.path.exists(OPEN_PORTS_FREQ_PATH), (
        f"The output file '{OPEN_PORTS_FREQ_PATH}' already exists. "
        f"Please remove it before starting the task, as it should only be created after completion."
    )