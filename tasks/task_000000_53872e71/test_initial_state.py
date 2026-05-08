# test_initial_state.py

import os
import pytest

CONFIG_PATH = "/home/user/ci_cd/config.ini"
DEPLOYMENT_CONFIG_PATH = "/home/user/ci_cd/deployment_config.log"

@pytest.mark.describe("Initial OS/Filesystem State Validation")
class TestInitialState:

    def test_config_ini_exists(self):
        assert os.path.isfile(CONFIG_PATH), (
            f"Missing required configuration file: {CONFIG_PATH}"
        )

    def test_config_ini_contents(self):
        """
        Validates the exact contents of /home/user/ci_cd/config.ini.
        """
        expected = (
            "[general]\n"
            "env=staging\n"
            "build_number=615\n"
            "\n"
            "[deployment]\n"
            "strategy=blue-green\n"
            "timeout=300\n"
            "rollback=true\n"
            "\n"
            "[notifications]\n"
            "slack_channel=devops-alerts\n"
        )
        try:
            with open(CONFIG_PATH, "r") as f:
                actual = f.read()
        except Exception as e:
            pytest.fail(f"Could not read {CONFIG_PATH}: {e}")

        assert actual == expected, (
            f"The contents of {CONFIG_PATH} do not match the expected initial state.\n"
            f"--- Expected ---\n{expected}\n"
            f"--- Actual ---\n{actual}"
        )

    def test_deployment_config_log_does_not_exist(self):
        """
        deployment_config.log should not exist before the student performs the action.
        """
        assert not os.path.exists(DEPLOYMENT_CONFIG_PATH), (
            f"{DEPLOYMENT_CONFIG_PATH} should NOT exist before the task is performed."
        )