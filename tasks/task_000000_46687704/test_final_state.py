# test_final_state.py

import os
import pytest

DATASET_PATH_VAR = "DATASET_PATH"
EXPECTED_DATASET_PATH = "/home/user/projects/cleaning/datasets/iris.csv"
OUTPUT_FILE = "/home/user/cleaning_envvar_output.txt"

def test_dataset_path_envvar_set():
    value = os.environ.get(DATASET_PATH_VAR)
    assert value is not None, (
        f"Environment variable {DATASET_PATH_VAR} is not set in the current shell environment."
    )
    assert value == EXPECTED_DATASET_PATH, (
        f"Environment variable {DATASET_PATH_VAR} is set to '{value}', "
        f"but expected value is '{EXPECTED_DATASET_PATH}'."
    )

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), (
        f"File {OUTPUT_FILE} does not exist. "
        f"You must create this file by redirecting the output of 'echo ${DATASET_PATH_VAR}'."
    )

def test_output_file_content_exact():
    try:
        with open(OUTPUT_FILE, "rb") as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Could not open {OUTPUT_FILE} for reading: {e}")

    expected_bytes = EXPECTED_DATASET_PATH.encode("utf-8")
    assert content == expected_bytes, (
        f"Contents of {OUTPUT_FILE} are not exactly correct.\n"
        f"Expected: {repr(EXPECTED_DATASET_PATH)}\n"
        f"Actual:   {repr(content.decode('utf-8', errors='replace'))}\n"
        f"File must contain exactly one line with no extra whitespace or newline characters."
    )