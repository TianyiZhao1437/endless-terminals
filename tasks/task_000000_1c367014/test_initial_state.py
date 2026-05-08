# test_initial_state.py

import os
import pytest

INI_PATH = "/home/user/project/config/settings.ini"

EXPECTED_INI = """[General]
app_name = ExampleApp
version = 1.0.0
maintainer = Alice Smith

[Features]
feature_x_enabled = true
color_scheme = dark
autosave = yes
"""

@pytest.mark.parametrize("path", [
    INI_PATH,
])
def test_ini_file_exists(path):
    assert os.path.isfile(path), (
        f"Missing required INI file: {path}\n"
        "Please ensure the file exists before proceeding."
    )

def test_ini_file_contents():
    assert os.path.isfile(INI_PATH), (
        f"Missing required INI file: {INI_PATH}\n"
        "Please ensure the file exists before proceeding."
    )
    with open(INI_PATH, "r", encoding="utf-8") as f:
        actual_contents = f.read()
    # Normalize line endings and strip trailing whitespace for comparison
    expected = EXPECTED_INI.strip().replace('\r\n', '\n')
    actual = actual_contents.strip().replace('\r\n', '\n')
    assert actual == expected, (
        f"The INI file at {INI_PATH} does not match the expected initial contents.\n"
        f"Expected contents:\n{EXPECTED_INI}\n"
        f"Actual contents:\n{actual_contents}\n"
        "Please ensure the INI file contains the correct sections and key-value pairs."
    )

@pytest.mark.parametrize("directory", [
    "/home/user/project/config",
    "/home/user/project/docs",
])
def test_required_directories_exist(directory):
    assert os.path.isdir(directory), (
        f"Missing required directory: {directory}\n"
        "Please ensure the directory exists before proceeding."
    )

@pytest.mark.parametrize("directory", [
    "/home/user/project/docs",
])
def test_docs_directory_writeable(directory):
    assert os.access(directory, os.W_OK), (
        f"The directory {directory} is not writeable.\n"
        "Please ensure write permissions are set so the agent can create the summary file."
    )