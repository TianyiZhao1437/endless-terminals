# test_initial_state.py

import os
import stat
import pytest

SCRIPTS_DIR = "/home/user/mobile-pipeline/scripts"
LOGS_DIR = "/home/user/mobile-pipeline/logs"
BUILD_SCRIPT = os.path.join(SCRIPTS_DIR, "build_v1.sh")
LEGACY_DEP_FILE = os.path.join(SCRIPTS_DIR, "legacy-dependency.txt")


def test_scripts_dir_exists():
    assert os.path.isdir(SCRIPTS_DIR), (
        f"Required directory '{SCRIPTS_DIR}' does not exist. "
        "Make sure the mobile pipeline scripts directory is present."
    )


def test_logs_dir_exists():
    assert os.path.isdir(LOGS_DIR), (
        f"Required directory '{LOGS_DIR}' does not exist. "
        "Make sure the mobile pipeline logs directory is present."
    )


def test_build_script_exists_and_executable():
    assert os.path.isfile(BUILD_SCRIPT), (
        f"Required build script '{BUILD_SCRIPT}' does not exist. "
        "Ensure the legacy build script is present before starting."
    )
    st = os.stat(BUILD_SCRIPT)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, (
        f"Build script '{BUILD_SCRIPT}' exists but is not executable by the user. "
        "Add executable permission (chmod u+x) before running the script."
    )


def test_legacy_dependency_not_present():
    assert not os.path.exists(LEGACY_DEP_FILE), (
        f"File '{LEGACY_DEP_FILE}' exists, but the initial state requires it to be missing. "
        "Remove this file before starting the task to ensure the correct error message is produced."
    )