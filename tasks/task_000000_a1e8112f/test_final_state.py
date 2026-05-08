# test_final_state.py

import os
import pytest

HOME = "/home/user"
NODES = ["node1", "node2", "node3"]
NODE_DIRS = [os.path.join(HOME, n) for n in NODES]
CONFIG_FILES = [os.path.join(d, "config.txt") for d in NODE_DIRS]
FINAL_CONFIGS = {
    "node1": "setting=alpha",
    "node2": "setting=beta",
    "node3": "setting=gamma",
}
LOG_FILE = os.path.join(HOME, "config_changes.log")
EXPECTED_LOG_LINES = [
    "[node1] setting: alpha - DIFF",
    "[node2] setting: beta - DIFF",
    "[node3] setting: gamma - DIFF",
]


@pytest.mark.parametrize("node_dir", NODE_DIRS)
def test_node_directory_exists(node_dir):
    assert os.path.isdir(node_dir), (
        f"Required directory missing after task: {node_dir}"
    )


@pytest.mark.parametrize("config_file", CONFIG_FILES)
def test_config_file_exists(config_file):
    assert os.path.isfile(config_file), (
        f"Required config file missing after task: {config_file}"
    )


@pytest.mark.parametrize("node,expected_line", FINAL_CONFIGS.items())
def test_config_file_content(node, expected_line):
    config_path = os.path.join(HOME, node, "config.txt")
    assert os.path.isfile(config_path), (
        f"Config file missing after task: {config_path}"
    )
    with open(config_path, "rt") as f:
        lines = [line.rstrip("\n") for line in f]
    assert len(lines) == 1, (
        f"Config file {config_path} must have exactly one line, found {len(lines)}"
    )
    assert lines[0] == expected_line, (
        f"Config file {config_path} has incorrect content after task: "
        f"expected '{expected_line}', found '{lines[0]}'"
    )


def test_log_file_exists():
    assert os.path.isfile(LOG_FILE), (
        f"Log file {LOG_FILE} was not created after the task."
    )


def test_log_file_content():
    assert os.path.isfile(LOG_FILE), (
        f"Log file {LOG_FILE} does not exist."
    )
    with open(LOG_FILE, "rt", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    assert len(lines) == 3, (
        f"Log file {LOG_FILE} must have exactly 3 lines, found {len(lines)}."
    )
    for i, (actual, expected) in enumerate(zip(lines, EXPECTED_LOG_LINES)):
        assert actual == expected, (
            f"Line {i+1} of log file {LOG_FILE} incorrect:\n"
            f"  Expected: '{expected}'\n"
            f"  Found:    '{actual}'"
        )
    # Check no extra content (e.g., trailing lines)
    with open(LOG_FILE, "rb") as f:
        content = f.read()
    # The expected content is lines joined by '\n' + a final '\n' if the file ends with one
    expected_content = "\n".join(EXPECTED_LOG_LINES)
    # The task requires single newlines between lines, UNIX format, and no extra whitespace.
    # Accept with or without a final '\n'
    valid_endings = [expected_content.encode("utf-8"),
                     (expected_content + "\n").encode("utf-8")]
    assert content in valid_endings, (
        f"Log file {LOG_FILE} must contain exactly three lines separated by single UNIX newlines, "
        f"and no extra whitespace or blank lines.\n"
        f"Expected content:\n{expected_content}\n"
        f"Actual content:\n{content.decode('utf-8')}"
    )