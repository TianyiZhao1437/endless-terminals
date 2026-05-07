# test_initial_state.py

import os
import pytest

HOME = "/home/user"
WEBSERVER_DIR = os.path.join(HOME, "test_webserver")
STATUS_FILE = os.path.join(WEBSERVER_DIR, "status.txt")
LOG_FILE = os.path.join(HOME, "webserver_test.log")

def test_webserver_directory_does_not_exist():
    """
    Before the student starts, /home/user/test_webserver must not exist.
    """
    assert not os.path.exists(WEBSERVER_DIR), (
        f"Directory {WEBSERVER_DIR} already exists. "
        f"Please remove it before beginning the task."
    )

def test_status_file_does_not_exist():
    """
    Before the student starts, /home/user/test_webserver/status.txt must not exist.
    """
    assert not os.path.exists(STATUS_FILE), (
        f"File {STATUS_FILE} already exists. "
        f"Please remove it before beginning the task."
    )

def test_log_file_does_not_exist():
    """
    Before the student starts, /home/user/webserver_test.log must not exist.
    """
    assert not os.path.exists(LOG_FILE), (
        f"File {LOG_FILE} already exists. "
        f"Please remove it before beginning the task."
    )