# test_final_state.py

import pytest
import os

OPERATOR_DIR = "/home/user/operator"
VERSION_FILE = os.path.join(OPERATOR_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(OPERATOR_DIR, "CHANGELOG.md")
LOG_FILE = os.path.join(OPERATOR_DIR, "version_bump.log")

EXPECTED_VERSION = "1.2.4"

EXPECTED_CHANGELOG = (
    "## [1.2.4] - 2023-08-18\n\n"
    "* Bumped patch version for bugfix\n\n"
    "## [1.2.3] - 2023-08-10\n\n"
    "* Fixed deployment timeout issue\n\n"
    "## [1.2.2] - 2023-07-15\n\n"
    "* Improved reconciliation logic"
)

EXPECTED_LOG_LINE = "VERSION bumped to 1.2.4 and changelog updated."

def normalize(text):
    """Strip trailing spaces on each line and unify line endings."""
    return "\n".join(line.rstrip() for line in text.strip().splitlines())

def test_operator_directory_still_exists():
    assert os.path.isdir(OPERATOR_DIR), (
        f"Directory '{OPERATOR_DIR}' is missing after task completion. "
        "It must exist."
    )

def test_version_file_final_state():
    assert os.path.isfile(VERSION_FILE), (
        f"VERSION file '{VERSION_FILE}' does not exist after task. "
        "It must be present."
    )
    with open(VERSION_FILE, "r") as f:
        content = f.read().strip()
    assert content == EXPECTED_VERSION, (
        f"VERSION file should contain '{EXPECTED_VERSION}' after the patch bump, "
        f"but found '{content}'."
    )
    # Ensure there is nothing but the version string
    lines = content.splitlines()
    assert len(lines) == 1, (
        f"VERSION file should contain only the version string '{EXPECTED_VERSION}', "
        f"but found multiple lines."
    )

def test_changelog_file_final_state():
    assert os.path.isfile(CHANGELOG_FILE), (
        f"CHANGELOG.md file '{CHANGELOG_FILE}' does not exist after task. "
        "It must be present."
    )
    with open(CHANGELOG_FILE, "r") as f:
        content = f.read()
    norm_content = normalize(content)
    norm_expected = normalize(EXPECTED_CHANGELOG)
    assert norm_content == norm_expected, (
        "CHANGELOG.md does not match the required final content after the version bump.\n"
        "---- Expected ----\n"
        f"{EXPECTED_CHANGELOG}\n"
        "---- Found ----\n"
        f"{content}\n"
        "Please ensure the new entry is added EXACTLY as specified, above all existing entries."
    )
    # Additionally, check the new entry is truly at the very top
    first_line = content.lstrip().splitlines()[0]
    assert first_line == "## [1.2.4] - 2023-08-18", (
        "The new changelog entry must be the very first section at the top of CHANGELOG.md."
    )
    # Ensure the bullet is present and correctly formatted right after the new header
    lines = content.lstrip().splitlines()
    assert len(lines) > 2 and lines[2].strip() == "* Bumped patch version for bugfix", (
        "The bullet point for the new version must be exactly as specified and follow the header."
    )

def test_log_file_created_and_correct():
    assert os.path.isfile(LOG_FILE), (
        f"Log file '{LOG_FILE}' was not created after the task. "
        "It must exist."
    )
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    lines = [line.rstrip("\r\n") for line in lines]
    assert len(lines) == 1, (
        f"Log file '{LOG_FILE}' must contain exactly one line, "
        f"but found {len(lines)} lines."
    )
    assert lines[0] == EXPECTED_LOG_LINE, (
        f"Log file '{LOG_FILE}' has incorrect content.\n"
        f"Expected: '{EXPECTED_LOG_LINE}'\n"
        f"Found:    '{lines[0]}'\n"
        "Ensure the log message is exactly as specified."
    )