# test_initial_state.py

import os
import pytest

HOME = "/home/user"
PROJECT_DIR = os.path.join(HOME, "weather_app")
SRC_DIR = os.path.join(PROJECT_DIR, "src")
TESTS_DIR = os.path.join(PROJECT_DIR, "tests")
LOG_FILE = os.path.join(PROJECT_DIR, "project_structure.log")


def test_weather_app_directory_does_not_exist():
    """weather_app directory must NOT exist before the task starts."""
    assert not os.path.exists(PROJECT_DIR), (
        f"Directory {PROJECT_DIR} should NOT exist before starting the task. "
        "Please remove it before proceeding."
    )


def test_home_directory_is_writable():
    """Agent must have write permission to /home/user."""
    assert os.access(HOME, os.W_OK), (
        f"Cannot write to {HOME}. Please ensure write permissions are set."
    )