# test_initial_state.py

import os
import pytest

HOME = "/home/user"
ARTIFACTS_DB = "/home/user/artifacts.db"
BINARIES_REPORT = "/home/user/binaries_report.txt"

def test_home_directory_exists_and_writable():
    assert os.path.isdir(HOME), f"Expected directory {HOME} to exist."
    assert os.access(HOME, os.W_OK), f"Expected directory {HOME} to be writable."

def test_artifacts_db_does_not_exist_initially():
    assert not os.path.exists(ARTIFACTS_DB), (
        f"File {ARTIFACTS_DB} should NOT exist before the task is performed."
    )

def test_binaries_report_does_not_exist_initially():
    assert not os.path.exists(BINARIES_REPORT), (
        f"File {BINARIES_REPORT} should NOT exist before the task is performed."
    )