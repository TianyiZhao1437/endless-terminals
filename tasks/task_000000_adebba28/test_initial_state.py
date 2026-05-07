# test_initial_state.py

import os
import pytest
import stat

ARTIFACTS_DIR = "/home/user/mlruns/artifacts"
MODEL_FILE = os.path.join(ARTIFACTS_DIR, "trained_model.pt")
LOG_FILE = os.path.join(ARTIFACTS_DIR, "artifact_checksum.log")
EXPECTED_MODEL_BYTES = bytes([
    0x50, 0x59, 0x54, 0x4f, 0x52, 0x43, 0x48, 0x20,
    0x6d, 0x6f, 0x64, 0x65, 0x6c, 0x20, 0x66, 0x69, 0x6c, 0x65
])
EXPECTED_SHA256 = "5e01e1bbd9be7eec772abfc5ec61d7f606c2c27a9aee302011390dbe2a53c6f6"

def test_artifacts_dir_exists_and_writable():
    assert os.path.isdir(ARTIFACTS_DIR), (
        f"Directory '{ARTIFACTS_DIR}' does not exist. Please create it before proceeding."
    )
    assert os.access(ARTIFACTS_DIR, os.W_OK), (
        f"Directory '{ARTIFACTS_DIR}' is not writable. Please ensure write permissions for the agent."
    )

def test_trained_model_pt_exists_and_content():
    assert os.path.isfile(MODEL_FILE), (
        f"File '{MODEL_FILE}' does not exist. Please ensure it is present before proceeding."
    )
    try:
        with open(MODEL_FILE, "rb") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Could not read '{MODEL_FILE}': {e}")

    assert content == EXPECTED_MODEL_BYTES, (
        f"File '{MODEL_FILE}' does not have the expected byte content. "
        f"Expected: {EXPECTED_MODEL_BYTES!r}, Found: {content!r}"
    )

def test_artifact_checksum_log_absent():
    # The log file should not exist before the agent runs.
    assert not os.path.exists(LOG_FILE), (
        f"File '{LOG_FILE}' already exists. It should be created or overwritten by the agent."
    )