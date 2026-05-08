# test_final_state.py

import os
import stat
import pwd
import grp
import pytest
import subprocess

ETL_LOGS_DIR = '/home/user/etl_logs'
PERMISSIONS_CHECK_LOG = '/home/user/permissions_check.log'


def get_ls_ld_line(path):
    """
    Returns the output line of `ls -ld <path>` as a string,
    stripped of trailing newlines.
    """
    try:
        result = subprocess.run(
            ['ls', '-ld', path],
            capture_output=True, text=True, check=True
        )
        # Remove trailing newline, but do not strip spaces within the line.
        return result.stdout.rstrip('\n')
    except Exception as e:
        pytest.fail(f"Failed to run 'ls -ld {path}': {e}")


def test_etl_logs_dir_permissions_700_and_owner():
    """
    The /home/user/etl_logs directory must exist, be a directory,
    have permissions 700 (drwx------), and be owned by user 'user'.
    Group ownership must not have changed from before.
    """
    assert os.path.exists(ETL_LOGS_DIR), (
        f"Directory {ETL_LOGS_DIR} does not exist. "
        "It must exist after completing the task."
    )
    assert os.path.isdir(ETL_LOGS_DIR), (
        f"{ETL_LOGS_DIR} exists but is not a directory."
    )

    st = os.stat(ETL_LOGS_DIR)
    mode = stat.S_IMODE(st.st_mode)
    uid = st.st_uid
    gid = st.st_gid
    username = pwd.getpwuid(uid).pw_name
    groupname = grp.getgrgid(gid).gr_name

    assert mode == 0o700, (
        f"{ETL_LOGS_DIR} permissions are {oct(mode)} "
        f"(should be 0o700, drwx------). "
        "Only the owner must have read, write, and execute permissions."
    )
    assert username == 'user', (
        f"{ETL_LOGS_DIR} is owned by '{username}', but should be owned by 'user'."
    )
    # The group must not have changed from the initial state, but since we don't have
    # initial group here, we recommend the group is still 'user' or whatever it was.
    # If you want to lock this stricter, you can capture the initial group in a fixture.


def test_permissions_check_log_exists_and_content():
    """
    /home/user/permissions_check.log must exist, be readable,
    and contain only the output line of `ls -ld /home/user/etl_logs`
    reflecting the current state (after chmod 700).
    """
    assert os.path.exists(PERMISSIONS_CHECK_LOG), (
        f"{PERMISSIONS_CHECK_LOG} does not exist. "
        "You must create this file containing the output of 'ls -ld /home/user/etl_logs'."
    )
    assert os.path.isfile(PERMISSIONS_CHECK_LOG), (
        f"{PERMISSIONS_CHECK_LOG} exists but is not a regular file."
    )

    # Read the contents of the log file
    with open(PERMISSIONS_CHECK_LOG, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 1, (
        f"{PERMISSIONS_CHECK_LOG} should contain exactly one line, "
        f"but has {len(lines)} lines."
    )

    log_line = lines[0].rstrip('\n')
    expected_ls_ld = get_ls_ld_line(ETL_LOGS_DIR)

    assert log_line == expected_ls_ld, (
        f"Content of {PERMISSIONS_CHECK_LOG} does not match the expected 'ls -ld' output.\n"
        f"Expected:\n{expected_ls_ld}\n"
        f"Found:\n{log_line}\n"
        "Make sure you run 'ls -ld /home/user/etl_logs' AFTER setting permissions, "
        "and write only that line to the log file (no extra lines)."
    )


def test_permissions_check_log_no_extra_lines():
    """
    Ensure /home/user/permissions_check.log does not have extra blank lines.
    """
    with open(PERMISSIONS_CHECK_LOG, 'rb') as f:
        content = f.read()
    # Should not end with two newlines
    assert not content.endswith(b'\n\n'), (
        f"{PERMISSIONS_CHECK_LOG} contains extra blank line(s) at the end. "
        "There should be only one line, and no trailing blank lines."
    )