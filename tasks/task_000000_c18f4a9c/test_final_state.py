# test_final_state.py

import os
import stat
import pytest

DATA_DIR = "/home/user/data"
RAW_DATASET_PATH = "/home/user/data/raw_dataset.csv"
CLEANED_DATASET_PATH = "/home/user/data/cleaned_dataset.csv"
SCRIPT_PATH = "/home/user/data/clean_csv.sh"

EXPECTED_CLEANED_CONTENT = (
    "Name,Age,Occupation\n"
    "Alice,30,Data Scientist\n"
)

EXPECTED_LISTING = {"clean_csv.sh", "cleaned_dataset.csv", "raw_dataset.csv"}

def test_data_directory_exists():
    assert os.path.isdir(DATA_DIR), (
        f"Expected data directory '{DATA_DIR}' does not exist."
    )

def test_clean_csv_script_exists_and_is_file():
    assert os.path.isfile(SCRIPT_PATH), (
        f"Expected script '{SCRIPT_PATH}' does not exist or is not a file."
    )

def test_clean_csv_script_is_executable():
    mode = os.stat(SCRIPT_PATH).st_mode
    is_executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"Script '{SCRIPT_PATH}' exists but is not executable. "
        f"Please ensure it has execute permissions (chmod +x)."
    )

def test_cleaned_dataset_exists_and_is_file():
    assert os.path.isfile(CLEANED_DATASET_PATH), (
        f"Expected cleaned CSV file '{CLEANED_DATASET_PATH}' does not exist."
    )

def test_cleaned_dataset_content_exact():
    with open(CLEANED_DATASET_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Normalize newlines for comparison
    actual_lines = content.strip().splitlines()
    expected_lines = EXPECTED_CLEANED_CONTENT.strip().splitlines()
    assert actual_lines == expected_lines, (
        f"'{CLEANED_DATASET_PATH}' does not have the expected cleaned content.\n"
        f"Expected:\n{EXPECTED_CLEANED_CONTENT}\n"
        f"Actual:\n{content}"
    )

def test_cleaned_dataset_no_extra_blank_lines():
    with open(CLEANED_DATASET_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # There should not be extra blank lines at the end
    lines = content.splitlines()
    assert all(line.strip() != "" for line in lines), (
        f"'{CLEANED_DATASET_PATH}' contains extra blank lines."
    )

def test_data_directory_listing():
    actual_listing = set(os.listdir(DATA_DIR))
    missing = EXPECTED_LISTING - actual_listing
    assert not missing, (
        f"The following expected files are missing from '{DATA_DIR}': {missing}\n"
        f"Actual directory contents: {sorted(actual_listing)}"
    )
    # Also check there are no unexpected extra files with similar names
    for expected in EXPECTED_LISTING:
        assert expected in actual_listing, (
            f"Expected file '{expected}' not found in '{DATA_DIR}'."
        )

def test_script_does_not_modify_other_files(tmp_path):
    # Only the three files should be present, or if extra files exist, they must not be named like the expected outputs
    allowed_files = EXPECTED_LISTING
    actual_listing = set(os.listdir(DATA_DIR))
    suspicious = [f for f in actual_listing if f not in allowed_files and f.endswith('.csv')]
    assert not suspicious, (
        f"Unexpected CSV files found in '{DATA_DIR}': {suspicious}.\n"
        "The script should not create or modify extra files."
    )

def test_cleaned_dataset_printed_to_console_matches(monkeypatch, capsys):
    # Simulate the expected print to console (since we can't capture real terminal output here,
    # we simulate by reading and printing the file, as a student would do with 'cat')
    with open(CLEANED_DATASET_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    print(content, end="")  # end="" to avoid adding extra newline
    captured = capsys.readouterr().out
    # Remove possible trailing newlines for robust comparison
    assert captured.strip() == EXPECTED_CLEANED_CONTENT.strip(), (
        "The printed output of 'cleaned_dataset.csv' does not match the expected cleaned content.\n"
        f"Expected printed content:\n{EXPECTED_CLEANED_CONTENT}\n"
        f"Actual printed content:\n{captured}"
    )