# test_final_state.py

import os
import sys
import stat
import pytest

VENV_DIR = "/home/user/devtools/pytools_env"
BIN_DIR = os.path.join(VENV_DIR, "bin")
LIB_DIR = os.path.join(VENV_DIR, "lib")
ACTIVATE_PATH = os.path.join(BIN_DIR, "activate")
PYTHON_PATH = os.path.join(BIN_DIR, "python")
SITE_PACKAGES_GLOB = os.path.join(LIB_DIR)  # We'll check that at least one site-packages exists

EXPECTED_OUTPUT = "/home/user/devtools/pytools_env\n"

def read_console_output():
    """
    Reads the output from the script execution.
    Assumes the output is stored in a file named 'console_output.txt' in the current directory.
    """
    output_file = "console_output.txt"
    if not os.path.isfile(output_file):
        pytest.fail(
            "Console output file 'console_output.txt' not found. "
            "Please ensure your script writes the output of the task to this file for testing."
        )
    with open(output_file, "r", encoding="utf-8") as f:
        return f.read()


def test_virtualenv_directory_exists():
    assert os.path.isdir(VENV_DIR), (
        f"The virtual environment directory '{VENV_DIR}' does not exist. "
        "It must be created using the venv module in the correct location."
    )

def test_virtualenv_bin_activate_exists():
    assert os.path.isfile(ACTIVATE_PATH), (
        f"The activate script '{ACTIVATE_PATH}' does not exist. "
        "The virtualenv is missing the 'activate' script in its bin directory."
    )
    # Should be readable
    assert os.access(ACTIVATE_PATH, os.R_OK), (
        f"The activate script '{ACTIVATE_PATH}' exists but is not readable."
    )

def test_virtualenv_bin_python_exists_and_is_executable():
    assert os.path.isfile(PYTHON_PATH), (
        f"The python binary '{PYTHON_PATH}' does not exist. "
        "The virtualenv is missing the python executable in its bin directory."
    )
    # Should be executable
    assert os.access(PYTHON_PATH, os.X_OK), (
        f"The python binary '{PYTHON_PATH}' exists but is not executable."
    )

def test_virtualenv_lib_and_site_packages_exists():
    assert os.path.isdir(LIB_DIR), (
        f"The lib directory '{LIB_DIR}' does not exist in the virtualenv. "
        "A valid venv must have a 'lib' directory."
    )
    # Find subdirectories of LIB_DIR, look for one ending with 'site-packages'
    found = False
    for entry in os.listdir(LIB_DIR):
        full_path = os.path.join(LIB_DIR, entry)
        if os.path.isdir(full_path) and "site-packages" in os.listdir(full_path):
            found = True
            break
        elif os.path.isdir(full_path) and entry.endswith("site-packages"):
            found = True
            break
    if not found:
        # Try deeper: look for a pythonX.Y directory, then site-packages inside
        for entry in os.listdir(LIB_DIR):
            py_dir = os.path.join(LIB_DIR, entry)
            if os.path.isdir(py_dir) and entry.startswith("python"):
                sp_dir = os.path.join(py_dir, "site-packages")
                if os.path.isdir(sp_dir):
                    found = True
                    break
    assert found, (
        f"No 'site-packages' directory found inside '{LIB_DIR}'. "
        "A valid venv must have a 'site-packages' directory inside the lib/pythonX.Y/ directory."
    )

def test_console_output_is_exact_and_only_path():
    output = read_console_output()
    assert output == EXPECTED_OUTPUT, (
        "Console output is not exactly as required.\n"
        f"Expected: {repr(EXPECTED_OUTPUT)}\n"
        f"Got:      {repr(output)}\n"
        "Output must be exactly the absolute path to the virtualenv directory, and nothing else."
    )