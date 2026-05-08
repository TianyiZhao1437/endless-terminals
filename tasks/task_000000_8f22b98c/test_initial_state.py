# test_initial_state.py

import os
import stat
import pwd
import grp
import pytest

BACKUP_SH = "/home/user/scripts/backup.sh"
PERMISSION_LOG = "/home/user/scripts/permission_log.txt"

def test_backup_sh_exists_and_is_file():
    assert os.path.exists(BACKUP_SH), (
        f"Required file does not exist: {BACKUP_SH}"
    )
    assert os.path.isfile(BACKUP_SH), (
        f"Path exists but is not a file: {BACKUP_SH}"
    )

def test_backup_sh_is_world_writable_mode_777():
    st = os.stat(BACKUP_SH)
    file_mode = stat.S_IMODE(st.st_mode)
    expected_mode = 0o777
    assert file_mode == expected_mode, (
        f"{BACKUP_SH} must have permissions 777 (-rwxrwxrwx) before the task, "
        f"but has {oct(file_mode)} ({stat.filemode(st.st_mode)})"
    )

def test_backup_sh_owner_and_group_are_user():
    st = os.stat(BACKUP_SH)
    uid = st.st_uid
    gid = st.st_gid
    user_name = pwd.getpwuid(uid).pw_name
    group_name = grp.getgrgid(gid).gr_name
    assert user_name == "user", (
        f"{BACKUP_SH} must be owned by user 'user', but owner is '{user_name}'"
    )
    assert group_name == "user", (
        f"{BACKUP_SH} must have group 'user', but group is '{group_name}'"
    )

def test_permission_log_does_not_exist():
    assert not os.path.exists(PERMISSION_LOG), (
        f"{PERMISSION_LOG} must not exist before the task is performed."
    )