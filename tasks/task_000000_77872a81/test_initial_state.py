# test_initial_state.py

import os
import pytest

LOG_DIR = "/home/user/etl_logs"
LOG_FILE = "/home/user/etl_logs/pipeline_run.log"
EXPECTED_CONTENT = """[2024-06-29T14:23:57Z] user_import - FAILED
[2024-06-29T14:25:01Z] sales_transform - SUCCESS
[2024-06-29T14:27:42Z] user_import - SUCCESS
[2024-06-29T14:29:10Z] payment_load - FAILED
[2024-06-29T14:31:10Z] product_transform - FAILED
[2024-06-29T14:33:11Z] sales_transform - FAILED
[2024-06-29T14:35:11Z] payment_load - SUCCESS
"""

def test_etl_logs_directory_exists():
    assert os.path.isdir(LOG_DIR), (
        f"Directory '{LOG_DIR}' does not exist. "
        "Please ensure the ETL logs directory is present."
    )

def test_pipeline_run_log_exists():
    assert os.path.isfile(LOG_FILE), (
        f"File '{LOG_FILE}' does not exist. "
        "Please ensure the log file pipeline_run.log is present in /home/user/etl_logs/."
    )

def test_pipeline_run_log_readable():
    try:
        with open(LOG_FILE, "r") as f:
            f.read()
    except Exception as e:
        pytest.fail(
            f"File '{LOG_FILE}' is not readable: {e}. "
            "Please check file permissions."
        )

def test_pipeline_run_log_content():
    with open(LOG_FILE, "r") as f:
        actual_content = f.read()
    # Remove trailing newlines for comparison
    expected = EXPECTED_CONTENT.strip()
    actual = actual_content.strip()
    assert actual == expected, (
        f"File '{LOG_FILE}' does not contain the expected content.\n"
        "Expected content:\n"
        f"{expected}\n\n"
        "Actual content:\n"
        f"{actual}\n\n"
        "Please ensure the log file contains exactly the expected lines."
    )