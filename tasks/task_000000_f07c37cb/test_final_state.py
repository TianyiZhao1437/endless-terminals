# test_final_state.py

import os
import stat
import pytest

MONITORING_DIR = "/home/user/monitoring"
VENV_DIR = os.path.join(MONITORING_DIR, "alertenv")
LOG_FILE = os.path.join(MONITORING_DIR, "env_creation.log")
EXPECTED_LOG_LINES = ["alertenv", "env_creation.log"]

def test_monitoring_directory_exists_and_is_dir():
    assert os.path.exists(MONITORING_DIR), (
        f"Expected directory '{MONITORING_DIR}' to exist, but it does not."
    )
    assert os.path.isdir(MONITORING_DIR), (
        f"'{MONITORING_DIR}' exists but is not a directory."
    )

def test_monitoring_directory_contents_exact():
    contents = sorted(os.listdir(MONITORING_DIR))
    expected = sorted(EXPECTED_LOG_LINES)
    assert contents == expected, (
        f"Expected '{MONITORING_DIR}' to contain only {expected}, but found: {contents}. "
        "Remove any extra files or directories, and ensure both 'alertenv' and 'env_creation.log' are present."
    )

def test_venv_directory_exists_and_is_dir():
    assert os.path.exists(VENV_DIR), (
        f"Expected Python virtual environment directory '{VENV_DIR}' to exist, but it does not."
    )
    assert os.path.isdir(VENV_DIR), (
        f"'{VENV_DIR}' exists but is not a directory."
    )

def test_venv_has_expected_structure():
    """
    The venv directory should have at least:
      - 'bin' (or 'Scripts' on Windows, but we expect 'bin' on Linux),
      - 'lib' (should exist),
      - 'pyvenv.cfg' file.
    """
    entries = set(os.listdir(VENV_DIR))
    missing = []
    # bin directory
    if "bin" not in entries:
        missing.append("bin/")
    # lib directory (may be 'lib' or 'lib64' depending on the system, but 'lib' is standard)
    if not any(name.startswith("lib") and os.path.isdir(os.path.join(VENV_DIR, name)) for name in entries):
        missing.append("lib/ (or lib64/)")
    # pyvenv.cfg file
    if "pyvenv.cfg" not in entries or not os.path.isfile(os.path.join(VENV_DIR, "pyvenv.cfg")):
        missing.append("pyvenv.cfg")
    assert not missing, (
        f"The virtual environment directory '{VENV_DIR}' is missing required items: {missing}. "
        "Ensure it is a valid Python venv created with the 'venv' module."
    )

def test_venv_pyvenv_cfg_is_valid():
    cfg_path = os.path.join(VENV_DIR, "pyvenv.cfg")
    assert os.path.isfile(cfg_path), (
        f"Expected 'pyvenv.cfg' file in '{VENV_DIR}', but it is missing."
    )
    # Basic sanity check: file is not empty and contains the word 'venv'
    with open(cfg_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "venv" in content.lower(), (
        f"'pyvenv.cfg' in '{VENV_DIR}' does not appear to contain valid venv configuration."
    )

def test_env_creation_log_exists_and_is_file():
    assert os.path.exists(LOG_FILE), (
        f"Expected log file '{LOG_FILE}' to exist, but it does not."
    )
    assert os.path.isfile(LOG_FILE), (
        f"'{LOG_FILE}' exists but is not a regular file."
    )

def test_env_creation_log_contents_exact():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines == EXPECTED_LOG_LINES, (
        f"'{LOG_FILE}' contents are incorrect.\n"
        f"Expected exactly:\n"
        f"alertenv\n"
        f"env_creation.log\n"
        f"But got:\n"
        f"{chr(10).join(lines)}\n"
        "Ensure the file contains only the names of 'alertenv' and 'env_creation.log', one per line, "
        "with no extra whitespace or metadata."
    )

def test_no_extra_files_or_dirs():
    """
    Ensure no extra files or directories are present in /home/user/monitoring.
    """
    allowed = set(EXPECTED_LOG_LINES)
    actual = set(os.listdir(MONITORING_DIR))
    extra = actual - allowed
    assert not extra, (
        f"Found unexpected files or directories in '{MONITORING_DIR}': {sorted(extra)}. "
        "Only 'alertenv' and 'env_creation.log' should be present."
    )