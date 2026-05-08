# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/myapp"
VERSION_FILE = os.path.join(PROJECT_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(PROJECT_DIR, "CHANGELOG.md")
RELEASE_LOG_FILE = os.path.join(PROJECT_DIR, "release.log")

EXPECTED_OLD_VERSION = "1.3.7"
EXPECTED_NEW_VERSION = "1.4.0"
EXPECTED_DATE = "2024-06-18"

EXPECTED_VERSION_FILE_CONTENT = EXPECTED_NEW_VERSION + "\n"

EXPECTED_CHANGELOG_CONTENT = (
    f"## [{EXPECTED_NEW_VERSION}] - {EXPECTED_DATE}\n"
    f"- Minor version bump for new deployment.\n"
    "\n"
    f"## [{EXPECTED_OLD_VERSION}] - 2024-06-17\n"
    "- Fixed issue with user authentication.\n"
    "- Improved documentation.\n"
)

EXPECTED_RELEASE_LOG_CONTENT = (
    f"Version bumped from {EXPECTED_OLD_VERSION} to {EXPECTED_NEW_VERSION}\n"
    f"Changelog updated on {EXPECTED_DATE}\n"
)

def test_project_directory_still_exists():
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory '{PROJECT_DIR}' is missing after task. "
        "It must exist."
    )

def test_version_file_exists():
    assert os.path.isfile(VERSION_FILE), (
        f"Version file '{VERSION_FILE}' is missing after task. "
        "It must exist."
    )

def test_version_file_content():
    with open(VERSION_FILE, "r") as f:
        content = f.read()
    assert content == EXPECTED_VERSION_FILE_CONTENT, (
        f"'{VERSION_FILE}' content is incorrect after version bump.\n"
        f"Expected: {EXPECTED_VERSION_FILE_CONTENT!r}\n"
        f"Found:    {content!r}\n"
        "The file must contain exactly the new version string, a single line ending with a newline."
    )

def test_changelog_file_exists():
    assert os.path.isfile(CHANGELOG_FILE), (
        f"Changelog file '{CHANGELOG_FILE}' is missing after task. "
        "It must exist."
    )

def test_changelog_file_content():
    with open(CHANGELOG_FILE, "r") as f:
        content = f.read()
    if content != EXPECTED_CHANGELOG_CONTENT:
        # Try to give a detailed diff
        import difflib
        diff = ''.join(difflib.unified_diff(
            EXPECTED_CHANGELOG_CONTENT.splitlines(keepends=True),
            content.splitlines(keepends=True),
            fromfile='expected',
            tofile='found'
        ))
        pytest.fail(
            f"'{CHANGELOG_FILE}' content is incorrect after update.\n"
            f"Difference between expected and found:\n{diff}\n"
            "The changelog must:\n"
            "- Start with the new version section in the specified format.\n"
            "- Contain the bullet point exactly as specified.\n"
            "- Have a single blank line between sections.\n"
            "- Preserve previous sections unmodified.\n"
        )

def test_release_log_file_exists():
    assert os.path.isfile(RELEASE_LOG_FILE), (
        f"Release log file '{RELEASE_LOG_FILE}' is missing after task. "
        "It must be created."
    )

def test_release_log_file_content():
    with open(RELEASE_LOG_FILE, "r") as f:
        content = f.read()
    assert content == EXPECTED_RELEASE_LOG_CONTENT, (
        f"'{RELEASE_LOG_FILE}' content is incorrect.\n"
        f"Expected: {EXPECTED_RELEASE_LOG_CONTENT!r}\n"
        f"Found:    {content!r}\n"
        "The release log must contain exactly two lines, in the specified format."
    )