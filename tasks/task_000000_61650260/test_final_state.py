# test_final_state.py

import os
import pytest

ARTIFACTS_DIR = "/home/user/project/artifacts"
ARCHIVED_ZIPS_DIR = "/home/user/project/archived_zips"
ZIP_MOVE_LOG = "/home/user/project/zip_move.log"

EXPECTED_ZIP_FILES = ["build1.zip", "build2.zip", "test.zip"]
EXPECTED_NON_ZIP_FILES = ["report.txt", "notes.md", "archive.tar.gz"]

def test_archived_zips_dir_exists():
    assert os.path.isdir(ARCHIVED_ZIPS_DIR), (
        f"Directory '{ARCHIVED_ZIPS_DIR}' does not exist. "
        f"Ensure you created it and moved the ZIP files there."
    )

def test_archived_zips_dir_contents():
    actual_files = sorted(os.listdir(ARCHIVED_ZIPS_DIR))
    expected_files = sorted(EXPECTED_ZIP_FILES)
    missing = set(expected_files) - set(actual_files)
    unexpected = set(actual_files) - set(expected_files)
    assert not missing, (
        f"The following ZIP files are missing from '{ARCHIVED_ZIPS_DIR}': {sorted(missing)}"
    )
    assert not unexpected, (
        f"The following unexpected files are present in '{ARCHIVED_ZIPS_DIR}': {sorted(unexpected)}"
    )

def test_archived_zips_contains_only_files():
    for fname in os.listdir(ARCHIVED_ZIPS_DIR):
        fpath = os.path.join(ARCHIVED_ZIPS_DIR, fname)
        assert os.path.isfile(fpath), (
            f"Found a non-file entry '{fpath}' in '{ARCHIVED_ZIPS_DIR}'. "
            f"Only the expected ZIP files should be present."
        )

def test_artifacts_dir_contents_after_move():
    actual_files = sorted(os.listdir(ARTIFACTS_DIR))
    expected_files = sorted(EXPECTED_NON_ZIP_FILES)
    missing = set(expected_files) - set(actual_files)
    unexpected = set(actual_files) - set(expected_files)
    assert not missing, (
        f"The following files are missing from '{ARTIFACTS_DIR}' after moving ZIPs: {sorted(missing)}"
    )
    assert not unexpected, (
        f"The following unexpected files remain in '{ARTIFACTS_DIR}': {sorted(unexpected)}. "
        f"Only non-ZIP files should remain."
    )

def test_artifacts_dir_contains_only_non_zip_files():
    for fname in os.listdir(ARTIFACTS_DIR):
        assert not fname.endswith(".zip"), (
            f"ZIP file '{fname}' still present in '{ARTIFACTS_DIR}'. "
            f"All ZIP files should have been moved."
        )

def test_zip_move_log_exists():
    assert os.path.isfile(ZIP_MOVE_LOG), (
        f"Log file '{ZIP_MOVE_LOG}' does not exist. "
        f"Ensure you created the log file after moving the ZIP files."
    )

def test_zip_move_log_contents():
    with open(ZIP_MOVE_LOG, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    expected_lines = sorted(EXPECTED_ZIP_FILES)
    assert lines == expected_lines, (
        f"Log file '{ZIP_MOVE_LOG}' contains incorrect contents.\n"
        f"Expected (one ZIP name per line, lex order):\n"
        f"{chr(10).join(expected_lines)}\n"
        f"But got:\n"
        f"{chr(10).join(lines)}"
    )

def test_zip_move_log_no_extra_lines():
    with open(ZIP_MOVE_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        assert line.endswith('\n') or i == len(lines)-1, (
            f"Line {i+1} in '{ZIP_MOVE_LOG}' does not end with a newline character."
        )
    # Accept last line without trailing newline

def test_zip_files_not_duplicated():
    # Ensure ZIP files are not present in both locations
    artifacts_files = set(os.listdir(ARTIFACTS_DIR))
    archived_files = set(os.listdir(ARCHIVED_ZIPS_DIR))
    overlap = artifacts_files & archived_files & set(EXPECTED_ZIP_FILES)
    assert not overlap, (
        f"The following ZIP files are present in BOTH '{ARTIFACTS_DIR}' and '{ARCHIVED_ZIPS_DIR}': {sorted(overlap)}. "
        f"ZIP files should be moved, not copied."
    )