# test_initial_state.py

import os
import pytest

SHADOW_PATH = "/etc/shadow"
AUDIT_LOG_PATH = "/home/user/audit_empty_pw.log"

@pytest.mark.skipif(not os.path.exists(SHADOW_PATH), reason="/etc/shadow does not exist on this system.")
def test_shadow_file_exists_and_readable():
    """Check that /etc/shadow exists and is readable."""
    assert os.path.isfile(SHADOW_PATH), (
        f"Required file {SHADOW_PATH} does not exist or is not a regular file."
    )
    try:
        with open(SHADOW_PATH, "r"):
            pass
    except PermissionError:
        pytest.skip(f"Cannot read {SHADOW_PATH} due to permissions. Run as root or with proper access.")
    except Exception as e:
        pytest.fail(f"Unexpected error reading {SHADOW_PATH}: {e}")

def _get_empty_password_users():
    """Parse /etc/shadow and return a list of usernames with empty password hash fields."""
    users_with_empty_pw = []
    try:
        with open(SHADOW_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue  # skip blank/comment lines
                fields = line.split(":")
                if len(fields) < 2:
                    continue  # skip malformed lines
                username, pw_hash = fields[0], fields[1]
                if pw_hash == "":
                    users_with_empty_pw.append(username)
    except Exception as e:
        pytest.fail(f"Error parsing {SHADOW_PATH}: {e}")
    return users_with_empty_pw

def test_at_least_one_user_with_empty_password():
    """There must be at least one user account with an empty password hash field in /etc/shadow."""
    users_with_empty_pw = _get_empty_password_users()
    assert users_with_empty_pw, (
        f"No user accounts with empty password hashes found in {SHADOW_PATH}. "
        "There must be at least one (e.g., 'testuser::...')."
    )

def test_audit_log_does_not_exist_yet():
    """Ensure /home/user/audit_empty_pw.log does NOT exist before the task is performed."""
    assert not os.path.exists(AUDIT_LOG_PATH), (
        f"The file {AUDIT_LOG_PATH} should NOT exist before you perform the task."
    )