# test_final_state.py

import os
import stat
import pytest

LOG_DIR = "/home/user/iot_deploy_logs"
LOG_FILE = "/home/user/iot_deploy_logs/sensor_agent_pull.log"

EXPECTED_LOG_CONTENT = (
    "Pull Timestamp: 2024-06-01 16:45:39\n"
    "Image Name: iot-sensor-agent:latest\n"
    "Image Digest: sha256:509a2c2e38d5a1c57b28725cbbbb8fbb3d763219c918f84ba2df49926719db8a\n"
)

def test_log_dir_exists_and_is_directory():
    """
    The log directory must exist and be a directory after the task.
    """
    assert os.path.exists(LOG_DIR), (
        f"The directory {LOG_DIR} does not exist after the task. "
        "You must create it before writing the log."
    )
    assert os.path.isdir(LOG_DIR), (
        f"{LOG_DIR} exists but is not a directory. "
        "It must be a directory to store the log file."
    )

def test_log_dir_is_writeable_by_user():
    """
    The log directory must be writeable by the user after the task.
    """
    # Check write permission for the current user
    assert os.access(LOG_DIR, os.W_OK), (
        f"The directory {LOG_DIR} exists but is not writeable by the current user. "
        "Ensure the permissions allow writing."
    )

def test_log_file_exists():
    """
    The log file must exist after the task is completed.
    """
    assert os.path.exists(LOG_FILE), (
        f"The log file {LOG_FILE} does not exist after the task. "
        "You must create this file after pulling the image."
    )
    assert os.path.isfile(LOG_FILE), (
        f"{LOG_FILE} exists but is not a regular file. "
        "It must be a regular file containing the log entry."
    )

def test_log_file_content_exact_match():
    """
    The log file content must exactly match the expected format and values.
    """
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == EXPECTED_LOG_CONTENT, (
        f"The log file {LOG_FILE} does not contain the expected content.\n"
        "Expected:\n"
        f"{EXPECTED_LOG_CONTENT!r}\n"
        "Found:\n"
        f"{content!r}\n"
        "Please ensure the log entry is EXACTLY as specified, with correct timestamp, image name, digest, and format."
    )

def test_log_file_has_single_log_entry():
    """
    The log file must contain exactly 3 lines (one complete log entry).
    """
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 3, (
        f"The log file {LOG_FILE} should contain exactly 3 lines (one log entry), "
        f"but it contains {len(lines)} lines.\n"
        "Each field must be on its own line."
    )
    # Check for trailing newline at end of file
    assert lines[-1].endswith('\n'), (
        f"The last line of {LOG_FILE} must end with a newline character."
    )

def test_no_extra_files_in_log_dir():
    """
    No extra files or directories should be created in the log directory.
    """
    files = os.listdir(LOG_DIR)
    assert files == ['sensor_agent_pull.log'], (
        f"The directory {LOG_DIR} contains unexpected files or directories: {files}. "
        "Only 'sensor_agent_pull.log' should be present."
    )