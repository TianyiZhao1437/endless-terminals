# test_final_state.py

import os
import subprocess
import pytest

HOME = "/home/user"
VENV_DIR = os.path.join(HOME, "logenv")
VENV_BIN = os.path.join(VENV_DIR, "bin")
VENV_ACTIVATE = os.path.join(VENV_BIN, "activate")
VENV_PYTHON = os.path.join(VENV_BIN, "python")
LOG_FILE = os.path.join(VENV_DIR, "setup_log.txt")


def get_installed_pandas_version():
    """
    Returns the installed pandas version string in the virtualenv,
    or raises AssertionError if not installed.
    """
    try:
        # Use pip show pandas to get the version
        result = subprocess.run(
            [VENV_PYTHON, "-m", "pip", "show", "pandas"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        for line in result.stdout.splitlines():
            if line.startswith("Version:"):
                return line.split(":", 1)[1].strip()
        pytest.fail(
            "Could not find a 'Version:' line for pandas in 'pip show pandas' output. "
            "Is pandas installed in the virtual environment?"
        )
    except FileNotFoundError:
        pytest.fail(f"Could not find python interpreter at {VENV_PYTHON}. "
                    "Is the virtual environment created?")
    except subprocess.CalledProcessError as e:
        pytest.fail(
            f"Failed to run 'pip show pandas' in the virtual environment. "
            f"stderr: {e.stderr.strip()}"
        )

def test_logenv_directory_exists():
    assert os.path.isdir(VENV_DIR), (
        f"The directory '{VENV_DIR}' does not exist.\n"
        "The virtual environment was not created at the required location."
    )

def test_activate_script_exists():
    assert os.path.isfile(VENV_ACTIVATE), (
        f"The virtual environment activate script '{VENV_ACTIVATE}' does not exist.\n"
        "The virtual environment is not valid or was not created using venv."
    )

def test_virtualenv_python_exists():
    assert os.path.isfile(VENV_PYTHON) and os.access(VENV_PYTHON, os.X_OK), (
        f"Could not find executable python interpreter at '{VENV_PYTHON}'.\n"
        "The virtual environment appears corrupt or was not created correctly."
    )

def test_pandas_installed_in_virtualenv():
    version = get_installed_pandas_version()
    assert version, (
        "Pandas is not installed in the virtual environment at "
        f"'{VENV_DIR}'."
    )

def test_setup_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"The log file '{LOG_FILE}' does not exist.\n"
        "You must create this file at the required location."
    )

def test_setup_log_file_contents():
    """
    Check that the log file contains the correct content and that the pandas version
    matches exactly what is installed in the virtualenv.
    """
    pandas_version = get_installed_pandas_version()
    expected_lines = [
        f"Virtual environment created at: {VENV_DIR}",
        f"Pandas version: {pandas_version}",
    ]

    try:
        with open(LOG_FILE, "r") as f:
            contents = f.read()
    except Exception as e:
        pytest.fail(
            f"Could not read the log file '{LOG_FILE}': {e}"
        )

    actual_lines = contents.strip().splitlines()
    assert actual_lines == expected_lines, (
        f"The contents of '{LOG_FILE}' are incorrect.\n"
        "Expected exactly:\n"
        f"---\n{expected_lines[0]}\n{expected_lines[1]}\n---\n"
        f"But got:\n"
        f"---\n{contents}\n---\n"
        "Please ensure the log file matches the required format, contains exactly two lines, "
        "and the pandas version matches the version installed in the virtual environment."
    )

def test_no_extra_lines_in_log():
    """
    The log file must contain exactly two lines, no more, no less.
    """
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    assert len(lines) == 2, (
        f"The log file '{LOG_FILE}' must contain exactly 2 lines.\n"
        f"It contains {len(lines)} lines."
    )