# test_initial_state.py

import os
import pytest

CONFIG_PATH = "/home/user/build/config_android.txt"
UTF8_OUTPUT_PATH = "/home/user/build/config_android_utf8.txt"
LOG_PATH = "/home/user/build/encoding_conversion.log"

@pytest.mark.describe("Initial OS/filesystem state before encoding conversion")
class TestInitialState:
    def test_config_android_txt_exists(self):
        assert os.path.isfile(CONFIG_PATH), (
            f"Missing required file: {CONFIG_PATH}. "
            "Please ensure the configuration file exists before starting the task."
        )

    def test_config_android_utf8_does_not_exist(self):
        assert not os.path.exists(UTF8_OUTPUT_PATH), (
            f"Output file {UTF8_OUTPUT_PATH} should NOT exist before the task. "
            "Please remove it if present."
        )

    def test_encoding_conversion_log_does_not_exist(self):
        assert not os.path.exists(LOG_PATH), (
            f"Log file {LOG_PATH} should NOT exist before the task. "
            "Please remove it if present."
        )

    def test_config_android_txt_is_iso_8859_1(self):
        """
        Validates that /home/user/build/config_android.txt is encoded in ISO-8859-1
        and contains the expected contents (with 'é' as 0xe9 bytes).
        """
        expected_lines = [
            b"name=Andr\xe9\n",
            b"mode=Desenvolvimento\n",
            b"api=29\n"
        ]
        try:
            with open(CONFIG_PATH, "rb") as f:
                content = f.readlines()
        except Exception as e:
            pytest.fail(f"Could not read {CONFIG_PATH}: {e}")

        assert content == expected_lines, (
            f"{CONFIG_PATH} does not contain the expected ISO-8859-1 encoded contents.\n"
            "Expected (ISO-8859-1 bytes):\n"
            + b"".join(expected_lines).decode("latin1")
            + "\nGot (ISO-8859-1 bytes):\n"
            + b"".join(content).decode("latin1")
        )