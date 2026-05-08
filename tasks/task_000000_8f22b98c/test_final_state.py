# test_final_state.py

import os
import stat
import pwd
import grp
import pytest
import subprocess

BACKUP_SH = "/home/user/scripts/backup.sh"
PERMISSION_LOG = "/home/user/scripts/permission_log.txt"


def test_backup_sh_exists_and_is_file():
    assert os.path.exists(BACKUP_SH), (
        f"Expected file does not exist: {BACKUP_SH}"
    )
    assert os.path.isfile(BACKUP_SH), (
        f"Path exists but is not a file: {BACKUP_SH}"
    )


def test_backup_sh_permissions_are_700_owner_user_group_user():
    st = os.stat(BACKUP_SH)
    file_mode = stat.S_IMODE(st.st_mode)
    expected_mode = 0o700
    assert file_mode == expected_mode, (
        f"{BACKUP_SH} must have permissions 700 (-rwx------), "
        f"but has {oct(file_mode)} ({stat.filemode(st.st_mode)})"
    )
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


def test_backup_sh_no_permissions_for_group_or_others():
    st = os.stat(BACKUP_SH)
    file_mode = stat.S_IMODE(st.st_mode)
    # Only user permissions should be set; group and others must be 0
    group_perms = (file_mode & 0o070) >> 3
    others_perms = (file_mode & 0o007)
    assert group_perms == 0, (
        f"{BACKUP_SH} must have no permissions for group (---), "
        f"but has {oct(group_perms << 3)}"
    )
    assert others_perms == 0, (
        f"{BACKUP_SH} must have no permissions for others (---), "
        f"but has {oct(others_perms)}"
    )


def test_permission_log_exists_and_is_single_line():
    assert os.path.exists(PERMISSION_LOG), (
        f"{PERMISSION_LOG} does not exist. You must create it after securing the script."
    )
    assert os.path.isfile(PERMISSION_LOG), (
        f"{PERMISSION_LOG} exists but is not a file."
    )
    with open(PERMISSION_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()
    assert len(lines) == 1, (
        f"{PERMISSION_LOG} must contain exactly one line, but has {len(lines)} lines."
    )
    line = lines[0].rstrip('\n')
    assert line, f"{PERMISSION_LOG} must not be empty."


def test_permission_log_content_matches_ls_output():
    # Get actual ls -l output as 'user'
    # Try to get the 'user' UID and GID; if not found, skip test
    try:
        user_pw = pwd.getpwnam("user")
    except KeyError:
        pytest.skip("User 'user' does not exist on this system.")
    # Use subprocess to run ls -l as 'user'
    try:
        result = subprocess.run(
            ["ls", "-l", BACKUP_SH],
            check=True,
            capture_output=True,
            text=True,
            env={"LANG": "C", "LC_ALL": "C"},
            preexec_fn=lambda: os.setuid(user_pw.pw_uid) if os.geteuid() == 0 else None
        )
    except PermissionError:
        pytest.skip("Cannot switch to user 'user' to run ls -l. Skipping content match.")
    except Exception as e:
        pytest.fail(f"Failed to run ls -l as user 'user': {e}")

    ls_output = result.stdout.strip()
    with open(PERMISSION_LOG, "r", encoding="utf-8") as f:
        log_line = f.read().strip()
    assert log_line == ls_output, (
        f"Content of {PERMISSION_LOG} does not match the output of 'ls -l {BACKUP_SH}' as user 'user'.\n"
        f"Expected (from ls -l):\n{ls_output}\n"
        f"Actual (in log file):\n{log_line}\n"
        "Ensure you run 'ls -l /home/user/scripts/backup.sh' after changing permissions, "
        "and write its output as a single line to the log file."
    )