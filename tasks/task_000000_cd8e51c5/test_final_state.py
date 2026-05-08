# test_final_state.py

import os
import stat
import hashlib
import pytest

EXPERIMENT_DIR = "/home/user/experiments/exp42"
MODEL_BIN_PATH = os.path.join(EXPERIMENT_DIR, "model.bin")
MODEL_BIN_SHA256_PATH = os.path.join(EXPERIMENT_DIR, "model.bin.sha256")
CHECKSUM_LOG_PATH = os.path.join(EXPERIMENT_DIR, "checksum_verification.log")

# Truth data
MODEL_BIN_EXPECTED_CONTENT = b"Hello, Experiment 42!\n"
MODEL_BIN_EXPECTED_SHA256 = "b2b95deb0706e89e8ad51a4a4cde98a29a97ed2267a1a479b0de92c5c6fb366b"
MODEL_BIN_SHA256_EXPECTED_LINE = (
    f"{MODEL_BIN_EXPECTED_SHA256}  model.bin"
)
LOG_LINE_OK = "model.bin: OK"
LOG_LINE_FAILED = "model.bin: FAILED"

@pytest.mark.describe("Final state of experiment artifact integrity task")
def test_experiment_directory_still_exists_and_writable():
    assert os.path.isdir(EXPERIMENT_DIR), (
        f"Required directory {EXPERIMENT_DIR} does not exist after task completion."
    )
    st = os.stat(EXPERIMENT_DIR)
    mode = st.st_mode
    assert mode & stat.S_IWUSR, (
        f"User does not have write permissions on {EXPERIMENT_DIR} after task completion."
    )

def test_model_bin_exists_and_content_unchanged():
    assert os.path.isfile(MODEL_BIN_PATH), (
        f"Required file {MODEL_BIN_PATH} does not exist after task completion."
    )
    with open(MODEL_BIN_PATH, "rb") as f:
        content = f.read()
    assert content == MODEL_BIN_EXPECTED_CONTENT, (
        f"{MODEL_BIN_PATH} content was modified after the task.\n"
        f"Expected:\n{MODEL_BIN_EXPECTED_CONTENT!r}\n"
        f"Got:\n{content!r}"
    )

def test_model_bin_sha256_file_exists_and_correct():
    assert os.path.isfile(MODEL_BIN_SHA256_PATH), (
        f"Checksum file {MODEL_BIN_SHA256_PATH} does not exist after task completion."
    )
    with open(MODEL_BIN_SHA256_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    assert len(lines) == 1, (
        f"{MODEL_BIN_SHA256_PATH} should contain exactly one line, but contains {len(lines)} lines."
    )
    actual_line = lines[0]
    assert actual_line == MODEL_BIN_SHA256_EXPECTED_LINE, (
        f"{MODEL_BIN_SHA256_PATH} does not contain the correct SHA256 line.\n"
        f"Expected:\n{MODEL_BIN_SHA256_EXPECTED_LINE!r}\n"
        f"Got:\n{actual_line!r}"
    )

def test_checksum_is_correct_for_model_bin():
    # Validate the actual file hash matches the content in model.bin.sha256
    with open(MODEL_BIN_PATH, "rb") as f:
        content = f.read()
    actual_sha256 = hashlib.sha256(content).hexdigest()
    assert actual_sha256 == MODEL_BIN_EXPECTED_SHA256, (
        f"The SHA256 of {MODEL_BIN_PATH} does not match the expected value.\n"
        f"Expected: {MODEL_BIN_EXPECTED_SHA256}\n"
        f"Got:      {actual_sha256}"
    )

def test_checksum_verification_log_exists_and_correct():
    assert os.path.isfile(CHECKSUM_LOG_PATH), (
        f"Log file {CHECKSUM_LOG_PATH} does not exist after task completion."
    )
    with open(CHECKSUM_LOG_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    assert len(lines) == 1, (
        f"{CHECKSUM_LOG_PATH} must contain exactly one line, but contains {len(lines)} lines."
    )
    actual_line = lines[0]
    # Determine what the correct log line should be
    # If model.bin content is as expected, log must be OK; otherwise, it must be FAILED
    with open(MODEL_BIN_PATH, "rb") as f:
        content = f.read()
    actual_sha256 = hashlib.sha256(content).hexdigest()
    if actual_sha256 == MODEL_BIN_EXPECTED_SHA256:
        expected_log_line = LOG_LINE_OK
    else:
        expected_log_line = LOG_LINE_FAILED
    assert actual_line == expected_log_line, (
        f"{CHECKSUM_LOG_PATH} contains the wrong verification result.\n"
        f"Expected:\n{expected_log_line!r}\n"
        f"Got:\n{actual_line!r}"
    )