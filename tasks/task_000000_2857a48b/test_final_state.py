# test_final_state.py

import os
import sys
import pytest

PROJECT_DIR = "/home/user/projects/support_app"
VENV_DIR = os.path.join(PROJECT_DIR, "env_support")
LOG_FILE = os.path.join(PROJECT_DIR, "venv_setup.log")
LOG_EXPECTED_LINE = f"Venv created: {VENV_DIR}"

def test_env_support_directory_exists():
    assert os.path.isdir(VENV_DIR), (
        f"The virtual environment directory '{VENV_DIR}' does not exist. "
        "You must create the venv using Python's built-in venv module."
    )

def test_venv_structure():
    # The venv should contain at minimum: pyvenv.cfg, bin/, lib/
    pyvenv_cfg = os.path.join(VENV_DIR, "pyvenv.cfg")
    bin_dir = os.path.join(VENV_DIR, "bin")
    lib_dir = os.path.join(VENV_DIR, "lib")

    assert os.path.isfile(pyvenv_cfg), (
        f"'pyvenv.cfg' is missing in '{VENV_DIR}'. "
        "This file is required for a valid Python virtual environment."
    )
    assert os.path.isdir(bin_dir), (
        f"'bin/' directory is missing in '{VENV_DIR}'. "
        "This directory is required for a valid Python virtual environment."
    )
    assert os.path.isdir(lib_dir), (
        f"'lib/' directory is missing in '{VENV_DIR}'. "
        "This directory is required for a valid Python virtual environment."
    )

    # Check that at least one executable exists in bin/
    bin_contents = os.listdir(bin_dir)
    python_executables = [fname for fname in bin_contents if fname.startswith("python")]
    assert python_executables, (
        f"No Python executable found in '{bin_dir}'. "
        "The venv's bin directory should contain a Python executable."
    )

def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"The log file '{LOG_FILE}' does not exist. "
        "You must generate the log file after creating the venv."
    )

def test_log_file_content_exact():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read log file '{LOG_FILE}': {e}")

    # Check for exact content: single line, no extra whitespace, no extra lines
    if content != LOG_EXPECTED_LINE:
        # Show a diff-like output for debugging
        import reprlib
        actual_repr = reprlib.repr(content)
        expected_repr = reprlib.repr(LOG_EXPECTED_LINE)
        pytest.fail(
            f"Log file '{LOG_FILE}' content is incorrect.\n"
            f"Expected exactly:\n  {expected_repr}\n"
            f"But got:\n  {actual_repr}\n"
            "Ensure the log file contains only the required single line, "
            "without extra spaces, newlines, or formatting."
        )

def test_log_file_no_extra_lines():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1, (
        f"Log file '{LOG_FILE}' should contain exactly one line, "
        f"but found {len(lines)} lines."
    )
    # The line should not have trailing newline or whitespace
    line = lines[0]
    assert line == LOG_EXPECTED_LINE, (
        f"Log file '{LOG_FILE}' line is not exactly correct.\n"
        f"Expected: '{LOG_EXPECTED_LINE}'\n"
        f"Found:    '{line}'"
    )