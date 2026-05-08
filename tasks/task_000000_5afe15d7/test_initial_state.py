# test_initial_state.py

import os
import stat
import pytest

PROJECT_DIR = "/home/user/config-app"
VERSION_FILE = os.path.join(PROJECT_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(PROJECT_DIR, "CHANGELOG.md")


def test_project_directory_exists_and_writeable():
    assert os.path.isdir(PROJECT_DIR), (
        f"Required directory does not exist: {PROJECT_DIR}"
    )
    # Test that user can write to the directory
    if not os.access(PROJECT_DIR, os.W_OK):
        st = os.stat(PROJECT_DIR)
        perms = oct(st.st_mode)[-3:]
        raise AssertionError(
            f"Directory {PROJECT_DIR} exists but is not writeable by the user "
            f"(permissions: {perms})"
        )


def test_version_file_exists_and_content():
    assert os.path.isfile(VERSION_FILE), (
        f"Required file does not exist: {VERSION_FILE}"
    )
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        data = f.read()
    # Check for exact content: '1.4.2' and nothing else (no extra newlines or spaces)
    assert data == "1.4.2", (
        f"{VERSION_FILE} must contain exactly '1.4.2' (no extra spaces or newlines), "
        f"but got: {repr(data)}"
    )


def test_changelog_file_exists_and_content():
    assert os.path.isfile(CHANGELOG_FILE), (
        f"Required file does not exist: {CHANGELOG_FILE}"
    )
    with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
        data = f.read()

    expected = (
        "## [1.4.2] - 2024-06-10\n"
        "\n"
        "### Fixed\n"
        "- Patched vulnerability in YAML parser\n"
        "\n"
        "## [1.4.0] - 2024-05-28\n"
        "\n"
        "### Added\n"
        "- Command-line argument <code>--safe-mode</code>\n"
    )

    # The file must match exactly, including blank lines and spacing
    assert data == expected, (
        f"{CHANGELOG_FILE} does not match the expected initial content.\n\n"
        f"Expected:\n{repr(expected)}\n\n"
        f"Got:\n{repr(data)}"
    )