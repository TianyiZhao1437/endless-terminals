# test_final_state.py

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

EXPECTED_SUMMARY_CONTENT = """CPLEX, 2, 1
GLPK, 1, 0
Gurobi, 3, 1
"""

@pytest.mark.describe("Final OS state: /home/user/logs/solvers_summary.txt existence and contents")
def test_logs_directory_unchanged():
    assert os.path.isdir(LOGS_DIR), (
        f"Directory '{LOGS_DIR}' does not exist after completion. "
        "It must remain present."
    )

def test_log_file_unchanged():
    assert os.path.isfile(LOG_FILE), (
        f"Log file '{LOG_FILE}' is missing after completion. "
        "It must not be removed or renamed."
    )
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        actual_content = f.read()
    assert actual_content == EXPECTED_LOG_CONTENT, (
        f"Log file '{LOG_FILE}' contents have changed after completion.\n"
        "Expected:\n"
        f"{EXPECTED_LOG_CONTENT!r}\n"
        "Found:\n"
        f"{actual_content!r}\n"
        "Do not modify the log file."
    )

def test_summary_file_exists():
    assert os.path.isfile(SUMMARY_FILE), (
        f"Summary file '{SUMMARY_FILE}' does not exist after completion. "
        "It must be created in '{LOGS_DIR}'."
    )

def test_summary_file_contents():
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        actual_summary = f.read()
    assert actual_summary == EXPECTED_SUMMARY_CONTENT, (
        f"Summary file '{SUMMARY_FILE}' does not contain the exact expected contents.\n"
        "Expected:\n"
        f"{EXPECTED_SUMMARY_CONTENT!r}\n"
        "Found:\n"
        f"{actual_summary!r}\n"
        "Check formatting, ordering, and counts."
    )

def test_no_other_files_changed():
    # Ensure no other files exist or were changed in /home/user/logs/
    expected_files = {"solver_usage.log", "solvers_summary.txt"}
    actual_files = set(os.listdir(LOGS_DIR))
    unexpected_files = actual_files - expected_files
    assert not unexpected_files, (
        f"Unexpected files found in '{LOGS_DIR}': {sorted(unexpected_files)}. "
        "Only 'solver_usage.log' and 'solvers_summary.txt' should exist."
    )