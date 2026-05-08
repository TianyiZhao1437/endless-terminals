# test_initial_state.py
import os
import pytest

ARTIFACTS_DIR = "/home/user/project/artifacts"
ARCHIVED_ZIPS_DIR = "/home/user/project/archived_zips"
ZIP_MOVE_LOG = "/home/user/project/zip_move.log"

@pytest.mark.parametrize("path", [
    ARTIFACTS_DIR,
])
def test_artifacts_dir_exists(path):
    assert os.path.isdir(path), (
        f"Required directory '{path}' does not exist. "
        f"Please ensure it exists before starting the task."
    )

def test_artifacts_dir_contents():
    expected_files = {
        "build1.zip",
        "build2.zip",
        "report.txt",
        "notes.md",
        "test.zip",
        "archive.tar.gz",
    }
    actual_files = set(os.listdir(ARTIFACTS_DIR))
    missing = expected_files - actual_files
    unexpected = actual_files - expected_files
    assert not missing, (
        f"The following files are missing from '{ARTIFACTS_DIR}': {sorted(missing)}"
    )
    assert not unexpected, (
        f"The following unexpected files are present in '{ARTIFACTS_DIR}': {sorted(unexpected)}"
    )

def test_archived_zips_dir_absent():
    assert not os.path.exists(ARCHIVED_ZIPS_DIR), (
        f"Directory '{ARCHIVED_ZIPS_DIR}' should NOT exist before the task. "
        f"Please remove it if present."
    )

def test_zip_move_log_absent():
    assert not os.path.exists(ZIP_MOVE_LOG), (
        f"Log file '{ZIP_MOVE_LOG}' should NOT exist before the task. "
        f"Please remove it if present."
    )