# test_initial_state.py

import os
import pytest

UTF16_FILE = "/home/user/configs/app-deployment.yaml.utf16"
UTF8_FILE = "/home/user/configs/app-deployment.yaml"
LOG_FILE = "/home/user/configs/conversion.log"
CONFIGS_DIR = "/home/user/configs"

@pytest.mark.describe("Initial system state for Kubernetes manifest encoding conversion")
class TestInitialState:
    def test_configs_directory_exists(self):
        assert os.path.isdir(CONFIGS_DIR), (
            f"Required directory {CONFIGS_DIR} does not exist."
        )

    def test_utf16_file_exists(self):
        assert os.path.isfile(UTF16_FILE), (
            f"Required UTF-16 manifest file {UTF16_FILE} does not exist."
        )

    def test_utf16_file_is_nonempty(self):
        size = os.path.getsize(UTF16_FILE)
        assert size > 0, (
            f"UTF-16 manifest file {UTF16_FILE} exists but is empty."
        )

    def test_utf16_file_is_utf16le_with_bom(self):
        with open(UTF16_FILE, "rb") as f:
            raw = f.read(4)
        # BOM for UTF-16 LE is b'\xff\xfe'
        assert raw.startswith(b'\xff\xfe'), (
            f"{UTF16_FILE} does not start with a UTF-16 LE BOM."
        )

    def test_utf16_file_contents_are_ascii_yaml(self):
        # Read entire file as UTF-16
        with open(UTF16_FILE, "rb") as f:
            content_bytes = f.read()
        # Decode as UTF-16 with BOM
        try:
            text = content_bytes.decode('utf-16')
        except UnicodeDecodeError:
            pytest.fail(f"Failed to decode {UTF16_FILE} as UTF-16.")
        # All characters must be ASCII
        non_ascii = [ch for ch in text if ord(ch) > 127]
        assert not non_ascii, (
            f"{UTF16_FILE} contains non-ASCII characters: {non_ascii}"
        )
        # Check that the manifest is as expected (basic verification)
        assert "---" in text, (
            f"{UTF16_FILE} does not appear to contain a valid YAML manifest."
        )
        assert "apiVersion:" in text and "kind: Deployment" in text, (
            f"{UTF16_FILE} does not appear to contain correct deployment YAML."
        )

    def test_utf8_file_does_not_exist(self):
        assert not os.path.exists(UTF8_FILE), (
            f"Output file {UTF8_FILE} should not exist before conversion."
        )

    def test_log_file_does_not_exist(self):
        assert not os.path.exists(LOG_FILE), (
            f"Log file {LOG_FILE} should not exist before conversion."
        )