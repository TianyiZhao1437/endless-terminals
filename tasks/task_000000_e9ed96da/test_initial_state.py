# test_initial_state.py

import os
import stat
import pytest

REPOS_DIR = "/home/user/repos"
BINARY_VERSIONS_FILE = os.path.join(REPOS_DIR, "binary_versions.txt")

@pytest.mark.describe("Initial OS/FS state")
def test_repos_directory_exists_and_writable():
    assert os.path.isdir(REPOS_DIR), (
        f"Required directory '{REPOS_DIR}' does not exist. "
        "Please ensure the directory is present before starting."
    )
    # Check writability by user
    mode = os.stat(REPOS_DIR).st_mode
    is_writable = bool(mode & stat.S_IWUSR)
    assert is_writable, (
        f"Directory '{REPOS_DIR}' exists but is not writable by the agent (user). "
        "Please set correct permissions."
    )

def test_binary_versions_file_exists():
    assert os.path.isfile(BINARY_VERSIONS_FILE), (
        f"Required file '{BINARY_VERSIONS_FILE}' does not exist. "
        "Please ensure the file is present before starting."
    )

def test_binary_versions_file_contents():
    expected_lines = [
        "AlphaRepo 1.0.0",
        "betaRepo 2.3.1",
        "GammaRepo 0.9.6",
        "deltaRepo 3.2.0",
        "BetaRepo 2.2.2",
    ]
    with open(BINARY_VERSIONS_FILE, encoding="utf-8") as f:
        contents = f.read().splitlines()
    assert contents == expected_lines, (
        f"File '{BINARY_VERSIONS_FILE}' does not have the expected contents.\n"
        f"Expected lines:\n{expected_lines}\n"
        f"Found lines:\n{contents}"
    )