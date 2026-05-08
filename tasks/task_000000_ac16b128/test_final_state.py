# test_final_state.py

import os
import pytest

CRED_FILE = "/home/user/secure/credentials.txt"
CRED_DIR = "/home/user/secure"
EXPECTED_CONTENT = "API_KEY=new_secret_key"
EXPECTED_BYTES = EXPECTED_CONTENT.encode("utf-8")

def test_secure_directory_still_exists():
    assert os.path.isdir(CRED_DIR), (
        f"Directory '{CRED_DIR}' is missing after rotation. "
        "The secure directory must remain present."
    )

def test_credentials_file_still_exists():
    assert os.path.isfile(CRED_FILE), (
        f"Credentials file '{CRED_FILE}' is missing after rotation. "
        "It must not be deleted or moved."
    )

def test_credentials_file_content_exact():
    """
    The credentials file must contain exactly:
    API_KEY=new_secret_key
    with no extra spaces, newlines, or other characters.
    """
    try:
        with open(CRED_FILE, "rb") as f:
            content_bytes = f.read()
    except Exception as e:
        pytest.fail(f"Could not read '{CRED_FILE}': {e}")

    if content_bytes != EXPECTED_BYTES:
        actual = content_bytes.decode("utf-8", errors="replace")
        pytest.fail(
            f"File '{CRED_FILE}' content is incorrect after rotation.\n"
            f"Expected exactly: {repr(EXPECTED_CONTENT)}\n"
            f"Found: {repr(actual)}\n"
            "The file must contain exactly one line with the new API key and no extra whitespace or newlines."
        )

def test_no_extra_files_or_deletions():
    """
    Ensure that no files or directories have been created or deleted in /home/user/secure.
    Only /home/user/secure/credentials.txt must be present.
    """
    try:
        entries = os.listdir(CRED_DIR)
    except Exception as e:
        pytest.fail(f"Could not list directory '{CRED_DIR}': {e}")

    expected_files = {"credentials.txt"}
    actual_files = set(entries)
    extra = actual_files - expected_files
    missing = expected_files - actual_files
    assert not missing, (
        f"Missing expected file(s) in '{CRED_DIR}': {missing}. "
        "No files should have been deleted."
    )
    assert not extra, (
        f"Unexpected extra file(s) in '{CRED_DIR}': {extra}. "
        "No files should have been created."
    )

def test_displayed_credentials_file_contents(capsys):
    """
    Verify that the contents displayed (printed) are exactly 'API_KEY=new_secret_key'
    and nothing else.
    This simulates the verification step.
    """
    # Simulate the code that prints the file's contents
    try:
        with open(CRED_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read '{CRED_FILE}' for display verification: {e}")

    # Print the content (simulate student display)
    print(content, end="")

    captured = capsys.readouterr()
    # The output must be exactly the expected content, with no extra newline
    if captured.out != EXPECTED_CONTENT:
        pytest.fail(
            f"When displaying the credentials file, output is incorrect.\n"
            f"Expected exactly: {repr(EXPECTED_CONTENT)}\n"
            f"Found: {repr(captured.out)}\n"
            "The displayed output must match the file content exactly, with no extra whitespace or newlines."
        )