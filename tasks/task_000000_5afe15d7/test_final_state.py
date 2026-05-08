# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/config-app"
VERSION_FILE = os.path.join(PROJECT_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(PROJECT_DIR, "CHANGELOG.md")

EXPECTED_VERSION = "1.5.0"

EXPECTED_CHANGELOG = (
    "## [1.5.0] - 2024-06-20\n"
    "\n"
    "### Added\n"
    "- New option <code>max_retries</code> in <code>config.yml</code> (default: 5)\n"
    "\n"
    "### Changed\n"
    "- Updated default log level to <code>INFO</code> in <code>config.yml</code>\n"
    "\n"
    "### Fixed\n"
    "- Resolved error with invalid port number in <code>service_manager.py</code>\n"
    "\n"
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


def test_project_directory_still_exists_and_writeable():
    assert os.path.isdir(PROJECT_DIR), (
        f"Project directory missing: {PROJECT_DIR}"
    )
    if not os.access(PROJECT_DIR, os.W_OK):
        perms = oct(os.stat(PROJECT_DIR).st_mode)[-3:]
        raise AssertionError(
            f"Project directory {PROJECT_DIR} exists but is not writeable (permissions: {perms})"
        )

def test_version_file_updated_and_correct():
    assert os.path.isfile(VERSION_FILE), (
        f"VERSION file missing: {VERSION_FILE}"
    )
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        data = f.read()
    # Must match *exactly* (no trailing newline, no spaces)
    assert data == EXPECTED_VERSION, (
        f"{VERSION_FILE} does not contain the correct version after the bump.\n"
        f"Expected exactly: {repr(EXPECTED_VERSION)}\n"
        f"Got:            {repr(data)}\n"
        f"Check for extra spaces, newlines, or incorrect version."
    )

def test_changelog_file_updated_and_correct():
    assert os.path.isfile(CHANGELOG_FILE), (
        f"CHANGELOG file missing: {CHANGELOG_FILE}"
    )
    with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
        data = f.read()
    assert data == EXPECTED_CHANGELOG, (
        f"{CHANGELOG_FILE} does not match the expected final content after update.\n\n"
        f"Expected:\n{repr(EXPECTED_CHANGELOG)}\n\n"
        f"Got:\n{repr(data)}\n"
        f"Check for:\n"
        f"- Missing or extra blank lines\n"
        f"- Incorrect or missing heading/date/version\n"
        f"- Formatting of bullet points or code blocks\n"
        f"- Previous entries being changed or removed\n"
    )

def test_version_and_changelog_printed_to_console(capsys):
    """
    This test simulates the verification step: print contents of VERSION and CHANGELOG.md to stdout.
    """
    # Print VERSION
    with open(VERSION_FILE, "r", encoding="utf-8") as f:
        version_content = f.read()
    print(version_content)

    # Print CHANGELOG.md
    with open(CHANGELOG_FILE, "r", encoding="utf-8") as f:
        changelog_content = f.read()
    print(changelog_content)

    # Capture output and check that both are present and correct
    captured = capsys.readouterr()
    output = captured.out

    # The output should contain the version string and the changelog, each as printed
    expected_output = f"{EXPECTED_VERSION}\n{EXPECTED_CHANGELOG}\n"
    assert output == expected_output, (
        "Printed output of VERSION and CHANGELOG.md does not match expected.\n"
        "Expected output (VERSION followed by CHANGELOG.md):\n"
        f"{repr(expected_output)}\n"
        "Actual:\n"
        f"{repr(output)}"
    )