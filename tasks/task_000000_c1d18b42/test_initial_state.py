# test_initial_state.py

import os
import pytest

HOME = "/home/user"
VENV_DIR = os.path.join(HOME, "logenv")
VENV_ACTIVATE = os.path.join(VENV_DIR, "bin", "activate")
LOG_FILE = os.path.join(VENV_DIR, "setup_log.txt")

def test_logenv_directory_does_not_exist():
    assert not os.path.isdir(VENV_DIR), (
        f"The directory '{VENV_DIR}' already exists.\n"
        "Please ensure you have NOT yet created the virtual environment."
    )

def test_activate_script_does_not_exist():
    assert not os.path.isfile(VENV_ACTIVATE), (
        f"The virtual environment activate script '{VENV_ACTIVATE}' already exists.\n"
        "Please ensure the virtual environment has NOT been created yet."
    )

def test_setup_log_file_does_not_exist():
    assert not os.path.isfile(LOG_FILE), (
        f"The log file '{LOG_FILE}' already exists.\n"
        "Please ensure you have NOT yet created or written the log file."
    )