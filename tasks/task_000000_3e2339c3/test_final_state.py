# test_final_state.py

import os
import stat
import pytest

COMPLIANCE_DIR = "/home/user/compliance_check"
VENV_DIR = os.path.join(COMPLIANCE_DIR, "audit_env")
LOG_FILE = os.path.join(COMPLIANCE_DIR, "audit_env_creation.log")
EXPECTED_LOG_LINE = (
    "Virtual environment 'audit_env' created successfully at /home/user/compliance_check/audit_env"
)

# Standard venv subdirs and files for a Linux environment using Python's built-in venv
STANDARD_SUBDIRS = ["bin", "lib"]
STANDARD_FILES = ["pyvenv.cfg"]

def test_venv_dir_exists():
    assert os.path.isdir(VENV_DIR), (
        f"Virtual environment directory '{VENV_DIR}' does not exist. "
        "Ensure you have correctly created the venv using the 'venv' module."
    )

def test_venv_standard_structure():
    # Check for required subdirectories
    missing_subdirs = []
    for subdir in STANDARD_SUBDIRS:
        path = os.path.join(VENV_DIR, subdir)
        if not os.path.isdir(path):
            missing_subdirs.append(subdir)
    assert not missing_subdirs, (
        f"Virtual environment '{VENV_DIR}' is missing required subdirectories: {missing_subdirs}. "
        "Ensure the venv was initialized with the standard structure."
    )

    # Check for required files
    missing_files = []
    for filename in STANDARD_FILES:
        path = os.path.join(VENV_DIR, filename)
        if not os.path.isfile(path):
            missing_files.append(filename)
    assert not missing_files, (
        f"Virtual environment '{VENV_DIR}' is missing required files: {missing_files}. "
        "Ensure the venv was initialized with the standard structure."
    )

    # Check for the python executable in bin/
    python_bin = os.path.join(VENV_DIR, "bin", "python")
    assert os.path.isfile(python_bin), (
        f"'python' executable not found at '{python_bin}'. "
        "The virtual environment must contain a working Python executable in 'bin/'."
    )
    # Check that the python executable is indeed executable
    assert os.access(python_bin, os.X_OK), (
        f"'python' at '{python_bin}' is not executable. "
        "Ensure correct permissions are set."
    )

def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"Log file '{LOG_FILE}' does not exist. "
        "You must create this file after initializing the virtual environment."
    )

def test_log_file_content():
    with open(LOG_FILE, "rb") as f:
        content = f.read()
    # The log file must contain only the single line, no trailing newline or extra whitespace
    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError:
        raise AssertionError(
            f"Log file '{LOG_FILE}' is not valid UTF-8 text."
        )
    # Check for exact match, no trailing newline, spaces, or extra lines
    assert decoded == EXPECTED_LOG_LINE, (
        f"Log file '{LOG_FILE}' content is incorrect.\n"
        f"Expected exactly:\n{EXPECTED_LOG_LINE!r}\n"
        f"Found:\n{decoded!r}\n"
        "Ensure it contains only the required line, with no trailing newline, blank lines or extra whitespace."
    )

def test_no_extra_files_in_compliance_dir():
    expected = {"audit_env", "audit_env_creation.log"}
    actual = set(os.listdir(COMPLIANCE_DIR))
    extra = actual - expected
    missing = expected - actual
    assert not missing, (
        f"The following required items are missing from '{COMPLIANCE_DIR}': {missing}."
    )
    assert not extra, (
        f"The following unexpected files or directories are present in '{COMPLIANCE_DIR}': {extra}.\n"
        "Only 'audit_env' and 'audit_env_creation.log' should exist after completion."
    )

def test_permissions_on_compliance_dir_and_contents():
    # Check write permission for compliance dir
    assert os.access(COMPLIANCE_DIR, os.W_OK), (
        f"Directory '{COMPLIANCE_DIR}' is not writable by the user."
    )
    # Check write permissions for all contents
    for item in os.listdir(COMPLIANCE_DIR):
        item_path = os.path.join(COMPLIANCE_DIR, item)
        assert os.access(item_path, os.W_OK), (
            f"'{item_path}' is not writable by the user."
        )