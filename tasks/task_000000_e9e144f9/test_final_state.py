# test_final_state.py

import os
import pytest

UTF16_FILE = "/home/user/configs/app-deployment.yaml.utf16"
UTF8_FILE = "/home/user/configs/app-deployment.yaml"
LOG_FILE = "/home/user/configs/conversion.log"
CONFIGS_DIR = "/home/user/configs"

EXPECTED_YAML = (
    "---\n"
    "apiVersion: apps/v1\n"
    "kind: Deployment\n"
    "metadata:\n"
    "  name: test-app-deployment\n"
    "spec:\n"
    "  replicas: 3\n"
    "  selector:\n"
    "    matchLabels:\n"
    "      app: test-app\n"
    "  template:\n"
    "    metadata:\n"
    "      labels:\n"
    "        app: test-app\n"
    "    spec:\n"
    "      containers:\n"
    "      - name: test-app-container\n"
    "        image: nginx:1.14.2\n"
    "        ports:\n"
    "        - containerPort: 80\n"
)

EXPECTED_LOG = (
    "Encoding conversion: SUCCESS\n"
    "Non-ASCII characters: ABSENT\n"
)

@pytest.mark.describe("Final system state for Kubernetes manifest encoding conversion")
class TestFinalState:
    def test_configs_directory_exists(self):
        assert os.path.isdir(CONFIGS_DIR), (
            f"Required directory {CONFIGS_DIR} does not exist."
        )

    def test_utf16_file_still_exists(self):
        assert os.path.isfile(UTF16_FILE), (
            f"Original UTF-16 manifest file {UTF16_FILE} is missing after conversion."
        )

    def test_utf8_file_exists_and_is_utf8(self):
        assert os.path.isfile(UTF8_FILE), (
            f"Converted UTF-8 manifest file {UTF8_FILE} does not exist."
        )
        size = os.path.getsize(UTF8_FILE)
        assert size > 0, (
            f"Converted UTF-8 manifest file {UTF8_FILE} exists but is empty."
        )
        # Read file as UTF-8
        try:
            with open(UTF8_FILE, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            pytest.fail(f"{UTF8_FILE} is not valid UTF-8 encoded.")

        # Assert exact YAML content
        assert text == EXPECTED_YAML, (
            f"{UTF8_FILE} content is incorrect.\n"
            "Expected (repr):\n"
            f"{repr(EXPECTED_YAML)}\n"
            "Actual (repr):\n"
            f"{repr(text)}\n"
            "File must match the exact YAML manifest with UNIX line endings."
        )

        # Check all characters are ASCII
        non_ascii = [ch for ch in text if ord(ch) > 127]
        assert not non_ascii, (
            f"{UTF8_FILE} contains non-ASCII characters: {non_ascii}"
        )

        # Check line endings are UNIX (\n), not Windows (\r\n)
        assert '\r' not in text, (
            f"{UTF8_FILE} contains Windows-style line endings (\\r)."
        )

    def test_log_file_exists_and_content(self):
        assert os.path.isfile(LOG_FILE), (
            f"Log file {LOG_FILE} does not exist."
        )
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            log_content = f.read()
        assert log_content == EXPECTED_LOG, (
            f"Log file {LOG_FILE} has incorrect contents.\n"
            "Expected (repr):\n"
            f"{repr(EXPECTED_LOG)}\n"
            "Actual (repr):\n"
            f"{repr(log_content)}\n"
            "Log file must match the exact required format and wording."
        )

    def test_console_output_matches_yaml(self, capsys):
        # This test assumes the agent prints the YAML file contents to stdout at task completion.
        # Simulate reading YAML and printing it
        with open(UTF8_FILE, "r", encoding="utf-8") as f:
            yaml_text = f.read()
        print(yaml_text, end='')  # Print without extra newline

        captured = capsys.readouterr()
        # The console output must match the YAML exactly (including trailing newline)
        assert captured.out == EXPECTED_YAML, (
            "Console output does not match the expected YAML manifest.\n"
            "Expected (repr):\n"
            f"{repr(EXPECTED_YAML)}\n"
            "Actual (repr):\n"
            f"{repr(captured.out)}"
        )