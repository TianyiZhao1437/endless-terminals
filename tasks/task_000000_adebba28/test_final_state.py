# test_final_state.py

import os
import pytest
import stat
import hashlib

ARTIFACTS_DIR = "/home/user/mlruns/artifacts"
MODEL_FILE = os.path.join(ARTIFACTS_DIR, "trained_model.pt")
LOG_FILE = os.path.join(ARTIFACTS_DIR, "artifact_checksum.log")

EXPECTED_MODEL_BYTES = bytes([
    0x50, 0x59, 0x54, 0x4f, 0x52, 0x43, 0x48, 0x20,
    0x6d, 0x6f, 0x64, 0x65, 0x6c, 0x20, 0x66, 0x69, 0x6c, 0x65
])
EXPECTED_SHA256 = "5e01e1bbd9be7eec772abfc5ec61d7f606c2c27a9aee302011390dbe2a53c6f6"
EXPECTED_LOG_LINE = f"trained_model.pt SHA256: {EXPECTED_SHA256}"

def test_artifacts_dir_exists_and_writable():
    assert os.path.isdir(ARTIFACTS_DIR), (
        f"Directory '{ARTIFACTS_DIR}' does not exist after task completion."
    )
    assert os.access(ARTIFACTS_DIR, os.W_OK), (
        f"Directory '{ARTIFACTS_DIR}' is not writable after task completion."
    )

def test_trained_model_pt_exists_and_content():
    assert os.path.isfile(MODEL_FILE), (
        f"File '{MODEL_FILE}' does not exist after task completion."
    )
    try:
        with open(MODEL_FILE, "rb") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read '{MODEL_FILE}': {e}")

    assert content == EXPECTED_MODEL_BYTES, (
        f"File '{MODEL_FILE}' content was modified. "
        f"Expected: {EXPECTED_MODEL_BYTES!r}, Found: {content!r}"
    )

def test_trained_model_pt_checksum():
    try:
        with open(MODEL_FILE, "rb") as f:
            file_bytes = f.read()
    except Exception as e:
        pytest.fail(f"Could not read '{MODEL_FILE}' for checksum calculation: {e}")

    sha256 = hashlib.sha256(file_bytes).hexdigest()
    assert sha256 == EXPECTED_SHA256, (
        f"SHA256 checksum of '{MODEL_FILE}' is incorrect. "
        f"Expected: {EXPECTED_SHA256}, Found: {sha256}"
    )

def test_artifact_checksum_log_exists():
    assert os.path.isfile(LOG_FILE), (
        f"File '{LOG_FILE}' does not exist after task completion."
    )

def test_artifact_checksum_log_content():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        pytest.fail(f"Could not read '{LOG_FILE}': {e}")

    # Check for exactly one line, no extra whitespace or lines
    if not lines:
        pytest.fail(
            f"File '{LOG_FILE}' is empty. Expected exactly one line: {EXPECTED_LOG_LINE!r}"
        )
    if len(lines) != 1:
        pytest.fail(
            f"File '{LOG_FILE}' has {len(lines)} lines. Expected exactly one line."
        )
    line = lines[0].rstrip('\r\n')
    assert line == EXPECTED_LOG_LINE, (
        f"File '{LOG_FILE}' line content is incorrect.\n"
        f"Expected: {EXPECTED_LOG_LINE!r}\nFound: {line!r}"
    )

def test_artifact_checksum_log_permissions():
    st = os.stat(LOG_FILE)
    mode = st.st_mode
    # User must have read and write permission
    user_can_read = mode & stat.S_IRUSR
    user_can_write = mode & stat.S_IWUSR
    assert user_can_read, (
        f"File '{LOG_FILE}' is not readable by the user."
    )
    assert user_can_write, (
        f"File '{LOG_FILE}' is not writable by the user."
    )