# test_final_state.py

import os
import pytest

CONFIG_PATH = "/home/user/ci_cd/config.ini"
DEPLOYMENT_CONFIG_PATH = "/home/user/ci_cd/deployment_config.log"

@pytest.mark.describe("Final State Validation: deployment_config.log extraction")
class TestFinalState:

    def test_deployment_config_log_exists(self):
        assert os.path.isfile(DEPLOYMENT_CONFIG_PATH), (
            f"Expected {DEPLOYMENT_CONFIG_PATH} to exist after task completion, but it does not."
        )

    def test_deployment_config_log_contents_exact(self):
        """
        Validates that deployment_config.log contains exactly the key-value pairs from the [deployment]
        section in config.ini, in order, no extra whitespace or blank lines.
        """
        expected_lines = [
            "strategy=blue-green",
            "timeout=300",
            "rollback=true"
        ]
        try:
            with open(DEPLOYMENT_CONFIG_PATH, "r") as f:
                actual_lines = f.read().splitlines()
        except Exception as e:
            pytest.fail(
                f"Could not read {DEPLOYMENT_CONFIG_PATH}: {e}"
            )

        assert actual_lines == expected_lines, (
            f"{DEPLOYMENT_CONFIG_PATH} does not contain the exact expected lines from the [deployment] section.\n"
            f"--- Expected ---\n" + "\n".join(expected_lines) + "\n"
            f"--- Actual ---\n" + "\n".join(actual_lines) + "\n"
            f"Check for extra/missing lines, whitespace, or incorrect key order."
        )

    def test_deployment_config_log_no_extra_content(self):
        """
        Ensures no extra blank lines, whitespace, or keys from other sections are present.
        """
        with open(DEPLOYMENT_CONFIG_PATH, "r") as f:
            lines = f.readlines()
        for idx, line in enumerate(lines):
            stripped = line.rstrip('\n')
            assert stripped == stripped.strip(), (
                f"Line {idx+1} in {DEPLOYMENT_CONFIG_PATH} contains leading or trailing whitespace: {repr(line)}"
            )
            assert stripped != "", (
                f"Line {idx+1} in {DEPLOYMENT_CONFIG_PATH} is blank. There should be no blank lines."
            )
        # Ensure file ends with a newline (POSIX convention)
        with open(DEPLOYMENT_CONFIG_PATH, "rb") as f:
            f.seek(-1, os.SEEK_END)
            last_char = f.read(1)
            assert last_char == b'\n', (
                f"{DEPLOYMENT_CONFIG_PATH} should end with a single newline character."
            )

    def test_config_ini_is_unchanged(self):
        """
        Ensures config.ini is not modified in any way.
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
            f"The contents of {CONFIG_PATH} have been modified. This file must remain unchanged.\n"
            f"--- Expected ---\n{expected}\n"
            f"--- Actual ---\n{actual}"
        )