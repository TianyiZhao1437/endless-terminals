# test_final_state.py

import os
import pytest

HOME = "/home/user"
NODE1_DIR = os.path.join(HOME, "node1")
NODE2_DIR = os.path.join(HOME, "node2")
NODE1_RESULT = os.path.join(NODE1_DIR, "result.txt")
NODE2_RESULT = os.path.join(NODE2_DIR, "result.txt")
SUMMARY_LOG = os.path.join(HOME, "experiment_artifacts_summary.log")

EXPECTED_NODE1_RESULT = "accuracy: 0.91"
EXPECTED_NODE2_RESULT = "accuracy: 0.88"

EXPECTED_SUMMARY_LOG = (
    "Node: node1\n"
    "Output: accuracy: 0.91\n"
    "---\n"
    "Node: node2\n"
    "Output: accuracy: 0.88\n"
    "---\n"
)

def test_node1_result_file_untouched():
    """Ensure node1 result file still exists and is unchanged."""
    assert os.path.isfile(NODE1_RESULT), (
        f"Missing required file: {NODE1_RESULT}. It must remain after task completion."
    )
    with open(NODE1_RESULT, "r") as f:
        content = f.read().strip()
    assert content == EXPECTED_NODE1_RESULT, (
        f"Content of {NODE1_RESULT} was modified. Expected exactly:\n{EXPECTED_NODE1_RESULT}\nGot:\n{content}"
    )

def test_node2_result_file_untouched():
    """Ensure node2 result file still exists and is unchanged."""
    assert os.path.isfile(NODE2_RESULT), (
        f"Missing required file: {NODE2_RESULT}. It must remain after task completion."
    )
    with open(NODE2_RESULT, "r") as f:
        content = f.read().strip()
    assert content == EXPECTED_NODE2_RESULT, (
        f"Content of {NODE2_RESULT} was modified. Expected exactly:\n{EXPECTED_NODE2_RESULT}\nGot:\n{content}"
    )

def test_summary_log_exists():
    """Check that the summary log file was created."""
    assert os.path.isfile(SUMMARY_LOG), (
        f"{SUMMARY_LOG} does not exist. You must create this file in the specified location."
    )

def test_summary_log_content_exact():
    """Check that the summary log file content matches the required format and values exactly."""
    if not os.path.isfile(SUMMARY_LOG):
        pytest.fail(f"{SUMMARY_LOG} does not exist. Cannot check its content.")
    with open(SUMMARY_LOG, "r") as f:
        content = f.read()
    if content != EXPECTED_SUMMARY_LOG:
        # Give a clear diff of what's wrong
        import difflib
        diff = "\n".join(
            difflib.unified_diff(
                EXPECTED_SUMMARY_LOG.splitlines(),
                content.splitlines(),
                fromfile="expected",
                tofile="actual",
                lineterm=""
            )
        )
        pytest.fail(
            f"{SUMMARY_LOG} content is not correct. Diff (expected vs actual):\n{diff}\n\n"
            "Expected content:\n"
            f"{EXPECTED_SUMMARY_LOG!r}\n"
            "Actual content:\n"
            f"{content!r}"
        )

def test_summary_log_format_strict():
    """Ensure that the summary log strictly follows the 3-line-per-node format, in order, with correct separators."""
    with open(SUMMARY_LOG, "r") as f:
        lines = f.readlines()
    expected_lines = [
        "Node: node1\n",
        "Output: accuracy: 0.91\n",
        "---\n",
        "Node: node2\n",
        "Output: accuracy: 0.88\n",
        "---\n",
    ]
    assert lines == expected_lines, (
        f"{SUMMARY_LOG} format is incorrect. Each node's section must be 3 lines, in order, with '---' as separator.\n"
        f"Expected lines:\n{expected_lines}\nGot:\n{lines}"
    )