# test_final_state.py

import os
import pytest

RESTORE_TEST_DIR = "/home/user/restore_test"
PROJECT_DOCS_DIR = "/home/user/restore_test/project_docs"
README_PATH = "/home/user/restore_test/project_docs/README.txt"
INSTRUCTIONS_PATH = "/home/user/restore_test/project_docs/instructions.txt"
RESTORE_LOG_PATH = "/home/user/restore_test/restore_log.txt"

README_EXPECTED_CONTENT = "This is a README for the project.\n"
INSTRUCTIONS_EXPECTED_CONTENT = "Follow these steps to restore your files.\n"
RESTORE_LOG_EXPECTED_CONTENT = (
    "Restored files:\n"
    f"{README_PATH}\n"
    f"{INSTRUCTIONS_PATH}\n"
)

def test_project_docs_directory_exists():
    assert os.path.isdir(PROJECT_DOCS_DIR), (
        f"Directory '{PROJECT_DOCS_DIR}' does not exist after restore. "
        "The backup should have extracted the 'project_docs' directory."
    )

def test_readme_txt_exists_and_content():
    assert os.path.isfile(README_PATH), (
        f"File '{README_PATH}' does not exist after restore."
    )
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == README_EXPECTED_CONTENT, (
        f"Contents of '{README_PATH}' do not match expected.\n"
        f"Expected:\n{README_EXPECTED_CONTENT!r}\n"
        f"Found:\n{content!r}"
    )

def test_instructions_txt_exists_and_content():
    assert os.path.isfile(INSTRUCTIONS_PATH), (
        f"File '{INSTRUCTIONS_PATH}' does not exist after restore."
    )
    with open(INSTRUCTIONS_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == INSTRUCTIONS_EXPECTED_CONTENT, (
        f"Contents of '{INSTRUCTIONS_PATH}' do not match expected.\n"
        f"Expected:\n{INSTRUCTIONS_EXPECTED_CONTENT!r}\n"
        f"Found:\n{content!r}"
    )

def test_restore_log_exists_and_content():
    assert os.path.isfile(RESTORE_LOG_PATH), (
        f"Log file '{RESTORE_LOG_PATH}' does not exist after restore."
    )
    with open(RESTORE_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert content == RESTORE_LOG_EXPECTED_CONTENT, (
        f"Contents of '{RESTORE_LOG_PATH}' do not match expected.\n"
        f"Expected:\n{RESTORE_LOG_EXPECTED_CONTENT!r}\n"
        f"Found:\n{content!r}"
    )

def test_restore_test_dir_only_contains_expected():
    """
    After restore, /home/user/restore_test must only contain:
      - project_docs/ (directory)
      - restore_log.txt (file)
    """
    expected_entries = {"project_docs", "restore_log.txt"}
    actual_entries = set(os.listdir(RESTORE_TEST_DIR))
    missing = expected_entries - actual_entries
    extra = actual_entries - expected_entries
    assert not missing, (
        f"Missing expected entries in '{RESTORE_TEST_DIR}': {missing}. "
        "Only 'project_docs' and 'restore_log.txt' should exist."
    )
    assert not extra, (
        f"Unexpected extra entries in '{RESTORE_TEST_DIR}': {extra}. "
        "Only 'project_docs' and 'restore_log.txt' should exist."
    )

def test_project_docs_dir_only_contains_expected_files():
    """
    /home/user/restore_test/project_docs must only contain:
      - README.txt
      - instructions.txt
    """
    expected_files = {"README.txt", "instructions.txt"}
    actual_files = set(os.listdir(PROJECT_DOCS_DIR))
    missing = expected_files - actual_files
    extra = actual_files - expected_files
    assert not missing, (
        f"Missing expected files in '{PROJECT_DOCS_DIR}': {missing}. "
        "Only 'README.txt' and 'instructions.txt' should exist."
    )
    assert not extra, (
        f"Unexpected extra files in '{PROJECT_DOCS_DIR}': {extra}. "
        "Only 'README.txt' and 'instructions.txt' should exist."
    )