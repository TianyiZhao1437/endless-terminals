# test_final_state.py

import os
import stat
import pytest

HOME = '/home/user'
CLEANUP_SH = os.path.join(HOME, 'cleanup.sh')
SCRIPTS_DIR = os.path.join(HOME, 'scripts')
CLEAN_SYMLINK = os.path.join(SCRIPTS_DIR, 'clean')
SYMLINK_LOG = os.path.join(HOME, 'symlink_check.log')

def test_scripts_dir_exists_and_is_dir():
    assert os.path.exists(SCRIPTS_DIR), (
        f"Directory {SCRIPTS_DIR} does not exist. "
        "You must create the directory for symlink management."
    )
    assert os.path.isdir(SCRIPTS_DIR), (
        f"{SCRIPTS_DIR} exists but is not a directory. "
        "Ensure it is a directory, not a file or symlink."
    )

def test_cleanup_sh_exists_and_executable():
    assert os.path.isfile(CLEANUP_SH), (
        f"Script file {CLEANUP_SH} is missing after task completion. "
        "Do not remove or rename this file."
    )
    st = os.stat(CLEANUP_SH)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, (
        f"Script file {CLEANUP_SH} exists but is not executable. "
        "Ensure it retains execute permissions after your changes."
    )

def test_clean_symlink_exists_and_points_correctly():
    assert os.path.lexists(CLEAN_SYMLINK), (
        f"Symlink {CLEAN_SYMLINK} does not exist. "
        "You must create this symlink as part of the task."
    )
    assert os.path.islink(CLEAN_SYMLINK), (
        f"{CLEAN_SYMLINK} exists but is not a symlink. "
        "Remove any file or directory and create a symlink instead."
    )
    target = os.readlink(CLEAN_SYMLINK)
    # Resolve relative symlink to absolute path, for comparison
    if not os.path.isabs(target):
        abs_target = os.path.abspath(os.path.join(os.path.dirname(CLEAN_SYMLINK), target))
    else:
        abs_target = target
    assert abs_target == CLEANUP_SH, (
        f"Symlink {CLEAN_SYMLINK} points to {abs_target!r} instead of {CLEANUP_SH!r}. "
        "Update the symlink to point to the correct script."
    )

def test_symlink_log_exists_and_correct_content():
    assert os.path.isfile(SYMLINK_LOG), (
        f"Log file {SYMLINK_LOG} is missing. "
        "You must generate this log file as specified."
    )
    with open(SYMLINK_LOG, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    expected_lines = [
        "Symbolic link exists: YES",
        f"Symlink target: {CLEANUP_SH}",
    ]
    assert lines == expected_lines, (
        f"Log file {SYMLINK_LOG} content is incorrect.\n"
        f"Expected:\n{expected_lines!r}\n"
        f"Actual:\n{lines!r}\n"
        "Ensure the log file contains exactly two lines, in order, with no extra spaces or blank lines."
    )