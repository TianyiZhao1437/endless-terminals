# test_initial_state.py

import os
import pytest

VERSION_FILE = "/home/user/version.txt"
CHANGELOG_FILE = "/home/user/CHANGELOG.md"
LOG_FILE = "/home/user/version_update.log"

def test_version_file_exists_and_content():
    """Check that /home/user/version.txt exists and contains '1.0.2'."""
    assert os.path.isfile(VERSION_FILE), (
        f"Missing file: {VERSION_FILE}. This file must exist before you start."
    )
    with open(VERSION_FILE, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1, (
        f"{VERSION_FILE} should contain exactly one line with the version number."
    )
    version = lines[0].strip()
    assert version == "1.0.2", (
        f"{VERSION_FILE} should contain '1.0.2' before you start, but found '{version}'."
    )

def test_changelog_exists_and_content():
    """Check that /home/user/CHANGELOG.md exists and contains the correct initial entry."""
    assert os.path.isfile(CHANGELOG_FILE), (
        f"Missing file: {CHANGELOG_FILE}. This file must exist before you start."
    )
    with open(CHANGELOG_FILE, "r") as f:
        content = f.read().strip()
    expected = (
        "## 1.0.2 - 2024-05-31\n\n"
        "- Improved username validation in user_manager.py"
    )
    assert content == expected, (
        f"{CHANGELOG_FILE} does not match the expected initial content.\n"
        f"Expected:\n{expected}\n\nFound:\n{content}"
    )

def test_log_file_does_not_exist():
    """Check that /home/user/version_update.log does not exist before the task."""
    assert not os.path.exists(LOG_FILE), (
        f"{LOG_FILE} should not exist before you start the task."
    )