# test_initial_state.py

import os
import pytest

CLOUD_USAGE_DIR = "/home/user/cloud_usage"
CLOUD_REPORT_LOG = "/home/user/cloud_report.log"
EXPECTED_FILES = {
    "/home/user/cloud_usage/report_2024-06-01.txt",
    "/home/user/cloud_usage/report_2024-06-02.txt",
    "/home/user/cloud_usage/report_2024-06-03.csv",
    "/home/user/cloud_usage/metadata.json",
    "/home/user/cloud_usage/report_2024-06-04.txt",
    "/home/user/cloud_usage/readme.md",
}
EXPECTED_TXT_FILES = {
    "report_2024-06-01.txt",
    "report_2024-06-02.txt",
    "report_2024-06-04.txt",
}


def test_cloud_usage_directory_exists():
    assert os.path.isdir(CLOUD_USAGE_DIR), (
        f"The directory '{CLOUD_USAGE_DIR}' does not exist. "
        "It must exist before you start the task."
    )


@pytest.mark.parametrize("file_path", list(EXPECTED_FILES))
def test_expected_files_exist(file_path):
    assert os.path.isfile(file_path), (
        f"The file '{file_path}' is missing in '{CLOUD_USAGE_DIR}'. "
        "It must exist before you start the task."
    )


def test_txt_files_count_and_presence():
    files_in_dir = os.listdir(CLOUD_USAGE_DIR)
    txt_files = {f for f in files_in_dir if f.endswith(".txt")}
    missing_txt_files = EXPECTED_TXT_FILES - txt_files
    extra_txt_files = txt_files - EXPECTED_TXT_FILES

    assert len(txt_files) == 3, (
        f"Expected exactly 3 '.txt' files in '{CLOUD_USAGE_DIR}', "
        f"but found {len(txt_files)}: {sorted(txt_files)}."
    )

    assert not missing_txt_files, (
        f"The following expected '.txt' files are missing in '{CLOUD_USAGE_DIR}': {sorted(missing_txt_files)}."
    )

    # Allow extra .txt files (in case), but warn if present
    if extra_txt_files:
        pytest.skip(
            f"Warning: Extra '.txt' files found in '{CLOUD_USAGE_DIR}': {sorted(extra_txt_files)}. "
            "Only 3 specific '.txt' files should be present."
        )


def test_cloud_report_log_does_not_exist():
    assert not os.path.exists(CLOUD_REPORT_LOG), (
        f"The log file '{CLOUD_REPORT_LOG}' already exists. "
        "It should NOT exist before the task; it must be created by the agent."
    )