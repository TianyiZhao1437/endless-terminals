# test_initial_state.py

import os
import pytest

CRED_FILE = "/home/user/secure/credentials.txt"
CRED_DIR = "/home/user/secure"
EXPECTED_CONTENT = "API_KEY=old_secret_key"

def test_secure_directory_exists():
    assert os.path.isdir(CRED_DIR), (
        f"Required directory '{CRED_DIR}' does not exist. "
        "Make sure the secure directory is present before proceeding."
    )

def test_credentials_file_exists():
    assert os.path.isfile(CRED_FILE), (
        f"Required credentials file '{CRED_FILE}' does not exist. "
        "It must exist before rotating the API key."
    )

def test_credentials_file_content_exact():
    try:
        with open(CRED_FILE, "rb") as f:
            content_bytes = f.read()
    except Exception as e:
        pytest.fail(f"Could not read '{CRED_FILE}': {e}")

    # The file must contain exactly the expected content (no extra newlines or spaces)
    expected_bytes = EXPECTED_CONTENT.encode("utf-8")
    assert content_bytes == expected_bytes, (
        f"File '{CRED_FILE}' content is incorrect.\n"
        f"Expected exactly: {repr(EXPECTED_CONTENT)}\n"
        f"Found: {repr(content_bytes.decode('utf-8', errors='replace'))}\n"
        "The file must contain exactly one line with the old API key and no extra whitespace or newlines."
    )