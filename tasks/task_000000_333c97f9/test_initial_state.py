# test_initial_state.py

import os
import pytest

SERVICE_UPDATES_PATH = "/home/user/deployment_data/service_updates.log"
SERVICE_UPDATE_FREQ_PATH = "/home/user/deployment_data/service_update_frequencies.log"

@pytest.mark.describe("Initial OS/filesystem state before student action")
def test_service_updates_log_exists_and_content():
    """Verify that /home/user/deployment_data/service_updates.log exists and contains the correct lines."""
    assert os.path.isfile(SERVICE_UPDATES_PATH), (
        f"Missing required file: {SERVICE_UPDATES_PATH}. "
        "This file should exist before you begin processing."
    )

    expected_lines = [
        "webserver",
        "auth",
        "db",
        "webserver",
        "auth",
        "cache",
        "webserver",
        "auth",
    ]

    with open(SERVICE_UPDATES_PATH, "rt", encoding="utf-8") as f:
        actual_lines = [line.rstrip('\n') for line in f]

    assert actual_lines == expected_lines, (
        f"{SERVICE_UPDATES_PATH} does not contain the expected contents.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Actual lines:\n{actual_lines}\n"
        "Ensure the file contains exactly these lines (no extra spaces, no extra lines, LF endings)."
    )

@pytest.mark.describe("Initial OS/filesystem state before student action")
def test_service_update_frequencies_log_does_not_exist():
    """Ensure that /home/user/deployment_data/service_update_frequencies.log does NOT exist yet."""
    assert not os.path.exists(SERVICE_UPDATE_FREQ_PATH), (
        f"{SERVICE_UPDATE_FREQ_PATH} should NOT exist before you begin the task.\n"
        "Do not create the output file until you have processed the input."
    )