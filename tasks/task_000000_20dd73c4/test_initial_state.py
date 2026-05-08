# test_initial_state.py

import os
import pytest

ARTIFACTS_TXT_PATH = "/home/user/mlops/experiments/artifacts.txt"
EXPERIMENTS_DIR = "/home/user/mlops/experiments"

EXPECTED_ARTIFACTS_TXT_CONTENT = (
    "model\n"
    "log\n"
    "model\n"
    "plot\n"
    "model\n"
    "plot\n"
    "model\n"
    "log\n"
    "plot\n"
    "model\n"
)

def test_experiments_directory_exists_and_is_writable():
    assert os.path.isdir(EXPERIMENTS_DIR), (
        f"Required directory does not exist: {EXPERIMENTS_DIR}"
    )
    assert os.access(EXPERIMENTS_DIR, os.W_OK), (
        f"Directory is not writable: {EXPERIMENTS_DIR}"
    )

def test_artifacts_txt_exists_and_has_expected_content():
    assert os.path.isfile(ARTIFACTS_TXT_PATH), (
        f"Required file does not exist: {ARTIFACTS_TXT_PATH}"
    )
    with open(ARTIFACTS_TXT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_ARTIFACTS_TXT_CONTENT, (
        f"File {ARTIFACTS_TXT_PATH} does not have the expected contents.\n"
        "Expected content (repr):\n"
        f"{repr(EXPECTED_ARTIFACTS_TXT_CONTENT)}\n"
        "Actual content (repr):\n"
        f"{repr(content)}"
    )

def test_artifact_type_counts_txt_does_not_exist():
    output_path = os.path.join(EXPERIMENTS_DIR, "artifact_type_counts.txt")
    assert not os.path.exists(output_path), (
        f"Output file should not exist before execution: {output_path}"
    )