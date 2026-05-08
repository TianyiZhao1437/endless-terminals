# test_initial_state.py

import os
import pytest

CONFIG_DIR = "/home/user/configs"
CONFIG_FILE = os.path.join(CONFIG_DIR, "device_settings.conf")
LOG_FILE = os.path.join(CONFIG_DIR, "encoding_conversion.log")

DEVICE_SETTINGS_CONTENT = (
    "# Device Configuration\n"
    "location=São Paulo\n"
    "temperature_unit=Celsius\n"
)

@pytest.fixture(scope="module")
def config_file_exists():
    return os.path.isfile(CONFIG_FILE)

@pytest.fixture(scope="module")
def config_file_content():
    if not os.path.isfile(CONFIG_FILE):
        return None
    try:
        with open(CONFIG_FILE, "rb") as f:
            content_bytes = f.read()
        # Try to decode as UTF-8
        try:
            content = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return None
        return content
    except Exception:
        return None

def test_config_file_exists(config_file_exists):
    assert config_file_exists, (
        f"Missing required file: {CONFIG_FILE}. "
        "Create the file before proceeding."
    )

def test_config_file_is_utf8_and_content(config_file_exists, config_file_content):
    if not config_file_exists:
        pytest.skip(f"{CONFIG_FILE} does not exist")
    assert config_file_content is not None, (
        f"{CONFIG_FILE} must be encoded in UTF-8 and readable as such. "
        "Check the file encoding."
    )
    # Check for at least one non-ASCII character ("ã" or "é")
    assert any(c in config_file_content for c in ("ã", "é")), (
        f"{CONFIG_FILE} must contain at least one non-ASCII (Latin-1 compatible) character (e.g., 'é', 'ã')."
    )
    # Check for exact expected content
    assert config_file_content == DEVICE_SETTINGS_CONTENT, (
        f"{CONFIG_FILE} content does not match the expected initial configuration:\n"
        f"Expected:\n{DEVICE_SETTINGS_CONTENT}\n"
        f"Found:\n{config_file_content}"
    )

def test_log_file_does_not_exist_initially():
    assert not os.path.exists(LOG_FILE), (
        f"The log file {LOG_FILE} should NOT exist before you perform the encoding conversion task."
    )

def test_configs_directory_exists():
    assert os.path.isdir(CONFIG_DIR), (
        f"Missing required directory: {CONFIG_DIR}. "
        "Create this directory before proceeding."
    )