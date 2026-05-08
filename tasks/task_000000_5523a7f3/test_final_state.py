# test_final_state.py

import os
import pytest

VERSION_PATH = "/home/user/project/VERSION"
CHANGELOG_PATH = "/home/user/project/CHANGELOG.md"
VERSION_BUMP_LOG_PATH = "/home/user/project/version_bump.log"

def test_version_file_updated():
    """Check that VERSION file exists and contains exactly '2.3.5'."""
    assert os.path.isfile(VERSION_PATH), (
        f"VERSION file is missing at {VERSION_PATH}.\n"
        f"Expected a file containing the new version."
    )
    with open(VERSION_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content == "2.3.5", (
        f"VERSION file at {VERSION_PATH} should contain only '2.3.5' after the update.\n"
        f"Actual content: {repr(content)}"
    )

def test_changelog_file_updated():
    """Check that CHANGELOG.md exists and the new entry is at the very top with exact formatting."""
    assert os.path.isfile(CHANGELOG_PATH), (
        f"CHANGELOG.md file is missing at {CHANGELOG_PATH}.\n"
        f"Expected the file to document the new version entry."
    )
    expected_content = (
        "## [2.3.5] - 2024-06-10\n"
        "### Changed\n"
        "- Improved profiling result: reduced function load time by optimizing database query.\n"
        "\n"
        "## [2.3.4] - 2024-05-12\n"
        "### Fixed\n"
        "- Patched thread leak issue in data collector.\n"
    )
    with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == expected_content, (
        f"CHANGELOG.md at {CHANGELOG_PATH} does not have the correct content after the update.\n"
        f"--- Expected ---\n{expected_content!r}\n"
        f"--- Actual ---\n{content!r}\n"
        "Make sure the new entry for 2.3.5 is at the very top, with an empty line before the previous entry, "
        "and the formatting matches exactly."
    )

def test_version_bump_log_created_and_correct():
    """Check that version_bump.log exists and contains exactly the two required lines."""
    assert os.path.isfile(VERSION_BUMP_LOG_PATH), (
        f"version_bump.log is missing at {VERSION_BUMP_LOG_PATH}.\n"
        f"Expected a log file documenting the version bump and changelog addition."
    )
    expected_lines = [
        "Updated VERSION from 2.3.4 to 2.3.5",
        "Added changelog entry for 2.3.5"
    ]
    with open(VERSION_BUMP_LOG_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
    assert lines == expected_lines, (
        f"version_bump.log at {VERSION_BUMP_LOG_PATH} does not contain the expected log entries.\n"
        f"--- Expected ---\n{expected_lines}\n"
        f"--- Actual ---\n{lines}\n"
        "The file must contain exactly these two lines, in order, and nothing else."
    )