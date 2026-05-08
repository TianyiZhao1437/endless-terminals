# test_initial_state.py

import os
import pytest

PIPELINE_LOGS_DIR = "/home/user/pipeline_logs"
PIPELINE_LOG_FILE = os.path.join(PIPELINE_LOGS_DIR, "pipeline.log")

EXPECTED_LOG_CONTENT = """2024-06-05 10:41:33 INFO stage:extract Source initialized
2024-06-05 10:41:33 ERROR stage:extract Unable to read data source
2024-06-05 10:41:34 INFO stage:transform Starting transformations
2024-06-05 10:41:35 ERROR stage:transform Data type mismatch in column 'age'
2024-06-05 10:41:35 WARN stage:transform Non-critical warning
2024-06-05 10:41:36 INFO stage:load Loading data into destination
2024-06-05 10:41:37 ERROR stage:load Target database unreachable
"""

def test_pipeline_logs_dir_exists():
    assert os.path.isdir(PIPELINE_LOGS_DIR), (
        f"Required directory '{PIPELINE_LOGS_DIR}' does not exist. "
        "Ensure the pipeline_logs directory is present before starting the task."
    )

def test_pipeline_log_file_exists():
    assert os.path.isfile(PIPELINE_LOG_FILE), (
        f"Required log file '{PIPELINE_LOG_FILE}' does not exist. "
        "Ensure pipeline.log is present in pipeline_logs before starting the task."
    )

def test_pipeline_log_file_content():
    with open(PIPELINE_LOG_FILE, "r", encoding="utf-8") as f:
        actual = f.read()
    # Normalize line endings and strip possible trailing newlines for robust comparison
    expected = EXPECTED_LOG_CONTENT.strip().replace('\r\n', '\n')
    actual = actual.strip().replace('\r\n', '\n')
    assert actual == expected, (
        f"The contents of '{PIPELINE_LOG_FILE}' do not match the expected initial state.\n"
        "Expected:\n"
        f"{expected}\n"
        "Actual:\n"
        f"{actual}\n"
        "Ensure the log file is unmodified before starting the task."
    )