# test_final_state.py

import os
import pytest

SHADOW_PATH = "/etc/shadow"
AUDIT_LOG_PATH = "/home/user/audit_empty_pw.log"

def _get_empty_password_users():
    """
    Parse /etc/shadow and return a list of usernames with empty password hash fields.
    """
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

@pytest.mark.skipif(not os.path.exists(SHADOW_PATH), reason="/etc/shadow does not exist on this system.")
def test_audit_log_exists():
    """Check that the audit log file exists after the task is completed."""
    assert os.path.isfile(AUDIT_LOG_PATH), (
        f"Audit log file {AUDIT_LOG_PATH} does not exist after the task; it must be created."
    )

@pytest.mark.skipif(not os.path.exists(SHADOW_PATH), reason="/etc/shadow does not exist on this system.")
def test_audit_log_content_is_correct():
    """
    Validate the exact contents of /home/user/audit_empty_pw.log:
    - If there are any users with empty password hashes, log contains only their usernames, one per line.
    - If none, log contains only 'NONE'.
    - No extra spaces, blank lines, or extra text.
    """
    users_with_empty_pw = _get_empty_password_users()
    try:
        with open(AUDIT_LOG_PATH, "r") as f:
            lines = f.readlines()
    except Exception as e:
        pytest.fail(f"Could not read audit log file {AUDIT_LOG_PATH}: {e}")

    # Remove trailing newline characters for comparison
    stripped_lines = [line.rstrip("\n") for line in lines]

    if users_with_empty_pw:
        # There must be exactly one line per user, matching the usernames found.
        expected_lines = users_with_empty_pw
        assert stripped_lines == expected_lines, (
            f"Audit log contents are incorrect.\n"
            f"Expected exactly the following usernames, one per line:\n"
            f"{expected_lines}\n"
            f"Actual contents:\n"
            f"{stripped_lines}\n"
            f"- No extra spaces, blank lines, or text are allowed.\n"
        )
    else:
        # There must be exactly one line: 'NONE'
        assert stripped_lines == ["NONE"], (
            f"Audit log must contain only the line 'NONE' when no users with empty passwords exist.\n"
            f"Actual contents:\n"
            f"{stripped_lines}\n"
            f"- No extra spaces, blank lines, or text are allowed.\n"
        )

@pytest.mark.skipif(not os.path.exists(AUDIT_LOG_PATH), reason="Audit log file does not exist.")
def test_audit_log_format_strict():
    """
    Ensure the log file contains no extra spaces, blank lines, or extra text.
    """
    with open(AUDIT_LOG_PATH, "r") as f:
        raw = f.read()
    # Check for trailing spaces or blank lines
    lines = raw.splitlines()
    for idx, line in enumerate(lines):
        assert line == line.strip(), (
            f"Line {idx+1} in {AUDIT_LOG_PATH} has leading/trailing whitespace: {repr(line)}"
        )
    # No blank lines allowed
    assert all(line != "" for line in lines), (
        f"{AUDIT_LOG_PATH} contains blank lines; only usernames or 'NONE' are allowed, one per line."
    )
    # File must not end with an extra newline (last line must be text)
    if lines:
        assert raw.endswith(lines[-1]), (
            f"{AUDIT_LOG_PATH} ends with an extra newline; last line must be text only."
        )