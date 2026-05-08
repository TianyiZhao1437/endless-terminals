# test_initial_state.py

import os
import tarfile
import pytest

BACKUP_DATA_DIR = "/home/user/backup_data"
BACKUP_ARCHIVE = "/home/user/backup_data/sample_backup.tar.gz"
RESTORE_TEST_DIR = "/home/user/restore_test"

def test_backup_data_dir_exists():
    assert os.path.isdir(BACKUP_DATA_DIR), (
        f"Required directory '{BACKUP_DATA_DIR}' does not exist."
    )

def test_backup_archive_exists():
    assert os.path.isfile(BACKUP_ARCHIVE), (
        f"Backup archive '{BACKUP_ARCHIVE}' does not exist in '{BACKUP_DATA_DIR}'."
    )

def test_backup_archive_contents():
    """
    The archive sample_backup.tar.gz contains:
      - project_docs/ (directory)
        - README.txt (file, contents: "This is a README for the project.\n")
        - instructions.txt (file, contents: "Follow these steps to restore your files.\n")
    """
    assert tarfile.is_tarfile(BACKUP_ARCHIVE), (
        f"File '{BACKUP_ARCHIVE}' is not a valid tar archive."
    )
    with tarfile.open(BACKUP_ARCHIVE, "r:gz") as tf:
        names = tf.getnames()
        expected_dir = "project_docs"
        expected_files = [
            "project_docs/README.txt",
            "project_docs/instructions.txt",
        ]
        # Check for the directory
        assert any(n.rstrip("/") == expected_dir for n in names), (
            f"'project_docs/' directory is missing in the archive '{BACKUP_ARCHIVE}'."
        )
        # Check for files
        for fname in expected_files:
            assert fname in names, (
                f"File '{fname}' is missing from the archive '{BACKUP_ARCHIVE}'."
            )
        # Check file contents
        contents_expect = {
            "project_docs/README.txt": "This is a README for the project.\n",
            "project_docs/instructions.txt": "Follow these steps to restore your files.\n",
        }
        for member in tf.getmembers():
            if member.name in contents_expect:
                extracted = tf.extractfile(member)
                assert extracted is not None, (
                    f"Could not extract file '{member.name}' from the archive."
                )
                content = extracted.read().decode("utf-8")
                assert content == contents_expect[member.name], (
                    f"Content of '{member.name}' in archive does not match expected.\n"
                    f"Expected:\n{contents_expect[member.name]!r}\n"
                    f"Found:\n{content!r}"
                )

def test_restore_test_dir_exists_and_empty():
    assert os.path.isdir(RESTORE_TEST_DIR), (
        f"Required directory '{RESTORE_TEST_DIR}' does not exist."
    )
    contents = os.listdir(RESTORE_TEST_DIR)
    assert contents == [] or contents == ['.'] or contents == ['..'], (
        f"Directory '{RESTORE_TEST_DIR}' is not empty: contains {contents}. "
        "It should be empty before extraction."
    )