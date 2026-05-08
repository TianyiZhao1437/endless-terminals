# test_initial_state.py

import os
import pytest

PROJECT_DIR = "/home/user/projects/support_app"
VENV_DIR = os.path.join(PROJECT_DIR, "env_support")
LOG_FILE = os.path.join(PROJECT_DIR, "venv_setup.log")


def test_project_directory_exists_and_writable():
    assert os.path.isdir(PROJECT_DIR), (
        f"Required project directory '{PROJECT_DIR}' is missing. "
        "Please ensure the directory exists before proceeding."
    )
    assert os.access(PROJECT_DIR, os.W_OK), (
        f"Project directory '{PROJECT_DIR}' is not writable. "
        "Ensure you have write permissions to this directory."
    )


def test_env_support_directory_does_not_exist():
    assert not os.path.exists(VENV_DIR), (
        f"The virtual environment directory '{VENV_DIR}' already exists. "
        "The environment should not be present before you create it."
    )


def test_log_file_does_not_exist():
    assert not os.path.exists(LOG_FILE), (
        f"The log file '{LOG_FILE}' already exists. "
        "The log file should not be present before you generate it."
    )