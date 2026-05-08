# test_final_state.py

import os
import pytest
import tarfile

HOME = "/home/user"
PROJECTS = os.path.join(HOME, "projects")
ARCHIVES = os.path.join(HOME, "archives")

# Source directories and files
alpha_dir = os.path.join(PROJECTS, "alpha_data")
beta_dir = os.path.join(PROJECTS, "beta_data")
alpha_file = os.path.join(alpha_dir, "file_a.txt")
alpha_config = os.path.join(alpha_dir, "config_a.yaml")
beta_file = os.path.join(beta_dir, "file_b.txt")
beta_config = os.path.join(beta_dir, "config_b.yaml")

# Backup archives
alpha_archive = os.path.join(ARCHIVES, "alpha_data_backup_2024-06-20.tar.gz")
beta_archive = os.path.join(ARCHIVES, "beta_data_backup_2024-06-20.tar.gz")
verification_log = os.path.join(ARCHIVES, "backup_verification_2024-06-20.log")

def read_file(path):
    with open(path, "r") as f:
        return f.read().strip()

def read_log_lines(path):
    with open(path, "r") as f:
        return f.read().splitlines()

def get_tar_contents(tar_path):
    """Returns set of top-level file names inside the tar.gz archive."""
    with tarfile.open(tar_path, "r:gz") as tar:
        return set(member.name for member in tar.getmembers() if member.isfile())

def get_tar_file_content(tar_path, file_name):
    """Returns the content of a file inside a tar.gz archive."""
    with tarfile.open(tar_path, "r:gz") as tar:
        f = tar.extractfile(file_name)
        if f is None:
            return None
        return f.read().decode("utf-8").strip()

@pytest.mark.parametrize("archive_path,expected_files", [
    (alpha_archive, {"file_a.txt", "config_a.yaml"}),
    (beta_archive, {"file_b.txt", "config_b.yaml"}),
])
def test_archive_exists_and_contents_correct(archive_path, expected_files):
    assert os.path.isfile(archive_path), (
        f"Archive file missing: {archive_path}"
    )

    actual_files = get_tar_contents(archive_path)
    assert actual_files == expected_files, (
        f"Archive {archive_path} contents incorrect.\n"
        f"Expected files: {sorted(expected_files)}\n"
        f"Found files: {sorted(actual_files)}"
    )

@pytest.mark.parametrize("archive_path,source_dir,files_expected", [
    (alpha_archive, alpha_dir, {
        "file_a.txt": "Alpha file content",
        "config_a.yaml": "alpha: config"
    }),
    (beta_archive, beta_dir, {
        "file_b.txt": "Beta file content",
        "config_b.yaml": "beta: config"
    }),
])
def test_archive_file_contents_match_source(archive_path, source_dir, files_expected):
    for fname, expected_content in files_expected.items():
        tar_content = get_tar_file_content(archive_path, fname)
        assert tar_content == expected_content, (
            f"Archive {archive_path} has incorrect content for {fname}.\n"
            f"Expected: '{expected_content}'\n"
            f"Found: '{tar_content}'"
        )

def test_verification_log_exists():
    assert os.path.isfile(verification_log), (
        f"Verification log file missing: {verification_log}"
    )

def test_verification_log_format_and_success():
    expected_log = (
        "Verification results for alpha_data_backup_2024-06-20.tar.gz:\n"
        "Success: Archive matches source directory.\n"
        "========\n"
        "Verification results for beta_data_backup_2024-06-20.tar.gz:\n"
        "Success: Archive matches source directory.\n"
        "========\n"
    )
    actual_log = read_file(verification_log)
    assert actual_log == expected_log.strip(), (
        f"Verification log file {verification_log} does not match expected format/content.\n"
        f"Expected:\n{expected_log}\n"
        f"Found:\n{actual_log}\n"
        "If there was an error, the log should contain the exact tar error output."
    )