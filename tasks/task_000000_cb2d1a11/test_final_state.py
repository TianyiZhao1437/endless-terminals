# test_final_state.py
import os
import pytest

PROJECT_DIR = "/home/user/iot-data-collector"
VERSION_FILE = os.path.join(PROJECT_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(PROJECT_DIR, "CHANGELOG.md")

@pytest.mark.describe("Final IoT Data Collector project directory state after version bump and changelog update")
class TestFinalState:
    def test_project_directory_exists(self):
        assert os.path.isdir(PROJECT_DIR), (
            f"Required directory '{PROJECT_DIR}' does not exist. "
            "The project directory must still exist after the update."
        )

    def test_version_file_exists(self):
        assert os.path.isfile(VERSION_FILE), (
            f"Required file '{VERSION_FILE}' does not exist. "
            "The VERSION file must exist after the update."
        )

    def test_version_file_contents(self):
        with open(VERSION_FILE, "r") as f:
            contents = f.read().strip()
        assert contents == "1.3.0", (
            f"VERSION file at '{VERSION_FILE}' must contain '1.3.0' after the update (found '{contents}'). "
            "The version was not properly bumped to the next minor version."
        )

    def test_changelog_file_exists(self):
        assert os.path.isfile(CHANGELOG_FILE), (
            f"Required file '{CHANGELOG_FILE}' does not exist. "
            "The CHANGELOG.md file must still exist after the update."
        )

    def test_changelog_new_entry_and_format(self):
        """
        Validates that:
        - The new entry is present at the very top,
        - The entry uses the correct version and today's date,
        - The entry text is exactly as specified,
        - There is a blank line between entries,
        - The previous entries are preserved and not altered.
        """
        expected = [
            "## [1.3.0] - 2024-06-10",
            "",
            "- Added new data aggregation endpoint for edge nodes.",
            "",
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
        # Only check the first 11 lines (all truth lines in this changelog)
        actual = lines[:len(expected)]
        assert actual == expected, (
            "CHANGELOG.md does not contain the expected entries and format after the update.\n"
            "Expected first lines:\n"
            + "\n".join(expected)
            + "\nFound:\n"
            + "\n".join(actual)
            + "\n\n"
            "Check that:\n"
            "- The new entry is at the top, with the correct version and date.\n"
            "- The entry text is exactly: '- Added new data aggregation endpoint for edge nodes.'\n"
            "- There is a single blank line between entries.\n"
            "- Older entries are preserved and NOT changed."
        )

    def test_changelog_first_7_lines_output(self):
        """
        Validates that the first 7 lines of the changelog are exactly as expected,
        as would be printed for release review.
        """
        expected = [
            "## [1.3.0] - 2024-06-10",
            "",
            "- Added new data aggregation endpoint for edge nodes.",
            "",
            "## [1.2.3] - 2024-05-10",
            "",
            "- Fixed bug in sensor data parser.",
        ]
        with open(CHANGELOG_FILE, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]
        actual = lines[:7]
        assert actual == expected, (
            "The first 7 lines of CHANGELOG.md are not as expected for release review.\n"
            "Expected:\n"
            + "\n".join(expected)
            + "\nFound:\n"
            + "\n".join(actual)
            + "\n"
            "Check that the top of the changelog matches the correct new entry and previous entry."
        )