# test_final_state.py

import os
import pytest

CONFIG_DIR = "/home/user/configs"
CONFIG_FILE = os.path.join(CONFIG_DIR, "device_settings.conf")
LOG_FILE = os.path.join(CONFIG_DIR, "encoding_conversion.log")

EXPECTED_CONFIG_CONTENT = (
    "# Device Configuration\n"
    "location=São Paulo\n"
    "temperature_unit=Celsius\n"
)

EXPECTED_LOG_LINE = (
    "Original encoding: UTF-8, New encoding: ISO-8859-1, File: /home/user/configs/device_settings.conf"
)


def test_configs_directory_exists():
    assert os.path.isdir(CONFIG_DIR), (
        f"Required directory {CONFIG_DIR} does not exist. "
        "You must not delete or rename this directory."
    )


def test_config_file_exists():
    assert os.path.isfile(CONFIG_FILE), (
        f"Required configuration file {CONFIG_FILE} does not exist. "
        "You must not delete or rename this file."
    )


def test_config_file_is_iso_8859_1_and_content():
    assert os.path.isfile(CONFIG_FILE), (
        f"Required configuration file {CONFIG_FILE} does not exist."
    )

    # Try to decode as ISO-8859-1
    try:
        with open(CONFIG_FILE, "rb") as f:
            content_bytes = f.read()
        content_iso = content_bytes.decode("iso-8859-1")
    except Exception as e:
        pytest.fail(
            f"{CONFIG_FILE} could not be read or decoded as ISO-8859-1 (Latin-1): {e}. "
            "Ensure you converted the file encoding correctly."
        )

    # Content must match exactly
    if content_iso != EXPECTED_CONFIG_CONTENT:
        pytest.fail(
            f"{CONFIG_FILE} content incorrect after encoding conversion.\n"
            "Expected content:\n"
            f"{EXPECTED_CONFIG_CONTENT}\n"
            "Found:\n"
            f"{content_iso}\n"
            "Did you accidentally change the file content during conversion?"
        )

    # Confirm file cannot be decoded as UTF-8 (should raise UnicodeDecodeError)
    # This is a strong but not absolute check: if only ASCII/Latin-1 chars, it could decode as UTF-8.
    # But since the original file had 'ã' (0xE3 in Latin-1, not valid UTF-8), decoding as UTF-8 must fail.
    with open(CONFIG_FILE, "rb") as f:
        content_bytes = f.read()
    try:
        content_bytes.decode("utf-8")
        pytest.fail(
            f"{CONFIG_FILE} is still decodable as UTF-8 after supposed conversion. "
            "The file must be re-encoded as ISO-8859-1 and should not be valid UTF-8 if non-ASCII Latin-1 chars are present."
        )
    except UnicodeDecodeError:
        pass  # Expected: file is not valid UTF-8 anymore


def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"Required log file {LOG_FILE} does not exist. "
        "You must create this log file after conversion."
    )


def test_log_file_content_exact():
    assert os.path.isfile(LOG_FILE), (
        f"Required log file {LOG_FILE} does not exist."
    )
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1, (
        f"{LOG_FILE} must contain exactly one line. "
        f"Found {len(lines)} lines."
    )
    line = lines[0].rstrip('\n')
    assert line == EXPECTED_LOG_LINE, (
        f"{LOG_FILE} content does not match expected log line.\n"
        f"Expected:\n{EXPECTED_LOG_LINE}\n"
        f"Found:\n{line}"
    )
    # Ensure no trailing newlines or whitespace
    with open(LOG_FILE, "rb") as f:
        raw = f.read()
    if not raw.endswith(b'\n'):
        pytest.fail(
            f"{LOG_FILE} must end with a single newline character (\\n)."
        )
    if raw.count(b'\n') != 1:
        pytest.fail(
            f"{LOG_FILE} must contain exactly one line ending with a single newline. "
            f"Found {raw.count(b'\\n')} newlines."
        )