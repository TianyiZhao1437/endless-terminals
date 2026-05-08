# test_initial_state.py

import os
import pytest

CONFIG_PATH = "/home/user/project/config.ini"
EXPECTED_CONFIG = """[general]
project_name = DataCleaner
version = 1.1

[paths]
main_script = scripts/process.py
data_dir = data/input
"""

def test_config_ini_exists():
    assert os.path.isfile(CONFIG_PATH), (
        f"Required INI file is missing: {CONFIG_PATH}"
    )

def test_config_ini_contents():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        actual = f.read()
    # Normalize line endings for comparison
    expected = EXPECTED_CONFIG.replace('\r\n', '\n').replace('\r', '\n')
    actual = actual.replace('\r\n', '\n').replace('\r', '\n')
    assert actual == expected, (
        f"The file at {CONFIG_PATH} does not have the expected contents.\n"
        "Expected contents:\n"
        f"{EXPECTED_CONFIG}\n"
        "Actual contents:\n"
        f"{actual}"
    )

def test_main_script_path_txt_does_not_exist():
    target_path = "/home/user/project/main_script_path.txt"
    assert not os.path.exists(target_path), (
        f"The answer file {target_path} should NOT exist before the task is performed."
    )