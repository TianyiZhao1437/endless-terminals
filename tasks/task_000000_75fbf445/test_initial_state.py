# test_initial_state.py

import os
import stat
import pytest

HOME = '/home/user'
CLEANUP_SH = os.path.join(HOME, 'cleanup.sh')
SCRIPTS_DIR = os.path.join(HOME, 'scripts')
CLEAN_SYMLINK = os.path.join(SCRIPTS_DIR, 'clean')
SYMLINK_LOG = os.path.join(HOME, 'symlink_check.log')

def test_cleanup_sh_exists_and_executable():
    assert os.path.isfile(CLEANUP_SH), (
        f"Required file {CLEANUP_SH} does not exist. "
        "Please ensure the script exists before starting the task."
    )
    st = os.stat(CLEANUP_SH)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"File {CLEANUP_SH} exists but is not executable. "
        "Please ensure it has execute permissions before starting the task."
    )

def test_scripts_dir_does_not_exist():
    assert not os.path.exists(SCRIPTS_DIR), (
        f"Directory {SCRIPTS_DIR} already exists. "
        "The initial state should not contain this directory."
    )

def test_clean_symlink_does_not_exist():
    assert not os.path.lexists(CLEAN_SYMLINK), (
        f"Symlink or file {CLEAN_SYMLINK} already exists. "
        "The initial state should not contain this symlink or file."
    )

def test_symlink_log_does_not_exist():
    assert not os.path.exists(SYMLINK_LOG), (
        f"Log file {SYMLINK_LOG} already exists. "
        "The initial state should not contain this log file."
    )