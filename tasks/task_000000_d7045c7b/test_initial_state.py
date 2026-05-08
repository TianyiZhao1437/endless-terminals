"""
test_initial_state.py

Pytest suite to validate the initial state of the OS/filesystem before the student performs the benchmarking/logging task.
"""

import os
import pwd
import pytest

HOME = "/home/user"
BENCHMARKS_DIR = f"{HOME}/benchmarks"
LOG_FILE = f"{BENCHMARKS_DIR}/performance_tickets.log"

def test_benchmarks_directory_does_not_exist():
    """
    The /home/user/benchmarks directory must NOT exist before the task.
    """
    assert not os.path.exists(BENCHMARKS_DIR), (
        f"The directory {BENCHMARKS_DIR} should NOT exist before you begin the task. "
        f"Remove it before starting."
    )

def test_log_file_does_not_exist():
    """
    The /home/user/benchmarks/performance_tickets.log file must NOT exist before the task.
    """
    assert not os.path.exists(LOG_FILE), (
        f"The log file {LOG_FILE} should NOT exist before you begin the task. "
        f"Remove it before starting."
    )