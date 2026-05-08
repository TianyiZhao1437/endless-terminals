# test_final_state.py

import os
import pytest

DATA_DIR = "/home/user/data"
INPUT_CSV = os.path.join(DATA_DIR, "server_usage.csv")
REPORT_CSV = os.path.join(DATA_DIR, "peak_usage_report.csv")
LOG_FILE = os.path.join(DATA_DIR, "report_generation.log")

# The expected input file content, for reference
EXPECTED_INPUT_CSV = """2024-06-04,server1,70.4,2564
2024-06-05,server1,78.5,2048
2024-06-04,server2,92.0,1740
2024-06-05,server2,88.2,1820
2024-06-04,server3,66.0,1480
2024-06-05,server3,68.1,1620
"""

# The canonical expected output for the report
EXPECTED_REPORT_CSV = (
    "Server,Peak CPU Date,Peak CPU Value,Peak Memory Date,Peak Memory Value\n"
    "server1,2024-06-05,78.5,2024-06-04,2564\n"
    "server2,2024-06-04,92.0,2024-06-05,1820\n"
    "server3,2024-06-05,68.1,2024-06-05,1620\n"
)

# The canonical expected log file (two lines, no extra blank lines)
EXPECTED_LOG_CONTENT = (
    "Peak usage report generated successfully.\n"
    "Output file: /home/user/data/peak_usage_report.csv\n"
)

def test_data_directory_still_exists_and_writable():
    assert os.path.isdir(DATA_DIR), (
        f"Required directory '{DATA_DIR}' does not exist after the task. "
        "It must remain present."
    )
    assert os.access(DATA_DIR, os.W_OK), (
        f"Directory '{DATA_DIR}' is not writable by the user after the task. "
        "Permissions must not be changed."
    )

def test_input_csv_unchanged():
    assert os.path.isfile(INPUT_CSV), (
        f"Input file '{INPUT_CSV}' is missing after the task was completed. "
        "You must NOT delete or move the input file."
    )
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        content = f.read()
    norm_actual = "\n".join([line.rstrip() for line in content.strip().splitlines()])
    norm_expected = "\n".join([line.rstrip() for line in EXPECTED_INPUT_CSV.strip().splitlines()])
    assert norm_actual == norm_expected, (
        f"The input file '{INPUT_CSV}' was modified during processing. "
        "It must remain unchanged.\n"
        "Expected:\n"
        f"{EXPECTED_INPUT_CSV}"
        "\nBut found:\n"
        f"{content}"
    )

def test_peak_usage_report_created_with_correct_content():
    assert os.path.isfile(REPORT_CSV), (
        f"Output file '{REPORT_CSV}' does not exist. "
        "You must create the peak usage report file at the specified path."
    )
    with open(REPORT_CSV, "r", encoding="utf-8") as f:
        content = f.read()
    # Normalize line endings and trailing newlines for robust comparison
    norm_actual = "\n".join([line.rstrip() for line in content.strip().splitlines()])
    norm_expected = "\n".join([line.rstrip() for line in EXPECTED_REPORT_CSV.strip().splitlines()])
    assert norm_actual == norm_expected, (
        f"The contents of '{REPORT_CSV}' do not match the expected report.\n"
        "Expected:\n"
        f"{EXPECTED_REPORT_CSV}"
        "\nBut found:\n"
        f"{content}"
    )

def test_log_file_created_and_content_correct():
    assert os.path.isfile(LOG_FILE), (
        f"Log file '{LOG_FILE}' does not exist. "
        "You must create the log file at the specified path."
    )
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    # Check for exact two lines, including their order and no extra blank lines
    norm_actual = "\n".join([line.rstrip() for line in content.strip().splitlines()])
    norm_expected = "\n".join([line.rstrip() for line in EXPECTED_LOG_CONTENT.strip().splitlines()])
    assert norm_actual == norm_expected, (
        f"The contents of '{LOG_FILE}' do not match the expected log file.\n"
        "Expected:\n"
        f"{EXPECTED_LOG_CONTENT}"
        "\nBut found:\n"
        f"{content}"
    )