# test_final_state.py

import os
import zipfile
import pytest

HOME = "/home/user"
BILLING_REPORTS_DIR = os.path.join(HOME, "billing_reports")
ARCHIVE_PATH = os.path.join(HOME, "cloud_costs_archive.zip")
EXTRACTED_REPORTS_DIR = os.path.join(HOME, "extracted_reports")
LOG_PATH = os.path.join(HOME, "finops_archive_log.txt")

EXPECTED_CSV_FILES = [
    "cloud_june.csv",
    "cloud_may.csv",
]
# Sorted order as per requirements
EXPECTED_CSV_FILES_SORTED = sorted(EXPECTED_CSV_FILES)


def test_archive_exists_and_is_zip():
    assert os.path.isfile(ARCHIVE_PATH), (
        f"Archive file missing: {ARCHIVE_PATH}\n"
        "You must create the zip archive named 'cloud_costs_archive.zip' in /home/user."
    )
    # Check that it's a valid zip file
    assert zipfile.is_zipfile(ARCHIVE_PATH), (
        f"The file at {ARCHIVE_PATH} is not a valid zip archive."
    )


def test_archive_contains_expected_csv_files():
    with zipfile.ZipFile(ARCHIVE_PATH, "r") as zf:
        zip_names = sorted(zf.namelist())
        assert zip_names == EXPECTED_CSV_FILES_SORTED, (
            f"The zip archive must contain these files (sorted): {EXPECTED_CSV_FILES_SORTED},\n"
            f"but it contains: {zip_names}."
        )


def test_extracted_reports_directory_exists():
    assert os.path.isdir(EXTRACTED_REPORTS_DIR), (
        f"Extracted reports directory missing: {EXTRACTED_REPORTS_DIR}\n"
        "You must extract the archive into /home/user/extracted_reports."
    )


@pytest.mark.parametrize("csv_file", EXPECTED_CSV_FILES_SORTED)
def test_extracted_csv_files_exist(csv_file):
    extracted_path = os.path.join(EXTRACTED_REPORTS_DIR, csv_file)
    assert os.path.isfile(extracted_path), (
        f"Extracted file missing: {extracted_path}\n"
        "You must extract all CSV files from the archive into /home/user/extracted_reports."
    )


def test_log_file_exists():
    assert os.path.isfile(LOG_PATH), (
        f"Log file missing: {LOG_PATH}\n"
        "You must create the log file at /home/user/finops_archive_log.txt after extraction."
    )


def test_log_file_contents_are_correct():
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        contents = f.read()
    expected_lines = [
        "Compressed files:",
    ]
    for name in EXPECTED_CSV_FILES_SORTED:
        expected_lines.append(f"- {name}")
    expected_lines.append("")
    expected_lines.append("Extraction output directory:")
    expected_lines.append(f"- {EXTRACTED_REPORTS_DIR}")
    expected_contents = "\n".join(expected_lines)
    assert contents == expected_contents, (
        "The log file contents are incorrect.\n"
        "Expected log file contents (exactly):\n"
        f"{expected_contents!r}\n"
        "But got:\n"
        f"{contents!r}\n"
        "Ensure you follow the required format, including order, indentation, blank lines, and directory path."
    )