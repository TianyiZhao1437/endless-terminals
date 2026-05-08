# test_initial_state.py

import os
import pytest

CERT_LOGS_DIR = "/home/user/cert_logs"
LOG1 = os.path.join(CERT_LOGS_DIR, "cert_activity_01.log")
LOG2 = os.path.join(CERT_LOGS_DIR, "cert_activity_02.log")

@pytest.mark.parametrize("path", [
    CERT_LOGS_DIR,
])
def test_cert_logs_directory_exists(path):
    assert os.path.isdir(path), (
        f"Required directory '{path}' does not exist. "
        "Please ensure it is present before starting the task."
    )

@pytest.mark.parametrize("path,expected_lines", [
    (
        LOG1,
        [
            "2024-06-01T10:12:54Z alice self-signed",
            "2024-06-01T11:30:02Z carol ca-signed",
            "2024-06-02T08:07:23Z bob self-signed"
        ]
    ),
    (
        LOG2,
        [
            "2024-06-03T12:04:12Z eve self-signed",
            "2024-06-02T13:15:58Z dan ca-signed",
            "2024-06-02T20:09:40Z frank self-signed"
        ]
    ),
])
def test_cert_activity_logs_exist_and_content(path, expected_lines):
    assert os.path.isfile(path), (
        f"Required log file '{path}' does not exist. "
        "Please ensure it is present before starting the task."
    )
    with open(path, 'r', encoding='utf-8') as f:
        actual_lines = [line.rstrip('\n') for line in f.readlines()]
    assert actual_lines == expected_lines, (
        f"Log file '{path}' does not contain the expected lines.\n"
        f"Expected:\n{expected_lines}\n"
        f"Actual:\n{actual_lines}\n"
        "Please restore the original log file contents before starting the task."
    )

@pytest.mark.parametrize("output_path", [
    os.path.join(CERT_LOGS_DIR, "self_signed_summary.log"),
])
def test_output_file_does_not_exist_yet(output_path):
    assert not os.path.exists(output_path), (
        f"The output file '{output_path}' already exists. "
        "Please remove it before starting the task."
    )