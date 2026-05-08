# test_initial_state.py

import os
import pytest

LOGS_DIR = "/home/user/logs"
LOG_FILE = os.path.join(LOGS_DIR, "solver_usage.log")
SUMMARY_FILE = os.path.join(LOGS_DIR, "solvers_summary.txt")

EXPECTED_LOG_CONTENT = """2024-06-08T15:42:13Z Gurobi success
2024-06-08T15:50:12Z CPLEX failure
2024-06-08T16:01:27Z Gurobi failure
2024-06-08T16:10:05Z GLPK success
2024-06-08T16:15:42Z CPLEX success
2024-06-08T16:21:08Z Gurobi success
"""

@pytest.mark.describe("Initial OS state: /home/user/logs/solver_usage.log existence and contents")
def test_logs_directory_exists():
    assert os.path.isdir(LOGS_DIR), f"Required directory '{LOGS_DIR}' does not exist. Please create it before proceeding."

def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"Required log file '{LOG_FILE}' does not exist. "
        "Please ensure the file is present before proceeding."
    )

def test_log_file_contents():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_LOG_CONTENT, (
        f"The file '{LOG_FILE}' does not contain the expected contents.\n"
        "Expected:\n"
        f"{EXPECTED_LOG_CONTENT!r}\n"
        "Found:\n"
        f"{content!r}\n"
        "Please ensure the file contents are exactly as specified before proceeding."
    )

def test_summary_file_does_not_exist():
    assert not os.path.exists(SUMMARY_FILE), (
        f"The summary file '{SUMMARY_FILE}' already exists. "
        "It should not exist before you begin the task."
    )