# test_final_state.py

import os
import pytest
import pwd
import stat

ID_RSA_PATH = '/home/user/test-environment/id_rsa'
FIX_LOG_PATH = '/home/user/fix_permissions.log'
EXPECTED_PERMS = 0o600  # Should be octal 0600 after the fix
EXPECTED_OWNER = 'user'
EXPECTED_GROUP = 'user'
EXPECTED_LOG_LINE = 'id_rsa permissions: 0600'


def test_id_rsa_exists():
    assert os.path.isfile(ID_RSA_PATH), (
        f"Missing file: {ID_RSA_PATH}. "
        "The private SSH key file must exist after completing the task."
    )


def test_id_rsa_permissions():
    st = os.stat(ID_RSA_PATH)
    actual_perms = stat.S_IMODE(st.st_mode)
    assert actual_perms == EXPECTED_PERMS, (
        f"Incorrect permissions for {ID_RSA_PATH}: "
        f"expected 0600 (owner read/write only), found {oct(actual_perms)[2:].zfill(4)}. "
        "Set permissions to 0600 so only the owner can read/write the file."
    )


def test_id_rsa_owner_and_group():
    st = os.stat(ID_RSA_PATH)
    actual_uid = st.st_uid
    actual_gid = st.st_gid
    actual_owner = pwd.getpwuid(actual_uid).pw_name
    actual_group = pwd.getpwuid(actual_gid).pw_name
    assert actual_owner == EXPECTED_OWNER, (
        f"{ID_RSA_PATH} must be owned by '{EXPECTED_OWNER}' after completing the task, "
        f"but owner is '{actual_owner}'."
    )
    assert actual_group == EXPECTED_GROUP, (
        f"{ID_RSA_PATH} must have group '{EXPECTED_GROUP}' after completing the task, "
        f"but group is '{actual_group}'."
    )


def test_fix_permissions_log_exists():
    assert os.path.isfile(FIX_LOG_PATH), (
        f"Missing log file: {FIX_LOG_PATH}. "
        "The verification log must exist after completing the task."
    )


def test_fix_permissions_log_content():
    with open(FIX_LOG_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 1, (
        f"{FIX_LOG_PATH} must contain exactly one line, but found {len(lines)} lines."
    )

    # Remove any trailing newline or whitespace for exact match
    log_line = lines[0].rstrip('\r\n')
    assert log_line == EXPECTED_LOG_LINE, (
        f"{FIX_LOG_PATH} must contain exactly:\n"
        f"    {EXPECTED_LOG_LINE}\n"
        f"but found:\n"
        f"    {log_line}\n"
        "Check for extra whitespace, incorrect permissions value, or additional content."
    )


def test_fix_permissions_log_no_extra_content():
    with open(FIX_LOG_PATH, 'rb') as f:
        content = f.read()
    # The log file must not contain trailing whitespace or extra newlines
    expected_bytes = (EXPECTED_LOG_LINE + '\n').encode('utf-8')
    assert content == expected_bytes, (
        f"{FIX_LOG_PATH} must contain only the single line '{EXPECTED_LOG_LINE}' followed by a single newline. "
        "Do not include extra blank lines, spaces, or headers."
    )