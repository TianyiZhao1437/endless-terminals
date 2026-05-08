# test_final_state.py

import os
import pytest

REPOS_DIR = "/home/user/repos"
BINARY_VERSIONS_FILE = os.path.join(REPOS_DIR, "binary_versions.txt")
SORTED_REPOS_FILE = os.path.join(REPOS_DIR, "sorted_repos.txt")

EXPECTED_SORTED_REPOS = [
    "AlphaRepo",
    "BetaRepo",
    "GammaRepo",
    "betaRepo",
    "deltaRepo",
]

@pytest.mark.describe("Final OS/FS state after extracting and sorting repository names")
def test_sorted_repos_file_exists():
    assert os.path.isfile(SORTED_REPOS_FILE), (
        f"File '{SORTED_REPOS_FILE}' does not exist. "
        "You must create this file with the sorted repository names."
    )

def test_sorted_repos_file_contents_exact():
    assert os.path.isfile(SORTED_REPOS_FILE), (
        f"File '{SORTED_REPOS_FILE}' does not exist. "
        "You must create this file with the sorted repository names."
    )
    with open(SORTED_REPOS_FILE, encoding="utf-8") as f:
        lines = f.read().splitlines()

    # Check for leading/trailing whitespace
    for i, line in enumerate(lines):
        assert line == line.strip(), (
            f"Line {i+1} in '{SORTED_REPOS_FILE}' has leading or trailing whitespace: {repr(line)}"
        )

    # Check for empty lines
    assert all(line != "" for line in lines), (
        f"File '{SORTED_REPOS_FILE}' contains empty lines. "
        "Each line must contain exactly one repository name."
    )

    assert lines == EXPECTED_SORTED_REPOS, (
        f"File '{SORTED_REPOS_FILE}' does not have the expected sorted repository names.\n"
        f"Expected lines:\n{EXPECTED_SORTED_REPOS}\n"
        f"Found lines:\n{lines}\n"
        "Ensure you extract only the repository names, sort them alphabetically (case-sensitive), "
        "and write one per line with no extra whitespace."
    )

def test_sorted_repos_file_no_extra_lines():
    with open(SORTED_REPOS_FILE, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert len(lines) == len(EXPECTED_SORTED_REPOS), (
        f"File '{SORTED_REPOS_FILE}' contains {len(lines)} lines, but {len(EXPECTED_SORTED_REPOS)} were expected. "
        "There must be exactly one line for each repository name, and no extra blank lines."
    )