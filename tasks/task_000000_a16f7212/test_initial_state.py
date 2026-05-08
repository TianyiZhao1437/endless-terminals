# test_initial_state.py

import pytest
import os

OPERATOR_DIR = "/home/user/operator"
VERSION_FILE = os.path.join(OPERATOR_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(OPERATOR_DIR, "CHANGELOG.md")
LOG_FILE = os.path.join(OPERATOR_DIR, "version_bump.log")

@pytest.mark.parametrize("path", [OPERATOR_DIR])
def test_operator_directory_exists(path):
    assert os.path.isdir(path), (
        f"Required directory '{path}' does not exist. "
        "Please ensure the /home/user/operator directory is present before starting."
    )

def test_version_file_initial_state():
    assert os.path.isfile(VERSION_FILE), (
        f"Required VERSION file '{VERSION_FILE}' does not exist. "
        "Please ensure the VERSION file is present before starting."
    )
    with open(VERSION_FILE, "r") as f:
        content = f.read().strip()
    assert content == "1.2.3", (
        f"Initial VERSION file should contain '1.2.3', but found '{content}'. "
        "Please reset the VERSION file to its initial state."
    )

def test_changelog_file_initial_state():
    assert os.path.isfile(CHANGELOG_FILE), (
        f"Required CHANGELOG.md file '{CHANGELOG_FILE}' does not exist. "
        "Please ensure the CHANGELOG.md file is present before starting."
    )
    with open(CHANGELOG_FILE, "r") as f:
        content = f.read().strip()
    expected = (
        "## [1.2.3] - 2023-08-10\n\n"
        "* Fixed deployment timeout issue\n\n"
        "## [1.2.2] - 2023-07-15\n\n"
        "* Improved reconciliation logic"
    )
    # Normalize whitespace for comparison
    def normalize(text):
        return "\n".join(line.rstrip() for line in text.strip().splitlines())
    assert normalize(content) == normalize(expected), (
        f"Initial CHANGELOG.md content does not match expected.\n"
        f"Expected:\n{expected}\n\nFound:\n{content}\n"
        "Please reset the CHANGELOG.md file to its initial state."
    )

def test_log_file_absent_before_task():
    assert not os.path.exists(LOG_FILE), (
        f"The log file '{LOG_FILE}' should NOT exist before the task is performed. "
        "Please remove it if present."
    )