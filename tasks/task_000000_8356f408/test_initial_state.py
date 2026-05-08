# test_initial_state.py

import os
import pytest
import pwd
import stat

ID_RSA_PATH = '/home/user/test-environment/id_rsa'
EXPECTED_PERMS = 0o644  # Should be octal 0644 before the fix
EXPECTED_OWNER = 'user'

@pytest.mark.parametrize("path", [ID_RSA_PATH])
def test_id_rsa_exists(path):
    assert os.path.isfile(path), (
        f"Missing file: {path}. "
        "The private SSH key file must exist before starting the task."
    )

def test_id_rsa_permissions():
    st = os.stat(ID_RSA_PATH)
    actual_perms = stat.S_IMODE(st.st_mode)
    assert actual_perms == EXPECTED_PERMS, (
        f"Incorrect permissions for {ID_RSA_PATH}: "
        f"expected 0644 (owner read/write, group/world read), found {oct(actual_perms)[2:].zfill(4)}. "
        "Set permissions to 0644 before starting the task."
    )

def test_id_rsa_owner():
    st = os.stat(ID_RSA_PATH)
    actual_uid = st.st_uid
    actual_owner = pwd.getpwuid(actual_uid).pw_name
    assert actual_owner == EXPECTED_OWNER, (
        f"{ID_RSA_PATH} must be owned by '{EXPECTED_OWNER}' before starting the task, "
        f"but owner is '{actual_owner}'."
    )

@pytest.mark.parametrize("path", ['/home/user/fix_permissions.log'])
def test_fix_permissions_log_absent(path):
    assert not os.path.exists(path), (
        f"The log file {path} should NOT exist before the task begins."
    )