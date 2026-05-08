# test_initial_state.py

import os
import pytest

DATASET_DIR = "/home/user/projects/cleaning/datasets"
DATASET_FILE = "/home/user/projects/cleaning/datasets/iris.csv"
OUTPUT_FILE = "/home/user/cleaning_envvar_output.txt"

def test_dataset_dir_exists():
    assert os.path.isdir(DATASET_DIR), (
        f"Required directory does not exist: {DATASET_DIR}"
    )

def test_dataset_file_exists_and_readable():
    assert os.path.isfile(DATASET_FILE), (
        f"Required file does not exist: {DATASET_FILE}"
    )
    assert os.access(DATASET_FILE, os.R_OK), (
        f"Required file is not readable: {DATASET_FILE}"
    )

def test_output_file_does_not_exist():
    assert not os.path.exists(OUTPUT_FILE), (
        f"File {OUTPUT_FILE} should NOT exist before you perform the task."
    )