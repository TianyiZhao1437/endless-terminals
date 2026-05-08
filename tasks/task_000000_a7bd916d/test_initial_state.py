# test_initial_state.py

import os
import stat
import tarfile
import pytest

BACKUP_DIR = "/home/user/backup_restore_test"
TAR_PATH = os.path.join(BACKUP_DIR, "repo_backup.tar")
RESTORE_DIR = os.path.join(BACKUP_DIR, "restore_dir")
LOG_FILE = os.path.join(BACKUP_DIR, "restore_verification.log")

def test_backup_directory_exists_and_writable():
    assert os.path.isdir(BACKUP_DIR), (
        f"Required directory '{BACKUP_DIR}' does not exist. "
        f"Please create it before proceeding."
    )
    # Check writable by attempting to create and delete a temp file
    try:
        testfile = os.path.join(BACKUP_DIR, '.pytest_write_test')
        with open(testfile, 'w') as f:
            f.write('test')
        os.remove(testfile)
    except Exception:
        pytest.fail(
            f"Directory '{BACKUP_DIR}' is not writable. "
            "Ensure the agent has write permissions."
        )

def test_tar_archive_exists():
    assert os.path.isfile(TAR_PATH), (
        f"Backup archive '{TAR_PATH}' does not exist. "
        "Please ensure it is present."
    )

def test_tar_archive_has_required_contents():
    expected_top_level = {".git", "README.md", "main.py"}
    assert tarfile.is_tarfile(TAR_PATH), (
        f"File '{TAR_PATH}' is not a valid tar archive."
    )
    with tarfile.open(TAR_PATH, "r") as tar:
        top_level = set()
        for member in tar.getmembers():
            # Only consider items at top-level (no '/')
            name = member.name
            if "/" not in name.strip("/"):
                # e.g. "README.md", ".git"
                top_level.add(name.rstrip("/"))
            else:
                # For cases like ".git/config", only the first segment is top-level
                top_level.add(name.split("/", 1)[0])
        missing = expected_top_level - top_level
        extra = top_level - expected_top_level
        assert not missing, (
            f"Archive '{TAR_PATH}' is missing required items at the top level: {', '.join(sorted(missing))}."
        )
        # We tolerate extra files, but check that required ones are present

def test_restore_dir_does_not_exist_yet():
    assert not os.path.exists(RESTORE_DIR), (
        f"Restore directory '{RESTORE_DIR}' already exists before restore. "
        "Please remove it to start with a clean state."
    )

def test_restore_verification_log_does_not_exist_yet():
    assert not os.path.exists(LOG_FILE), (
        f"Log file '{LOG_FILE}' already exists before restore. "
        "Please remove it to start with a clean state."
    )