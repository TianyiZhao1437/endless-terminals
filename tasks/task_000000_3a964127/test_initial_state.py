# test_initial_state.py

import os
import pytest

GRAFANA_DIR = "/home/user/grafana-dashboard"
VERSION_PATH = os.path.join(GRAFANA_DIR, "VERSION")
CHANGELOG_PATH = os.path.join(GRAFANA_DIR, "CHANGELOG.md")

@pytest.mark.describe("Initial Grafana dashboard project state")
def test_grafana_dashboard_directory_exists():
    assert os.path.isdir(GRAFANA_DIR), (
        f"Missing directory: {GRAFANA_DIR}. "
        "The project directory must exist before you start."
    )

def test_version_file_exists():
    assert os.path.isfile(VERSION_PATH), (
        f"Missing file: {VERSION_PATH}. "
        "VERSION file is required before updating the version."
    )

def test_version_file_contents():
    with open(VERSION_PATH, "r", encoding="utf-8") as f:
        contents = f.read().strip()
    assert contents == "1.3.2", (
        f"VERSION file should contain '1.3.2' exactly, but found: '{contents}'. "
        "Do not update the version before starting."
    )

def test_changelog_file_exists():
    assert os.path.isfile(CHANGELOG_PATH), (
        f"Missing file: {CHANGELOG_PATH}. "
        "CHANGELOG.md must exist before you prepend a new entry."
    )

def test_changelog_file_initial_contents():
    expected = [
        "## [1.3.2] - 2024-05-14",
        "- Added new thresholds for alerting",
        "",
        "## [1.3.1] - 2024-05-07",
        "- Integrated dashboard with Prometheus",
        "",
        "## [1.3.0] - 2024-05-01",
        "- Initial dashboard setup"
    ]

    with open(CHANGELOG_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    # Remove any leading/trailing blank lines
    while lines and lines[0] == "":
        lines.pop(0)
    while lines and lines[-1] == "":
        lines.pop()

    # The file must start with the expected first 7 lines
    assert lines[:7] == expected[:7], (
        "CHANGELOG.md does not match expected initial contents.\n"
        "Expected first lines:\n"
        + "\n".join(expected[:7])
        + "\nActual first lines:\n"
        + "\n".join(lines[:7])
        + "\nDo not update the changelog before starting."
    )