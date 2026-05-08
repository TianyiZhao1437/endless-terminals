# test_initial_state.py

import os
import stat
import pwd
import grp
import pytest

ETL_LOGS_DIR = '/home/user/etl_logs'
PERMISSIONS_CHECK_LOG = '/home/user/permissions_check.log'

def test_etl_logs_directory_exists_and_owned_by_user():
    """Check that /home/user/etl_logs exists and is a directory owned by user 'user'."""
    assert os.path.exists(ETL_LOGS_DIR), (
        f"Missing directory: {ETL_LOGS_DIR}.\n"
        "Please create this directory before proceeding."
    )
    assert os.path.isdir(ETL_LOGS_DIR), (
        f"{ETL_LOGS_DIR} exists but is not a directory."
    )

    st = os.stat(ETL_LOGS_DIR)
    uid = st.st_uid
    gid = st.st_gid
    username = pwd.getpwuid(uid).pw_name
    groupname = grp.getgrgid(gid).gr_name

    assert username == 'user', (
        f"{ETL_LOGS_DIR} is owned by '{username}', but should be owned by 'user'."
    )
    # Accept any group ownership at this stage; it will be checked for consistency later.

def test_etl_logs_permissions_are_not_too_restrictive_initially():
    """
    The initial permissions must allow at least user rwx and group r-x,
    i.e., not already 700, so the student can perform the chmod task.
    """
    st = os.stat(ETL_LOGS_DIR)
    mode = stat.S_IMODE(st.st_mode)
    # Check that it's not already 0o700 (drwx------)
    assert mode != 0o700, (
        f"{ETL_LOGS_DIR} already has permissions 700 (drwx------). "
        "Permissions should be less restrictive initially (e.g., 770 or 755)."
    )
    # Must have user rwx
    assert mode & 0o700 == 0o700, (
        f"{ETL_LOGS_DIR} does not have user read/write/execute permissions."
    )

def test_permissions_check_log_does_not_exist_initially():
    """
    The permissions_check.log file should not exist before the student runs the task.
    """
    assert not os.path.exists(PERMISSIONS_CHECK_LOG), (
        f"{PERMISSIONS_CHECK_LOG} already exists. "
        "It should NOT exist before you perform the task."
    )