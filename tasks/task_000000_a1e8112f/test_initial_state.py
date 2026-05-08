# test_initial_state.py

import os
import pytest

HOME = "/home/user"
NODES = ["node1", "node2", "node3"]
NODE_DIRS = [os.path.join(HOME, n) for n in NODES]
CONFIG_FILES = [os.path.join(d, "config.txt") for d in NODE_DIRS]
INITIAL_CONFIGS = {
    "node1": "setting=old1",
    "node2": "setting=old2",
    "node3": "setting=gamma",
}
LOG_FILE = os.path.join(HOME, "config_changes.log")

@pytest.mark.parametrize("node_dir", NODE_DIRS)
def test_node_directory_exists(node_dir):
    assert os.path.isdir(node_dir), (
        f"Missing required directory: {node_dir}"
    )

@pytest.mark.parametrize("config_file", CONFIG_FILES)
def test_config_file_exists(config_file):
    assert os.path.isfile(config_file), (
        f"Missing required config file: {config_file}"
    )

@pytest.mark.parametrize("node,expected_line", INITIAL_CONFIGS.items())
def test_config_file_content(node, expected_line):
    config_path = os.path.join(HOME, node, "config.txt")
    assert os.path.isfile(config_path), (
        f"Config file missing: {config_path}"
    )
    with open(config_path, "rt") as f:
        lines = [line.rstrip("\n") for line in f]
    assert len(lines) == 1, (
        f"Config file {config_path} should have exactly one line, found {len(lines)}"
    )
    assert lines[0] == expected_line, (
        f"Config file {config_path} has incorrect content: "
        f"expected '{expected_line}', found '{lines[0]}'"
    )

def test_log_file_does_not_exist():
    assert not os.path.exists(LOG_FILE), (
        f"Log file {LOG_FILE} should NOT exist before the task is performed."
    )