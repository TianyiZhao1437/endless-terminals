# test_final_state.py

import os
import pytest

INI_PATH = "/home/user/project/config/settings.ini"
MD_PATH = "/home/user/project/docs/config_summary.md"

EXPECTED_MD = """# Configuration Summary

## [General]
- app_name: ExampleApp
- version: 1.0.0
- maintainer: Alice Smith

## [Features]
- feature_x_enabled: true
- color_scheme: dark
- autosave: yes
"""

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
    MD_PATH,
])
def test_summary_file_exists(path):
    assert os.path.isfile(path), (
        f"Missing expected summary markdown file: {path}\n"
        "The file must exist after completing the task."
    )

def test_summary_file_contents_exact():
    assert os.path.isfile(MD_PATH), (
        f"Missing expected summary markdown file: {MD_PATH}\n"
        "The file must exist after completing the task."
    )
    with open(MD_PATH, "r", encoding="utf-8") as f:
        actual_md = f.read()
    # Normalize line endings for comparison, but DO NOT strip whitespace for exactness
    expected = EXPECTED_MD.replace('\r\n', '\n')
    actual = actual_md.replace('\r\n', '\n')
    assert actual == expected, (
        f"The markdown summary at {MD_PATH} does not match the expected format and contents.\n"
        f"Expected contents:\n{EXPECTED_MD}\n"
        f"Actual contents:\n{actual_md}\n"
        "Check for missing, extra, or misordered keys, sections, or headings."
    )

def test_ini_file_unchanged():
    assert os.path.isfile(INI_PATH), (
        f"Missing INI file: {INI_PATH} (should not be deleted or moved).\n"
        "The original configuration file must remain unchanged."
    )
    with open(INI_PATH, "r", encoding="utf-8") as f:
        actual_ini = f.read()
    expected = EXPECTED_INI.strip().replace('\r\n', '\n')
    actual = actual_ini.strip().replace('\r\n', '\n')
    assert actual == expected, (
        f"The INI file at {INI_PATH} was modified.\n"
        f"Expected contents:\n{EXPECTED_INI}\n"
        f"Actual contents:\n{actual_ini}\n"
        "The agent must NOT alter the original configuration file."
    )

@pytest.mark.parametrize("directory", [
    "/home/user/project/config",
    "/home/user/project/docs",
])
def test_required_directories_still_exist(directory):
    assert os.path.isdir(directory), (
        f"Missing required directory after task completion: {directory}\n"
        "No directories should have been deleted or moved."
    )

@pytest.mark.parametrize("directory", [
    "/home/user/project/docs",
])
def test_docs_directory_still_writeable(directory):
    assert os.access(directory, os.W_OK), (
        f"The directory {directory} is no longer writeable after task completion.\n"
        "Write permissions must remain so documentation can be updated in the future."
    )