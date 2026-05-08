# test_initial_state.py

import os
import pytest

VERSION_PATH = "/home/user/project/VERSION"
CHANGELOG_PATH = "/home/user/project/CHANGELOG.md"
VERSION_BUMP_LOG_PATH = "/home/user/project/version_bump.log"

def test_version_file_exists_and_content():
    assert os.path.isfile(VERSION_PATH), (
        f"Missing VERSION file at {VERSION_PATH}.\n"
        f"Please ensure the file exists with the correct initial version."
    )
    with open(VERSION_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == "2.3.4", (
        f"VERSION file at {VERSION_PATH} should contain only '2.3.4' before starting the task.\n"
        f"Actual content: {repr(content)}"
    )

def test_changelog_file_exists_and_content():
    assert os.path.isfile(CHANGELOG_PATH), (
        f"Missing CHANGELOG.md file at {CHANGELOG_PATH}.\n"
        f"Please ensure the file exists with the correct initial changelog."
    )
    expected_content = (
        "## [2.3.4] - 2024-05-12\n"
        "### Fixed\n"
        "- Patched thread leak issue in data collector.\n"
    )
    with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == expected_content, (
        f"CHANGELOG.md at {CHANGELOG_PATH} does not have the expected initial content.\n"
        f"Expected:\n{repr(expected_content)}\n"
        f"Actual:\n{repr(content)}"
    )

def test_version_bump_log_does_not_exist():
    assert not os.path.exists(VERSION_BUMP_LOG_PATH), (
        f"The version bump log '{VERSION_BUMP_LOG_PATH}' should not exist before you start.\n"
        f"Please remove it if present."
    )