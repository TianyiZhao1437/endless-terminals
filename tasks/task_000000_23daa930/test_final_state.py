# test_final_state.py

import os
import pytest

BUILD_CONFIG_PATH = "/home/user/build_config.ini"
PROD_BUILD_LOG_PATH = "/home/user/prod_build_version.log"
EXPECTED_PROD_BUILD_VERSION = "4.2.5"
EXPECTED_LOG_CONTENT = EXPECTED_PROD_BUILD_VERSION + "\n"

@pytest.mark.describe("Final OS/filesystem state after mobile build engineer task")
class TestFinalState:

    def test_prod_build_version_log_exists(self):
        assert os.path.isfile(PROD_BUILD_LOG_PATH), (
            f"The output log file {PROD_BUILD_LOG_PATH} does not exist. "
            "You must create this log file after extracting the production build version."
        )

    def test_prod_build_version_log_content_exact(self):
        """
        The log file must contain ONLY the production build_version value, and a single newline.
        """
        try:
            with open(PROD_BUILD_LOG_PATH, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            pytest.fail(
                f"Could not read {PROD_BUILD_LOG_PATH}: {e}"
            )

        if content != EXPECTED_LOG_CONTENT:
            # Give a helpful diff for common mistakes
            lines = content.splitlines(keepends=True)
            expected_lines = EXPECTED_LOG_CONTENT.splitlines(keepends=True)
            msg = (
                f"{PROD_BUILD_LOG_PATH} has incorrect content.\n"
                f"Expected exactly: {repr(EXPECTED_LOG_CONTENT)}\n"
                f"Found: {repr(content)}\n"
            )
            # Check common errors
            if not content:
                msg += "The file is empty. Did you forget to write the version value?\n"
            elif content.strip() != EXPECTED_PROD_BUILD_VERSION:
                msg += (
                    f"The file does not contain the correct version value. "
                    f"Expected '{EXPECTED_PROD_BUILD_VERSION}' on the first line.\n"
                )
            elif content != content.strip() + "\n":
                msg += (
                    "There is extra whitespace before or after the version value. "
                    "It must be exactly the version, then a single newline.\n"
                )
            elif len(lines) > 1 and any(l.strip() for l in lines[1:]):
                msg += "There are extra lines after the version value. Only a single line is allowed.\n"
            else:
                msg += "Double-check for any invisible characters or extra whitespace.\n"
            pytest.fail(msg)

    def test_prod_build_version_log_no_extra_content(self):
        """
        The log file should NOT contain any section headers, labels, or extra lines.
        """
        with open(PROD_BUILD_LOG_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

        assert len(lines) == 1, (
            f"{PROD_BUILD_LOG_PATH} should contain only a single line with the version value.\n"
            f"Actual lines: {lines}"
        )
        assert lines[0] == EXPECTED_LOG_CONTENT, (
            f"The only line in {PROD_BUILD_LOG_PATH} is incorrect.\n"
            f"Expected: {repr(EXPECTED_LOG_CONTENT)}\n"
            f"Found: {repr(lines[0])}\n"
            "There should be no extra whitespace, labels, or headers."
        )

    def test_prod_build_version_matches_config_file(self):
        """
        Asserts that the version in the log file matches the build_version under [production] in the config file.
        """
        # Parse the INI manually (no configparser allowed)
        current_section = None
        prod_version = None
        try:
            with open(BUILD_CONFIG_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith("[") and stripped.endswith("]"):
                        current_section = stripped[1:-1].strip().lower()
                    elif "=" in stripped and current_section == "production":
                        key, _, value = stripped.partition("=")
                        if key.strip() == "build_version":
                            prod_version = value.strip()
                            break
        except Exception as e:
            pytest.fail(f"Could not read {BUILD_CONFIG_PATH}: {e}")

        assert prod_version is not None, (
            f"Could not find 'build_version' under [production] in {BUILD_CONFIG_PATH}. "
            "Ensure the section and key exist."
        )

        with open(PROD_BUILD_LOG_PATH, "r", encoding="utf-8") as f:
            log_value = f.read().rstrip("\n")

        assert log_value == prod_version, (
            f"The version in {PROD_BUILD_LOG_PATH} ('{log_value}') does not match the "
            f"build_version in [production] of {BUILD_CONFIG_PATH} ('{prod_version}')."
        )