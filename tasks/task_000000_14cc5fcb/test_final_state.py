# test_final_state.py

import os
import pytest
import socket

HOME = "/home/user"
WEBSERVER_DIR = os.path.join(HOME, "test_webserver")
STATUS_FILE = os.path.join(WEBSERVER_DIR, "status.txt")
LOG_FILE = os.path.join(HOME, "webserver_test.log")
EXPECTED_CONTENT = "Server Status: Online\n"

def test_webserver_directory_exists_and_has_correct_contents():
    """
    Validate that /home/user/test_webserver exists and contains only status.txt with exact content.
    """
    assert os.path.isdir(WEBSERVER_DIR), (
        f"Directory {WEBSERVER_DIR} does not exist. "
        f"Did you create it as required?"
    )
    contents = os.listdir(WEBSERVER_DIR)
    assert contents == ["status.txt"], (
        f"{WEBSERVER_DIR} should contain only 'status.txt', but contains: {contents}"
    )
    assert os.path.isfile(STATUS_FILE), (
        f"File {STATUS_FILE} does not exist."
    )
    with open(STATUS_FILE, 'r', encoding='utf-8') as f:
        status = f.read()
    assert status == EXPECTED_CONTENT, (
        f"{STATUS_FILE} does not have the exact required content.\n"
        f"Expected: {repr(EXPECTED_CONTENT)}\n"
        f"Actual:   {repr(status)}"
    )

def test_log_file_exists_and_has_correct_content():
    """
    Validate that /home/user/webserver_test.log exists and contains only the status.txt body, with a newline.
    """
    assert os.path.isfile(LOG_FILE), (
        f"Log file {LOG_FILE} does not exist."
    )
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        log = f.read()
    assert log == EXPECTED_CONTENT, (
        f"{LOG_FILE} does not match the expected output.\n"
        f"Expected: {repr(EXPECTED_CONTENT)}\n"
        f"Actual:   {repr(log)}"
    )

def test_no_extra_files_in_webserver_dir():
    """
    Ensure /home/user/test_webserver contains only status.txt.
    """
    contents = os.listdir(WEBSERVER_DIR)
    assert contents == ["status.txt"], (
        f"Extra files found in {WEBSERVER_DIR}: {contents}. "
        f"Only 'status.txt' should be present."
    )

def test_server_not_running_on_port_8080():
    """
    Validate that HTTP server was stopped after verification, and port 8080 is not listening.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex(("127.0.0.1", 8080))
        assert result != 0, (
            "The HTTP server is still running on port 8080. "
            "It should have been stopped after verification."
        )
    finally:
        sock.close()

@pytest.mark.parametrize("path", [
    WEBSERVER_DIR,
    STATUS_FILE,
    LOG_FILE,
])
def test_absolute_paths_exist(path):
    """
    Ensure all required absolute paths exist.
    """
    assert os.path.exists(path), (
        f"Required path does not exist: {path}"
    )