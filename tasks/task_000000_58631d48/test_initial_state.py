# test_initial_state.py

import os
import pytest

HOME = "/home/user"
BILLING_REPORTS_DIR = os.path.join(HOME, "billing_reports")
EXPECTED_CSV_FILES = [
    os.path.join(BILLING_REPORTS_DIR, "cloud_june.csv"),
    os.path.join(BILLING_REPORTS_DIR, "cloud_may.csv"),
]

@pytest.mark.parametrize("filepath", EXPECTED_CSV_FILES)
def test_billing_reports_csv_files_exist(filepath):
    assert os.path.isfile(filepath), (
        f"Required CSV file missing: {filepath}\n"
        "Please ensure the initial billing report files are present at the specified paths."
    )

def test_billing_reports_directory_exists():
    assert os.path.isdir(BILLING_REPORTS_DIR), (
        f"Required directory missing: {BILLING_REPORTS_DIR}\n"
        "Please ensure /home/user/billing_reports exists before proceeding."
    )

def test_no_archive_exists_yet():
    archive_path = os.path.join(HOME, "cloud_costs_archive.zip")
    assert not os.path.exists(archive_path), (
        f"Archive file already exists: {archive_path}\n"
        "The archive file should NOT exist before you start the task."
    )

def test_no_extracted_reports_directory_yet():
    extracted_dir = os.path.join(HOME, "extracted_reports")
    assert not os.path.exists(extracted_dir), (
        f"Extracted reports directory already exists: {extracted_dir}\n"
        "The extracted_reports directory should NOT exist before you start the task."
    )

def test_no_log_file_yet():
    log_path = os.path.join(HOME, "finops_archive_log.txt")
    assert not os.path.exists(log_path), (
        f"Log file already exists: {log_path}\n"
        "The log file should NOT exist before you start the task."
    )