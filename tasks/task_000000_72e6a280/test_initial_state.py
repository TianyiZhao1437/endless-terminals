# test_initial_state.py
import os
import pytest

NETWORK_UTILS_DIR = "/home/user/network_utils"
NETWORK_CHECK_SH = os.path.join(NETWORK_UTILS_DIR, "network_check.sh")
VERSION_FILE = os.path.join(NETWORK_UTILS_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(NETWORK_UTILS_DIR, "CHANGELOG.md")

def test_network_utils_directory_exists():
    assert os.path.isdir(NETWORK_UTILS_DIR), (
        f"Missing required directory: {NETWORK_UTILS_DIR}"
    )

def test_network_check_sh_exists_and_contents():
    assert os.path.isfile(NETWORK_CHECK_SH), (
        f"Missing required script: {NETWORK_CHECK_SH}"
    )
    with open(NETWORK_CHECK_SH, "r") as f:
        contents = f.read().strip()
    expected = "#!/bin/bash\nping -c 4 8.8.8.8"
    assert contents == expected, (
        f"{NETWORK_CHECK_SH} does not have the expected contents.\n"
        f"Expected:\n{expected}\nActual:\n{contents}"
    )

def test_version_file_exists_and_value():
    assert os.path.isfile(VERSION_FILE), (
        f"Missing required VERSION file: {VERSION_FILE}"
    )
    with open(VERSION_FILE, "r") as f:
        version = f.read().strip()
    assert version == "1.2.3", (
        f"{VERSION_FILE} should contain version '1.2.3' before the patch bump.\n"
        f"Actual contents: '{version}'"
    )

def test_changelog_file_exists_and_initial_content():
    assert os.path.isfile(CHANGELOG_FILE), (
        f"Missing required changelog file: {CHANGELOG_FILE}"
    )
    with open(CHANGELOG_FILE, "r") as f:
        contents = f.read().strip()
    expected = (
        "## [1.2.3] - 2024-04-09\n"
        "### Fixed\n"
        "- Handle unreachable hosts error.\n\n"
        "## [1.2.2] - 2024-02-27\n"
        "### Added\n"
        "- Verbose mode for debug output."
    )
    assert contents == expected, (
        f"{CHANGELOG_FILE} does not have the expected initial contents.\n"
        f"Expected:\n{expected}\nActual:\n{contents}"
    )