# test_final_state.py

import os
import pytest

CLOUD_USAGE_DIR = "/home/user/cloud_usage"
CLOUD_REPORT_LOG = "/home/user/cloud_report.log"

# The expected files in the directory after the task
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
EXPECTED_TXT_COUNT = 3
EXPECTED_LOG_CONTENT = f"Total .txt files: {EXPECTED_TXT_COUNT}"

def test_cloud_usage_directory_still_exists():
    assert os.path.isdir(CLOUD_USAGE_DIR), (
        f"The directory '{CLOUD_USAGE_DIR}' does not exist after task completion. "
        "It must remain present."
    )

@pytest.mark.parametrize("file_path", list(EXPECTED_FILES))
def test_expected_files_still_exist(file_path):
    assert os.path.isfile(file_path), (
        f"The file '{file_path}' is missing in '{CLOUD_USAGE_DIR}' after the task. "
        "All original files must remain present."
    )

def test_txt_files_count_and_presence_final():
    files_in_dir = os.listdir(CLOUD_USAGE_DIR)
    txt_files = {f for f in files_in_dir if f.endswith(".txt")}
    missing_txt_files = EXPECTED_TXT_FILES - txt_files
    extra_txt_files = txt_files - EXPECTED_TXT_FILES

    assert len(txt_files) == EXPECTED_TXT_COUNT, (
        f"Expected exactly {EXPECTED_TXT_COUNT} '.txt' files in '{CLOUD_USAGE_DIR}' after the task, "
        f"but found {len(txt_files)}: {sorted(txt_files)}."
    )

    assert not missing_txt_files, (
        f"The following expected '.txt' files are missing in '{CLOUD_USAGE_DIR}' after the task: {sorted(missing_txt_files)}."
    )

    if extra_txt_files:
        pytest.fail(
            f"Unexpected extra '.txt' files found in '{CLOUD_USAGE_DIR}' after the task: {sorted(extra_txt_files)}. "
            f"Only these should be present: {sorted(EXPECTED_TXT_FILES)}."
        )

def test_cloud_report_log_created_with_correct_content():
    assert os.path.isfile(CLOUD_REPORT_LOG), (
        f"The log file '{CLOUD_REPORT_LOG}' was not created after the task. "
        "It must exist at the specified location."
    )

    try:
        with open(CLOUD_REPORT_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        pytest.fail(f"Could not read '{CLOUD_REPORT_LOG}': {e}")

    assert len(lines) == 1, (
        f"'{CLOUD_REPORT_LOG}' must contain exactly one line, "
        f"but it contains {len(lines)} lines."
    )

    actual_content = lines[0].rstrip("\n")
    assert actual_content == EXPECTED_LOG_CONTENT, (
        f"The content of '{CLOUD_REPORT_LOG}' is incorrect.\n"
        f"Expected: '{EXPECTED_LOG_CONTENT}'\n"
        f"Found:    '{actual_content}'\n"
        "The format must be exactly as specified: 'Total .txt files: <number>' with no extra spaces or lines."
    )