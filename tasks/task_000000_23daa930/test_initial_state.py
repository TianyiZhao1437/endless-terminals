# test_initial_state.py

import os
import pytest

BUILD_CONFIG_PATH = "/home/user/build_config.ini"
PROD_BUILD_LOG_PATH = "/home/user/prod_build_version.log"

@pytest.mark.describe("Initial OS/filesystem state for mobile build engineer task")
class TestInitialState:

    def test_build_config_ini_exists(self):
        assert os.path.isfile(BUILD_CONFIG_PATH), (
            f"Missing required configuration file: {BUILD_CONFIG_PATH}. "
            "Ensure that the build_config.ini file exists at the specified path."
        )

    def test_prod_build_version_log_does_not_exist(self):
        assert not os.path.exists(PROD_BUILD_LOG_PATH), (
            f"The output log file {PROD_BUILD_LOG_PATH} should NOT exist before the task is performed."
        )

    def test_build_config_ini_has_required_sections_and_keys(self):
        """
        Validates that /home/user/build_config.ini contains both [development] and [production] sections,
        and that each has a build_version entry.
        """
        required_sections = {
            "development": False,
            "production": False,
        }
        build_versions = {
            "development": False,
            "production": False,
        }

        current_section = None
        try:
            with open(BUILD_CONFIG_PATH, "r") as f:
                for line in f:
                    stripped = line.strip()
                    if stripped.startswith("[") and stripped.endswith("]"):
                        section = stripped[1:-1].strip().lower()
                        if section in required_sections:
                            current_section = section
                            required_sections[section] = True
                        else:
                            current_section = None
                    elif "=" in stripped and current_section in build_versions:
                        key, _, value = stripped.partition("=")
                        if key.strip() == "build_version":
                            build_versions[current_section] = True
        except Exception as e:
            pytest.fail(f"Could not read {BUILD_CONFIG_PATH}: {e}")

        missing_sections = [s for s, found in required_sections.items() if not found]
        missing_build_versions = [s for s, found in build_versions.items() if not found]

        if missing_sections:
            pytest.fail(
                f"{BUILD_CONFIG_PATH} is missing the following required section(s): {', '.join(missing_sections)}."
            )
        if missing_build_versions:
            pytest.fail(
                f"{BUILD_CONFIG_PATH} is missing 'build_version' key in section(s): {', '.join(missing_build_versions)}."
            )