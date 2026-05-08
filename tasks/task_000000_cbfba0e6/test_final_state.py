# test_final_state.py

import os
import pytest

VERSION_FILE = "/home/user/version.txt"
CHANGELOG_FILE = "/home/user/CHANGELOG.md"
LOG_FILE = "/home/user/version_update.log"

EXPECTED_VERSION = "1.0.3"
TODAYS_DATE = "2024-06-05"

EXPECTED_CHANGELOG = (
    "## 1.0.2 - 2024-05-31\n\n"
    "- Improved username validation in user_manager.py\n\n"
    f"## {EXPECTED_VERSION} - {TODAYS_DATE}\n\n"
    "- Fixed bug with user ID handling in user_manager.py"
)

EXPECTED_LOG_LINE = f"Version bumped to {EXPECTED_VERSION} on {TODAYS_DATE}"

def test_version_file_exists_and_correct_content():
    """Check that /home/user/version.txt exists and contains the new version only."""
    assert os.path.isfile(VERSION_FILE), (
        f"Missing file: {VERSION_FILE}. This file must exist after the task is completed."
    )
    with open(VERSION_FILE, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1, (
        f"{VERSION_FILE} should contain exactly one line with the version number, "
        f"but found {len(lines)} lines."
    )
    version = lines[0].strip()
    assert version == EXPECTED_VERSION, (
        f"{VERSION_FILE} should contain '{EXPECTED_VERSION}' after the version bump, "
        f"but found '{version}'."
    )

def test_changelog_file_exists_and_last_entry_format():
    """Check that /home/user/CHANGELOG.md exists and ends with the correct new entry."""
    assert os.path.isfile(CHANGELOG_FILE), (
        f"Missing file: {CHANGELOG_FILE}. This file must exist after the task is completed."
    )
    with open(CHANGELOG_FILE, "r") as f:
        content = f.read().strip()
    # Check full file content matches expected (including blank lines and formatting)
    if content != EXPECTED_CHANGELOG:
        # Find where it differs for easier debugging
        from difflib import unified_diff
        diff = "\n".join(unified_diff(EXPECTED_CHANGELOG.splitlines(), content.splitlines(), fromfile="expected", tofile="found", lineterm=""))
        pytest.fail(
            f"{CHANGELOG_FILE} does not match the expected final content.\n"
            f"Diff:\n{diff}\n"
            f"Expected:\n{EXPECTED_CHANGELOG}\n\nFound:\n{content}"
        )

def test_log_file_exists_and_correct_content():
    """Check that /home/user/version_update.log exists and contains the correct summary line."""
    assert os.path.isfile(LOG_FILE), (
        f"Missing file: {LOG_FILE}. This file must exist after the task is completed."
    )
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    assert len(lines) == 1, (
        f"{LOG_FILE} should contain exactly one line, but found {len(lines)} lines."
    )
    log_line = lines[0].strip()
    assert log_line == EXPECTED_LOG_LINE, (
        f"{LOG_FILE} should contain exactly:\n'{EXPECTED_LOG_LINE}'\nbut found:\n'{log_line}'"
    )