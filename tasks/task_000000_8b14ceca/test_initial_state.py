# test_initial_state.py

import os
import stat
import pwd
import pytest

PIPELINE_UTIL_DIR = "/home/user/pipeline_util"
NUMBERS_TXT = os.path.join(PIPELINE_UTIL_DIR, "numbers.txt")
PROCESS_SH = os.path.join(PIPELINE_UTIL_DIR, "process_numbers.sh")
PIPELINE_LOG = os.path.join(PIPELINE_UTIL_DIR, "pipeline_test.log")
USER = "user"


def test_pipeline_util_directory_exists():
    assert os.path.isdir(PIPELINE_UTIL_DIR), (
        f"Required directory does not exist: {PIPELINE_UTIL_DIR}"
    )


def test_numbers_txt_exists_and_contents():
    assert os.path.isfile(NUMBERS_TXT), (
        f"Required file does not exist: {NUMBERS_TXT}"
    )
    with open(NUMBERS_TXT, "r") as f:
        contents = f.read()
    expected = "3\n7\nnotanumber\n9\n"
    assert contents == expected, (
        f"File {NUMBERS_TXT} does not have the expected contents.\n"
        f"Expected:\n{repr(expected)}\nGot:\n{repr(contents)}"
    )


def test_process_numbers_sh_not_present_yet():
    """
    The process_numbers.sh script should NOT exist before the student performs the action.
    """
    assert not os.path.exists(PROCESS_SH), (
        f"The script {PROCESS_SH} should NOT exist before you start the task."
    )


def test_pipeline_test_log_not_present_yet():
    """
    The pipeline_test.log should NOT exist before the student performs the action.
    """
    assert not os.path.exists(PIPELINE_LOG), (
        f"The log file {PIPELINE_LOG} should NOT exist before you start the task."
    )