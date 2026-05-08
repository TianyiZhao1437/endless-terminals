# test_final_state.py

import os
import pytest

CONFIG_PATH = "/home/user/project/config.ini"
TARGET_PATH = "/home/user/project/main_script_path.txt"
EXPECTED_MAIN_SCRIPT_PATH = "scripts/process.py"

def test_main_script_path_txt_exists():
    assert os.path.isfile(TARGET_PATH), (
        f"The file {TARGET_PATH} does not exist. You must create this file with the extracted main_script path."
    )

def test_main_script_path_txt_contents():
    with open(TARGET_PATH, "rb") as f:
        content = f.read()
    # The file must contain exactly the expected string, with no extra newlines or spaces
    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(f"The file {TARGET_PATH} is not valid UTF-8 text.")

    assert decoded == EXPECTED_MAIN_SCRIPT_PATH, (
        f"The file {TARGET_PATH} must contain exactly the main_script value from the config, "
        f"and nothing else.\nExpected: {repr(EXPECTED_MAIN_SCRIPT_PATH)}\nActual: {repr(decoded)}"
        "\n\nCheck for extra newlines, spaces, or formatting."
    )

def test_main_script_path_txt_no_extra_bytes():
    # Ensure there are no trailing newlines or extra bytes after the expected value
    with open(TARGET_PATH, "rb") as f:
        content = f.read()
    expected_bytes = EXPECTED_MAIN_SCRIPT_PATH.encode("utf-8")
    assert content == expected_bytes, (
        f"The file {TARGET_PATH} contains extra bytes or characters. "
        "It must contain only the exact value: "
        f"{repr(EXPECTED_MAIN_SCRIPT_PATH)}"
    )

def test_config_ini_unchanged():
    # The original config.ini must not be modified
    expected = (
        "[general]\n"
        "project_name = DataCleaner\n"
        "version = 1.1\n\n"
        "[paths]\n"
        "main_script = scripts/process.py\n"
        "data_dir = data/input\n"
    )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        actual = f.read()
    # Normalize line endings
    expected = expected.replace('\r\n', '\n').replace('\r', '\n')
    actual = actual.replace('\r\n', '\n').replace('\r', '\n')
    assert actual == expected, (
        f"The file at {CONFIG_PATH} has been modified.\n"
        "Expected contents:\n"
        f"{expected}\n"
        "Actual contents:\n"
        f"{actual}"
    )