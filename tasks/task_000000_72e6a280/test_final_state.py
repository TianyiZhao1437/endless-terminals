# test_final_state.py
import os
import pytest
from datetime import date

NETWORK_UTILS_DIR = "/home/user/network_utils"
VERSION_FILE = os.path.join(NETWORK_UTILS_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(NETWORK_UTILS_DIR, "CHANGELOG.md")

def test_version_file_bumped():
    """Check that VERSION file contains '1.2.4' (patch bump from 1.2.3)."""
    assert os.path.isfile(VERSION_FILE), (
        f"Missing VERSION file after patch: {VERSION_FILE}"
    )
    with open(VERSION_FILE, "r") as f:
        version = f.read().strip()
    assert version == "1.2.4", (
        f"{VERSION_FILE} must contain version '1.2.4' after patch bump.\n"
        f"Actual contents: '{version}'"
    )

def test_changelog_new_entry_and_preserved_history():
    """Check that CHANGELOG.md has the new entry prepended with today's date and previous content preserved."""
    assert os.path.isfile(CHANGELOG_FILE), f"Missing changelog file: {CHANGELOG_FILE}"
    with open(CHANGELOG_FILE, "r") as f:
        lines = f.readlines()

    # The new entry must be at the very top
    today = date.today().isoformat()  # YYYY-MM-DD
    expected_new_entry = [
        f"## [1.2.4] - {today}\n",
        "### Fixed\n",
        "- Fixed bug in gateway connectivity check.\n",
        "\n"
    ]

    # Must be at least as long as the new entry plus previous content
    assert len(lines) >= len(expected_new_entry) + 6, (
        f"{CHANGELOG_FILE} is unexpectedly short after adding new entry."
    )

    # Check that the new entry is exactly at the top
    for idx, expected_line in enumerate(expected_new_entry):
        assert lines[idx] == expected_line, (
            f"CHANGELOG.md entry line {idx+1} incorrect.\n"
            f"Expected: {repr(expected_line)}\nActual:   {repr(lines[idx])}\n"
            f"Your changelog is missing the correct new entry in the exact format at the top."
        )

    # Now check that the rest of the file is the previous content, unaltered (from the truth data)
    expected_prev = [
        "## [1.2.3] - 2024-04-09\n",
        "### Fixed\n",
        "- Handle unreachable hosts error.\n",
        "\n",
        "## [1.2.2] - 2024-02-27\n",
        "### Added\n",
        "- Verbose mode for debug output.\n"
    ]
    # The previous content must follow immediately after the new entry
    prev_start = len(expected_new_entry)
    for idx, expected_line in enumerate(expected_prev):
        actual_idx = prev_start + idx
        assert lines[actual_idx] == expected_line, (
            f"CHANGELOG.md history was not preserved correctly starting at line {actual_idx+1}.\n"
            f"Expected: {repr(expected_line)}\nActual:   {repr(lines[actual_idx])}"
        )

def test_changelog_tail_matches_expected():
    """Check that the last 6 lines of CHANGELOG.md match the truth (as would be shown by tail -n 6)."""
    assert os.path.isfile(CHANGELOG_FILE), f"Missing changelog file: {CHANGELOG_FILE}"
    with open(CHANGELOG_FILE, "r") as f:
        all_lines = f.readlines()

    # Get last 6 lines
    tail6 = all_lines[-6:]
    expected_tail = [
        "## [1.2.3] - 2024-04-09\n",
        "### Fixed\n",
        "- Handle unreachable hosts error.\n",
        "\n",
        "## [1.2.2] - 2024-02-27\n"
    ]
    assert tail6 == expected_tail, (
        "The last 6 lines of CHANGELOG.md do not match the expected prior entries.\n"
        "This suggests the changelog history was altered or entry was not prepended correctly.\n"
        f"Expected last 6 lines:\n{''.join(expected_tail)}\n"
        f"Actual last 6 lines:\n{''.join(tail6)}"
    )