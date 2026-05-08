# test_initial_state.py

import os
import pytest

HOME = "/home/user"
DATA_DIR = os.path.join(HOME, "data")
SERVER_USAGE_CSV = os.path.join(DATA_DIR, "server_usage.csv")
EXPECTED_CSV_CONTENT = """2024-06-04,server1,70.4,2564
2024-06-05,server1,78.5,2048
2024-06-04,server2,92.0,1740
2024-06-05,server2,88.2,1820
2024-06-04,server3,66.0,1480
2024-06-05,server3,68.1,1620
"""

def test_data_directory_exists_and_writable():
    assert os.path.isdir(DATA_DIR), (
        f"Required directory '{DATA_DIR}' does not exist. "
        "Please ensure the /home/user/data/ directory is present."
    )
    assert os.access(DATA_DIR, os.W_OK), (
        f"Directory '{DATA_DIR}' is not writable by the user. "
        "Please ensure proper permissions."
    )

def test_server_usage_csv_exists():
    assert os.path.isfile(SERVER_USAGE_CSV), (
        f"Input file '{SERVER_USAGE_CSV}' does not exist. "
        "Please ensure the input data file is present before running your solution."
    )

def test_server_usage_csv_content():
    with open(SERVER_USAGE_CSV, "r", encoding="utf-8") as f:
        content = f.read()
    # Normalize line endings and trailing newlines for robust comparison
    norm_actual = "\n".join([line.rstrip() for line in content.strip().splitlines()])
    norm_expected = "\n".join([line.rstrip() for line in EXPECTED_CSV_CONTENT.strip().splitlines()])
    assert norm_actual == norm_expected, (
        f"The contents of '{SERVER_USAGE_CSV}' do not match the expected input data.\n"
        "Expected:\n"
        f"{EXPECTED_CSV_CONTENT}"
        "\nBut found:\n"
        f"{content}"
    )