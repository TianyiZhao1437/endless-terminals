# test_final_state.py

import os
import pytest

JENKINS_LOG_PATH = "/home/user/cicd/logs/jenkins_pipeline.log"
REPORTS_DIR_PATH = "/home/user/cicd/reports"
SLOW_REPORT_PATH = "/home/user/cicd/reports/slow_steps_report.txt"

EXPECTED_REPORT_CONTENT = "build,7\ndeploy,9"

def test_reports_dir_still_exists_and_writable():
    assert os.path.isdir(REPORTS_DIR_PATH), (
        f"Reports directory {REPORTS_DIR_PATH} is missing after the task. "
        "It must exist for report generation."
    )
    assert os.access(REPORTS_DIR_PATH, os.W_OK), (
        f"Reports directory {REPORTS_DIR_PATH} is not writable. "
        "It must be writable for the report file."
    )

def test_jenkins_log_file_unchanged():
    """
    Ensure the log file still exists and is unmodified.
    """
    assert os.path.isfile(JENKINS_LOG_PATH), (
        f"Jenkins pipeline log file {JENKINS_LOG_PATH} is missing after the task."
    )
    expected_content = (
        "Step: build | Started: 2024-06-05T10:01:44 | Ended: 2024-06-05T10:01:51 | Duration: 7\n"
        "Step: test | Started: 2024-06-05T10:02:00 | Ended: 2024-06-05T10:02:01 | Duration: 1\n"
        "Step: deploy | Started: 2024-06-05T10:02:30 | Ended: 2024-06-05T10:02:39 | Duration: 9\n"
        "Step: post-cleanup | Started: 2024-06-05T10:03:01 | Ended: 2024-06-05T10:03:03 | Duration: 2\n"
    )
    with open(JENKINS_LOG_PATH, "r") as f:
        content = f.read()
    normalized_actual = content.replace('\r\n', '\n').strip()
    normalized_expected = expected_content.strip()
    assert normalized_actual == normalized_expected, (
        f"The Jenkins log file at {JENKINS_LOG_PATH} was modified during the task.\n"
        "Expected content:\n"
        f"{normalized_expected}\n"
        "Actual content:\n"
        f"{normalized_actual}"
    )

def test_slow_steps_report_file_exists():
    assert os.path.isfile(SLOW_REPORT_PATH), (
        f"Expected summary report file {SLOW_REPORT_PATH} was not created.\n"
        "You must create this file as part of your solution."
    )

def test_slow_steps_report_content_exact():
    with open(SLOW_REPORT_PATH, "r") as f:
        content = f.read()
    # Normalize line endings for comparison
    normalized_actual = content.replace('\r\n', '\n').strip()
    normalized_expected = EXPECTED_REPORT_CONTENT.strip()
    assert normalized_actual == normalized_expected, (
        f"The report file {SLOW_REPORT_PATH} does not contain the correct summary of slow steps.\n"
        "Expected content:\n"
        f"{normalized_expected}\n"
        "Actual content:\n"
        f"{normalized_actual}\n"
        "The report must list each slow step (duration > 5 seconds) as <step_name>,<duration_in_seconds> on a separate line, "
        "with no extra lines or characters."
    )

def test_slow_steps_report_is_plain_text():
    """
    Ensure the report file is plain text and readable by 'cat'.
    """
    try:
        with open(SLOW_REPORT_PATH, "r") as f:
            f.read()
    except Exception as e:
        pytest.fail(f"The report file {SLOW_REPORT_PATH} is not plain text or not readable: {e}")