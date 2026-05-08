# test_initial_state.py

import os
import stat
import pytest
import hashlib

EXPERIMENT_DIR = "/home/user/experiments/exp42"
MODEL_BIN_PATH = os.path.join(EXPERIMENT_DIR, "model.bin")
MODEL_BIN_EXPECTED_CONTENT = b"Hello, Experiment 42!\n"

@pytest.mark.describe("Initial state of experiment artifact integrity task")
def test_experiment_directory_exists_and_writable():
    assert os.path.isdir(EXPERIMENT_DIR), (
        f"Required directory {EXPERIMENT_DIR} does not exist."
    )
    # Check write permission for user
    st = os.stat(EXPERIMENT_DIR)
    mode = st.st_mode
    assert mode & stat.S_IWUSR, (
        f"User does not have write permissions on {EXPERIMENT_DIR}."
    )

def test_model_bin_exists_with_expected_content():
    assert os.path.isfile(MODEL_BIN_PATH), (
        f"Required file {MODEL_BIN_PATH} does not exist."
    )
    with open(MODEL_BIN_PATH, "rb") as f:
        content = f.read()
    assert content == MODEL_BIN_EXPECTED_CONTENT, (
        f"File {MODEL_BIN_PATH} does not contain the expected content.\n"
        "Expected:\n"
        f"{MODEL_BIN_EXPECTED_CONTENT!r}\n"
        "Got:\n"
        f"{content!r}"
    )

def test_model_bin_sha256_file_does_not_exist_yet():
    sha256_path = os.path.join(EXPERIMENT_DIR, "model.bin.sha256")
    assert not os.path.exists(sha256_path), (
        f"The checksum file {sha256_path} should NOT exist before the student performs the action."
    )

def test_checksum_verification_log_does_not_exist_yet():
    log_path = os.path.join(EXPERIMENT_DIR, "checksum_verification.log")
    assert not os.path.exists(log_path), (
        f"The log file {log_path} should NOT exist before the student performs the action."
    )