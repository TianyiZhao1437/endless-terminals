# test_final_state.py
"""
Pytest suite to validate the FINAL OS and filesystem state
for the "securely transfer processed CSV files to a remote server using SSH key-based authentication" task.

Checks:
- SSH keypair and public key copy exist, correct permissions, correct keytype/comment, and fingerprint.
- Extracted CSV file contains only intended rows.
- Log file format and values as described.
- No modification/removal of original files.

Author: Senior Python Engineer
"""

import os
import stat
import pytest
import subprocess

HOME = "/home/user"
CSV_DIR = f"{HOME}/csv_files"
RAW_CSV = f"{CSV_DIR}/data_raw.csv"
SUCCESS_CSV = f"{CSV_DIR}/data_success.csv"
TRANSFER_LOG = f"{CSV_DIR}/transfer.log"

SSH_DIR = f"{HOME}/.ssh"
KEY_PRIVATE = f"{SSH_DIR}/data_transfer_ed25519"
KEY_PUBLIC = f"{SSH_DIR}/data_transfer_ed25519.pub"

PUBKEY_COPY_DIR = f"{HOME}/ssh_public_keys"
PUBKEY_COPY = f"{PUBKEY_COPY_DIR}/data_transfer_ed25519.pub"

# Expected CSV output
EXPECTED_SUCCESS_CSV = [
    "id,name,status\n",
    "1,Alice,SUCCESS\n",
    "3,Charlie,SUCCESS\n",
    "5,Eve,SUCCESS\n",
]

# Expected public key comment
EXPECTED_KEY_COMMENT = "data-analyst"

# Permissions
PERM_PRIVATE = 0o600
PERM_PUBLIC = 0o644

def _file_perm(path):
    return stat.S_IMODE(os.stat(path).st_mode)

def _readlines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def _read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def _get_fingerprint(key_path):
    # Returns the fingerprint line (like: "256 SHA256:xxxxxx data-analyst")
    result = subprocess.run(
        ["ssh-keygen", "-lf", key_path],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        pytest.fail(
            f"Failed to get fingerprint for {key_path}.\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
    # line: "256 SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx data-analyst"
    line = result.stdout.strip()
    return line

def _get_pubkey_content(path):
    return _read(path).strip()

@pytest.mark.parametrize("path", [
    KEY_PRIVATE,
    KEY_PUBLIC,
    PUBKEY_COPY,
])
def test_key_files_exist(path):
    assert os.path.isfile(path), (
        f"Missing required SSH key file: {path}\n"
        f"Did you generate the SSH keypair and save the public key copy?"
    )

def test_private_key_permissions():
    perm = _file_perm(KEY_PRIVATE)
    assert perm == PERM_PRIVATE, (
        f"SSH private key permissions are incorrect: {KEY_PRIVATE} (got {oct(perm)})\n"
        f"Should be 0o600 (owner read/write only)."
    )

def test_public_key_permissions():
    perm = _file_perm(KEY_PUBLIC)
    assert perm == PERM_PUBLIC, (
        f"SSH public key permissions are incorrect: {KEY_PUBLIC} (got {oct(perm)})\n"
        f"Should be 0o644 (owner read/write, others read)."
    )

def test_pubkey_copy_permissions():
    perm = _file_perm(PUBKEY_COPY)
    assert perm == PERM_PUBLIC, (
        f"Copied SSH public key permissions are incorrect: {PUBKEY_COPY} (got {oct(perm)})\n"
        f"Should be 0o644 (owner read/write, others read)."
    )

def test_private_key_type_and_no_passphrase():
    # Check key type (ed25519) and no passphrase
    result = subprocess.run(
        ["ssh-keygen", "-y", "-f", KEY_PRIVATE],
        capture_output=True, text=True
    )
    assert result.returncode == 0, (
        f"Could not extract public key from private key (likely passphrase set or wrong format):\n"
        f"stderr: {result.stderr}"
    )
    pub_from_priv = result.stdout.strip()
    pub_actual = _get_pubkey_content(KEY_PUBLIC)
    assert pub_from_priv == pub_actual, (
        f"SSH private key is not valid or does not match the public key.\n"
        f"Public key from private: {pub_from_priv}\n"
        f"Actual public: {pub_actual}"
    )
    # Check key type - ed25519
    fingerprint_line = _get_fingerprint(KEY_PRIVATE)
    assert "ED25519"