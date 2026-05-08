# test_initial_state.py

import os
import pytest

RAW_DATASET_PATH = "/home/user/data/raw_dataset.csv"
CLEANED_DATASET_PATH = "/home/user/data/cleaned_dataset.csv"
SCRIPT_PATH = "/home/user/data/clean_csv.sh"
DATA_DIR = "/home/user/data"

EXPECTED_RAW_DATASET_CONTENT = (
    "Name,Age,Occupation\n"
    "Alice,30,Data Scientist\n"
    "Bob,,Analyst\n"
    ",25,Engineer\n"
    "Charlie,22,\n"
    "David,28,Developer\n"
)

def test_data_directory_exists():
    assert os.path.isdir(DATA_DIR), (
        f"Expected data directory '{DATA_DIR}' does not exist."
    )

def test_raw_dataset_exists():
    assert os.path.isfile(RAW_DATASET_PATH), (
        f"Expected raw CSV file '{RAW_DATASET_PATH}' does not exist."
    )

def test_raw_dataset_content():
    with open(RAW_DATASET_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Normalize possible trailing newlines for comparison
    actual_lines = content.strip().splitlines()
    expected_lines = EXPECTED_RAW_DATASET_CONTENT.strip().splitlines()
    assert actual_lines == expected_lines, (
        f"'{RAW_DATASET_PATH}' does not have the expected content.\n"
        f"Expected:\n{EXPECTED_RAW_DATASET_CONTENT}\n"
        f"Actual:\n{content}"
    )

def test_cleaned_dataset_does_not_exist_yet():
    assert not os.path.exists(CLEANED_DATASET_PATH), (
        f"'{CLEANED_DATASET_PATH}' should not exist before the cleaning script is run."
    )

def test_clean_csv_script_does_not_exist_yet():
    assert not os.path.exists(SCRIPT_PATH), (
        f"'{SCRIPT_PATH}' should not exist before the student writes the cleaning script."
    )