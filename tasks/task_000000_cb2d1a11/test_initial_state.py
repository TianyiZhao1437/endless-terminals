# test_initial_state.py

import os
import pytest

PROJECT_DIR = "/home/user/iot-data-collector"
VERSION_FILE = os.path.join(PROJECT_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(PROJECT_DIR, "CHANGELOG.md")

@pytest.mark.describe("Initial IoT Data Collector project directory state")
class TestInitialState:

    def test_project_directory_exists(self):
        assert os.path.isdir(PROJECT_DIR), (
            f"Required directory '{PROJECT_DIR}' does not exist. "
            "Please ensure the IoT project directory is present."
        )

    def test_version_file_exists(self):
        assert os.path.isfile(VERSION_FILE), (
            f"Required file '{VERSION_FILE}' does not exist. "
            "Please ensure the VERSION file is present in the project directory."
        )

    def test_version_file_contents(self):
        with open(VERSION_FILE, "r") as f:
            contents = f.read().strip()
        assert contents == "1.2.3", (
            f"VERSION file at '{VERSION_FILE}' must contain '1.2.3' (found '{contents}'). "
            "Ensure the correct version is present before updating."
        )

    def test_changelog_file_exists(self):
        assert os.path.isfile(CHANGELOG_FILE), (
            f"Required file '{CHANGELOG_FILE}' does not exist. "
            "Please ensure the CHANGELOG.md file is present in the project directory."
        )

    def test_changelog_initial_contents(self):
        expected = [
            "## [1.2.3] - 2024-05-10",
            "",
            "- Fixed bug in sensor data parser.",
            "",
            "## [1.2.2] - 2024-04-27",
            "",
            "- Improved MQTT reconnect strategy.",
        ]
        with open(CHANGELOG_FILE, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
        # Only check the first 7 lines (which are all the initial contents in this case)
        actual = lines[:7]
        assert actual == expected, (
            f"CHANGELOG.md does not contain the expected initial entries.\n"
            f"Expected first 7 lines:\n{expected}\n"
            f"Found:\n{actual}\n"
            "Please ensure the changelog is correct before updating."
        )