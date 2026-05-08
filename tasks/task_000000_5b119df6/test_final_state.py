# test_final_state.py

import os
import pytest
import subprocess

ETL_ENV_DIR = "/home/user/etl_env"
PACKAGES_LIST_FILE = "/home/user/etl_env/packages_list.txt"

@pytest.mark.describe("Final OS/FS state for ETL pipeline environment preparation")
def test_etl_env_directory_still_exists():
    """The /home/user/etl_env directory must exist after the task is completed."""
    assert os.path.isdir(ETL_ENV_DIR), (
        f"Required directory '{ETL_ENV_DIR}' does not exist after task completion."
    )

def test_packages_list_file_exists():
    """The file /home/user/etl_env/packages_list.txt must exist after the task is completed."""
    assert os.path.isfile(PACKAGES_LIST_FILE), (
        f"File '{PACKAGES_LIST_FILE}' does not exist after task completion."
    )

def test_packages_list_file_content_matches_pip_list():
    """
    The contents of /home/user/etl_env/packages_list.txt must match the exact output of 'pip list'
    as produced in the current environment, including headers, formatting, and package list.
    """
    # Get current 'pip list' output as bytes
    try:
        pip_list_output = subprocess.check_output(
            ["pip", "list"], stderr=subprocess.STDOUT
        )
    except FileNotFoundError:
        pytest.fail(
            "Could not run 'pip list'. Is pip installed and available in the PATH?"
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(
            f"Error running 'pip list': {e.output.decode('utf-8', errors='replace')}"
        )

    # Read the file as bytes
    try:
        with open(PACKAGES_LIST_FILE, "rb") as f:
            file_content = f.read()
    except Exception as e:
        pytest.fail(
            f"Failed to read '{PACKAGES_LIST_FILE}': {e}"
        )

    # Compare byte-for-byte
    if file_content != pip_list_output:
        # Find where the mismatch occurs for easier debugging
        pip_lines = pip_list_output.splitlines()
        file_lines = file_content.splitlines()

        mismatch_index = None
        for i, (pip_line, file_line) in enumerate(zip(pip_lines, file_lines)):
            if pip_line != file_line:
                mismatch_index = i
                break
        if mismatch_index is not None:
            pip_line_str = pip_lines[mismatch_index].decode('utf-8', errors='replace')
            file_line_str = file_lines[mismatch_index].decode('utf-8', errors='replace')
            msg = (
                f"Mismatch at line {mismatch_index+1}:\n"
                f"Expected (from 'pip list'): '{pip_line_str}'\n"
                f"Found in file:           '{file_line_str}'"
            )
        else:
            # If number of lines differs, or mismatch after zip
            msg = (
                f"File '{PACKAGES_LIST_FILE}' does not match 'pip list' output.\n"
                f"Number of lines in 'pip list': {len(pip_lines)}\n"
                f"Number of lines in file:      {len(file_lines)}"
            )
        pytest.fail(
            f"The contents of '{PACKAGES_LIST_FILE}' do not match the current 'pip list' output.\n"
            f"{msg}\n"
            "Please ensure you run 'pip list' and save its exact output to the file."
        )

def test_packages_list_file_is_writable():
    """
    The file should be writable by the user (not read-only), so the ETL pipeline can update it in future steps.
    """
    assert os.access(PACKAGES_LIST_FILE, os.W_OK), (
        f"File '{PACKAGES_LIST_FILE}' is not writable. "
        "Please ensure user has write permissions on this file."
    )