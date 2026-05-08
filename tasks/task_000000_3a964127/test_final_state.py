# test_final_state.py

import os
import pytest

GRAFANA_DIR = "/home/user/grafana-dashboard"
VERSION_PATH = os.path.join(GRAFANA_DIR, "VERSION")
CHANGELOG_PATH = os.path.join(GRAFANA_DIR, "CHANGELOG.md")

# The expected final values after task completion.
EXPECTED_VERSION = "1.3.3"
EXPECTED_CHANGELOG_TOP = [
    "## [1.3.3] - 2024-06-25",
    "- Tuned dashboard query for improved latency",
    "",
    "## [1.3.2] - 2024-05-14",
    "- Added new thresholds for alerting",
    "",
    "## [1.3.1] - 2024-05-07",
    "- Integrated dashboard with Prometheus",
    "",
    "## [1.3.0] - 2024-05-01",
    "- Initial dashboard setup"
]

@pytest.mark.describe("Final Grafana dashboard project state after update")
def test_grafana_dashboard_directory_still_exists():
    assert os.path.isdir(GRAFANA_DIR), (
        f"Directory missing after task: {GRAFANA_DIR}. "
        "The project directory must not be removed."
    )

def test_version_file_exists():
    assert os.path.isfile(VERSION_PATH), (
        f"Missing file after task: {VERSION_PATH}. "
        "VERSION file must exist after version bump."
    )

def test_version_file_final_contents():
    with open(VERSION_PATH, "r", encoding="utf-8") as f:
        contents = f.read().strip()
    assert contents == EXPECTED_VERSION, (
        f"VERSION file does not contain expected version '{EXPECTED_VERSION}'. "
        f"Actual contents: '{contents}'. "
        "Did you correctly increment the PATCH version?"
    )

def test_changelog_file_exists():
    assert os.path.isfile(CHANGELOG_PATH), (
        f"Missing file after task: {CHANGELOG_PATH}. "
        "CHANGELOG.md must exist after prepending new entry."
    )

def test_changelog_file_final_contents():
    with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    # Remove any leading/trailing blank lines
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()

    # Check the changelog starts with the expected top entry and previous entries
    expected_lines = EXPECTED_CHANGELOG_TOP
    actual_top = lines[:len(expected_lines)]

    assert actual_top == expected_lines, (
        "CHANGELOG.md does not start with the expected new entry and previous entries.\n"
        "Expected:\n"
        + "\n".join(expected_lines)
        + "\nActual:\n"
        + "\n".join(actual_top)
        + "\n\nDid you prepend the new entry in the correct format with the correct date, version, and description?"
    )

    # Additional check: The first two lines are exactly as specified for automated verification.
    assert lines[0] == "## [1.3.3] - 2024-06-25", (
        f"First line of CHANGELOG.md should be '## [1.3.3] - 2024-06-25', but found: '{lines[0]}'. "
        "Check version, date, and formatting."
    )
    assert lines[1] == "- Tuned dashboard query for improved latency", (
        f"Second line of CHANGELOG.md should be '- Tuned dashboard query for improved latency', but found: '{lines[1]}'. "
        "Check description and formatting."
    )