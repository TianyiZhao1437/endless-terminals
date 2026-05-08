# test_final_state.py

import os
import pytest

EXPERIMENTS_DIR = "/home/user/mlops/experiments"
ARTIFACTS_TXT_PATH = "/home/user/mlops/experiments/artifacts.txt"
ARTIFACT_TYPE_COUNTS_PATH = "/home/user/mlops/experiments/artifact_type_counts.txt"

# The expected output file contents after correct execution
EXPECTED_ARTIFACT_TYPE_COUNTS_CONTENT = (
    "log 2\n"
    "model 5\n"
    "plot 3\n"
)

@pytest.mark.order(1)
def test_output_file_exists():
    assert os.path.isfile(ARTIFACT_TYPE_COUNTS_PATH), (
        f"artifact_type_counts.txt does not exist at {ARTIFACT_TYPE_COUNTS_PATH}. "
        "The required frequency report file was not created."
    )

@pytest.mark.order(2)
def test_output_file_content_is_exact():
    with open(ARTIFACT_TYPE_COUNTS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_ARTIFACT_TYPE_COUNTS_CONTENT, (
        f"artifact_type_counts.txt content is incorrect.\n"
        "Expected content (repr):\n"
        f"{repr(EXPECTED_ARTIFACT_TYPE_COUNTS_CONTENT)}\n"
        "Actual content (repr):\n"
        f"{repr(content)}\n"
        "Each line must be in the format 'artifact_type frequency', sorted alphabetically by artifact_type, "
        "with a single space separator, and no extra text or whitespace."
    )

@pytest.mark.order(3)
def test_output_file_has_no_extra_lines_or_whitespace():
    with open(ARTIFACT_TYPE_COUNTS_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Check no leading/trailing whitespace
    for i, line in enumerate(lines):
        stripped = line.rstrip('\n')
        assert stripped == stripped.strip(), (
            f"Line {i+1} in artifact_type_counts.txt has leading or trailing whitespace: {repr(line)}"
        )
        # Must be a single space separator and exactly two tokens per line
        tokens = stripped.split(' ')
        assert len(tokens) == 2, (
            f"Line {i+1} in artifact_type_counts.txt does not contain exactly two tokens separated by a single space: {repr(line)}"
        )
        artifact_type, freq = tokens
        assert artifact_type in {"log", "model", "plot"}, (
            f"Unexpected artifact_type '{artifact_type}' found in artifact_type_counts.txt."
        )
        assert freq.isdigit(), (
            f"Frequency value '{freq}' in line {i+1} of artifact_type_counts.txt is not an integer."
        )
    # Check number of lines
    assert len(lines) == 3, (
        f"artifact_type_counts.txt should contain exactly 3 lines, one for each artifact type. "
        f"Found {len(lines)} lines."
    )

@pytest.mark.order(4)
def test_output_file_is_not_empty():
    size = os.path.getsize(ARTIFACT_TYPE_COUNTS_PATH)
    assert size > 0, (
        f"artifact_type_counts.txt is empty."
    )