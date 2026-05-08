# test_initial_state.py

import os
import pytest

PROJECT_DIR = "/home/user/myapp"
VERSION_FILE = os.path.join(PROJECT_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(PROJECT_DIR, "CHANGELOG.md")
RELEASE_LOG_FILE = os.path.join(PROJECT_DIR, "release.log")


def test_project_directory_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Required project directory '{PROJECT_DIR}' does not exist. "
        "Create it before proceeding."
    )


def test_version_file_exists():
    assert os.path.isfile(VERSION_FILE), (
        f"Required version file '{VERSION_FILE}' does not exist. "
        "Create it with the correct semantic version before proceeding."
    )


def test_version_file_content():
    with open(VERSION_FILE, "r") as f:
        content = f.read()
    assert content == "1.3.7\n", (
        f"'{VERSION_FILE}' must contain exactly '1.3.7' followed by a newline. "
        f"Found: {repr(content)}"
    )


def test_changelog_file_exists():
    assert os.path.isfile(CHANGELOG_FILE), (
        f"Required changelog file '{CHANGELOG_FILE}' does not exist. "
        "Create it with the correct content before proceeding."
    )


def test_changelog_file_content():
    expected = (
        "## [1.3.7] - 2024-06-17\n"
        "- Fixed issue with user authentication.\n"
        "- Improved documentation.\n"
    )
    with open(CHANGELOG_FILE, "r") as f:
        content = f.read()
    assert content == expected, (
        f"'{CHANGELOG_FILE}' must contain the initial changelog section for version 1.3.7 as follows:\n\n"
        f"{expected!r}\nBut found:\n{content!r}"
    )


def test_release_log_does_not_exist():
    assert not os.path.exists(RELEASE_LOG_FILE), (
        f"'{RELEASE_LOG_FILE}' should NOT exist before starting the task. "
        "It must be created by your deployment script."
    )