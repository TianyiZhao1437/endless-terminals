# test_initial_state.py

import os
import shutil
import subprocess
import pytest

HOME = "/home/user"
SEC_SCAN_DIR = os.path.join(HOME, "sec_scan")
TARGETS_TXT = os.path.join(SEC_SCAN_DIR, "targets.txt")
SCAN_REPORT = os.path.join(SEC_SCAN_DIR, "scan_report.log")

def test_nmap_installed():
    """nmap must be installed and available in $PATH before starting the task."""
    nmap_path = shutil.which("nmap")
    assert nmap_path is not None, (
        "nmap is not installed or not found in $PATH. Please install nmap before starting the task."
    )
    # Optionally, check executable
    assert os.access(nmap_path, os.X_OK), (
        f"nmap found at {nmap_path} but is not executable."
    )

def test_home_directory_exists_and_writable():
    """The /home/user directory must exist and be writable."""
    assert os.path.isdir(HOME), (
        f"Required home directory '{HOME}' does not exist."
    )
    assert os.access(HOME, os.W_OK), (
        f"Home directory '{HOME}' is not writable."
    )

def test_sec_scan_directory_does_not_exist_yet():
    """The /home/user/sec_scan directory must NOT exist before the task."""
    assert not os.path.exists(SEC_SCAN_DIR), (
        f"Directory '{SEC_SCAN_DIR}' already exists before the task. It should not pre-exist."
    )

def test_targets_txt_does_not_exist():
    """The /home/user/sec_scan/targets.txt file must NOT exist before the task."""
    assert not os.path.exists(TARGETS_TXT), (
        f"File '{TARGETS_TXT}' already exists before the task. It should not pre-exist."
    )

def test_scan_report_log_does_not_exist():
    """The /home/user/sec_scan/scan_report.log file must NOT exist before the task."""
    assert not os.path.exists(SCAN_REPORT), (
        f"File '{SCAN_REPORT}' already exists before the task. It should not pre-exist."
    )