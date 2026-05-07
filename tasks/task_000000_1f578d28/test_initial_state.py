# test_initial_state.py

import os
import pytest

JENKINS_LOG_PATH = "/home/user/cicd/logs/jenkins_pipeline.log"
REPORTS_DIR_PATH = "/home/user/cicd/reports"
SLOW_REPORT_PATH = "/home/user/cicd/reports/slow_steps_report.txt"

JENKINS_LOG_CONTENT = """Step: build | Started: 2024-06-05T10:01:44 | Ended: 2024-06-05T10:01:51 | Duration: 7
Step: test | Started: 2024-06-05T10:02:00 | Ended: 2024-06-05T10:02:01 | Duration: 1
Step: deploy | Started: 2024-06-05T10:02:30 | Ended: 2024-06-05T10:02:39 | Duration: 9
Step: post-cleanup | Started: 2024-06-05T10:03:01 | Ended: 2024-06-05T10:03:03 | Duration: 2
"""

@pytest.mark.parametrize("path", [
    JENKINS_LOG_PATH,
])
def test_jenkins_log_file_exists(path):
    assert os.path.isfile(path), (
        f"Missing required log file: {path}. "
        "Ensure that the Jenkins pipeline log file exists before proceeding."
    )

def test_jenkins_log_file_content():
    with open(JENKINS_LOG_PATH, "r") as f:
        content = f.read()
    # Normalize line endings for comparison
    normalized_actual = content.replace('\r\n', '\n').strip()
    normalized_expected = JENKINS_LOG_CONTENT.strip()
    assert normalized_actual == normalized_expected, (
        f"The log file at {JENKINS_LOG_PATH} does not contain the expected pipeline log entries.\n"
        "Expected content:\n"
        f"{normalized_expected}\n"
        "Actual content:\n"
        f"{normalized_actual}\n"
        "Please ensure the log file is correct before proceeding."
    )

@pytest.mark.parametrize("path", [
    REPORTS_DIR_PATH,
])
def test_reports_dir_exists_and_writable(path):
    assert os.path.isdir(path), (
        f"Missing reports directory: {path}. "
        "Ensure that /home/user/cicd/reports/ exists before proceeding."
    )
    assert os.access(path, os.W_OK), (
        f"Reports directory {path} is not writable. "
        "Ensure that the agent has write permissions to this directory."
    )

def test_slow_steps_report_file_does_not_exist():
    assert not os.path.exists(SLOW_REPORT_PATH), (
        f"The summary report file {SLOW_REPORT_PATH} already exists. "
        "This file should NOT exist before you start the task."
    )