# test_initial_state.py

import os
import pytest

HOME = "/home/user"
NODE1_DIR = os.path.join(HOME, "node1")
NODE2_DIR = os.path.join(HOME, "node2")
NODE1_RESULT = os.path.join(NODE1_DIR, "result.txt")
NODE2_RESULT = os.path.join(NODE2_DIR, "result.txt")
SUMMARY_LOG = os.path.join(HOME, "experiment_artifacts_summary.log")

def test_node1_directory_exists():
    assert os.path.isdir(NODE1_DIR), f"Missing required directory: {NODE1_DIR}"

def test_node2_directory_exists():
    assert os.path.isdir(NODE2_DIR), f"Missing required directory: {NODE2_DIR}"

def test_node1_result_file_exists():
    assert os.path.isfile(NODE1_RESULT), f"Missing required file: {NODE1_RESULT}"

def test_node2_result_file_exists():
    assert os.path.isfile(NODE2_RESULT), f"Missing required file: {NODE2_RESULT}"

def test_node1_result_file_content():
    if not os.path.isfile(NODE1_RESULT):
        pytest.skip(f"{NODE1_RESULT} does not exist, cannot check content.")
    with open(NODE1_RESULT, "r") as f:
        content = f.read().strip()
    expected = "accuracy: 0.91"
    assert content == expected, (
        f"Incorrect content in {NODE1_RESULT}. Expected exactly:\n{expected}\nGot:\n{content}"
    )

def test_node2_result_file_content():
    if not os.path.isfile(NODE2_RESULT):
        pytest.skip(f"{NODE2_RESULT} does not exist, cannot check content.")
    with open(NODE2_RESULT, "r") as f:
        content = f.read().strip()
    expected = "accuracy: 0.88"
    assert content == expected, (
        f"Incorrect content in {NODE2_RESULT}. Expected exactly:\n{expected}\nGot:\n{content}"
    )

def test_summary_log_does_not_exist():
    assert not os.path.exists(SUMMARY_LOG), (
        f"{SUMMARY_LOG} already exists. This file should not exist before the student performs the action."
    )