# test_initial_state.py

import os
import pytest

ENV_PATH = "/home/user/backup_job/.env"

@pytest.mark.describe("Check for the existence and contents of the .env file for backup integrity.")
def test_env_file_exists():
    assert os.path.isfile(ENV_PATH), (
        f"Required .env file not found at {ENV_PATH}. "
        "Ensure the file exists with the correct path before proceeding."
    )

@pytest.mark.describe("Validate the .env file contains the required INTEGRITY_KEY variable with correct value.")
def test_env_file_contains_integrity_key():
    try:
        with open(ENV_PATH, "r") as f:
            lines = f.readlines()
    except Exception as e:
        pytest.fail(f"Could not read {ENV_PATH}: {e}")

    found = False
    expected_value = "abc123secure"
    for line in lines:
        line = line.strip()
        if line.startswith("INTEGRITY_KEY="):
            found = True
            # Ensure exact value
            actual_value = line[len("INTEGRITY_KEY="):]
            assert actual_value == expected_value, (
                f"INTEGRITY_KEY in {ENV_PATH} does not have the expected value.\n"
                f"Expected: {expected_value}\n"
                f"Found: {actual_value}"
            )
            break
    assert found, (
        f"{ENV_PATH} is missing the INTEGRITY_KEY variable. "
        "Add a line like INTEGRITY_KEY=your_integrity_value to the file."
    )

@pytest.mark.describe("Ensure no extra files or directories are present for this task.")
def test_no_output_files_created():
    # This test is just a placeholder to clarify that no output files or directories should exist.
    # Since no files are to be created, this always passes.
    pass