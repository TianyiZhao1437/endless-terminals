# test_initial_state.py

import os
import pytest

SERVICE_STATUS_PATH = "/home/user/service_status_report.txt"

def test_service_status_report_file_does_not_exist():
    """
    Ensure that the status report file does NOT exist before the student runs their solution.
    """
    assert not os.path.exists(SERVICE_STATUS_PATH), (
        f"The file {SERVICE_STATUS_PATH} already exists. "
        "You should start with no such file present before running your command."
    )